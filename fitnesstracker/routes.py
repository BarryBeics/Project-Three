from flask import render_template
from fitnesstracker import app, db
from fitnesstracker.models import Users, Map_data, Notifications, Chat_log, Activity_log, Groups


@app.route("/")
def home():
    return render_template("base.html")