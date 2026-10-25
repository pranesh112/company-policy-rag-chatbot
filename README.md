# Company Policy RAG Chatbot

A learning project by Pranesh Mohan that answers questions using sample company-policy text. I built this to understand how retrieval-augmented generation (RAG) combines document search with a language model.

## What it does

The app embeds a question, searches a Pinecone index for one relevant text chunk, and sends that chunk and the question to a model hosted on Groq. Streamlit displays the conversation. The model is instructed to use only the supplied context and acknowledge missing information.

## Project status

- The notebook retrieved policy text and generated the answer “24 days per year” to a paid-leave question.
- The Streamlit interface loaded through a temporary Cloudflare tunnel.
- The original web app failed because `llama3-8b-8192` had been retired.
- This packaged version changes the default to `openai/gpt-oss-20b`, removes the shared credential-dependent vector-store cache, passes Pinecone credentials explicitly, and handles empty retrieval results.
- This revision has passed a Python syntax check. It has **not** been tested end to end with live credentials. A successful notebook demonstration is not proof that every web-app path works.

## Technology

Python, Streamlit, LangChain, Pinecone, Hugging Face sentence-transformer embeddings, and Groq's OpenAI-compatible API. The `openai` Python package is used as the client; generation requests go to Groq.

## Before running

You need a Groq API key and a Pinecone API key for a project with an existing populated index. The app does not create an index or upload documents.

Default index configuration:

- Index name: `rag-deployment`
- Dense vector dimension: 384
- Metric used in the demonstration: cosine
- Namespace: empty/default (`""`)
- Text metadata field: `text`
- Embedding model: `all-MiniLM-L6-v2`

Documents must already have been embedded using the same model and stored with their text in the `text` metadata field. A 384-dimensional index alone does not guarantee compatible embeddings. The original ingestion notebook is not included in this package.

The demonstration used sample policy text describing 24 paid-leave days per year, two work-from-home days per week, office hours of 9 AM–6 PM, insurance for an employee and two dependents, and laptop replacement every three years. These are demonstration facts, not employment advice.

## Run on Windows in PowerShell

Open this project folder in VS Code, then run:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the local URL printed in the terminal. Enter your own Groq and Pinecone keys in the sidebar. This method does not require activating the virtual environment or changing PowerShell execution policy.

## Run on macOS or Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

The first embedding-model download requires internet access. Both external APIs also require network access and may have quotas or charges. Dependencies are intentionally unpinned because the original environment's exact versions were not provided; this is not a reproducible lockfile.

## Optional configuration

Set these environment variables before starting Streamlit if your setup differs:

| Variable | Default |
| --- | --- |
| `GROQ_MODEL` | `openai/gpt-oss-20b` |
| `PINECONE_INDEX_NAME` | `rag-deployment` |
| `PINECONE_NAMESPACE` | empty/default |

Model availability can change. Check the Groq model documentation if a model request fails.

## Try it

1. Ask: “How many days of paid leave do employees receive?” Expected from the sample data: 24 days per year.
2. Ask: “How often can employees work from home?” Expected: twice a week.
3. Ask a question absent from the policy, such as “What is the annual bonus?” Check that the answer acknowledges missing information.

These are manual test cases, not claims that all tests have passed. Retrieval returns the nearest chunk, which may not contain the answer. The prompt does not guarantee factual correctness.

## Limitations and next steps

This is an educational prototype. It retrieves one chunk and displays chat history, but it does not send earlier conversation turns to the model. It has no document uploader, citations UI, authentication, rate limiting, or production monitoring. API and network failures may still display errors. Add a reproducible ingestion script, dependency lockfile, more retrieval tests, source citations, and friendly error handling before a broader release.

## Sharing safely

Never commit API keys, `.env` files, virtual environments, or screenshots with visible credentials. Revoke keys previously exposed in screenshots or notebook cells. Clear sensitive notebook outputs before uploading a notebook. `.gitignore` does not remove secrets already committed. A temporary tunnel URL is only a development preview, not permanent hosting.

## What I learned

I practised connecting embeddings, vector search and generation; debugging missing dependencies and empty search results; separating notebook code from an application file; and troubleshooting browser assets, tunnels and retired models. This repository documents a guided learning project, including its remaining limitations.

## References

- Streamlit: https://docs.streamlit.io/
- PineconeVectorStore: https://reference.langchain.com/python/langchain-pinecone/vectorstores/PineconeVectorStore
- Groq models: https://console.groq.com/docs/models

## Credits

Developed as a guided learning project with AI-assisted debugging and documentation. Add the specific workshop or tutorial credit if applicable before publishing.
