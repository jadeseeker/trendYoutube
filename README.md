Project Topic - Study on data corresponding to poular YouTube videos using a Temporal Database

fetchAnalyseStore.py is the python script that fetches data from YouTube and then stores it in the database. This does not perform sentiment analysis on the comments. There is another script which is at present not in this repo which when when run fetches comments correpsonding to the videos already present in the database, performs sentiment analysis on them and then updates the sentiment values in the database.

The temporal database features have been implemented using the temporal\_tables-1.0.1 extension for PostgreSQL databases. The code for that will be updated soon in this repo.

fetch.py is the old file which when run fetched top 100 video (if available) and corresponding data (minus comments) from the 4 playlists. Currently it prints to terminal.
