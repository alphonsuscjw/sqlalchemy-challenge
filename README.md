# sqlalchemy-challenge

I've decided to treat myself to a long holiday vacation in Honolulu, Hawaii. To help with my trip planning, I decided to do a climate analysis about the area.

There are two parts to this task. First I used Python and SQLAlchemy to do a basic climate analysis and data exploration of a Hawaii climate SQLite database. Then I designed a Flask API based on the queries that I had developed.

## Part 1: Analyse and Explore the Climate Data
In this part, I first designed a query to retrieve the last 12 months of precipitation data from the database and plotted the results. Then, using data from the most active station (determined from the previous query), I calculated the lowest, highest, and average temperature this station had ever recorded. I also queried the last 12 months of temperature observation data for this station and plotted the results as a histogram.

## Part 2: Design Climate App
In the next part, I designed a Flask API that has several routes that can make different queries from the Hawaii climate SQLite database. The Homepage lists all available routes. The available routes allow users to make queries on:
1. all precipitation data of the last 12 months in the database
2. the data on all stations
3. the last 12 months of temperatures recorded by the most active station (USC00519281) in the database
4. the minimum, average and maximum temperatures calculated from the user-input start date to the end of the dataset
5. the minimum, average and maximum temperatures calculated from the user-input start date to the user-input end date
