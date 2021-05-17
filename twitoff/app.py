"""Main app/routing file for Twitoff"""

from flask import Flask, render_template
from .models import DB, User


def create_app():
    """Creates and configures an instance of the flask application"""
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template("base.html", title="Home", users=users)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        users = User.query.all()
        return render_template("base.html", title="Home", users=users)

    @app.route('/populate')
    def populate():
        insert_users(["elonmusk", "jackblack"])
        users = User.query.all()
        return render_template("base.html", title="Home", users=users)

    return app


def insert_users(usernames):
    for id_index, username in enumerate(usernames):
        user = User(id=id_index, username=username)
        DB.session.add(user)
        DB.session.commit()