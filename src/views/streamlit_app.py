import streamlit as st
import requests
from io import BytesIO

# --- Configuration ---
API_BASE_URL = "http://localhost:8000/api/v1"

# Page Setup
st.set_page_config(page_title="MisrLeX", layout="wide")
st.title("📚 MisrLeX: Egyptian Legal RAG")

# --- Sidebar: Project Config & API Health ---
st.sidebar.header("🔧 Project Configuration")
project_id_input = st.sidebar.text_input("Project ID", value="1")

# Validate project ID
if not project_id_input.isdigit():
    st.sidebar.error("Project ID must be an integer.")
    st.stop()
project_id = int(project_id_input)

# Health check
try:
    health_response = requests.get(f"{API_BASE_URL}/")
    health_data = health_response.json()
    st.sidebar.success(f"✅ API: {health_data.get('app_name')} v{health_data.get('app_version')}")
except Exception as e:
    st.sidebar.error("❌ API is not available.")
    st.stop()

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# --- 1. Document Management ---
st.header("1️⃣ Document Management")

# 1.1 Upload
st.subheader("📤 Upload Document")
uploaded_file = st.file_uploader("Choose a file to upload (TXT or PDF)", type=["txt", "pdf"])

if uploaded_file:
    if st.button("Upload File"):
        file_bytes = BytesIO(uploaded_file.read())
        files = {'file': (uploaded_file.name, file_bytes, uploaded_file.type)}
        try:
            response = requests.post(f"{API_BASE_URL}/data/upload/{project_id}", files=files)
            response_data = response.json()
            if response.status_code == 200 and response_data.get("signal") == "file_upload_success":
                st.success(f"✅ Uploaded: {uploaded_file.name} | File ID: {response_data.get('file_id')}")
                with st.expander("API Response"):
                    st.json(response_data)
            else:
                st.error("⚠️ File upload failed.")
                st.json(response_data)
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

# 1.2 Process
st.subheader("⚙️ Process Documents")

with st.expander("Advanced Settings"):
    chunk_size = st.number_input("Chunk Size", min_value=100, max_value=2000, value=500, step=100)
    overlap = st.number_input("Overlap", min_value=0, max_value=500, value=100, step=50)
    do_reset = st.checkbox("Reset before processing", value=False)

if st.button("Process Documents"):
    process_payload = {
        "chunk_size": chunk_size,
        "chunk_overlap": overlap,
        "do_reset": int(do_reset)
    }
    try:
        response = requests.post(f"{API_BASE_URL}/data/process/{project_id}", json=process_payload)
        response_data = response.json()
        if response.status_code == 200:
            st.success("✅ Documents processed.")
            with st.expander("API Response"):
                st.json(response_data)
        else:
            st.error("⚠️ Processing failed.")
            st.json(response_data)
    except Exception as e:
        st.error(f"Error processing documents: {e}")

# --- 2. Index Management ---
st.header("2️⃣ Index Management")

col1, col2 = st.columns(2)

with col1:
    if st.button("📌 Push Project to Index"):
        try:
            response = requests.post(f"{API_BASE_URL}/nlp/index/push/{project_id}", json={"do_reset": 0})
            response_data = response.json()
            if response.status_code == 200:
                st.success("✅ Pushed to index.")
                with st.expander("API Response"):
                    st.json(response_data)
            else:
                st.error("⚠️ Indexing failed.")
                st.json(response_data)
        except Exception as e:
            st.error(f"Indexing error: {e}")

with col2:
    if st.button("🔄 Reset Chat History"):
        st.session_state.chat_history = []
        st.success("Chat history cleared.")

# --- 3. Q&A Section ---
st.header("3️⃣ Q&A and Search")

# Show chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_question = st.chat_input("Ask a question about your documents:")

if user_question:
    st.session_state.chat_history.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    try:
        payload = {"text": user_question, "limit": 3}
        with st.spinner("Searching..."):
            response = requests.post(f"{API_BASE_URL}/nlp/index/answer/{project_id}", json=payload)
            response_data = response.json()

        if response.status_code == 200 and response_data.get("signal") == "rag_success":
            answer = response_data.get("answer", "No answer found.")
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(answer)
        else:
            error_message = response_data.get("detail") or response_data.get("signal") or "Unknown error."
            fallback = f"⚠️ Could not retrieve an answer. Error: {error_message}"
            st.session_state.chat_history.append({"role": "assistant", "content": fallback})
            with st.chat_message("assistant"):
                st.markdown(fallback)
            st.error("RAG API response issue:")
            st.json(response_data)

    except requests.exceptions.RequestException as e:
        err = f"API connection failed: {e}"
        st.session_state.chat_history.append({"role": "assistant", "content": err})
        st.error(err)
    except Exception as e:
        err = f"Unexpected error: {e}"
        st.session_state.chat_history.append({"role": "assistant", "content": err})
        st.error(err)

# Footer
st.markdown("---")
st.caption("MisrLeX")

