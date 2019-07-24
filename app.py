from flask import Flask
import os
from secrets import *
import praw
from flask import request, flash

from urbandict import define

app = Flask(__name__)

reddit = praw.Reddit( user_agent=reddit_user_agent, client_id=reddit_client_id, client_secret=reddit_secret,
                            username=reddit_username, password=reddit_password )
print( reddit.read_only )

@app.route('/')
def index():
    """Return homepage."""
    return "Hello, World!"

@app.route('/praw')
def p():
    subr = request.args.get('sub')

    if subr == None:
        # TODO: Need secret key
        flash('Specify subreddit with /urban?sub=...')

    sub = reddit.subreddit(subr)
    top = sub.top() 

    top_posts = []

    for t in top:
        top_posts.append(t.selftext)

    return " ".join( top_posts )

@app.route('/urban')
def u():
    term = request.args.get('term')

    if term == None:
        # TODO: Need secret key
        flash('Specify term with /urban?term=...')

    title, meaning, example = define(term)
    print( title, meaning, example)
    return title + " " + meaning + " " + example

if __name__ == '__main__':
    app.run()