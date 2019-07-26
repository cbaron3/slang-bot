web: gunicorn slangbot:app
worker: rq worker -u $REDIS_URL reddit-tasks