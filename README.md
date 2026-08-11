# 🤖 DevOps Co-Pilot — Autonomous SRE System

> **AI-powered SRE agent for incident analysis, Kubernetes remediation, and automated escalation.**

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Hugging%20Face-yellow)](https://huggingface.co/spaces/MonkJay/DevopsCopilot)
[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-purple)](https://ai.google.dev/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Automation-326CE5?logo=kubernetes)](https://kubernetes.io/)

DevOps Co-Pilot is an **autonomous SRE system** that combines **Gemini 2.5 Flash, local vector RAG, and Kubernetes automation** to analyze incidents, retrieve relevant operational procedures, execute remediation actions, and escalate unresolved issues to Jira.

The goal is simple:

**Detect → Understand → Remediate → Verify → Escalate**

---

## 🚀 Live Demo

### [▶️ Try DevOps Co-Pilot on Hugging Face](https://huggingface.co/spaces/MonkJay/DevopsCopilot)

---

## 🏗️ System Architecture

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
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
        ┌──────────────────┐       ┌──────────────────┐
        │   Local Vector   │       │   Incident       │
        │       RAG        │       │   Classification │
        └────────┬─────────┘       └────────┬─────────┘
                 │                          │
                 └────────────┬─────────────┘
                              ▼
                    ┌──────────────────────┐
                    │   Recovery Agent     │
                    │   SOP → Remediation  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Kubernetes Actions   │
                    │     kubectl patch     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ State Verification   │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                 Resolved              Unresolved
                    │                     │
                    ▼                     ▼
              ✅ Close Incident     🎫 Jira Escalation
