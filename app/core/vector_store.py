from pathlib import Path

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

class VectorStore:
    """
        Gestiona la base vectorial ChromaDB.
    """

    def __init__(
            self,
            persist_directory: str = "data/chroma",
            embedding_model: str = "mxbai-embed-large",
    ):
        self.persist_directory = persist_directory
        self.embeddings = OllamaEmbeddings(model=embedding_model)

    def create_from_documents(self, documents):
        Path(self.persist_directory).mkdir(parents=True, exist_ok = True)
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding = self.embeddings,
            persist_directory=self.persist_directory,
        )
        return vector_store
    
    def load(self):
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
        )