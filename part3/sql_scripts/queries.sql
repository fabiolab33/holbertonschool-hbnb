-- HBnB Verification Queries
-- Test CRUD operations and relationships

-- ============================================
-- READ Operations
-- ============================================

-- Query 1: List all users
SELECT 
    id, 
    email, 
    first_name, 
    last_name, 
    is_admin
FROM users
ORDER BY email;

-- Query 2: List all places with owner information
SELECT 
    p.id,
    p.title,
    p.price,
    p.latitude,
    p.longitude,
    u.email as owner_email,
    u.first_name || ' ' || u.last_name as owner_name
FROM places p
JOIN users u ON p.owner_id = u.id
ORDER BY p.title;

-- Query 3: List all amenities
SELECT 
    id,
    name,
    description
FROM amenities
ORDER BY name;

-- Query 4: Get places with their amenities (many-to-many)
SELECT 
    p.title as place,
    GROUP_CONCAT(a.name, ', ') as amenities
FROM places p
LEFT JOIN place_amenity pa ON p.id = pa.place_id
LEFT JOIN amenities a ON pa.amenity_id = a.id
GROUP BY p.id, p.title
ORDER BY p.title;

-- Query 5: Get places with their reviews
SELECT 
    p.title as place,
    COUNT(r.id) as review_count,
    AVG(r.rating) as average_rating
FROM places p
LEFT JOIN reviews r ON p.id = r.place_id
GROUP BY p.id, p.title
ORDER BY average_rating DESC;

-- Query 6: Get detailed reviews with user and place info
SELECT 
    r.id,
    r.rating,
    r.comment,
    u.first_name || ' ' || u.last_name as reviewer,
    p.title as place,
    r.created_at
FROM reviews r
JOIN users u ON r.user_id = u.id
JOIN places p ON r.place_id = p.id
ORDER BY r.created_at DESC;

-- Query 7: Count entities
SELECT 
    'Users' as entity, COUNT(*) as count FROM users
UNION ALL
SELECT 'Places', COUNT(*) FROM places
UNION ALL
SELECT 'Reviews', COUNT(*) FROM reviews
UNION ALL
SELECT 'Amenities', COUNT(*) FROM amenities;

-- ============================================
-- Advanced Queries
-- ============================================

-- Query 8: Find places with specific amenity (e.g., WiFi)
SELECT DISTINCT
    p.title,
    p.price,
    p.description
FROM places p
JOIN place_amenity pa ON p.id = pa.place_id
JOIN amenities a ON pa.amenity_id = a.id
WHERE a.name = 'WiFi'
ORDER BY p.price;

-- Query 9: Find users who own multiple places
SELECT 
    u.email,
    u.first_name || ' ' || u.last_name as owner,
    COUNT(p.id) as place_count
FROM users u
JOIN places p ON u.id = p.owner_id
GROUP BY u.id, u.email, u.first_name, u.last_name
HAVING COUNT(p.id) > 1
ORDER BY place_count DESC;

-- Query 10: Find places without reviews
SELECT 
    p.title,
    p.price,
    p.description
FROM places p
LEFT JOIN reviews r ON p.id = r.place_id
WHERE r.id IS NULL
ORDER BY p.title;
