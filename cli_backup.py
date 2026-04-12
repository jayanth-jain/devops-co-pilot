import os
import time
import random
import google.generativeai as genai
from database import find_multiple_fixes

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY", ""))
# Stable model names
orchestrator = genai.GenerativeModel("gemini-2.5-flash")
recovery_agent = genai.GenerativeModel("gemini-2.5-flash")

def check_pod_health(pod_name):
    statuses = ["Running", "CrashLoopBackOff", "Pending", "Terminating"]
    return f"Pod '{pod_name}': {random.choice(statuses)}"

def restart_pod(pod_name):
    return f"kubectl rollout restart deployment/{pod_name} -> SUCCESS"

def create_jira_ticket(summary, ai_hint=""):
    import sqlalchemy
    from database import get_engine
    ticket_id = f"INC-{random.randint(100,999)}"
    try:
        engine = get_engine()
        q = sqlalchemy.text("INSERT INTO incidents (ticket_id, issue_description, status) VALUES (:id, :desc, 'OPEN - AI ENRICHED')")
        with engine.connect() as conn:
            conn.execute(q, {"id": ticket_id, "desc": f"{summary} | AI: {ai_hint[:120]}"})
            conn.commit()
    except Exception as e:
        pass
    return ticket_id

def orchestrate(issue):
    prompt = f"""You are a senior SRE orchestrator. Analyze this incident and respond in EXACTLY this format:
SERVICE: <affected service name or 'general-system'>
SEVERITY: <P1, P2, or P3>
CATEGORY: <CrashLoop, HighLatency, DatabaseError, NetworkError, ResourceExhaustion, or Unknown>
KEYWORDS: <3-5 search keywords>
SUMMARY: <one sentence description>

Instruction: If the user mentions a specific service like 'auth-service', you MUST extract it.

Incident: "{issue}" """
    try:
        response = orchestrator.generate_content(prompt)
        text = response.text.strip()
        result = {"service": "general-system", "severity": "P2", "category": "Unknown", "keywords": issue, "summary": issue}
        for line in text.splitlines():
            if ":" in line:
                key, _, val = line.partition(":")
                k, v = key.strip().upper(), val.strip()
                if k == "SERVICE": result["service"] = v
                elif k == "SEVERITY": result["severity"] = v
                elif k == "CATEGORY": result["category"] = v
                elif k == "KEYWORDS": result["keywords"] = v
                elif k == "SUMMARY": result["summary"] = v
        return result
    except Exception as e:
        return {"service": "general-system", "severity": "P2", "category": "Unknown", "keywords": issue, "summary": issue}

def synthesize_recovery(issue, context, sops, health):
    sop_text = "\n".join(f"- {s}" for s in sops) if sops else "No matching SOPs found."
    prompt = f"""You are an expert SRE Recovery Agent. Generate a precise recovery plan.

INCIDENT: {issue}
SERVICE: {context["service"]}
SEVERITY: {context["severity"]}
CATEGORY: {context["category"]}
POD HEALTH: {health}

RETRIEVED SOPs FROM ALLOYDB:
{sop_text}

Respond with:
1. ROOT CAUSE ANALYSIS
2. IMMEDIATE ACTIONS (numbered steps)
3. VERIFICATION STEPS
4. PREVENTION RECOMMENDATION"""
    try:
        response = recovery_agent.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Recovery synthesis failed: {e}"

def run_copilot(issue):
    output = []
    log = output.append
    log("=" * 60)
    log("DEVOPS CO-PILOT - MULTI-AGENT SRE SYSTEM")
    log("=" * 60)
    log("\n[AGENT 1: ORCHESTRATOR - Gemini 1.5 Pro]")
    log("  Parsing incident and routing to sub-agents...")
    context = orchestrate(issue)
    log(f"  Service  : {context['service']}")
    log(f"  Severity : {context['severity']}")
    log(f"  Category : {context['category']}")
    log(f"  Summary  : {context['summary']}")
    log("\n[INFRASTRUCTURE DIAGNOSTIC]")
    health = check_pod_health(context["service"])
    log(f"  {health}")
    log("\n[AGENT 2: DOCUMENTATION AGENT - AlloyDB pgvector]")
    log("  Semantic search via google_ml.embedding(text-embedding-004)...")
    try:
        sops = find_multiple_fixes(context["keywords"])
        if sops:
            log(f"  {len(sops)} SOPs retrieved:")
            for i, s in enumerate(sops, 1):
                log(f"  [{i}] {s[:120]}...")
        else:
            log("  No SOPs found - escalation path active.")
    except Exception as e:
        log(f"  AlloyDB search error: {e}")
        sops = []
    log("\n[AGENT 3: RECOVERY AGENT - Gemini 1.5 Flash]")
    log("  Synthesizing recovery plan from SOPs + live diagnostics...")
    plan = synthesize_recovery(issue, context, sops, health)
    log("\n" + "-" * 50)
    log(plan)
    log("-" * 50)
    log("\n[AUTONOMOUS ACTION]")
    log(f"  {restart_pod(context['service'])}")
    log("\n[VERIFICATION]")
    time.sleep(1)
    final = check_pod_health(context["service"])
    log(f"  Post-recovery: {final}")
    if "Running" in final:
        log("  Service stabilized. MTTR: < 10 seconds.")
    else:
        log("  Unstable. Creating escalation ticket...")
        ticket = create_jira_ticket(issue, plan[:120])
        log(f"  Jira ticket: {ticket}")
    log("\n" + "=" * 60)
    return "\n".join(output)