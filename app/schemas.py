from pydantic import BaseModel
from datetime import datetime

class EventsCreate(BaseModel):
    metric: str
    value: float
    event_at: datetime = None

class EventsResponse(BaseModel):
    id: int
    metric: str
    value: float
    event_at: datetime

    class Config:
        from_attributes = True