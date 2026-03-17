-- HBnB Initial Data
-- Inserts administrator user and common amenities

-- Insert Administrator User
-- Password: AdminPass123 (hashed with bcrypt)
-- Note: This hash is for demonstration only. In production, generate a proper hash.
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    'admin-001',
    'System',
    'Administrator',
    'admin@hbnb.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEkKt6',  -- AdminPass123
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Insert Common Amenities
INSERT INTO amenities (id, name, description, created_at, updated_at) VALUES
('amenity-001', 'WiFi', 'High-speed wireless internet', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-002', 'Air Conditioning', 'Climate control system', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-003', 'Heating', 'Central heating system', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-004', 'Kitchen', 'Fully equipped kitchen', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-005', 'Washer', 'Washing machine', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-006', 'Dryer', 'Clothes dryer', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-007', 'TV', 'Television with cable', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-008', 'Pool', 'Swimming pool', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-009', 'Gym', 'Fitness center', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-010', 'Parking', 'Free parking space', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert Sample Users
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at) VALUES
('user-001', 'John', 'Doe', 'john@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEkKt6', FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('user-002', 'Jane', 'Smith', 'jane@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEkKt6', FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert Sample Places
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at) VALUES
('place-001', 'Cozy Studio in Downtown', 'Perfect for solo travelers', 75.00, 40.7128, -74.0060, 'user-001', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('place-002', 'Luxury Apartment with View', 'Stunning city skyline views', 200.00, 34.0522, -118.2437, 'user-001', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('place-003', 'Beach House Paradise', 'Direct beach access', 350.00, 25.7617, -80.1918, 'user-002', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Associate amenities with places
INSERT INTO place_amenity (place_id, amenity_id) VALUES
-- Cozy Studio amenities
('place-001', 'amenity-001'),  -- WiFi
('place-001', 'amenity-002'),  -- AC
('place-001', 'amenity-004'),  -- Kitchen
('place-001', 'amenity-007'),  -- TV
-- Luxury Apartment amenities
('place-002', 'amenity-001'),  -- WiFi
('place-002', 'amenity-002'),  -- AC
('place-002', 'amenity-003'),  -- Heating
('place-002', 'amenity-004'),  -- Kitchen
('place-002', 'amenity-009'),  -- Gym
('place-002', 'amenity-010'),  -- Parking
-- Beach House amenities
('place-003', 'amenity-001'),  -- WiFi
('place-003', 'amenity-002'),  -- AC
('place-003', 'amenity-004'),  -- Kitchen
('place-003', 'amenity-008'),  -- Pool
('place-003', 'amenity-010');  -- Parking

-- Insert Sample Reviews
INSERT INTO reviews (id, rating, comment, user_id, place_id, created_at, updated_at) VALUES
('review-001', 5, 'Amazing location! Clean and comfortable.', 'user-002', 'place-001', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('review-002', 4, 'Great view but a bit pricey.', 'user-002', 'place-002', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('review-003', 5, 'Perfect beach getaway! Highly recommended.', 'user-001', 'place-003', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
