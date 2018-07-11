"""Utility file to seed project database"""

import datetime
from sqlalchemy import func

from model import User, User_Moods, Moods, UserGoals, Goals, Hashtag, Activities, UserDataHashtags, connect_to_db, db
from server import app


def load_users():
    """Hard-code load users from u.user into database."""

    #print("Users")
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
    
 

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    
    load_users()
    

    
