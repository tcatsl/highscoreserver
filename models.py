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
