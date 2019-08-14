import time
import praw
import datetime
import pytz
import sys

from flask import jsonify

from app import db
from app.models import Request
from app.slang import define 
from app.config import PRAWConfig



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
        dots = '.'
        for comment in poll_subreddits.stream.comments():
            if keyphrase in comment.body:
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
                            user=comment.author.name,
                            subreddit=comment.permalink.split('/')[2],
                            url='https://reddit.com' + comment.permalink,
                            word=title
                        )

                        db.session.add(req)
                        db.session.commit()
                        print("Request added. req id={}".format(req.id))
                    except Exception as e:
                        print(str(e))
                print('Polling' + dots)

                if dots == '...':
                    dots = '.'
                else:
                    dots += '.'
                    
            print('Polling' + dots)

            if dots == '...':
                dots = '.'
            else:
                dots += '.'

            time.sleep(1)