# app/__init__.py
from flask import Flask
from flask_restx import Api

# Imports namespaces from API modules
from app.api.users import api as users_ns
from app.api.places import api as places_ns
from app.api.reviews import api as reviews_ns
from app.api.amenities import api as amenities_ns

# Initialize the Facade
from app.business.facade import HBnBFacade
facade = HBnBFacade()

def create_app():
    app = Flask(__name__)
    api = Api(app, version="1.0", title="HBnB Evolution API",
              description="A simple AirBnB clone API")

    # Register namespaces
    api.add_namespace(users_ns, path="/users")
    api.add_namespace(places_ns, path="/places")
    api.add_namespace(reviews_ns, path="/reviews")
    api.add_namespace(amenities_ns, path="/amenities")

    # Save the facade in the app so that it can be used in the endpoints
    app.facade = facade

    return app
