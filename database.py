import os
import math
from typing import List, Dict, Any

# Local In-Memory Knowledge Base Store for Standard Operating Procedures (SOPs)
KNOWLEDGE_BASE_SOPS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "issue_type": "CrashLoopBackOff",
        "content": "SOP-101: Pod memory limit reached. FIX: Increase memory limit to 512Mi in deployment.yaml and execute kubectl rollout restart.",
        "embedding": None
    },
    {
        "id": 2,
        "issue_type": "DatabaseError",
        "content": "SOP-110: Database connection pool exhausted. FIX: Increase max_connections in database parameters or implement connection pooling (PgBouncer).",
        "embedding": None
    },
    {
        "id": 3,
        "issue_type": "ErrImagePull",
        "content": "SOP-105: Image pull failure. FIX: Verify Artifact Registry permissions and ensure the image tag exists in the repository.",
        "embedding": None
    },
    {
        "id": 4,
        "issue_type": "HighLatency",
        "content": "SOP-120: High latency detected on HTTP routes. FIX: Scale replica set up by executing kubectl scale deployment --replicas=5 and check upstream rate limits.",
        "embedding": None
    },
    {
        "id": 5,
        "issue_type": "ResourceExhaustion",
        "content": "SOP-130: CPU/Disk throttle warning. FIX: Provision additional node capacity, clear log caches, and restart affected workloads.",
        "embedding": None
    }
]

# Simple in-memory incidents store for Jira ticket simulation
INCIDENTS_STORE: List[Dict[str, str]] = []

def generate_embedding(text_to_embed: str) -> List[float]:
    """Generates vector embeddings using the google-genai SDK (text-embedding-004)."""
    try:
        from google import genai
        client = genai.Client()
        response = client.models.embed_content(
            model='text-embedding-004',
            contents=text_to_embed,
        )
        return response.embeddings[0].values
    except Exception as e:
        print(f"[EMBEDDING WARNING]: Using text fallback ({e})")
        return []

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Calculates cosine similarity between two vectors."""
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)

def seed_local_kb() -> int:
    """Pre-computes embeddings for all SOPs in the local knowledge base."""
    count = 0
    for sop in KNOWLEDGE_BASE_SOPS:
        if not sop["embedding"]:
            emb = generate_embedding(sop["content"])
            if emb:
                sop["embedding"] = emb
                count += 1
    return count if count > 0 else len(KNOWLEDGE_BASE_SOPS)

def get_engine():
    """Backwards compatibility stub for legacy database references."""
    return None

def find_multiple_fixes(error_message: Any, top_k: int = 3, threshold: float = 0.75) -> List[str]:
    """Retrieves top matching SOPs from the local vector database with strict thresholding (0.75)."""
    if not error_message:
        return []

    if not isinstance(error_message, str):
        error_message = str(error_message)

    # 1. Try Vector Similarity Search via google-genai
    query_vector = generate_embedding(error_message)
    if query_vector:
        scored = []
        for sop in KNOWLEDGE_BASE_SOPS:
            if not sop["embedding"]:
                sop["embedding"] = generate_embedding(sop["content"])
            
            if sop["embedding"]:
                score = cosine_similarity(query_vector, sop["embedding"])
                scored.append((score, sop["content"]))
        
        if scored:
            scored.sort(key=lambda x: x[0], reverse=True)
            # Enforce strict minimum similarity threshold (>= 0.75)
            results = [content for score, content in scored[:top_k] if score >= threshold]
            if results:
                return results

    # 2. Strict Keyword Search Fallback
    query_lower = error_message.lower()
    matches = []
    
    # Specific keyword map to prevent false positive matching on unmapped errors (DNS, Network, Gateway, etc.)
    sop_keywords = {
        "CrashLoopBackOff": ["crashloop", "oomkilled", "memory limit", "oom"],
        "DatabaseError": ["database", "connection pool", "pgbouncer", "max_connections"],
        "ErrImagePull": ["errimagepull", "image pull", "artifact registry", "image tag"],
        "HighLatency": ["high latency", "latency", "rate limit", "scale replica"],
        "ResourceExhaustion": ["resource exhaustion", "cpu throttle", "disk throttle"]
    }
    
    for sop in KNOWLEDGE_BASE_SOPS:
        issue_type = sop["issue_type"]
        keywords = sop_keywords.get(issue_type, [])
        if any(kw in query_lower for kw in keywords):
            matches.append(sop["content"])
            
    if matches:
        return matches[:top_k]
    
    # Strict threshold fallback: Return empty list if no relevant SOP is found
    return []
