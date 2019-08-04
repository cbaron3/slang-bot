# App module
from app import app, db
from app.tasks import PRAWConfig, poll_reddit
from app.models import Request
from flask import jsonify

praw_config = PRAWConfig( user_agent=app.config['REDDIT_USER_AGENT'], 
                            client_id=app.config['REDDIT_CLIENT_ID'], 
                            secret=app.config['REDDIT_SECRET'],
                            username=app.config['REDDIT_USERNAME'],
                            password=app.config['REDDIT_PASSWORD'], )

@app.route('/')
@app.route('/index')
def index():
    # Enqueue reddit worker
    if app.task_queue.count == 0:
        job = app.task_queue.enqueue(f=poll_reddit, args=(['testingground4bots'],praw_config), job_timeout=-1)
    else:
        print('Background task already running')
    # Check for ui updates
    # Publish ui for any new requests
    return "Hello, World!"

# route to test db
@app.route('/db')
def db_test():
    try:

        req=Request(
            user="Carl",
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
        return "Request added. req id={}".format(req.id)
    except Exception as e:
	    return(str(e))

@app.route("/getall")
def get_all():
    try:
        requests=Request.query.all()
        return  jsonify([e.serialize() for e in requests])
    except Exception as e:
	    return(str(e))