#Load Requisite Libraries
import pandas as pd
from pymongo import MongoClient


#Load Data
df = pd.read_csv(r'\movie_data_final.csv')
cast = pd.read_csv(r'\cast_stats.csv')
crew = pd.read_csv(r'\crew_stats.csv')
cast_trended = pd.read_csv(r'\cast_trended_stats.csv')
crew_trended = pd.read_csv(r'\crew_trended_stats.csv')


#Mongo credentials that will be in secret.toml
username = ''
password = ''
cluster = ''

#Establish connection to MongoDB
mongo_uri = 'mongodb+srv://%s:%s@%s.ycr5yln.mongodb.net/?retryWrites=true&w=majority' % (username, password, cluster)
conn = MongoClient(mongo_uri)
#Connect to database in cluster
db = conn["letterboxd"]

#Write movie_data_final to master_df collection
collection = db.get_collection("master_df")
collection.insert_many(df.to_dict('records'))

#Write cast to cast collection
collection = db.get_collection("cast")
collection.insert_many(cast.to_dict('records'))

#Write crew to crew collection
collection = db.get_collection("crew")
collection.insert_many(crew.to_dict('records'))

#Write cast_trended to cast_trended collection
collection = db.get_collection("cast_trended")
collection.insert_many(cast_trended.to_dict('records'))

#Write crew_trended to crew_trended collection
collection = db.get_collection("crew_trended")
collection.insert_many(crew_trended.to_dict('records'))