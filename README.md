# 🏥 DocBot Advisor - Healthcare RAG Assistant

> A Retrieval-Augmented Generation (RAG) powered conversational AI assistant designed for healthcare environments, enabling natural language queries over medical documents, protocols, and guidelines.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.65.0-FF4B4B)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-1.4.3-green)](https://www.langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Use Cases](#use-cases)
- [Technologies](#technologies)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**DocBot Advisor** is a specialized RAG-based AI assistant built to democratize access to medical knowledge in rural clinics, healthcare facilities, and environments with limited digital literacy. It allows healthcare professionals to:

- Upload medical documents (PDFs, DOCX, TXT, images)
- Ingest content from websites and YouTube videos
- Ask natural language questions about treatment protocols, drug interactions, and medical guidelines
- Receive contextual, accurate responses powered by advanced LLMs

Perfect for rural healthcare workers, medical students, and clinical staff who need quick access to reliable medical information.

---

## ✨ Features

- **🗂️ Multi-Format Document Support**: PDF, DOCX, TXT, PNG image extraction
- **🌐 Web & Video Ingestion**: Extract content from websites and YouTube transcripts
- **🧠 Advanced RAG Pipeline**: ChromaDB vector store + OpenRouter/OpenAI LLMs
- **💬 Conversational Interface**: Chat-style UI with persistent conversation history
- **📊 Query Analytics**: Automatic logging and export of chart-related queries
- **🔒 Privacy-First**: Local vector storage, secure API key management
- **🎨 Custom UI**: Healthcare-themed interface with background customization
- **📝 Comprehensive Logging**: Detailed application logs for debugging and monitoring

---

## 🏗️ Architecture

```
┌─────────────────┐
│  User Interface │  ← Streamlit Web App
└────────┬────────┘
         │
┌────────▼────────┐
│ Document Loader │  ← PDF, DOCX, TXT, PNG, Web, YouTube
└────────┬────────┘
         │
┌────────▼────────┐
│ Text Chunking   │  ← RecursiveCharacterTextSplitter
└────────┬────────┘
         │
┌────────▼────────┐
│   Embeddings    │  ← Sentence Transformers / OpenAI
└────────┬────────┘
         │
┌────────▼────────┐
│   ChromaDB      │  ← Persistent Vector Store
└────────┬────────┘
         │
┌────────▼────────┐
│  LLM (OpenAI/   │  ← Conversational Retrieval Chain
│   OpenRouter)   │
└────────┬────────┘
         │
┌────────▼────────┐
│    Response     │  ← Contextual Answer + Sources
└─────────────────┘
```

### Key Components

1. **Document Loader**: Parses multiple formats using `unstructured` library
2. **Embeddings**: Converts text chunks to vector representations
3. **Vector Store**: ChromaDB with persistent storage for efficient similarity search
4. **LLM Chain**: Conversational retrieval chain with memory
5. **UI Layer**: Streamlit-based interactive interface

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- OpenAI API key or OpenRouter API key

### Step 1: Clone the Repository

```bash
git clone https://github.com/Saranya1092/DocBot-Advisor-A-RAG-Based-Conversational-AI-Assistant-for-Healthcare.git
cd DocBot-Advisor-A-RAG-Based-Conversational-AI-Assistant-for-Healthcare
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### 1. Set Up API Keys

Create a `.env` file in the project root:

```bash
# Copy the example
copy .env.example .env   # Windows
cp .env.example .env     # Linux/Mac
```

Add your API key to `.env`:

```env
# Option 1: OpenRouter (supports multiple models)
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# Option 2: OpenAI (direct)
OPENAI_API_KEY=sk-your-openai-key-here
```

**Get API Keys:**
- OpenRouter: [https://openrouter.ai/keys](https://openrouter.ai/keys)
- OpenAI: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### 2. Configure Application Settings (Optional)

Edit parameters in the Streamlit sidebar:
- **Chunk Size**: 500-2000 (default: 1000)
- **Chunk Overlap**: 0-200 (default: 50)
- **Top K Results**: 1-10 (default: 3)
- **LLM Model**: Choose from available models

---

## 💻 Usage

### Start the Application

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

### Using DocBot

1. **Upload Documents** (Sidebar)
   - Click "Browse files" to upload PDF, DOCX, TXT, or PNG files
   - Or provide website URLs
   - Or paste YouTube video links

2. **Process Data**
   - Click "Process Data" button
   - Wait for document processing and embedding

3. **Ask Questions**
   - Type your question in the chat input
   - Press Enter or click Send
   - View contextual responses with source citations

4. **Export Conversations**
   - Chart-related queries are auto-saved to `chat_exports/charts.csv`
   - Full logs available in `logs/docbot.log`

---

## 📁 Project Structure

```
DocBot-Advisor/
│
├── app.py                          # Main application entry point
├── streamlitui.py                  # UI rendering and styling
├── dataloader.py                   # Document loading and parsing
├── llm.py                          # LLM setup and QA chain
├── build_review_ppt.py             # Review presentation generator
│
├── requirements.txt                # Python dependencies
├── .env                            # API keys (not in git)
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
│
├── bg/                             # Background images
│   ├── sample1.jpg
│   ├── sample2.jpg
│   └── ...
│
├── DOC/                            # Documentation files
│   ├── Review 1.docx
│   ├── MTech_SE_REVIEW_2_DocBot_Verified.md
│   └── ...
│
├── localresource/                  # Sample datasets
│   └── DietaryGuidelinesforNINwebsite.pdf
│
├── data/                           # Uploaded documents (runtime)
├── chat_exports/                   # Exported conversations
│   └── charts.csv
│
├── logs/                           # Application logs
│   └── docbot.log
│
├── chromadb_store/                 # Vector database (persistent)
└── chroma_db/                      # Alternative vector store
```

---

## 🏥 Use Cases

### 1. Rural Healthcare Clinics
> Upload treatment protocols and diagnostic guidelines. Healthcare workers can ask questions in their native language about symptoms, treatments, and drug dosages.

### 2. Medical Training
> Students can upload textbooks and research papers, then query complex medical concepts interactively.

### 3. Clinical Decision Support
> Doctors can quickly reference drug interactions, dosage guidelines, and treatment protocols during patient consultations.

### 4. Health Information Kiosks
> Deploy in community health centers for public health education on nutrition, preventive care, and common illnesses.

### 5. Telemedicine Support
> Remote consultations can be augmented with AI-assisted information retrieval from medical databases.

---

## 🛠️ Technologies

| Category | Technology |
|----------|-----------|
| **Frontend** | Streamlit |
| **LLM Framework** | LangChain |
| **Vector Database** | ChromaDB |
| **Embeddings** | Sentence Transformers, OpenAI |
| **LLM Providers** | OpenAI, OpenRouter |
| **Document Parsing** | Unstructured, PyMuPDF |
| **Web Scraping** | Requests, BeautifulSoup |
| **Video Transcripts** | youtube-transcript-api |
| **Data Processing** | Pandas, NumPy |
| **Logging** | Python logging module |

---

## 🔧 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'streamlit'`
```bash
pip install -r requirements.txt
```

**Issue**: `API key missing` error
- Ensure `.env` file exists in project root
- Verify `OPENROUTER_API_KEY` or `OPENAI_API_KEY` is set

**Issue**: ChromaDB persistence errors
```bash
# Clear vector database
Remove-Item -Recurse -Force chromadb_store/  # Windows
rm -rf chromadb_store/                        # Linux/Mac
```

**Issue**: Streamlit port already in use
```bash
streamlit run app.py --server.port 8502
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

**Saranya** - [@Saranya1092](https://github.com/Saranya1092)

**Project Supervisor**: Hari R.

---

## 🙏 Acknowledgments

- Built with ❤️ using LangChain, ChromaDB, and Streamlit
- Inspired by the need for accessible healthcare information in underserved communities
- Special thanks to the open-source AI community

---

## 📧 Contact

For questions, suggestions, or collaborations:

- GitHub Issues: [Report a bug](https://github.com/Saranya1092/DocBot-Advisor-A-RAG-Based-Conversational-AI-Assistant-for-Healthcare/issues)
- Email: [Contact via GitHub](https://github.com/Saranya1092)

---

## 🗺️ Roadmap

- [ ] Add support for voice input/output
- [ ] Implement multi-language support (Hindi, Tamil, Telugu)
- [ ] Add reranking for improved retrieval accuracy
- [ ] Create admin dashboard for usage analytics
- [ ] Deploy as web service (Docker + Kubernetes)
- [ ] Add user feedback mechanism
- [ ] Integrate with hospital management systems

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star!**

Made with 💙 for Healthcare Professionals

</div>
