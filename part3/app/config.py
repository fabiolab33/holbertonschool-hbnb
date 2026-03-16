"""
Configuration settings for the HBnB application.
Supports different environments: development, testing, production.
"""
import os
from datetime import timedelta

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config:
    """Base configuration class with common settings."""
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    # SQLAlchemy Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development environment configuration."""
    
    DEBUG = True
    # ABSOLUTE PATH for SQLite database
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'development.db')}"

class TestingConfig(Config):
    """Testing environment configuration."""
    
    TESTING = True
    # In-memory database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)


class ProductionConfig(Config):
    """Production environment configuration."""
    
     # MySQL/PostgreSQL connection string
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://username:password@localhost/hbnb_prod'
    
    # Longer token expiration in production    
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config(config_name='development'):
    """
    Get configuration class by name.
    
    Args:
        config_name: Name of configuration ('development', 'testing', 'production')
        
    Returns:
        Configuration class
    """
    return config.get(config_name, DevelopmentConfig)
