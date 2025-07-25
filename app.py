from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, current_user
from flask_socketio import SocketIO
from flask_mail import Mail, Message
import os
from config import Config
from models.models import Notification, Booking, RoommateBooking, TiffinBooking, PG, Roommate, TiffinVendor
from extensions import db

# Extensions
app = Flask(__name__)
app.config.from_object(Config)
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@smartstay.com')
mail = Mail(app)
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
socketio = SocketIO(app)

# Import and register blueprints
from blueprints.auth import auth_bp
app.register_blueprint(auth_bp)
from blueprints.listings import listings_bp
app.register_blueprint(listings_bp)
from blueprints.roommate import roommate_bp
app.register_blueprint(roommate_bp)
from blueprints.tiffin import tiffin_bp
app.register_blueprint(tiffin_bp)
from blueprints.events import events_bp
app.register_blueprint(events_bp)
from blueprints.expenses import expenses_bp
app.register_blueprint(expenses_bp)

# User loader for Flask-Login
from models.models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home route (placeholder)
@app.route('/')
def home():
    from models.models import PG
    featured_pgs = PG.query.limit(6).all()
    return render_template('home.html', featured_pgs=featured_pgs)

@app.route('/notifications')
@login_required
def notifications():
    notifs = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.timestamp.desc()).all()
    # Mark all as read
    for n in notifs:
        n.is_read = True
    from models.models import db
    db.session.commit()
    return render_template('notifications.html', notifications=notifs)

@app.route('/profile')
@login_required
def profile():
    # Bookings for the user
    property_bookings = Booking.query.filter_by(user_id=current_user.id).all()
    roommate_bookings = RoommateBooking.query.filter_by(user_id=current_user.id).all()
    tiffin_bookings = TiffinBooking.query.filter_by(user_id=current_user.id).all()
    pgs = {pg.id: pg for pg in PG.query.all()}
    roommates = {r.id: r for r in Roommate.query.all()}
    tiffins = {v.id: v for v in TiffinVendor.query.all()}
    return render_template('profile.html', user=current_user, property_bookings=property_bookings, roommate_bookings=roommate_bookings, tiffin_bookings=tiffin_bookings, pgs=pgs, roommates=roommates, tiffins=tiffins)

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'owner':
        return redirect(url_for('listings.owner_dashboard'))
    elif current_user.role == 'vendor':
        return redirect(url_for('tiffin.vendor_dashboard'))
    elif current_user.role == 'student':
        return redirect(url_for('expenses.dashboard'))
    else:
        # For admin or unknown roles, redirect to home or a generic dashboard
        return redirect(url_for('home'))

@app.route('/my_bookings')
@login_required
def my_bookings():
    # Property bookings
    property_bookings = Booking.query.filter_by(user_id=current_user.id).all()
    # Roommate bookings
    roommate_bookings = RoommateBooking.query.filter_by(user_id=current_user.id).all()
    # Tiffin bookings
    tiffin_bookings = TiffinBooking.query.filter_by(user_id=current_user.id).all()
    # Get related objects for display
    pgs = {pg.id: pg for pg in PG.query.all()}
    roommates = {r.id: r for r in Roommate.query.all()}
    tiffins = {v.id: v for v in TiffinVendor.query.all()}
    return render_template('my_bookings.html', property_bookings=property_bookings, roommate_bookings=roommate_bookings, tiffin_bookings=tiffin_bookings, pgs=pgs, roommates=roommates, tiffins=tiffins)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True) 