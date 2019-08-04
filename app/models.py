from app import db

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
    created_time = db.Column(db.String())
    received_time = db.Column(db.String())
    subreddit = db.Column(db.String())
    url = db.Column(db.String())
    # Urban dictionary stuff
    word = db.Column(db.String())
    meaning = db.Column(db.String())
    example = db.Column(db.String())

    def __init__(self, user, created_time, received_time, subreddit, url, word, meaning, example):
        self.user = user
        self.created_time = created_time
        self.received_time = received_time
        self.subreddit = subreddit
        self.url = url
        self.word = word
        self.meaning = meaning
        self.example = example

    def __repr__(self):
        return '<id> {}'.format(self.id)

    def serialize(self):
        return { 
            'user': self.user,
            'created_time': self.created_time,
            'received_time': self.received_time,
            'subreddit': self.subreddit,
            'url': self.url,
            'word': self.word,
            'meaning': self.meaning,
            'example': self.example
        }
