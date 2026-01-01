from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from . import db as database

app = Flask(__name__)

#set up db
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)



#set up sessions
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
#Session(app)


def login_is_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if ("email" not in session and "logged_in" not in session):
            return abort(401)
        else:
            return function(*args, **kwargs)
    return wrapper


@app.route('/')
def index():
    return render_template("index.html")



@app.route('/sensors', methods=["GET", "POST"])
@login_is_required
def sensors():
    sensor1 = {
        "sensor_name": "Fridge Sensor",
        "sensor_current": 1.4,
        "sensor_min": 1,
        "sensor_max": 4
    }

    sensor2 = {
        "sensor_name": "Freezer Sensor",
        "sensor_current": -5,
        "sensor_min": -10,
        "sensor_max": -3
    }

    return render_template("sensors_monitor.html", sensors=[sensor1, sensor2])



@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        #validate input
        if not email:
            return render_template("login.html", error="Email is Required")
        if not password:
            return render_template("login.html", error="Password is Required")

        #validate login
        user = db.find_user_if_exists(email)
        if not user:
            return render_template("login.html", error="Invalid email and password combination")

        if not check_password_hash(user.password, password):
            return render_template("login.html", error="Invalid email and password combination")

        session["email"] = email
        session["logged_in"] = 1

        return redirect("/sensors")




@app.route('/logout')
def logout():
    pass

@app.route('/register')
def register():
    pass



if __name__ == "__main__":
    app.run()
