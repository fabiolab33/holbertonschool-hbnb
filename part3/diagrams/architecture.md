# HBnB Application Architecture

## System Architecture Diagram
```mermaid
graph TB
    Client[Client Browser/API Consumer]
    
    subgraph "Flask Application"
        API[API Layer<br/>Flask-RESTX]
        Auth[Authentication<br/>JWT]
        Facade[Business Logic<br/>Facade Pattern]
        Repo[Repository Layer]
        
        API --> Auth
        API --> Facade
        Facade --> Repo
    end
    
    subgraph "Persistence Layer"
        Memory[InMemory Repository]
        SQLAlchemy[SQLAlchemy Repository]
        
        Repo --> Memory
        Repo --> SQLAlchemy
    end
    
    subgraph "Database"
        SQLite[(SQLite DB)]
        
        SQLAlchemy --> SQLite
    end
    
    subgraph "Models"
        User[User Model]
        Place[Place Model]
        Review[Review Model]
        Amenity[Amenity Model]
        
        SQLAlchemy --> User
        SQLAlchemy --> Place
        SQLAlchemy --> Review
        SQLAlchemy --> Amenity
    end
    
    Client -->|HTTP/JSON| API
    
    style Client fill:#e1f5ff
    style API fill:#fff4e1
    style Facade fill:#f0e1ff
    style SQLite fill:#e1ffe1
```

## Architecture Layers

### 1. API Layer (Flask-RESTX)
- RESTful endpoints
- Request validation
- Response formatting
- Swagger documentation

### 2. Authentication Layer (JWT)
- Token generation
- Token validation
- Role-based access control
- Password hashing (Bcrypt)

### 3. Business Logic Layer (Facade)
- Business rules
- Validation logic
- Orchestration
- Repository coordination

### 4. Repository Layer
- Abstraction over data access
- Switchable implementations
- CRUD operations

### 5. Persistence Layer
- InMemory (for testing)
- SQLAlchemy (for production)

### 6. Database Layer
- SQLite (development)
- MySQL/PostgreSQL (production)

## Data Flow
```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant J as JWT Auth
    participant F as Facade
    participant R as Repository
    participant D as Database
    
    C->>A: POST /api/places/
    A->>J: Validate Token
    J->>A: User ID + Claims
    A->>F: create_place(data, user_id)
    F->>F: Validate Business Rules
    F->>R: create(place)
    R->>D: INSERT INTO places
    D->>R: Success
    R->>F: Place Object
    F->>A: Place Object
    A->>C: 201 Created + JSON
```