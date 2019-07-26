from flask import Flask
from config import Config
from redis import Redis
import rq

# Flask instance
app = Flask(__name__)
app.config.from_object(Config)

app.redis = Redis.from_url( app.config['REDIS_URL'])
app.task_queue = rq.Queue('reddit-tasks', connection=app.redis)


# Avoid circular dependencies
from app import routes