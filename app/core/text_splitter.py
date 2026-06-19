from langchain_text_splitters import RecursiveCharacterTextSplitter

class TextSplitter:
    """Divide documentos en chunks para usarlos en el sistema RAG."""

    @staticmethod
    def split_documents(documents,chunk_size: int = 1000, chunk_overlap: int = 150):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap,
        )
        return splitter.split_documents(documents)