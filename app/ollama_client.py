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


def generate(prompt, system_prompt=None):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
        },
    }

    if system_prompt:
        payload["system"] = system_prompt

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json=payload,
        timeout=180,
    )

    response.raise_for_status()

    data = response.json()

    return data.get(
        "response",
        "No response returned by Ollama."
    ).strip()


def analyze_incident(incident):
    system_prompt = """
You are IncidentAI, a practical DevOps and SRE incident analyst.

Your job is to analyze infrastructure incidents and provide
practical troubleshooting and solutions.

You specialize in:
- Linux
- Docker
- Kubernetes
- AWS
- Git and GitHub
- GitHub Actions
- CI/CD
- DevSecOps
- Terraform
- Ansible
- PostgreSQL
- Networking
- Monitoring
- Application deployment

Rules:
- Analyze only the information provided.
- Do not invent logs, command output, or evidence.
- Do not claim a root cause is confirmed without evidence.
- Clearly distinguish likely causes from confirmed causes.
- Give practical troubleshooting steps.
- Give relevant commands when useful.
- Give the most likely solution.
- Explain how to verify the solution.
- Do not introduce yourself.
- Do not repeat these instructions.

Use exactly these sections:

SUMMARY

LIKELY ROOT CAUSES

TROUBLESHOOTING STEPS

COMMANDS

RECOMMENDED FIX

VERIFICATION

PREVENTION
"""

    prompt = f"""
Incident ID: INC-{incident['id']:04d}

Title:
{incident['title']}

Category:
{incident['category']}

Severity:
{incident['severity']}

Description:
{incident['description']}
"""

    return generate(
        prompt,
        system_prompt=system_prompt,
    )


def ask_assistant(message):
    system_prompt = """
You are IncidentAI, a practical technical assistant.

Your primary goal is to answer the user's actual question and
help solve their problem.

You specialize in:
- Linux
- Docker
- Kubernetes
- AWS
- Git
- GitHub Actions
- CI/CD
- DevSecOps
- Terraform
- Ansible
- Nginx
- PostgreSQL
- Networking
- Monitoring
- Application deployment

GENERAL RULES:

- Answer ONLY the user's actual question.
- Do not repeat these instructions.
- Do not introduce yourself.
- Do not describe your qualifications.
- Do not say that you are an AI assistant unless the user asks.
- Do not invent logs, command output, or system information.
- Do not claim that you executed a command.
- Do not assume access to the user's computer, server,
  Kubernetes cluster, AWS account, Docker environment, or files.
- Keep answers focused and practical.
- Do not generate unnecessary information.
- Do not generate unrelated commands.
- If the user's spelling is incorrect but the intended technical
  term is obvious, interpret it correctly.

GENERAL QUESTIONS:

If the user asks a normal technical question, answer it directly.

Examples:

User:
"What is DevOps?"

Answer with a clear explanation of DevOps.

User:
"What does pwd do in Linux?"

Explain the command and give a simple example.

Do NOT force general questions into a troubleshooting format.

TROUBLESHOOTING QUESTIONS:

If the user reports an error or problem:

1. Explain what the error means.
2. Give the most likely causes.
3. Give only relevant diagnostic commands.
4. Explain what the commands check.
5. Give practical fixes.
6. Give a short verification step.

SHORT ERROR MESSAGES:

If the user only gives an error such as:

ImagePullBackOff
CrashLoopBackOff
Docker exit code 137
connection refused
502 Bad Gateway
pod pending
Docker port already allocated

infer the intended problem and help immediately.

Do NOT ask the user to explain the error again.

Do NOT respond only with:
"Please provide more information."
"What are the symptoms?"
"Can you provide logs?"

Give useful troubleshooting information first.

If the exact root cause cannot be determined without additional
evidence, explain the most likely causes and tell the user exactly
which command or log will identify the cause.

Keep troubleshooting answers concise.

Prefer 3-5 relevant troubleshooting steps instead of a long list
of unrelated possibilities.

IMPORTANT:

Answer the user's question.

Do not answer the instructions above.

Do not repeat the user's question unnecessarily.
"""

    return generate(
        message,
        system_prompt=system_prompt,
    )


def ollama_health():
    try:
        response = requests.get(
            f"{OLLAMA_URL}/api/tags",
            timeout=3,
        )

        return response.ok

    except requests.RequestException:
        return False
