          
# MisrLeX: Egyptian Legal RAG

MisrLeX is a Retrieval-Augmented Generation (RAG) platform designed for legal document management and question answering, tailored for Egyptian law. It leverages FastAPI, Streamlit, PostgreSQL (with pgvector), and modern LLMs (OpenAI, Cohere, etc.) to provide document upload, processing, vector search, and chat-based Q&A.

---

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Development & Contribution](#development--contribution)


---

## Features
- Upload and process legal documents (TXT, PDF)
- Chunking and vectorization of documents
- Vector database search (Qdrant/pgvector)
- RAG-based Q&A with LLMs (OpenAI, Cohere, etc.)
- Multilingual support (English, Arabic)
- Prometheus metrics for monitoring
- Dockerized for easy deployment

---

## Architecture
- **Frontend:** Streamlit app for user interaction
- **Backend:** FastAPI REST API
- **Database:** PostgreSQL with pgvector extension for vector search
- **Vector DB:** Qdrant or pgvector
- **LLM Providers:** OpenAI, Cohere, JinaAI (configurable)
- **Containerization:** Docker Compose for orchestration

---

## Project Structure
```
MisrLeX/
├── docker/                # Docker, Nginx, Prometheus configs
├── src/
│   ├── controllers/       # Business logic (Data, NLP, Process, Project)
│   ├── helpers/           # Config and settings
│   ├── models/            # ORM models and database schemas
│   ├── routes/            # FastAPI routers (data, nlp, base)
│   ├── stores/            # LLM and VectorDB provider factories
│   ├── utils/             # Metrics and utilities
│   ├── views/             # Streamlit frontend
│   └── main.py            # FastAPI app entrypoint
└── requirements.txt       # Python dependencies
```

---

## Setup & Installation
### Prerequisites
- Docker & Docker Compose
- Python 3.10+

### 1. Clone the Repository
```bash
git clone https://github.com/ahmudmuhamad/MisrLeX.git
cd MisrLeX
```

### 2. Configure Environment Variables
- Copy `.env.example` files to `.env` and fill in required values (API keys, DB credentials, etc.)
- For Docker: Edit `docker/env/.env.example.app` and `docker/env/.env.example.postgres`

### 3. Start Services with Docker Compose
```bash
docker-compose -f docker/docker-compose.dev.yml up -d
```
- This will start FastAPI, PostgreSQL (with pgvector), Qdrant, pgAdmin, and Nginx.

### 4. Access the Services
- **API:** http://localhost:8000/docs (FastAPI Swagger UI)
- **Streamlit UI:** http://localhost:8501
- **pgAdmin:** http://localhost:5050 (login with credentials from `.env`)

---

## Usage
### 1. Upload Documents
- Use the Streamlit UI or `/api/v1/data/upload/{project_id}` endpoint to upload TXT/PDF files.

### 2. Process Documents
- Chunk and preprocess documents via Streamlit or `/api/v1/data/process/{project_id}`.

### 3. Index Documents
- Push processed chunks to the vector database using `/api/v1/nlp/index/push/{project_id}`.

### 4. Ask Questions
- Use the chat interface in Streamlit or `/api/v1/nlp/index/answer/{project_id}` for RAG-based Q&A.

---

## API Endpoints (Key Examples)
- `GET /api/v1/` — API health check
- `POST /api/v1/data/upload/{project_id}` — Upload a document
- `POST /api/v1/data/process/{project_id}` — Process documents (chunking)
- `POST /api/v1/nlp/index/push/{project_id}` — Index processed chunks
- `POST /api/v1/nlp/index/answer/{project_id}` — RAG Q&A

See [src/routes/](src/routes/) for full API details.

---

## Development & Contribution
- Install Python dependencies: `pip install -r src/requirements.txt`
- Run FastAPI locally: `uvicorn src.main:app --reload`
- Run Streamlit UI: `streamlit run src/views/streamlit_app.py`
- Linting and formatting: (add your preferred tools)
- PRs and issues welcome!

---

## Credits
- Built with FastAPI, Streamlit, PostgreSQL, Qdrant, OpenAI, JinaAI, HuggingFace and Cohere.

---

For more details, see the codebase and Docker configs. If you have questions, open an issue.

        
