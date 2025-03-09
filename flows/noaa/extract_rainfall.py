from prefect import task, flow
from datetime import timedelta
import pandas as pd
import requests

@task
def get_rainfall_data(start_date: str, end_date: str):
    """Fetch rainfall data from NOAA API"""
    url = f"https://www.ncei.noaa.gov/access/services/data/v1?dataset=global-hourly&startDate={start_date}&endDate={end_date}&dataTypes=PRCP&format=json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

@task
def process_rainfall_data(data):
    """Process the rainfall data into a DataFrame"""
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['DATE'])
    df.set_index('date', inplace=True)
    df['PRCP'] = pd.to_numeric(df['PRCP'], errors='coerce')
    return df

@flow
def extract_rainfall(start_date: str, end_date: str):
    """Extract rainfall data from NOAA API and process it"""
    raw_data = get_rainfall_data(start_date, end_date)
    processed_data = process_rainfall_data(raw_data)
    return processed_data

if __name__ == "__main__":
    start_date = "2023-01-01"
    end_date = "2023-01-31"
    rainfall_data = extract_rainfall(start_date, end_date)
    print(rainfall_data.head())