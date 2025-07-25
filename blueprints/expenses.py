from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.models import db, Expense
from datetime import datetime

expenses_bp = Blueprint('expenses', __name__, url_prefix='/expenses')

@expenses_bp.route('/')
@login_required
def dashboard():
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.month.desc()).all()
    return render_template('expenses_dashboard.html', expenses=expenses)

@expenses_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        month = request.form.get('month')
        rent = int(request.form.get('rent', 0))
        food = int(request.form.get('food', 0))
        other = int(request.form.get('other', 0))
        transport = int(request.form.get('transport', 0))
        expense = Expense(user_id=current_user.id, month=month, rent=rent, food=food, other=other, transport=transport)
        db.session.add(expense)
        db.session.commit()
        flash('Expense added!', 'success')
        return redirect(url_for('expenses.dashboard'))
    return render_template('add_expense.html')

@expenses_bp.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('expenses.dashboard'))
    if request.method == 'POST':
        expense.month = request.form.get('month')
        expense.rent = int(request.form.get('rent', 0))
        expense.food = int(request.form.get('food', 0))
        expense.other = int(request.form.get('other', 0))
        expense.transport = int(request.form.get('transport', 0))
        db.session.commit()
        flash('Expense updated!', 'success')
        return redirect(url_for('expenses.dashboard'))
    return render_template('edit_expense.html', expense=expense) 