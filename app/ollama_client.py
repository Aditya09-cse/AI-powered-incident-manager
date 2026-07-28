import os

import requests
from dotenv import load_dotenv


load_dotenv()


OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434"
).rstrip("/")

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2:3b"
)


def generate(prompt):
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=180,
    )

    response.raise_for_status()

    data = response.json()

    return data.get(
        "response",
        "No response returned by Ollama."
    ).strip()


def analyze_incident(incident):
    prompt = f"""
You are an experienced DevOps and Site Reliability Engineer.

Analyze the following infrastructure incident.

Incident ID:
INC-{incident['id']:04d}

Title:
{incident['title']}

Category:
{incident['category']}

Severity:
{incident['severity']}

Description:
{incident['description']}

Provide a practical analysis using exactly these sections:

SUMMARY
Briefly explain what may be happening.

LIKELY ROOT CAUSES
List the most likely causes.

TROUBLESHOOTING STEPS
Give ordered troubleshooting steps.

COMMANDS
Provide useful Linux, Docker, Kubernetes, AWS,
networking, database, or application commands where relevant.

RECOMMENDED FIX
Explain the most likely fix.

PREVENTION
Explain how this could be prevented in the future.

Do not claim that a root cause is confirmed unless the incident
description provides enough evidence.
"""

    return generate(prompt)


def ask_assistant(message):
    prompt = f"""
You are DevOps AI Assistant, an experienced DevOps/SRE engineer.

You help engineers troubleshoot:

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
- networking
- monitoring
- application deployments

Give practical answers.

When troubleshooting:
1. Explain what the problem probably means.
2. Give troubleshooting steps.
3. Include useful commands when appropriate.
4. Explain what the commands are checking.
5. Never pretend a diagnosis is confirmed without evidence.

User question:

{message}
"""

    return generate(prompt)


def ollama_health():
    try:
        response = requests.get(
            f"{OLLAMA_URL}/api/tags",
            timeout=3,
        )

        return response.ok

    except requests.RequestException:
        return False