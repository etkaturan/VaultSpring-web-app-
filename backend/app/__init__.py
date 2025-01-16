from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()  # Add Flask-Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    print(f"JWT_SECRET_KEY: {app.config['JWT_SECRET_KEY']}")


    jwt = JWTManager()

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

    # Import and register blueprints
    from app.routes.user_routes import user_blueprint
    app.register_blueprint(user_blueprint)
    from app.routes.balance_routes import balance_blueprint
    app.register_blueprint(balance_blueprint)  # Register balance routes
    
    # Spendings Block
    from app.routes.spending.spending_routes import spending_bp
    from app.routes.spending.recurring_routes import recurring_bp
    from app.routes.spending.category_routes import category_bp

    app.register_blueprint(spending_bp)
    app.register_blueprint(recurring_bp)
    app.register_blueprint(category_bp)



    return app
