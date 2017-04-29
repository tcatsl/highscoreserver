from models import Scores, Version
from app import db

version = Version(2)
db.session.add(version)
db.session.commit()
