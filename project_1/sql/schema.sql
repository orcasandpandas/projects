CREATE IF NOT EXISTS weather_data(
    weather_id INTEGER NOT NULL,
    weather_date DATE NOT NULL,
    precip FLOAT NOT NULL,
    wind_spd_10m FLOAT NOT NULL,
    PRIMARY KEY (weather_id)
);