from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.balance_model import Balance
from app import db

# Define the blueprint
balance_blueprint = Blueprint('balance_routes', __name__, url_prefix='/balances')

# Route to add a new balance account
@balance_blueprint.route('/add', methods=['POST'])
@jwt_required()
def add_account():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        # Extract account details
        account_type = data.get('account_type')
        balance = data.get('balance', 0.0)

        # Validate inputs
        if not account_type:
            return jsonify({"error": "Account type is required"}), 400

        # Create a new balance account
        new_account = Balance(user_id=user_id, account_type=account_type, balance=balance)
        db.session.add(new_account)
        db.session.commit()

        return jsonify({"message": "Account added successfully"}), 201
    except Exception as e:
        print(f"Error in add_account: {e}")
        return jsonify({"error": "Failed to add account"}), 500

# Route to fetch all accounts for the logged-in user
@balance_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_accounts():
    try:
        # Debug: Log the Authorization header
        print(f"Authorization Header: {request.headers.get('Authorization')}")

        # Decode the user ID from the token
        user_id = get_jwt_identity()
        print(f"User ID from Token: {user_id}")

        # Fetch user accounts
        accounts = Balance.query.filter_by(user_id=user_id).all()

        return jsonify([
            {
                "id": account.id,
                "account_type": account.account_type,
                "balance": account.balance
            } for account in accounts
        ]), 200
    except Exception as e:
        print(f"Error in get_accounts: {e}")
        return jsonify({"error": "Failed to fetch accounts"}), 500


