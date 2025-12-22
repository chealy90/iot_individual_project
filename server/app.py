from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/sensors')
def sensors():
    return render_template("sensors_monitor.html")



if __name__ == "__main__":
    app.run()