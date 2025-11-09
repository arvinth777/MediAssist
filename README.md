# MediAssist RAG - Maternal Health QA System

A Retrieval-Augmented Generation (RAG) system for maternal health question answering, built with FAISS vector search and local language models.

## 🎯 Features

- **Fast semantic search** using FAISS vector database
- **Two modes**: Full LLM generation or instant retrieval-only
- **Local deployment** - runs entirely on your machine
- **10 curated documents** on maternal health topics (pregnancy, complications, risk factors)
- **Citation support** - answers reference source documents

## 📁 Project Structure

```
demo/
├── data/               # 10 maternal health text files
├── app.py             # Full RAG app with FLAN-T5
├── app_fast.py        # Fast retrieval-only version
├── ingest.py          # Script to build FAISS index
└── requirements.txt   # Python dependencies
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r demo/requirements.txt
```

### 2. Build the Vector Index

```bash
python demo/ingest.py
```

This will:
- Load all `.txt` files from `demo/data/`
- Create embeddings using `sentence-transformers/all-MiniLM-L6-v2`
- Save FAISS index to `demo/faiss_index/`

### 3. Run the App

**Option A: Fast retrieval-only (< 1 second response)**
```bash
streamlit run demo/app_fast.py
```

**Option B: Full RAG with LLM (5-10 seconds response)**
```bash
streamlit run demo/app.py
```

## 🔍 How It Works

1. **Ingestion**: Medical documents are chunked and embedded into a FAISS vector store
2. **Retrieval**: User questions are matched against the vector store to find top-3 relevant passages
3. **Generation** (optional): A local LLM (FLAN-T5) generates answers using only the retrieved context
4. **Citation**: Answers reference source documents [1], [2], [3]

## 📚 Data Sources

The `demo/data/` folder contains 10 text files on maternal health:
- Anemia in pregnancy
- Antenatal care basics
- Fetal growth restriction
- Gestational diabetes complications
- Hypertensive disorders
- Maternal infections
- Postpartum hemorrhage
- Preeclampsia risk factors
- Preterm birth risk
- Fetal ultrasound markers

## 🛠️ Tech Stack

- **LangChain** - RAG orchestration
- **FAISS** - Vector similarity search
- **HuggingFace Transformers** - Embeddings & LLMs
- **Streamlit** - Web interface
- **FLAN-T5** - Text generation (250MB model)

## 🎨 Customization

### Add More Documents
1. Drop `.txt` files into `demo/data/`
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

## 📊 Performance

| Mode | Response Time | Model Size | Quality |
|------|--------------|------------|---------|
| Fast (retrieval-only) | < 1s | 90MB | Shows raw context |
| Full RAG (FLAN-T5) | 5-10s | 250MB | Generated answers with citations |

## ⚠️ Limitations

- Answers are based ONLY on the 10 documents in `demo/data/`
- Not a substitute for professional medical advice
- Runs on CPU (no GPU acceleration)
- FLAN-T5 has limited context window (~1000 tokens)

## 📝 Example Queries

- "What are complications of gestational diabetes?"
- "Risk factors for preeclampsia?"
- "Management of postpartum hemorrhage?"
- "Signs of preterm birth?"

## 🤝 Contributing

Feel free to add more medical documents, improve the prompts, or enhance the UI!

## 📄 License

MIT License - feel free to use for your projects!

## 👤 Author

**Arvinth Cinmayan G.K**
- GitHub: [@arvinth777](https://github.com/arvinth777)

---

Built with ❤️ for maternal healthcare education
