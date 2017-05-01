from app import db
import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

class Scores(db.Model):
    __table_args__ = {'extend_existing': True}
    @property
    def serialize(self):
        return {
            'score' : self.score,
            'name': self.name,
            'difficulty': self.difficulty,
            'kills': self.kills,
            'created_date': self.created_date
        }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    score = db.Column(db.Integer)
    difficulty = db.Column(db.Integer)
    kills = db.Column(db.Integer)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    def __init__(self, name=None, score=None, kills=None, difficulty=None):
        self.name = name
        self.score = score
        self.kills = kills
        self.difficulty = difficulty


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
