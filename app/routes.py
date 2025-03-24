import time
import random
import json
import asyncio
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from database import get_db
from models import Events
from schemas import EventsResponse
from datetime import datetime

router = APIRouter()

@router.post("/event", response_model=list[EventsResponse])
def get_timeseries(db: Session = Depends(get_db)):
    try:
        event = Events()
        event.metric = "temperature"
        event.value = random.random() * 100
        event.event_at = datetime.now()
        db.add(event)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

@router.get("/stream")
async def stream_timeseries(db: Session = Depends(get_db)):
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

async def event_stream_get(db: Session):
    last_id = 0
    while True:
        event_data = db.query(Events).filter(Events.id > last_id).all()
        if event_data:
            for item in event_data:
                data = EventsResponse.from_orm(item).dict()
                yield f"data: {json.dumps(data)}\n\n"
                last_id = item.id

        await asyncio.sleep(10) 