from app.core.document_loader import DocumentLoader
from app.core.text_splitter import TextSplitter


documents = DocumentLoader.load_pdfs("data/raw")

chunks = TextSplitter.split_documents(documents)

print(f"Documentos originales: {len(documents)}")
print(f"Chunks generados: {len(chunks)}")

print("\nPrimer chunk:")
print(chunks[0].page_content[:1000])

print("\nMetadata:")
print(chunks[0].metadata)