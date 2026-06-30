URL = "https://archive-api.open-meteo.com/v1/archive"

import httpx



async def get_weather():
    params = {
	"latitude": 52.52,
	"longitude": 13.41,
	"start_date": "2026-06-13",
	"end_date": "2026-06-27",
	"hourly": ["temperature_2m",
        "precipitation",
        "wind_speed_10m"]
    }
    
    with httpx.Client() as client:
        response = client.get(URL, params=params)
        response.raise_for_status()

    data = response.json()

    return data