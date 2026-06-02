from pydantic import BaseModel
# incoming API Request
class DeploymentCreate(BaseModel):
    app_name: str
    image_name: str
    replicas: int
    container_port: int