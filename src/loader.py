from langchain.document_loaders import PyPDFLoader, TextLoader
from pathlib import Path

def load_document(file_path):
    ext = Path(file_path).suffix.lower()
    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path)
    else:
        raise ValueError("Unsupported file type")
    return loader.load()
