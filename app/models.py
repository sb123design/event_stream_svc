from sqlalchemy import Column, Integer, String, DateTime, Float
from .database import Base

class Events(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    metric = Column(String, index=True)
    value = Column(Float, index=True)
    event_at = Column(DateTime)