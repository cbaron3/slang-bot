# App module
from app import app
from app.tasks import PRAWConfig, poll_reddit

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