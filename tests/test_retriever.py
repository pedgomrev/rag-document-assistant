from app.core.vector_store import VectorStore

vector_store = VectorStore().load()

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

query = "¿Qué es la preparación de datos?"

results = retriever.invoke(query)

print(f"Resultados encontrados: {len(results)}")

for i, doc in enumerate(results, start=1):
    print(f"\n--- Resultado {i} ---")
    print(doc.page_content[:800])
    print("\nMetadata:")
    print(doc.metadata)