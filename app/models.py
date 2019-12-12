from app import login
from flask_login import UserMixin
from app import db
import datetime
from flask_login import current_user

from werkzeug.security import check_password_hash

## users and message thread?

friends = db.Table('friends',
                   db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                   db.Column('user_id', db.Integer, db.ForeignKey('user.id')))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    name = db.Column(db.String(15))
    email = db.Column(db.String(30), unique=True)
    age = db.Column(db.Integer)
    university = db.Column(db.String(25))
    course = db.String(db.String)
    password = db.Column(db.String(64))
    is_moderator = db.Column(db.Boolean)
    inbox = db.relationship('Message', backref='owner', lazy='dynamic')
    connections = db.relationship('User', secondary=friends, backref=db.backref('connect', lazy='dynamic'), lazy='dynamic')


# try to avoid duplicating friends when making a query
# class Friends(db.Model):
#     id = db.Column(db.Integer,  db.ForeignKey('user.id'), primary_key=True)
#     friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
#

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid_receiver = db.Column(db.Integer, db.ForeignKey('user.id'))
    sender = db.Column(db.String)
    date = db.Column(db.DateTime)
    message = db.Column(db.String)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime)
    message = db.Column(db.String(120))

# give flask user instance
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# def load_friends():
#     friend_objs = Friends.query.filter_by(friend_id=current_user.id).all()
#     friend_objs = friend_objs + Friends.query.filter_by(id=current_user.id).all()
#
#     names = []
#     for friend_obj in friend_objs:
#
#         # friend_ids can come under the 'friend_id' or 'id' fields so query for both
#         if not friend_obj.id == current_user.id:
#             name = User.query.filter_by(id=friend_obj.id).first.name()
#         else:
#             name = User.query.filter_by(id=friend_obj.friend_id).first.name()
#
#         names.append((name, name))
#
#     return names
