from app import db

class Scores(db.Model):
    @property
    def serialize(self):
        return {
            'score' : self.score,
            'name': self.name
        }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    score = db.Column(db.Integer)

    def __init__(self, name=None, score=None):
        self.name = name
        self.score = score

    def __repr__(self):
        return '<Scores %r>' % self.score

class Version(db.Model):
    @property
    def serialize(self):
        return {
            'version' : self.version
        }

    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer)

    def __init__(self, version=None):
        self.version = version

    def __repr__(self):
        return '<Version %r>' % self.version
class User(db.Model):
    @property
    def serialize(self):
        return {
            'user_name' : self.user_name,
            'email' : self.email
        }

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String)
    email = db.Column(db.String)

    def __init__(self, user_name=None, email=None):
        self.user_name = user_name
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.user_name
