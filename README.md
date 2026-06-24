# NAGP 2026 - Kubernetes, DevOps & FinOps Assignment

## Code Repository
https://github.com/Chitra-Mittal/nagp-k8s-assignment

## Docker Hub Image
https://hub.docker.com/r/chitramittal/nagp-api

## Service API URL
http://34.132.12.144/employees

## Screen Recording
https://nagarro-my.sharepoint.com/:f:/p/chitra_mittal/IgBQvuQyeoIOSr_dQ37dWdLHAaa8Fm1n73rxdrvDmrnL9LU?tdid=81bb23ea-83f2-4a1c-94cd-6921ea1f1866

## Project Structure
- `app/` - FastAPI application source code
- `k8s/` - All Kubernetes YAML manifests
- `Dockerfile` - Container image definition
- `docs/` - Assignment documentation

## Tech Stack
- API: Python FastAPI
- Database: PostgreSQL 15
- Container: Docker
- Orchestration: Kubernetes (GKE)

## Kubernetes Objects Deployed
- ConfigMap - DB host, port, database name
- Secret - DB password (base64 encoded)
- PersistentVolumeClaim - DB data persistence
- StatefulSet - PostgreSQL database (1 replica)
- Deployment - FastAPI API (4 replicas, RollingUpdate)
- HPA - Autoscaling (min:2, max:6, CPU threshold: 50%)
- Ingress - External access via Nginx Ingress Controller
- Services - ClusterIP for DB and API tiers
