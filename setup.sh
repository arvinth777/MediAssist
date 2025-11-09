#!/bin/bash
# Setup script for MediAssist RAG

set -e  # Exit on error

echo "🚀 Setting up MediAssist RAG..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

echo "✅ Python 3 found"

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r demo/requirements.txt

# Build FAISS index
echo "🔨 Building FAISS vector index..."
python demo/ingest.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "  1. Fast retrieval-only app:  streamlit run demo/app_fast.py"
echo "  2. Full RAG with LLM:        streamlit run demo/app.py"
echo ""
echo "💡 The fast app responds instantly, the full app takes 5-10 seconds per query."
