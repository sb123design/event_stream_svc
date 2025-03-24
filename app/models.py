from sqlalchemy import Column, Integer, String, DateTime
from .database import Base

class Events(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    event_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)