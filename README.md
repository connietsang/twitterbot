A simple twitter bot which finds all relevant tweets fitting a given search query in the past 7 days and likes and retweets these tweets.

The minimum number of likes and retweets a tweet must have can be specified. Also filters out controversial tweets.

The script can be run every week on any Unix system using crontab 

My crontab specification: 0 18 * * WED cd ~/twitterbot && /usr/local/bin/python3.9 twitterbot.py
