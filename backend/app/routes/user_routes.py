from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user_model import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

user_blueprint = Blueprint('user_routes', __name__, url_prefix='/users')

# User Registration
@user_blueprint.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email is already registered"}), 400

    user = User(username=username, email=email)
    user.set_password(password)  # Hash the password using the model method
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


# User Login
@user_blueprint.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Generate a valid token
    token = create_access_token(identity=user.id)
    return jsonify({
        "access_token": token,
        "username": user.username
    }), 200


# Get Current User
@user_blueprint.route('/me', methods=['GET'])
@jwt_required()
def get_user_data():
    try:
        # Decode user ID from JWT token
        user_id = get_jwt_identity()
        print(f"Decoded user_id: {user_id}")  # Debug log
        user = User.query.get(user_id)

        if not user:
            print(f"User with ID {user_id} not found.")  # Debug log
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email
        }), 200

    except Exception as e:
        print(f"Error in /users/me: {e}")  # Debugging error
        return jsonify({"error": "Invalid token or request"}), 422
