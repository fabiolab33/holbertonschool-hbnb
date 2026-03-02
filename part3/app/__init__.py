# app/__init__.py
from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_name=None):
    """Creates and configures the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    from app.config import get_config
    config_class = get_config(config_name)
    app.config.from_object(config_class)

    print(f"Loading configuration: {config_class.__name__}")

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Initialize API
    api = Api(
        app,
        version='1.0',
        title='HBnB Evolution API',
        description='RESTful API for HBnB application with authentication',
        doc='/api/docs'
    )

    # Import namespaces
    from app.api.users import api as users_ns
    from app.api.places import api as places_ns
    from app.api.reviews import api as reviews_ns
    from app.api.amenities import api as amenities_ns

    # Register namespaces
    api.add_namespace(users_ns, path='/api/users')
    api.add_namespace(places_ns, path='/api/places')
    api.add_namespace(reviews_ns, path='/api/reviews')
    api.add_namespace(amenities_ns, path='/api/amenities')
    
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

# Import facade after app initialization to avoid circular imports
from app.business.facade import facade