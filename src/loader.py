from pathlib import Path

def load_document(file_path):
    ext = Path(file_path).suffix.lower()

    if ext == ".pdf":
        from PyPDF2 import PdfReader
        reader = PdfReader(file_path)
        text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
        return [{"page_content": text}]
    
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        return [{"page_content": text}]
    
    else:
        raise ValueError("Unsupported file type. Only .pdf and .txt are allowed.")
