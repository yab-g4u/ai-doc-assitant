import streamlit as st
import os
from uuid import uuid4

from src.loader import load_document
from src.splitter import split_documents
from src.vectorstore import store_embeddings
from src.memory import create_memory
from src.gemini_llm import generate_gemini_response

from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain

st.set_page_config(page_title="AI Doc Assistant", layout="wide")
st.title("🧠 Chat With Your Document (Gemini LLM)")

UPLOAD_DIR = "data/uploads"
INDEX_DIR = "data/indexes"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)

# Session State Setup
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid4())

uploaded_file = st.file_uploader("📄 Upload your document (.pdf or .txt)", type=["pdf", "txt"])

if uploaded_file:
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("✅ File uploaded successfully.")

    # Document Handling
    with st.spinner("Processing document..."):
        docs = load_document(file_path)
        chunks = split_documents(docs)
        index_path = os.path.join(INDEX_DIR, st.session_state.session_id)
        vectorstore = store_embeddings(chunks, index_path)

        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
        memory = create_memory()

        # Build Chat Chain
        def answer_query(query):
            docs = retriever.get_relevant_documents(query)
            context = "\n".join([doc.page_content for doc in docs])
            prompt = f"Use the following context to answer the question:\n\n{context}\n\nQuestion: {query}"
            return generate_gemini_response(prompt)

        st.subheader("💬 Ask questions about your document")

        user_input = st.text_input("Your question:", placeholder="E.g. What is this document about?")
        if user_input:
            with st.spinner("Thinking..."):
                answer = answer_query(user_input)
                st.session_state.chat_history.append((user_input, answer))

        for i, (q, a) in enumerate(st.session_state.chat_history):
            st.markdown(f"**🧑 You:** {q}")
            st.markdown(f"**🤖 AI:** {a}")
