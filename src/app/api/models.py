from pydantic import BaseModel
from datetime import datetime


class SearchQuery(BaseModel):
    text: str
    region: str


class Counter(BaseModel):
    query_id: int
    number_of_deals: int
    timestamp: datetime
