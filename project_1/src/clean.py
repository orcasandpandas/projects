import pandas as pd

def process_data(raw_data):
    records = []
    
    # Flatten the JSON
    for city_data in raw_data:
        city_name = city_data['city_name']
        lat = city_data['latitude']
        lon = city_data['longitude']
        daily = city_data['daily']
        
        # Loop through the days
        for i in range(len(daily['time'])):
            records.append({
                "city_name": city_name,
                "latitude": lat,
                "longitude": lon,
                "weather_date": daily['time'][i], # Note the column name change
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
    
    df['weather_date'] = pd.to_datetime(df['weather_date']).dt.date
    df = df.dropna() 
    
    return df