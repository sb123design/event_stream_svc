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
from .utilities import event_stream_get, create_dummy_data, get_history_logic, stream_timeseries_logic, create_event_logic

router = APIRouter()

@router.post("/event", response_model=list[EventsResponse])
def create_event(event_data: EventsCreate, db: Session = Depends(get_db)):
    return create_event_logic(event_data, db)


@router.get("/stream")
def stream_timeseries(interval: float = 10.0, db: Session = Depends(get_db)):
    return stream_timeseries_logic(db, interval)

@router.get("/history", response_model=list[EventsResponse])
def get_history(n: int = 10, db: Session = Depends(get_db)):
    return get_history_logic(db, n)


@router.get("/create_dummy_data")
def create_dummy(n: int = 10, db: Session = Depends(get_db)):
    return create_dummy_data(db)

