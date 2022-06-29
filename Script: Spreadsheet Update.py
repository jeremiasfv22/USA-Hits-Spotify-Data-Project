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

################################################################################
####                                                                        ####
####     importing Google Sheet with new songs and new weekly streams       ####
####                                                                        ####
################################################################################

#service account
sa = gspread.service_account("gspread_service_account.json")

#sheet
sh = sa.open("HITS Streaming Songs")

#worksheet
wks = sh.worksheet("HITS Streaming Songs")

#uses all values in the worksheet for the data frame
gsheets_df_updated = pd.DataFrame(wks.get_all_values())

header = gsheets_df_updated.iloc[0] #isolate first row as header
gsheets_df_updated = gsheets_df_updated[1:] #get rid of header in original df
gsheets_df_updated.columns = header

gsheets_df_updated = gsheets_df_updated.set_index('index') #set 'index' as index

gsheets_df_updated['title'] = gsheets_df_updated['title'].str.rstrip(' ')
gsheets_df_updated['artist'] = gsheets_df_updated['artist'].str.rstrip(' ')
gsheets_df_updated['album'] = gsheets_df_updated['album'].str.rstrip(' ')

#convert index from string to int
gsheets_df_updated.index = gsheets_df_updated.index.astype(int)

#fill in blank values with 0
gsheets_df_updated = gsheets_df_updated.replace(r'^\s*$', "0", regex=True)

#convert all numbers-as-strings to numbers from row 4 in python's index and onwards
for col_name in gsheets_df_updated.columns.to_list()[4:len(gsheets_df_updated.columns.to_list())]:
    
    #get rid of strings' commas and convert strings to integers
    gsheets_df_updated[col_name] = gsheets_df_updated[col_name].str.replace(',','').astype('int')

#######################################################################
####                                                               ####
####    importing non-updated version of "DF to Gspread" sheet     ####
####                                                               ####
#######################################################################

#dg to gspread worksheet
df2gspread_wks = sh.worksheet("DF to Gspread")

#uses all values in the worksheet for the data frame
df2gspread_wks = pd.DataFrame(df2gspread_wks.get_all_values())

header = df2gspread_wks.iloc[0] #isolate first row as header
df2gspread_wks = df2gspread_wks[1:] #get rid of header in original df
df2gspread_wks.columns = header

df2gspread_wks = df2gspread_wks.set_index('index') #set 'index' as index

#convert index from string to int
df2gspread_wks.index = df2gspread_wks.index.astype(int)

#convert all numbers-as-strings to numbers
df2gspread_wks.loc[:,'streams_2017_to_present':'units'] = df2gspread_wks.loc[:,'streams_2017_to_present':'units'].astype(int)

##############################################
####                                      ####
####            join all data             ####
####                                      ####
##############################################

final_df_updated = pd.concat([gsheets_df_updated, df2gspread_wks.loc[:,'uri':] ],
                            axis=1)

final_df_updated = final_df_updated.replace(np.nan, "")
final_df_updated.index = final_df_updated.index.astype(int)

#############################################
####                                     ####
####          Getting song URIs          ####
####                                     ####
#############################################

new_uri_list = []

[new_uri_list.append(search_for_URI(final_df_updated.loc[n+1,'title':'album'])) 
for n in range(len(final_df_updated.loc[:])) if final_df_updated.iloc[n]['uri'] == ""]

#convert list to DataFrame
new_uri_df = pd.DataFrame(new_uri_list,columns=["song","artist","album","explicit","uri"])

#change index to fit the updated Google Sheet's index
new_uri_df.index = range(len(final_df_updated)-len(new_uri_df)+1,len(final_df_updated)+1)

#add name for index column
new_uri_df.index.name = 'index'

#create a dataframe with all songs that have no URI
data_to_clean = new_uri_df[new_uri_df['uri'] == ""]
data_to_clean.index = range(1,len(data_to_clean)+1) #reset index

##################################################
####                                          ####
####     (if necessary) manually add URIs     ####
####                                          ####
##################################################

if len(data_to_clean) > 0:
    data_cleaning_func(data_to_clean, new_uri_df)

print("Success! The entire dataframe is now updated with song URIs! Please wait for Spotify's track features to be retreived.")

##############################################
####                                      ####
####   Getting Spotify's track features   ####
####                                      ####
##############################################

#Get track features for all new tracks, append to a list
new_track_features_list = []

[new_track_features_list.append(getTrackFeatures(new_uri_df['uri'][i]) ) for i in new_uri_df.index]

#Convert list to DataFrame

new_api_info_df = pd.DataFrame(new_track_features_list ,columns=['name','album','artist',
    'release_date','length','popularity','acousticness','danceability',
    'energy','instrumentalness','key','liveness','loudness','mode',
    'speechiness','tempo','time_signature','valence'])

#change index to fit the updated Google Sheet's index
new_api_info_df.index = range(len(final_df_updated)-len(new_api_info_df)+1,len(final_df_updated)+1)

#change release_date to date format
new_api_info_df['release_date'] = pd.to_datetime(new_api_info_df['release_date'])

#############################################
####                                     ####
####    concat new variables together    ####
####                                     ####
#############################################

#concatinate all new variables into a final dataframe titled new_variables_to_add
new_variables_to_add = pd.concat(
    
    #this gets all the new song streaming data from the Google Sheets
    [final_df_updated.loc[len(final_df_updated)-len(new_api_info_df)+1:len(final_df_updated)+1,:'units'],
    new_uri_df.loc[:,'uri'],
    new_api_info_df.loc[:,'release_date':'valence'],
    new_uri_df.loc[:,'explicit']
    ],
    axis=1)

#add variables_to_add to the end of the final_df_updated
df_to_save = pd.concat([
    final_df_updated.loc[:len(final_df_updated)-len(new_api_info_df),:],
    new_variables_to_add
])

#add name for index column
df_to_save.index.name = 'index'

#add variables_to_add to the end of the final_df_updated
df_to_save = pd.concat([
    final_df_updated.loc[:len(final_df_updated)-len(new_api_info_df),:],
    new_variables_to_add
])

#add name for index column
df_to_save.index.name = 'index'

#reset index and convert all integers/float/dates to strings in preparation to convert to a Google Shet
df_to_save = df_to_save.reset_index()
df_to_save = df_to_save.astype(str)

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

d2g.upload(df_to_save, spreadsheet_key, wks_name, credentials = credentials,
          row_names=False)