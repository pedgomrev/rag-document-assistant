import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title = "RAG Document Assistant",
    page_icon="📄",
    layout="wide"
)

st.title("📄 RAG Document Assistant")
st.write("Consulta documentos PDF usando RAG, ChromDB, Ollama y FastAPI.")

def get_documents():
    try:
        response = requests.get(f"{API_URL}/documents")
        response.raise_for_status()
        return response.json().get("documents",[])
    except requests.exceptions.RequestException:
        return []
    
def upload_document(file):
    files = {
        "file": (
            file.name,
            file.getvalue(),
            "application/pdf"
        )
    }

    response = requests.post(
        f"{API_URL}/upload",
        files=files
    )
    return response.json()

def ask_question(question: str):
    response = requests.post(
        f"{API_URL}/ask",
        json={"question": question}
    )

    return response.json()

def delete_document(filename: str):
    response = requests.delete(
        f"{API_URL}/documents/{filename}"
    )

    return response.json()

with st.sidebar:
    st.header("📚 Documents")

    uploaded_file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:
        if st.button("Upload and index"):
            with st.spinner("Uploading and indexing document..."):
                result = upload_document(uploaded_file)

            if result.get("success"):
                st.success("Document uploaded and indexed successfully.")
                st.rerun()
            else:
                st.error(result.get("message", "Upload failed."))

    st.divider()

    documents = get_documents()

    if documents:
        st.subheader("Indexed documents")

        for doc in documents:
            col1, col2 = st.columns([3, 1])

            with col1:
                st.write(doc)

            with col2:
                if st.button("Delete", key=f"delete_{doc}"):
                    with st.spinner("Deleting and reindexing..."):
                        result = delete_document(doc)

                    if result.get("success"):
                        st.success("Document deleted.")
                        st.rerun()
                    else:
                        st.error(result.get("message", "Delete failed."))
    else:
        st.info("No documents indexed yet.")

st.header("Ask a question")

question = st.text_input(
    "Write your question about the indexed documents:"
)

if st.button("Ask"):
    if not question.strip():
        st.warning("Please write a question.")
    else:
        with st.spinner("Generating answer..."):
            result = ask_question(question)

        st.subheader("Answer")
        st.write(result.get("answer", "No answer returned."))

        sources = result.get("sources", [])

        if sources:
            st.subheader("Sources")

            for source in sources:
                st.write(
                    f"- `{source.get('source')}` — page `{source.get('page')}`"
                )