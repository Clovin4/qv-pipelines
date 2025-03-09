from prefect import flow
from prefect import task
import requests
from models.noaa_overvier import NOAAParams

@task
def extract_data(params: NOAAParams):
    base_url = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"
    headers = {"token": "YOUR_NOAA_API_TOKEN"}
    query_params = {
        "datasetid": params.dataset_id,
        "startdate": params.start_date,
        "enddate": params.end_date,
        "locationid": params.location_id,
        "datatypeid": ",".join(params.data_types),
        "limit": 1000
    }
    response = requests.get(base_url, headers=headers, params=query_params)
    response.raise_for_status()
    return response.json()

@task
def transform_data(raw_data):
    # Implement your transformation logic here
    transformed_data = raw_data  # Placeholder
    return transformed_data

@task
def load_data(transformed_data):
    # Implement your data loading logic here
    pass



@flow
def etl_flow(params: NOAAParams):
    raw_data = extract_data(params)
    transformed_data = transform_data(raw_data)
    load_data(transformed_data)

if __name__ == "__main__":
    params = NOAAParams(
        dataset_id="GHCND",
        start_date="2025-01-01",
        end_date="2025-01-31",
        location_id="FIPS:28",  # Mississippi FIPS code
        data_types=["TMAX", "TMIN", "PRCP"]
    )
    etl_flow(params)
