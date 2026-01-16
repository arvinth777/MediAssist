# MediAssist RAG - Maternal Health QA System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mediassist-rag-9mblcgtthnnenruigzvydn.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **🚀 [Try the Live Demo](https://mediassist-rag-9mblcgtthnnenruigzvydn.streamlit.app/)** - Interactive maternal health Q&A powered by AI

A Retrieval-Augmented Generation (RAG) system for maternal health question answering, built with FAISS vector search and local language models.

## 🎯 Features

- **Fast semantic search** using FAISS vector database
- **Two modes**: Full LLM generation or instant retrieval-only
- **Local deployment** - runs entirely on your machine
- **10 curated documents** on maternal health topics (pregnancy, complications, risk factors)
- **Citation support** - answers reference source documents

## 🏗️ Architecture

```
┌─────────────────┐
│  User Question  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│  Embedding Model            │
│  (all-MiniLM-L6-v2)        │
└────────┬────────────────────┘
         │ Query Vector
         ▼
┌─────────────────────────────┐
│  FAISS Vector Store         │
│  (10 maternal health docs)  │
└────────┬────────────────────┘
         │ Top-3 Relevant Passages
         ▼
┌─────────────────────────────┐
│  Mode Selection             │
├─────────────────────────────┤
│  Fast: Return passages      │
│  Full: LLM Generation       │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  FLAN-T5 Language Model     │
│  (Optional)                 │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Answer with Citations      │
└─────────────────────────────┘
```

## 📁 Project Structure

```
demo/
├── corpus/            # 10 maternal health text files
├── faiss_index/       # Pre-built FAISS vector store
├── streamlit_app.py   # ⭐ Enhanced demo (recommended)
├── app.py             # Full RAG app with FLAN-T5
├── app_fast.py        # Fast retrieval-only version
├── ingest.py          # Script to build FAISS index
└── requirements.txt   # Python dependencies (pinned versions)
setup.sh               # One-command installation script
EXAMPLES.md            # 15 sample queries
LICENSE                # MIT License
```

## 🌐 Live Demo

**Try it now:** [https://mediassist-rag-9mblcgtthnnenruigzvydn.streamlit.app/](https://mediassist-rag-9mblcgtthnnenruigzvydn.streamlit.app/)

The live demo includes:
- 🎛️ **Dual Mode**: Toggle between Fast Retrieval and Full RAG
- 💡 **Example Questions**: Pre-loaded maternal health queries
- 💬 **Conversation History**: Track your Q&A session
- 📚 **Source Citations**: View retrieved medical documents

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
bash setup.sh
```

This will automatically:
1. Check Python version
2. Install all dependencies
3. Build the FAISS index
4. Provide instructions to run the app

### Option 2: Manual Setup

**1. Install Dependencies**

```bash
pip install -r demo/requirements.txt
```

**2. Build the Vector Index**

```bash
python demo/ingest.py
```

This will:
- Load all `.txt` files from `demo/corpus/`
- Create embeddings using `sentence-transformers/all-MiniLM-L6-v2`
- Save FAISS index to `demo/faiss_index/`

**3. Run the App**

**Option A: Enhanced Demo (Recommended) 🌟**
```bash
streamlit run demo/streamlit_app.py
```
Features:
- Toggle between Fast Retrieval and Full RAG modes
- Example questions in sidebar
- Conversation history
- Modern, professional UI

**Option B: Fast retrieval-only (< 1 second response)**
```bash
streamlit run demo/app_fast.py
```

**Option C: Full RAG with LLM (5-10 seconds response)**
```bash
streamlit run demo/app.py
```

## 🔍 How It Works

1. **Ingestion**: Medical documents are chunked (500 chars) and embedded into a FAISS vector store
2. **Retrieval**: User questions are matched against the vector store to find top-3 relevant passages
3. **Generation** (optional): A local LLM (FLAN-T5) generates answers using only the retrieved context
4. **Citation**: Answers reference source documents [1], [2], [3]

## 📚 Data Sources

The `demo/corpus/` folder contains 10 text files on maternal health:
- Anemia in pregnancy
- Antenatal care basics
- Fetal growth restriction
- Fetal ultrasound markers
- Gestational diabetes complications
- Hypertensive disorders
- Maternal infections
- Postpartum hemorrhage
- Preeclampsia risk factors
- Preterm birth risk

## 🛠️ Tech Stack

- **LangChain** (v1.0.5) - RAG orchestration
- **FAISS** (v1.12.0) - Vector similarity search
- **HuggingFace Transformers** (v4.57.1) - Embeddings & LLMs
- **Streamlit** (v1.50.0) - Web interface
- **FLAN-T5-base** - Text generation (250MB model)
- **Sentence Transformers** (v5.1.2) - all-MiniLM-L6-v2 embeddings

## 🎨 Customization

### Add More Documents
1. Drop `.txt` files into `demo/corpus/`
2. Run `python demo/ingest.py` to rebuild the index

### Use a Different LLM
Edit `demo/app.py` and change the `LLM_MODEL` variable:
```python
LLM_MODEL = "google/flan-t5-large"  # Bigger model, better quality
```

### Adjust Retrieval Settings
In `app.py` or `app_fast.py`, modify the retriever parameters:
```python
return vs.as_retriever(search_kwargs={"k": 5})  # Retrieve top-5 instead of top-3
```

## � Deploy to Streamlit Cloud

Deploy your MediAssist-RAG app to the cloud for free:

### Prerequisites
1. Push your code to a GitHub repository
2. Sign up at [share.streamlit.io](https://share.streamlit.io)

### Deployment Steps

1. **Prepare Your Repository**
   ```bash
   git add .
   git commit -m "Add MediAssist-RAG Streamlit demo"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Set main file path: `demo/streamlit_app.py`
   - Click "Deploy"

3. **Configuration**
   - Streamlit Cloud will automatically install dependencies from `demo/requirements.txt`
   - The FAISS index will be loaded from the committed `demo/faiss_index/` directory
   - First deployment may take 5-10 minutes

### Deployment Tips

- **Recommended Mode**: Use "Fast Retrieval" mode for public demos (better performance on free tier)
- **Model Loading**: First visitor will trigger model downloads (~340MB), subsequent visits will be faster
- **Resource Limits**: Streamlit Cloud free tier has memory limits - Full RAG mode may be slower
- **Custom Domain**: Available on paid plans

### Example Deployment

**✅ This project is deployed!** Check out the live demo:

**[https://mediassist-rag-9mblcgtthnnenruigzvydn.streamlit.app/](https://mediassist-rag-9mblcgtthnnenruigzvydn.streamlit.app/)**

## 📊 Performance

| Mode | Response Time | Model Size | Quality |
|------|--------------|------------|---------|
| Enhanced Demo (Fast) | < 1s | 90MB | Shows raw context with modern UI |
| Enhanced Demo (Full RAG) | 5-10s | 250MB | Generated answers with citations + UI |
| Fast (retrieval-only) | < 1s | 90MB | Shows raw context |
| Full RAG (FLAN-T5) | 5-10s | 250MB | Generated answers with citations |

## 🐛 Troubleshooting

### Error: "FAISS index not found"
**Solution**: Run `python demo/ingest.py` to build the index first.

### Error: "ModuleNotFoundError: No module named 'langchain_community'"
**Solution**: Install dependencies with `pip install -r demo/requirements.txt`

### Error: Model download is too slow
**Solution**: 
- First run will download ~340MB of models (embeddings + LLM)
- Use `app_fast.py` to avoid downloading the LLM (only needs 90MB embeddings)
- Set `HF_HOME` environment variable to use a different cache location

### Streamlit shows "Connection error"
**Solution**: Make sure you're running the command from the project root, not inside the `demo/` folder.

### Answers are not relevant
**Solution**: 
- Check if your question is related to the 10 maternal health topics
- Try rephrasing your question
- Add more documents to `demo/corpus/` and rebuild the index

### App runs out of memory
**Solution**:
- Use `app_fast.py` instead of `app.py` (no LLM)
- Close other applications
- Switch to a smaller embedding model in `ingest.py`

## ⚠️ Limitations

- Answers are based ONLY on the 10 documents in `demo/corpus/`
- Not a substitute for professional medical advice
- Runs on CPU (no GPU acceleration)
- FLAN-T5 has limited context window (~1000 tokens)

## 📝 Example Queries

See [EXAMPLES.md](EXAMPLES.md) for 15 sample questions, including:
- "What are complications of gestational diabetes?"
- "Risk factors for preeclampsia?"
- "Management of postpartum hemorrhage?"
- "Signs of preterm birth?"

## 🤝 Contributing

Feel free to:
- Add more medical documents
- Improve the prompts
- Enhance the UI
- Add new features (e.g., PDF support, multi-language)
- Report bugs or suggest improvements

## 📄 License

MIT License - feel free to use for your projects!

## 👤 Author

**Arvinth Cinmayan G.K**
- GitHub: [@arvinth777](https://github.com/arvinth777)

---

Built with ❤️ for maternal healthcare education
