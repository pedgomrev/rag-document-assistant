# RAG Document Assistant

A Retrieval-Augmented Generation (RAG) application that enables users to upload PDF documents, index their contents into a vector database, and ask natural language questions grounded on the uploaded documents.

The project uses local Large Language Models (LLMs) through Ollama, semantic search with ChromaDB, and a REST API built with FastAPI.

---

# Features

* Upload PDF documents through a REST API.
* Automatic document processing and chunking.
* Embedding generation using local models.
* Semantic search with ChromaDB.
* Question answering based exclusively on indexed documents.
* Source attribution showing the document and page used to generate each answer.
* Document deletion and automatic reindexing.
* Fully local execution without external LLM APIs.

---

# Tech Stack

* Python 3.11
* FastAPI
* LangChain
* ChromaDB
* Ollama
* Llama 3.2
* mxbai-embed-large
* Pydantic

---

# Architecture

```text
PDF Documents
      │
      ▼
Document Loader
      │
      ▼
Text Splitter
      │
      ▼
Embeddings (mxbai-embed-large)
      │
      ▼
ChromaDB
      │
      ▼
Retriever
      │
      ▼
Llama 3.2 (Ollama)
      │
      ▼
Answer + Sources
```

---

# API Endpoints

## Upload a document

```http
POST /upload
```

Uploads a PDF document and automatically indexes it into the vector database.

## Ask a question

```http
POST /ask
```

Example request:

```json
{
  "question": "What is data preprocessing?"
}
```

## List indexed documents

```http
GET /documents
```

Returns all currently indexed PDF documents.

## Delete a document

```http
DELETE /documents/{filename}
```

Deletes a document and rebuilds the vector database.

## Reindex all documents

```http
POST /reindex
```

Recreates the vector database from all PDFs stored in the repository.

## Health check

```http
GET /health
```

Returns the API status.

---

# Project Structure

```text
rag-document-assistant/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── schemas/
│   └── services/
│
├── data/
│   ├── raw/
│   └── chroma/
│
├── tests/
│
├── requirements.txt
├── environment.yml
└── README.md
```

---

# Installation

## Clone the repository

```bash
git clone https://github.com/pedgomrev/rag-document-assistant.git
cd rag-document-assistant
```

## Create the Conda environment

```bash
conda env create -f environment.yml
conda activate rag-assistant
```

## Install Ollama

Download and install Ollama:

https://ollama.com/download

## Pull the required models

```bash
ollama pull llama3.2:3b
ollama pull mxbai-embed-large
```

## Run the API

```bash
uvicorn app.api.main:app --reload
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Future Improvements

* Streamlit user interface.
* Docker support.
* Hybrid retrieval (BM25 + Vector Search).
* Document metadata filtering.
* Automated testing pipeline.
* User authentication and document ownership.

---

# Author

**Pedro Gómez Revilla**

Master's Degree in Data Science and Artificial Intelligence (UOC)
