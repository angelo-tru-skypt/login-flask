from models.db import db

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(400))
    password = db.Column(db.String(200))

