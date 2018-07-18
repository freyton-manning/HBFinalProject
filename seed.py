"""Utility file to seed project database"""

import datetime
from sqlalchemy import func

from model import User, User_Moods, Moods, UserGoals, Goals, Hashtag, Activities, UserDataHashtags, connect_to_db, db
from server import app


def load_users():
    """Hard-code load users from into database."""

    UserGoals.query.delete()
    User.query.delete()
    Goals.query.delete()
    edith = User(email="edith@edith.com",
                   password="password",
                   username = "edith",
                   reminders_on=True)
    #user object has user_goals relationship
    #user_goals has relationship to goals and to users

    goal_1 = Goals(goal_description = "Fitness")
    goal_2 = Goals(goal_description = "Social Acitivities")
    goal_3 = Goals(goal_description = "Volunteering")

    edith_goal=UserGoals(frequency=10, timeframe="Month")
    edith_goal.goal = goal_1
    edith.user_goals = [edith_goal]

    # user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # email = db.Column(db.String(64), nullable=False)
    # username = db.Column(db.String(20), nullable= False)
    # password = db.Column(db.String(64), nullable=False)
    # reminders_on = db.Column(db.Boolean, nullable=False)
    db.session.add(edith)
    db.session.add(edith_goal)
    db.session.add(goal_1)
    db.session.add(goal_2)
    db.session.add(goal_3)
    db.session.commit()
    
 #add mood data to db

 # def load_goals():
    """Load mood data into db"""
def load_moods(): 

    mood_10 = Moods(mood_word = "Really Great", mood_num=10)
    mood_9 = Moods(mood_word = "Great", mood_num=9)
    mood_8 = Moods(mood_word = "Very Good", mood_num=8)
    mood_7 = Moods(mood_word = "Good", mood_num=7)
    mood_6 = Moods(mood_word = "Okay", mood_num=6)
    mood_5 = Moods(mood_word = "So-So", mood_num=5)
    mood_4 = Moods(mood_word = "Meh", mood_num=4)
    mood_3 = Moods(mood_word = "Bad", mood_num=3)
    mood_2 = Moods(mood_word = "Very Bad", mood_num=2)
    mood_1 = Moods(mood_word = "Couldn't Be Worse", mood_num=1)

    db.session.add(mood_10)
    db.session.add(mood_9)
    db.session.add(mood_8)
    db.session.add(mood_7)
    db.session.add(mood_6)
    db.session.add(mood_5)
    db.session.add(mood_4)
    db.session.add(mood_3)
    db.session.add(mood_2)
    db.session.add(mood_1)
    db.session.commit()


#TODO: 
# def load_user_moods(): 


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    
    load_users()
    load_moods()
    

    
