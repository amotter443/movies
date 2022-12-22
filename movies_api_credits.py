#NB: The formatting for cast and crew was created and read in even on the initial execution. If starting
#for the first time, need to run for just the first title and write to CSV before the full run.

#Before running: add API key into line 11, file path to lines 14-16, 77-78

import requests
import json
import numpy as np
import pandas as pd

API_key = ''

#Read in previous data
df = pd.read_csv(r'\lb_tmdb.csv')
cast_full = pd.read_csv(r'\cast.csv')
crew_full = pd.read_csv(r'\crew.csv')


#Letterboxd logged titles, i.e. titles for the API to search for
title = df['id'].astype(str).tolist()
#Filter the title list to only values not in cast_full already
title = np.setdiff1d(title,cast_full['id'].astype(str).tolist())
print(title)

#Iterative approach to pulling all the credits
for i in range (0,len(title)):
        query = 'https://api.themoviedb.org/3/movie/'+title[i]+'/credits?api_key='+API_key+''
        response =  requests.get(query)
        if response.status_code==200: 
                json_format = json.loads(response.text)
                #Only tries to format correctly if both cast and crew are in JSON payload
                if len(json_format['cast']) > 0 and len(json_format['crew']) > 0 :

                        #Convert cast dictionary into its own dataframe
                        cast = pd.DataFrame.from_dict(json_format['cast'])
                        cast['id'] = json_format['id']
                        #Remove exteraneous columns 
                        cast.drop(['adult','known_for_department','cast_id','character','credit_id','original_name'],axis=1,inplace=True)
                        #Recode Gender to String
                        cast['gender'] = np.where(cast['gender']==1,"Female","Male")

                        #Filter people to only the first 20 credited cast members
                        cast = cast[cast['order']<=20]
                        #If profile image isn't blank add in necessary prefix, else revert to default
                        cast['profile_path'] = np.where(cast['profile_path'].notna(),r'https://image.tmdb.org/t/p/original' + cast['profile_path'].astype(str),r'https://i0.wp.com/s.ltrbxd.com/static/img/avatar1000.a71b6e9c.png?ssl=1')

                        #Convert crew dictionary into its own dataframe
                        crew = pd.DataFrame.from_dict(json_format['crew'])
                        crew['id'] = json_format['id']
                        #Drop exteraneous columns
                        crew.drop(['adult','known_for_department','credit_id','original_name'],axis=1,inplace=True)
                        #Recode Gender to String
                        crew['gender'] = np.where(crew['gender']==1,"Female","Male")
                        #If profile image isn't blank add in necessary prefix, else revert to default
                        crew['profile_path'] = np.where(crew['profile_path'].notna(),r'https://image.tmdb.org/t/p/original' + crew['profile_path'].astype(str),r'https://i0.wp.com/s.ltrbxd.com/static/img/avatar1000.a71b6e9c.png?ssl=1')

                        #Limit departaments to only the ones I'm interested in
                        crew = crew[crew.department.isin(["Writing","Directing","Costume & Make-Up","Editing","Camera"])]
                        #Limit roles to only the ones I'm looking at tracking
                        crew = crew[crew.job.isin(["Director of Photography","Director","Costume Design","Editor","Book","Novel","Screenplay","Writer","Lyricist","Script Consultant"])]

                        #Append to existing df
                        cast_full = cast_full.append(cast)
                        crew_full = crew_full.append(crew)

                        #Print iterator to make sure it doesn't get stuck
                        print(i)
                else:
                        i = i + 1
                        print("Missing cast or crew")
        else:
                i = i + 1
                print("Non-200 response")


#Write to CSV
cast_full.to_csv(r'\cast.csv',header=True, index = False)
crew_full.to_csv(r'd\crew.csv',header=True, index = False)