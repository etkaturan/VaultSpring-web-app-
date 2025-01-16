from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.spending.recurring_spending import RecurringSpending
from app.models.spending.spending import Spending
from datetime import datetime

recurring_bp = Blueprint('recurring', __name__, url_prefix='/api/recurring')

@recurring_bp.route('/', methods=['POST'])
@jwt_required()
def add_recurring_spending():
    """
    Adds a new recurring spending based on an existing spending entry.
    """
    user_id = get_jwt_identity()
    data = request.json

    # Validate spending ID
    spending = Spending.query.filter_by(id=data['spending_id'], user_id=user_id).first()
    if not spending:
        return jsonify({'error': 'Spending not found or unauthorized'}), 404

    # Validate frequency
    valid_frequencies = ['daily', 'weekly', 'monthly', 'yearly']
    if data['frequency'] not in valid_frequencies:
        return jsonify({'error': f"Invalid frequency. Choose from {valid_frequencies}"}), 400

    # Create the recurring spending
    try:
        next_occurrence = datetime.strptime(data['next_occurrence'], '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return jsonify({'error': 'Invalid date format for next_occurrence'}), 400

    recurring = RecurringSpending(
        spending_id=spending.id,
        frequency=data['frequency'],
        next_occurrence=next_occurrence
    )
    db.session.add(recurring)
    db.session.commit()

    return jsonify({'message': 'Recurring spending added successfully', 'recurring_id': recurring.id}), 201

@recurring_bp.route('/', methods=['GET'])
@jwt_required()
def get_recurring_spendings():
    """
    Fetches all recurring spendings for the authenticated user.
    """
    user_id = get_jwt_identity()

    # Retrieve recurring spendings linked to the user
    recurring_spendings = db.session.query(RecurringSpending).join(Spending).filter(
        Spending.user_id == user_id
    ).all()

    return jsonify([{
        'id': r.id,
        'spending_id': r.spending_id,
        'frequency': r.frequency,
        'next_occurrence': r.next_occurrence.strftime('%Y-%m-%dT%H:%M:%S'),
    } for r in recurring_spendings]), 200

@recurring_bp.route('/<int:recurring_id>', methods=['DELETE'])
@jwt_required()
def delete_recurring_spending(recurring_id):
    """
    Deletes a specific recurring spending for the authenticated user.
    """
    user_id = get_jwt_identity()

    # Retrieve the recurring spending and ensure it belongs to the user
    recurring = db.session.query(RecurringSpending).join(Spending).filter(
        RecurringSpending.id == recurring_id,
        Spending.user_id == user_id
    ).first()

    if not recurring:
        return jsonify({'error': 'Recurring spending not found or unauthorized'}), 404

    db.session.delete(recurring)
    db.session.commit()
    return jsonify({'message': 'Recurring spending deleted successfully'}), 200
