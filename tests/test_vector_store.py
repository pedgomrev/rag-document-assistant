from app.core.document_loader import DocumentLoader
from app.core.text_splitter import TextSplitter
from app.core.vector_store import VectorStore


documents = DocumentLoader.load_pdfs("data/raw")
chunks = TextSplitter.split_documents(documents)

print(f"Chunks a guardar: {len(chunks)}")

vector_store = VectorStore()
vector_store.create_from_documents(chunks)

print("Base vectorial creada correctamente en data/chroma")