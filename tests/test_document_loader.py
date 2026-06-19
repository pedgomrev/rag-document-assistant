from app.core.document_loader import DocumentLoader

documents = DocumentLoader.load_pdf(
    "data/raw/paper_ejemplo.pdf"
)

print(f"Paginas cargadas: {len(documents)} ")

print(documents[0].page_content[:500])

print(documents[0].metadata)