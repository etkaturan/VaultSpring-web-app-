import requests
from flask import Blueprint, request, jsonify
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
def add_spending():
    data = request.json

    # Handle category creation
    category_name = data['category']
    subcategory_name = data.get('subcategory', None)
    parent_category = get_or_create_category(category_name)
    category = parent_category

    # If a subcategory is provided, create or get it
    if subcategory_name:
        category = get_or_create_category(subcategory_name, parent_id=parent_category.id)

    # Create a new spending entry
    spending = Spending(
        user_id=data['user_id'],
        category_id=category.id,
        amount=data['amount'],
        currency=data.get('currency', 'USD'),
        description=data.get('description'),
        date=data.get('date', datetime.utcnow()),
        payment_method=data['payment_method'],
        account_id=data['account_id']
    )
    db.session.add(spending)
    db.session.commit()

    return jsonify({'message': 'Spending added successfully', 'spending_id': spending.id}), 201

@spending_bp.route('/', methods=['GET'])
def get_spendings():
    spendings = Spending.query.all()
    return jsonify([{
        'id': s.id,
        'user_id': s.user_id,
        'category': s.category_id,
        'amount': s.amount,
        'currency' : s.currency,
        'description': s.description,
        'date': s.date,
        'payment_method': s.payment_method,
        'account_id': s.account_id
    } for s in spendings]), 200


# 
# Analytics
# 
def get_exchange_rates():
    """
    Fetches exchange rates from the API.
    """
    response = requests.get(EXCHANGE_API_URL)
    if response.status_code == 200:
        return response.json().get("rates", {})
    return {}

def calculate_total_spendings(parent_category_id, exchange_rates, base_currency="USD"):
    """
    Calculates total spendings for a category, including subcategories, in the base currency.
    """
    # Get all subcategories of the parent category
    def get_all_subcategories(category_id):
        subcategories = Category.query.filter_by(parent_id=category_id).all()
        result = [category_id]
        for subcategory in subcategories:
            result.extend(get_all_subcategories(subcategory.id))
        return result

    category_ids = get_all_subcategories(parent_category_id)

    # Query spendings for these categories
    spendings = db.session.query(
        Spending.amount, Spending.currency
    ).filter(Spending.category_id.in_(category_ids)).all()

    # Convert amounts to base currency
    total = 0.0
    for amount, currency in spendings:
        rate = exchange_rates.get(currency, 1.0)  # Default to 1.0 if rate not found
        total += amount / rate if currency != base_currency else amount

    return total

@spending_bp.route('/analytics', methods=['GET'])
def get_spendings_analytics():
    start_date = request.args.get('start_date', '2000-01-01')
    end_date = request.args.get('end_date', datetime.utcnow().strftime('%Y-%m-%d'))
    base_currency = request.args.get('base_currency', 'USD')

    # Fetch exchange rates
    exchange_rates = get_exchange_rates()

    # Get all parent categories
    parent_categories = Category.query.filter_by(parent_id=None).all()

    # Calculate total spendings for each parent category
    analytics = []
    for category in parent_categories:
        total_spent = calculate_total_spendings(category.id, exchange_rates, base_currency)
        analytics.append({
            'category': category.name,
            'total_spent': round(total_spent, 2),
            'currency': base_currency
        })

    return jsonify(analytics)