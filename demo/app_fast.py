import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

INDEX_PATH = os.path.join(os.path.dirname(__file__), "faiss_index")
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

@st.cache_resource
def get_retriever():
    """Load FAISS vector store and return retriever."""
    try:
        embed = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
        vs = FAISS.load_local(INDEX_PATH, embed, allow_dangerous_deserialization=True)
        return vs.as_retriever(search_kwargs={"k": 3})
    except Exception as e:
        st.error(f"❌ Error loading FAISS index: {e}")
        st.info("💡 Try running: `python demo/ingest.py` to rebuild the index")
        st.stop()

def answer_simple(q, retriever):
    """Fast retrieval-only - no LLM generation."""
    try:
        docs = retriever.invoke(q)
        if not docs:
            return "No relevant documents found.", []
        return docs, docs
    except Exception as e:
        st.error(f"Error: {e}")
        return [], []

st.set_page_config(page_title="MediAssist RAG (Fast)", page_icon="⚡")
st.title("⚡ MediAssist RAG — Fast Retrieval Mode")
st.caption("Instant semantic search with FAISS + MiniLM embeddings (no LLM)")
st.warning("⚠️ Educational demo only. Not for medical advice.")

q = st.text_input("Search the corpus:", placeholder="e.g., gestational diabetes complications")

if st.button("🔍 Search", type="primary") and q.strip():
    with st.spinner("�� Searching..."):
        retriever = get_retriever()
        docs, _ = answer_simple(q, retriever)
    
    if docs:
        st.success(f"✅ Found {len(docs)} relevant passages")
        
        for i, d in enumerate(docs):
            with st.container():
                st.markdown(f"### 📄 [{i+1}] {d.metadata.get('source', 'Unknown')}")
                st.write(d.page_content)
                st.divider()
    else:
        st.warning("No relevant information found")

# Sidebar
with st.sidebar:
    st.header("⚡ Fast Mode")
    st.markdown("""
    This version skips LLM generation and shows you the raw retrieved passages instantly.
    
    **Speed**: < 1 second  
    **Output**: Top 3 most relevant document chunks
    """)
    
    st.header("🔄 Want Generated Answers?")
    st.markdown("""
    Use `demo/app.py` for AI-generated answers with citations.
    
    Trade-off: 5-10 seconds per query
    """)
    
    st.header("📊 How It Works")
    st.markdown("""
    1. Your question → embedded to vector
    2. FAISS finds top-3 similar chunks
    3. Display results immediately
    """)
