import glob, os
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

CORPUS_DIR = os.path.join(os.path.dirname(__file__), "corpus")
INDEX_PATH = os.path.join(os.path.dirname(__file__), "faiss_index")

def load_docs():
    docs = []
    for p in sorted(glob.glob(os.path.join(CORPUS_DIR, "*.txt"))):
        with open(p, "r", encoding="utf-8") as f:
            text = f.read().strip()
        docs.append(Document(page_content=text, metadata={"source": os.path.basename(p)}))
    return docs

def main():
    os.makedirs(CORPUS_DIR, exist_ok=True)
    docs = load_docs()
    if not docs:
        raise SystemExit("No .txt files found in demo/corpus")
    embed = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vs = FAISS.from_documents(docs, embed)
    vs.save_local(INDEX_PATH)
    print(f"✅ Saved FAISS index to {INDEX_PATH} with {len(docs)} docs")

if __name__ == "__main__":
    main()
