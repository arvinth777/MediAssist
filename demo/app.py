import os, streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

INDEX_PATH = os.path.join(os.path.dirname(__file__), "faiss_index")
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL   = "google/flan-t5-base"   # Much faster than phi-2, good quality

@st.cache_resource
def get_retriever():
    embed = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vs = FAISS.load_local(INDEX_PATH, embed, allow_dangerous_deserialization=True)
    return vs.as_retriever(search_kwargs={"k": 3})

@st.cache_resource
def get_llm():
    tok = AutoTokenizer.from_pretrained(LLM_MODEL)
    mdl = AutoModelForSeq2SeqLM.from_pretrained(LLM_MODEL)
    return pipeline("text2text-generation", model=mdl, tokenizer=tok, max_new_tokens=280)

def answer(q, retriever, llm):
    docs = retriever.invoke(q)
    context = "\n\n".join([f"[{i+1}] {d.page_content}" for i, d in enumerate(docs)])
    prompt = (
        "You are a careful medical assistant for maternal health. Use ONLY the context. "
        "If unsure, say you don't know.\n\n"
        f"Context:\n{context}\n\nQuestion: {q}\nAnswer with citations like [1]/[2]/[3]:"
    )
    out = llm(prompt)[0]["generated_text"]
    return out, docs

st.title("MediAssist RAG — Maternal Health QA (Demo)")
st.caption("Local RAG: FAISS + MiniLM embeddings + FLAN-T5 (faster & lighter than Phi-2).")

q = st.text_input("Ask a question (e.g., 'Complications of gestational diabetes?')")
if st.button("Answer") and q.strip():
    retriever = get_retriever(); llm = get_llm()
    ans, docs = answer(q, retriever, llm)
    st.write(ans)
    with st.expander("Retrieved Context"):
        for i, d in enumerate(docs):
            st.markdown(f"**[{i+1}] {d.metadata.get('source','?')}**\n\n{d.page_content[:900]}…")
