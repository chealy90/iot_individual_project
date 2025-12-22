from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/sensors', methods=["GET", "POST"])
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


@app.route('/login')
def login():
    pass

@app.route('/logout')
def logout():
    pass

@app.route('/register')
def register():
    pass



if __name__ == "__main__":
    app.run()