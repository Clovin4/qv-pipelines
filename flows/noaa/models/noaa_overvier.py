from pydantic import BaseModel
from typing import List

class NOAAParams(BaseModel):
    dataset_id: str
    start_date: str
    end_date: str
    location_id: str
    data_types: List[str]
