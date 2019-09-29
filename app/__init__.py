import os

# Load in environment settings
from dotenv import load_dotenv
from pathlib import Path
env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

# Creating the application
from flask import Flask
app = Flask(__name__, static_folder='../dist/static')

# Application API access configuration
from flask import Blueprint
from flask_restplus import Api

api_bp = Blueprint('api_bp', __name__, url_prefix='/api')
api_rest = Api(api_bp)

@api_bp.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response

app.register_blueprint(api_bp)

# Load project configuration
from .config import Config
app.logger.info('>>> {}'.format(Config.FLASK_ENV))
app.config.from_object('app.config.Config')

# Redis
from redis import Redis
import rq
app.redis = Redis.from_url( app.config['REDIS_URL'])
app.task_queue = rq.Queue('reddit-tasks', connection=app.redis)

# Handling cross origin resource handling
from flask_cors import CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Database object relational mapper for mapping PSQL calls to object notation
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create configuration for Reddit API access and begin subreddit polling task
from app.tasks import poll_reddit
from app.config import PRAWConfig

praw_config = PRAWConfig( user_agent=app.config['REDDIT_USER_AGENT'], 
                            client_id=app.config['REDDIT_CLIENT_ID'], 
                            secret=app.config['REDDIT_SECRET'],
                            username=app.config['REDDIT_USERNAME'],
                            password=app.config['REDDIT_PASSWORD'], )
                            
if app.task_queue.count == 0:
    job = app.task_queue.enqueue(f=poll_reddit, args=(['testingground4bots'],praw_config), job_timeout=-1)
    print('Enqueuing task')
else:
    print('Background task already running')
