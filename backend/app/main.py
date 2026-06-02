from fastapi import FastAPI

from app.database.base import Base
from app.database.database import engine

# Import model so SQLAlchemy registers the table
from app.models.deployment import Deployment

from app.routes.deployments import router as deployment_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PodPilot API",
    version="1.0.0"
)

app.include_router(deployment_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to PodPilot. It's good to see you. Hope you had a good experience"
    }