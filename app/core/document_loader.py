from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

class DocumentLoader:

    @staticmethod
    def load_pdf(pdf_path: str):
        if not Path(pdf_path).exists():
            raise FileNotFoundError(f"No se encontró el archivo: {pdf_path}")

        loader = PyPDFLoader(pdf_path)
        return loader.load()

    @staticmethod
    def load_pdfs(folder_path: str):
        documents = []

        pdf_files = Path(folder_path).glob("*.pdf")

        for pdf_file in pdf_files:
            loader = PyPDFLoader(str(pdf_file))
            documents.extend(loader.load())

        return documents
