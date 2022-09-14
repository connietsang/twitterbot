A simple Twitter bot Python script which finds all relevant and original tweets fitting a given search query in the past 7 days and likes and retweets them. Uses Twitter API v2. 

API keys, bearer token, and access tokens should be specified in an .env file

The minimum number of likes and retweets a tweet must have, and the interval the script waits before liking/rting the next tweet can be specified. Also filters out controversial tweets.

The script can be run every week on any Unix system using crontab 

My crontab specification: 0 18 * * WED cd ~/twitterbot && /usr/local/bin/python3.9 twitterbot.py (runs the script every Wednesday at 6PM)
