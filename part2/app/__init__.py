# app/__init__.py
from flask import Flask
from flask_restx import Api

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Initialize API with Flask-RESTX
    api = Api(
        app,
        version="1.0",
        title="HBnB Evolution API",
        description="A simple AirBnB clone RESTful API",
        doc='/api/docs'
    )

    # Import and initialize facade
    from app.business.facade import HBnBFacade
    global facade
    facade = HBnBFacade()

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

    return app

# Global facade instance
facade = None