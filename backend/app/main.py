from fastapi import FastAPI

from app.database.database import engine
from app.database.base import Base

from app.models.deployment import Deployment

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PodPilot API", version="1.0.0")


@app.get("/")
def root():
    return {
        "message": "Welcome to PodPilot. Its good to see you. Hope you had a good experience"
    }
