import streamlit as st
from dataloader import load_all_documents
from llm import setup_qa_chain
from streamlitui import setup_ui, set_bg_image
import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# ✅ Load .env variables if available
load_dotenv()

# ✅ Set page config FIRST (before any other Streamlit command)
st.set_page_config(page_title="DocBot RAG Assistant", layout="wide")

# ✅ Ensure required directories exist
os.makedirs("logs", exist_ok=True)
os.makedirs("chat_exports", exist_ok=True)

# ✅ Setup background and UI
set_bg_image("bg/sample5.jpg")
setup_ui()

# --- Process Button ---
if st.sidebar.button("Process Data"):
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
    uploaded_files = st.session_state.uploaded_files
    websites = [url.strip() for url in st.session_state.website_urls if url.strip()]
    youtube_links = [url.strip() for url in st.session_state.youtube_urls if url.strip()]

    if not api_key:
        st.error("⚠️ API key missing! Please add `OPENROUTER_API_KEY` to your `.env` file.")
        st.stop()

    if not (uploaded_files or websites or youtube_links):
        st.warning("⚠️ Please provide at least one data source (document, website, or YouTube link).")
        st.stop()

    with st.spinner("🔄 Loading documents..."):
        docs = load_all_documents(uploaded_files, websites, youtube_links)

    if not docs:
        st.warning("No content loaded.")
        st.stop()

    with st.spinner("⚙️ Processing with LLM..."):
        model_choice = st.session_state.get("llm_model")
        chunk_sz = st.session_state.get("chunk_size", 1000)
        chunk_ov = st.session_state.get("chunk_overlap", 50)
        top_k = st.session_state.get("top_k", 3)
        qa_chain = setup_qa_chain(
            docs,
            api_key,
            model=model_choice,
            chunk_size=chunk_sz,
            chunk_overlap=chunk_ov,
            top_k=top_k
        )
        st.session_state.qa_chain = qa_chain
        st.session_state.chat_history = []

    st.success("✅ Ready to chat!")

# --- Chat Interface ---
if "qa_chain" in st.session_state:
    user_input = st.chat_input("Ask something about your data")
    if user_input:
        with st.spinner("🤖 Thinking..."):
            response = st.session_state.qa_chain.invoke({"question": user_input})
            answer = response.get("answer", "No answer returned.")
            st.session_state.chat_history.append({"user": user_input, "assistant": answer})

    for entry in st.session_state.chat_history:
        st.markdown(f"**You:** {entry['user']}")
        st.markdown(f"**Assistant:** {entry['assistant']}")
        st.markdown("---")

# --- Export to CSV ---
def export_chat_to_csv(chat_history, filename="chat_history.csv"):
    if not chat_history:
        st.warning("No chat history to save.")
        return
    df = pd.DataFrame(chat_history)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    full_path = os.path.join("chat_exports", f"{filename}_{timestamp}.csv")
    df.to_csv(full_path, index=False)
    st.success(f"Chat saved to `{full_path}`")

if "chat_history" in st.session_state and st.session_state.chat_history:
    if st.button("📥 Download Chat as CSV"):
        export_chat_to_csv(st.session_state.chat_history)
