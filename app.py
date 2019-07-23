from flask import Flask
import os
from secrets import *
import praw

import urllib, json

_URBANDICT_URL = "http://api.urbandictionary.com/v0/define?term="

def _run_urbandict(search):
    safe_search = ""
    words = ' '.join(search.split()).split(' ')
    for idx, word in enumerate(words):
        if len(words) == idx+1:
            safe_search += "%s" % urllib.parse.quote_plus(word)
        else:
            safe_search += "%s+" % urllib.parse.quote_plus(word)
    with urllib.request.urlopen("http://www.python.org") as url:
        print(url.read())
        # Need to parse html for div meaning and example
        # may need to parse all responses to find most upvoted
        # filters: top-response, most-upvotes, best-vote-ratio
        #return json.loads(url.read())

def urbandict(word):
    return _run_urbandict(word)

app = Flask(__name__)

@app.route('/')
def index():
    """Return homepage."""
    return "Hello, World!"

@app.route('/praw')
def p():
    reddit = praw.Reddit( user_agent=reddit_user_agent, client_id=reddit_client_id, client_secret=reddit_secret,
                            username=reddit_username, password=reddit_password )
    print( reddit.read_only )
    # print( reddit.user.me() )
    sub = reddit.subreddit('all')
    print(sub.top())
    return "PRAW Testing endpoint"

@app.route('/urban')
def u():
    print( urbandict('netflix') )
    return "Urban Dict Testing endpoint"

if __name__ == '__main__':
    app.run()