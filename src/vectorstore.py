from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

def store_embeddings(docs, index_path):
    vectorstore = FAISS.from_documents(docs, OpenAIEmbeddings())
    vectorstore.save_local(index_path)
    return vectorstore

def load_vectorstore(index_path):
    return FAISS.load_local(index_path, OpenAIEmbeddings())
