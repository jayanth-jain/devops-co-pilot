Yes. Paste this as your **entire `README.md`**. I’ve kept the claims aligned with the README content you provided and removed the review/commentary text that accidentally got appended.

````markdown
# 🤖 DevOps Co-Pilot — Autonomous SRE System

> **AI-powered SRE agent for incident analysis, Kubernetes remediation, verification, and automated escalation.**

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Hugging%20Face-yellow)](https://huggingface.co/spaces/MonkJay/DevopsCopilot)
[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-purple)](https://ai.google.dev/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Automation-326CE5?logo=kubernetes)](https://kubernetes.io/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)](https://www.docker.com/)

DevOps Co-Pilot is an **autonomous SRE system** that combines **Gemini 2.5 Flash, Retrieval-Augmented Generation (RAG), Kubernetes automation, and incident management** to analyze operational incidents, retrieve relevant troubleshooting procedures, execute controlled remediation actions, verify system recovery, and escalate unresolved incidents to Jira.

The goal is simple:

> **Detect → Understand → Remediate → Verify → Escalate**

---

## 🚀 Live Demo

### [▶️ Try DevOps Co-Pilot on Hugging Face](https://huggingface.co/spaces/MonkJay/DevopsCopilot)

Experience the AI-driven incident analysis and remediation workflow through the live demo.

---

## ✨ Key Capabilities

- 🧠 **AI-Powered Incident Analysis**
  - Uses Gemini 2.5 Flash to analyze incident symptoms and determine likely causes.

- 🔎 **RAG-Powered Troubleshooting**
  - Retrieves relevant operational procedures and SOPs from the knowledge base.

- 🤖 **Agent-Based Decision Making**
  - Combines incident analysis, knowledge retrieval, remediation, and verification into an automated workflow.

- ☸️ **Kubernetes Remediation**
  - Executes controlled Kubernetes recovery actions through operational tools.

- ✅ **Post-Remediation Verification**
  - Checks the resulting system state after a remediation action.

- 🎫 **Jira Escalation**
  - Escalates unresolved incidents for human intervention.

- 🐳 **Containerized Deployment**
  - Supports Docker-based deployment and is deployed through Hugging Face Spaces.

---

## 🎯 Problem Statement

Traditional SRE incident response often requires engineers to manually:

1. Investigate the alert.
2. Inspect application and infrastructure state.
3. Search runbooks or SOPs.
4. Identify the likely root cause.
5. Execute recovery commands.
6. Verify that the system has recovered.
7. Escalate the incident if recovery fails.

This process can be time-consuming and repetitive.

DevOps Co-Pilot automates this workflow by combining:

**LLM reasoning + operational knowledge + infrastructure tools + verification + escalation**

---

## 🔄 Incident Response Workflow

```text
                    ┌──────────────────────┐
                    │   Incident / Alert   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   AI Orchestrator    │
                    │   Gemini 2.5 Flash   │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
       │ Classification│ │ RAG Knowledge│ │   Incident   │
       │    Agent     │ │    Agent     │ │   Analysis    │
       └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
              │                │                │
              └────────────────┼────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Recovery Agent     │
                    │    SOP → Action      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Kubernetes Automation│
                    │      kubectl         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  State Verification  │
                    │  Health / Pod State  │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
              ┌───────────┐        ┌──────────────┐
              │  RESOLVED │        │  UNRESOLVED  │
              └─────┬─────┘        └──────┬───────┘
                    │                     │
                    ▼                     ▼
             ✅ Close Incident       🎫 Jira Escalation
````

---

## 🏗️ System Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                     DEVOPS CO-PILOT                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐                                           │
│  │ User / Alert │                                           │
│  └──────┬───────┘                                           │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────────────┐                                   │
│  │   AI Orchestrator    │                                   │
│  │   Gemini 2.5 Flash   │                                   │
│  └──────────┬───────────┘                                   │
│             │                                               │
│     ┌───────┼────────┬──────────────┐                       │
│     ▼       ▼        ▼              ▼                       │
│  ┌──────┐ ┌──────┐ ┌──────────┐ ┌───────────┐              │
│  │ RAG  │ │Class.│ │ Recovery │ │  Tools    │              │
│  │Agent │ │Agent │ │  Agent   │ │  Layer    │              │
│  └──┬───┘ └──┬───┘ └────┬─────┘ └─────┬─────┘              │
│     │         │          │              │                   │
│     ▼         │          ▼              ▼                   │
│  ┌──────────┐ │   ┌────────────┐  ┌──────────────┐          │
│  │Knowledge │ │   │    SOP     │  │ Kubernetes   │          │
│  │  Base    │ │   │ Procedures │  │   Actions    │          │
│  └──────────┘ │   └────────────┘  └──────┬───────┘          │
│                │                         │                  │
│                └────────────┬────────────┘                  │
│                             ▼                               │
│                    ┌──────────────────┐                      │
│                    │    Verification  │                      │
│                    └────────┬─────────┘                      │
│                             │                               │
│                    ┌────────┴─────────┐                      │
│                    ▼                  ▼                      │
│              ┌──────────┐       ┌──────────┐                │
│              │ Resolved │       │  Jira    │                │
│              │ Incident │       │Escalation│                │
│              └──────────┘       └──────────┘                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧰 Technology Stack

| Layer                | Technology                           |
| -------------------- | ------------------------------------ |
| Programming Language | Python                               |
| LLM                  | Gemini 2.5 Flash                     |
| AI Architecture      | Agent-based orchestration            |
| Knowledge Retrieval  | Retrieval-Augmented Generation (RAG) |
| Database             | PostgreSQL                           |
| Infrastructure       | Kubernetes                           |
| Automation           | kubectl / Kubernetes tooling         |
| Incident Management  | Jira                                 |
| Containerization     | Docker                               |
| Deployment           | Hugging Face Spaces                  |
| Configuration        | Environment Variables                |

---

## 🧠 AI & RAG Pipeline

The system combines LLM reasoning with operational knowledge to provide incident-specific context.

```text
Incident
   │
   ▼
Incident Classification
   │
   ▼
Knowledge Retrieval
   │
   ▼
Relevant SOP / Operational Context
   │
   ▼
Gemini 2.5 Flash
   │
   ▼
Recovery Decision
   │
   ▼
Controlled Tool Execution
   │
   ▼
Verification
   │
   ▼
Resolved / Escalated
```

The knowledge base can contain operational information such as:

* Troubleshooting procedures
* Recovery procedures
* Known failure patterns
* Operational runbooks
* Kubernetes recovery guidance

---

## ☸️ Kubernetes Remediation

DevOps Co-Pilot is designed to go beyond simply recommending a recovery command.

The remediation workflow follows:

```text
Incident
   ↓
Analyze
   ↓
Retrieve operational procedure
   ↓
Select remediation
   ↓
Execute Kubernetes action
   ↓
Observe resulting state
   ↓
Verify recovery
```

This creates a closed-loop operational workflow:

```text
AI Decision
    ↓
Infrastructure Action
    ↓
System State
    ↓
Verification
    ↓
Resolution / Escalation
```

---

## 🎫 Automated Jira Escalation

When automated remediation cannot restore the expected system state, the incident is escalated for human intervention.

```text
              Remediation
                   │
                   ▼
             Verification
                   │
          ┌────────┴────────┐
          │                 │
          ▼                 ▼
       Healthy          Unhealthy
          │                 │
          ▼                 ▼
      Resolved        Jira Escalation
```

This provides a clear fallback:

> **Autonomous remediation → Verification → Human escalation**

---

## 🔐 Safety & Guardrails

Infrastructure automation requires controlled execution.

DevOps Co-Pilot follows these principles:

* Remediation actions should be based on defined operational procedures.
* Infrastructure operations are executed through controlled tools.
* The system verifies the result after remediation.
* Failed remediation is escalated rather than repeatedly attempting recovery.
* Credentials should be supplied through environment variables.
* Secrets and API keys should never be committed to the repository.
* Production deployments should use least-privilege Kubernetes permissions.

> **The goal is controlled AI-driven infrastructure automation, not unrestricted AI access to production systems.**

---

## 📁 Project Structure

```text
devops-co-pilot/
│
├── app.py
│   └── Application entry point
│
├── agent_engine.py
│   └── AI agent orchestration and reasoning
│
├── tools.py
│   └── Operational and infrastructure tools
│
├── database.py
│   └── Database and knowledge retrieval operations
│
├── gui.py
│   └── User interface
│
├── knowledge_base.sql
│   └── Operational knowledge and SOP data
│
├── requirements.txt
│   └── Python dependencies
│
├── Dockerfile
│   └── Container configuration
│
├── Procfile
│   └── Deployment configuration
│
├── .gitignore
│   └── Git exclusions
│
└── README.md
    └── Project documentation
```

---

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/jayanth-jain/devops-co-pilot.git
cd devops-co-pilot
```

### 2. Create a virtual environment

#### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

#### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file with the credentials required by the application.

Example:

```env
GEMINI_API_KEY=your_gemini_api_key

JIRA_URL=your_jira_url
JIRA_EMAIL=your_jira_email
JIRA_API_TOKEN=your_jira_api_token

DATABASE_URL=your_database_url
```

> Use the exact environment variable names expected by the application.

### 5. Start the application

```bash
python app.py
```

---

## 🐳 Docker

Build the Docker image:

```bash
docker build -t devops-co-pilot .
```

Run the container:

```bash
docker run --env-file .env -p 7860:7860 devops-co-pilot
```

---

## 🧪 Example Incident

### Scenario

```text
Application pod enters CrashLoopBackOff.
```

### Automated workflow

```text
🔍 Incident detected
        │
        ▼
🧠 Incident analyzed
        │
        ▼
🔎 Relevant operational procedure retrieved
        │
        ▼
🛠️ Remediation selected
        │
        ▼
☸️ Kubernetes action executed
        │
        ▼
🔍 System state verified
        │
        ▼
     ┌──┴──┐
     │     │
     ▼     ▼
  Healthy Failed
     │     │
     ▼     ▼
 Resolved Jira
          Escalation
```

### Example result

```text
Incident:     Pod health failure
Analysis:     Completed
Remediation:  Executed
Verification: Passed
Status:       Resolved
Escalation:   Not required
```

---

## 💡 Why This Project?

SRE teams spend significant time handling repetitive operational incidents.

Many incidents follow predictable patterns:

```text
Alert
  ↓
Diagnosis
  ↓
Runbook lookup
  ↓
Known remediation
  ↓
Verification
```

DevOps Co-Pilot attempts to automate this workflow while maintaining a verification and escalation path.

The project combines:

* Artificial Intelligence
* LLM Agents
* Retrieval-Augmented Generation
* Kubernetes
* Infrastructure Automation
* Incident Management
* DevOps
* SRE practices

---

## 📊 Engineering Goals

### 1. Reduce Mean Time to Recovery

Automate repetitive investigation and recovery procedures.

### 2. Make Operational Knowledge Actionable

Use runbooks and SOPs as contextual knowledge during incident analysis.

### 3. Close the Automation Loop

Instead of stopping at:

```text
AI → Recommendation
```

the goal is:

```text
AI → Action → Verification → Decision
```

### 4. Provide a Human Escalation Path

When automation cannot safely resolve an incident:

```text
Agent
  ↓
Failed Recovery
  ↓
Jira
  ↓
Human SRE
```

---

## 📈 Evaluation

An autonomous SRE system should be evaluated using operational metrics rather than only LLM response quality.

| Metric                   | Description                                                      |
| ------------------------ | ---------------------------------------------------------------- |
| Remediation Success Rate | Percentage of incidents successfully resolved                    |
| MTTR                     | Mean time to recovery                                            |
| Tool Selection Accuracy  | Correctness of selected remediation tool                         |
| RAG Retrieval Quality    | Relevance of retrieved operational procedures                    |
| Verification Accuracy    | Ability to correctly determine recovery                          |
| Escalation Accuracy      | Correct identification of incidents requiring human intervention |
| Agent Latency            | Time from incident to remediation decision                       |

These metrics provide a framework for evaluating the system as an engineering platform.

---

## 🔭 Future Improvements

* 📊 Prometheus and Grafana integration
* 🔔 Alertmanager integration
* 🧠 Advanced multi-agent orchestration
* 🔐 Role-based Kubernetes permissions
* 🛡️ Approval gates for high-risk remediation
* 📈 Incident and remediation metrics
* 🧪 Automated incident simulation
* 🔄 Retry and rollback strategies
* 📝 Automated post-incident reports
* 🔍 Distributed tracing integration
* 🚨 Real-time alert ingestion
* 📦 Kubernetes-native deployment
* 🔬 Agent evaluation and benchmarking

---

## 🗺️ Roadmap

```text
[x] Gemini-powered incident analysis
[x] RAG knowledge retrieval
[x] Kubernetes remediation workflow
[x] Incident verification
[x] Jira escalation
[x] Docker deployment
[x] Hugging Face demo

[ ] Prometheus integration
[ ] Alertmanager integration
[ ] Automated evaluation suite
[ ] Incident simulation framework
[ ] Observability dashboard
[ ] Advanced safety / approval gates
[ ] Kubernetes-native deployment
```

---

## 🔒 Security Considerations

Never commit credentials or API keys to the repository.

Use environment variables or a dedicated secrets manager for:

```text
GEMINI_API_KEY
JIRA_API_TOKEN
DATABASE_CREDENTIALS
KUBERNETES_CREDENTIALS
```

For production environments:

* Follow the principle of least privilege.
* Restrict Kubernetes permissions to required resources.
* Avoid unrestricted shell execution.
* Add approval gates for destructive operations.
* Store secrets outside source control.
* Audit remediation actions.

---

## 🧑‍💻 Author

### Jayanth Jain

**Linux Administrator → AI Agent Developer**

Areas of interest:

* AI Agents
* SRE Automation
* Kubernetes
* DevOps
* MLOps
* RAG Systems
* LLM Applications

---

## 🔗 Links

**GitHub Repository**

[https://github.com/jayanth-jain/devops-co-pilot](https://github.com/jayanth-jain/devops-co-pilot)

**Live Demo**

[https://huggingface.co/spaces/MonkJay/DevopsCopilot](https://huggingface.co/spaces/MonkJay/DevopsCopilot)

---

## ⭐ DevOps Co-Pilot

```text
        DETECT
           │
           ▼
       UNDERSTAND
           │
           ▼
        RETRIEVE
           │
           ▼
       REMEDIATE
           │
           ▼
         VERIFY
           │
     ┌─────┴─────┐
     ▼           ▼
 RESOLVED       FAILED
     │           │
     ▼           ▼
   CLOSE       JIRA
              ESCALATION
```


