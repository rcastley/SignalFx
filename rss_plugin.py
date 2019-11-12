#!/usr/bin/python

import feedparser
import time
import sys
import requests

# Feed name and URL
feed_name = 'BBC'
url = 'http://feeds.bbci.co.uk/news/rss.xml'

# Limit the number of posts to send
limit_items = 3

# Local DB for caching posts
db = '/tmp/feeds.db'
limit = 12 * 3600 * 1000

# Get the current time
current_time_millis = lambda: int(round(time.time() * 1000))
current_timestamp = current_time_millis()

# Check to see if RSS title is in local file DB
def post_is_in_db(title):
    with open(db, 'r') as database:
        for line in database:
            if title in line:
                return True
    return False

# Return true if the title is in the DB with a timestamp < limit
def post_is_in_db_with_old_timestamp(title):
    with open(db, 'r') as database:
        for line in database:
            if title in line:
                ts_as_string = line.split('|', 1)[1]
                ts = int(ts_as_string)
                if current_timestamp - ts < limit:
                    return True
    return False


# Get the feed data from the url
feed = feedparser.parse(url)

# Select headlines to print or skip
posts_to_print = []
posts_to_skip = []

for post in feed.entries:
    # if post is already in the database, skip it
    title = post.title
    if post_is_in_db_with_old_timestamp(title):
        posts_to_skip.append(title)
    else:
        posts_to_print.append(title)    

# Add posts to send to the database with the current timestamp
f = open(db, 'a')
for title in posts_to_print:
    if not post_is_in_db(title):
        f.write(title + "|" + str(current_timestamp) + "\n")
f.close

# SignalFx
endpoint = 'https://ingest.signalfx.com/v2/event'
org_access_token = 'xxx'
# Set headers
headers = {
    'Content-Type': 'application/json',
    'X-SF-TOKEN': org_access_token
}

# Send 5 posts to SFx Events Ingest
for title in posts_to_print[:limit_items]:
    print(title + "\n")
    # SFx JSON payload
    data = [{
        "category": "USER_DEFINED",
        "eventType": title,
        "dimensions": {
            "feed": feed_name
        }
    }]
    r = requests.post(endpoint, headers=headers, json=data)
