# HBnB Evolution API - Part 2: Complete Implementation Guide

## Project Overview

**Part 2** of the HBnB Evolution project focuses on implementing the **Business Logic** and **Presentation layers** of a RESTful API for an Airbnb-like application. This phase builds the foundation of the application using Flask and Flask-RESTX, implementing core CRUD operations, validations, and the Facade design pattern.

**Architecture:**
- Presentation Layer (API endpoints)
- Business Logic Layer (entities and validations)
- Persistence Layer (in-memory repository)

---

##  Project Structure
```
part2/
│
├── app/
│   ├── __init__.py                 # Flask app factory
│   │
│   ├── api/                        # Presentation Layer
│   │   ├── __init__.py
│   │   ├── users.py               # User endpoints
│   │   ├── places.py              # Place endpoints (extended serialization)
│   │   ├── reviews.py             # Review endpoints (with DELETE)
│   │   └── amenities.py           # Amenity endpoints
│   │
│   ├── business/                   # Business Logic Layer
│   │   ├── __init__.py
│   │   ├── base_model.py          # Base entity (UUID, timestamps)
│   │   ├── user.py                # User entity (email validation)
│   │   ├── place.py               # Place entity (coordinate validation)
│   │   ├── review.py              # Review entity (rating validation)
│   │   ├── amenity.py             # Amenity entity
│   │   └── facade.py              # Facade pattern implementation
│   │
│   └── persistence/                # Persistence Layer
│       ├── __init__.py
│       └── memory_repository.py    # In-memory CRUD operations
│
├── tests/                          # Testing
│   ├── __init__.py
│   └── test_models.py              # 52 unit tests
│
├── venv/                           # Virtual environment
├── run.py                          # Application entry point
├── run_all_tests.sh                # Test automation script
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation
```bash
# 1. Navigate to project directory
cd part2

# 2. Create virtual environment (if not exists)
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Start the Flask development server
python3 run.py
```

The API will be available at: `http://localhost:5001`

**Access Swagger Documentation:** `http://localhost:5001/api/docs`

---

## Task Overview

### Task 0: Project Setup and Package Initialization

**Objective:** Establish the initial project structure with proper separation of concerns.

**What Was Implemented:**
- Three-layer architecture (Presentation, Business Logic, Persistence)
- Flask application factory pattern
- In-memory repository implementation
- Facade pattern structure

**Key Files:**
- `app/__init__.py` - Flask app initialization
- `app/persistence/memory_repository.py` - CRUD operations
- `app/business/facade.py` - Business logic coordinator

---

### Task 1: Core Business Logic Classes

**Objective:** Implement fundamental entity models with validations and relationships.

**Entities Implemented:**

#### BaseModel
- Auto-generated UUID
- Timestamps (created_at, updated_at)
- save() and to_dict() methods

#### User
```python
Attributes:
- first_name, last_name
- email (validated with regex)
- password (not returned in API responses)
- is_admin
- places[], reviews[]

Validations:
- Email format: ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
- Email uniqueness
```

#### Place
```python
Attributes:
- title, description
- price (validated >= 0)
- latitude (validated -90 to 90)
- longitude (validated -180 to 180)
- owner_id
- reviews[], amenities[]

Validations:
- Price must be positive
- Coordinates within valid ranges
- Owner must exist
```

#### Review
```python
Attributes:
- rating (validated 1-5)
- comment (validated not empty)
- user_id, place_id

Validations:
- Rating must be integer 1-5
- Comment cannot be empty/whitespace
- User cannot review their own place
```

#### Amenity
```python
Attributes:
- name (validated)
- description

Validations:
- Name cannot be empty
```

**Relationships:**
```
User (1) ──────< (N) Place
User (1) ──────< (N) Review
Place (1) ─────< (N) Review
Place (N) ─────< (N) Amenity
```

---

### Task 2: User Endpoints

**Objective:** Implement CRUD operations for User management (excluding DELETE).

**Endpoints:**
```http
POST   /api/users              Create user (201)
GET    /api/users              List all users (200)
GET    /api/users/{id}         Get user by ID (200/404)
PUT    /api/users/{id}         Update user (200/404)
```

**Security Features:**
- Password never returned in responses
- Email uniqueness enforced
- Email format validated

---

### Task 3: Amenity Endpoints

**Objective:** Implement CRUD operations for Amenity management (excluding DELETE).

**Endpoints:**
```http
POST   /api/amenities          Create amenity (201)
GET    /api/amenities          List all amenities (200)
GET    /api/amenities/{id}     Get amenity by ID (200/404)
PUT    /api/amenities/{id}     Update amenity (200/404)
```

---

### Task 4: Place Endpoints

**Objective:** Implement CRUD with relationship handling and extended serialization.

**Endpoints:**
```http
POST   /api/places             Create place (201)
GET    /api/places             List all places (200)
GET    /api/places/{id}        Get place with extended attributes (200/404)
PUT    /api/places/{id}        Update place (200/404)
```

**Extended Serialization:**
When retrieving a Place, the API includes:
- Owner's complete information (first_name, last_name, email)
- List of amenities with details
- List of reviews with details

**Example Response:**
```json
{
  "id": "place-uuid",
  "title": "Cozy Apartment",
  "price": 120.50,
  "owner": {
    "id": "user-uuid",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com"
  },
  "amenities": [
    {"id": "amenity-uuid", "name": "WiFi"}
  ],
  "reviews": [
    {"id": "review-uuid", "rating": 5, "comment": "Great!"}
  ]
}
```

---

### Task 5: Review Endpoints

**Objective:** Implement full CRUD including DELETE (only entity with DELETE in Part 2).

**Endpoints:**
```http
POST   /api/reviews                              Create review (201)
GET    /api/reviews                              List all reviews (200)
GET    /api/reviews/{id}                         Get review (200/404)
PUT    /api/reviews/{id}                         Update review (200/404)
DELETE /api/reviews/{id}                         Delete review (204/404) 
GET    /api/reviews/places/{place_id}/reviews    Get place reviews (200/404)
```

**DELETE Operation:**
When a review is deleted:
1. Removed from review repository
2. Removed from user.reviews[] list
3. Removed from place.reviews[] list
4. Returns HTTP 204 No Content

**Business Rules:**
- User cannot review their own place
- Rating must be 1-5 (integer)
- Comment cannot be empty

---

### Task 6: Testing and Validation

**Objective:** Comprehensive testing with automated and manual approaches.

**What Was Implemented:**

#### Unit Tests (pytest)
- 52 automated tests across 5 test classes
- 96% code coverage
- Tests for all validations and edge cases

**Test Classes:**
```
TestUserModel (8 tests)
TestPlaceModel (17 tests)
TestReviewModel (15 tests)
TestAmenityModel (8 tests)
TestBaseModel (4 tests)
```

**Run Unit Tests:**
```bash
pytest tests/test_models.py -v

# With coverage
pytest tests/test_models.py --cov=app/business --cov-report=html
```

#### Integration Tests
- 30 automated API tests with cURL
- Tests all endpoints
- Validates request/response flow

**Run Integration Tests:**
```bash
python3 test_api.py
```

#### Run All Tests
```bash
./run_all_tests.sh
```

**Expected Output:**
```
============================================
HBnB API - Complete Test Suite
============================================

 Server is running on port 5001

============================================
PART 1: Unit Tests (pytest)
============================================
==================== 52 passed in 0.5s ====================
 All unit tests passed!

============================================
PART 2: Integration Tests (API with cURL)
============================================
 All integration tests passed!

============================================
 ALL TESTS PASSED!
============================================
```

---

## API Documentation

### Accessing Swagger UI

**URL:** `http://localhost:5001/api/docs`

The Swagger interface provides:
- Interactive API testing ("Try it out" feature)
- Complete endpoint documentation
- Request/response schemas
- Model definitions
- Error response examples

### Available Endpoints

| Entity | Endpoints | Operations |
|--------|-----------|------------|
| **Users** | `/api/users` | POST, GET, GET/:id, PUT/:id |
| **Places** | `/api/places` | POST, GET, GET/:id, PUT/:id |
| **Reviews** | `/api/reviews` | POST, GET, GET/:id, PUT/:id, DELETE/:id |
| **Amenities** | `/api/amenities` | POST, GET, GET/:id, PUT/:id |

### Response Codes

| Code | Meaning | When |
|------|---------|------|
| 200 | OK | Successful GET/PUT |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation error |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Unexpected error |

---

## Additional Documentation

For more detailed information, see:
- **Swagger UI:** `http://localhost:5001/api/docs`
- **Test Reports:** Run `./run_all_tests.sh` for detailed test output

---
