from models import Scores
from app import db

scores = Scores('tcats', 666)

db.session.add(scores)
db.session.commit()
