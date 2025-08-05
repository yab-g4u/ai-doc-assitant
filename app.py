import streamlit as st
import os
from uuid import uuid4

from src.loader import load_document
from src.splitter import split_documents
from src.vectorstore import store_embeddings
from src.memory import create_memory
from src.gemini_llm import generate_gemini_response

from langchain_community.vectorstores import FAISS
import logging
logging.basicConfig(level=logging.INFO)
logging.info("App starting..") 

# Streamlit app for AI Document Assistant    
st.set_page_config(page_title="AI Doc Assistant", layout="wide", initial_sidebar_state="expanded")

# --- Directories ---
UPLOAD_DIR = "data/uploads"
INDEX_DIR = "data/indexes"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("📂 Upload & Settings")
    uploaded_file = st.file_uploader("Upload your document (.pdf or .txt)", type=["pdf", "txt"])
    st.markdown("---")
    st.subheader("⚙️ Model Settings")
    # Example model settings
    model_options = ["gemini-pro", "gemini-1.5", "gemini-ultra"]
    selected_model = st.selectbox("Select Gemini Model", model_options, index=0)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.05)
    max_tokens = st.number_input("Max Tokens", min_value=64, max_value=4096, value=512, step=32)
    st.markdown("---")
    st.subheader("ℹ️ About")
    st.info(
        "AI Doc Assistant lets you chat with your documents using Gemini LLM.\n\n"
        "Upload a PDF or TXT file and ask questions about its content."
    )

# Save model settings in session state
st.session_state["model_settings"] = {
    "model": selected_model,
    "temperature": temperature,
    "max_tokens": max_tokens
}

# --- MAIN CHAT INTERFACE ---
st.markdown(
    """
    <style>
    .chat-container {height: 65vh; overflow-y: auto; padding: 1rem; background: #f7f7fa; border-radius: 10px;}
    .user-msg {background: #d1e7dd; color: #222; padding: 0.7em 1em; border-radius: 12px 12px 0 12px; margin-bottom: 0.5em; max-width: 80%; align-self: flex-end;}
    .bot-msg {background: #fff; color: #222; padding: 0.7em 1em; border-radius: 12px 12px 12px 0; margin-bottom: 0.5em; max-width: 80%; align-self: flex-start; border: 1px solid #eee;}
    .chat-history {display: flex; flex-direction: column;}
    .typing {font-style: italic; color: #888;}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Session State Setup ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid4())
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "retriever" not in st.session_state:
    st.session_state.retriever = None

# --- Handle file upload and processing ---
if uploaded_file:
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.sidebar.success("✅ File uploaded successfully.")

    with st.spinner("Processing document..."):
        docs = load_document(file_path)
        chunks = split_documents(docs)
        if not chunks:
            st.error("❌ The document could not be processed or is empty. Please try another file.")
        else:
            index_path = os.path.join(INDEX_DIR, st.session_state.session_id)
            vectorstore = store_embeddings(chunks, index_path)
            retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
            st.session_state.vectorstore = vectorstore
            st.session_state.retriever = retriever

# --- CHAT UI ---
st.title("🧠 Chat With Your Document")

chat_placeholder = st.empty()

def render_chat():
    messages = st.session_state.chat_history
    chat_html = '<div class="chat-container"><div class="chat-history">'
    for q, a in messages:
        chat_html += f'<div class="user-msg">🧑 {q}</div>'
        chat_html += f'<div class="bot-msg">🤖 {a}</div>'
    chat_html += '</div></div>'
    chat_placeholder.markdown(chat_html, unsafe_allow_html=True)

render_chat()

# --- INPUT BOX AT BOTTOM ---
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Your question:", placeholder="Type your question and press Enter...", label_visibility="collapsed")
    submitted = st.form_submit_button("Send", use_container_width=True)

# --- HANDLE USER INPUT ---
if submitted and user_input and st.session_state.retriever:
    with st.spinner("🤖 Thinking..."):
        def answer_query(query):
            docs = st.session_state.retriever.get_relevant_documents(query)
            context = "\n".join([doc.page_content for doc in docs])
            prompt = f"Use the following context to answer the question:\n\n{context}\n\nQuestion: {query}"
            # Pass model settings to your LLM function if supported
            settings = st.session_state["model_settings"]
            return generate_gemini_response(
                prompt,
                model=settings["model"],
                temperature=settings["temperature"],
                max_tokens=settings["max_tokens"]
            )
        answer = answer_query(user_input)
        st.session_state.chat_history.append((user_input, answer))
        render_chat()

