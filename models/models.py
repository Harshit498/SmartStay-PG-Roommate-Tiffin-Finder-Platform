from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from extensions import db

class PG(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    sharing_type = db.Column(db.String(50), nullable=False)
    amenities = db.Column(db.String(200), nullable=False)  # Comma-separated
    image_url = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    gallery_images = db.Column(db.Text, nullable=True)  # Comma-separated image URLs
    food_menu = db.Column(db.Text, nullable=True)  # JSON string: {"days": [{"day": "Monday", "breakfast": [...], "lunch": [...], "dinner": [...]} ...]}

class Roommate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    about = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    hobbies = db.Column(db.String(200), nullable=True)  # Comma-separated hobbies/interests

class TiffinService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    menu = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    area_covered = db.Column(db.String(200), nullable=False)
    contact_info = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    contact_info = db.Column(db.String(100), nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # student, owner, vendor, admin

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Optional, for multi-user
    month = db.Column(db.String(20), nullable=False)
    rent = db.Column(db.Integer, nullable=False)
    food = db.Column(db.Integer, nullable=False)
    other = db.Column(db.Integer, nullable=False)
    transport = db.Column(db.Integer, nullable=True)

class RoommateBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    roommate_id = db.Column(db.Integer, db.ForeignKey('roommate.id'), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

class TiffinBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('tiffin_vendor.id'), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('tiffin_menu.id'))
    date = db.Column(db.Date)
    type = db.Column(db.String(20))  # daily, monthly, trial
    status = db.Column(db.String(20), default='pending')
    user = db.relationship('User', backref='tiffin_bookings')
    menu = db.relationship('TiffinMenu')

class TiffinVendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    image_url = db.Column(db.String(255))
    is_approved = db.Column(db.Boolean, default=False)
    menus = db.relationship('TiffinMenu', backref='vendor', lazy=True)
    reviews = db.relationship('TiffinReview', backref='vendor', lazy=True)
    bookings = db.relationship('TiffinBooking', backref='vendor', lazy=True)
    food_menu = db.Column(db.Text, nullable=True)  # JSON string for weekly menu

class TiffinMenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('tiffin_vendor.id'), nullable=False)
    day = db.Column(db.String(20))  # e.g. Monday, Tuesday
    items = db.Column(db.Text)  # Comma-separated
    price = db.Column(db.Integer)

class TiffinReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('tiffin_vendor.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='tiffin_reviews')

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), default='info')  # info, request, chat, etc.
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='notifications')

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pg_id = db.Column(db.Integer, db.ForeignKey('pg.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')
    user = db.relationship('User', backref='bookings')
    pg = db.relationship('PG', backref='bookings')

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pg_id = db.Column(db.Integer, db.ForeignKey('pg.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='contact_messages')
    pg = db.relationship('PG', backref='contact_messages')

class RoommateRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_roommate_requests')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_roommate_requests')

class RoommateChat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_roommate_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_roommate_messages') 