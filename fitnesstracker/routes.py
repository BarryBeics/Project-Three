from flask import render_template, request, redirect, url_for, flash
from fitnesstracker import app, db
from fitnesstracker.models import Users, Map_data, Notifications, Chat_log, Activity_log, Groups
from werkzeug.security import generate_password_hash, check_password_hash


# Home page end point
@app.route("/")
def home():
    return render_template("map.html")

# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check email to see if user already exisits in db
        email = request.form.get("email")
        existing_user = Users_info.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already exists")
            return redirect(url_for("register"))

        register_user = Users_info(
            first_name=request.form.get("first_name"),
            last_name=request.form.get("last_name"),
            email=request.form.get("email"),
            password=generate_password_hash(request.form.get("password")),
            account_created=request.form.get("account_created")
        )
        db.session.add(register_user)
        db.session.commit()
    return render_template("register.html")