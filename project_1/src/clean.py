import pandas as pd
import json

def process_data(filepath="raw_weather_data.json"):
    with open(filepath, "r") as f:
        raw_data = json.load(f)
        
    records = []
    # Flatten the JSON
    for city_data in raw_data:
        city_name = city_data['city_name']
        daily = city_data['daily']
        
        # Loop through the days
        for i in range(len(daily['time'])):
            records.append({
                "city_name": city_name,
                "date": daily['time'][i],
                "max_temp": daily['temperature_2m_max'][i],
                "precip": daily['precipitation_sum'][i],
                "wind_speed": daily['wind_speed_10m_max'][i]
            })
            
    df = pd.DataFrame(records)
    
    print("--- Data Profiling ---")
    print("Null Values:\n", df.isnull().sum())
    print("\nData Types:\n", df.dtypes)
    print("\nDuplicate Rows:", df.duplicated().sum())
    print("\nValue Ranges:\n", df.describe())
    
    df['date'] = pd.to_datetime(df['date'])
    df = df.dropna() 
    
    return df