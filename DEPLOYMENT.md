# MediAssist-RAG Streamlit Cloud Deployment Guide

## Quick Deployment Steps

### 1. Commit FAISS Index to Git

The FAISS index needs to be committed to your repository:

```bash
cd /Users/arvinthcinmayankirupakaran/Desktop/medassistdemo/MediAssist
git add demo/faiss_index/
git add demo/streamlit_app.py
git add README.md
git commit -m "Add enhanced Streamlit demo with FAISS index"
git push origin main
```

### 2. Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Fill in:
   - **Repository:** arvinth777/MediAssist
   - **Branch:** main
   - **Main file path:** demo/streamlit_app.py
5. Click "Deploy"

### 3. Wait for Deployment

- Initial deployment: 5-10 minutes
- Streamlit will install all dependencies from `demo/requirements.txt`
- Models will be downloaded on first visitor (~340MB)

### 4. Get Your Public URL

Your app will be available at:
```
https://[your-username]-mediassist-[random-id].streamlit.app
```

## Performance Tips

- **Fast Retrieval Mode** is recommended for public demos (better performance)
- **Full RAG Mode** works but may be slower on free tier
- First visitor will experience longer load time (model downloads)
- Subsequent visitors will have faster experience (cached models)

## Troubleshooting

### Memory Errors
- Use Fast Retrieval mode instead of Full RAG
- Streamlit Cloud free tier has 1GB memory limit

### Slow Performance
- Expected on first load (model downloads)
- Recommend Fast Retrieval mode for demos
- Consider upgrading to paid tier for better performance

### FAISS Index Not Found
- Ensure `demo/faiss_index/` is committed to git
- Check file paths in deployment logs

## Local Testing

Before deploying, test locally:

```bash
streamlit run demo/streamlit_app.py
```

Access at: http://localhost:8501

## Resources

- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
- [Resource Limits](https://docs.streamlit.io/streamlit-community-cloud/manage-your-app/resource-limits)
