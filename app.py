from flask import Flask
import os
from secrets import *
import praw

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

if __name__ == '__main__':
    app.run()