import os
from flask import Flask, current_app, send_file

from .client import client_bp
from flask_cors import CORS
from redis import Redis
import rq
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv
load_dotenv()

# OR, explicitly providing path to '.env'
from pathlib import Path  # python3 only
env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__, static_folder='../dist/static')

from flask import Blueprint, current_app
from flask_restplus import Api


api_bp = Blueprint('api_bp', __name__, url_prefix='/api')
api_rest = Api(api_bp)


@api_bp.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response

app.register_blueprint(api_bp)
# app.register_blueprint(client_bp)

from .config import Config
app.logger.info('>>> {}'.format(Config.FLASK_ENV))
app.config.from_object('app.config.Config')

# Redis
app.redis = Redis.from_url( app.config['REDIS_URL'])
app.task_queue = rq.Queue('reddit-tasks', connection=app.redis)

CORS(app, resources={r'/*': {'origins': '*'}})

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)





from app import routes
