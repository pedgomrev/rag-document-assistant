from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

class DocumentLoader:

    @staticmethod
    def load_pdfs(pdf_path:str):
        documents = []
        pdf_files = Path(pdf_path).glob("*.pdf")
        for pdf_file in pdf_files:

            loader = PyPDFLoader(str(pdf_file))
            documents.extend(
                loader.load()
            )
        return loader.load()