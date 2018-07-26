"""Final Project Flask server.

Provides web interface for login, tracking mood / comments / hashtags, and
viewing mood visualization data. Also lets a user select goals from a menu.

"""

from flask import Flask, render_template, redirect, flash, session, request
import jinja2

from model import User, User_Moods, Moods, UserGoals, Goals, Hashtag, Activities, UserDataHashtags, connect_to_db, db

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def homepage():
    """Return homepage."""

    return render_template("homepage.html")

@app.route("/about")
def about():
    """Return About Informational Page"""
    return render_template("about.html")

#added mood chart route
@app.route("/mood-chart")
def chart():
    labels = ["January","February","March","April","May","June","July","August"]
    values = [10,9,8,7,6,4,7,8]
    return render_template('standin_mood_chart.html', values=values, labels=labels)

@app.route("/user-chart")
def user_chart():

    results = User_Moods.query.filter(User_Moods.user_id == 0, User_Moods.hours_slept.isnot(None))
    return render_template('user_mood_chart.html', results=results)

@app.route("/diff-chart")
def diff_user_chart():

    results = User_Moods.query.filter(User_Moods.user_id == 0)
    prev = 5
    #chart_out = {}
    class chart_out:
        def __init__(self):
            self.mood_id = None
            self.datetime = None
    result_list = []        
    for result in results:
        co = chart_out()
        co.datetime = result.datetime
        co.mood_id = int(result.mood_id) - prev
        #chart_out.result.datetime = result.mood_id - prev
        prev = result.mood_id
        result_list.append(co)
    return render_template('diff_mood_chart.html', results=result_list)

@app.route("/exercise-chart")
def exercise_chart():
    #uid = webapp2.request.get('uid')
    #if uid == '':
        #uid = 0
    results = User_Moods.query.filter(User_Moods.user_id == 0, User_Moods.exercise_mins.isnot(None))
    return render_template('exercise_chart.html', results=results)

@app.route("/sleep-chart")
def sleep_chart():

    results = User_Moods.query.filter(User_Moods.user_id == 0, User_Moods.hours_slept.isnot(None))
    return render_template('hours_slept.html', results=results)

#mood chart update
#request.args.get
#todo: add view mood chart by zoom in feature

#todo: add view mood chart by 

@app.route("/goals")
def show_goals():
    """Return Page with User Goals"""

    return render_template("goals.html")

@app.route("/track-mood", methods=["GET"])
def show_mood_picker():
    """Return Page that shows mood picker for user to select"""

    return render_template("mood_picker.html") 

#TODO: ADD 'ADD TRACKED MOOD' ROUTE
@app.route("/track-mood", methods=["POST"])
def pick_mood():
    mood = request.form.get("mood")
    comment = request.form.get("comment")
    hours_slept = request.form.get("hrslept")
    exercise_mins = request.form.get("exmins")
    hashtag = request.form.get("hashtag")
    success_string = "TA-DA! " + str(mood) + " " + str(comment) + str(hours_slept) + str(exercise_mins) + str(hashtag)

    hashtag_obj = Hashtag.query.filter_by(text=hashtag).first()
    if hashtag_obj is None:
        hashtag_obj = Hashtag(text=hashtag)

    user_mood= User_Moods(user_id=0, 
        mood_id=int(mood), 
        comments=str(comment),
        exercise_mins=int(exercise_mins),
        hours_slept=int(hours_slept), 
        hashtags=[hashtag_obj])

    db.session.add(user_mood)
    db.session.add(hashtag_obj)
    db.session.commit()

    return render_template("success_message.html", success_string=success_string)

#make form on mood picker into radio buttons so you don't have to add event listeners 
    #new_mood = 
        #db.session.add(new_mood)
        #db.session.commit()

# user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     mood_id = db.Column(db.Integer, db.ForeignKey('moods.mood_id'), nullable=False)
#     datetime = db.Column(db.DateTime, nullable=False)
#     comments = db.Column(db.String(1000), nullable = True)
#     hours_slept = db.Column(db.Float, nullable=True)
#     exercise_mins = db.Column(db.Integer, nullable=True)

@app.route("/register", methods=["GET"])
def register_form():
    """Return page showing the registration form
    Show all fields user needs to fill out in order to register for app
    """
    return render_template("registration_form.html")

@app.route('/register', methods=["POST"])
def register_process():
    email = request.form.get("email")
    password = request.form.get("password")
    username = request.form.get("username")
    reminders_on = request.form.get("reminders_on") == 'on'

    print(reminders_on)

    query = User.query.filter(User.email == email).first()
    
    if query is None:
        new_user = User(email=email, password=password, username=username, reminders_on=reminders_on)
        db.session.add(new_user)
        db.session.commit()
    return redirect("/")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    """logs an existing user in after they register"""
    user_email = request.form.get('email')
    password = request.form.get('password')
     #user_id = User.query.filter(User.email)

    #query = User.query.filter(User.email==user_email, User.password == password).first()
    user = User.query.filter(User.email == user_email).first()

    if user is not None:
        if user.password == password:
            session["user_name"] = user.user_id
            flash("Logged in")
            return redirect("/")
        else: 
            flash("Password is incorrect!")
            return redirect("/login")
    else: 
        flash("Incorrect email, please register")
        return redirect ("/register")        




if __name__ == "__main__":
    #app.run(debug=True)
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    #DebugToolbarExtension(app)

    app.run(debug=True, port=5000, host='0.0.0.0')
