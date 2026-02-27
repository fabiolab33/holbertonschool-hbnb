"""
Flask Application Factory for HBnB Evolution API.
Supports different configurations for development, testing, and production.
"""
from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions (without app binding)
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_name=None):
    """
    Application Factory pattern.
    Creates and configures the Flask application.
    
    Args:
        config_name: Configuration to use ('development', 'testing', 'production')
                    If None, uses FLASK_ENV environment variable
    
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    from app.config import get_config
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    # Print current configuration (for debugging)
    print(f"Loading configuration: {config_class.__name__}")
    print(f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')}")
    
    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Initialize Flask-RESTX API
    api = Api(
        app,
        version='1.0',
        title='HBnB Evolution API',
        description='RESTful API for HBnB application with authentication',
        doc='/api/docs'
    )
    
    # Register API namespaces
    # Import here to avoid circular imports
    from app.api.users import api as users_ns
    from app.api.places import api as places_ns
    from app.api.reviews import api as reviews_ns
    from app.api.amenities import api as amenities_ns
    
    api.add_namespace(users_ns, path='/api/users')
    api.add_namespace(places_ns, path='/api/places')
    api.add_namespace(reviews_ns, path='/api/reviews')
    api.add_namespace(amenities_ns, path='/api/amenities')
    
    # Create database tables (for development/testing)
    with app.app_context():
        # Only create tables in development and testing
        if app.config['TESTING'] or app.config['DEBUG']:
            db.create_all()
            print("Database tables created successfully")
    
    # Register error handlers
    register_error_handlers(app)
    
    return app


def register_error_handlers(app):
    """Register custom error handlers."""
    
    @app.errorhandler(404)
    def not_found(error):
        return {'message': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'message': 'Internal server error'}, 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return {'message': 'Bad request'}, 400


facade = None
