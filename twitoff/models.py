"""SQLAlchemy models and database architecture"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


# Creates a 'user' Table
class User(DB.Model):
    # id primary key column for 'user'
    id = DB.Column(DB.BigInteger, primary_key=True)
    # username column for 'user'
    username = DB.Column(DB.String, nullable=False)

    def __repr__(self):
        return f"<User: {self.username}>"


# Creates a 'tweet' Table
class Tweet(DB.Model):
    # id primary key column for 'tweet'
    id = DB.Column(DB.BigInteger, primary_key=True)
    # text column for 'tweet'
    text = DB.Column(DB.Unicode(300))
    # user_id foreign key column for 'tweet'
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        'user.id'), nullable=False)

    ### TODO: STRETCH GOAL ###
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return f"<Tweet: {self.text}>"