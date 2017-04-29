from models import Scores, Version
from app import db

scores = Scores('tcats', 666)
version = Version(1)
db.session.add(scores)
db.session.add(version)
db.session.commit()
