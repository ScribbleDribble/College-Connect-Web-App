from app import login
from flask_login import UserMixin
from app import db
from werkzeug.security import check_password_hash

class User(UserMixin, db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    # for login and authentication
    is_authenticated = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean)
    is_anonymous = db.Column(db.Boolean)
    password = db.Column(db.String)

    def check_password(password):
        check_password_hash(password, User.password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

