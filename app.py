from flask import Flask
import os
from secrets import *
import praw

from urbandict import define

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
    title, meaning, example = define('yeet')
    print( title, meaning, example)
    return title + " " + meaning + " " + example

if __name__ == '__main__':
    app.run()