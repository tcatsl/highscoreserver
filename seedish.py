from models import Scores, Version, Users
from app import db

user = Users("tcats", "thomas.castleman@gmail.com")
db.session.add(user)
db.session.commit()
