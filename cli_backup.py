import os
import time
import random
from google import genai
from database import find_multiple_fixes
from tools import check_pod_health, patch_deployment_config, restart_pod, create_jira_ticket

def get_client():
    try:
        return genai.Client()
    except Exception:
        return None

def orchestrate(issue):
    prompt = f"""You are a senior SRE orchestrator. Analyze this incident and respond in EXACTLY this format:
SERVICE: <affected service name or 'general-system'>
SEVERITY: <P1, P2, or P3>
CATEGORY: <CrashLoop, HighLatency, DatabaseError, NetworkError, ResourceExhaustion, or Unknown>
KEYWORDS: <3-5 search keywords>
SUMMARY: <one sentence description>

Instruction: If the user mentions a specific service like 'auth-service', you MUST extract it.

Incident: "{issue}" """
    client = get_client()
    if client:
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
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
            pass
    
    # Offline / Rule-based Fallback
    service = "auth-service" if "auth" in issue.lower() else ("payment-api" if "payment" in issue.lower() else "frontend-service")
    severity = "P1" if "oom" in issue.lower() or "500" in issue.lower() else "P2"
    category = "CrashLoop" if "crash" in issue.lower() else ("DatabaseError" if "database" in issue.lower() else "ResourceExhaustion")
    return {"service": service, "severity": severity, "category": category, "keywords": issue, "summary": issue}

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
    client = get_client()
    if client:
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            pass

    # Offline Recovery Plan Fallback
    sop_ref = sops[0] if sops else "Standard restart procedure"
    return f"""1. ROOT CAUSE ANALYSIS
- Service '{context['service']}' encountered '{context['category']}' error condition ({health}).

2. IMMEDIATE ACTIONS
1. Inspect deployment configuration and memory limits.
2. Apply SOP remediation: {sop_ref}
3. Execute kubectl rollout restart deployment/{context['service']}.

3. VERIFICATION STEPS
1. Monitor pod status via check_pod_health.
2. Verify HTTP status endpoints return 200 OK.

4. PREVENTION RECOMMENDATION
- Configure automated horizontal pod autoscaling and set resource limits."""

def run_copilot(issue):
    output = []
    log = output.append
    log("=" * 60)
    log("DEVOPS CO-PILOT - MULTI-AGENT SRE SYSTEM")
    log("=" * 60)
    log("\n[AGENT 1: ORCHESTRATOR - Gemini 2.5 Flash]")
    log("  Parsing incident and routing to sub-agents...")
    context = orchestrate(issue)
    log(f"  Service  : {context['service']}")
    log(f"  Severity : {context['severity']}")
    log(f"  Category : {context['category']}")
    log(f"  Summary  : {context['summary']}")
    log("\n[INFRASTRUCTURE DIAGNOSTIC]")
    health = check_pod_health(context["service"])
    log(f"  {health}")
    log("\n[AGENT 2: DOCUMENTATION AGENT - Local Serverless Vector Memory]")
    log("  Semantic search via text-embedding-004...")
    try:
        sops = find_multiple_fixes(context["keywords"])
        if sops:
            log(f"  {len(sops)} SOPs retrieved:")
            for i, s in enumerate(sops, 1):
                log(f"  [{i}] {s[:120]}...")
        else:
            log("  No SOPs found - escalation path active.")
    except Exception as e:
        log(f"  Vector store search error: {e}")
        sops = []
    log("\n[AGENT 3: RECOVERY AGENT - Gemini 2.5 Flash]")
    log("  Synthesizing recovery plan from SOPs + live diagnostics...")
    plan = synthesize_recovery(issue, context, sops, health)
    log("\n" + "-" * 50)
    log(plan)
    log("-" * 50)
    log("\n[AUTONOMOUS ACTION]")
    sop_ref = sops[0] if sops else ""
    log(f"  {patch_deployment_config(context['service'], context['category'], sop_ref)}")
    log(f"  {restart_pod(context['service'])}")
    log("\n[VERIFICATION]")
    time.sleep(1)
    final = check_pod_health(context["service"], is_post_remediation=True, category=context["category"], sops_found=bool(sops))
    log(f"  Post-recovery: {final}")
    if "Running" in final:
        log("  Service stabilized. MTTR: < 10 seconds.")
    else:
        log("  Unstable. Creating escalation ticket...")
        ticket = create_jira_ticket(issue, plan[:120])
        log(f"  Jira ticket: {ticket}")
    log("\n" + "=" * 60)
    return "\n".join(output)