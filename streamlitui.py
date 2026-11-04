import streamlit as st
import base64
import os

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# def set_bg_image(image_path):
#     encoded = get_base64_image(image_path)
#     st.markdown(
#         f"""
#         <style>
#         .stApp {{
#             background-image: url("data:image/jpg;base64,{encoded}");
#             background-size: cover;
#             background-position: center;
#             background-repeat: no-repeat;
#             background-attachment: fixed;
#         }}
#         </style>
#         """, unsafe_allow_html=True
#     )

def set_bg_image(image_path):
    encoded = get_base64_image(image_path)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255,255,255,0.7), rgba(255,255,255,0.7)),
                              url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """, unsafe_allow_html=True
    )


def setup_ui():
    st.markdown("<h1 style='text-align:center;'>DocBot Advisor</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center;'>AI-powered assistant for medical documents and research.</h4>", unsafe_allow_html=True)

    with st.sidebar:
        st.header("⚙️ Configuration")
        st.session_state.embedding_model = st.selectbox("Embedding Model", ["BAAI/bge-small-en"])

        llm_options = {
            "Auto Free (Best Available)": "openrouter/free",
            "Google Gemma 4 31B (Free)": "google/gemma-4-31b-it:free",
            "Ling 3.0 Santé Medical (Free)": "inclusionai/ling-3.0-flash-sante:free",
            "Qwen 3.8 27B (Free)": "qwen/qwen3.8-27b:free",
            "NVIDIA Nemotron Lightning (Free)": "nvidia/nemotron-3.5-lightning:free"
        }

        st.session_state.llm_label = st.selectbox("LLM Model (Free)", list(llm_options.keys()))
        st.session_state.llm_model = llm_options[st.session_state.llm_label]

        st.session_state.chunk_size = st.slider("Chunk Size", 100, 2000, 1000, step=100)
        st.session_state.chunk_overlap = st.slider("Chunk Overlap", 0, 200, 50, step=10)
        st.session_state.top_k = st.slider("Top-K Retrieval", 1, 10, 3)

        st.session_state.uploaded_files = st.file_uploader("Upload PDFs/DOCX", accept_multiple_files=True, type=["pdf", "docx"])
        st.session_state.website_urls = st.text_area("Website URLs (comma-separated)").split(",")
        st.session_state.youtube_urls = st.text_area("YouTube URLs (comma-separated)").split(",")
