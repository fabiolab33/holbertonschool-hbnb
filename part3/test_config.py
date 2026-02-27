"""
Test script to verify configuration loading.
"""
import os
from app import create_app

def test_configurations():
    """Test different configuration loads."""
    
    print("\n" + "="*60)
    print("TESTING CONFIGURATION SYSTEM")
    print("="*60 + "\n")
    
    print("1. Testing Development Configuration...")
    app = create_app('development')
    with app.app_context():
        assert app.config['DEBUG'] == True
        assert app.config['TESTING'] == False
        assert 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']
        print("   ✓ Development config loaded successfully")
        print(f"   Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    print("\n2. Testing Testing Configuration...")
    app = create_app('testing')
    with app.app_context():
        assert app.config['DEBUG'] == False
        assert app.config['TESTING'] == True
        assert ':memory:' in app.config['SQLALCHEMY_DATABASE_URI']
        print("   ✓ Testing config loaded successfully")
        print(f"   Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    print("\n3. Testing Production Configuration...")
    os.environ['SECRET_KEY'] = 'test-production-key'
    os.environ['DATABASE_URL'] = 'mysql+pymysql://user:pass@localhost/test_db'
    app = create_app('production')
    with app.app_context():
        assert app.config['DEBUG'] == False
        assert app.config['TESTING'] == False
        assert 'mysql' in app.config['SQLALCHEMY_DATABASE_URI']
        print("   ✓ Production config loaded successfully")
        print(f"   Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    del os.environ['SECRET_KEY']
    del os.environ['DATABASE_URL']
    
    print("\n" + "="*60)
    print("✓ ALL CONFIGURATION TESTS PASSED")
    print("="*60 + "\n")

if __name__ == '__main__':
    test_configurations()
