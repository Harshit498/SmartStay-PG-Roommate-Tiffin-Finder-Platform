from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, send_file
from flask_login import login_required, current_user
from models.models import db, Roommate, RoommateRequest, User, RoommateChat, Notification
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_socketio import emit, join_room
from sqlalchemy import or_, and_
from flask_mail import Message
from flask import current_app
import io

def send_email_notification(to, subject, body):
    try:
        mail = current_app.extensions['mail']
        msg = Message(subject, recipients=[to], body=body)
        mail.send(msg)
    except Exception as e:
        print(f'Email send failed: {e}')

roommate_bp = Blueprint('roommate', __name__, url_prefix='/roommates')

class RoommateProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    gender = SelectField('Gender', choices=[('Male','Male'),('Female','Female')], validators=[DataRequired()])
    location = StringField('Preferred Locality', validators=[DataRequired(), Length(max=100)])
    budget = IntegerField('Budget (₹/month)', validators=[DataRequired(), NumberRange(min=1000, max=100000)])
    hobbies = StringField('Hobbies/Interests (comma-separated)', validators=[Length(max=200)])
    about = TextAreaField('About You', validators=[Length(max=500)])
    image_url = StringField('Profile Image URL', validators=[Length(max=200)])
    submit = SubmitField('Save Profile')

@roommate_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    # In production, filter by user_id
    profile = Roommate.query.filter_by(name=current_user.username).first()
    form = RoommateProfileForm(obj=profile)
    if form.validate_on_submit():
        if not profile:
            profile = Roommate()
            db.session.add(profile)
        form.populate_obj(profile)
        profile.name = current_user.username  # Link to user
        db.session.commit()
        flash('Profile saved!', 'success')
        return redirect(url_for('roommate.profile'))
    return render_template('roommate/profile.html', form=form, profile=profile)

@roommate_bp.route('/search')
def search():
    gender = request.args.get('gender')
    location = request.args.get('location')
    budget = request.args.get('budget')
    query = Roommate.query
    if gender:
        query = query.filter_by(gender=gender)
    if location:
        query = query.filter(Roommate.location.ilike(f'%{location}%'))
    if budget:
        try:
            budget_val = int(budget)
            query = query.filter(Roommate.budget <= budget_val)
        except ValueError:
            pass
    roommates = query.all()
    return render_template('roommate/search.html', roommates=roommates, RoommateRequest=RoommateRequest)

@roommate_bp.route('/request/<int:receiver_id>', methods=['POST'])
@login_required
def send_request(receiver_id):
    if receiver_id == current_user.id:
        flash('You cannot send a request to yourself.', 'warning')
        return redirect(url_for('roommate.search'))
    existing = RoommateRequest.query.filter_by(sender_id=current_user.id, receiver_id=receiver_id).first()
    if existing:
        flash('Request already sent.', 'info')
        return redirect(url_for('roommate.search'))
    req = RoommateRequest(sender_id=current_user.id, receiver_id=receiver_id)
    db.session.add(req)
    # Create notification for receiver
    notif = Notification(user_id=receiver_id, message=f'You have a new roommate request from {current_user.username}', type='request')
    db.session.add(notif)
    db.session.commit()
    flash('Request sent!', 'success')
    receiver = User.query.get(receiver_id)
    if receiver and receiver.email:
        send_email_notification(receiver.email, 'New Roommate Request', f'You have a new roommate request from {current_user.username} on SmartStay.')
    return redirect(url_for('roommate.search'))

@roommate_bp.route('/requests')
@login_required
def requests_dashboard():
    sent = RoommateRequest.query.filter_by(sender_id=current_user.id).all()
    received = RoommateRequest.query.filter_by(receiver_id=current_user.id).all()
    matches = RoommateRequest.query.filter_by(status='accepted').filter(
        (RoommateRequest.sender_id==current_user.id) | (RoommateRequest.receiver_id==current_user.id)
    ).all()
    return render_template('roommate/dashboard.html', sent=sent, received=received, matches=matches)

@roommate_bp.route('/request/<int:req_id>/accept', methods=['POST'])
@login_required
def accept_request(req_id):
    req = RoommateRequest.query.get_or_404(req_id)
    if req.receiver_id != current_user.id:
        abort(403)
    req.status = 'accepted'
    # Notify sender
    notif = Notification(user_id=req.sender_id, message=f'{current_user.username} accepted your roommate request!', type='request')
    db.session.add(notif)
    db.session.commit()
    flash('Request accepted! You are now matched.', 'success')
    sender = User.query.get(req.sender_id)
    if sender and sender.email:
        send_email_notification(sender.email, 'Roommate Request Accepted', f'{current_user.username} accepted your roommate request on SmartStay!')
    return redirect(url_for('roommate.requests_dashboard'))

@roommate_bp.route('/request/<int:req_id>/reject', methods=['POST'])
@login_required
def reject_request(req_id):
    req = RoommateRequest.query.get_or_404(req_id)
    if req.receiver_id != current_user.id:
        abort(403)
    req.status = 'rejected'
    # Notify sender
    notif = Notification(user_id=req.sender_id, message=f'{current_user.username} rejected your roommate request.', type='request')
    db.session.add(notif)
    db.session.commit()
    flash('Request rejected.', 'info')
    sender = User.query.get(req.sender_id)
    if sender and sender.email:
        send_email_notification(sender.email, 'Roommate Request Rejected', f'{current_user.username} rejected your roommate request on SmartStay.')
    return redirect(url_for('roommate.requests_dashboard'))

@roommate_bp.route('/chat/<int:user_id>')
@login_required
def chat(user_id):
    # Only allow chat if matched
    match = RoommateRequest.query.filter_by(status='accepted').filter(
        or_(
            and_(RoommateRequest.sender_id==current_user.id, RoommateRequest.receiver_id==user_id),
            and_(RoommateRequest.sender_id==user_id, RoommateRequest.receiver_id==current_user.id)
        )
    ).first()
    if not match:
        flash('You are not matched with this user.', 'danger')
        return redirect(url_for('roommate.requests_dashboard'))
    q = request.args.get('q', '').strip()
    base_query = RoommateChat.query.filter(
        ((RoommateChat.sender_id==current_user.id) & (RoommateChat.receiver_id==user_id)) |
        ((RoommateChat.sender_id==user_id) & (RoommateChat.receiver_id==current_user.id))
    )
    if q:
        messages = base_query.filter(RoommateChat.message.ilike(f'%{q}%')).order_by(RoommateChat.timestamp.asc()).all()
    else:
        messages = base_query.order_by(RoommateChat.timestamp.asc()).all()
    return render_template('roommate/chat.html', user_id=user_id, messages=messages)

@roommate_bp.route('/chat/<int:user_id>/download')
@login_required
def download_chat(user_id):
    match = RoommateRequest.query.filter_by(status='accepted').filter(
        or_(
            and_(RoommateRequest.sender_id==current_user.id, RoommateRequest.receiver_id==user_id),
            and_(RoommateRequest.sender_id==user_id, RoommateRequest.receiver_id==current_user.id)
        )
    ).first()
    if not match:
        flash('You are not matched with this user.', 'danger')
        return redirect(url_for('roommate.requests_dashboard'))
    messages = RoommateChat.query.filter(
        ((RoommateChat.sender_id==current_user.id) & (RoommateChat.receiver_id==user_id)) |
        ((RoommateChat.sender_id==user_id) & (RoommateChat.receiver_id==current_user.id))
    ).order_by(RoommateChat.timestamp.asc()).all()
    chat_text = '\n'.join([
        f"[{m.timestamp.strftime('%Y-%m-%d %H:%M')}] {m.sender.username}: {m.message or ''}" for m in messages
    ])
    buf = io.BytesIO()
    buf.write(chat_text.encode('utf-8'))
    buf.seek(0)
    return send_file(buf, mimetype='text/plain', as_attachment=True, download_name='chat_history.txt')

from app import socketio

@socketio.on('join_room')
def handle_join_room(data):
    room = data['room']
    join_room(room)

@socketio.on('send_message')
def handle_send_message(data):
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']
    message = data['message']
    room = data['room']
    # Save to DB
    chat = RoommateChat(sender_id=sender_id, receiver_id=receiver_id, message=message)
    db.session.add(chat)
    # Create notification for receiver
    notif = Notification(user_id=receiver_id, message=f'New message from {chat.sender.username}', type='chat')
    db.session.add(notif)
    db.session.commit()
    emit('receive_message', {
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'message': message,
        'timestamp': chat.timestamp.strftime('%Y-%m-%d %H:%M')
    }, room=room)
    receiver = User.query.get(receiver_id)
    if receiver and receiver.email:
        send_email_notification(receiver.email, 'New Chat Message', f'You have a new message from {chat.sender.username} on SmartStay.') 