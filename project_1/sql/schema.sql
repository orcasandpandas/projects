CREATE TABLE IF NOT EXISTS cities (
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) UNIQUE NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS weather_records (
    record_id SERIAL PRIMARY KEY,
    city_id INTEGER NOT NULL,
    weather_date DATE NOT NULL,
    max_temperature_c FLOAT,
    precipitation_mm FLOAT,
    max_wind_speed FLOAT,
    FOREIGN KEY (city_id) REFERENCES cities(city_id),
    UNIQUE (city_id, weather_date)
);