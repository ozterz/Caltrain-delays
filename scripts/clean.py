import csv
import pandas as pd
import os

#read local file into Python to be manipulated
from pathlib import Path
cwd = Path(__file__).parent
localfile = Path.joinpath(cwd, "filtered_tweets.csv")
all_tweets = pd.read_csv(localfile)

#create new column for time
all_tweets.insert(2, "time", None, allow_duplicates = True)

#delete merged index (it was off)
del all_tweets["Unnamed: 0"]

#turn dates from UTC to PST time 
from datetime import datetime
from pytz import timezone

UTC = timezone("UTC")
PST = timezone("America/Los_Angeles")

#converts UTC to PST & creates 2 different date and time strings
for tweet in all_tweets.index:
    utc_time = datetime.strptime(all_tweets["created_at"][tweet], "%Y-%m-%d %H:%M:%S+00:00") #read in the created_at string into a datetime object
    utc_time = utc_time.replace(tzinfo = UTC) #let the datetime object know that the timezone is UTC
    pst_time = utc_time.astimezone(PST) #create a clone of the datetime object and convert it to PST
    date = pst_time.strftime("%Y-%m-%d") #the cloned datetime object spits out a string with the date in YYYY-MM-DD format
    time = pst_time.strftime("%H:%M:%S") #the cloned datetime object spits out a string with the time in HH:MM:SS format
    
    #fill columns with updated time data 
    all_tweets["created_at"][tweet] = date 
    all_tweets["time"][tweet] = time

all_tweets.to_csv("filtered_tweets.csv")