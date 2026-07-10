from api import get_weather
from clean import process_data
from database import load_data_to_db

def main():
    raw_data = get_weather()    
    cleaned_df = process_data(raw_data)
    load_data_to_db(cleaned_df)
    

if __name__ == "__main__":
    main()