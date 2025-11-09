import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

INDEX_PATH = os.path.join(os.path.dirname(__file__), "faiss_index")
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "google/flan-t5-base"

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

@st.cache_resource
def get_llm():
    """Load and cache the FLAN-T5 model."""
    try:
        with st.spinner("🔄 Loading FLAN-T5 model (first time only, ~250MB)..."):
            tok = AutoTokenizer.from_pretrained(LLM_MODEL)
            mdl = AutoModelForSeq2SeqLM.from_pretrained(LLM_MODEL)
            return pipeline("text2text-generation", model=mdl, tokenizer=tok, max_new_tokens=280)
    except Exception as e:
        st.error(f"❌ Error loading LLM: {e}")
        st.stop()

def answer(q, retriever, llm):
    """Generate answer using RAG with retrieved context."""
    try:
        docs = retriever.invoke(q)
        if not docs:
            return "No relevant information found in the corpus.", []
        
        context = "\n\n".join([f"[{i+1}] {d.page_content}" for i, d in enumerate(docs)])
        prompt = (
            "You are a medical assistant for maternal health. Use ONLY the context provided. "
            "If unsure, say you don't know.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {q}\n\n"
            "Answer with citations [1]/[2]/[3]:"
        )
        out = llm(prompt)[0]["generated_text"]
        return out, docs
    except Exception as e:
        return f"Error: {e}", []

st.set_page_config(page_title="MediAssist RAG", page_icon="🏥")
st.title("🏥 MediAssist RAG — Maternal Health QA")
st.caption("Local RAG: FAISS + MiniLM + FLAN-T5-base")
st.warning("⚠️ Educational demo only. Not for medical advice.")

q = st.text_input("Ask a question:", placeholder="e.g., Complications of gestational diabetes?")

if st.button("🔍 Generate Answer") and q.strip():
    with st.spinner("🤔 Generating answer..."):
        retriever = get_retriever()
        llm = get_llm()
        ans, docs = answer(q, retriever, llm)
    
    st.markdown("### 💡 Answer")
    st.write(ans)
    
    if docs:
        with st.expander("📚 Retrieved Sources"):
            for i, d in enumerate(docs):
                st.markdown(f"**[{i+1}] {d.metadata.get('source', '?')}**")
                st.text(d.page_content[:700] + "...")
                st.divider()
