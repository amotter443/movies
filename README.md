# movies
>Using Letterboxd personal data, TMDB API, and data science techniques to analyze movie watching data




Who is this project for?
------------------------
- Cinephiles with a passion for coding
- Developers interested in multiple areas of development (API calling, sentiment analysis, classification, regression, etc.)
- Affinity users of other sub-communities (i.e. having a Goodreads instead of Letterboxd/IMDB/a movie logging site) who want to also derive personal analytics from their platform usage 


Accessing The Data
--------
- Download personal movie data from Letterboxd: Setting -> Import & Export -> Export Your Data
- You can also access the direct link to download your data [here](https://letterboxd.com/settings/data/)
- Save the following files: `watched.csv`, `ratings.csv`, and `reviews.csv`
- Request an API key from [TMDB](https://developers.themoviedb.org/3/getting-started/introduction)
- Once API Key retrieved, use with `movies_api.py` to retrieve additional movie data


Usage
--------
- The TMDB allows for 30-40 API requests every 10 seconds, so if you have thousands of movies logged as I do this could factor into the performance time of `movies_api.py`
- If you've logged an limited series/prestige TV on the app (like the Emmy award winning limited series _Big Little Lies_) those won't have any TMDB API hits since it is pointed at the movie side of the database. I just cleared these records since they aren't within the scope of the project anyways. 


Helpful Data Resources
--------
![image](https://user-images.githubusercontent.com/71201000/133646506-dd7c798c-42ad-44d9-b138-d39dd67ce91f.png)
- [TMDB API Details](https://developers.themoviedb.org/3/movies/get-movie-details)
- [IMDB API](https://rapidapi.com/blog/how-to-use-imdb-api) for those who don't want to use TMDB
- [Accessing total IMDB raw data](https://www.imdb.com/interfaces/) not advised because the full data has around 100 million records
- [Python API Tutorial](https://www.dataquest.io/blog/python-api-tutorial/)
