# 🚀 DevOps Co-Pilot: Multi-Agent SRE System

**Autonomous Agentic Framework for Automated Incident Remediation.** *Built for Google Gen AI Academy APAC Hackathon.*

---

## 🏗️ Technical Architecture Matrix
| Layer | Technology | Implementation Detail |
| :--- | :--- | :--- |
| **Orchestrator** | Gemini 1.5 Pro | Multi-step reasoning & intent classification. |
| **Knowledge Base** | AlloyDB + pgvector | Semantic RAG using `google_ml.embedding`. |
| **Recovery Agent** | Gemini 1.5 Flash | Real-time SOP synthesis & remediation scripts. |
| **Runtime** | Google Cloud Run | Serverless scaling with Startup CPU Boost. |

---

## 🤖 Multi-Agent Workflow Logic
1. **The Orchestrator:** Parses natural language into metadata and severity tiers.
2. **The Librarian:** Executes semantic retrieval of internal SOPs using `text-embedding-004`.
3. **The Recovery Agent:** Fuses context with live diagnostics for non-hallucinated plans.
4. **The Executor:** Simulates remediation and auto-escalates to Jira if unstable.

---

## 🔗 Live Submission Assets
* **Live App URL:** [https://devops-copilot-977439299115.us-central1.run.app](https://devops-copilot-977439299115.us-central1.run.app)
* **GitHub Repository:** [https://github.com/jayanth-jain/devops-co-pilot](https://github.com/jayanth-jain/devops-co-pilot)
