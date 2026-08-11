import random

# Color toolkit for internal tool logs
class Color:
    YELLOW = '\033[93m'
    END = '\033[0m'

def check_pod_health(pod_name, is_post_remediation=False, category="", sops_found=True):
    """Checks Kubernetes status for a specific pod with category state-awareness."""
    cat_str = str(category).lower()
    unmapped_categories = ["networkerror", "dnsfailure", "unknown", "dns", "gateway"]
    
    if is_post_remediation:
        # Unmapped categories or zero SOPs retrieved cannot be resolved by a standard rollout restart
        if any(unmap in cat_str for unmap in unmapped_categories) or not sops_found:
            status = random.choice(["CrashLoopBackOff", "Pending", "Terminating"])
        else:
            status = "Running"
    else:
        status = random.choice(["CrashLoopBackOff", "CrashLoopBackOff", "Pending", "Terminating"])
        
    print(f"\n[TOOL CALL]: check_pod_health(pod_name='{pod_name}') -> {status}")
    return f"Pod '{pod_name}': {status}"

def patch_deployment_config(pod_name, category="", sop_text=""):
    """ACTUAL TOOL: Dynamically patches Kubernetes deployment specs before rollout."""
    sop_str = str(sop_text).lower()
    cat_str = str(category).lower()
    
    if "crash" in cat_str or "oom" in sop_str or "memory" in sop_str or "512mi" in sop_str:
        cmd = f"kubectl set resources deployment/{pod_name} -c {pod_name} --limits=memory=512Mi --requests=memory=256Mi"
    elif "database" in cat_str or "pool" in sop_str:
        cmd = f"kubectl set env deployment/{pod_name} MAX_CONNECTIONS=100 DB_POOL_SIZE=20"
    elif "image" in cat_str or "permission" in sop_str:
        cmd = f"kubectl set image deployment/{pod_name} {pod_name}=gcr.io/devops-copilot/{pod_name}:v2.1"
    else:
        cmd = f"kubectl patch deployment/{pod_name} -p '{{\"spec\":{{\"template\":{{\"metadata\":{{\"annotations\":{{\"reconfiguredBy\":\"DevOpsCoPilot\"}}}}}}}}}}'"
    
    print(f"\n[TOOL CALL]: patch_deployment_config(pod_name='{pod_name}')")
    return f"{cmd} -> SUCCESS"

def restart_pod(pod_name):
    """ACTUAL TOOL: Simulates a kubectl rollout restart."""
    print(f"\n[TOOL CALL]: restart_pod(pod_name='{pod_name}')")
    return f"kubectl rollout restart deployment/{pod_name} -> SUCCESS"

def create_jira_ticket(summary, ai_hint="Investigate logs."):
    """ACTUAL TOOL: Logs the incident AND the AI's findings into incident store."""
    from database import INCIDENTS_STORE
    ticket_id = f"INC-{random.randint(100, 999)}"
    INCIDENTS_STORE.append({
        "ticket_id": ticket_id,
        "issue_description": f"{summary} | AI: {ai_hint[:120]}",
        "status": "OPEN - AI ENRICHED"
    })
    print(f"[TOOL CALL]: Incident ticket {ticket_id} logged successfully.")
    return ticket_id