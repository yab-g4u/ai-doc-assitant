from pathlib import Path
from langchain.schema import Document  # Add this import

def load_document(file_path):
    ext = Path(file_path).suffix.lower()

    if ext == ".pdf":
        from PyPDF2 import PdfReader
        reader = PdfReader(file_path)
        text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
        # Return a list of Document objects
        return [Document(page_content=text, metadata={"source": file_path})]
    
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        # Return a list of Document objects
        return [Document(page_content=text, metadata={"source": file_path})]
    
    else:
        raise ValueError("Unsupported file type. Only .pdf and .txt are allowed.")