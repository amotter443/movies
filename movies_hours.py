#Load Requisite Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from sklearn.utils import _to_object_array
pd.options.mode.chained_assignment = None  # default='warn'

#Read in data
df = pd.read_csv('lb_tmdb.csv')
diary = pd.read_csv('diary.csv')

#Initialize Count column 
diary['count'] = 1

for i in range (0,len(diary)):
    #Make an array of the titles so far
    titles = diary['Name'][:i]
    #Get counts of the array and store in dictionary
    titles_counts = titles.value_counts().to_dict()
    if diary['Name'][i] not in titles_counts and diary['Rewatch'][i]=='Yes':
        diary['count'][i] = 2

#Group by title
diary = diary.groupby(['Name']).sum()
diary = diary.sort_values(by='count', ascending=False).reset_index()
#Reduce to just name and count columns
diary = diary[['Name','count']]

#Create list of the remaining Name values in df not in diary
remaining = df[~df['Name'].isin(diary['Name'])]
#Reduce to just Name and count columns
remaining['count'] = 1
remaining = remaining[['Name','count']]
#add remaining records to diary df
diary = pd.concat([diary, remaining])
print(diary.head())

#Export to separate file
diary.to_csv('movie_log_counts.csv')


#Join diary df with df
df = pd.merge(diary, df, on='Name', how='left')

#Select just the runtime and count columns
df = df[['Name','count','runtime']]

#Calculate the minutes watched of each movie
df['minutes_watched'] = df['count']*df['runtime']
print(df.head())

#Print the total minutes watched
print('Total minutes watched: ', round(df['minutes_watched'].sum()))
#Print the total hours watched
print('Total hours watched: ', round(df['minutes_watched'].sum()/60))
