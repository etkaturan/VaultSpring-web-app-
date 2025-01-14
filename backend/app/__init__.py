from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()  # Add Flask-Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.config['JWT_SECRET_KEY'] = 'super_jwt_secret'

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

    # Import and register blueprints
    from app.routes.user_routes import user_blueprint
    app.register_blueprint(user_blueprint)
    from app.routes.balance_routes import balance_blueprint
    app.register_blueprint(balance_blueprint)  # Register balance routes


    return app
