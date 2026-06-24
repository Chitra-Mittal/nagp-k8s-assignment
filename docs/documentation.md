# NAGP 2026 - Kubernetes, DevOps & FinOps Assignment
## Documentation

---

## 1. Requirement Understanding

The assignment requires deploying a two-tier application on Kubernetes:
- A Service API tier that exposes an HTTP endpoint and fetches data from a database
- A Database tier that stores data persistently and is accessible only within the cluster

Key requirements understood:
- API tier must run 4 pods, support rolling updates, self-healing, and HPA
- Database must use persistent storage so data survives pod restarts
- Passwords must not be visible in YAML files
- Database config must be injected via ConfigMap, not hardcoded
- API must be accessible externally via Ingress
- FinOps: define resource limits and identify cost optimization opportunities

---

## 2. Assumptions

- A fresh Kubernetes cluster is used with no pre-existing resources
- PostgreSQL is used as the database with one table (employees) containing 7 records
- Python FastAPI is used for the service API tier
- GKE (Google Kubernetes Engine) is used as the Kubernetes platform
- Nginx Ingress Controller is used for external access
- Docker Hub is used to host the container image
- HPA manages pod scaling dynamically based on CPU utilization

---

## 3. Solution Overview

Tech Stack: Python FastAPI, PostgreSQL 15, Docker, Kubernetes on GKE

Architecture:
- External traffic hits Nginx Ingress at the external IP
- Ingress routes to API Service (ClusterIP)
- API Service load balances across 4 FastAPI pods
- Each API pod connects to PostgreSQL using service name, not pod IP
- PostgreSQL runs as StatefulSet with PVC for data persistence

Kubernetes Objects Used:
- ConfigMap: DB host, port, name injected as env vars into API pods
- Secret: DB password in base64, never visible in plain text
- PVC: Persistent storage for PostgreSQL data
- StatefulSet: Runs PostgreSQL with stable identity and persistent volume
- Deployment: Runs 4 API replicas with RollingUpdate strategy
- ClusterIP Services: Internal communication between tiers using DNS names
- Ingress: Exposes API externally via Nginx Ingress Controller
- HPA: Scales API pods between 2-6 based on 50% CPU utilization

Self-healing: Kubernetes automatically restarts any pod that crashes or is deleted.
Rolling Updates: maxSurge 1, maxUnavailable 1 - at least 3 pods always running during updates.
Data Persistence: PostgreSQL data stored on PVC-backed disk, survives pod deletion.

---

## 4. Justification for Resources Utilized

e2-small nodes (2 nodes):
Selected for cost efficiency on GKE. Sufficient for running FastAPI and PostgreSQL for demo purposes.

PostgreSQL 15:
Stable relational database. Fits the requirement of a single table with structured records.

Python FastAPI:
Lightweight and fast. Low memory footprint suits the 128Mi memory request per pod.

Resource Requests and Limits (FinOps):
- CPU request: 100m, limit: 250m
- Memory request: 128Mi, limit: 256Mi
- Prevents any single pod from consuming excessive cluster resources

Three FinOps Optimization Opportunities:
1. HPA scales pods down during low traffic - avoids paying for idle replicas
2. Resource limits prevent over-provisioning - pods only use what they need
3. Using e2-small nodes instead of larger machine types reduces compute cost significantly
