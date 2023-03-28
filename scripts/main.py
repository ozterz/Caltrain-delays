import tweepy
import os
import csv

bearer_token = os.environ["BEARER_TOKEN"]
client = tweepy.Client(bearer_token = bearer_token, wait_on_rate_limit = True)

with open("main_account_data.csv", mode = "w") as tweet_file:
    tweet_writer = csv.writer(tweet_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
    tweet_writer.writerow(["created_at","id","text"])

for item in tweepy.Paginator(client.search_all_tweets, query = 'from:Caltrain', max_results = 500, start_time = "2006-03-21T00:00:00Z", end_time = "2020-10-01T00:00:00Z", tweet_fields = ["created_at","id","text"]):
    for tweets in item.data:
        with open("main_account_data.csv", mode = "a") as tweet_file:
            tweet_writer = csv.writer(tweet_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            tweet_writer.writerow([tweets["created_at"], tweets["id"], tweets["text"]])