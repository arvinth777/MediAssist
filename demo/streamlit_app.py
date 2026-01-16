import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Configuration
INDEX_PATH = os.path.join(os.path.dirname(__file__), "faiss_index")
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "google/flan-t5-base"

# Example questions from EXAMPLES.md
EXAMPLE_QUESTIONS = [
    "What are complications of gestational diabetes?",
    "What are risk factors for preeclampsia?",
    "What causes postpartum hemorrhage?",
    "Signs of preterm birth?",
    "How is anemia in pregnancy diagnosed?",
    "What ultrasound measurements are taken during pregnancy?",
    "What is fetal growth restriction?",
    "How is anemia in pregnancy treated?",
    "What are components of antenatal care?",
    "What infections are screened in pregnancy?",
]

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

def answer_fast(q, retriever):
    """Fast retrieval-only mode - returns top passages."""
    try:
        docs = retriever.invoke(q)
        if not docs:
            return "No relevant information found in the corpus.", []
        return None, docs  # Return None for answer to indicate retrieval-only mode
    except Exception as e:
        return f"Error: {e}", []

def answer_full(q, retriever, llm):
    """Full RAG mode - generates answer using LLM."""
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

# Page configuration
st.set_page_config(
    page_title="MediAssist RAG",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "current_question" not in st.session_state:
    st.session_state.current_question = ""

# Sidebar
with st.sidebar:
    st.title("🏥 MediAssist RAG")
    st.markdown("---")
    
    # Mode selection
    st.subheader("⚙️ Mode")
    mode = st.radio(
        "Select mode:",
        ["Fast Retrieval", "Full RAG"],
        help="Fast: Instant retrieval (<1s) | Full: AI-generated answers (5-10s)"
    )
    
    st.markdown("---")
    
    # Example questions
    st.subheader("💡 Example Questions")
    st.caption("Click to auto-fill:")
    
    for i, example in enumerate(EXAMPLE_QUESTIONS[:5]):  # Show first 5
        if st.button(f"📌 {example[:40]}...", key=f"ex_{i}", use_container_width=True):
            st.session_state.current_question = example
            st.rerun()
    
    with st.expander("➕ More examples"):
        for i, example in enumerate(EXAMPLE_QUESTIONS[5:], start=5):
            if st.button(f"📌 {example[:40]}...", key=f"ex_{i}", use_container_width=True):
                st.session_state.current_question = example
                st.rerun()
    
    st.markdown("---")
    
    # Info
    st.subheader("ℹ️ About")
    st.caption("**Tech Stack:**")
    st.caption("• FAISS Vector Search")
    st.caption("• MiniLM Embeddings")
    st.caption("• FLAN-T5 Language Model")
    st.caption("• 10 Maternal Health Docs")
    
    st.markdown("---")
    
    # Clear history
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.history = []
        st.rerun()

# Main content
st.title("🏥 MediAssist-RAG: Maternal Health Q&A")
st.markdown("**AI-powered question answering system for maternal health education**")

# Medical disclaimer
st.warning("⚠️ **Medical Disclaimer:** This is an educational demo only. Not a substitute for professional medical advice.")

st.markdown("---")

# Question input
col1, col2 = st.columns([4, 1])
with col1:
    question = st.text_area(
        "Enter your question:",
        value=st.session_state.current_question,
        placeholder="e.g., What are the signs of preeclampsia?",
        height=100,
        key="question_input"
    )
with col2:
    st.markdown("<br>", unsafe_allow_html=True)  # Spacing
    submit_button = st.button("🔍 Get Answer", type="primary", use_container_width=True)

# Process question
if submit_button and question.strip():
    # Clear the current_question from session state
    st.session_state.current_question = ""
    
    # Load retriever
    retriever = get_retriever()
    
    if mode == "Fast Retrieval":
        with st.spinner("🔎 Searching knowledge base..."):
            ans, docs = answer_fast(question, retriever)
    else:  # Full RAG
        with st.spinner("🤔 Generating AI answer... (this may take 5-10 seconds)"):
            llm = get_llm()
            ans, docs = answer_full(question, retriever, llm)
    
    # Add to history
    st.session_state.history.append({
        "question": question,
        "answer": ans,
        "docs": docs,
        "mode": mode
    })

# Display conversation history
if st.session_state.history:
    st.markdown("---")
    st.subheader("💬 Conversation History")
    
    # Display in reverse order (newest first)
    for idx, item in enumerate(reversed(st.session_state.history)):
        actual_idx = len(st.session_state.history) - idx - 1
        
        with st.container():
            # Question
            st.markdown(f"**Q{actual_idx + 1}:** {item['question']}")
            
            # Answer
            if item['answer']:
                st.markdown("**Answer:**")
                st.info(item['answer'])
            else:
                st.markdown("**Retrieved Passages:**")
            
            # Sources
            if item['docs']:
                with st.expander(f"📚 View {len(item['docs'])} Retrieved Sources"):
                    for i, d in enumerate(item['docs']):
                        source_name = d.metadata.get('source', 'Unknown')
                        st.markdown(f"**[{i+1}] {source_name}**")
                        st.text(d.page_content[:500] + ("..." if len(d.page_content) > 500 else ""))
                        if i < len(item['docs']) - 1:
                            st.divider()
            
            st.markdown(f"*Mode: {item['mode']}*")
            st.markdown("---")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        Built with ❤️ for maternal healthcare education | 
        <a href='https://github.com/arvinth777' target='_blank'>GitHub</a>
    </div>
    """,
    unsafe_allow_html=True
)
