"""Structuring the DB and models"""

from enum import unique
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


# Creates the User table in the DB
class User(DB.Model):
    # Setting up the id for the user
    id = DB.Column(DB.BigInteger, primary_key=True)
    # Setting up the username for the user
    username = DB.Column(DB.String, nullable=False, unique=True)
    # Stores most recent tweet_id
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return f"<User: {self.username}>"


# Creates the tweet table in the DB
class Tweet(DB.Model):
    # Setting up the tweet id for tweet
    id = DB.Column(DB.BigInteger, primary_key=True)
    # Text column for each tweet
    text = DB.Column(DB.Unicode(300))
    # Stores numbers for user tweets
    vect = DB.Column(DB.PickleType, nullable=False)
    # user_id foreign key column for tweet
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'),
                        nullable=False)
    
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))
    
    def __repr__(self):
        return f"<Tweet: {self.text}>"