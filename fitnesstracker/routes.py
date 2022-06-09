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


@app.route("/view_activity")
def view_activity():
    activities = Activity_log.query.filter_by(user_id=session["user"]).all()
    #access = Users_info.query.filter_by(user_id=session["user"]).all()
    return render_template("view_activity.html", activities=activities)


# landmarks list
@app.route("/landmarks")
def landmarks():
    landmarks = list(Map_data.query.order_by(Map_data.landmark_name).all())
    return render_template("landmarks.html", landmarks=landmarks)

# Landmarks Add New
@app.route("/add_landmark", methods=["GET", "POST"])
def add_landmark():
    if request.method == "POST":
        landmark = Map_data(
            landmark_name=request.form.get("landmark_name"),
            modal_link=request.form.get("modal_link"),
            main_image=request.form.get("main_image"),
            video_link=request.form.get("video_link"),
            body_text=request.form.get("body_text"),
            user_id=session["user"],
            longitude=request.form.get("longitude"),
            latitude=request.form.get("latitude")
        )
        db.session.add(landmark)
        db.session.commit()
        return redirect(url_for("landmarks"))
    return render_template("add_landmark.html")


# Landmark Edit
@app.route("/edit_landmark/<int:landmark_id>", methods=["GET", "POST"])
def edit_landmark(landmark_id):
    landmark = Map_data.query.get_or_404(landmark_id)
    if request.method == "POST":
        landmark.landmark_name = request.form.get("landmark_name")
        landmark.modal_link=request.form.get("modal_link"),
        landmark.main_image=request.form.get("main_image"),
        landmark.video_link=request.form.get("video_link"),
        landmark.body_text=request.form.get("body_text"),
        user_id=session["user"],
        landmark.longitude=request.form.get("longitude"),
        landmark.latitude=request.form.get("latitude")
        db.session.commit()
        return redirect(url_for("landmarks"))
    return render_template("edit_landmark.html", landmark=landmark)



# Landmark Delete
@app.route("/delete_landmark/<int:landmark_id>")
def delete_landmark(landmark_id):
    landmark = Map_data.query.get_or_404(landmark_id)
    db.session.delete(landmark)
    db.session.commit()
    return redirect(url_for("landmarks"))


# Register a new group
@app.route("/register_group", methods=["GET", "POST"])
def register_group():
    if request.method == "POST":
        # check group name to see if user already exisits in db
        existing_group = Groups.query.filter(
            Groups.name == request.form.get("name").lower()).all()

        if existing_group:
            flash("Group Name already exists")
            return redirect(url_for("register_group"))

        register_group = Groups(
            name=request.form.get("name").lower(),
            user_id=session["user"]
        )
        db.session.add(register_group)
        db.session.commit()
        flash("Successfully created, {}".format(
                            request.form.get("name")))

    return render_template("register_group.html")