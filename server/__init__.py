from flask import Flask, render_template, request, session, redirect, abort
from flask_session import Session
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
#from . import db as database
import db as database
from pubnub_publisher import publish_msg

load_dotenv()

app = Flask(__name__)
app.secret_key = "secret"

#set up db
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
database.db.init_app(app)



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
    print(session["user_scanners"])

    return render_template("sensors_monitor.html", sensors=session["user_scanners"])



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
        user = database.find_user_if_exists(email)
        if not user:
            return render_template("login.html", error="Invalid email and password combination")

        if not check_password_hash(user.password, password):
            return render_template("login.html", error="Invalid email and password combination")

        session["email"] = email
        session["logged_in"] = 1
        session["user_scanners"] = database.get_user_scanners(email)

        return redirect("/sensors")




@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirmPassword"]

        #validate forms
        if not name:
            return render_template("register.html", error="Name is Required")
        if not email:
            return render_template("register.html", error="Email is Required")
        if not password:
            return render_template("register.html", error="Password is Required")
        if not confirm_password:
            return render_template("register.html", error="Please Confirm Password")
        
        if password != confirm_password:
            return render_template("register.html", error="Passwords do not match")
        
        #create new user and log in
        hashed_password = generate_password_hash(password)
        created = database.register_new_user(name, email, hashed_password)

        if not created:
            return render_template("register.html", error="User Already Exists")
        else:
            session["email"] = email
            session["logged_in"] = 1
            return redirect("/sensors")


@app.route('/write_temp', methods=["POST"])
def write_temp():
    data = request.get_json()


    
    scanner = data["scanner"]
    temperature = data["temperature"]
    time = data["time"]

    try:
        database.write_temp(time, scanner, temperature)
    except:
        print("Error")

    return redirect("/sensors")
        

@app.route('/update_sensor', methods=["POST"])
def update_sensor():
    device_name = request.form["device_name"]
    device_id = request.form["sensor_id"]
    min_temp = int(request.form["min_temp"])
    max_temp = int(request.form["max_temp"])

    if len(device_name) == 0:
        return render_template("/sensors", error="Device name is required")
    
    if (min_temp < -20 or min_temp  > 60) or (max_temp < -20 or max_temp > 60) or not min_temp or not max_temp:
        return render_template("/sensors", error="Please enter a valid min and max temp between -20 and 60")
    
    if min_temp > max_temp:
        return render_template("/sensors", error="Min Temp must be less than max temp")
    
    #db
    database.update_sensor(device_id, device_name, min_temp, max_temp)

    #session
    session["user_scanners"] = database.get_user_scanners(session["email"])

    #pubnub
    message = {"message_type": "update_sensor", "min_temp": min_temp, "max_temp": max_temp}
    publish_msg(message)

    return redirect("/sensors")




if __name__ == "__main__":
    app.run()
