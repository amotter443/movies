#Load Requisite Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from sklearn.utils import _to_object_array
pd.options.mode.chained_assignment = None  # default='warn'

#Read in data
df = pd.read_csv(r'\lb_tmdb.csv')

#Read in secondary LB sources
ratings = pd.read_csv(r'\ratings.csv')
reviews = pd.read_csv(r'\reviews.csv')
diary = pd.read_csv(r'\diary.csv')

###############  DIARY SECTION ###############

#Initialize Count column 
diary['watch_count'] = 1

for i in range (0,len(diary)):
    #Make an array of the titles so far
    titles = diary['Name'][:i]
    #Get counts of the array and store in dictionary
    titles_counts = titles.value_counts().to_dict()
    if diary['Name'][i] not in titles_counts and diary['Rewatch'][i]=='Yes':
        diary['watch_count'][i] = 2

#Group by title
diary = diary.groupby(['Name']).sum()
diary = diary.sort_values(by='watch_count', ascending=False).reset_index()
diary = diary[['Name','watch_count']]

#Add into main df, create total minutes of that film watched
df = df.merge(diary, on=['Name'],  how='left')
df['watch_count'] = np.where(df['watch_count'].isnull(),1,df['watch_count'])
df['min_watched'] = df['watch_count'] * df['runtime']

#Ratings and Revews join on Name and Date
df = df.merge(ratings, on=['Date', 'Name'],  how='left')
df.drop(['Year_y','Letterboxd URI'], axis=1, inplace=True)
df = df.merge(reviews, on=['Date', 'Name'],  how='left')
df.drop(['Rating_y','Letterboxd URI','Year','Rewatch','Tags','Watched Date'], axis=1, inplace=True)


#Delete secondary dfs
del ratings, reviews, diary

#Drop the _x suffix
df = df.rename(columns = lambda v: re.sub('_x','',v))
#If rating is na fill it with 0, else keep
df['Rating'] = np.where(df['Rating'].isna(),0,df['Rating'])
#Review if there is something 1 else 0
df['Review'] = np.where(df['Review'].notna(),1,0)

#Filter out where id == 0 for tv shows/movies with no match in the database
df = df[df['id']!=0]


###############  DATE SECTION ###############

#Rename Date to Logged_Date
df.rename(columns={'Date':'Logged_Date'}, inplace=True)

#Augmenting Logged Date Values
df['Logged_DOW'] = pd.to_datetime(df['Logged_Date'], format='%Y-%m-%d').dt.weekday
df['Logged_DOW'] = df['Logged_DOW'] + 1
df['Logged_Month'] = pd.to_datetime(df['Logged_Date'], format='%Y-%m-%d').dt.month
df['Logged_Year'] = pd.to_datetime(df['Logged_Date'], format='%Y-%m-%d').dt.year
df['Logged_Week'] = pd.to_datetime(df['Logged_Date'], format='%Y-%m-%d').dt.isocalendar().week

#Group by date and count/sum ID values 
temp = df.groupby('Logged_Date')['id'].aggregate(['count',sum])
temp.reset_index(level=0, inplace=True)

#How many movies I watched that day
df = df.merge(temp, on='Logged_Date', how='left')
df.drop('sum', axis=1, inplace=True)
df.rename(columns={'count': 'Daily_Movie_Count'}, inplace=True)


#Group by year/week and aggregate to count and sum ID values
temp = df.groupby(['Logged_Year','Logged_Week'])['id'].aggregate(['count',sum])
temp.reset_index(level=0, inplace=True)
temp.reset_index(level=0, inplace=True)

#How many movies I watched that week 
df = df.merge(temp, on=['Logged_Year', 'Logged_Week'],  how='left')
df.drop('sum', axis=1, inplace=True)
df.rename(columns={'count': 'Weekly_Movie_Count'}, inplace=True)


###############  GENRE SECTION ###############

#Remove TV Movie and Family Genres
df.genres = df.genres.str.replace('{\'id\': 10751, \'name\': \'Family\'},','')
df.genres = df.genres.str.replace('{\'id\': 10770, \'name\': \'TV Movie\'},','')
df.genres = df.genres.str.replace('{\'id\': 10751, \'name\': \'Family\'}','')
df.genres = df.genres.str.replace('{\'id\': 10770, \'name\': \'TV Movie\'}','')


#Remove extra charecters from genre strings 
df['genres'].replace(to_replace='[0-9]+', value='',inplace=True,regex=True)
df['genres'].replace(to_replace='\{\'id\'\: \, \'name\'\:', value='',inplace=True,regex=True)
df['genres'].replace(to_replace='\}', value='',inplace=True,regex=True)
df['genres'].replace(to_replace=' ', value='',inplace=True,regex=True)
df['genres'].replace(to_replace='\,\]', value=']',inplace=True,regex=True)

#If no genre, replace with 'none'
df['genres'] = np.where(df['genres']=='[]','[none]',df['genres'])


#Get a list of all the unique genres
vals = pd.Series(df['genres']).tolist()
vals = str(vals)
vals = vals.replace('\"','')
vals = vals.replace('\'','')
vals = vals.replace('[','')
vals = vals.replace(']','')
vals = vals.replace(' ','')
vals = vals.split(",")

unique_genres = []
for x in vals:
    if x not in unique_genres:
            unique_genres.append(x)


#For each genre, if that genre appears in the list of genres for a given movie True else False
for col in unique_genres:
    df[col] = df['genres'].apply(lambda x: col in x)

#Convert them all to Boolean 0s and 1s
df[unique_genres] = df[unique_genres].apply(lambda x: x.astype('int'))


#Create new romcom genre column 
df['Rom_Com'] = np.where(((df['Romance']==1) & (df['Comedy']==1)),1,0)
df.loc[((df['Romance']==1) & (df['Rom_Com']==1)),'Romance'] = 0
df.loc[((df['Comedy']==1) & (df['Rom_Com']==1)),'Comedy'] = 0

#Rename ScienceFiction
df.rename(columns={'ScienceFiction':'Sci_Fi'}, inplace=True)

#Drop the none and genre columns 
df.drop(['none','genres'], axis=1, inplace=True)


#Convert language column to boolean for whether language is English
df['original_language'] = np.where(df['original_language']=='en',1,0)
df.rename(columns={'original_language':'english_language'}, inplace=True)


###############  MISC NEW ADDITIONS SECTION ###############

#Replace empty revenue values with 0
df['runtime'] = np.where(df['runtime'].isnull(),0,df['runtime'])
df['runtime'] = np.where(df['runtime']=='None',0,df['runtime'])


#Add in new credit-related data
credits = pd.read_csv(r'\movie_stats.csv')
credits.drop(['Date','Name'], axis=1, inplace=True)
df = df.merge(credits, on=['id','Year'], how='left')


#If these new values are NA (aka weren't pulled in by API) set as 0
df['female_roles'] = np.where(df['female_roles'].isnull(),0,df['female_roles'])
df['female_driven'] = np.where(df['female_driven'].isnull(),0,df['female_driven'])
df['female_directed'] = np.where(df['female_directed'].isnull(),0,df['female_directed'])


#Show cleaned data
print(df)

#Print to CSV
df.to_csv(r'\movie_data_cleaned.csv',header=True, index = False)
