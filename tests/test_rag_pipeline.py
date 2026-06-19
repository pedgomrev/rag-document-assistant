from app.core.rag_pipeline import RAGPipeline

rag = RAGPipeline()

result = rag.ask("¿Qué es la preparación de datos?")

print("\nRespuesta:")
print(result["answer"])

print("\nFuentes:")
for source in result["sources"]:
    print(source)