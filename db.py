from app import db
db.drop_all()
db.commit()
db.create_all()
