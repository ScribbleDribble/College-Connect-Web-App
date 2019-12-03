from app import login
from flask_login import UserMixin
from app import db
import datetime

from werkzeug.security import check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    name = db.Column(db.String(15))
    email = db.Column(db.String(15), unique=True)
    age = db.Column(db.Integer)
    university = db.Column(db.String(15))
    course = db.String(db.String)
    password = db.Column(db.String(15))
    inbox = db.relationship('Message', backref='owner', lazy='dynamic')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid_receiver = db.Column(db.Integer, db.ForeignKey('user.id'))
    sender = db.Column(db.String)
    date_sent = db.Column(db.DateTime)




# give flask user instance
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

