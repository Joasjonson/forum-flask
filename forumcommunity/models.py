from forumcommunity import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader          # Function to find the user and load.
def load_user(id_user):
    return User.query.get(int(id_user))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    profile_picture = db.Column(db.String, default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)
    courses = db.Column(db.String, nullable=False, default='Uninformed')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False )

