from pathlib import Path
from fastapi import UploadFile

from app.core.document_loader import DocumentLoader
from app.core.text_splitter import TextSplitter
from app.core.vector_store import VectorStore

class DocumentService:

    RAW_DATA_PATH = Path("data/raw")

    @classmethod
    def save_pdf(
        cls,
        file: UploadFile
    ) -> Path:
        cls.RAW_DATA_PATH.mkdir(
            parents= True,
            exist_ok= True
        )

        file_path = cls.RAW_DATA_PATH / file.filename

        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        return file_path

    @classmethod
    def delete_pdf(
        cls,
        filename: str
    ) -> dict:

        file_path = cls.RAW_DATA_PATH / filename

        if not file_path.exists():
            return {
                "success": False,
                "message": f"El archivo '{filename}' no existe."
            }

        file_path.unlink()

        return {
            "success": True,
            "message": f"El archivo '{filename}' ha sido eliminado."
        }
    
    @classmethod
    def index_pdf(cls, file_path: Path) -> dict:
        documents = DocumentLoader.load_pdf(str(file_path))
        chunks = TextSplitter.split_documents(documents)

        VectorStore().add_documents(chunks)

        return {
            "success": True,
            "message": f"Documento indexado correctamente: {file_path.name}",
            "chunks": len(chunks)
        }
    
    @classmethod
    def reindex_all_documents(cls) -> dict:
        documents = DocumentLoader.load_pdfs(str(cls.RAW_DATA_PATH))
        chunks = TextSplitter.split_documents(documents)

        vector_store = VectorStore()
        vector_store.reset()

        if chunks:
            vector_store.create_from_documents(chunks)

        return {
            "success": True,
            "message": "Todos los documentos han sido reindexados correctamente.",
            "documents": len(documents),
            "chunks": len(chunks)
        }