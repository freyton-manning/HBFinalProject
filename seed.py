"""Utility file to seed project database"""

import datetime
import random
from sqlalchemy import func

from model import User, User_Moods, Moods, UserGoals, Goals, Hashtag, Activities, UserDataHashtags, connect_to_db, db
from server import app


def load_users():
    """Hard-code load users from into database."""

    UserGoals.query.delete()
    User.query.delete()
    Goals.query.delete()
    edith = User(user_id=0,
                email="edith@edith.com",
                   password="password",
                   username = "Edith",
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

    Moods.query.delete()
    

    mood_10 = Moods(mood_word = "Really Great", mood_num=10, mood_id=10)
    mood_9 = Moods(mood_word = "Great", mood_num=9, mood_id=9)
    mood_8 = Moods(mood_word = "Very Good", mood_num=8, mood_id=8)
    mood_7 = Moods(mood_word = "Good", mood_num=7, mood_id=7)
    mood_6 = Moods(mood_word = "Okay", mood_num=6, mood_id=6)
    mood_5 = Moods(mood_word = "So-So", mood_num=5, mood_id=5)
    mood_4 = Moods(mood_word = "Meh", mood_num=4, mood_id=4)
    mood_3 = Moods(mood_word = "Bad", mood_num=3, mood_id=3)
    mood_2 = Moods(mood_word = "Very Bad", mood_num=2, mood_id=2)
    mood_1 = Moods(mood_word = "Couldn't Be Worse", mood_num=1, mood_id=1)

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
def load_user_moods(): 

    User_Moods.query.delete()
    
    user_mood_1= User_Moods(user_id=0, 
        mood_id=5, 
        datetime='2018-01-01 12:00:00',
        comments= "Feeling average...",
        hours_slept=8,
        exercise_mins=60)

    db.session.add(user_mood_1)
    db.session.commit()
    
    mood_pots = [1,2,3,4,5, 5,5, 5, 5, 6,6,6, 6,7,8,9,9,10,10,10,10,10]
    comments_pots = ["Feeling Average", "Positive Vibes", "Need Caffeine", "Sunny Day!", "Went for a walk", "Good times with friends", "Travel Fun", "Gloomy", "Too much caffeine", "Great Day", "Worked Overtime", "Cooked Dinner", "Beach Day", "PTO, Woo!", "Cranky today", ]
    hashtag_pots = [ "#Blessed", "#StillBlessed", "#RainyDay", "#BailedOnPlans", "#LegDay", "#WhenisFriYAY", "#Hungry" ,"#Bored", "#ItsHandled", "#TheStruggleIsReal", "#GoodTimes", "#WFH", "#Motivated", "#MoreSleepPlz", "#CoffeeBreaks", "#Glad2BeHere"]
    exercise_pots = [0,30,60,60,90,180,0,30]
    
    i = 1
    while i < 50:
        #never sad 
        #mood_id = random.randint(5,10)
        #high variation 
        #mood_pots = [1,1,1,2,2,2,3,4,6,7,8,9,9,10,10,10,10,10]
        #mood_id = random.choice(mood_pots)
        #mostly happy
        comments = random.choice(comments_pots)
        mood_id = random.choice(mood_pots)
        hours_slept = random.randint(0,2)+mood_id
        exercise_mins = random.choice(exercise_pots)
        month = 1+ int(i/27)
        day = i % 27 + 1
        
        # query for hashtag by text field
        # if it's NOT in the hashtag table, add it
        
       
        hashtag_text = random.choice(hashtag_pots)

        hashtag = Hashtag.query.filter(Hashtag.text == hashtag_text).first()
        if hashtag is None:
            hashtag = Hashtag(text=hashtag_text)
            db.session.add(hashtag)
            db.session.commit()

        user_mood_rnd = User_Moods(user_id=0, 
        mood_id=mood_id, 
        datetime='2018-' + str(month) +'-'+str(day) + ' 12:00:00',
        comments=comments,
        #comments= "Feeling average...",
        hours_slept= hours_slept,
        exercise_mins=exercise_mins)

        db.session.add(user_mood_rnd)
        db.session.commit()

        userdatahashtag = UserDataHashtags(hashtag_id=hashtag.hashtag_id, record_id=user_mood_rnd.record_id)
        
        db.session.add(userdatahashtag)
        db.session.commit()

        i+=1


# def load_user_hashtags():
#     Hashtag.query.delete()

#     i = 1 
#     while i < 50:
#         hashtag_pots = [ "#Blessed", "#StillBlessed", "#LegDay" "#WhenisFriYAY", "#Hungry" "#Bored", "#ItsHandled", "#TheStruggleIsReal", "#GoodTimes", "#WFH", "#Motivated", "#MoreSleepPlz" "#CoffeeBreaks", "#Glad2BeHere"]
#         hashtag_rnd = Hashtag(text=random.choice(hashtatg_pots))
#         db.session.add(hashtag_rnd)

#         db.session(commit)

#class Hashtag(db.Model):
    """ Table of all hashtags with an id, for searching later"""
    #__tablename__ = "hashtags"

    #hashtag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    #text = db.Column(db.String(25), nullable=False)

# record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     mood_id = db.Column(db.Integer, db.ForeignKey('moods.mood_id'), nullable=False)
#     datetime = db.Column(db.DateTime, nullable=False)
#     comments = db.Column(db.String(1000), nullable = True)
#     hours_slept = db.Column(db.Float, nullable=True)
#     exercise_mins = db.Column(db.Integer, nullable=True)

#     hashtags = db.relationship("Hashtag", secondary = "user_data_hashtags")


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    
    load_users()
    load_moods()
    load_user_moods()
    

    
