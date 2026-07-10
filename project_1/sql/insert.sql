INSERT INTO cities (city_name, latitude, longitude)
VALUES (%s, %s, %s)
ON CONFLICT (city_name) DO NOTHING;

INSERT INTO weather_records (
    city_id, weather_date, max_temperature_c, 
    precipitation_mm, max_wind_speed
)
VALUES (
    (SELECT city_id FROM cities WHERE city_name = %s),
    %s, %s, %s, %s
)
ON CONFLICT (city_id, weather_date) DO NOTHING;