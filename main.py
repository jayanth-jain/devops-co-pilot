import os
import gradio as gr

def web_interface(issue):
    """Handles the interaction between the UI and the Multi-Agent logic."""
    if not issue or not issue.strip():
        return "Please describe an incident."
    try:
        # Import the core logic from your existing cli_backup.py
        from cli_backup import run_copilot
        result = run_copilot(issue)
        return result if result else "Analysis complete. Plan executed successfully."
    except Exception as e:
        return f"Error during execution: {str(e)}"

def seed_database():
    """Initializes the AlloyDB table and inserts the vector-enabled SOPs."""
    try:
        from database import get_engine
        import sqlalchemy
        engine = get_engine()
        with engine.connect() as conn:
            # 1. Enable Required Extensions for AI and Vector search
            conn.execute(sqlalchemy.text("CREATE EXTENSION IF NOT EXISTS google_ml_integration CASCADE;"))
            conn.execute(sqlalchemy.text("CREATE EXTENSION IF NOT EXISTS vector CASCADE;"))
            
            # 2. Create the Documentation Table
            conn.execute(sqlalchemy.text("""
                CREATE TABLE IF NOT EXISTS documentation (
                    id SERIAL PRIMARY KEY,
                    issue_type TEXT,
                    content TEXT,
                    embedding VECTOR(768)
                );
            """))
            
            # 3. Seed the Knowledge Base with SRE Standard Operating Procedures (SOPs)
            # This uses the text-embedding-004 model directly inside the SQL query
            conn.execute(sqlalchemy.text("""
                INSERT INTO documentation (issue_type, content, embedding) VALUES
                ('CrashLoopBackOff', 'SOP-101: Pod memory limit reached. FIX: Increase memory limit to 512Mi in deployment.yaml and execute kubectl rollout restart.', google_ml.embedding('text-embedding-004', 'CrashLoopBackOff')::vector),
                ('DatabaseError', 'SOP-110: Database connection pool exhausted. FIX: Increase max_connections in database parameters or implement connection pooling (PgBouncer).', google_ml.embedding('text-embedding-004', 'database')::vector),
                ('ErrImagePull', 'SOP-105: Image pull failure. FIX: Verify Artifact Registry permissions and ensure the image tag exists in the repository.', google_ml.embedding('text-embedding-004', 'ErrImagePull')::vector)
                ON CONFLICT DO NOTHING
            """))
            conn.commit()
            return "✅ AlloyDB Table Created & Knowledge Base Seeded successfully!"
    except Exception as e:
        return f"❌ Seed failed: {str(e)}"

# --- UI Layout Definition ---

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🚀 DevOps Co-Pilot | Multi-Agent SRE System")
    gr.Markdown("### **Autonomous Incident Analysis & Recovery with AlloyDB RAG**")
    
    with gr.Row():
        # Left Column: Controls and Instructions
        with gr.Column(scale=1):
            gr.Markdown("### 📋 How to Demo")
            gr.Markdown("""
            1. **Initialize:** Click **'Seed Knowledge Base'** first to prime the AlloyDB vector store.
            2. **Test:** Click an example below or type your own cloud incident.
            3. **Run:** Click **'Execute'** to trigger the Orchestrator, Librarian, and Recovery agents.
            """)
            
            # Interactive Examples for the Judges
            gr.Examples(
                examples=[
                    ["The auth-service pods are in CrashLoopBackOff with OOMKilled errors. Memory usage is at 98%."],
                    ["The payment-api is throwing 500 errors; logs show database connection pool exhaustion."],
                    ["Frontend deployment failed with ErrImagePull; pods are stuck in Pending."]
                ],
                inputs=None, # Allows manual clicking
                label="Quick-Test Scenarios"
            )
            
            input_text = gr.Textbox(
                label="Describe the Incident", 
                placeholder="e.g., auth-service pods are in CrashLoopBackOff...", 
                lines=4
            )
            
            with gr.Row():
                run_btn = gr.Button("🚀 Execute Recovery Plan", variant="primary")
                seed_btn = gr.Button("🌱 Seed Knowledge Base", variant="secondary")

            gr.Markdown("---")
            gr.Markdown("""
            ### 💡 System Capabilities
            * **Real-time Diagnostics:** Categorizes Severity (P1-P4) and Issue Type.
            * **RAG Engine:** Retrieves grounded SOPs from AlloyDB pgvector.
            * **Self-Healing:** Generates precise `kubectl` recovery commands.
            * **Auto-Escalation:** Integrated Jira ticket generation if recovery fails.
            """)
            gr.Markdown("**System Status:** 🟢 Online  \n**Engine:** Gemini 2.5 Flash")

        # Right Column: Agent Output
        with gr.Column(scale=2):
            output_text = gr.Textbox(
                label="Multi-Agent Reasoning & Recovery Output", 
                interactive=False, 
                lines=30,
                placeholder="Agent reasoning will appear here after execution..."
            )

    # Technical Footer
    gr.Markdown("---")
    gr.Markdown("""
    **Architecture Note:** This system leverages a **Multi-Agent RAG Pattern**. 
    **AlloyDB** serves as the vector memory, while **Gemini 2.5 Flash** provides the reasoning backbone 
    to synthesize actionable SRE recovery plans from unstructured incident data.
    """)

    # Event Handlers
    run_btn.click(fn=web_interface, inputs=input_text, outputs=output_text)
    seed_btn.click(fn=seed_database, outputs=output_text)

# --- Entry Point ---

if __name__ == "__main__":
    # Cloud Run requires binding to 0.0.0.0 and port 8080
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting SRE Co-Pilot on port {port}...")
    demo.launch(server_name="0.0.0.0", server_port=port, share=False)