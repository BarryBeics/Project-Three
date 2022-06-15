from flask import render_template, request, redirect, url_for, flash, session, jsonify
from sqlalchemy import func
from fitnesstracker import app, db
from fitnesstracker.models import Users, Map_data, Notifications, Chat_log, Activity_log, Groups
from werkzeug.security import generate_password_hash, check_password_hash
import math, json


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
        session["user"] = request.form.get("email").lower()
        flash("Welcome, {}".format(session["user"]))
        return redirect(url_for("profile", email=session["user"]))

    return render_template("register.html")


# Log In
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check email to see if user already exisits in db
        existing_user = Users.query.filter(
            Users.email == request.form.get("email").lower()).all()

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user[0].password, request.form.get("password")):
                        session["user"] = request.form.get("email").lower()
                        flash("Welcome, {}".format(session["user"]))
                        return redirect(url_for("profile"))
            else:
                #invalid password
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # email doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")



@app.route("/profile", methods=["GET", "POST"])
def profile():
    
    if "user" in session:
        email = session["user"]
        # swap the session value from email to user_id
        user_data = Users.query.filter(Users.email == session["user"]).first()
        user_id = user_data.user_id
        session["user"] = user_id

        is_new = Activity_log.query.filter_by(user_id=session["user"]).count()
        print(is_new)
        if is_new == 0:
            flash("new account detected")
            return render_template("profile.html", user_data=user_data)


        return render_template("profile.html", user_data=user_data)

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
        flash("Activity Successfully added")
    return render_template("post_activity.html")


@app.route("/view_activity")
def view_activity():
    activities = Activity_log.query.filter_by(user_id=session["user"]).all()
    #access = Users.query.filter_by(user_id=session["user"]).all()
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


# Setting Edit
@app.route("/settings", methods=["GET", "POST"])
def settings():
    settings = Users.query.get_or_404(session["user"])
    if request.method == "POST":
        settings.icon_url = request.form.get("icon_url"),
        settings.icon_num = request.form.get("icon_num"),
        settings.email = request.form.get("email"),
        settings.group_name = request.form.get("group_name")
        
        db.session.commit()
        flash("Edits have been saved")
    return render_template("settings.html", settings=settings)


# comments
@app.route("/chat", methods=["GET", "POST"])
def chat():
    group = Users.query.filter_by(user_id=session["user"]).all()
    group_name=group[0].group_name
    comments = Chat_log.query.filter_by(group_name=group_name).all()
    if request.method == "POST":
        # check group name to see if user already exisits in db
        group = Users.query.filter_by(user_id=session["user"]).all()

        comment = Chat_log(
            user_id=session["user"],
            comment=request.form.get("comment"),
            group_name=group_name
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("chat"))
    return render_template("chat.html", comments=comments)

    
# get sum of distance traveled
@app.route("/map_link", methods=["GET"])
def map_link():
    update = Users.query.get_or_404(session["user"])
    # get sum total of all activity for a user
    total_distance = Activity_log.query.with_entities(
             func.sum(Activity_log.distance).label("mySum")).filter_by(user_id=session["user"]).first()
    
    lap_distance = 130
    # calculate current distance
    round_down = math.floor(total_distance[0])
    carry_decimal = total_distance[0] - round_down
    current_distance = round((round_down % lap_distance) + carry_decimal,1)
    # calculate number of laps
    laps_calc = total_distance[0] / lap_distance
    laps = math.floor(laps_calc)

    
    # load the JSON files containing the map reference data 
    landmarks = json.load(open("fitnesstracker/static/JSON/map_landmarks.json"))
    zones = json.load(open("fitnesstracker/static/JSON/map_zones.json"))
    coordinates = json.load(open("fitnesstracker/static/JSON/map_coordinates.json"))
    longitude = 0
    latitude = 0
    flash("current distance {}" .format(current_distance))
    
    for x in range(1,len(zones)):
        ref = str(x)
        # Get the ref for which lankmark you near.   and 
       
        if (current_distance >= zones[ref][0] and current_distance <= zones[ref][1]):
            longitude = coordinates[ref][0]
            latitude = coordinates[ref][1]
            update.total_distance = total_distance[0]
            update.current_distance = current_distance
            update.laps = laps
            update.longitude = longitude
            update.latitude = latitude
            db.session.commit()
            
    return render_template("map_link.html", update=update)


@app.route("/user_json")
def user_json():
    #identify all the users who share the same group as the session user in order to retrieve only their data
    group = Users.query.filter_by(user_id=session["user"]).all()
    group_name=group[0].group_name
    count = Users.query.filter_by(group_name=group_name).count()
    the_data = Users.query.filter_by(group_name=group_name).all()
    
    all_users = []
    for x in range(count):
        user_id = the_data[x].user_id
        first_name = the_data[x].first_name
        last_name = the_data[x].last_name
        icon_num = the_data[x].icon_num
        current_distance = the_data[x].current_distance
        total_distance = the_data[x].total_distance
        longitude = the_data[x].longitude
        latitude= the_data[x].latitude
        dict = {"id" : user_id, 
              "first" : first_name, 
              "last" : last_name,
              "icon_num" : icon_num,
              "current": current_distance,
              "total" : total_distance,
              "longitude" : longitude,
              "latitude" : latitude}
        all_users.append(dict)

    with open('fitnesstracker/static/JSON/user_data.json', 'w') as outfile:
        json.dump(all_users, outfile)
    return render_template("user_json.html")


@app.route("/landmark_json")
def landmark_json():
    map_data = Map_data.query.all()
    count = Map_data.query.count()
    
    all_landmarks = []
    for x in range(count):
        landmark_id = map_data[x].landmark_id
        landmark_name = map_data[x].landmark_name
        modal_link = map_data[x].modal_link
        video_link = map_data[x].video_link
        main_image = map_data[x].main_image
        body_text = map_data[x].body_text
        longitude = map_data[x].longitude
        latitude= map_data[x].latitude
        dict = {"landmark_id" : landmark_id, 
              "landmark_name" : landmark_name, 
              "modal_link" : modal_link,
              "video_link": video_link,
              "main_image" : main_image,
              "body_text" : body_text,
              "longitude" : longitude,
              "latitude" : latitude}
        all_landmarks.append(dict)

    with open('fitnesstracker/static/JSON/landmark_data.json', 'w') as outfile:
        json.dump(all_landmarks, outfile)
    flash("Landmark data added to map")
    return render_template("landmark_json.html")


# Home page end point
@app.route("/map/<int:user_id>", methods=["GET", "POST"])
def map(user_id):
    data = Users.query.get_or_404(user_id)
    
    return render_template("map.html", data=data)


