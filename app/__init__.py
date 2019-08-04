from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from redis import Redis
import rq

# Flask instance
app = Flask(__name__)
app.config.from_object(Config)

# Redis
app.redis = Redis.from_url( app.config['REDIS_URL'])
app.task_queue = rq.Queue('reddit-tasks', connection=app.redis)

# Database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Avoid circular dependencies
from app import routes
from app import models
