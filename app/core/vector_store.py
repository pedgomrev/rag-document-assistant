import shutil
from pathlib import Path

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

class VectorStore:
    """
        Gestiona la base vectorial de chromaDB
    """
    def __init__(
        self,
        persist_directory: str = "data/chroma",
        embedding_model: str = "mxbai-embed-large",
        collection_name: str = "documents",
    ):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.embeddings = OllamaEmbeddings(model=embedding_model)

    def create_from_documents(self, documents):
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)

        return Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name=self.collection_name,
        )

    def add_documents(self, documents):
        vector_store = self.load()
        vector_store.add_documents(documents)
        return vector_store

    def load(self):
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name=self.collection_name,
        )

    def reset(self):
        vector_store = self.load()
        vector_store.delete_collection()