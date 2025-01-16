from flask import Blueprint, request, jsonify
from app import db
from app.models.spending.recurring_spending import RecurringSpending
from app.models.spending.spending import Spending
from datetime import datetime, timedelta

recurring_bp = Blueprint('recurring', __name__, url_prefix='/api/recurring')

@recurring_bp.route('/', methods=['POST'])
def add_recurring_spending():
    data = request.json
    spending = Spending.query.get(data['spending_id'])
    if not spending:
        return jsonify({'error': 'Spending not found'}), 404

    next_occurrence = datetime.strptime(data['next_occurrence'], '%Y-%m-%dT%H:%M:%S')
    recurring = RecurringSpending(
        spending_id=spending.id,
        frequency=data['frequency'],
        next_occurrence=next_occurrence
    )
    db.session.add(recurring)
    db.session.commit()
    return jsonify({'message': 'Recurring spending added successfully', 'recurring_id': recurring.id}), 201

@recurring_bp.route('/', methods=['GET'])
def get_recurring_spendings():
    recurring_spendings = RecurringSpending.query.all()
    return jsonify([{
        'id': r.id,
        'spending_id': r.spending_id,
        'frequency': r.frequency,
        'next_occurrence': r.next_occurrence
    } for r in recurring_spendings]), 200
