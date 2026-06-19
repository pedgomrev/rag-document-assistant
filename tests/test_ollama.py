from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2:3b",
    temperature = 0
)

response = llm.invoke(
    "Dime una receta que lleve patatas fritas, solo quiero el nombre"
)

print(response.content)