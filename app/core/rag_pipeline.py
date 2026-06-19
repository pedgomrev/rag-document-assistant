from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from app.core.vector_store import VectorStore

class RAGPipeline:
    """
        Pipeline RAG: recupera context orelevante y genera una respuesta.
    """
    def __init__(
            self,
            llm_model: str = "llama3.2:3b",
            k: int = 3,
    ):
        self.vector_sotre = VectorStore().load()
        self.retriever = self.vector_sotre.as_retriever(
            search_kwargs={"k": k}
        )
        self.llm = ChatOllama(
            model = llm_model,
            temperature = 0
        )

        self.prompt = ChatPromptTemplate.from_template(
            """
            Eres un asistente especializado en responder preguntas sobre documentos.

            Responde de forma clara, directa y en español.
            Usa únicamente el contexto proporcionado.
            No menciones "el contexto proporcionado" en la respuesta.

            Si la respuesta no aparece en los documentos, responde exactamente:
            "No encuentro información suficiente en los documentos."

            Contexto:
            {context}

            Pregunta:
            {question}

            Respuesta:
            """
        )

    def ask(self,question:str):
        docs = self.retriever.invoke(question)
        context = "\n\n".join(
            doc.page_content for doc in docs
        )
        chain = self.prompt | self.llm
        response = chain.invoke(
            {
                "context": context,
                "question":question,
            }
        )

        sources = [
            {
                "source": doc.metadata.get("source"),
                "page": doc.metadata.get("page_label", doc.metadata.get("page")),
            }
            for doc in docs
        ]

        return {
            "answer": response.content,
            "sources": sources,
        }