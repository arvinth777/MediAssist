import os, streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

INDEX_PATH = os.path.join(os.path.dirname(__file__), "faiss_index")
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

@st.cache_resource
def get_retriever():
    embed = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vs = FAISS.load_local(INDEX_PATH, embed, allow_dangerous_deserialization=True)
    return vs.as_retriever(search_kwargs={"k": 3})

def answer_simple(q, retriever):
    """Fast version - just retrieve relevant docs, no LLM generation"""
    docs = retriever.invoke(q)
    context = "\n\n".join([f"**[{i+1}] {d.metadata.get('source', '?')}**\n{d.page_content}" 
                           for i, d in enumerate(docs)])
    return context, docs

st.title("MediAssist RAG — Maternal Health QA (Demo) - FAST")
st.caption("Retrieval-only mode: FAISS + MiniLM embeddings (no slow LLM).")

q = st.text_input("Ask a question (e.g., 'Complications of gestational diabetes?')")
if st.button("Search") and q.strip():
    retriever = get_retriever()
    context, docs = answer_simple(q, retriever)
    
    st.subheader("📚 Most Relevant Information:")
    st.markdown(context)
    
    st.info("💡 **Tip**: Review the retrieved context above to find your answer. "
            "This is much faster than waiting for LLM generation!")
