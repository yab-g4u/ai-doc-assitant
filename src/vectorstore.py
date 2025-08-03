from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# Use a compact model to avoid memory issues
def get_embedding_model():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def store_embeddings(docs, index_path):
    embeddings = get_embedding_model()
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(index_path)
    return vectorstore

def load_vectorstore(index_path):
    embeddings = get_embedding_model()
    return FAISS.load_local(index_path, embeddings)
