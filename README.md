# Hit-Music-of-the-Streaming-Era

Ever since 10 years old, I was fascinated by music charts such as the Billboard Hot 100. Like many Gen-Z, I grew up with streaming services and became fascinated by how music changed as a result of the on-demand streaming era. As a result of this passion, I collected and continue to gather week-to-week numbers since 2017 on the weekly on-demand audio streams top hit songs recieve in the United States. 

This project aims to analyze the characteristics of hit songs and what styles of music do the general public prefer to listen to. It utilizes various Python packages such as gspread to connect Python with Google Sheets and spotipy which hosts Spotify's API data.

This project hosts 4 main Jupyter Notebooks for the following purposes:
## **1. Data Collection**
   
I collect data using a Python script from a combination of the HITS Revenue and HITS Streaming charts alongside educated guesses from Billboard Streaming Charts to get what songs charted on the top 50 on streaming. The process involves the following steps:

  a) Initial Data Collection: The script gathers data on song/artist/album information and retrieves corresponding song IDs and metadata from Spotify's API.
  
  b) Data Storage: All gathered information is consolidated into a Google Sheet, which allows for easier management and avoids the need to re-run the code frequently.

  Two Iterations of Jupyter Notebook 1:
  
    1a): Collects Spotify metadata for all songs in the Google Sheet, focusing on those that have reached the top 50.
    
    1b): Collects Spotify metadata only for new songs in the Google Sheet. Due to the large number of songs, I primarily use this iteration for updates.

## **2. Data Analysis**
  
In this step, I retrieve the data from the Google Sheet mentioned in step 1 and generate various graphs and charts to analyze the top 50 songs. The analysis includes:

  a) Top Songs, Albums, and Artists: Interactive graphs showcase the biggest songs, albums, and artists within the top 50, allowing for exploration of their cumulative and weekly streams.

![Screenshot 2024-08-13 at 10 33 23 AM](https://github.com/user-attachments/assets/db2fad2c-7719-41c6-9c9f-c4c0c47d6725)
![Screenshot 2024-08-13 at 10 34 10 AM](https://github.com/user-attachments/assets/351dd459-20b1-4dd2-9a22-cb81fe0eb887)
![Screenshot 2024-08-13 at 10 35 28 AM](https://github.com/user-attachments/assets/0d10fb55-5f95-4e51-8d5e-f406c66ea06e)

  b) Original Visual Analysis of Song Characteristics: This section, which I consider the most exciting part of the analysis, dives into the unique aspects of the project. I create graphs for different song characteristics like acousticness, danceability, energy, speechiness, happiness/valence levels, instrumentalness, etc. The process involves several steps:

    i) Calculate Z-Scores: Determine Z-scores for all weekly data points based on their deviation from a centered rolling average using an N-week window (e.g., 8 weeks).
    ii) Set Confidence Interval: Define an 85% confidence interval for the analysis.
    iii) Filtered Rolling Average: Generate a new rolling average by excluding data points with Z-scores outside the confidence interval, reducing the impact of outliers.
    iv) Upper and Lower Bounds: Establish bounds by adding and subtracting the standard deviation of the dataset’s residuals, multiplied by the Z-score for the confidence interval.

    *** Adjustable Parameters: The code allows for customization of the N-week window, confidence interval, centered rolling averages, and the number of weeks used for calculations.
    
![Screenshot 2024-08-13 at 10 39 27 AM](https://github.com/user-attachments/assets/b993d65b-d7f6-48bd-ba9b-82c8378b129b)
![Screenshot 2024-08-13 at 10 45 58 AM](https://github.com/user-attachments/assets/ecb1bf77-ea54-4a96-8f12-e7d3017ea18b)


Some charts related to this portion of the project are still being updated (expected completion by the end of August), but they already provide an outlier detection system and offer a novel way to visualize music trends. 

I will also write analyses for each metric, with an example included: 
https://docs.google.com/document/d/1Z5UcSWbxj9_ttbWUqcNC7KrrXhg5XkvC9USP1fR78Zs/edit?usp=sharing

## **3. Data Modeling**

The goal of this portion is to understand the categories that songs fall into. Given that the data is unlabeled (although genres could be added, many songs are genre-ambiguous), an unsupervised clustering model is necessary. The K-Means Clustering algorithm is used as it is simple to implement.

I isolated five variables for clustering: acousticness, danceability, speechiness, energy, and instrumentalness. The number of clusters (k) was determined using the elbow method, graphing the sum of squared differences for each data point relative to cluster centroids across a range of k values. Principal Component Analysis (PCA) was performed to scale down the dataset's dimensions, and the results were visualized with bar graphs and radar charts.


The four main types of songs that entered the top 50 since 2017 are:
  1. Danceable/energetic songs with higher speechiness levels
  2. Danceable/energetic songs with lower speechiness levels
  3. Acoustic/acoustic-leaning songs
  4. Songs with higher-than-normal instrumentalness

![Screenshot 2024-08-13 at 10 56 33 AM](https://github.com/user-attachments/assets/892001e2-c310-4c4c-9607-38259ea0ef67)

Example of songs in a cluster: ![Screenshot 2024-08-13 at 10 57 04 AM](https://github.com/user-attachments/assets/d13c79e0-6960-467d-8b01-73d84f199fb5)

## **4. Playlist creation! 🥳**
This portion of the project is a more relaxed endeavor, focused on creating a playlist from the songs analyzed throughout the project. The playlist features all the hit songs that charted in the top 50, providing an enjoyable listening experience that reflects the trends identified in the data analysis.
Listen to the playlist [here](https://open.spotify.com/playlist/2fqpXYOyQG3q3HCaRjZitJ?si=9c248042f7f342d3)


## **Future plans**
1. Finish updating some of the graphs associated with the statistical/outlier detection analysis portion of the project (expected completion: end of August).
2. Use a mixture of kworb.net data and Spotify data to gather data on the top 200 songs and replicate this analysis with Spotify-only data (expected completion: end of November).
3. Draft write-ups for trends involving each metric analyzed.
