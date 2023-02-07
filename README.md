# movies
>Using Letterboxd personal data, TMDB API, and data science techniques to analyze movie watching data


As an avid movie watcher, the opportunity to combine my loves of data science and film was too good to pass up. Having been a Letterboxd user for many years, I leveraged my personal watch history data to better understand my viewing patterns and learn more about myself in the process. For more detailed report on this project and its methodology, please check out my [LinkedIn article](https://www.linkedin.com/pulse/how-i-used-machine-learning-quantify-my-movie-obsession-alex-motter) and its [follow-up](https://www.linkedin.com/pulse/using-personal-analytics-determine-my-most-watched-actors-alex-motter/) detailing the credits code implementation.


Who is this project for?
------------------------
- Cinephiles with a passion for coding
- Developers interested in multiple areas of development (API calling, sentiment analysis, regression-based modeling, etc.)
- Affinity users of other sub-communities (i.e. having a Goodreads instead of Letterboxd/IMDB/a movie logging site) who want to also derive personal analytics from their platform usage 


Accessing The Data
--------
- Download personal movie data from Letterboxd: Setting -> Import & Export -> Export Your Data
- You can also access the direct link to download your data [here](https://letterboxd.com/settings/data/)
- Save the following files: `watched.csv`, `ratings.csv`, and `reviews.csv`
- Request an API key from [TMDB](https://developers.themoviedb.org/3/getting-started/introduction)
- Once API Key retrieved, use with `movies_api.py` to retrieve additional movie data


Usage Insights
--------
- The TMDB allows for 30-40 API requests every 10 seconds, so if you have thousands of movies logged as I do this could factor into the performance time of `movies_api.py`
- If you've logged an limited series/prestige TV on the app (like the Emmy award winning limited series _Big Little Lies_) those won't have any TMDB API hits since it is pointed at the movie side of the database. I removed those records since they aren't within the scope of the project anyways. 
- Even though the dashboard was created in Power BI, I wrote the code in `movies_eda.ipynb` to re-create all the visualizations from the final dashboard. I included it as an ipynb rather than just a .py script so you could see the output of each code chunk, but a .py version would be suitable as well if using a different IDE


Script Execution Order
------------------------
1. `movies_api.py`
2. `movies_api_credits.py`
3. `movies_api_credits_cleaning.py`
4. `movies_cleaning.py`
5. `movies_sentiment.py`
6. `movies_modeling.py`
7. *Optional* `movies_eda.py` or `movies_eda.ipynb`


Data Dictionary
------------------------
- `Logged_Date` -- Date I logged the film on Letterboxd
- `Name` -- Name of the film as it appears on Letterboxd's site
- `Year` -- Generally, the year of the US release date. Can vary depending on whether it was released internationally or at film festivals first
- `Rating` -- Records on a scale of 0 to 5 by increments of 0.5 the star rating I gave the film
- `Review` -- Boolean value that preserves whether or not I wrote a review for the film on Letterboxd
- `id` -- Unique identifying value in TMDB's database
- `english_language` -- Boolean value that records whether or not the movie's original language is English. Considered breaking this value out further but over 90% of them are surprisingly listed as English language in TMDB
- `overview` -- Provides brief synopsis of the film
- `popularity` -- Internally calculated score based on site interaction data. More information about this feature can be found [here](https://developers.themoviedb.org/3/getting-started/popularity)
- `vote_average` -- Average user rating of the film on a scale of 0 to 10
- `vote_count` -- Total number of users who rated the film
- `vote_revenue` -- Total amount of money grossed at the domestic and international box office
- `runtime` -- Total running length of the film excluding commercials, measured in minutes
- `tagline` -- Marketing verbiage which provides a punchy incentive for potential viewers to choose to watch the film
- `Logged_DOW` -- Extracts day of the week from the `Logged_Date` values, recorded in numeric form (0 - Monday, 1 - Tuesday, 2 - Wednesday, 3 - Thursday, 4 - Friday, 5 - Saturday, 6 - Sunday)
- `Logged_Month` -- Extracts month value from the `Logged_Date` values
- `Logged_Year` -- Extracts year value from the `Logged_Date` values
- `Logged_Week` -- Calculates from 0 to 54 the week value from the `Logged_Date` values
- `Daily_Movie_Count` --  Calculates using the `Logged_Date` values how many movies I watched on a given date
- `Weekly_Movie_Count` --  Calculates using the `Logged_Week` and `Logged_Year` values how many movies I watched on a given week
- `genres` -- Several boolean columns exist that indicate whether or not the movie was classified into the following genres: (Action, Crime, War, Drama, Thriller, Mystery, Comedy, Romance, Sci_Fi, Animation, Documentary, Adventure, Music, Horror, Fantasy, History, Western, Rom_Com)
- `female_roles` -- Measures the number of female roles in the first 20 billed of a movie's acting credits
- `female_driven` -- Boolean value that records whether 9 or more of those 20 roles are female, therefore classifying the film as "female-driven"
- `female_directed` -- Boolean value that records whether or not the director of the film self-identifies as female
- `negativity_percentage` --  Measures what percentage of the string input has a negative association
- `neutrality_percentage` --  Measures what percentage of the string input has a neutral association
- `positivity_percentage` --  Measures what percentage of the string input has a positive association
- `movie_sentiment` --  The compound score is the aggregate sum of positive, negative & neutral percentages. The closer this value is to 1, the more positive the movie's overview is


Future Project Expansions
------------------------
- ~~Integrate additional movie attributes such as the film's director, leading actors, and thematic content~~ *Completed Jan 2023 with "credits" expansion*
- Rather than just the film's lanaguage, integrating country of origin to better understand domestic vs. international viewing
- Left joining on the Diary dataset rather than Watched one to conduct time series analysis/predict what genre or type of movies I'll watch next


Helpful Data Resources
--------
![image](https://user-images.githubusercontent.com/71201000/133646506-dd7c798c-42ad-44d9-b138-d39dd67ce91f.png)
- [TMDB API Details](https://developers.themoviedb.org/3/movies/get-movie-details)
- [IMDB API](https://rapidapi.com/blog/how-to-use-imdb-api) for those who don't want to use TMDB
- [Accessing total IMDB raw data](https://www.imdb.com/interfaces/) not advised because the full data has around 100 million records
- [Python API Tutorial](https://www.dataquest.io/blog/python-api-tutorial/)
- [Python Sentiment Analysis](https://realpython.com/python-nltk-sentiment-analysis/)
