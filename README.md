# Hit-Music-of-the-Streaming-Era

Ever since 10 years old, I was fascinated by music charts such as the Billboard Hot 100. Like many Gen-Z, I grew up with streaming services and became fascinated by how music changed as a result of the on-demand streaming era. As a result of this passion, I collected and continue to collect week-to-week numbers since 2017 on the weekly on-demand audio streams top hit songs recieve in the United States. Specifically, I collect data from the HITS Daily Double magazine on this Google Sheet: https://docs.google.com/spreadsheets/d/165OdLYjLt4AgeqP5S5PunRonDkpp28nueHLFv994bPk/edit?usp=sharing

This project aims to analyze the characteristics of hit songs and what styles of music does the general public prefer to listen to. It utilizes various Python packages such as gspread to connect Python with Google Sheets and spotipy which hosts Spotify's API data.

This project hosts 4 Jupyter Notebooks for the following purposes:
- 1a) To collect data
- 1b) To update data (it takes a lot of time to run 1a and data updates weekly when new songs come out)
- 2) To analyze the data
- 3) To model the data (with K-Means clustering)

It also includes 4 Python script documents for the following purposes:
- To collect data (the same as Notebook 1a but in script form)
- To update data (the same as Notebook 1b but in script form)
- To create a playlist of all songs that ever touched the top 50 on streaming in the USA! (something fun to look at!)
- To store functions (to be called whenever the previously mentioned scripts are run)
