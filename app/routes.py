from app import app, db
from flask import jsonify
from app.tasks import PRAWConfig, poll_reddit
from flask import current_app, send_file
import os
from app.models import Request
from app.scraper.urbandict import define

@app.route('/')
def index_client():
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'index.html')
    return send_file(entry)

praw_config = PRAWConfig( user_agent=app.config['REDDIT_USER_AGENT'], 
                            client_id=app.config['REDDIT_CLIENT_ID'], 
                            secret=app.config['REDDIT_SECRET'],
                            username=app.config['REDDIT_USERNAME'],
                            password=app.config['REDDIT_PASSWORD'], )
                            
@app.route('/test')
def f():
    if app.task_queue.count == 0:
        job = app.task_queue.enqueue(f=poll_reddit, args=(['testingground4bots'],praw_config), job_timeout=-1)
    else:
        print('Background task already running')

    return "test"

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

@app.route("/table", methods=['GET'])
def table():
    BOOKS = [
        {
            'title': 'On the Road',
            'author': 'Jack Kerouac',
            'read': True
        },
        {
            'title': 'Harry Potter and the Philosopher\'s Stone',
            'author': 'J. K. Rowling',
            'read': False
        },
        {
            'title': 'Green Eggs and Ham',
            'author': 'Dr. Seuss',
            'read': True
        }
    ]
    try:
        requests=Request.query.all()
        results = []
        for e in requests:
            results.append(e.serialize())
        return jsonify({
            'status': 'success',
            'books': results
        })
    except Exception as e:
	    return(str(e))