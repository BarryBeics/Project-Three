from flask import render_template, request, redirect, \
    url_for, flash, session, jsonify
from sqlalchemy import func
from fitnesstracker import app, db
from fitnesstracker.models import Users, Map_data, \
    Chat_log, Activity_log, Groups
from werkzeug.security import generate_password_hash, check_password_hash
import math
import json
import functools


# SECURITY - Check user is logged in
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "user" not in session:
            flash("You need to be logged in to access that page!")
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)

    return secure_function


# SECURITY - Restirc access to admin pages
def admin_access(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        access = Users.query.filter(Users.user_id == session["user"]).first()
        if access.access is False:
            flash('Sorry, You must have admin rights to access that page!')
            return redirect(url_for("home"))
        return func(*args, **kwargs)

    return secure_function


# DATE FORMAT - Date filter
@app.template_filter('datetimeformat')
def datetimeformat(value, format='%B %d, %Y'):
    return value.strftime(format)


# ADMIN - Landmarks
@app.route("/add_landmark", methods=["GET", "POST"])
@login_required
@admin_access
def add_landmark():
    if request.method == "POST":
        # Check landmark name to see if user already exisits in db
        existing_landmark = Map_data.query.filter(
            Map_data.landmark_name == request.form.get("landmark_name")).all()

        if existing_landmark:
            flash("Landmark already exists")
            return redirect(url_for("add_landmark"))

        # Check Modal Link to see if user already exisits in db
        existing_modal_link = Map_data.query.filter(
            Map_data.modal_link == request.form.get("modal_link")).all()

        if existing_modal_link:
            flash("Modal Link already exists")
            return redirect(url_for("add_landmark"))

        # Check main image name to see if user already exisits in db
        existing_main_image = Map_data.query.filter(
            Map_data.main_image == request.form.get("main_image")).all()

        if existing_main_image:
            flash("Main Image already exists")
            return redirect(url_for("add_landmark"))

        landmark = Map_data(
            landmark_name=request.form.get("landmark_name"),
            modal_link=request.form.get("modal_link"),
            main_image=request.form.get("main_image"),
            body_text=request.form.get("body_text"),
            user_id=session["user"],
            longitude=request.form.get("longitude"),
            latitude=request.form.get("latitude")
        )
        db.session.add(landmark)
        db.session.commit()
        # Redirect to landmark json to update json file for the map
        return redirect(url_for("landmark_json"))
    return render_template("admin/add_landmark.html")


# ADMIN - Admin
@app.route("/admin")
@login_required
@admin_access
def admin():
    return render_template("admin/admin.html")


# ADMIN - Group
@app.route("/edit_group/<int:group_id>", methods=["GET", "POST"])
@login_required
@admin_access
def edit_group(group_id):
    group = Groups.query.get_or_404(group_id)
    # Check group name to see if user already exisits in db
    existing_group = Groups.query.filter(
        Groups.name == request.form.get("name")).all()
    # Check if the group size has been change
    size_change = Groups.query.filter(
        Groups.size == request.form.get("size")).all()

    if existing_group:
        if request.method == "POST":
            if size_change:
                flash("No change!")
                return redirect(url_for("edit_group", group_id=group_id))

            group.size = request.form.get("size")
            db.session.commit()
            flash("Group size updated!")            
            return redirect(url_for("edit_group", group_id=group_id))

    if request.method == "POST":
        group.name = request.form.get("name")
        group.size = request.form.get("size")
        db.session.commit()
        flash("Group data updated!")
        return redirect(url_for("edit_group", group_id=group_id))
    return render_template("admin/edit_group.html", group=group)


# ADMIN - Landmark
@app.route("/edit_landmark/<int:landmark_id>", methods=["GET", "POST"])
@login_required
@admin_access
def edit_landmark(landmark_id):
    landmark = Map_data.query.get_or_404(landmark_id)
    if request.method == "POST":
        landmark.landmark_name = request.form.get("landmark_name")
        landmark.modal_link = request.form.get("modal_link"),
        landmark.main_image = request.form.get("main_image"),
        landmark.body_text = request.form.get("body_text"),
        user_id = session["user"],
        landmark.longitude = request.form.get("longitude"),
        landmark.latitude = request.form.get("latitude")
        db.session.commit()
        # Redirect to landmark json to update json file for the map
        return redirect(url_for("landmark_json"))
    return render_template("admin/edit_landmark.html", landmark=landmark)


# ADMIN - Users
@app.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
@login_required
@admin_access
def edit_user(user_id):
    user = Users.query.get_or_404(user_id)
    if request.method == "POST":
        user.access = request.form.get("access") == 'on'
        user.longitude = request.form.get("longitude")
        user.latitude = request.form.get("latitude")
        db.session.commit()
        return redirect(url_for("users"))
    return render_template("admin/edit_user.html", user=user)


# ADMIN - Groups
@app.route("/groups")
@login_required
@admin_access
def groups():
    groups = list(Groups.query.order_by(Groups.name).all())
    return render_template("admin/groups.html", groups=groups)


# ADMIN - Landmarks
@app.route("/landmarks")
@login_required
@admin_access
def landmarks():
    landmarks = list(Map_data.query.order_by(Map_data.modal_link).all())
    return render_template("admin/landmarks.html", landmarks=landmarks)


# ADMIN - Users
@app.route("/users")
@login_required
@admin_access
def users():
    users = list(Users.query.order_by(Users.first_name).all())
    return render_template("admin/users.html", users=users)


# ADMIN - DELETE User
@app.route("/delete_user/<int:user_id>")
@login_required
@admin_access
def delete_user(user_id):
    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("users"))


# ADMIN - DELETE Group
@app.route("/delete_group/<int:group_id>")
@login_required
@admin_access
def delete_group(group_id):
    group = Groups.query.get_or_404(group_id)
    db.session.delete(group)
    db.session.commit()
    return redirect(url_for("groups"))


# ADMIN - DELETE Landmark
@app.route("/delete_landmark/<int:landmark_id>")
@login_required
@admin_access
def delete_landmark(landmark_id):
    landmark = Map_data.query.get_or_404(landmark_id)
    db.session.delete(landmark)
    db.session.commit()
    return redirect(url_for("landmarks"))


# ERROR HANDLERS - Forbidden
@app.errorhandler(403)
def page_not_found(e):
    return render_template("error_handlers/403.html"), 403


# ERROR HANDLERS - Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error_handlers/404.html"), 404


# ERROR HANDLERS - Internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("error_handlers/500.html"), 500


# LOADING - Build Landmark JSON
@app.route("/landmark_json")
@login_required
def landmark_json():
    map_data = Map_data.query.all()
    count = Map_data.query.count()

    all_landmarks = []
    for x in range(count):
        landmark_id = map_data[x].landmark_id
        landmark_name = map_data[x].landmark_name
        modal_link = map_data[x].modal_link
        main_image = map_data[x].main_image
        body_text = map_data[x].body_text
        longitude = map_data[x].longitude
        latitude = map_data[x].latitude
        dict = {"landmark_id": landmark_id,
                "landmark_name": landmark_name,
                "modal_link": modal_link,
                "main_image": main_image,
                "body_text": body_text,
                "longitude": longitude,
                "latitude": latitude}
        all_landmarks.append(dict)

    with open('fitnesstracker/static/json/landmark_data.json', 'w') as outfile:
        json.dump(all_landmarks, outfile)
    flash("Landmark data added to map")
    return render_template("loading/landmark_json.html")


# LOADING - Map Link get sum of distance traveled
@app.route("/map_link", methods=["GET"])
@login_required
def map_link():
    # Check if this is a new user with no activity posted yet
    is_new = Activity_log.query.filter_by(user_id=session["user"]).count()
    if is_new == 0:
        flash('You will need to log an activity before viewing the map')
        return render_template("logged_in/post_activity.html")
    update = Users.query.get_or_404(session["user"])

    # get sum total of all activity for a user
    total_distance = Activity_log.query. \
        with_entities(func.sum(Activity_log.distance).label("mySum")). \
        filter_by(user_id=session["user"]).first()

    lap_distance = 130
    # calculate current distance
    round_down = math.floor(total_distance[0])
    carry_decimal = total_distance[0] - round_down
    current_distance = round((round_down % lap_distance) + carry_decimal, 1)

    # calculate number of laps
    laps_calc = total_distance[0] / lap_distance
    laps = math.floor(laps_calc)

    # load the JSON files containing the map reference data
    landmarks = json. \
        load(open("fitnesstracker/static/json/map_landmarks.json"))
    zones = json. \
        load(open("fitnesstracker/static/json/map_zones.json"))
    coordinates = json. \
        load(open("fitnesstracker/static/json/map_coordinates.json"))

    # Create coordinates variable to be update with users data
    longitude = 0
    latitude = 0
    flash("current distance {}" .format(current_distance))

    json_obj = update.unlocked_zones
    # Once the second if statement is true it sets switch to off
    # so that it doesn't get tried again
    switch = 'on'

    for x in range(1, len(zones)):
        mile = str(x)
        # Get the mile for which lankmark you near
        if (current_distance >= zones[mile][0] and
                current_distance <= zones[mile][1]):
            longitude = coordinates[mile][0]
            latitude = coordinates[mile][1]
            update.total_distance = total_distance[0]
            update.current_distance = current_distance
            update.laps = laps
            update.longitude = longitude
            update.latitude = latitude

        if switch == 'on':
            if (current_distance >= landmarks[mile][0] and
                    current_distance <= landmarks[mile][1]):

                landmark_num = landmarks[mile][2]
                json_obj[landmark_num] = 'yes'
                update.unlocked_zones = json_obj
                switch = 'off'

        db.session.commit()

    return render_template("loading/map_link.html", update=update)


# LOADING - Set up
@app.route("/set_up", methods=["GET", "POST"])
def set_up():
    if "user" in session:
        email = session["user"]
        # swap the session value from email to user_id
        user_data = Users.query.filter(Users.email == session["user"]).first()
        user_id = user_data.user_id
        session["user"] = user_id
        access = user_data.access
        session["access"] = access

        # As json column can not have a default value, detect
        # if this is a new account and
        # complete set up by adding this default to the users account
        is_new = Activity_log.query.filter_by(user_id=user_id).count()
        print(is_new)
        if is_new == 0:
            setup = Users.query.get_or_404(user_id)
            setup.unlocked_zones = {"L1": "no",
                                    "L2": "no",
                                    "L3": "no",
                                    "L4": "no",
                                    "L5": "no",
                                    "L6": "no",
                                    "L7": "no"}
            db.session.commit()
            flash("Account set up!")
            return render_template("loading/set_up.html", user_data=user_data)

        return render_template("loading/set_up.html", user_data=user_data)

    return redirect(url_for("login"))


# LOADING - Build User JSON
@app.route("/user_json")
@login_required
def user_json():
    # identify all the users who share the same group as
    # the session user in order to retrieve only their data
    group = Users.query.filter_by(user_id=session["user"]).all()
    group_name = group[0].group_name
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
        latitude = the_data[x].latitude
        dict = {"id": user_id,
                "first": first_name,
                "last": last_name,
                "icon_num": icon_num,
                "current": current_distance,
                "total": total_distance,
                "longitude": longitude,
                "latitude": latitude}
        all_users.append(dict)

    with open('fitnesstracker/static/json/user_data.json', 'w') as outfile:
        json.dump(all_users, outfile)
    return render_template("loading/user_json.html")


# LOGGED IN - Comments
@app.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    group = Users.query.filter_by(user_id=session["user"]).all()
    # Get the group name this user is part of
    group_name = group[0].group_name

    get_chat = db.session.query(Users, Chat_log).join(Chat_log). \
        filter(Users.group_name == group_name).all()

    if request.method == "POST":
        group = Users.query.filter_by(user_id=session["user"]).all()

        comment = Chat_log(
            user_id=session["user"],
            comment=request.form.get("comment"),
            group_name=group_name
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("chat"))
    return render_template("logged_in/chat.html", get_chat=get_chat)


# LOGGED IN - Edit Activity
@app.route("/edit_activity/<int:entry_id>", methods=["GET", "POST"])
@login_required
def edit_activity(entry_id):
    activity = Activity_log.query.get_or_404(entry_id)
    if request.method == "POST":
        activity.distance = request.form.get("distance")
        activity.activity_type = request.form.get("activity_type")
        activity.commute = request.form.get('commute') == 'on'

        db.session.commit()
        return redirect(url_for("view_activity"))
    return render_template("logged_in/edit_activity.html", activity=activity)


# LOGGED IN - Edit Comments
@app.route("/edit_comment/<int:comment_id>", methods=["GET", "POST"])
@login_required
def edit_comment(comment_id):
    comment = Chat_log.query.get_or_404(comment_id)
    if request.method == "POST":
        comment.comment = request.form.get("comment")
        db.session.commit()
        return redirect(url_for("chat"))
    return render_template("logged_in/edit_comment.html", comment=comment)


# LOGGED IN - Map view
@app.route("/map", methods=["GET", "POST"])
@login_required
def map():
    data = Users.query.get_or_404(session["user"])
    zones = Users.query.filter(Users.user_id == session["user"]).first()
    # Change Python Dict to a json object
    unlocked_status = zones.unlocked_zones

    json_object = json.dumps(unlocked_status)
    landmarks = Map_data.query.all()

    return render_template("logged_in/map.html", data=data,
                           json_object=json_object, landmarks=landmarks)


# LOGGED IN - Post Activity
@app.route("/post_activity", methods=["GET", "POST"])
@login_required
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
        return redirect(url_for("view_activity"))
    return render_template("logged_in/post_activity.html")


# LOGGED IN - Profile
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    if "user" in session:
        # swap the session value from email to user_id
        user_data = Users.query.filter(Users.
                                       user_id == session["user"]).first()
        # load the JSON files containing the icon images data
        icons = json.load(open("fitnesstracker/static/json/user_icons.json"))
        num_str = str(user_data.icon_num)
        icon = icons[num_str]
        return render_template("logged_in/profile.html",
                               user_data=user_data, icon=icon, num_str=num_str)

    return redirect(url_for("login"))


# LOGGED IN - Register a new group
@app.route("/register_group", methods=["GET", "POST"])
@login_required
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
        flash("Successfully created a group called: {}".format(
                            request.form.get("name")))

    return render_template("logged_in/register_group.html")


# LOGGED IN Settings
@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    # load the JSON files containing the icon images data
    icons = json.load(open("fitnesstracker/static/json/user_icons.json"))
    settings = Users.query.get_or_404(session["user"])
    num_str = str(settings.icon_num)

    groups = list(Groups.query.order_by(Groups.name).all())
    icon_nums = list(Users.query.order_by(Users.first_name).all())
    if request.method == "POST":
        settings.email = request.form.get("email")
        settings.group_name = request.form.get("group_name")
        settings.icon_num = request.form.get("icon_num")
        db.session.commit()
        flash("Your changes have been saved")
        return redirect(url_for("settings"))

    return render_template("logged_in/settings.html", settings=settings,
                           groups=groups, icon_nums=icon_nums,
                           icons=icons, num_str=num_str)


# LOGGED IN - View Activity
@app.route("/view_activity")
@login_required
def view_activity():
    activities = Activity_log. \
        query.filter(Activity_log.user_id == session["user"]). \
        order_by(Activity_log.date).all()
    return render_template("logged_in/view_activity.html",
                           activities=activities)


# LOGGED IN - DELETE Activity
@app.route("/delete_activity/<int:entry_id>")
@login_required
def delete_activity(entry_id):
    activity = Activity_log.query.get_or_404(entry_id)
    db.session.delete(activity)
    db.session.commit()
    return redirect(url_for("view_activity"))


# LOGGED IN - DELETE User own account
@app.route("/delete_self/<int:user_id>")
@login_required
def delete_self(user_id):
    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Your account has been succefully deleted!')
    session.pop("user")
    return redirect(url_for("home"))


# LOGGED IN - DELETE Comments
@app.route("/delete_comment/<int:comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Chat_log.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for("chat"))


# LOGGED IN - Logout
@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# PUBLIC - Landing page
@app.route("/")
def home():
    return render_template("public/landing_page.html")


#  PUBLIC - Log In
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
                        return redirect(url_for("set_up"))
            else:
                # invalid password
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # email doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("public/login.html")


#  PUBLIC - Register New User
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
        return redirect(url_for("set_up", email=session["user"]))

    return render_template("public/register.html")
