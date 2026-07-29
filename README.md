<div align="center">

# ⚡ IncidentAI

## AI-Powered Incident Management & DevOps Troubleshooting Platform

A self-hosted incident management platform combining  
**Flask + PostgreSQL + Ollama + Kubernetes** to help engineers track, investigate, and resolve infrastructure issues with local AI assistance.

<br>

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-black?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Deployed-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local_AI-black?style=for-the-badge)

</div>

---

# 🚀 Overview

IncidentAI is a self-hosted DevOps incident management platform designed for engineers who need a practical way to:

- Record operational incidents
- Track incident lifecycle
- Investigate failures
- Generate AI-assisted troubleshooting reports
- Maintain historical incident knowledge

The platform runs a local Large Language Model using Ollama, meaning incident data stays inside your own infrastructure.

No external AI API is required.

---

# ✨ Features

## 🚨 Incident Management

Create and manage incidents with:

- Title
- Description
- Category
- Severity
- Status

Incident lifecycle:

```
OPEN
  |
  v
INVESTIGATING
  |
  v
RESOLVED
```

---

## 🤖 AI Incident Analysis

IncidentAI sends incident context to a local Ollama model and generates structured troubleshooting guidance.

AI provides:

```
SUMMARY

LIKELY ROOT CAUSES

TROUBLESHOOTING STEPS

COMMANDS

RECOMMENDED FIX

PREVENTION
```

Example supported areas:

- Kubernetes troubleshooting
- Docker issues
- Linux debugging
- PostgreSQL failures
- Networking problems
- CI/CD failures
- Cloud infrastructure concepts

---

## 💬 DevOps AI Assistant

A conversational assistant for engineers.

Example questions:

```
Why is my Kubernetes pod restarting?

How do I debug PostgreSQL connection issues?

Why is my Docker container failing?

How do I troubleshoot nginx 502 errors?
```

Chat history is stored in PostgreSQL.

---

# 🏗 Architecture

```
                         USER
                          |
                          |
                          v

                  Flask Application
                  Gunicorn Server

                          |
          ---------------------------------
          |                               |
          v                               v

     PostgreSQL                      Ollama
     Database                       Local LLM

          |                               |
          |                               |
          v                               v

     Incident Data                  AI Analysis
     Chat History                   Inference
```

---

# ☸ Kubernetes Architecture

IncidentAI is deployed using Kubernetes resources.

```
                 Kubernetes Cluster

                        |
        --------------------------------

             |              |              |

             v              v              v

        Flask App      PostgreSQL       Ollama
        Deployment     Deployment      Deployment


             |              |              |

             v              v              v

             PVC            PVC            PVC


             |
             v

       Persistent Storage
```

---

# 🧩 Technology Stack

| Component | Purpose |
|---|---|
| Python | Application development |
| Flask | Backend framework |
| Gunicorn | Production WSGI server |
| PostgreSQL 16 | Persistent database |
| Ollama | Local LLM inference |
| TinyLlama | AI troubleshooting model |
| Docker | Containerization |
| Kubernetes | Container orchestration |
| Persistent Volumes | Data persistence |
| ConfigMap | Application configuration |
| Secrets | Sensitive configuration |

---

# 📂 Repository Structure

```
AI-powered-incident-manager
│
├── app
│   ├── app.py
│   ├── db.py
│   ├── ollama_client.py
│   ├── requirements.txt
│   │
│   ├── static
│   │
│   └── templates
│
├── database
│   └── init.sql
│
├── k8s
│   │
│   ├── namespace.yml
│   │
│   ├── app-deployment.yml
│   ├── flask-service.yml
│   │
│   ├── postgres-deployment.yml
│   ├── postgres-service.yml
│   │
│   ├── ollama-deployment.yml
│   ├── ollama-service.yml
│   │
│   ├── pv.yml
│   ├── pvc.yml
│   │
│   ├── ollama-pv.yml
│   ├── ollama-pvc.yml
│   │
│   ├── ConfigMap.yml
│   └── secrets.yml
│
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

# 🚀 Kubernetes Deployment

## 1. Create Namespace

```bash
kubectl apply -f k8s/namespace.yml
```

---

## 2. Apply Configuration

```bash
kubectl apply -f k8s/ConfigMap.yml
```

---

## 3. Create Persistent Storage

Application storage:

```bash
kubectl apply -f k8s/pv.yml
kubectl apply -f k8s/pvc.yml
```

Ollama model storage:

```bash
kubectl apply -f k8s/ollama-pv.yml
kubectl apply -f k8s/ollama-pvc.yml
```

---

## 4. Deploy PostgreSQL

```bash
kubectl apply -f k8s/postgres-deployment.yml
kubectl apply -f k8s/postgres-service.yml
```

---

## 5. Deploy Ollama

```bash
kubectl apply -f k8s/ollama-deployment.yml
kubectl apply -f k8s/ollama-service.yml
```

---

## 6. Deploy Application

```bash
kubectl apply -f k8s/app-deployment.yml
kubectl apply -f k8s/flask-service.yml
```

---

## Verify Deployment

```bash
kubectl get pods -n ai-incident-namespace
```

Expected:

```
ai-incident-deployment     Running
postgres-deployment        Running
ollama                     Running
```

---

# 🔌 Service Communication

Inside Kubernetes:

```
Flask Application

        |
        |

postgres:5432


        |
        |

ollama:11434
```

Services communicate internally through Kubernetes DNS.

---

# 💾 Database Design

IncidentAI uses PostgreSQL with three main tables.

```
                incidents

                    |
                    |
                    v

              ai_analyses


              chat_history
```

---

## incidents

Stores operational incidents:

```
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

---

## ai_analyses

Stores AI generated investigation reports:

```
id
incident_id
analysis
created_at
```

---

## chat_history

Stores DevOps assistant conversations:

```
id
user_message
ai_response
created_at
```

---

# 🤖 AI Workflow

```
Incident Created

        |
        v

Incident Details

        |
        v

Ollama Local Model

        |
        v

AI Troubleshooting Report

        |
        v

Stored in PostgreSQL
```

---

# 🩺 Health Checks

The application supports health endpoints for monitoring.

## Liveness

```
GET /health
```

Checks whether the application is running.

---

## Readiness

```
GET /ready
```

Checks application dependencies:

```
Application

   |
   +---- PostgreSQL

   |
   +---- Ollama
```

---

# 🔐 Security

Sensitive information should never be committed.

Ignored files:

```
.env
k8s/secrets.yml
```

Use:

```
.env.example
```

as a template.

Secrets should be managed using:

- Kubernetes Secrets
- External secret managers
- Environment injection

---

# 🐳 Docker Development

Run locally:

```bash
docker compose up -d
```

Check containers:

```bash
docker compose ps
```

Stop:

```bash
docker compose down
```

---

# 🛠 Useful Kubernetes Commands

View pods:

```bash
kubectl get pods -n ai-incident-namespace
```

View services:

```bash
kubectl get svc -n ai-incident-namespace
```

View logs:

```bash
kubectl logs <pod-name> -n ai-incident-namespace
```

Enter container:

```bash
kubectl exec -it <pod-name> \
-n ai-incident-namespace -- bash
```

Port forward application:

```bash
kubectl port-forward \
svc/ai-incident-service \
5001:80 \
-n ai-incident-namespace
```

---

# 📈 Engineering Roadmap

## Completed ✅

- Incident management
- PostgreSQL persistence
- AI incident analysis
- DevOps assistant
- Docker containerization
- Kubernetes deployment
- Persistent storage
- ConfigMap integration
- Kubernetes Secrets
- Ollama local inference
- Health probes


---

## Future Improvements 🚧

### CI/CD

- GitHub Actions pipeline
- Automated image builds
- Container security scanning
- Automated Kubernetes deployment


### Observability

- Prometheus metrics
- Grafana dashboards
- Centralized logging
- Distributed tracing


### AI Improvements

- Larger local models
- RAG based incident knowledge
- Historical incident analysis
- Automated remediation suggestions


---

# 🎯 Project Goal

IncidentAI is designed as a practical DevOps engineering project combining:

```
Software Development

        +

Containerization

        +

Kubernetes

        +

Infrastructure Operations

        +

Local Artificial Intelligence
```

---

<div align="center">

# ⚡ IncidentAI

### Track. Investigate. Resolve. Learn.

Built by **Aditya Singh Tomar**

</div>
