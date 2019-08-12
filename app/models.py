from app import db, api_rest
from flask_restplus import Resource
from flask import jsonify
# Database will store bot requests
# user, time, created, subreddit, link_id or url, body, meaning, example
# Could improve this by having a request store a reddit key and a urban dictionary key
# think that would be good for the future
class Request(db.Model):
    __tablename__ = 'requests'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    # Columns for the table. Gunna store everything as strings for simplicity
    user = db.Column(db.String())
    subreddit = db.Column(db.String())
    url = db.Column(db.String())
    # Urban dictionary stuff
    word = db.Column(db.String())

    def __init__(self, user,subreddit, word, url):
        self.user = user
        self.subreddit = subreddit
        self.word = word
        self.url = url

    def __repr__(self):
        return '<id> {}'.format(self.id)

    def serialize(self):
        return { 
            'user': self.user,
            'subreddit': self.subreddit,
            'word': self.word,
            'url': self.url
        }

    @api_rest.route('/tabletest/<string:resource_id>')
    class Test(Resource):
        def get(self, resource_id):
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
                print(str(e))
                return(str(e))