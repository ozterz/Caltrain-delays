import csv
import os
import pandas as pd 
import re

#collect files from my local machine into Python
from pathlib import Path
cwd = Path(__file__).parent
start_file = Path.joinpath(cwd, "analyze_tweets.csv")
tweets = pd.read_csv(start_file)

#create new columns for clean data
if "clean_route" not in tweets.columns:
    tweets.insert(3, "clean_route", None, allow_duplicates = True)
    tweets.insert(5, "clean_delay", None, allow_duplicates = True)
    tweets.insert(7, "clean_terminated", None, allow_duplicates = True)

for index, search in enumerate(tweets["route"]):
    flag = r"#"
    clean_route = re.sub(flag, "", search)
    tweets.at[index, "clean_route"] = clean_route

for index, search in enumerate(tweets["delay_length"]):
    filter = r"\D|[aA-zZ]"
    if type(search) == float:
        search = str(search)
    clean_mins = re.sub(filter, "", search)
    tweets.at[index, "clean_delay"] = clean_mins

for index, search in enumerate(tweets["terminated_train"]):
    flag_2 = r"terminated|annulled|canceled|cancelled"
    clean_term = re.sub(flag_2, "Yes", search)
    tweets.at[index, "clean_terminated"] = clean_term

tweets.to_csv(start_file)