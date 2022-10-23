# Hit-Music-of-the-Streaming-Era

Ever since 10 years old, I was fascinated by music charts such as the Billboard Hot 100. Like many Gen-Z, I grew up with streaming services and became fascinated by how music changed as a result of the on-demand streaming era. As a result of this passion, I collected and continue to collect week-to-week numbers since 2017 on the weekly on-demand audio streams top hit songs recieve in the United States. Specifically, I collect data from the HITS Daily Double magazine on this Google Sheet: https://docs.google.com/spreadsheets/d/165OdLYjLt4AgeqP5S5PunRonDkpp28nueHLFv994bPk/edit?usp=sharing

This project aims to analyze the characteristics of hit songs and what styles of music does the general public prefer to listen to. It utilizes various Python packages such as gspread to connect Python with Google Sheets and spotipy which hosts Spotify's API data.

This project hosts 4 Jupyter Notebooks for the following purposes:
- 1 - To collect data
- 2 - To analyze the data
- 3 - To model the data (with K-Means clustering)
- 4 - To create a playlist of all the songs used for this project! 🥳 Something fun to look at/listen to!

*** In the near future, I will upload a part zero to this project. In part zero, information taken from HITS Daily Double's Overall Song Streams Chart (https://hitsdailydouble.com/streaming_songs) will be webscraped and added onto the Google Sheet above every week. So far, it is still in the testing phase. In the far future, I plan on automating the data collection for every week since 2017, so that my resulting data can look exactly like the Google Sheet I have. The reason for this taking a while is because so many data entries in my Google Sheet are edited versions of what comes from HITS Daily Double. Sometimes HITS Daily Double has notable mistakes such as accidentally omitting a song from the charts one week but having it present the next. Luckily, HITS Daily Double also shows weekly changes in streams by percentage point to help correct these errors. 
