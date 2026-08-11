import os
import gradio as gr
from google import genai
from dotenv import load_dotenv

# 1. Read the .env file
load_dotenv()

# 2. Pull the key explicitly
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

# 3. Initialize the client safely
try:
    client = genai.Client(api_key=api_key) if api_key else genai.Client()
except Exception:
    client = None

def web_interface(issue):
    """Handles the interaction between the UI and the Multi-Agent logic."""
    if not issue or not issue.strip():
        return "Please describe an incident."
    try:
        from agent_engine import run_copilot
        result = run_copilot(issue)
        return result if result else "Analysis complete. Plan executed successfully."
    except Exception as e:
        return f"Error during execution: {str(e)}"

def seed_database():
    """Initializes the local vector database and pre-computes SOP embeddings."""
    try:
        from database import seed_local_kb
        count = seed_local_kb()
        return f"✅ Local Vector Store Initialized & Seeded with {count} SRE SOPs!"
    except Exception as e:
        return f"❌ Seed failed: {str(e)}"

# --- UI Layout Definition ---

with gr.Blocks() as demo:
    gr.Markdown("# 🚀 DevOps Co-Pilot | Multi-Agent SRE System")
    gr.Markdown("### **Autonomous Incident Analysis & Recovery with Local Serverless Vector RAG**")
    
    with gr.Row():
        # Left Column: Controls and Instructions
        with gr.Column(scale=1):
            gr.Markdown("### 📋 How to Demo")
            gr.Markdown("""
            1. **Initialize:** Click **'Seed Knowledge Base'** first to prime the vector store.
            2. **Test:** Click an example below or type your own cloud incident.
            3. **Run:** Click **'Execute'** to trigger the Orchestrator, Librarian, and Recovery agents.
            """)
            
            input_text = gr.Textbox(
                label="Describe the Incident", 
                placeholder="e.g., auth-service pods are in CrashLoopBackOff...", 
                lines=4
            )

            # Interactive Examples for the Judges
            gr.Examples(
                examples=[
                    ["The auth-service pods are in CrashLoopBackOff with OOMKilled errors. Memory usage is at 98%."],
                    ["The payment-api is throwing 500 errors; logs show database connection pool exhaustion."],
                    ["Frontend deployment failed with ErrImagePull; pods are stuck in Pending."]
                ],
                inputs=input_text, # Passed defined component
                label="Quick-Test Scenarios"
            )
            
            with gr.Row():
                run_btn = gr.Button("🚀 Execute Recovery Plan", variant="primary")
                seed_btn = gr.Button("🌱 Seed Knowledge Base", variant="secondary")

            gr.Markdown("---")
            gr.Markdown("""
            ### 💡 System Capabilities
            * **Real-time Diagnostics:** Categorizes Severity (P1-P4) and Issue Type.
            * **RAG Engine:** Retrieves grounded SOPs from Serverless Vector Memory.
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
    **Serverless Vector Memory** serves as the vector store, while **Gemini 2.5 Flash** provides the reasoning backbone 
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
    demo.launch(server_name="0.0.0.0", server_port=port, share=False, theme=gr.themes.Soft())