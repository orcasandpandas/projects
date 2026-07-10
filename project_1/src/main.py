# src/main.py
import psycopg
import pandas as pd
from api import get_weather
from clean import process_data
from database import load_data_to_db

DB_PARAMS = "dbname=weather user=postgres password=pass host=localhost"

def run_quick_analysis():
    print("\n--- Running Final Data Analysis ---")
    
    queries = [
        """SELECT c.city_name, MAX(w.max_temperature_c) AS highest_temp 
           FROM weather_records w JOIN cities c ON w.city_id = c.city_id 
           GROUP BY c.city_name;""",
           
        """SELECT c.city_name, DATE_TRUNC('month', w.weather_date) AS month, SUM(w.precipitation_mm) AS total_precip 
           FROM weather_records w JOIN cities c ON w.city_id = c.city_id 
           GROUP BY c.city_name, month ORDER BY c.city_name, month;""",
           
        """SELECT c.city_name, w.weather_date, w.max_wind_speed 
           FROM weather_records w JOIN cities c ON w.city_id = c.city_id 
           ORDER BY w.max_wind_speed DESC LIMIT 1;""",
           
        """SELECT c.city_name, AVG(w.precipitation_mm) AS avg_rainfall 
           FROM weather_records w JOIN cities c ON w.city_id = c.city_id 
           GROUP BY c.city_name;""",
           
        """SELECT c.city_name, COUNT(*) AS extreme_days 
           FROM weather_records w JOIN cities c ON w.city_id = c.city_id 
           WHERE w.max_temperature_c > 35 
           GROUP BY c.city_name;"""
    ]

    with psycopg.connect(DB_PARAMS) as conn:
        with conn.cursor() as cur:
            for i, query in enumerate(queries, 1):
                cur.execute(query)
                rows = cur.fetchall()
                colnames = [desc[0] for desc in cur.description]
                
                print(f"\nQuestion {i}:")
                df = pd.DataFrame(rows, columns=colnames)
                print(df.to_string())

def main():
    print("Step 1: Extracting...")
    raw_data = get_weather()    
    
    print("\nStep 2: Cleaning...")
    cleaned_df = process_data(raw_data)
    
    print("\nStep 3: Loading...")
    load_data_to_db(cleaned_df)
    
    # Running the dirty queries right here
    run_quick_analysis()
    
    print("\nPipeline execution fully complete.")

if __name__ == "__main__":
    main()