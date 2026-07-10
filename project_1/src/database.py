# src/database.py
import psycopg
import pandas as pd
import os

DB_PARAMS = "dbname=weather_db user=postgres password=yourpassword host=localhost"

def get_sql_queries():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sql_file_path = os.path.join(current_dir, '..', 'sql', 'insert.sql')
    
    with open(sql_file_path, 'r') as file:
        sql_content = file.read()
        
    # We split the file based on the SQL comments to get the exact query strings.
    # WARNING: Do not change the comments in your insert.sql file or this will break!
    try:
        city_query = sql_content.split('-- INSERT_CITY')[1].split('-- INSERT_WEATHER')[0].strip()
        weather_query = sql_content.split('-- INSERT_WEATHER')[1].strip()
    except IndexError:
        raise ValueError("Could not parse insert.sql. Make sure the '-- INSERT_CITY' and '-- INSERT_WEATHER' comments exist exactly as written.")
        
    return city_query, weather_query

def load_data_to_db(df):
    print("Connecting to the database...")
    city_query, weather_query = get_sql_queries()
    
    # We use psycopg to connect to the database
    with psycopg.connect(DB_PARAMS) as conn:
        with conn.cursor() as cur:
            
            # 1. Insert into the cities dimension table first
            unique_cities = df[['city_name', 'latitude', 'longitude']].drop_duplicates()
            for _, row in unique_cities.iterrows():
                cur.execute(city_query, (row['city_name'], row['latitude'], row['longitude']))
            
            # 2. Insert into the weather_records fact table
            for _, row in df.iterrows():
                cur.execute(weather_query, (
                    row['city_name'], 
                    row['weather_date'], 
                    row['max_temp'], 
                    row['precip'], 
                    row['wind_speed']
                ))
                
        # Commit the transaction to save changes
        conn.commit()
        
    print("Database load completed successfully.")