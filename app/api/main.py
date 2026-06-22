from fastapi import FastAPI

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

