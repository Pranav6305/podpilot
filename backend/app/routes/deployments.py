from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.deployment import Deployment
from app.schemas.deployment import (
    DeploymentCreate,
    DeploymentResponse
)

from app.services import deployment_service

router = APIRouter(tags=["deployments"])

@router.post(
    "/deployments",
    response_model=DeploymentResponse
)
def create_deployment(
    deployment_data: DeploymentCreate,
    db: Session = Depends(get_db)
):

    return deployment_service.create_deployment(deployment_data, db)

@router.get(
    "/deployments",
    response_model=list[DeploymentResponse]
)
def get_deployments(
    db: Session = Depends(get_db)
):

    return deployment_service.get_deployments(db)

@router.get(
    "/deployments/{deployment_id}",
    response_model=DeploymentResponse
)
def get_deployment(
    deployment_id: int,
    db: Session = Depends(get_db)
):

    return deployment_service.get_deployment(deployment_id, db)

@router.put(
    "/deployments/{deployment_id}",
    response_model=DeploymentResponse
)
def update_deployment(
    deployment_id: int,
    deployment_data: DeploymentCreate,
    db: Session = Depends(get_db)
):

    return deployment_service.update_deployment(deployment_id, deployment_data, db)

@router.delete("/deployments/{deployment_id}")
def delete_deployment(
    deployment_id: int,
    db: Session = Depends(get_db)
):

    return deployment_service.delete_deployment(deployment_id, db)