from fastapi import HTTPException
from sqlalchemy.orm import Session
from kubernetes.client.exceptions import ApiException

from app.models.deployment import Deployment
from app.schemas.deployment import DeploymentCreate
from app.services.kubernetes_service import create_service, delete_service

from app.services.kubernetes_service import (
    create_deployment as create_k8s_deployment,
    delete_deployment as delete_k8s_deployment,
    get_deployment as get_k8s_deployment # retrieves a Deployment from Kubernetes
)

from app.services.kubernetes_service import get_deployment, get_deployment_status


def create_deployment(deployment_data: DeploymentCreate, db: Session):

    create_k8s_deployment(
        app_name=deployment_data.app_name,
        image_name=deployment_data.image_name,
        replicas=deployment_data.replicas,
    )

    create_service(
        app_name=deployment_data.app_name,
        container_port=deployment_data.container_port,
    )

    deployment = Deployment(
        app_name=deployment_data.app_name,
        image_name=deployment_data.image_name,
        replicas=deployment_data.replicas,
        container_port=deployment_data.container_port,
        status="running",
    )

    db.add(deployment)
    db.commit()
    db.refresh(deployment)

    return deployment


def get_deployments(db: Session):

    deployments = db.query(Deployment).all()

    for deployment in deployments:
        try:
            k8s_deployment = get_k8s_deployment(deployment.app_name)
            deployment.status = get_deployment_status(deployment.app_name)
            deployment.replicas = k8s_deployment.spec.replicas or 0

        except ApiException as e:
            if e.status == 404:
                deployment.status= "Not Found"
            else:
                raise

    db.commit()

    return deployments


def get_deployment( 
    deployment_id: int,
    db: Session,
): # retrieves a record from PostgreSQL using its integer ID

    deployment = db.query(Deployment).filter(Deployment.id == deployment_id).first()

    if not deployment:
        raise HTTPException(
            status_code=404,
            detail=f"Deployment with id {deployment_id} not found",
        )

    current_status = get_deployment_status(app_name=deployment.app_name)
    deployment.status = current_status

    db.commit()
    db.refresh(deployment)

    return deployment


def update_deployment(
    deployment_id: int,
    deployment_data: DeploymentCreate,
    db: Session,
):

    deployment = db.query(Deployment).filter(Deployment.id == deployment_id).first()

    if not deployment:
        raise HTTPException(
            status_code=404,
            detail=f"Deployment with id {deployment_id} not found",
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
    db: Session,
):
    deployment = (
        db.query(Deployment)
        .filter(Deployment.id == deployment_id)
        .first()
    )

    if not deployment:
        raise HTTPException(
            status_code=404,
            detail=f"Deployment with ID {deployment_id} not found",
        )

    app_name = deployment.app_name

    try:
        delete_k8s_deployment(app_name)

    except ApiException as e:
        if e.status != 404:
            raise

    try:
        delete_service(app_name)

    except ApiException as e:
        if e.status != 404:
            raise

    db.delete(deployment)
    db.commit()

    return {
        "message": f"Deployment {app_name} deleted successfully"
    }
