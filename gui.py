import gradio as gr
from database import find_multiple_fixes
from main import run_copilot

def agent_interface(issue):
    # This calls your existing Librarian logic
    fixes = find_multiple_fixes(issue)
    
    if not fixes:
        return "🤖 [ORCHESTRATOR]: No matching SOPs found. Escalating to Jira (INC-207)."
    
    output = "🔍 [LIBRARIAN]: Grounded matches found in AlloyDB:\n\n"
    for i, fix in enumerate(fixes, 1):
        output += f"{i}. {fix}\n"
    
    output += "\n🤖 [ORCHESTRATOR]: Initiating recovery flow..."
    return output

# Define the Professional UI
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🚀 DevOps Co-Pilot: Agentic SRE Interface")
    gr.Markdown("Powered by **Gemini 1.5 Flash** & **AlloyDB pgvector**")
    
    with gr.Row():
        with gr.Column():
            input_text = gr.Textbox(label="Describe the System Issue", placeholder="e.g., Auth service is returning 500 errors...")
            submit_btn = gr.Button("Analyze & Remediate", variant="primary")
        
        with gr.Column():
            output_text = gr.Textbox(label="Agent Reasoning & Action Plan", interactive=False)

    submit_btn.click(fn=agent_interface, inputs=input_text, outputs=output_text)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8080)
