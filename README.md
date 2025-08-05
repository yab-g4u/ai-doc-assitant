
# 🧠 AI Document Assistant

This project was built as part of a hands-on **Langchain training** to explore how to build a document-based chatbot using modern tools in the AI ecosystem.

---

## 📌 About the Project

The core idea:  
> **Upload a document → Ask questions → Get smart, contextual answers.**

We used **Langchain**, **Streamlit**, and **FAISS** to build a simple app where users can upload documents (like PDFs) and interact with them through a conversational interface.

---
🔗 **Check it out live:** [Open App on Streamlit](https://ai-doc-assitant.streamlit.app/ )

## 💡 Project Objective

Build an AI Assistant that:

- 📄 Lets a user **upload a document** (PDF, TXT, etc.)
- 💬 Provides a **chat interface** where the user can ask questions about the uploaded document
- 🧠 Uses **LangChain**, **embeddings**, and **LLMs** to retrieve and respond with relevant document chunks
- 🔁 Maintains **short-term memory** of the conversation for more coherent interactions
- 💾 Optionally, includes functionality to **save chat history** based on session ID




---

## 🧰 Tech Stack

| Tool          | Purpose                                |
|---------------|----------------------------------------|
| **Streamlit** | UI and chat interface                  |
| **Langchain** | Document parsing, memory, prompt flow  |
| **FAISS**     | Vector store for fast document search  |
| **Gemini API**| LLM used for generating responses      |
| **pypdf**     | PDF document parsing                   |
| **tiktoken**  | Token counting                         |
| **dotenv**    | API key and environment management     |

---

## 💻 How to Run It

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/ai-doc-assistant.git
   cd ai-doc-assistant
2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
3. **Create a .env file**
Fill in your keys:
    ```bash
   GEMINI_API_KEY = your_key_here
4. **Run the app**
     ```bash
     streamlit run app.py
