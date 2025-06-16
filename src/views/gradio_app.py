import gradio as gr
import requests
import os
from typing import Optional

# Configuration
FASTAPI_URL = "http://localhost:8000"  # Update if your FastAPI runs elsewhere
DEFAULT_PROJECT_ID = 1  # Default project ID to work with

# Helper functions for API calls
def upload_file(project_id: float, file_path: str):
    """Upload a file to the FastAPI backend"""
    try:
        with open(file_path, 'rb') as f:
            response = requests.post(
                f"{FASTAPI_URL}/api/v1/data/upload/{int(project_id)}",
                files={"file": (os.path.basename(file_path), f)}
            )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def process_files(project_id: float, chunk_size: int, overlap_size: int, do_reset: bool, file_id: Optional[str] = None):
    """Process uploaded files"""
    try:
        response = requests.post(
            f"{FASTAPI_URL}/api/v1/data/process/{int(project_id)}",
            json={
                "chunk_size": chunk_size,
                "overlap_size": overlap_size,
                "do_reset": 1 if do_reset else 0,
                "file_id": file_id
            }
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def index_project(project_id: float, do_reset: bool):
    """Index project into vector database"""
    try:
        response = requests.post(
            f"{FASTAPI_URL}/api/v1/nlp/index/push/{int(project_id)}",
            json={"do_reset": 1 if do_reset else 0}
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_index_info(project_id: float):
    """Get information about the vector index"""
    try:
        response = requests.get(
            f"{FASTAPI_URL}/api/v1/nlp/index/info/{int(project_id)}"
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def semantic_search(project_id: float, query: str, limit: int = 5):
    """Perform semantic search"""
    try:
        response = requests.post(
            f"{FASTAPI_URL}/api/v1/nlp/index/search/{int(project_id)}",
            json={"text": query, "limit": limit}
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def ask_question(project_id: float, question: str, limit: int = 5):
    """Get an answer from the RAG system"""
    try:
        response = requests.post(
            f"{FASTAPI_URL}/api/v1/nlp/index/answer/{int(project_id)}",
            json={"text": question, "limit": limit}
        )
        data = response.json()
        return data.get("answer", ""), data.get("prompt", ""), data
    except Exception as e:
        return "", "", {"error": str(e)}

# Gradio Interface Components
def create_data_tab():
    """Create the data upload and processing tab"""
    with gr.Blocks() as tab:
        with gr.Row():
            project_id = gr.Number(value=DEFAULT_PROJECT_ID, label="Project ID")
            file_input = gr.File(label="Upload Legal Document")

        with gr.Row():
            upload_btn = gr.Button("Upload File")
            upload_output = gr.JSON(label="Upload Result")

        with gr.Row():
            with gr.Column():
                chunk_size = gr.Slider(100, 2000, value=512, step=100, label="Chunk Size")
                overlap_size = gr.Slider(0, 500, value=128, step=10, label="Overlap Size")
                reset_toggle = gr.Checkbox(label="Reset Existing Data", value=False)
                process_btn = gr.Button("Process Documents")
            process_output = gr.JSON(label="Processing Result")

        upload_btn.click(
            fn=lambda project_id, file: upload_file(project_id, file.name),
            inputs=[project_id, file_input],
            outputs=upload_output
        )

        process_btn.click(
            fn=process_files,
            inputs=[project_id, chunk_size, overlap_size, reset_toggle],
            outputs=process_output
        )

    return tab

def create_index_tab():
    """Create the vector index management tab"""
    with gr.Blocks() as tab:
        with gr.Row():
            project_id = gr.Number(value=DEFAULT_PROJECT_ID, label="Project ID")
            reset_toggle = gr.Checkbox(label="Reset Existing Index", value=False)
            index_btn = gr.Button("Create/Update Index")

        with gr.Row():
            index_output = gr.JSON(label="Indexing Result")
            info_btn = gr.Button("Get Index Info")
            info_output = gr.JSON(label="Index Information")

        index_btn.click(
            fn=index_project,
            inputs=[project_id, reset_toggle],
            outputs=index_output
        )

        info_btn.click(
            fn=get_index_info,
            inputs=[project_id],
            outputs=info_output
        )

    return tab

def create_search_tab():
    """Create the semantic search tab"""
    with gr.Blocks() as tab:
        with gr.Row():
            project_id = gr.Number(value=DEFAULT_PROJECT_ID, label="Project ID")
            query = gr.Textbox(label="Search Query")
            limit = gr.Slider(1, 10, value=5, step=1, label="Number of Results")
            search_btn = gr.Button("Search")

        search_output = gr.JSON(label="Search Results")

        search_btn.click(
            fn=semantic_search,
            inputs=[project_id, query, limit],
            outputs=search_output
        )

    return tab

def create_qa_tab():
    """Create the Q&A tab"""
    with gr.Blocks() as tab:
        with gr.Row():
            project_id = gr.Number(value=DEFAULT_PROJECT_ID, label="Project ID")
            question = gr.Textbox(label="Your Legal Question")
            limit = gr.Slider(1, 10, value=5, step=1, label="Context Chunks to Use")
            ask_btn = gr.Button("Ask")

        with gr.Row():
            answer_output = gr.Textbox(label="Answer", interactive=False)
            full_prompt = gr.Textbox(label="Full Prompt Used", interactive=False)

        with gr.Row():
            debug_output = gr.JSON(label="Debug Information")

        ask_btn.click(
            fn=ask_question,
            inputs=[project_id, question, limit],
            outputs=[answer_output, full_prompt, debug_output]
        )

    return tab

# Main Interface
with gr.Blocks(title="MisrLeX Legal RAG System") as demo:
    gr.Markdown("# MisrLeX Legal RAG System")
    gr.Markdown("Retrieval-Augmented Generation for Egyptian Legal Documents")

    with gr.Tabs():
        with gr.Tab("Data Management"):
            create_data_tab()
        with gr.Tab("Vector Index"):
            create_index_tab()
        with gr.Tab("Semantic Search"):
            create_search_tab()
        with gr.Tab("Q&A"):
            create_qa_tab()

# Launch the interface
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
