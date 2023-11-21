#Load Requisite Libraries
import numpy as np
import pandas as pd

#Read in previous data
cast_full = pd.read_csv(r'\cast.csv')
crew_full = pd.read_csv(r'\crew.csv')


#Derriving aggregate stats for cast
cast_full = cast_full.merge(cast_full.groupby('name').agg(credits=('id',list)).reset_index())
cast_full['female_role'] = np.where(cast_full['gender']=="Female",1,0)
cast_full['lead_performance'] = np.where(cast_full['order']<=2,1,0)
cast_stats = cast_full.groupby("name").agg({'id': pd.Series.nunique,'lead_performance': 'sum','gender': 'first','popularity': 'mean','profile_path': 'first','credits': 'first'})
cast_stats.reset_index(inplace=True)
cast_stats.rename(columns = {'index':'name','id':'movie_count'},inplace=True)
#Remove entries that only have 1 film seen since that is exteranous and unnecessary rows
cast_stats = cast_stats[cast_stats["movie_count"]>1]
cast_stats['order'] = cast_stats[["movie_count","lead_performance"]].apply(tuple,axis=1).rank(method='dense',ascending=False).sub(1).astype(int)
cast_stats = cast_stats.sort_values('order',ascending=True)
print(cast_stats)


#Derriving aggregate stats for crew
crew_full = crew_full.merge(crew_full.groupby('name').agg(credits=('id',list)).reset_index())
crew_full['female_directed'] = np.where(((crew_full['job']=="Director") & (crew_full['gender']=="Female")),1,0)
crew_stats = crew_full.groupby(['name','job']).agg({'id': pd.Series.nunique,'gender': 'first','popularity': 'mean','profile_path': 'first'})
crew_stats.reset_index(inplace=True)
crew_stats.rename(columns = {'id':'movie_count'},inplace=True)
#Remove entries that only have 1 film seen since that is exteranous and unnecessary rows
crew_stats = crew_stats[crew_stats["movie_count"]>1]
crew_stats['order'] = crew_stats[["movie_count","popularity"]].apply(tuple,axis=1).rank(method='dense',ascending=False).sub(1).astype(int)
crew_stats = crew_stats.sort_values('order',ascending=True)
print(crew_stats)


#Derriving movie stats for use with primary movie df
movie_stats_ca = cast_full.groupby("id").agg({'female_role': 'sum'})
movie_stats_ca.rename(columns = {'female_role':'female_roles'},inplace=True)
movie_stats_ca.reset_index(inplace=True)
movie_stats_ca['female_driven'] = np.where(movie_stats_ca['female_roles']>8,1,0)
movie_stats_cr = crew_full.groupby("id").agg({'female_directed': 'max'})
movie_stats_cr.reset_index(inplace=True)
#Merge both dataframes
movie_stats = movie_stats_ca.merge(movie_stats_cr, on=['id'], how='left')
print(len(movie_stats))
#Read in and merge tmdb df
movie_data = pd.read_csv(r'\lb_tmdb.csv')
movie_stats = movie_stats.merge(movie_data, on=['id'], how='left')
#Drop everything except Date, Name, and Year
movie_stats.drop(['original_language','overview','popularity','vote_average','vote_count','genres','revenue','runtime','tagline'], axis=1, inplace=True)
print(len(movie_stats))


#Create cast trending by year for additional visualizations
cast_full = cast_full.merge(movie_stats, on=['id'], how='left')
cast_full['Logged_Year'] = pd.to_datetime(cast_full['Date'], format='%Y-%m-%d').dt.year
cast_stats_yearly = cast_full.groupby(['name', 'Logged_Year']).agg({'id': pd.Series.nunique,'lead_performance': 'sum','gender': 'first','popularity': 'mean','profile_path': 'first'})
cast_stats_yearly.reset_index(inplace=True)
cast_stats_yearly.rename(columns = {'index':'name','id':'movie_count'},inplace=True)
#Remove 2017 since that was the first year with the most bulk uploads
cast_stats_yearly = cast_stats_yearly[(cast_stats_yearly["Logged_Year"]>2017)]

#Remove entries that only have 1 film seen since that is exteranous and unnecessary rows
cast_stats_yearly = cast_stats_yearly[cast_stats_yearly["movie_count"]>1]
cast_stats_yearly['order'] = cast_stats_yearly[["Logged_Year","movie_count","lead_performance","popularity"]].apply(tuple,axis=1).rank(method='dense',ascending=False).sub(1).astype(int)
cast_stats_yearly = cast_stats_yearly.sort_values('order',ascending=True)
#Create toggle value to display in UI
cast_stats_yearly['DELETE'] =  cast_stats_yearly.groupby(['Logged_Year','gender'])['order'].transform('min')
cast_stats_yearly['display'] = np.where(cast_stats_yearly['DELETE']==cast_stats_yearly['order'],1,0)
cast_stats_yearly.drop(['DELETE'], axis=1, inplace=True)
print(cast_stats_yearly)


#Create crew trending by year for additional visualizations
crew_full = crew_full.merge(movie_stats, on=['id'], how='left')
crew_full['Logged_Year'] = pd.to_datetime(crew_full['Date'], format='%Y-%m-%d').dt.year
crew_stats_yearly = crew_full.groupby(['name','job','Logged_Year']).agg({'id': pd.Series.nunique,'gender': 'first','popularity': 'mean','profile_path': 'first'})
crew_stats_yearly.reset_index(inplace=True)
crew_stats_yearly.rename(columns = {'index':'name','id':'movie_count'},inplace=True)
#Remove 2017 since that was the first year with the most bulk uploads
crew_stats_yearly = crew_stats_yearly[(crew_stats_yearly["Logged_Year"]>2017)]

#Remove entries that only have 1 film seen since that is exteranous and unnecessary rows
crew_stats_yearly = crew_stats_yearly[crew_stats_yearly["movie_count"]>1]
crew_stats_yearly['order'] = crew_stats_yearly[["Logged_Year","job","movie_count","popularity"]].apply(tuple,axis=1).rank(method='dense',ascending=False).sub(1).astype(int)
crew_stats_yearly = crew_stats_yearly.sort_values('order',ascending=True)
#Create toggle value to display in UI
crew_stats_yearly['DELETE'] =  crew_stats_yearly.groupby(['Logged_Year','job'])['order'].transform('min')
crew_stats_yearly['display'] = np.where(crew_stats_yearly['DELETE']==crew_stats_yearly['order'],1,0)
crew_stats_yearly.drop(['DELETE'], axis=1, inplace=True)
print(crew_stats_yearly)


cast_stats.to_csv(r'\cast_stats.csv',header=True, index = False)
crew_stats.to_csv(r'\crew_stats.csv',header=True, index = False)
movie_stats.to_csv(r'\movie_stats.csv',header=True, index = False)
cast_stats_yearly.to_csv(r'\cast_trended_stats.csv',header=True, index = False)
crew_stats_yearly.to_csv(r'\crew_trended_stats.csv',header=True, index = False)
