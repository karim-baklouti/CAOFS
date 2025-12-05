# Containerization and Orchestration of services Labs - Lab 3 & Lab 4

This repository contains the exercises and resources for Lab 3 and Lab 4 of the Containerization and Orchestration of services course.

## Lab 3: Containerization & Kubernetes Basics

This lab focuses on containerizing a Python FastAPI application and deploying it to a Kubernetes cluster.

### Structure
The lab is divided into several exercises (`Ex1` to `Ex7`), guiding you through the process of:
1.  **Application Development**: A simple User Management API built with FastAPI.
2.  **Dockerization**: Creating a `Dockerfile` to package the application.
3.  **Kubernetes Deployment**:
    -   Creating Pods (`pod.yaml`).
    -   Managing Deployments and Services (in later exercises).


---

## Lab 4: Advanced Deployment Strategies & Jobs

This lab explores advanced Kubernetes deployment patterns and batch processing using Jobs and CronJobs.

### Deployment Strategies
Located in `lab4/`, you will find manifests for various deployment strategies:

-   **Rolling Update** (`rolling-deploy.yaml`):
    -   Updates Pods in a rolling fashion, ensuring zero downtime.
    -   Key fields: `maxSurge`, `maxUnavailable`.

-   **Recreate** (`recreate-deploy.yaml`):
    -   Terminates all existing Pods before creating new ones.
    -   Useful when version incompatibility prevents running both versions simultaneously.

-   **Blue/Green Deployment** (`blue-green.yaml`):
    -   Maintains two identical environments (Blue and Green).
    -   Traffic is switched from the old version (Blue) to the new version (Green) instantly.

-   **Canary Deployment** (`canary-deploy.yaml`, `canary-stable.yaml`):
    -   Rolls out the new version to a small subset of users (Canary) before a full rollout.

### Jobs & CronJobs
-   **Simple Job** (`simple-job.yaml`): Runs a task to completion once.
-   **Multi-completion Job** (`multi-job.yaml`): Runs a task multiple times (parallel or sequential).
-   **CronJob** (`simple-cronjob.yaml`): Runs a task on a schedule (like a cron entry).


