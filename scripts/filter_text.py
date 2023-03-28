import csv
import os
import pandas as pd
import re 

#collect files from my local machine into Python
from pathlib import Path
cwd = Path(__file__).parent
filtered_tweets = Path.joinpath(cwd, "NEW_filtered_tweets.csv")
outfile = Path.joinpath(cwd, "analyze_tweets.csv")
start_file = pd.read_csv(filtered_tweets)

#filter for words that I want to pull from the "text" column
route_num = r"\bNo. [0-9]\b|\b#[0-9]\b|[0-9]{3}|#[A-Za-z]{2}[0-9]+\b|\b[A-Za-z]{2}[0-9]\b|\b[0-9]{3} -"
minutes_delayed = r"-?[0-9]+[\'\"]|[-][0-9]+|[0-9]{2}.|[0-9]{2,3} min"
delay_reason = r"due to\b|\bbecause of\b|\bfollowing\b|\b"
station = r"@?[A-Z][aA-zZ][A-Z]\b"
terminated = r"terminated\b|\bwill terminate\b|\bis terminating\b|\bcanceled\b|\bcancelled\b|\bannulled\b"
grab_reason = r"(?<=due to )(\w| )*(?:.)|(?<=because of )(\w| )*(?:.)|(?<=following )(\w| )*(?:.)"

#open & write to a new file the words that I'm going to pull
with open("analyze_tweets.csv", mode = "w") as new_file:    
        outfile = csv.writer(new_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        outfile.writerow(["created_at","time","route","station","delay_length","delay_reason","terminated_train"])

        for tweet in start_file.index:
                if re.search(route_num, start_file.loc[tweet,"text"]):
                    route_str = start_file.loc[tweet,"text"]
                    found_route = re.findall(route_num, route_str)
                    found_route_substr = re.split(route_num, route_str)
                    found_route_substr = found_route_substr[1:]

                    for index in range(0,found_route_substr.__len__()):
                        found_mins = None
                        found_reason = None
                        found_station = None
                        found_term = None

                        if re.search(minutes_delayed, found_route_substr[index]):
                            min_str = found_route_substr[index]
                            found_mins = re.findall(minutes_delayed, min_str)[0]
                            if re.findall(minutes_delayed, min_str).__len__() > 1:
                                    print(min_str)
                                    print(re.findall(minutes_delayed, min_str))
                        else:
                            found_mins = "" 

                        if re.search(delay_reason, found_route_substr[index], flags = re.IGNORECASE):
                            reason_str = found_route_substr[index]
                            found_iter = re.finditer(grab_reason, reason_str, flags = re.IGNORECASE)
                            for search in found_iter:
                                found_reason = search.string[search.start():search.end()]
                            if found_reason == None:
                                found_reason = ""
                        else: 
                             found_reason = ""
                    
                        if re.search(station, found_route_substr[index]):
                            station_str = found_route_substr[index]
                            found_station = re.findall(station, station_str)[0]
                        else:
                             found_station = ""
                            
                        if re.search(terminated, found_route_substr[index]):
                            term_str = found_route_substr[index]
                            found_term = re.findall(terminated, term_str)[0]
                        else:
                             found_term = "No"

                        if found_mins != "" or found_reason != "" or found_term != "No":
                            outfile.writerow([start_file.loc[tweet,"created_at"],start_file.loc[tweet,"time"],found_route[index],found_station,found_mins,found_reason,found_term])