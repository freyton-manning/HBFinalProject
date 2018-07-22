"""Models and database functions for Ratings project."""
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy



# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of mood tracking website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(20), nullable= False)
    password = db.Column(db.String(64), nullable=False)
    reminders_on = db.Column(db.Boolean, nullable=False)
    #age = db.Column(db.Integer, nullable=True)
    #zipcode = db.Column(db.String(15), nullable=True)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} email={self.email}>"

class User_Moods(db.Model):
    """User Moods Information - all the data they log"""
    __tablename__ = "user_moods"

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    # realized this wasn't added so updated - need a way to link mood id to the user
    # otherwise what are they actually logging? 
    mood_id = db.Column(db.Integer, db.ForeignKey('moods.mood_id'), nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    comments = db.Column(db.String(1000), nullable = True)
    hours_slept = db.Column(db.Float, nullable=True)
    exercise_mins = db.Column(db.Integer, nullable=True)

    hashtags = db.relationship("Hashtag", secondary = "user_data_hashtags")

class Moods(db.Model):
    """ Table of available Moods and mood information"""
    __tablename__ = "moods"

    mood_id = db.Column(db.Integer, autoincrement=False, primary_key=True)
    mood_word = db.Column(db.String(25), nullable=False)
    mood_num = db.Column(db.Integer, nullable= False)
    #Not quite sure what to do with Mood type rn, so keeping it nullable 
    #Might do initial DB seed without it 
    mood_type = db.Column(db.String(50), nullable = True)

class UserGoals(db.Model):
    __tablename__ = "users_goals"

    goal_record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.goal_id'), nullable=False)
    #Keeping timeframe optional field for now 
    timeframe = db.Column(db.String(50), nullable=False)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("user_goals"))
    goal = db.relationship("Goals")
    # Define relationship to movie
    #movie = db.relationship("Movie",
                            #backref=db.backref("ratings",
                                               #order_by=rating_id))

class Goals(db.Model):
    """ Table of all goals - predetermined list (ex: fitness)"""
    __tablename__ = "goals"

    goal_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    goal_description = db.Column(db.String(50), nullable=False)

class Hashtag(db.Model):
    """ Table of all hashtags with an id, for searching later"""
    __tablename__ = "hashtags"

    hashtag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    text = db.Column(db.String(25), nullable=False)

class Activities(db.Model):
    """Ratings information"""
    __tablename__ = "activities"

    activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    #TODO: FIGURE OUT RESPONSE TYPES FROM MEETUP API - ID 
    meetup_id = db.Column(db.String(100), nullable=True)
    meetup_url = db.Column(db.String(300), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.goal_id'), nullable=False)
    activity_date = db.Column(db.DateTime, nullable = False)
    did_attend = db.Column(db.BOOLEAN, nullable = False)

class UserDataHashtags(db.Model):
    """Ratings information"""
    __tablename__ = "user_data_hashtags"

    user_hashtag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    hashtag_id = db.Column(db.Integer, db.ForeignKey('hashtags.hashtag_id'), nullable=False)
    record_id = db.Column(db.Integer, db.ForeignKey('user_moods.record_id'), nullable=False)

    



    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Rating rating_id={self.rating_id} 
                   movie_id={self.movie_id} 
                   user_id={self.user_id} 
                   score={self.score}>"""


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///project'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")