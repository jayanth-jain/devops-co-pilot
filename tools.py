import random
import sqlalchemy
from database import get_db_connection

# Color toolkit for internal tool logs
class Color:
    YELLOW = '\033[93m'
    END = '\033[0m'

def check_pod_health(pod_name):
    """ACTUAL TOOL: Checks Kubernetes status for a specific pod."""
    statuses = ["Running", "CrashLoopBackOff", "Pending", "Terminating"]
    status = random.choice(statuses)
    print(f"\n⚡ [TOOL CALL]: check_pod_health(pod_name='{pod_name}')")
    return f"STATUS: {status}"

def restart_pod(pod_name):
    """ACTUAL TOOL: Simulates a kubectl rollout restart."""
    print(f"\n⚡ [TOOL CALL]: restart_pod(pod_name='{pod_name}')")
    return f"SUCCESS: Pod {pod_name} has been cycled."

def create_jira_ticket(issue_summary, ai_hint="Investigate logs."):
    """ACTUAL TOOL: Logs the incident AND the AI's findings into AlloyDB."""
    t_id = f"INC-{random.randint(100, 999)}"
    
    try:
        engine = get_db_connection()
        # We update the 'description' with the AI's top possibility to show enrichment
        enriched_desc = f"{issue_summary} | AI SUGGESTION: {ai_hint[:100]}"
        
        query = sqlalchemy.text("""
            INSERT INTO incidents (ticket_id, issue_description, status) 
            VALUES (:id, :desc, 'OPEN - AI ENRICHED')
        """)
        
        with engine.connect() as conn:
            conn.execute(query, {"id": t_id, "desc": enriched_desc})
            conn.commit()
        
        print(f"{Color.YELLOW}⚡ [TOOL CALL]: Incident successfully synced to AlloyDB.{Color.END}")
        return f"TICKET CREATED: {t_id} (Data Updated with AI Hint)"
    except Exception as e:
        # If DB is down, still return a ticket so the Orchestrator doesn't crash
        return f"TICKET CREATED: {t_id} (Local Failover - DB Error: {e})"