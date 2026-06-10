from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.deployment import Deployment
from app.schemas.deployment import (
    DeploymentCreate,
    DeploymentResponse
)

def create_deployment(deployment_data: DeploymentCreate, db: Session = Depends(get_db)):

    deployment = Deployment(
        app_name=deployment_data.app_name,
        image_name=deployment_data.image_name,
        replicas=deployment_data.replicas,
        container_port=deployment_data.container_port,
        status="running"
    )

    db.add(deployment)
    db.commit()
    db.refresh(deployment)

    return deployment

def get_deployments(
    db: Session = Depends(get_db)
):

    deployments = db.query(Deployment).all()

    return deployments

def get_deployment(
    deployment_id: int,
    db: Session = Depends(get_db)
):

    deployment = (
        db.query(Deployment)
        .filter(Deployment.id == deployment_id)
        .first()
    )

    if not deployment:
        raise HTTPException(
            status_code=404,
            detail=f"Deployment with id {deployment_id} not found"
        )

    return deployment

def update_deployment(
    deployment_id: int,
    deployment_data: DeploymentCreate,
    db: Session = Depends(get_db)
):

    deployment = (
        db.query(Deployment)
        .filter(Deployment.id == deployment_id)
        .first()
    )

    if not deployment:
        raise HTTPException(
            status_code=404,
            detail=f"Deployment with id {deployment_id} not found"
        )

    deployment.app_name = deployment_data.app_name
    deployment.image_name = deployment_data.image_name
    deployment.replicas = deployment_data.replicas
    deployment.container_port = deployment_data.container_port

    db.commit()
    db.refresh(deployment)

    return deployment

def delete_deployment(
    deployment_id: int,
    db: Session = Depends(get_db)
):

    deployment = (
        db.query(Deployment)
        .filter(Deployment.id == deployment_id)
        .first()
    )

    if not deployment:
        raise HTTPException(
            status_code=404,
            detail=f"Deployment with id {deployment_id} not found"
        )

    db.delete(deployment)
    db.commit()

    return {
        "message": f"Deployment with id {deployment_id} deleted successfully"
    }