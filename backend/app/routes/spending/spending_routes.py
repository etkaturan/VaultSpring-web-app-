import requests
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.spending.spending import Spending
from datetime import datetime
from sqlalchemy import func
from app.models.spending.category import Category

spending_bp = Blueprint('spending', __name__, url_prefix='/api/spendings')
EXCHANGE_API_URL = "https://open.er-api.com/v6/latest/USD"



def get_or_create_category(name, parent_id=None):
    """
    Helper function to get an existing category or create a new one.
    """
    category = Category.query.filter_by(name=name, parent_id=parent_id).first()
    if not category:
        category = Category(name=name, parent_id=parent_id)
        db.session.add(category)
        db.session.commit()
    return category

@spending_bp.route('/', methods=['POST'])
@jwt_required()
def add_spending():
    try:
        user_id = get_jwt_identity()  # Extract the logged-in user's ID

        # Parse request data
        data = request.json

        # Validate required fields
        category_id = data.get('category_id')
        if not category_id:
            return jsonify({"error": "'category_id' field is required"}), 400

        amount = data.get('amount')
        if amount is None or not isinstance(amount, (int, float)):
            return jsonify({"error": "'amount' field must be a number"}), 400

        # Fetch category
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404

        # Create a new spending entry
        spending = Spending(
            user_id=user_id,  # Use the logged-in user's ID
            category_id=category.id,
            amount=amount,
            currency=data.get('currency', 'USD'),
            description=data.get('description'),
            date=datetime.strptime(
                data.get('date', datetime.utcnow().strftime('%Y-%m-%d')), '%Y-%m-%d'
            ),
            payment_method=data.get('payment_method', 'Card'),
        )
        db.session.add(spending)
        db.session.commit()

        return jsonify({'message': 'Spending added successfully', 'spending_id': spending.id}), 201

    except Exception as e:
        print(f"Error in add_spending: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

@spending_bp.route('/', methods=['GET'])
@jwt_required()
def get_spendings():
    user_id = get_jwt_identity()
    spendings = Spending.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': s.id,
        'user_id': s.user_id,
        'category': Category.query.get(s.category_id).name if s.category_id else "Unknown",
        'amount': s.amount,
        'currency': s.currency,
        'description': s.description,
        'date': s.date.strftime('%Y-%m-%d'),
        'payment_method': s.payment_method,
    } for s in spendings]), 200

# 
# Analytics
# 

def get_exchange_rates():
    """
    Fetches exchange rates from the API.
    """
    try:
        response = requests.get(EXCHANGE_API_URL)
        response.raise_for_status()
        return response.json().get("rates", {})
    except Exception as e:
        print(f"Error fetching exchange rates: {e}")
        return {}

def calculate_total_spendings(parent_category_id, user_id, start_date, end_date, exchange_rates, base_currency="USD"):
    """
    Calculates total spendings for a category, including subcategories, in the base currency.
    """
    def get_all_subcategories(category_id):
        subcategories = Category.query.filter_by(parent_id=category_id).all()
        result = [category_id]
        for subcategory in subcategories:
            result.extend(get_all_subcategories(subcategory.id))
        return result

    category_ids = get_all_subcategories(parent_category_id)
    print(f"Category IDs for parent {parent_category_id}: {category_ids}")

    # Query spendings with date filter
    spendings = db.session.query(
        Spending.amount, Spending.currency
    ).filter(
        Spending.category_id.in_(category_ids),
        Spending.user_id == user_id,
        func.date(Spending.date).between(start_date, end_date)  # Extract date part
    ).all()
    print(f"Spendings for category {parent_category_id}, user {user_id}: {spendings}")

    total = 0.0
    for amount, currency in spendings:
        rate = exchange_rates.get(currency, 1.0)
        total += amount / rate if currency != base_currency else amount

    print(f"Total spent for category {parent_category_id}: {total}")
    return total


@spending_bp.route('/analytics/', methods=['GET'])
@jwt_required()
def get_spendings_analytics():
    user_id = get_jwt_identity()
    start_date = request.args.get('start_date', '2000-01-01')
    end_date = request.args.get('end_date', datetime.utcnow().strftime('%Y-%m-%d'))
    base_currency = request.args.get('base_currency', 'USD')

    try:
        # Convert start_date and end_date to datetime
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    # Fetch exchange rates
    exchange_rates = get_exchange_rates()

    # Get all parent categories
    parent_categories = Category.query.filter_by(parent_id=None).all()

    # Calculate total spendings for each parent category
    analytics = []
    for category in parent_categories:
        total_spent = calculate_total_spendings(
            parent_category_id=category.id,
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            exchange_rates=exchange_rates,
            base_currency=base_currency
        )
        analytics.append({
            'category': category.name,
            'total_spent': round(total_spent, 2),
            'currency': base_currency
        })

    return jsonify(analytics)
