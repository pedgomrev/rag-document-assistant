from fastapi import (
    FastAPI,
    UploadFile,
    File
)
from app.services.document_service import DocumentService
from app.core.rag_pipeline import RAGPipeline
from app.schemas.chat import(
    QuestionRequest,
    QuestionResponse
)

app = FastAPI(
    title = "RAG Document Assistant",
    description="API para consultar documentos mediante RAG",
    version="1.0.0"
)

rag_pipeline = RAGPipeline()

def reload_rag_pipeline():
    global rag_pipeline
    rag_pipeline = RAGPipeline()

@app.get("/")
def root():
    return {"message": "RAG Document Assistant API"}

@app.get("/health")
def health_check():
    return{
        "status": "healthy"
    }

@app.post(
    "/ask",
    response_model=QuestionResponse
)
def ask_question(
    request: QuestionRequest
):
    result = rag_pipeline.ask(
        request.question
    )

    return QuestionResponse(
        answer=result["answer"],
        sources=result["sources"]
    )

@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {
            "success": False,
            "message": "Solo se permiten archivos PDF."
        }

    file_path = DocumentService.save_pdf(file)
    index_result = DocumentService.index_pdf(file_path)

    reload_rag_pipeline()

    return {
        "success": True,
        "filename": file.filename,
        "path": str(file_path),
        "indexing": index_result
    }

@app.get("/documents")
def list_documents():
    from pathlib import Path

    return {
        "documents": [
            file.name
            for file in Path("data/raw").glob("*.pdf")
        ]
    }

@app.delete("/documents/{filename}")
def delete_pdf(filename: str):
    delete_result = DocumentService.delete_pdf(filename)

    if delete_result["success"]:
        reindex_result = DocumentService.reindex_all_documents()
        reload_rag_pipeline()
        delete_result["reindexing"] = reindex_result

    return delete_result


@app.post("/reindex")
def reindex_documents():
    result = DocumentService.reindex_all_documents()
    reload_rag_pipeline()
    return result
