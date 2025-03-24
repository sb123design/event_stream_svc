import time
import random
import json
import asyncio
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from .database import get_db
from .models import Events
from .schemas import EventsResponse, EventsCreate
from datetime import datetime

router = APIRouter()

@router.post("/event", response_model=list[EventsResponse])
def create_event(event_data: EventsCreate, db: Session = Depends(get_db)):
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


@router.get("/stream")
def stream_timeseries(db: Session = Depends(get_db)):
    return StreamingResponse(
        event_stream_get(db),
        media_type="text/event-stream",
        headers={ 
            "Cache-Control": "no-cache",
            "Connection": "keep-alive" 
        }
    )

@router.get("/history", response_model=list[EventsResponse])
def get_timeseries(n: int = 10, db: Session = Depends(get_db)):
    return db.query(Events).order_by(Events.event_at.desc()).limit(n).all()

def event_stream_get(db: Session):
    last_id = 0
    while True:
        event_data = db.query(Events).filter(Events.id > last_id).all()
        if event_data:
            for item in event_data:
                data = EventsResponse.model_validate(item).model_dump_json()  # Serializes datetime
                yield f"data: {data}\n\n"
                last_id = item.id

        time.sleep(10)