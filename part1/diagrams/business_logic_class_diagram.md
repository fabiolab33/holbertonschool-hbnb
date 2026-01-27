# Business Logic Layer – Class Diagram

```mermaid
classDiagram
    class User {
        +UUID id
        +string first_name
        +string last_name
        +string email
        +string password
        +boolean is_admin
        +datetime created_at
        +datetime updated_at
        +register()
        +update_profile()
        +delete()
    }

    class Place {
        +UUID id
        +string title
        +string description
        +float price
        +float latitude
        +float longitude
        +datetime created_at
        +datetime updated_at
        +create()
        +update()
        +delete()
        +list()
    }

    class Review {
        +UUID id
        +int rating
        +string comment
        +datetime created_at
        +datetime updated_at
        +create()
        +update()
        +delete()
    }

    class Amenity {
        +UUID id
        +string name
        +string description
        +datetime created_at
        +datetime updated_at
        +create()
        +update()
        +delete()
        +list()
    }

    User "1" --> "*" Place : owns
    User "1" --> "*" Review : writes
    Place "1" --> "*" Review : has
    Place "*" --> "*" Amenity : includes
```

- This class diagram represents the core bussines entities of the HBnB application. It defines their attributes, methods, and relationships, providing a clear view of the bussiness logic layer.