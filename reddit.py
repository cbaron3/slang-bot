import praw
import time
from secrets import *
from rq import get_current_job

def bot_invoke():
    reddit = praw.Reddit( user_agent=reddit_user_agent, client_id=reddit_client_id, client_secret=reddit_secret,
                            username=reddit_username, password=reddit_password )

    while True:
        job = get_current_job()
        print('Reddit bot running')
        time.sleep(1)


if __name__ == "__main__":
    sub = reddit.subreddit('all')
    top = sub.top() 

    top_posts = []

    for t in top:
        top_posts.append( t.selftext )

    print( " ".join( top_posts ) )