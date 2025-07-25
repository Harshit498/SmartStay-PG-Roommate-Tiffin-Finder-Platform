from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from models.models import db, TiffinVendor, TiffinMenu, TiffinBooking, TiffinReview
from datetime import datetime
import json

# Blueprint

tiffin_bp = Blueprint('tiffin', __name__, url_prefix='/tiffin')

@tiffin_bp.route('/')
def list_vendors():
    tiffins = TiffinVendor.query.filter_by(is_approved=True).all()
    return render_template('tiffins.html', tiffins=tiffins)

@tiffin_bp.route('/<int:vendor_id>')
def vendor_detail(vendor_id):
    tiffin = TiffinVendor.query.get_or_404(vendor_id)
    menus = TiffinMenu.query.filter_by(vendor_id=vendor_id).all()
    reviews = TiffinReview.query.filter_by(vendor_id=vendor_id).order_by(TiffinReview.timestamp.desc()).all()
    # Parse food_menu JSON if present
    food_menu = None
    if hasattr(tiffin, 'food_menu') and tiffin.food_menu:
        try:
            food_menu = json.loads(tiffin.food_menu)
        except Exception:
            food_menu = None
    return render_template('tiffin_detail.html', tiffin=tiffin, menus=menus, reviews=reviews, food_menu=food_menu)

@tiffin_bp.route('/book/<int:vendor_id>', methods=['GET', 'POST'])
@login_required
def book_tiffin(vendor_id):
    tiffin = TiffinVendor.query.get_or_404(vendor_id)
    if request.method == 'POST':
        plan = request.form.get('plan')
        menu_id = request.form.get('menu_id')
        booking = TiffinBooking(user_id=current_user.id, vendor_id=vendor_id, menu_id=menu_id, type=plan, status='pending')
        db.session.add(booking)
        db.session.commit()
        flash('Tiffin booking submitted!', 'success')
        return render_template('tiffin_book.html', tiffin=tiffin)
    menus = TiffinMenu.query.filter_by(vendor_id=vendor_id).all()
    return render_template('tiffin_book.html', tiffin=tiffin, menus=menus)

@tiffin_bp.route('/trial/<int:vendor_id>', methods=['GET', 'POST'])
@login_required
def trial_tiffin(vendor_id):
    tiffin = TiffinVendor.query.get_or_404(vendor_id)
    if request.method == 'POST':
        booking = TiffinBooking(user_id=current_user.id, vendor_id=vendor_id, menu_id=None, type='trial', status='pending')
        db.session.add(booking)
        db.session.commit()
        flash('Trial request submitted!', 'success')
        return render_template('tiffin_trial.html', tiffin=tiffin)
    return render_template('tiffin_trial.html', tiffin=tiffin)

@tiffin_bp.route('/review/<int:vendor_id>', methods=['POST'])
@login_required
def review_tiffin(vendor_id):
    vendor = TiffinVendor.query.get_or_404(vendor_id)
    rating = int(request.form.get('rating', 5))
    comment = request.form.get('comment', '')
    review = TiffinReview(user_id=current_user.id, vendor_id=vendor_id, rating=rating, comment=comment, timestamp=datetime.utcnow())
    db.session.add(review)
    db.session.commit()
    flash('Review submitted!', 'success')
    return redirect(url_for('tiffin.vendor_detail', vendor_id=vendor_id))

@tiffin_bp.route('/vendor/dashboard')
@login_required
def vendor_dashboard():
    # Only allow vendors (add role check if needed)
    vendors = TiffinVendor.query.filter_by(is_approved=True).all()  # TODO: filter by current_user if vendor
    bookings = TiffinBooking.query.all()  # TODO: filter by vendor
    return render_template('tiffin_dashboard.html', vendors=vendors, bookings=bookings) 