try:
    from langchain_community.document_loaders import PyMuPDFLoader, UnstructuredWordDocumentLoader, WebBaseLoader
except ImportError:
    from langchain.document_loaders import PyMuPDFLoader, UnstructuredWordDocumentLoader, WebBaseLoader

try:
    from langchain_core.documents import Document
except ImportError:
    from langchain.docstore.document import Document
from youtube_transcript_api import YouTubeTranscriptApi
from pathlib import Path
import tempfile
import streamlit as st

def load_pdf_docx(files):
    documents = []
    for file in files:
        suffix = Path(file.name).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file.read())
            path = tmp.name
        if suffix == ".pdf":
            loader = PyMuPDFLoader(path)
        elif suffix == ".docx":
            loader = UnstructuredWordDocumentLoader(path)
        else:
            continue
        documents.extend(loader.load())
    return documents

def load_websites(urls):
    docs = []
    for url in urls:
        url = url.strip()
        if not url:
            continue
        try:
            loader = WebBaseLoader(url)
            docs.extend(loader.load())
        except Exception as e:
            st.error(f"Error loading {url}: {e}")
    return docs

def load_youtube(urls):
    docs = []
    for link in urls:
        link = link.strip()
        if not link:
            continue
        try:
            if "v=" in link:
                video_id = link.split("v=")[-1].split("&")[0]
            elif "youtu.be/" in link:
                video_id = link.split("youtu.be/")[-1].split("?")[0]
            else:
                video_id = link.strip()
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            text = " ".join([t["text"] for t in transcript])
            docs.append(Document(page_content=text))
        except Exception as e:
            st.error(f"Error loading YouTube link {link}: {e}")
    return docs

def load_all_documents(files, websites, youtube_links):
    docs = []
    docs += load_pdf_docx(files)
    docs += load_websites(websites)
    docs += load_youtube(youtube_links)
    return docs
