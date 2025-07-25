from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from models.models import db, Event
from datetime import datetime

# Blueprint

events_bp = Blueprint('events', __name__, url_prefix='/events')

@events_bp.route('/')
def list_events():
    events = Event.query.order_by(Event.date).all()
    return render_template('events.html', events=events)

@events_bp.route('/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_query.html', event=event)

@events_bp.route('/book/<int:event_id>', methods=['POST'])
@login_required
def book_event(event_id):
    # TODO: Save RSVP/booking to database
    flash('Event booking successful!', 'success')
    return redirect(url_for('events.list_events')) 