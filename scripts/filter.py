import csv
import os
import pandas as pd
import re 

from pathlib import Path
cwd = Path(__file__).parent
localfile = Path.joinpath(cwd, "main_account_data.csv")
outfile = Path.joinpath(cwd, "filtered_tweets.csv")
alert_acct_data = Path.joinpath(cwd, "alert_acct_tweets.csv")

mainacct_tweets = pd.read_csv(localfile)
alert_tweets = pd.read_csv(alert_acct_data)

mainacct_tweets = pd.concat([mainacct_tweets, alert_tweets])

include = "[0-9]+[\'\"]|[-][0-9]+|delay|\blate\b|\bwaiting\b|\bterminated\b|\bstopped\b|\bemergency\b|\bstruck\b|\bc[as]ncel+ed\b|\bbroke down\b|\bdisabled\b|\bfatality\b|\bkilled\b|\bslow\b|\bdown\b|\bsingle track\b|\bsingle tracking\b|\boff loading\b|\bdrop\b|\bdead\b|\bstop\b|\bstalled\b|\bmechanical issue\b|\bincident\b|\bholding\b|\brestriction\b|\bannulled\b|\bnot running\b|\bclosed\b"
exclude = tuple(["@", "RT"])
exclude_regex = r"\bBoard of Directors\b|\bPublic Session\b|\bzoom\b"

include_mask = mainacct_tweets["text"].str.contains(include)
exclude_mask = mainacct_tweets["text"].str.startswith(exclude)
exclude_words = mainacct_tweets["text"].str.contains(exclude_regex)

filtered_tweets = mainacct_tweets[(include_mask & ~exclude_mask) & ~exclude_words]

filtered_tweets.to_csv(outfile)