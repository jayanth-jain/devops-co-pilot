import os
import sqlalchemy
from google.cloud.alloydb.connector import Connector

# ✅ NO top-level Connector() call — lazy init only
_connector = None
_db_engine = None

def get_connector():
    global _connector
    if _connector is None:
        _connector = Connector()
    return _connector

def get_db_connection():
    instance_connection_name = os.environ.get(
        "INSTANCE_CONNECTION_NAME",
        "projects/devops-co-pilot/locations/us-central1/clusters/devops-copilot-cluster/instances/devops-primary-instance"
    )
    db_user = os.environ.get("DB_USER", "postgres")
    db_pass = os.environ.get("DB_PASS")
    db_name = os.environ.get("DB_NAME", "postgres")

    def getconn():
        conn = get_connector().connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            ip_type="public"
        )
        return conn

    engine = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )
    return engine

def get_engine():
    global _db_engine
    if _db_engine is None:
        _db_engine = get_db_connection()
    return _db_engine

def find_multiple_fixes(error_message: str):
    engine = get_engine()
    query = sqlalchemy.text("""
        SELECT content FROM documentation
        ORDER BY embedding <=> google_ml.embedding('text-embedding-004', :msg)::vector
        LIMIT 3;
    """)
    try:
        with engine.connect() as conn:
            results = conn.execute(query, {"msg": error_message}).fetchall()
            return [r[0] for r in results] if results else []
    except Exception as e:
        print(f"❌ [DATABASE ERROR]: {e}")
        return []
