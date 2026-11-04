import os
import logging
try:
    from langchain_community.vectorstores import Chroma
except ImportError:
    from langchain.vectorstores import Chroma

try:
    from langchain_community.embeddings import HuggingFaceBgeEmbeddings
except ImportError:
    from langchain.embeddings import HuggingFaceBgeEmbeddings

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter

try:
    from langchain_classic.chains import ConversationalRetrievalChain
except ImportError:
    from langchain.chains import ConversationalRetrievalChain

try:
    from langchain_openai import ChatOpenAI
except ImportError:
    from langchain.chat_models import ChatOpenAI

try:
    from langchain_classic.memory import ConversationBufferMemory
except ImportError:
    from langchain.memory import ConversationBufferMemory

try:
    from langchain_core.prompts import ChatPromptTemplate
except ImportError:
    from langchain.prompts import ChatPromptTemplate

# ✅ Ensure log directory exists
os.makedirs("logs", exist_ok=True)

# ✅ Setup logging
logging.basicConfig(
    filename="logs/docbot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

PERSIST_DIR = "chromadb_store"

def setup_qa_chain(documents, api_key, model=None, chunk_size=1000, chunk_overlap=50, top_k=3):
    logging.info("Splitting documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_documents(documents)

    logging.info("Initializing embeddings and persistent ChromaDB...")
    embeddings = HuggingFaceBgeEmbeddings(
        model_name="BAAI/bge-small-en",
        encode_kwargs={"normalize_embeddings": True}
    )
    vectorstore = Chroma.from_documents(
        chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )
    if hasattr(vectorstore, "persist"):
        try:
            vectorstore.persist()
        except Exception:
            pass
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})

    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

    selected_model = model or os.getenv("LLM_MODEL", "openrouter/free")

    llm = ChatOpenAI(
        model=selected_model,
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.7,
        streaming=True
    )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "You are a helpful AI medical assistant. Only answer questions based on the provided context. "
         "If the context lacks the necessary information, respond with: "
         "'I'm sorry, I don't have enough information to answer that.'\n\nContext:\n{context}"),
        ("human", "{question}"),
    ])

    logging.info("LLM + Retriever chain ready.")
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt}
    )
