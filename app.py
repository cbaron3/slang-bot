from flask import Flask
import os
from flask import request, flash
from multiprocessing import Process, Value

# Time
import pytz
import datetime
import praw
import time

# Redis and redis queue
from redis import Redis
import rq
from rq import get_current_job

from urbandict import define


if 'HEROKU' in os.environ:
    reddit_user_agent = os.environ.get('REDDIT_USER_AGENT')
    reddit_client_id = os.environ.get('REDDIT_CLIENT_ID')
    reddit_secret = os.environ.get('REDDIT_SECRET')
    reddit_username = os.environ.get('REDDIT_USERNAME')
    reddit_password = os.environ.get('REDDIT_PASSWORD')
else:
    from api_secret import *


START_TIME = datetime.datetime.now(tz=pytz.utc).timestamp() 
REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'

app = Flask(__name__)
app.redis = Redis.from_url(REDIS_URL)
app.task_queue = rq.Queue('reddit-tasks', connection=app.redis)

reddit = praw.Reddit( user_agent=reddit_user_agent, client_id=reddit_client_id, client_secret=reddit_secret,
                            username=reddit_username, password=reddit_password )

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
        top_posts.append( t.selftext )

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

def bot_invoke( ):
    subreddit = reddit.subreddit('testingground4bots')
    keyphrase = '!slang-bot'

    while True:
        print('Bot task running')
        for comment in subreddit.stream.comments():
            if keyphrase in comment.body:
                # TODO: Get user who submitted the post for storing in database
                print(comment.body)
                print(comment.author)

                term = comment.body.replace( keyphrase, '' )
                term.strip()

                if term != '' and comment.created_utc > START_TIME:
                    try:
                        title, meaning, example = define(term) 
                        print( title, meaning, example)
                        comment.reply( "Slang Bot defines " + title + " as : \n" + meaning )
                    except:
                        print('To frequent')
        time.sleep(1)


@app.route('/')
def index():
    """Return homepage."""
    if app.task_queue.count == 0:
        job = app.task_queue.enqueue(bot_invoke, job_timeout=-1)
    else:
        print('Background task already running')
    return "Hello, World!"

if __name__ == '__main__':
    app.run(use_reloader=False)