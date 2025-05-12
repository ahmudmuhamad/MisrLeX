```markdown:e:\MisrLeX\README.md
# MisrLeX

MisrLeX is an open-source Retrieval-Augmented Generation (RAG) application designed to make Egyptian legal texts more accessible and understandable. By integrating advanced language models with a custom document retrieval system, MisrLeX delivers accurate, context-aware answers to legal queries grounded in Egyptian legislation and jurisprudence.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

---

## Features

- **Retrieval-Augmented Generation (RAG):** Combines semantic search with generative AI to provide grounded, context-aware legal answers.
- **Support for Egyptian Legal Texts:** Focused on Egyptian legislation and jurisprudence.
- **Multi-language Prompt Templates:** Supports both English and Arabic legal queries and responses.
- **Custom Document Chunking:** Efficiently splits and indexes legal documents for precise retrieval.
- **Extensible LLM Backend:** Easily switch between different LLM providers (OpenAI, Cohere, etc.).
- **API-First Design:** Built with FastAPI for easy integration and extension.

---

## Architecture

- **Backend:** Python (FastAPI)
- **Vector Database:** Qdrant (for semantic search)
- **Document Database:** MongoDB (for metadata and project management)
- **LLM Providers:** OpenAI, Cohere (pluggable)
- **Document Loaders:** Supports TXT and PDF formats
- **Prompt Templates:** Customizable, with localization support

---

## Installation

### Prerequisites

- Python 3.10+
- Docker & Docker Compose (for running MongoDB and Qdrant)
- (Optional) Virtual environment tool (e.g., `venv` or `conda`)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/MisrLeX.git
cd MisrLeX
```

### 2. Set Up the Environment

Create a virtual environment and activate it:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r src/requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment files and set your secrets:

```bash
copy src\.env.example src\.env
copy docker\.env.example docker\.env
```

Edit `.env` files to add your MongoDB, Qdrant, and LLM API keys.

### 5. Start Required Services (MongoDB & Qdrant)

```bash
docker-compose -f docker\docker-compose.dev.yml up -d
```

### 6. Run the Application

```bash
cd src
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

---

## Usage

- Use the API endpoints to upload legal documents, index them, and ask legal questions.
- Example endpoints:
  - `POST /data/upload/{project_id}`: Upload documents
  - `POST /index/{project_id}`: Index documents for semantic search
  - `POST /index/answer/{project_id}`: Ask a legal question and get an answer

See the FastAPI docs at `http://localhost:8000/docs` for interactive API documentation.

---

## Project Structure

```
MisrLeX/
│
├── docker/
│   └── docker-compose.dev.yml
├── src/
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   ├── stores/
│   ├── requirements.txt
│   └── main.py
├── README.md
└── ...
```

- **controllers/**: Business logic for processing, NLP, and project management
- **models/**: Database schemas and data models
- **routes/**: API endpoints
- **stores/**: LLM interfaces, vector DB, and prompt templates

---

## Configuration

- **MongoDB**: Used for storing project and document metadata.
- **Qdrant**: Used for vector-based semantic search.
- **LLM Providers**: Configure your API keys for OpenAI or Cohere in the `.env` files.

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests for new features, bug fixes, or documentation improvements.

---

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Qdrant](https://qdrant.tech/)
- [MongoDB](https://www.mongodb.com/)
- [LangChain](https://python.langchain.com/)
- [OpenAI](https://openai.com/)
- [Cohere](https://cohere.com/)

---




        