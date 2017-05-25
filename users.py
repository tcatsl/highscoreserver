from app import db

class App_users(db.Model):
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
        return '<App_users %r>' % self.user_name
