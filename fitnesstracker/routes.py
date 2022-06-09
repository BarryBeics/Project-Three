from flask import render_template, request, redirect, url_for, flash, session
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
        existing_user = Users.query.filter(
            Users.email == request.form.get("email").lower()).all()

        if existing_user:
            flash("Email already exists")
            return redirect(url_for("register"))

        register_user = Users(
            first_name=request.form.get("first_name").lower(),
            last_name=request.form.get("last_name").lower(),
            email=request.form.get("email").lower(),
            password=generate_password_hash(request.form.get("password"))
        )
        db.session.add(register_user)
        db.session.commit()

        # Put new user into 'session' cookie

        if existing_user:
            print(request.form.get("email"))
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user[0].password, request.form.get("password")):
                        session["user"] = existing_user[0].user_id
                        flash("Welcome, {}".format(
                            request.form.get("user_id")))
                        return redirect(url_for(
                            "profile", user_id=session["user"]))

    return render_template("register.html")


    # Log In
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check email to see if user already exisits in db
        existing_user = Users.query.filter(
            Users.email == request.form.get("email").lower()).all()

        if existing_user:
            print(request.form.get("email"))
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user[0].password, request.form.get("password")):
                        session["user"] = existing_user[0].user_id
                        flash("Welcome, {}".format(
                            request.form.get("user_id")))
                        return redirect(url_for(
                            "profile", user_id=session["user"]))
            else:
                #invalid password
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # email doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")



@app.route("/profile/<user_id>", methods=["GET", "POST"])
def profile(user_id):
    # grab the session user's email from db
    if "user" in session:
        return render_template("profile.html", user_id=session["user"])

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/post_activity", methods=["GET", "POST"])
def post_activity():
    if request.method == "POST":
        activity = Activity_log(
            user_id=session["user"],
            distance=request.form.get("distance"),
            activity_type=request.form.get("activity_type"),
            commute=request.form.get('commute') == 'on',
            date=request.form.get("datetime")
        )
        db.session.add(activity)
        db.session.commit()
    return render_template("post_activity.html")