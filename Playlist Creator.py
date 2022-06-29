#to access spotipy
import configparser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

#to clean data
import pandas as pd
import numpy as np

#to allow interaction with underlying operating system
import os

#to access google sheets with python
import gspread
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials

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

#get username:
username = "wsxf89bx2zlaopwpvtk2hrwa0"

#create a spotipy Object
scope = 'playlist-modify-public'
token = SpotifyOAuth(scope=scope, username=username)
sp = spotipy.Spotify(auth_manager=token)

#create the playlist 
playlist_name = "Streaming Hits - USA"
playlist_description = "Collecting of all songs that charted in the top 50 of the HITS Streaming Songs chart since 2017 ... for data science purposes lol ... to be coded into existance soon!!!! :)"
sp.user_playlist_create(user=username, name=playlist_name, public=True,description=playlist_description)

prePlaylist = sp.user_playlists(user=username)
playlist = prePlaylist['items'][0]['id']

#Google Sheets service account
sa = gspread.service_account("gspread_service_account.json")

#get sheet
sh = sa.open("HITS Streaming Songs")

#get worksheet
df2gspread_wks = sh.worksheet("DF to Gspread")

#uses all values in the worksheet for the data frame
df2gspread_wks = pd.DataFrame(df2gspread_wks.get_all_values())

header = df2gspread_wks.iloc[0] #isolate first row as header
df2gspread_wks = df2gspread_wks[1:] #get rid of header in original df
df2gspread_wks.columns = header

df2gspread_wks = df2gspread_wks.set_index('index') #set 'index' as index

tracks_to_add = list(df2gspread_wks['uri'])

while len(tracks_to_add) > 0:
    sp.user_playlist_add_tracks(user=username, playlist_id=playlist, tracks=tracks_to_add[0:100])
    tracks_to_add = tracks_to_add[100:]