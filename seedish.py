from models import Scores, Version
from users import App_users
from app import db

user = App_users("tcats", "thomas.castleman@gmail.com")
db.session.add(user)
db.session.commit()
