-- Create the flight_db database (this should be done separately if the DB doesn't exist yet)
-- CREATE DATABASE flight_db;

-- Table for countries
CREATE TABLE country (
    country_id SERIAL PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL UNIQUE
);

-- Table for states, linked to the country
CREATE TABLE state (
    state_id SERIAL PRIMARY KEY,
    state_name VARCHAR(100) NOT NULL,
    country_id INT NOT NULL,
    FOREIGN KEY (country_id) REFERENCES country(country_id) ON DELETE CASCADE
);

-- Table for cities, linked to the state
CREATE TABLE city (
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    state_id INT NOT NULL,
    FOREIGN KEY (state_id) REFERENCES state(state_id) ON DELETE CASCADE
);

-- Table for planes
CREATE TABLE plane (
    plane_id SERIAL PRIMARY KEY,
    plane_model VARCHAR(100) NOT NULL,
    manufacturer VARCHAR(100),
    capacity INT NOT NULL
);

-- Table for flights, including source (src) and destination (desti), and datetime
CREATE TABLE flight (
    flight_id SERIAL PRIMARY KEY,
    plane_id INT NOT NULL,
    source_city_id INT NOT NULL,
    dest_city_id INT NOT NULL,
    flight_date TIMESTAMP NOT NULL,
    FOREIGN KEY (plane_id) REFERENCES plane(plane_id) ON DELETE CASCADE,
    FOREIGN KEY (source_city_id) REFERENCES city(city_id) ON DELETE CASCADE,
    FOREIGN KEY (dest_city_id) REFERENCES city(city_id) ON DELETE CASCADE
);
