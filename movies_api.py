#Before running: add API key into line 11, file path on lines 14

#If running for first time: Comment out lines 74-78, uncomment 80-81 and add in file path
#If running as update to existing as a update to existing lb_tmdb.csv: Add in file path to 74-78 


import requests
import json
import pandas as pd

API_key = ''

#Read in data
df = pd.read_csv(r'\watched.csv')

#For Update Run: Allow filtering for values 
df = df[(df['Date'] > '2022-01-14')]


#Drop Letterboxd URI 
df.drop(['Letterboxd URI'], axis=1, inplace=True)
#Initialize columns for desired info
df['id'] = 000000
df['original_language'] = 'en'
df['overview'] = 'blank'
df['popularity'] = 0.00
df['vote_average'] = 0.00
df['vote_count'] = 0.00
df['genres'] = 'blank'
df['revenue'] = 000000
df['runtime'] = 000
df['tagline'] = 'blank'


#Initial for loop to pull high-level info about the film
for i in range (0,len(df)):
    title=format(df.iloc[i,1])
    query = 'https://api.themoviedb.org/3/search/movie?api_key='+API_key+'&query='+title+''
    response =  requests.get(query)
    if response.status_code==200: 
        json_format = json.loads(response.text)
        if len(json_format['results']) > 0 :
            df.iloc[i,3] = str(json_format['results'][0]['id'])
            df.iloc[i,4] = str(json_format['results'][0]['original_language'])
            df.iloc[i,5] = str(json_format['results'][0]['overview'])
            df.iloc[i,6] = str(json_format['results'][0]['popularity'])
            df.iloc[i,7] = str(json_format['results'][0]['vote_average'])
            df.iloc[i,8] = str(json_format['results'][0]['vote_count'])
        else:
            i = i + 1
    else:
        i = i + 1

#Secondary Pull that uses Movie ID to get more info 
for i in range (0,len(df)):
    title=format(df.iloc[i,3])
    query = 'https://api.themoviedb.org/3/movie/'+title+'?api_key='+API_key+''
    if df.iloc[i,3] != '000000':
       response =  requests.get(query)
       if response.status_code==200: 
            json_format = json.loads(response.text)
            df.iloc[i,9] = str(json_format['genres'])
            df.iloc[i,10] = str(json_format['revenue'])
            df.iloc[i,11] = str(json_format['runtime'])
            df.iloc[i,12] = str(json_format['tagline'])
       else:
           i = i + 1
    else:
        i = i + 1

print(df)


#For Update Run:
df.to_csv(r'\lb_tmdb_newentries.csv',header=True, index = False)
df_prev = pd.read_csv(r'\lb_tmdb.csv')
api_results = df_prev.append(df)
api_results.to_csv(r'\lb_tmdb.csv',header=True, index = False)

#Write to CSV
#df.to_csv(r'\lb_tmdb.csv',header=True, index = False)
