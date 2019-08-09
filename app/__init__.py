import os
from flask import Flask, current_app, send_file
from flask_sqlalchemy import SQLAlchemy
from .api import api_bp
from .client import client_bp
from flask_cors import CORS
from redis import Redis
import rq



app = Flask(__name__, static_folder='../dist/static')
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
