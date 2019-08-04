import time
import praw
import datetime
import pytz
import sys
from app import db
from flask import jsonify
from app.models import Request

from app.scraper.urbandict import define

class PRAWConfig:
    def __init__(self, user_agent, client_id, secret, username, password):
      self.user_agent = user_agent
      self.client_id = client_id
      self.secret = secret
      self.username = username
      self.password = password

def poll_reddit( sub_list, config ):
    """ Pass in a list of subreddit names to poll for the keyphrase !slangbot"""
    keyphrase = '!slangbot'
    subreddits = '+'.join(sub_list)
    print( 'Polling the following subreddits: {}'.format(subreddits) )
    
    # Reddit api wrapper init
    reddit = praw.Reddit( user_agent=config.user_agent, client_id=config.client_id, 
                            client_secret=config.secret, username=config.username, 
                            password=config.password )
    print( 'PRAW Read/Write privileges active? {}'.format( str( not reddit.read_only ) ) )

    # Start time of bot
    START_TIME = datetime.datetime.now( tz=pytz.utc ).timestamp() 

    # Subs to poll
    poll_subreddits = reddit.subreddit( 'testingground4bots' )
    while True:
        print('Polling for keyphrase {}'.format( keyphrase ) )
        for comment in poll_subreddits.stream.comments():
            if keyphrase in comment.body:
                # IMPROVE: Consolidate prints into one formatted print
                print(comment.body)
                print(comment.created_utc)
                print(comment.author)
                print(comment.subreddit)
                print(comment.link_id)
                # TODO: Log this data to a database. Then in home route, add another worker task
                # to check the database every so often

                # Extract term by replacing keyphrase from comment body and striping whitespace
                term = comment.body.replace( keyphrase, '' )
                term.strip()
                
                # Only reply if term is a non-empty string and the comment was created after the bot started running
                if term != '' and comment.created_utc > START_TIME:
                    # IMPROVE: Format the prints better
                    # TODO: Fix define function call. Causes an error that is blocked right now by try/except
                    title, meaning, example = define(term) 
                    print( title, meaning, example)
                    
                    try:
                        comment.reply( "Slang Bot defines " + title + " as : \n" + meaning )
                        req = Request(
                            user=comment.author,
                            created_time="Now",
                            received_time="Later",
                            subreddit="r",
                            url="urltest",
                            word="word",
                            meaning="asdf",
                            example="rly"
                        )

                        db.session.add(req)
                        db.session.commit()
                        print("Request added. req id={}".format(req.id))
                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
        time.sleep(1)

if __name__ == "__main__":
    title, meaning, example = define('yeet') 
    print( title, meaning, example )