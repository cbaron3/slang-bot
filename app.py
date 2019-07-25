from flask import Flask
import os
from flask import request, flash
from multiprocessing import Process, Value

# Time
import pytz
import datetime

# Redis and redis queue
from redis import Redis
import rq


from task import example
#from reddit import bot_invoke
from urbandict import define

app = Flask(__name__)

if 'HEROKU' in os.environ:
    reddit_user_agent = os.environ.get('REDDIT_USER_AGENT')
    reddit_client_id = os.environ.get('REDDIT_CLIENT_ID')
    reddit_secret = os.environ.get('REDDIT_SECRET')
    reddit_username = os.environ.get('REDDIT_USERNAME')
    reddit_password = os.environ.get('REDDIT_PASSWORD')

import praw
import time
from api_secret import *
from rq import get_current_job

def bott( t ):
    while True:
        job = get_current_job()
        print('Starting task')
        for i in range(t):
            job.meta['progress'] = 100.0 * i / t
            job.save_meta()
            print(i)
            time.sleep(1)
        job.meta['progress'] = 100
        job.save_meta()
        print('Task completed')

# def bot_invoke( ):
#     while True:
#         print('bot backend running')
#         for comment in subreddit.stream.comments():
#             if keyphrase in comment.body:
#                 # If keyphrase is in body, remove keyphrase from body and use rest of text as term
#                 # TODO: GEt user who submitted
#                 # Track already visited bot requests. Could use timestamp
#                 print(comment.body)
#                 print( START_TIME, comment.created_utc)
#                 term = comment.body.replace( keyphrase, '' )
#                 term.strip()

#                 if term != '' and comment.created_utc > START_TIME:
#                     try:
#                         title, meaning, example = define(term) 
#                         print( title, meaning, example)
#                         comment.reply( "Slang Bot defines " + title + " as : \n" + meaning )
#                     except:
#                         print('To frequent')
#         print('bot backend running')
#         time.sleep(1)

print(reddit_user_agent)
reddit = praw.Reddit( user_agent=reddit_user_agent, client_id=reddit_client_id, client_secret=reddit_secret,
                            username=reddit_username, password=reddit_password )

START_TIME = datetime.datetime.now(tz=pytz.utc).timestamp() 
REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'

app.redis = Redis.from_url(REDIS_URL)
app.task_queue = rq.Queue('reddit-tasks', connection=app.redis)


# @app.route('/praw')
# def p():
#     subr = request.args.get('sub')

#     if subr == None:
#         # TODO: Need secret key
#         flash('Specify subreddit with /urban?sub=...')

#     sub = reddit.subreddit(subr)
#     top = sub.top() 

#     top_posts = []

#     for t in top:
#         top_posts.append( t.selftext )

#     return " ".join( top_posts )

@app.route('/urban')
def u():
    term = request.args.get('term')

    if term == None:
        # TODO: Need secret key
        flash('Specify term with /urban?term=...')

    title, meaning, example = define(term)
    print( title, meaning, example)
    return title + " " + meaning + " " + example

subreddit = reddit.subreddit('testingground4bots')
keyphrase = '!slang-bot'

def bot_invoke( ):
    while True:
        print('bot backend running')
        for comment in subreddit.stream.comments():
            if keyphrase in comment.body:
                # If keyphrase is in body, remove keyphrase from body and use rest of text as term
                # TODO: GEt user who submitted
                # Track already visited bot requests. Could use timestamp
                print(comment.body)
                print( START_TIME, comment.created_utc)
                term = comment.body.replace( keyphrase, '' )
                term.strip()

                if term != '' and comment.created_utc > START_TIME:
                    try:
                        title, meaning, example = define(term) 
                        print( title, meaning, example)
                        comment.reply( "Slang Bot defines " + title + " as : \n" + meaning )
                    except:
                        print('To frequent')
        print('bot backend running')
        time.sleep(1)


@app.route('/')
def index():
    """Return homepage."""
    job = app.task_queue.enqueue(bot_invoke)

    return "Hello, World!"

if __name__ == '__main__':
    recording_on = Value('b', True)
    #p = Process(target=bot_invoke, args=())
    #p.start()  
    app.run(debug=True, use_reloader=False)
    #job = app.task_queue.enqueue('tasks.example', 23)
    #p.join()