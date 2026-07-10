# src/api.py
import httpx
import json

URL = "https://archive-api.open-meteo.com/v1/archive"

CITIES = [
    {"name": "Chicago", "lat": 41.88, "lon": 	-87.62},
    {"name": "Phoenix", "lat": 33.44, "lon": -112.07},
    {"name": "Beijing", "lat": 39.92, "lon": 116.38}
]

def get_weather():
    all_city_data = []
    
    with httpx.Client() as client:
        for city in CITIES:
            params = {
                "latitude": city["lat"],
                "longitude": city["lon"],
                "start_date": "2024-01-01", 
                "end_date": "2024-12-31",
                "daily": ["temperature_2m_max", "precipitation_sum", "wind_speed_10m_max"],
                "timezone": "auto"
            }
            
            response = client.get(URL, params=params)
            response.raise_for_status()
            
            data = response.json()
            data['city_name'] = city["name"]
            data['latitude'] = city["lat"]  
            data['longitude'] = city["lon"]
            all_city_data.append(data)

    with open("raw_weather_data.json", "w") as f:
        json.dump(all_city_data, f, indent=4)
        
    return all_city_data