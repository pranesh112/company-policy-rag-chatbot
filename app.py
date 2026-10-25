import streamlit as st
import os
from openai import OpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

st.set_page_config(page_title="RAG Chatbot", page_icon="💬")
st.title("💬 Company query and knowledge Chatbot")

# Securely input API Keys
groq_key = st.sidebar.text_input("Groq API Key", type="password")
pinecone_key = st.sidebar.text_input("Pinecone API Key", value=os.environ.get("PINECONE_API_KEY", ""), type="password")

if groq_key and pinecone_key:

    # Initialize Embeddings and Vector Store
    @st.cache_resource
    def load_embeddings():
        embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        return embedding_model

    # Credentials belong to this session, not a globally cached vector store.
    database = PineconeVectorStore(
        index_name=os.environ.get("PINECONE_INDEX_NAME", "rag-deployment"),
        embedding=load_embeddings(),
        pinecone_api_key=pinecone_key,
        namespace=os.environ.get("PINECONE_NAMESPACE", ""),
        text_key="text",
    )

    # Initialize OpenAI client with Groq base URL
    client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=groq_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if question := st.chat_input("Ask me anything about company policy:"):
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        # 1. Retrieve the most relevant context from Pinecone
        results = database.similarity_search(question, k=1)
        if not results:
            st.warning("No policy text was returned. Check the index and namespace.")
            st.stop()
        context = results[0].page_content

        # 2. Query the model hosted on Groq
        completion = client.chat.completions.create(
            model=os.environ.get("GROQ_MODEL", "openai/gpt-oss-20b"),
            messages=[
                {
                    "role": "system",
                    "content": "Answer using only the provided context. If the answer is missing, say I don't know."
                },
                {
                    "role": "user",
                    "content": f"Context: {context}\nQuestion: {question}"
                }
            ],
        )

        answer = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)
else:
    st.warning("Please enter your API keys in the sidebar to begin.")
