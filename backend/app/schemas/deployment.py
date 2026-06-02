from pydantic import BaseModel
from datetime import datetime


class DeploymentCreate(BaseModel):
    app_name: str
    image_name: str
    replicas: int
    container_port: int


class DeploymentResponse(BaseModel):
    id: int
    app_name: str
    image_name: str
    replicas: int
    container_port: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True