from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import TimeSeries
from schemas import TimeSeriesCreate, TimeSeriesResponse

router = APIRouter()

@router.post("/timeseries/", response_model=TimeSeriesResponse)
def create_timeseries(ts: TimeSeriesCreate, db: Session = Depends(get_db)):
    db_ts = TimeSeries(timestamp=ts.timestamp, value=ts.value)
    db.add(db_ts)
    db.commit()
    db.refresh(db_ts)
    return db_ts

@router.get("/stream", response_model=list[TimeSeriesResponse])
def get_timeseries(db: Session = Depends(get_db)):
    return db.query(TimeSeries).all()

@router.get("/history", response_model=list[TimeSeriesResponse])
def get_timeseries(db: Session = Depends(get_db)):
    return db.query(TimeSeries).all()