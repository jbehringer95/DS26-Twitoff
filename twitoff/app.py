"""Main app/routing file for Twitoff"""

from os import getenv
from twitoff.predict import predict_user
from flask import Flask, render_template, request
from .models import DB, User
from .twitter import add_or_update_user


def create_app():
    """Creates and configures an instance of the flask application"""
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    DB.init_app(app)

    @app.route('/')
    def root():
        return render_template("base.html", title="Home", users=User.query.all())

    @app.route('/compare', methods=["POST"])
    def compare():
        # getting users and hypothetical tweet from client
        user0, user1 = sorted(
            [request.values['user0'], request.values['user1']])
        hypo_tweet_text = request.values["tweet_text"]

        # stops clients from comparing same user
        if user0 == user1:
            message = "Cannot compare users to themselves!"

        else:
            prediction = predict_user(user0, user1, hypo_tweet_text)
            message = '"{}" is more likely to be said by {} than {}'.format(
                hypo_tweet_text,
                user1 if prediction else user0,
                user0 if prediction else user1
            )

        return render_template('prediction.html', title='Prediction', message=message)

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        name = name or request.values["user_name"]
        try:
            if request.method == "POST":
                add_or_update_user(name)
                message = f"User {name} successfully added!"

            tweets = User.query.filter(User.username == name).one().tweets
        except Exception as e:
            message = f"Error adding {name}: {e}"
            tweets = []

        return render_template("user.html", title=name, tweets=tweets, message=message)

    @app.route('/populate')
    def populate():
        add_or_update_user("garyvee")
        add_or_update_user("mcuban")
        return render_template("base.html", title="Home", users=User.query.all())

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template("base.html", title="Home", users=User.query.all())

    @app.route('/update')
    def update():
        for user in User.query.all():
            add_or_update_user(user.username)

        return render_template('base.html', title='All users tweets were updated!', users=User.query.all())

    return app


# def insert_users(usernames):
#     for id_index, username in enumerate(usernames):
#         user = User(id=id_index, username=username)
#         DB.session.add(user)
#         DB.session.commit()

# def insert_tweet(tweets):
#     for id_index, text in enumerate(tweets):
#         tweet = Tweet(id=id_index, text=text, user_id=User.id)
#         DB.session.add(tweet)
#         DB.session.commit()