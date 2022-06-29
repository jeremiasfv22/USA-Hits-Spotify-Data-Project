#to access spotipy
import configparser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

#to allow interaction with underlying operating system
import os

#to parse through spotipy's output
import json

#for dataframe cleaning
import numpy as np
import pandas as pd

#to access google sheets with python
import gspread
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials

#to edit google sheets from python
from df2gspread import df2gspread as d2g

#to ignore warnings
import warnings
warnings.filterwarnings('ignore')

#import spotify client credentials 
"""
MAKE SURE YOU IMPORT THE VARIABLES IN THE TERMINAL USING THE FOLLOWING FORMAT:
export SPOTIPY_CLIENT_ID=YOUR_SPOTIFY_APP_CLIENT_ID              #don't input as a string
export SPOTIPY_CLIENT_SECRET=YOUR_SPOTIFY_APP_CLIENT_SECRET_ID   #don't input as a string
export SPOTIPY_REDIRECT_URI=http://127.0.0.1:8080/               #feel free to use this same one
"""
spotify_client_id = os.environ['SPOTIPY_CLIENT_ID']
spotify_secret = os.environ['SPOTIPY_CLIENT_SECRET']
spotify_redirect_uri = os.environ['SPOTIPY_REDIRECT_URI']

#create a spotipy instance
client_credentials_manager = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


def search_for_URI(data):
    """
    Returns track URIs and the explicit status for a song

        Parameters:
            data (series): series containing a song title, artist, and the song's album
        
        Returns:
            song_info_list (list): list of song title, artist, album title, song URI and explicit status
                #otherwise, returns just the song title, artist, and album title
    """
    song_to_search = data['title'].replace("’","").replace("'","").lower()
    album_to_search = data['album'].replace("’","").replace("'","").lower()
    to_search = song_to_search + " " + data['artist']
    
    #this function searches for q on Spotify
    result = sp.search(q=to_search)
        
    #loops through all results from search
    for song_info_index in range(len(result['tracks']['items'])): 

        #checks for results' album to match the input data's album title (taking into account apostrophe formats)
        if result['tracks']['items'][song_info_index]['album']['name'].replace("’","").replace("'","").lower() == album_to_search:
                        
            #checks for results' song title to match input data's song title (taking into account apostrophe formats)
            if result['tracks']['items'][song_info_index]['name'].replace("’","").replace("'","").lower() == song_to_search:     
                
                #empty list to be filled with name/artist/album/explicit/uri info
                song_info_list = []

                #checks if a song is explicit       
                if result['tracks']['items'][song_info_index]['explicit'] == True:
                    song_info_list.append(result['tracks']['items'][song_info_index]['name'])
                    song_info_list.append(result['tracks']['items'][song_info_index]['artists'][0]['name'])
                    song_info_list.append(result['tracks']['items'][song_info_index]['album']['name'])
                    song_info_list.append(result['tracks']['items'][song_info_index]['explicit'])
                    song_info_list.append(result['tracks']['items'][song_info_index]['uri'])
                    return song_info_list
                
                #first, if a song is NOT explicit
                if result['tracks']['items'][song_info_index]['explicit'] == False:
                    song_info_list.append(result['tracks']['items'][song_info_index]['name'])
                    song_info_list.append(result['tracks']['items'][song_info_index]['artists'][0]['name'])
                    song_info_list.append(result['tracks']['items'][song_info_index]['album']['name'])
                    song_info_list.append(result['tracks']['items'][song_info_index]['explicit'])
                    song_info_list.append(result['tracks']['items'][song_info_index]['uri'])
                    return song_info_list
    
    #return just the song title/artist/album title if the URI is not found
    return [data['title'],data['artist'],data['album'],"",""]


#check for any songs that don't have URIs using the newly created data_to_clean
def missing_uri_detector(data_to_clean):
    """
    Returns a dataframe of songs with missing URIs if any exists

    Parameters:
        uri_df (DataFrame): the resulting dataframe from the search_for_URI function
    
    Returns
        data_to_clean (DataFrame): a subsection of uri_df with all songs with no URI
    """
    if len(data_to_clean) > 0 :
        if len(data_to_clean) == 1:
            print('\nThere is 1 song with missing data.', 'Here is a dataframe with all songs with missing URIs:')
        else:
            print('\nThere are', len(data_to_clean), 'songs with missing data.', 'Here is a dataframe with all songs with missing URIs:', "\n")
        return data_to_clean
    else:
        print('\nSuccess! The function successfully obtained the URIs for all songs')
              

def song_uri_search(q):
    """
    Prints out different URIs (and other info) from a resulting search on spotipy
    
    Parameter:
        q (str): a string to look up using spotipy's search function
    """
    result = sp.search(q) 
    
    for song_info_dict in range(len(result['tracks']['items'])):
        print("Song: ", result['tracks']['items'][song_info_dict]['name'])
        print("Artist: ", result['tracks']['items'][song_info_dict]['artists'][0]['name'])
        print("Album: ", result['tracks']['items'][song_info_dict]['album']['name'])
        print("Explicit status: ", result['tracks']['items'][song_info_dict]['explicit'])
        print("URI: ", result['tracks']['items'][song_info_dict]['uri'],"\n")


def data_cleaning_func(data_to_clean, uri_df):
    #loop through every song in data_to_clean
    for i in range(0,len(data_to_clean)):
        print("Please follow the following steps to fill in the missing URI(s)." + "\n")
        song_to_search = data_to_clean.iloc[i]['song'].replace("’","").replace("'","")
        album_to_search = data_to_clean.iloc[i]['album'].replace("’","").replace("'","")
        artist_to_search = data_to_clean.iloc[i]['artist']
            
        #concatenate the song title, artist name, and album title to search
        to_search = song_to_search + " " + artist_to_search + " " + album_to_search

        result = sp.search(to_search)
        print("The following results are the search results from searching: '" + to_search + "'")
        print("\n")
            
        #call on song_uri_search function to print out search results
        song_uri_search(to_search)
        print("Search the URI(s) on your browser to double check the song is correct")
            
        #ensure user obtains desired result from the above search
        print("Did you obtain a desired result? Please type 'yes' or 'no': ")
        desired_result = str(input())
            
        #ensure desired_result is a valid input
        while (desired_result != 'yes')  and (desired_result != 'no'):
            print("Please give a valid input. Type either 'yes' or 'no': ")
            desired_result = str(input())
            
        #run the following in case the desired output is not available in the search above
        while desired_result == 'no':
            print("\nPlease manually search the information for this song (be as specific as possible): ")
            manual_search = str(input())
            song_uri_search(manual_search)
                
            #ask if another search is necessary
            print("\nWould you like to make another search? Please type in 'yes' or 'no': ")
            another_search = str(input())
                
            #ensure request for another search is valid
            while (another_search != 'yes')  and (another_search != 'no'):
                print("\nPlease give a valid input. Type either 'yes' or 'no': ")
                another_search = str(input())
                
            if another_search == "no":
                desired_result = 'yes'
            if another_search == "yes":
                desired_result = 'no'
            
        #the index of the song being searched, obtained from uri_df using song and album titles from data_to_clean
        missing_song_index = uri_df[(uri_df['song']==data_to_clean.iloc[i]['song']) & (uri_df['album']==data_to_clean.iloc[i]['album'])].index.values[0]
            
        #obtain explicit status of the song. Have user input the status because numerous songs can result from the search
        print("\nPlease copy and paste the explicit status of your selected song.")
        print("Alternatively, type in 'True' or 'False' (make sure the first character is capitalized): ")
        explicit_status = str(input())
            
        #check if explicit_status is valid
        while (explicit_status != "True")  and (explicit_status != "False"):
            print("\nPlease give a valid input. Type either 'True' or 'False': ")
            explicit_status = str(input())
            
        #to convert the string to a boolean
        explicit_status = eval(explicit_status)
            
        #obtain URI of the song. Have user input the URI because numerous songs can result from the search
        print("\nPlease copy and paste the entire URI for your selected song here: ")
        uri = str(input())
            
        #to give the user a chance to re-enter the URI in case they mispelled it
        print("\nDouble check that your URI is correct. Ready to confirm? Please enter 'yes' or 'no': ")
        confirmation = str(input())
            
        #check if confirmation is valid
        while (confirmation != 'yes')  and (confirmation != 'no'):
            print("\nPlease give a valid input. Type either 'yes' or 'no': ")
            confirmation = str(input())
            
        #ask for user to input URI again if they do not confirm they want to move foward. Continue asking after every input for uri
        if confirmation == 'no':
            print("\nPlease retype your URI here: ")
            uri = str(input())
                
            print("\nDouble check that your URI is correct. Ready to confirm? Please enter 'yes' or 'no': ")
            confirmation = str(input())
                
        #edit the uri dataframe!
        uri_df.loc[missing_song_index]['explicit'] = explicit_status
        uri_df.loc[missing_song_index]['uri'] = uri
            
        print("\nThe URI/explicit status for " + data_to_clean.loc[i]['song'] + " by " + artist_to_search + " is now updated on the uri_df!")
            
    #create a dataframe with all songs that have no URI
    data_to_clean = uri_df[uri_df['uri'] == ""]
    data_to_clean.reset_index(drop=True, inplace=True)
    
    print("\nAll URI/explicit statuses are accounted for!")


def getTrackFeatures(track_id):
    """
    Returns a list of selected information from Spotify's API given a song's URI

    Parameters:
        track_id (str): a track's URI
    
    Returns
        track (list): a list of song information including it's danceability, length, tempo, etc. 
    """
    md = sp.track(track_id)
    features = sp.audio_features(track_id)
    
    #meta data
    name = md['name']
    album = md['album']['name']
    artist = md['album']['artists'][0]['name']
    release_date = md['album']['release_date']
    length = md['duration_ms']
    popularity = md['popularity']
    
    #features from the data
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    key = features[0]['key']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    mode = features[0]['mode']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']
    valence = features[0]['valence']
    
    #putting it all together
    track = [name, album, artist, release_date, length, popularity, 
             acousticness, danceability, energy, instrumentalness, key,
            liveness, loudness, mode, speechiness, 
             tempo, time_signature, valence]
    return track

def ms_to_time(ms):
    """
    Converts milliseconds to time in "minute:secconds:millisecond" format

    Parameters:
        milliseconds (str): the length of a song in milliseconds
    
    Returns
        song_length (str): the length of a song converted into min:sec:ms format 
    """
    millis = ms
    seconds=(millis/1000)%60
    seconds = int(seconds)
    minutes=(millis/(1000*60))%60
    minutes = int(minutes)
    
    #a string will be returned so add 0 before songs with length < 10 mins so that songs above 10 mins won't be misordered when ordering by min:sec:ms format
    if minutes < 10:
        return "0%d:%d:%d" % (minutes, seconds, millis)
    else:
        return "%d:%d:%d" % (minutes, seconds, millis)