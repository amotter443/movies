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
cast_stats = cast_stats.sort_values('movie_count',ascending=False)
cast_stats['order'] = cast_stats[["movie_count","lead_performance"]].apply(tuple,axis=1).rank(method='dense',ascending=False).sub(1).astype(int)
print(cast_stats)


#Derriving aggregate stats for crew
crew_full = crew_full.merge(crew_full.groupby('name').agg(credits=('id',list)).reset_index())
crew_full['female_directed'] = np.where(((crew_full['job']=="Director") & (crew_full['gender']=="Female")),1,0)
crew_stats = crew_full.groupby(['name','job']).agg({'id': pd.Series.nunique,'gender': 'first','female_directed': 'max','popularity': 'mean','profile_path': 'first'})
crew_stats.reset_index(inplace=True)
crew_stats.rename(columns = {'id':'movie_count'},inplace=True)
crew_stats = crew_stats.sort_values('movie_count',ascending=False)
crew_stats['order'] = crew_stats[["movie_count","popularity"]].apply(tuple,axis=1).rank(method='dense',ascending=False).sub(1).astype(int)
print(crew_stats)


#Derriving movie stats for use with primary movie df
movie_stats_ca = cast_full.groupby("id").agg({'popularity': 'mean','female_role': 'sum'})
movie_stats_ca.rename(columns = {'popularity':'cast_popularity','female_role':'female_roles'},inplace=True)
movie_stats_ca.reset_index(inplace=True)
movie_stats_ca['female_driven'] = np.where(movie_stats_ca['female_roles']>8,1,0)
movie_stats_cr = crew_full.groupby("id").agg({'popularity': 'mean','female_directed': 'max'})
movie_stats_cr.rename(columns = {'popularity':'crew_popularity'},inplace=True)
movie_stats_cr.reset_index(inplace=True)
#Merge both dataframes
movie_stats = movie_stats_ca.merge(movie_stats_cr, on=['id'], how='left')
print(movie_stats)


cast_stats.to_csv(r'\cast_stats.csv',header=True, index = False)
crew_stats.to_csv(r'\crew_stats.csv',header=True, index = False)
movie_stats.to_csv(r'\movie_stats.csv',header=True, index = False)