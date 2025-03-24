import time
from sqlalchemy.orm import Session
from .models import Events
from .schemas import EventsResponse


def event_stream_get(db: Session, interval: float = 10.0):
    last_id = 0
    while True:
        event_data = db.query(Events).filter(Events.id > last_id).all()
        if event_data:
            for item in event_data:
                data = EventsResponse.model_validate(item).model_dump_json()  # Serializes datetime
                yield f"data: {data}\n\n"
                last_id = item.id

        time.sleep(interval)