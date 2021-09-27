#Load Requisite Libraries
import pandas as pd
import numpy as np
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')


#Read in data
df = pd.read_csv(r'\movie_data_cleaned.csv')


############## SYNOPSIS SECTION ##############

#Collect words from synopses
words = pd.Series(df['overview']).tolist()
words = str(words)
words = words.replace('\'','')
words = words.replace('’','')
words = words.replace(',','')
words = words.replace('.','')
words = words.replace('[','')
words = words.replace(']','')
words = nltk.word_tokenize(words)

#Remove all special charecters
words= [word for word in words if word.isalnum()]
#Remove stopwords
stopwords = nltk.corpus.stopwords.words("english")
words = [w for w in words if w.lower() not in stopwords]

#Get frequency distribution
fd = nltk.FreqDist([w.lower() for w in words])
print(fd.most_common(25))

#Write full list to CSV
df_fd = pd.DataFrame.from_dict(fd, orient='index')
df_fd.columns = ['Frequency']
df_fd.index.name = 'Word'
#Filter to at least 15 occurances
df_fd = df_fd[df_fd['Frequency']>=15]
df_fd.to_csv(r'\movie_overview_fd.csv',header=True, index = True)


#Add Film Sentiments to DF
df['overview'] = df.overview.str.replace('[^a-zA-Z ]', '')
analyzer = SentimentIntensityAnalyzer()
df['negativity_percentage'] = [analyzer.polarity_scores(x)['neg'] for x in df['overview']]
df['neutrality_percentage'] = [analyzer.polarity_scores(x)['neu'] for x in df['overview']]
df['positivity_percentage'] = [analyzer.polarity_scores(x)['pos'] for x in df['overview']]
df['movie_sentiment'] = [analyzer.polarity_scores(x)['compound'] for x in df['overview']]

#Show polarity outcomes
print(df)


############## TITLE SECTION ##############

#Repeat process to collect frequencies of title words
words = pd.Series(df['Name']).tolist()
words = str(words)
words = words.replace('\'','')
words = words.replace('’','')
words = words.replace(',','')
words = words.replace('.','')
words = words.replace('[','')
words = words.replace(']','')
words = nltk.word_tokenize(words)

#Remove all special charecters
words= [word for word in words if word.isalnum()]
#Remove stopwords
stopwords = nltk.corpus.stopwords.words("english")
words = [w for w in words if w.lower() not in stopwords]

#Get frequency distribution
fd = nltk.FreqDist([w.lower() for w in words])
print(fd.most_common(25))

#Write full list to CSV
df_fd = pd.DataFrame.from_dict(fd, orient='index')
df_fd.columns = ['Frequency']
df_fd.index.name = 'Word'
#Filter to at least 4 occurances
df_fd = df_fd[df_fd['Frequency']>=4]
df_fd.to_csv(r'\movie_title_fd.csv',header=True, index = True)


#Drop overview, tagline, and ID columns because they won't be needed anymore
df.drop(['overview','tagline','id'], axis=1, inplace=True)


#Print to CSV
df.to_csv(r'\movie_data_final.csv',header=True, index = False)