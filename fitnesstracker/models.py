from fitnesstracker import db
from sqlalchemy.dialects.postgresql import JSON
import datetime


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(140), unique=True, nullable=False)
    account_created = db.Column(db.DateTime, default=datetime.datetime.now)
    icon_url = db.Column(db.String(50), unique=True, nullable=True)
    access = db.Column(db.String(6), nullable=False, default=False)
    refresh_token = db.Column(db.String(50), unique=True)
    connection_status = db.Column(db.Boolean, default=False, nullable=False)
    update_status = db.Column(db.Boolean, default=False, nullable=False)
    longitude = db.Column(db.Float, nullable=False, default=-4.0929)
    latitude = db.Column(db.Float, nullable=False, default=53.2637)
    miles = db.Column(db.Boolean, default=True, nullable=False)
    group_name = db.Column(db.String(4), nullable=False, default='all')
    total_distance = db.Column(db.Float, nullable=False, default=0)
    current_distance = db.Column(db.Float, nullable=False, default=0)
    laps = db.Column(db.Integer, nullable=False, default=0)
    connection_date = db.Column(db.Date, nullable=False)
    strava_fetch = db.Column(db.Boolean, default=False, nullable=False)
    unlocked_zones = db.Column(JSON)
    strava_last_activity_id = db.Column(db.String(20), unique=True, nullable=False, default='new account')
    landmarks = db.relationship("Map_data", backref="users", cascade="all, delete", lazy=True)
    notify = db.relationship("Notifications", backref="users", cascade="all, delete", lazy=True)
    chats = db.relationship("Chat_log", backref="users", cascade="all, delete", lazy=True)
    activities = db.relationship("Activity_log", backref="users", cascade="all, delete", lazy=True)
    group = db.relationship("Groups", backref="users", cascade="all, delete", lazy=True)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.email


class Map_data(db.Model):
    landmark_id = db.Column(db.Integer, primary_key=True)
    landmark_name = db.Column(db.String(50), unique=True, nullable=False)
    modal_link = db.Column(db.String(10), unique=True, nullable=False)
    main_image = db.Column(db.String(100), unique=True, nullable=False)
    video_link = db.Column(db.Text, nullable=False)
    body_text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.landmark_name


class Notifications(db.Model):
    notifcation_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    notification_text = db.Column(db.Text, nullable=False)
    marked_as_read = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0} - Read: {1}".format(
            self.user_id, self.marked_as_read
        )


class Chat_log(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    group_name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.comment_id


class Activity_log(db.Model):
    entry_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    distance = db.Column(db.Float, nullable=False)
    activity_type = db.Column(db.String(4), nullable=False)
    commute = db.Column(db.Boolean, default=False, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    strava_activity_id = db.Column(db.String(4), unique=True)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.user_id


class Groups(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.name  
