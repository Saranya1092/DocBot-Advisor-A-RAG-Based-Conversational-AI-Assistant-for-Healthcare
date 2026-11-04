# 📘 DocBot: A RAG-Based AI Assistant for Document QA

DocBot is a Retrieval-Augmented Generation (RAG) assistant built with LangChain and Streamlit that allows users to upload documents (PDF, DOCX, TXT, PNG), extract content, embed them using BGE embeddings, and ask questions interactively. It uses a local Ollama models for LLM responses, ChromaDB as the vector store, and stores conversations for analysis.

Medical Assistant (Rural Clinics or Clinics with Low Digital Literacy)
Upload treatment protocols, drug manuals, common diseases FAQs.
Doctors or staff can ask natural questions, even via voice → text.
---

## 📐 Architecture Overview

### 1. **Document Loader and Parser**

* Uses `unstructured.partition.auto` to parse various file types (PDF, DOCX, PNG, TXT).
* Extracted documents are converted to LangChain `Document` format.

### 2. **Chunking and Embeddings**

* Text is split using `RecursiveCharacterTextSplitter`.
* Embeddings are generated via `BGE` (Ollama embeddings) using `OllamaEmbeddings` from LangChain.

### 3. **Vector Store**

* ChromaDB used as vector store with persistent storage (`persist_directory="db"`).
* Allows similarity search during query time.

### 4. **LLM and Retrieval Chain**

* Local Ollama model (`qwen:7b`) loaded with streaming enabled.
* A Conversational Retrieval QA chain is built using LangChain's `ConversationalRetrievalChain`.
* Chat history is preserved with `ConversationBufferMemory`.

### 5. **UI with Streamlit**

* Sidebar for file uploads and configuration.
* Main panel for asking questions.
* Chat history displayed in a ChatGPT-style layout.
* Charts-related questions and answers are saved to `chat_exports/charts.csv`.

### 6. **Logging**

* Logs are written to `logs/docbot.log` using Python’s logging module.
* Folders like `logs/` and `chat_exports/` are created automatically if missing.

---

## 🧱 Project Structure

```bash
DocBot/
├── app.py                     # Main Streamlit entry point
├── streamlitui.py             # UI rendering logic
├── dataloader.py              # File upload and document loading
├── llm.py                     # Ollama LLM setup, QA chain, logging
├── chat_exports/
│   └── charts.csv             # Saved chart-based Q&A history
├── logs/
│   └── docbot.log             # Application logs
├── db/                        # Persistent ChromaDB directory
├── bg/
│   └── sample1.jpg            # Background image for Streamlit UI
└── README.md                  # This file
```

---

## 📦 Dependencies

* `streamlit`
* `langchain`
* `chromadb`
* `unstructured`
* `Ollama` (with local `qwen:7b` model)
* `pandas`
* `tiktoken`
* `python-dotenv`

---

## 🚀 How to Run

1. **Install dependencies**

```bash
pip install -r requirements.txt
```


3. **Launch the app**

```bash
streamlit run app.py
```

---

## 🧠 Key Features

* 📄 Multi-format document ingestion
* 🧩 BGE embeddings + ChromaDB vector search
* 🤖 Local RAG with ollama apis model
* 💬 Persistent chat history and chart question logging
* 🖼️ Custom background and full-width layout
* 🗃️ Persistent vector store (no re-embedding)

---

## 📈 Future Improvements

* Add rerankers (e.g., BGE M3 Reranker)
* Include feedback buttons for responses
* Enable admin panel for chat review
* Auto-categorize charts vs non-chart queries

---

## 📝 Maintained by

Hari R.
Built with ❤️ using LangChain, Chroma, and Streamlit.
