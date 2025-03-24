from fastapi import FastAPI
from .database import engine, Base
from .routes import router

app = FastAPI(title="Event Stream API")

Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Root endpoint, Hello world!"}