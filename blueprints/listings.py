from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from models.models import db, PG, Booking, ContactMessage
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, FileField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, NumberRange, Email

listings_bp = Blueprint('listings', __name__, url_prefix='/listings')

class ListingForm(FlaskForm):
    name = StringField('Property Name', validators=[DataRequired(), Length(max=100)])
    city = StringField('City', validators=[DataRequired(), Length(max=50)])
    address = StringField('Address', validators=[DataRequired(), Length(max=200)])
    price = IntegerField('Price (₹/month)', validators=[DataRequired(), NumberRange(min=1000, max=100000)])
    sharing_type = SelectField('Occupancy Type', choices=[('1BHK','1BHK'),('2BHK','2BHK'),('3-sharing','3-sharing'),('PG','PG'),('Flat','Flat'),('Villa','Villa')], validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male','Male'),('Female','Female'),('Unisex','Unisex')], validators=[DataRequired()])
    amenities = StringField('Amenities (comma-separated)', validators=[DataRequired()])
    food = StringField('Food (e.g. Home-style, North Indian, etc.)', validators=[DataRequired()])
    image_url = StringField('Main Image URL', validators=[DataRequired(), Length(max=200)])
    gallery_images = StringField('Gallery Image URLs (comma-separated)', validators=[Length(max=1000)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Save Listing')

class BookingForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Mobile', validators=[DataRequired()])
    move_in = DateField('Move-in Date', validators=[DataRequired()])
    submit = SubmitField('Book Now')

class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')

# Owner: Add Listing
@listings_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_listing():
    if current_user.role != 'owner':
        abort(403)
    form = ListingForm()
    if form.validate_on_submit():
        pg = PG(
            name=form.name.data,
            city=form.city.data,
            address=form.address.data,
            price=form.price.data,
            sharing_type=form.sharing_type.data,
            amenities=form.amenities.data,
            image_url=form.image_url.data,
            gallery_images=form.gallery_images.data,
            description=form.description.data
        )
        db.session.add(pg)
        db.session.commit()
        flash('Listing added successfully!', 'success')
        return redirect(url_for('listings.my_listings'))
    return render_template('listings/add.html', form=form)

# Owner: My Listings
@listings_bp.route('/my')
@login_required
def my_listings():
    if current_user.role != 'owner':
        abort(403)
    listings = PG.query.all()  # In production, filter by owner_id
    return render_template('listings/my_listings.html', listings=listings)

# Owner: Edit Listing
@listings_bp.route('/edit/<int:pg_id>', methods=['GET', 'POST'])
@login_required
def edit_listing(pg_id):
    if current_user.role != 'owner':
        abort(403)
    pg = PG.query.get_or_404(pg_id)
    form = ListingForm(obj=pg)
    if form.validate_on_submit():
        form.populate_obj(pg)
        db.session.commit()
        flash('Listing updated!', 'success')
        return redirect(url_for('listings.my_listings'))
    return render_template('listings/edit.html', form=form, pg=pg)

# Owner: Delete Listing
@listings_bp.route('/delete/<int:pg_id>', methods=['POST'])
@login_required
def delete_listing(pg_id):
    if current_user.role != 'owner':
        abort(403)
    pg = PG.query.get_or_404(pg_id)
    db.session.delete(pg)
    db.session.commit()
    flash('Listing deleted.', 'info')
    return redirect(url_for('listings.my_listings'))

# Public: List all
@listings_bp.route('/', methods=['GET'])
def public_listings():
    city = request.args.get('city')
    pg_type = request.args.get('type')
    gender = request.args.get('gender')
    query = PG.query
    if city:
        query = query.filter(PG.city.ilike(f'%{city}%'))
    if pg_type:
        query = query.filter(PG.sharing_type.ilike(f'%{pg_type}%'))
    if gender:
        query = query.filter(PG.description.ilike(f'%{gender}%'))
    listings = query.all()
    return render_template('listings/public_list.html', listings=listings)

# Public: Detail page
@listings_bp.route('/<int:pg_id>')
def listing_detail(pg_id):
    pg = PG.query.get_or_404(pg_id)
    return render_template('listings/detail.html', pg=pg)

@listings_bp.route('/<int:pg_id>/book', methods=['GET', 'POST'])
def book_listing(pg_id):
    pg = PG.query.get_or_404(pg_id)
    form = BookingForm()
    if form.validate_on_submit():
        booking = Booking(
            pg_id=pg.id,
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            move_in=form.move_in.data
        )
        db.session.add(booking)
        db.session.commit()
        flash('Booking request submitted! The owner will contact you soon.', 'success')
        return redirect(url_for('listings.listing_detail', pg_id=pg_id))
    return render_template('listings/book.html', pg=pg, form=form)

@listings_bp.route('/<int:pg_id>/contact', methods=['GET', 'POST'])
def contact_owner(pg_id):
    pg = PG.query.get_or_404(pg_id)
    form = ContactForm()
    if form.validate_on_submit():
        message = ContactMessage(
            pg_id=pg.id,
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        db.session.add(message)
        db.session.commit()
        flash('Your message has been sent to the owner!', 'success')
        return redirect(url_for('listings.listing_detail', pg_id=pg_id))
    return render_template('listings/contact.html', pg=pg, form=form)

@listings_bp.route('/owner_dashboard')
@login_required
def owner_dashboard():
    if current_user.role != 'owner':
        abort(403)
    listings = PG.query.all()  # In production, filter by owner_id
    bookings = Booking.query.all()
    messages = ContactMessage.query.all()
    return render_template('listings/owner_dashboard.html', listings=listings, bookings=bookings, messages=messages) 