import requests
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.balance_model import Balance
from app import db

balance_blueprint = Blueprint('balance_routes', __name__, url_prefix='/balances')

# API for exchange rates
EXCHANGE_API_URL = "https://open.er-api.com/v6/latest/USD"

def fetch_exchange_rates():
    """Fetch exchange rates from the API."""
    try:
        response = requests.get(EXCHANGE_API_URL)
        response.raise_for_status()  # Raise error for bad HTTP responses
        data = response.json()

        if data["result"] == "success":
            return data["rates"]
        else:
            print("API error:", data.get("error-type"))
            return None
    except Exception as e:
        print(f"Error fetching exchange rates: {e}")
        return None

# Add a new balance
@balance_blueprint.route('/add', methods=['POST'])
@jwt_required()
def add_account():
    user_id = get_jwt_identity()
    data = request.get_json()

    account_type = data.get("account_type")
    balance = data.get("balance", 0.0)
    currency = data.get("currency", "USD")

    if not account_type:
        return jsonify({"error": "Account type is required"}), 400

    new_account = Balance(
        user_id=user_id,
        account_type=account_type,
        balance=balance,
        currency=currency
    )
    db.session.add(new_account)
    db.session.commit()

    return jsonify({"message": "Account added successfully"}), 201

# Fetch all accounts and convert balances
@balance_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_accounts():
    user_id = get_jwt_identity()
    accounts = Balance.query.filter_by(user_id=user_id).all()
    exchange_rates = fetch_exchange_rates()

    if not exchange_rates:
        return jsonify({"error": "Failed to fetch exchange rates"}), 500

    result = []
    for account in accounts:
        converted_balances = {}
        for currency in ["USD", "EUR", "KZT"]:  # Add more currencies as needed
            if account.currency == currency:
                converted_balances[currency] = account.balance
            else:
                try:
                    converted_balances[currency] = round(
                        (account.balance / exchange_rates[account.currency]) * exchange_rates[currency], 2
                    )
                except KeyError:
                    converted_balances[currency] = "N/A"  # Handle missing rates

        result.append({
            "id": account.id,
            "account_type": account.account_type,
            "balance": account.balance,
            "currency": account.currency,
            "converted_balances": converted_balances,
        })

    return jsonify(result), 200

# Update balance account
@balance_blueprint.route('/<int:account_id>', methods=['PUT'])
@jwt_required()
def update_account(account_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    account = Balance.query.filter_by(id=account_id, user_id=user_id).first()

    if not account:
        return jsonify({"error": "Account not found"}), 404

    account.account_type = data.get("account_type", account.account_type)
    account.balance = data.get("balance", account.balance)
    account.currency = data.get("currency", account.currency)

    db.session.commit()
    return jsonify({"message": "Account updated successfully"}), 200

# Delete balance account
@balance_blueprint.route('/<int:account_id>', methods=['DELETE'])
@jwt_required()
def delete_account(account_id):
    user_id = get_jwt_identity()

    account = Balance.query.filter_by(id=account_id, user_id=user_id).first()

    if not account:
        return jsonify({"error": "Account not found"}), 404

    db.session.delete(account)
    db.session.commit()

    return jsonify({"message": "Account deleted successfully"}), 200
