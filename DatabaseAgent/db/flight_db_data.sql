-- Insert some countries
INSERT INTO country (country_name) VALUES ('USA'), ('India'), ('Germany');

-- Insert some states
INSERT INTO state (state_name, country_id) 
VALUES 
    ('California', 1),
    ('Texas', 1),
    ('Maharashtra', 2),
    ('Bavaria', 3);

-- Insert some cities
INSERT INTO city (city_name, state_id) 
VALUES 
    ('Los Angeles', 1),
    ('Dallas', 2),
    ('Mumbai', 3),
    ('Munich', 4);

-- Insert some planes
INSERT INTO plane (plane_model, manufacturer, capacity) 
VALUES 
    ('Boeing 737', 'Boeing', 200),
    ('Airbus A320', 'Airbus', 180);

-- Insert some flights
INSERT INTO flight (plane_id, source_city_id, dest_city_id, flight_date) 
VALUES 
    (1, 1, 3, '2024-01-05 10:00:00'), 
    (2, 2, 4, '2024-01-06 14:30:00');
