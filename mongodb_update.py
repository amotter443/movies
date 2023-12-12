#Before running: Update last run date on line 32

#Load Requisite Libraries
import pandas as pd
from pymongo import MongoClient


#Load Data
df_new = pd.read_csv(r'\movie_data_final.csv')
cast_new = pd.read_csv(r'\cast_stats.csv')
crew_new = pd.read_csv(r'\crew_stats.csv')
cast_trended_new = pd.read_csv(r'\cast_trended_stats.csv')
crew_trended_new = pd.read_csv(r'\crew_trended_stats.csv')


#Mongo credentials that will be in secret.toml
username = ''
password = ''
cluster = ''

#Establish connection to MongoDB
mongo_uri = 'mongodb+srv://%s:%s@%s.ycr5yln.mongodb.net/?retryWrites=true&w=majority' % (username, password, cluster)
conn = MongoClient(mongo_uri)
#Connect to database in cluster
db = conn["letterboxd"]

######### Final Dataframe section #########

collection = db.get_collection("master_df")

#For Execution: Change date to last script execution 
df_new = df_new[(df_new['Logged_Date'] > '2023-11-17')]
#Write to df
collection.insert_many(df_new.to_dict('records'))

######### Cast Dataframe section #########

#Connect to cast, wipe df, write new records
collection = db.get_collection("cast")
collection.delete_many(({}))
collection.insert_many(cast_new.to_dict('records'))

#Connect to cast_trended, wipe df, write new records
collection = db.get_collection("cast_trended")
collection.delete_many(({}))
collection.insert_many(cast_trended_new.to_dict('records'))


######### Crew Dataframe section #########

#Connect to crew, wipe df, write new records
collection = db.get_collection("crew")
collection.delete_many(({}))
collection.insert_many(crew_new.to_dict('records'))

#Connect to crew_trended, wipe df, write new records
collection = db.get_collection("crew_trended")
collection.delete_many(({}))
collection.insert_many(crew_trended_new.to_dict('records'))