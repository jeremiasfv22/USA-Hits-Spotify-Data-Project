"""
It is recommended practice to utilize a virtual environment. Use the following instructions (for Mac computers):
    pip install virtualenv 
    ls                                                               #to check what's in your directory
    cd "INSERT_DESIRED_FOLDER/DESTINATION_TO WORK_FROM_HERE"
    python3 -m venv INSERT_VIRTUAL_ENVIRONMENT_NAME_HERE             #this creates the virtual environment

Before running, be sure to have the following installed:
    pip install spotipy
    pip install gspread
    pip install oauth2client
    pip install df2gspread
    pip install pandas
"""
from functions import *

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

#############################################
####                                     ####
####       Importing Google Sheet        ####
####                                     ####
#############################################

#service account
sa = gspread.service_account(filename="gspread_service_account.json")

#sheet
sh = sa.open("HITS Streaming Songs")

#worksheet
wks = sh.worksheet("HITS Streaming Songs")

#uses all values in the worksheet for the data frame
gsheets_df = pd.DataFrame(wks.get_all_values())

header = gsheets_df.iloc[0] #isolate first row as header
gsheets_df = gsheets_df[1:] #get rid of header in original df
gsheets_df.columns = header

#set 'index' as index
gsheets_df = gsheets_df.set_index('index')

gsheets_df['title'] = gsheets_df['title'].str.rstrip(' ')
gsheets_df['artist'] = gsheets_df['artist'].str.rstrip(' ')
gsheets_df['album'] = gsheets_df['album'].str.rstrip(' ')

#convert index from string to int
gsheets_df.index = gsheets_df.index.astype(int)

#fill in blank values with 0
gsheets_df = gsheets_df.replace(r'^\s*$', "0", regex=True)

#convert all numbers-as-strings to numbers from row 4 in python's index and onwards
for col_name in gsheets_df.columns.to_list()[4:len(gsheets_df.columns.to_list())]:
    
    #get rid of strings' commas and convert strings to integers
    gsheets_df[col_name] = gsheets_df[col_name].str.replace(',','').astype('int')
    
#turn peak_date strings to date format
gsheets_df['peak_date'] = pd.to_datetime(gsheets_df['peak_date'])

#############################################
####                                     ####
####          Getting song URIs          ####
####                                     ####
#############################################

#create a list of song info: song title, artist, album, explicit or not, track URI
#search_for_URI is defined in functions.py
uri_list = []
[uri_list.append(search_for_URI(gsheets_df.loc[song_info_index+1,'title':'album'])) for song_info_index in range(len(gsheets_df.loc[:]))]

#convert list to DataFrame
uri_df = pd.DataFrame(uri_list,columns=["song","artist","album","explicit","uri"])

#change index to start at 1
uri_df.index = range(1,len(uri_df)+1)

#create a dataframe with all songs that have no URI
data_to_clean = uri_df[uri_df['uri'] == ""]
data_to_clean.reset_index(drop=True, inplace=True)
             
print(missing_uri_detector(data_to_clean))
print("\n")

##################################################
####                                          ####
####     (if necessary) manually add URIs     ####
####                                          ####
##################################################

if len(data_to_clean) > 0:
    data_cleaning_func(data_to_clean, uri_df)

print("Success! The entire dataframe is now updated with song URIs! Please wait for Spotify's track features to be retreived.")

##############################################
####                                      ####
####   Getting Spotify's track features   ####
####                                      ####
##############################################

#Get track features for all tracks, append to a list
track_features = []
[track_features.append(getTrackFeatures(uri_df['uri'][i]) ) for i in range(1,len(uri_df['uri'])+1)]

#Convert list to DataFrame
api_info_df = pd.DataFrame(track_features,columns=['name','album','artist',
    'release_date','length','popularity','acousticness','danceability',
    'energy','instrumentalness','key','liveness','loudness','mode',
    'speechiness','tempo','time_signature','valence'])

#change index to start at one
api_info_df.index = range(1,len(api_info_df)+1)

#change release_date to date format
api_info_df['release_date'] = pd.to_datetime(api_info_df['release_date'])

##############################################
####                                      ####
####            join all data             ####
####                                      ####
##############################################

#concatinate all variables into a final dataframe
final_df = pd.concat([gsheets_df.loc[:,:], uri_df.loc[:,'uri'], api_info_df.loc[:,'release_date':'valence'], uri_df.loc[:,'explicit']]
            ,axis=1)

#reset index and convert all integers/float/dates to strings in preparation to convert to a Google Shet
final_df = final_df.reset_index()
final_df = final_df.astype(str)
    
###################################################
####                                           ####
####     Convert DataFrame to Google Sheet     ####
####                                           ####
###################################################

url = "https://docs.google.com/spreadsheets/d/165OdLYjLt4AgeqP5S5PunRonDkpp28nueHLFv994bPk/edit#gid=0"

spreadsheet_key = url.split("/")[-2]

wks_name = 'DF to Gspread'

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('gspread_service_account.json', scope)

gc = gspread.authorize(credentials)

d2g.upload(final_df, spreadsheet_key, wks_name, credentials = credentials, row_names=False)