<div align="center">

# ⚡ IncidentAI

### AI-Powered Incident Management & DevOps Troubleshooting

Track incidents. Investigate failures. Get AI-assisted troubleshooting.  
All inside a self-hosted, containerized environment.

<br>

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local_AI-111111?style=for-the-badge)

</div>

---

## What is IncidentAI?

IncidentAI is a **self-hosted DevOps incident management platform** that combines traditional incident tracking with local AI-assisted troubleshooting.

Instead of only recording:

> "Docker container keeps restarting"

IncidentAI lets you track that incident through its lifecycle and use a locally running LLM to help investigate **why it is happening and what to check next**.

```text
Report Incident
      │
      ▼
Classify & Track
      │
      ▼
Investigate
      │
      ├───────────────┐
      ▼               ▼
Incident Data      Ollama AI
      │               │
      ▼               ▼
 PostgreSQL      Troubleshooting
      │               │
      └───────┬───────┘
              ▼
           Resolve
```

No external AI API is required.

---

## ✨ What You Can Do

<table>
<tr>
<td width="50%">

### 🚨 Manage Incidents

Create incidents with:

- Title & description
- Category
- Severity
- Operational status

Track them through:

`Open → Investigating → Resolved`

</td>

<td width="50%">

### 🤖 Analyze with AI

Send an incident to Ollama and receive:

- Incident summary
- Possible root causes
- Troubleshooting steps
- Useful commands
- Recommended fixes
- Prevention suggestions

</td>
</tr>

<tr>
<td>

### 📊 Monitor Operations

The dashboard provides visibility into:

- Total incidents
- Open incidents
- Investigations
- Resolved incidents
- Critical incidents
- Recent activity

</td>

<td>

### 🧠 Ask the DevOps Assistant

Use the standalone AI assistant for troubleshooting:

`Linux` · `Docker` · `Kubernetes` · `AWS`  
`CI/CD` · `Terraform` · `Networking` · `PostgreSQL`

Chat history is persisted in PostgreSQL.

</td>
</tr>
</table>

---

# 🏗 Architecture

```text
                         ┌──────────────────────┐
                         │        USER          │
                         │       Browser        │
                         └──────────┬───────────┘
                                    │
                                    │ :5001
                                    ▼
                    ┌───────────────────────────────┐
                    │          IncidentAI           │
                    │                               │
                    │       Flask + Gunicorn        │
                    │                               │
                    │  ┌─────────┐   ┌───────────┐  │
                    │  │Dashboard│   │ Incidents │  │
                    │  └─────────┘   └───────────┘  │
                    │                               │
                    │  ┌─────────┐   ┌───────────┐  │
                    │  │ History │   │AI Assistant│ │
                    │  └─────────┘   └───────────┘  │
                    └───────────────┬───────────────┘
                                    │
                             Docker Network
                                    │
                     ┌──────────────┴──────────────┐
                     │                             │
                     ▼                             ▼
           ┌───────────────────┐         ┌───────────────────┐
           │    PostgreSQL     │         │      Ollama       │
           │                   │         │                   │
           │    Incidents      │         │    Llama 3.2      │
           │    AI Analysis    │         │                   │
           │    Chat History   │         │  Local Inference  │
           └─────────┬─────────┘         └─────────┬─────────┘
                     │                             │
                     ▼                             ▼
              postgres-data                  ollama-data
               Docker Volume                  Docker Volume
```

The services communicate through a private Docker bridge network.

```text
IncidentAI ──────► postgres:5432
     │
     └───────────► ollama:11434
```

PostgreSQL and Ollama do not need to be exposed directly to the host.

---

# 🧩 System Components

| Component | Role |
|---|---|
| **Flask** | Application backend and routing |
| **Gunicorn** | WSGI application server |
| **PostgreSQL** | Persistent incident, analysis and chat storage |
| **Ollama** | Local LLM inference service |
| **Llama 3.2** | DevOps troubleshooting model |
| **Docker** | Application containerization |
| **Docker Compose** | Multi-container service orchestration |
| **Docker Volumes** | Persistent database and model storage |

---

# 🔥 Incident Workflow

An incident begins as:

```text
OPEN
```

and progresses through:

```text
┌──────────────┐
│     OPEN     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│INVESTIGATING │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   RESOLVED   │
└──────────────┘
```

Incident records remain available after resolution, providing a searchable history of previous operational problems.

---

# 🤖 AI Incident Analysis

AI analysis is attached directly to an incident.

For example:

```text
Incident
────────────────────────────────────

Title:
Docker container continuously restarting

Category:
Docker

Severity:
High

Description:
Container exits several seconds after startup.
```

IncidentAI sends the incident context to Ollama and asks for structured troubleshooting guidance:

```text
AI Analysis
────────────────────────────────────

SUMMARY
The application process is terminating after startup.

LIKELY CAUSES
• Invalid startup command
• Missing environment variable
• Dependency failure
• Database connection failure

TROUBLESHOOTING
1. Inspect container logs
2. Check container exit code
3. Inspect environment configuration
4. Verify dependent services

COMMANDS
docker logs <container>
docker inspect <container>
docker compose ps

PREVENTION
Add health checks and validate required configuration
before application startup.
```

AI analyses are stored in PostgreSQL so they remain associated with the incident.

---

# 🗄️ Data Model

IncidentAI stores three main types of data.

```text
┌─────────────────────┐
│      incidents      │
├─────────────────────┤
│ id                  │
│ title               │
│ description         │
│ category            │
│ severity            │
│ status              │
│ created_at          │
│ updated_at          │
│ resolved_at         │
└──────────┬──────────┘
           │
           │ 1 : N
           ▼
┌─────────────────────┐
│    ai_analyses      │
├─────────────────────┤
│ id                  │
│ incident_id         │
│ analysis            │
│ created_at          │
└─────────────────────┘


┌─────────────────────┐
│    chat_history     │
├─────────────────────┤
│ id                  │
│ user_message        │
│ ai_response         │
│ created_at          │
└─────────────────────┘
```

---

# 📁 Repository Structure

```text
AI-powered-incident-manager
│
├── app
│   ├── app.py
│   ├── db.py
│   ├── ollama_client.py
│   ├── requirements.txt
│   │
│   ├── static
│   │   ├── app.js
│   │   └── style.css
│   │
│   └── templates
│       ├── assistant.html
│       ├── base.html
│       ├── dashboard.html
│       ├── history.html
│       ├── incident.html
│       ├── incidents.html
│       └── index.html
│
├── database
│   └── init.sql
│
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

# 🚀 Run IncidentAI

## 1. Clone

```bash
git clone https://github.com/Aditya09-cse/AI-powered-incident-manager.git

cd AI-powered-incident-manager
```

## 2. Configure

Create your local environment file:

```bash
cp .env.example .env
```

Configure:

```env
DB_NAME=incident_manager
DB_USER=incident_user
DB_PASSWORD=your_secure_password

FLASK_HOST=0.0.0.0
FLASK_PORT=5001

OLLAMA_URL=http://ollama:11434
OLLAMA_MODEL=llama3.2:1b
```

`.env` is intentionally excluded from Git.

## 3. Start the Stack

```bash
docker compose up -d
```

Verify:

```bash
docker compose ps
```

You should have:

```text
devops-ai-app
devops-ai-postgres
devops-ai-ollama
```

## 4. Pull the AI Model

Ollama does not download a model automatically.

```bash
docker exec -it devops-ai-ollama \
  ollama pull llama3.2:1b
```

Verify:

```bash
docker exec devops-ai-ollama ollama list
```

## 5. Open

```text
http://localhost:5001
```

That's it.

---

# 🩺 Health, Readiness & Metrics

IncidentAI exposes operational endpoints that can later integrate with monitoring systems and container orchestrators.

### Liveness

```bash
curl http://localhost:5001/health
```

### Readiness

```bash
curl http://localhost:5001/ready
```

Readiness checks the application's dependencies:

```text
Application
    │
    ├── PostgreSQL  ✓
    │
    └── Ollama      ✓
```

If required dependencies are unavailable, the endpoint returns an unhealthy readiness response.

### Metrics

```bash
curl http://localhost:5001/metrics
```

Currently exposed incident metrics include:

```text
incidents_total
incidents_open
incidents_investigating
incidents_resolved
```

These are exposed in Prometheus-compatible text format.

---

# 🐳 Container Design

The application is served using **Gunicorn**, rather than Flask's development server.

```text
Container
   │
   ▼
Gunicorn
   │
   ├── Worker
   └── Worker
         │
         ▼
       Flask
```

The application container also runs using a dedicated **non-root user**.

Persistent state is kept outside containers:

```text
PostgreSQL Container
        │
        ▼
  postgres-data


Ollama Container
        │
        ▼
    ollama-data
```

This allows containers to be recreated without losing incident records or downloaded models.

---

# 🔐 Configuration & Secrets

Real credentials belong in:

```text
.env
```

The repository contains:

```text
.env.example
```

only as a configuration template.

Never commit:

- Database passwords
- API keys
- Cloud credentials
- Access tokens
- Private keys

---

# 🛠 Useful Commands

```bash
# Start
docker compose up -d

# Check services
docker compose ps

# Application logs
docker logs -f devops-ai-app

# Ollama logs
docker logs -f devops-ai-ollama

# Database logs
docker logs -f devops-ai-postgres

# Installed AI models
docker exec devops-ai-ollama ollama list

# Stop
docker compose down
```

Avoid:

```bash
docker compose down -v
```

unless you intentionally want to remove persistent database and Ollama volumes.

---

# 🧪 Built for DevOps Experimentation

IncidentAI is intentionally designed as more than a CRUD application.

Its architecture provides a practical workload for applying DevOps concepts around a real system:

```text
                    IncidentAI
                        │
          ┌─────────────┼─────────────┐
          │             │             │
     Application    PostgreSQL      Ollama
          │             │             │
          └─────────────┼─────────────┘
                        │
                     Docker
                        │
                 Docker Compose
```

This provides a foundation for future work involving CI/CD, container security, Kubernetes, observability, and infrastructure automation without claiming those capabilities are already implemented.

---

# 📍 Current Status

**Working**

`Incident Management` · `PostgreSQL Persistence` · `Incident History`  
`AI Incident Analysis` · `DevOps AI Assistant` · `Docker`  
`Docker Compose` · `Gunicorn` · `Health Checks` · `Metrics`

**Next engineering milestone**

CI/CD and DevSecOps automation.

---

<div align="center">

## IncidentAI

**Track. Investigate. Resolve. Learn.**

Built by **Aditya Singh Tomar**

</div>
