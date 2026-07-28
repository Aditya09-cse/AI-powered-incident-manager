# IncidentAI

### Self-Hosted AI-Assisted Incident Management for DevOps

IncidentAI is a containerized incident management application for recording, tracking, investigating, and resolving DevOps incidents with locally hosted AI assistance.

It combines a Python/Flask application, PostgreSQL persistence, and Ollama-based LLM inference in a Docker Compose environment. The project is designed as both a functional incident-management system and a foundation for practicing production-oriented DevOps workflows.

---

## Overview

Operational incidents often involve two separate workflows:

1. Recording and tracking the incident
2. Investigating the underlying technical problem

IncidentAI brings both into one application.

Engineers can create and manage incidents, track their lifecycle, search historical incidents, generate AI-assisted analysis for a specific incident, and use a dedicated DevOps assistant for general troubleshooting.

AI inference runs locally through Ollama rather than an external hosted LLM API.

---

## Features

### Incident Management

Create incidents with:

- Title and description
- Category
- Severity
- Operational status
- Creation and resolution timestamps

Supported categories include:

`Linux` · `Docker` · `Kubernetes` · `AWS` · `CI/CD` · `Terraform` · `Database` · `Networking` · `Application`

Supported severities:

`Low` · `Medium` · `High` · `Critical`

Incident lifecycle:

```text
Open → Investigating → Resolved
```

---

### Operations Dashboard

The dashboard provides a quick operational view of:

- Total incidents
- Open incidents
- Incidents under investigation
- Resolved incidents
- Active critical incidents
- Recently created incidents

---

### Incident Search & Filtering

Incidents can be filtered by:

- Status
- Severity

Search is supported across:

- Title
- Description
- Category

---

### AI Incident Analysis

Individual incidents can be sent to the local Ollama service for structured troubleshooting analysis.

The AI receives the incident's:

- ID
- Title
- Category
- Severity
- Description

and generates guidance covering:

- Summary
- Likely root causes
- Troubleshooting steps
- Relevant commands
- Recommended fix
- Prevention

Generated analyses are persisted in PostgreSQL and associated with the original incident.

---

### DevOps AI Assistant

IncidentAI also provides a standalone AI assistant for troubleshooting questions involving:

- Linux
- Git
- Docker
- Kubernetes
- CI/CD
- GitHub Actions
- AWS
- Terraform
- Ansible
- Nginx
- PostgreSQL
- Networking
- Monitoring
- Application deployments

Conversation history is stored in PostgreSQL and can be cleared from the application.

> AI responses are troubleshooting guidance, not confirmed diagnoses. Validate recommendations before applying changes to production systems.

---

### Incident History

Resolved incidents are retained and available through a dedicated history view.

Historical incidents can also be searched by title, description, or category.

---

### Health & Readiness Endpoints

IncidentAI exposes endpoints useful for container orchestration and monitoring.

```text
GET /health
```

Reports application process health.

```text
GET /ready
```

Checks application dependencies, including:

- PostgreSQL connectivity
- Ollama availability

The readiness endpoint returns HTTP `503` when required dependencies are unavailable.

---

### Application Metrics

```text
GET /metrics
```

Exposes Prometheus-compatible incident metrics:

```text
incidents_total
incidents_open
incidents_investigating
incidents_resolved
```

The application exposes the metrics endpoint; a Prometheus server and Grafana dashboard are not part of the current stack.

---

## Architecture

```text
                         ┌─────────────────────┐
                         │       Browser       │
                         └──────────┬──────────┘
                                    │
                                    │ HTTP :5001
                                    ▼
                    ┌──────────────────────────────┐
                    │          IncidentAI          │
                    │                              │
                    │   Flask + Gunicorn           │
                    │                              │
                    │   • Dashboard                │
                    │   • Incident Management      │
                    │   • Incident History         │
                    │   • AI Incident Analysis     │
                    │   • DevOps AI Assistant      │
                    │   • Health / Metrics         │
                    └──────────────┬───────────────┘
                                   │
                            Docker Network
                                   │
                     ┌─────────────┴─────────────┐
                     │                           │
                     ▼                           ▼
          ┌────────────────────┐      ┌────────────────────┐
          │     PostgreSQL     │      │       Ollama       │
          │                    │      │                    │
          │ • Incidents        │      │ Local LLM runtime  │
          │ • AI analyses      │      │                    │
          │ • Chat history     │      │ llama3.2 model     │
          └──────────┬─────────┘      └──────────┬─────────┘
                     │                           │
                     ▼                           ▼
             postgres-data                 ollama-data
              Docker Volume                 Docker Volume
```

All three services communicate through an isolated Docker bridge network.

The application uses Docker service discovery to reach:

```text
postgres:5432
ollama:11434
```

Only the web application is exposed to the host.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Application Server | Gunicorn |
| Frontend | HTML, CSS, JavaScript, Jinja |
| Database | PostgreSQL 16 |
| Database Driver | psycopg |
| AI Runtime | Ollama |
| LLM | Llama 3.2 |
| Containerization | Docker |
| Multi-container orchestration | Docker Compose |
| Persistence | Docker Volumes |

---

## Project Structure

```text
AI-powered-incident-manager/
│
├── app/
│   ├── app.py
│   ├── db.py
│   ├── ollama_client.py
│   ├── requirements.txt
│   │
│   ├── static/
│   │   ├── app.js
│   │   └── style.css
│   │
│   └── templates/
│       ├── assistant.html
│       ├── base.html
│       ├── dashboard.html
│       ├── history.html
│       ├── incident.html
│       ├── incidents.html
│       └── index.html
│
├── database/
│   └── init.sql
│
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Database Design

IncidentAI currently uses three PostgreSQL tables.

### `incidents`

Stores the incident lifecycle:

```text
id
title
description
category
severity
status
created_at
updated_at
resolved_at
```

### `ai_analyses`

Stores AI-generated analysis associated with an incident.

```text
id
incident_id
analysis
created_at
```

`incident_id` references the corresponding incident and uses cascade deletion.

### `chat_history`

Stores interactions with the standalone DevOps AI assistant.

```text
id
user_message
ai_response
created_at
```

Indexes are created for incident status, creation time, and AI analysis lookup.

---

# Getting Started

## Prerequisites

You need:

- Git
- Docker
- Docker Compose

Verify:

```bash
git --version
docker --version
docker compose version
```

---

## 1. Clone the Repository

```bash
git clone https://github.com/Aditya09-cse/AI-powered-incident-manager.git

cd AI-powered-incident-manager
```

---

## 2. Configure Environment Variables

Create your local environment file:

```bash
cp .env.example .env
```

Update `.env` with your own values.

Example:

```env
DB_NAME=incident_manager
DB_USER=incident_user
DB_PASSWORD=change_this_password

FLASK_HOST=0.0.0.0
FLASK_PORT=5001

OLLAMA_URL=http://ollama:11434
OLLAMA_MODEL=llama3.2:1b
```

Never commit `.env`.

The repository contains `.env.example` only as a configuration template.

---

## 3. Start the Stack

```bash
docker compose up -d
```

Check container state:

```bash
docker compose ps
```

The stack consists of:

```text
devops-ai-app
devops-ai-postgres
devops-ai-ollama
```

The PostgreSQL service includes a health check, and the application waits for the database to become healthy before starting.

---

## 4. Install an Ollama Model

The Ollama image provides the runtime, but the LLM itself must be pulled separately.

For a lightweight local setup:

```bash
docker exec -it devops-ai-ollama ollama pull llama3.2:1b
```

Verify:

```bash
docker exec devops-ai-ollama ollama list
```

Make sure the model configured for the application matches a model installed in Ollama.

---

## 5. Open IncidentAI

```text
http://localhost:5001
```

---

## Verify the Deployment

### Application health

```bash
curl http://localhost:5001/health
```

Expected:

```json
{
  "service": "incident-manager",
  "status": "healthy"
}
```

### Dependency readiness

```bash
curl http://localhost:5001/ready
```

When PostgreSQL and Ollama are available:

```json
{
  "status": "ready",
  "database": true,
  "ollama": true
}
```

### Metrics

```bash
curl http://localhost:5001/metrics
```

---

## Containerization

The application image is based on:

```text
python:3.12-slim
```

Dependencies are installed from `app/requirements.txt`.

The application runs as a dedicated non-root user inside the container and is served by Gunicorn:

```text
2 workers
Port 5001
180-second worker timeout
```

The extended timeout accommodates local LLM requests that may take longer on CPU-only systems.

---

## Persistent Storage

Two named Docker volumes are used.

### `postgres-data`

Persists:

- Incidents
- AI analyses
- Chat history

### `ollama-data`

Persists downloaded Ollama models.

Stopping the stack normally does not remove these volumes:

```bash
docker compose down
```

To inspect them:

```bash
docker volume ls
```

> `docker compose down -v` removes the project's named volumes. This can delete your PostgreSQL data and downloaded Ollama models.

---

## Useful Commands

Start services:

```bash
docker compose up -d
```

Check status:

```bash
docker compose ps
```

Follow application logs:

```bash
docker logs -f devops-ai-app
```

Follow database logs:

```bash
docker logs -f devops-ai-postgres
```

Follow Ollama logs:

```bash
docker logs -f devops-ai-ollama
```

List installed models:

```bash
docker exec devops-ai-ollama ollama list
```

Stop the stack:

```bash
docker compose down
```

---

## Security Considerations

The current implementation includes several useful container and configuration practices:

- Application runs as a non-root container user
- Database credentials are supplied through environment variables
- `.env` is excluded from version control
- PostgreSQL and Ollama are not published directly to the host
- PostgreSQL data and Ollama models use dedicated persistent volumes

For a production deployment, additional controls would still be required, including authentication, authorization, TLS, secret management, network policies, request validation, backup strategy, and production observability.

---

## Current Scope

Implemented:

- Incident creation and persistence
- Severity and category classification
- Incident lifecycle management
- Incident search and filtering
- Resolved incident history
- AI-assisted incident analysis
- Persistent AI analysis history
- Standalone DevOps AI assistant
- Persistent assistant chat history
- PostgreSQL persistence
- Ollama integration
- Docker application image
- Non-root application container
- Gunicorn application server
- Docker Compose orchestration
- PostgreSQL health check
- Application health endpoint
- Dependency readiness endpoint
- Prometheus-compatible metrics endpoint
- Persistent PostgreSQL and Ollama volumes

Not currently implemented:

- Authentication / user management
- CI/CD pipeline
- Kubernetes deployment
- Helm charts
- Prometheus server
- Grafana dashboards
- Centralized logging
- Terraform infrastructure
- Cloud deployment

Keeping this distinction explicit makes the repository reflect the actual implementation rather than planned functionality.

---

## Planned DevOps Evolution

IncidentAI is intended to provide a realistic application on which additional DevOps practices can be implemented incrementally.

```text
Current
   │
   ├── Application
   ├── PostgreSQL
   ├── Ollama
   ├── Docker
   ├── Docker Compose
   ├── Health / Readiness
   └── Metrics endpoint
          │
          ▼
Next
   │
   ├── Automated testing
   ├── GitHub Actions
   ├── Container vulnerability scanning
   ├── Secret scanning
   └── Automated image publishing
          │
          ▼
Orchestration
   │
   ├── Kubernetes
   ├── ConfigMaps / Secrets
   ├── Persistent storage
   ├── Probes
   └── Helm
          │
          ▼
Observability
   │
   ├── Prometheus
   ├── Grafana
   └── Centralized logs
          │
          ▼
Infrastructure
   │
   ├── Terraform
   └── Cloud deployment
```

Planned components are intentionally not presented as implemented features.

---

## Learning Goals

This project provides a single application for practicing how different DevOps concerns interact around a real workload:

- Container image design
- Multi-container networking
- Persistent storage
- Environment configuration
- Service dependencies
- Health and readiness checks
- Application metrics
- CI/CD
- DevSecOps scanning
- Container orchestration
- Observability
- Infrastructure as Code

Rather than building an unrelated demo for every tool, each capability can be introduced into the same application architecture.

---

## Author

**Aditya Singh Tomar**

GitHub: `Aditya09-cse`

---

## License

No license has currently been added to this repository.

If you intend to make the project reusable by others, add an appropriate open-source license before describing it as open source.

---

If you find the project useful, consider starring the repository.