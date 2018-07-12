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

@app.route("/goals")
def show_goals():
    """Return Page with User Goals"""

    return render_template("goals.html")

@app.route("/track-mood", methods=["GET"])
def show_mood_picker():
    """Return Page that shows mood picker for user to select"""

    return render_template("mood_picker.html") 


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
