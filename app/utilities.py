import time
from sqlalchemy.orm import Session
from .models import Events
from .schemas import EventsResponse
from datetime import datetime
from fastapi.responses import StreamingResponse
from .schemas import EventsResponse, EventsCreate
from fastapi import APIRouter, Depends
from .database import get_db
import random


def event_stream_get(db: Session, interval: float = 10.0):
    last_id = 0
    while True:
        event_data = db.query(Events).filter(Events.id > last_id).all()
        if event_data:
            for item in event_data:
                data = EventsResponse.model_validate(item).model_dump_json()  # Serializes datetime
                yield f"{data}\n\n"
                last_id = item.id
                time.sleep(interval)


def create_dummy_data(db: Session):
    for _ in range(10):
        event = Events(
            metric="temperature",
            value=round(random.uniform(0, 100), 2),
            event_at=datetime.now()
        )
        db.add(event)
    db.commit()
    db.refresh(event)
    return event


def get_history_logic(db: Session, n: int = 10):
    try:
        return db.query(Events).order_by(Events.event_at.desc()).limit(n).all()
    except Exception as e:
        raise Exception(status_code=500, detail=str(e))
    
def stream_timeseries_logic(db: Session, interval: float = 10.0):
    try:
        return StreamingResponse(
            event_stream_get(db, interval),
            media_type="text/event-stream",
            headers={ 
                "Cache-Control": "no-cache",
                "Connection": "keep-alive" 
            }
        )
    except Exception as e:
        raise Exception(status_code=500, detail=str(e))
    
def create_event_logic(event_data: EventsCreate, db: Session = Depends(get_db)):
    try:
        event = Events(
            metric=event_data.metric,
            value=event_data.value,
            event_at=event_data.event_at or datetime.now()
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        all_events = db.query(Events).all()
        return all_events
    except Exception as e:
        db.rollback()
        raise Exception(status_code=500, detail=str(e))