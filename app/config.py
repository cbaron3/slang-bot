import os
# Do not import api secrets if we are in Heroku environment
# This is to avoid having to push API secrets to git
if 'HEROKU' not in os.environ:
    from api_secret import *

class PRAWConfig:
    def __init__(self, user_agent, client_id, secret, username, password):
      self.user_agent = user_agent
      self.client_id = client_id
      self.secret = secret
      self.username = username
      self.password = password

class Config(object):
    # If not set fall back to production for safety
    FLASK_ENV =  os.getenv('FLASK_ENV', 'production')
    # Set FLASK_SECRET on your production Environment
    SECRET_KEY = os.getenv('FLASK_SECRET', 'Secret')

    # Directory formatting
    APP_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.dirname(APP_DIR)
    DIST_DIR = os.path.join(ROOT_DIR, 'dist')
    if not os.path.exists(DIST_DIR):
        raise Exception(
            'DIST_DIR not found: {}'.format(DIST_DIR))
    
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
    # Database work
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
