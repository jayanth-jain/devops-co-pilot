# 🤖 DevOps Co-Pilot — Autonomous SRE System

> **AI-powered SRE agent for incident analysis, Kubernetes remediation, verification, and automated escalation.**

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Hugging%20Face-yellow)](https://huggingface.co/spaces/MonkJay/DevopsCopilot)
[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-purple)](https://ai.google.dev/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Automation-326CE5?logo=kubernetes)](https://kubernetes.io/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)](https://www.docker.com/)

DevOps Co-Pilot is an **autonomous SRE system** that combines **Gemini 2.5 Flash, local vector RAG, Kubernetes automation, and incident management** to analyze operational incidents, retrieve relevant troubleshooting procedures, execute controlled remediation actions, verify system recovery, and escalate unresolved incidents to Jira.

The goal is simple:

> **Detect → Understand → Remediate → Verify → Escalate**

---

## 🚀 Live Demo

### [▶️ Try DevOps Co-Pilot on Hugging Face](https://huggingface.co/spaces/MonkJay/DevopsCopilot)

The live demo demonstrates the AI-driven incident analysis and remediation workflow.

---

## ✨ Key Capabilities

- 🧠 **AI-Powered Incident Analysis**
  - Uses Gemini 2.5 Flash to analyze incident symptoms and determine likely causes.

- 🔎 **RAG-Powered Troubleshooting**
  - Retrieves relevant operational procedures and SOPs from a local knowledge base.

- 🤖 **Agent-Based Decision Making**
  - Combines incident classification, knowledge retrieval, remediation, and verification into an automated workflow.

- ☸️ **Kubernetes Remediation**
  - Executes controlled Kubernetes recovery actions through operational tools.

- ✅ **Post-Remediation Verification**
  - Checks the resulting system state after a remediation action.

- 🎫 **Jira Escalation**
  - Automatically escalates incidents that cannot be resolved through the automated workflow.

- 🐳 **Containerized Deployment**
  - Designed to run in a Dockerized environment and deployed through Hugging Face Spaces.

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

This process can be time-consuming and inconsistent, especially during repetitive operational incidents.

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
       │ Classification│ │ RAG Knowledge│ │   Incident  │
       │    Agent     │ │    Agent     │ │   Analysis   │
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


🏗️ System Architecture




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




🧰 Technology Stack


| Layer                | Technology                   |
| -------------------- | ---------------------------- |
| Programming Language | Python                       |
| LLM                  | Gemini 2.5 Flash             |
| AI Architecture      | Agent-based orchestration    |
| Knowledge Retrieval  | Local Vector RAG             |
| Database             | PostgreSQL                   |
| Infrastructure       | Kubernetes                   |
| Automation           | kubectl / Kubernetes tooling |
| Incident Management  | Jira                         |
| Containerization     | Docker                       |
| Deployment           | Hugging Face Spaces          |
| Configuration        | Environment Variables        |

             
