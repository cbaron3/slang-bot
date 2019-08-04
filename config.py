import os 

basedir = os.path.abspath(os.path.dirname(__file__))

if 'HEROKU' not in os.environ:
    from api_secret import *

class Config(object):
    # Reddit api secrets
    if 'HEROKU' in os.environ:
        REDDIT_USER_AGENT = os.environ.get('REDDIT_USER_AGENT')
        REDDIT_CLIENT_ID = os.environ.get('REDDIT_CLIENT_ID')
        REDDIT_SECRET = os.environ.get('REDDIT_SECRET')
        REDDIT_USERNAME = os.environ.get('REDDIT_USERNAME')
        REDDIT_PASSWORD = os.environ.get('REDDIT_PASSWORD')
    else:
        REDDIT_USER_AGENT = reddit_user_agent
        REDDIT_CLIENT_ID = reddit_client_id
        REDDIT_SECRET = reddit_secret
        REDDIT_USERNAME = reddit_username
        REDDIT_PASSWORD = reddit_password
    # Redis url
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    # For database work
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']