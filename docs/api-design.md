API Design


POST/deploy

Purpose: Create Kubernetes deployments and services for application and stores deployment metadata in PostgreSQL.

Request:
{
    "app_name":"nginx-demo",
    "image":"nginx:latest",
    "replicas":2,
    "container_port":80
}

Response:
{
    "message":"Deployment created successfully"
}


GET/deployments

Purpose: Returns all the deployments managed by PodPilot.

Response:
[
    {
        "app_name":"nginx-demo",
        "image":"nginx-latest",
        "status":"Running"
    }
]

DELETE/deployments/{app_name}

Purpose: Deletes kubernetes deployments and services associated with the application

Response:
{
    "message":"Deployment deleted successfully"
}