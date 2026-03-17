# HBnB Evolution - Part 3: Authentication & Database Integration

Complete implementation of authentication, authorization, and database persistence for the HBnB application.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Database](#database)
- [API Documentation](#api-documentation)
- [Architecture](#architecture)
- [Tasks Completed](#tasks-completed)

---

## 🎯 Overview

Part 3 extends the HBnB application with:
- **JWT Authentication** for secure user sessions
- **Role-Based Access Control** (Admin/Regular users)
- **SQLAlchemy ORM** for database persistence
- **Complete API** with protected endpoints
- **SQL Scripts** for database setup
- **ER Diagrams** for schema visualization

---

## ✨ Features

### Authentication & Security
- ✅ Password hashing with Bcrypt
- ✅ JWT token-based authentication
- ✅ Protected API endpoints
- ✅ Admin-only operations
- ✅ Ownership validation

### Database
- ✅ SQLAlchemy ORM models
- ✅ Switchable repositories (InMemory/SQLAlchemy)
- ✅ Foreign key relationships
- ✅ Cascade delete operations
- ✅ Database indexes for performance

### API Endpoints
- ✅ User management (CRUD)
- ✅ Place listings (CRUD)
- ✅ Reviews system (CRUD)
- ✅ Amenities catalog (Admin only)
- ✅ Authentication (Login)
- ✅ Swagger documentation

---

## 📁 Project Structure
```
part3/
├── app/
│   ├── __init__.py              # Application factory
│   ├── config.py                # Multi-environment configuration
│   ├── api/                     # API endpoints
│   │   ├── auth.py              # Authentication (login)
│   │   ├── users.py             # User CRUD
│   │   ├── places.py            # Place CRUD
│   │   ├── reviews.py           # Review CRUD
│   │   └── amenities.py         # Amenity CRUD (admin only)
│   ├── business/                # Business logic
│   │   ├── user.py              # User model
│   │   ├── place.py             # Place model
│   │   ├── review.py            # Review model
│   │   ├── amenity.py           # Amenity model
│   │   └── facade.py            # Facade pattern
│   ├── models/                  # SQLAlchemy models
│   │   ├── base.py              # Base model
│   │   ├── user.py              # User ORM
│   │   ├── place.py             # Place ORM
│   │   ├── review.py            # Review ORM
│   │   ├── amenity.py           # Amenity ORM
│   │   └── place_amenity.py     # Many-to-many table
│   └── persistence/             # Repository layer
│       ├── memory_repository.py
│       └── sqlalchemy_repository.py
├── diagrams/                    # Database diagrams
│   ├── database_schema.md       # Complete ER diagram
│   ├── simple_schema.md         # Simplified view
│   ├── class_diagram.md         # SQLAlchemy classes
│   └── architecture.md          # System architecture
├── sql_scripts/                 # Database scripts
│   ├── schema.sql               # Table definitions
│   ├── seed.sql                 # Initial data
│   ├── queries.sql              # Verification queries
│   └── setup.sh                 # Automated setup
├── instance/
│   └── development.db           # SQLite database
├── .env                         # Environment variables
├── run.py                       # Application entry point
└── requirements.txt             # Python dependencies
```

---

## 🗄️ Database

### Schema Overview

The database consists of 5 tables:

1. **users** - User accounts
2. **places** - Property listings
3. **reviews** - User reviews
4. **amenities** - Available amenities
5. **place_amenity** - Many-to-many relationship

### Relationships

- **Users → Places** (One-to-Many): A user can own multiple places
- **Users → Reviews** (One-to-Many): A user can write multiple reviews
- **Places → Reviews** (One-to-Many): A place can have multiple reviews
- **Places ↔ Amenities** (Many-to-Many): Places can have multiple amenities

### Database Setup

#### Quick Setup (Automated)
```bash
cd sql_scripts
./setup.sh
```

#### Manual Setup
```bash
# Create schema
sqlite3 instance/development.db < sql_scripts/schema.sql

# Insert initial data
sqlite3 instance/development.db < sql_scripts/seed.sql

# Verify
sqlite3 instance/development.db < sql_scripts/queries.sql
```

### Initial Data

**Administrator Account:**
- Email: `admin@hbnb.com`
- Password: `AdminPass123`
- Role: Admin

**Sample Users:**
- `john@example.com` (Password: AdminPass123)
- `jane@example.com` (Password: AdminPass123)

**Amenities:** 10 common amenities (WiFi, AC, Pool, etc.)

**Sample Data:** 3 places, 3 reviews, multiple amenity associations

### Database Diagrams

View ER diagrams in the `diagrams/` directory:

- **database_schema.md** - Complete ER diagram with all attributes
- **simple_schema.md** - Simplified view
- **class_diagram.md** - SQLAlchemy class relationships
- **architecture.md** - System architecture

To view diagrams:
- Open any `.md` file on GitHub (renders automatically)

---

## 📚 API Documentation

### Authentication

#### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

Response: { "access_token": "jwt_token_here" }
```

### Protected Endpoints

All endpoints except `/api/users/` (POST) and `/api/auth/login` require JWT authentication.

**Include token in requests:**
```bash
Authorization: Bearer <your_jwt_token>
```

### API Examples

#### Create User (Public)
```bash
curl -X POST http://localhost:5001/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

#### Create Place (Protected)
```bash
curl -X POST http://localhost:5001/api/places/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Cozy Apartment",
    "description": "Perfect location",
    "price": 100.0,
    "latitude": 40.7128,
    "longitude": -74.0060
  }'
```

#### Create Amenity (Admin Only)
```bash
curl -X POST http://localhost:5001/api/amenities/ \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "WiFi",
    "description": "High-speed internet"
  }'
```

### Swagger Documentation

Interactive API documentation available at:
```
http://localhost:5001/api/docs
```

---

## 🏗️ Architecture

### Design Patterns

- **Application Factory**: Multi-environment configuration
- **Repository Pattern**: Abstraction over data access
- **Facade Pattern**: Simplified business logic interface

### Layers

1. **API Layer** (Flask-RESTX)
   - RESTful endpoints
   - Request validation
   - Response formatting

2. **Business Logic Layer** (Facade)
   - Business rules
   - Validation
   - Orchestration

3. **Repository Layer**
   - Data access abstraction
   - Switchable implementations (InMemory/SQLAlchemy)

4. **Persistence Layer**
   - SQLAlchemy ORM
   - Database operations

### Repository Switch

The application can use either InMemory or SQLAlchemy repositories:
```python
# In .env
USE_DATABASE=true   # Use SQLAlchemy
USE_DATABASE=false  # Use InMemory (testing)
```

---

## ✅ Tasks Completed

### Task 0: Application Factory
- ✅ Multi-environment configuration (Development, Testing, Production)
- ✅ Environment-based settings
- ✅ JWT configuration

### Task 1: Password Hashing
- ✅ Bcrypt password hashing
- ✅ Secure password storage
- ✅ Password verification

### Task 2: JWT Authentication
- ✅ Token generation
- ✅ Token validation
- ✅ Claims (user_id, is_admin)

### Task 3: Authenticated User Access
- ✅ Protected endpoints
- ✅ Ownership validation
- ✅ CRUD operations with authentication

### Task 4: Administrator Access
- ✅ Admin-only endpoints
- ✅ Admin bypass for ownership checks
- ✅ Role-based access control

### Task 5: SQLAlchemy Repository
- ✅ Repository implementation
- ✅ Switchable repositories
- ✅ CRUD operations

### Task 6: Map User Entity
- ✅ User SQLAlchemy model
- ✅ Password hashing integration
- ✅ Email validation

### Task 7: Map Entities
- ✅ Place SQLAlchemy model
- ✅ Review SQLAlchemy model
- ✅ Amenity SQLAlchemy model

### Task 8: Map Relationships
- ✅ One-to-Many relationships
- ✅ Many-to-Many relationships
- ✅ Foreign keys and constraints
- ✅ Cascade delete operations

### Task 9: SQL Scripts
- ✅ Schema creation script
- ✅ Data seeding script
- ✅ Verification queries
- ✅ Automated setup script

### Task 10: Database Diagrams
- ✅ Complete ER diagram
- ✅ Simplified diagram
- ✅ Class diagram
- ✅ Architecture diagram

---

## 🔒 Security Features

- **Password Hashing**: Bcrypt with salt
- **JWT Tokens**: Secure token-based authentication
- **Token Expiration**: Configurable token lifetime
- **Role-Based Access**: Admin and regular user roles
- **Ownership Validation**: Users can only modify their own data
- **Admin Bypass**: Admins can manage all resources

---

## 🧪 Testing

### Manual Testing
```bash
# Test user creation
curl -X POST http://localhost:5001/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Test","last_name":"User","email":"test@test.com","password":"Test123"}'

# Test login
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123"}'

# Use token for protected endpoints
TOKEN="<your_token_here>"
curl -X GET http://localhost:5001/api/users/ \
  -H "Authorization: Bearer $TOKEN"
```

### Database Verification
```bash
# Run verification queries
sqlite3 instance/development.db < sql_scripts/queries.sql

# Check database manually
sqlite3 instance/development.db
.tables
.schema users
SELECT * FROM users;
.quit
```

---

## 📝 Environment Variables
```bash
# .env
FLASK_ENV=development          # development, testing, production
SECRET_KEY=<secret-key>        # Flask secret key
JWT_SECRET_KEY=<jwt-key>       # JWT signing key
USE_DATABASE=true              # true=SQLAlchemy, false=InMemory
```

---
