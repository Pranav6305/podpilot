# Database Schema

## Table: deployments

| Column Name    | Data Type | Description                |
| -------------- | --------- | -------------------------- |
| id             | Integer   | Primary Key                |
| app_name       | String    | Application Name           |
| image_name     | String    | Docker Image Name          |
| replicas       | Integer   | Number of Replicas         |
| container_port | Integer   | Application Container Port |
| status         | String    | Deployment Status          |
| created_at     | Timestamp | Deployment Creation Time   |

## Example Record

| id | app_name   | image_name   | replicas | container_port | status  |
| -- | ---------- | ------------ | -------- | -------------- | ------- |
| 1  | nginx-demo | nginx:latest | 2        | 80             | Running |
