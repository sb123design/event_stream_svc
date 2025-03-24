import time
from sqlalchemy.orm import Session
from .models import Events
from .schemas import EventsResponse
from datetime import datetime
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