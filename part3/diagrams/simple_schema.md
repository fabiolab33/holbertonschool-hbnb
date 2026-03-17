# HBnB Database - Simplified View

## Entity Relationship Diagram (Simplified)
```mermaid
erDiagram
    USER ||--o{ PLACE : owns
    USER ||--o{ REVIEW : writes
    PLACE ||--o{ REVIEW : receives
    PLACE }o--o{ AMENITY : has
    
    USER {
        string id
        string email
        string first_name
        string last_name
        boolean is_admin
    }
    
    PLACE {
        string id
        string title
        float price
        string owner_id
    }
    
    REVIEW {
        string id
        int rating
        string comment
        string user_id
        string place_id
    }
    
    AMENITY {
        string id
        string name
    }
```

## Legend

- `||--o{` : One-to-Many relationship
- `}o--o{` : Many-to-Many relationship
- PK: Primary Key
- FK: Foreign Key
- UK: Unique Key
