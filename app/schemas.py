from pydantic import BaseModel

class EventsCreate(BaseModel):
    event_at: str
    metric: str
    value: float

class EventResponse(EventsCreate):
    id: int
    
    class Config:
        from_attributes = True