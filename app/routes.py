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
from .utilities import event_stream_get, create_dummy_data

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
def stream_timeseries(interval: float = 10.0, db: Session = Depends(get_db)):
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

@router.get("/history", response_model=list[EventsResponse])
def get_timeseries(n: int = 10, db: Session = Depends(get_db)):
    try:
        return db.query(Events).order_by(Events.event_at.desc()).limit(n).all()
    except Exception as e:
        raise Exception(status_code=500, detail=str(e))


@router.get("/create_dummy_data")
def create_dummy(n: int = 10, db: Session = Depends(get_db)):
    return create_dummy_data(db)

