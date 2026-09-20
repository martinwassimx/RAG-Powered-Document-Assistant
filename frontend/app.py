import os
from pathlib import Path
import streamlit as st
from api_client import APIClient

# Configure page metadata and layout
st.set_page_config(
    page_title="RAG Document Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for rich aesthetics, clean card layouts, and badges
st.markdown("""
<style>
    /* Global styling */
    .main {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Title banner */
    .header-container {
        padding: 1.5rem 0rem 1rem 0rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 1.5rem;
    }
    
    .header-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .header-subtitle {
        color: #94a3b8;
        font-size: 1rem;
        margin-top: 0.3rem;
    }

    /* Citation badge */
    .citation-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.3);
        color: #38bdf8;
        border-radius: 6px;
        padding: 0.25rem 0.6rem;
        font-size: 0.85rem;
        font-weight: 500;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }

    /* Citation card */
    .citation-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 8px;
        padding: 0.8rem;
        margin-top: 0.6rem;
    }

    /* Status indicator */
    .status-pill {
        display: inline-block;
        padding: 0.2rem 0.7rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-healthy {
        background-color: rgba(34, 197, 94, 0.2);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.4);
    }
    .status-degraded {
        background-color: rgba(234, 179, 8, 0.2);
        color: #fde047;
        border: 1px solid rgba(234, 179, 8, 0.4);
    }
    .status-offline {
        background-color: rgba(239, 68, 68, 0.2);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize API Client
client = APIClient()

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar: System Diagnostics & Settings
with st.sidebar:
    logo_path = Path(__file__).parent / "assets" / "logo.jpg"
    if logo_path.exists():
        st.image(str(logo_path), width=85)
    else:
        st.markdown("# 📚")
    st.title("System Status")
    
    # Check backend health
    health_info = client.get_health()
    status = health_info.get("status", "offline")
    
    if status == "healthy":
        st.markdown('<span class="status-pill status-healthy">● Backend Online</span>', unsafe_allow_html=True)
    elif status == "degraded":
        st.markdown('<span class="status-pill status-degraded">▲ Degraded Service</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-pill status-offline">✖ Backend Disconnected</span>', unsafe_allow_html=True)
        st.caption(f"Target: `{client.base_url}`")
        st.warning("Make sure the FastAPI backend is running via `uvicorn app.main:app`.")

    st.divider()
    
    st.subheader("Configuration")
    top_k = st.slider("Top Chunks (k)", min_value=1, max_value=8, value=4, help="Number of retrieved chunks used for context grounding.")
    
    if status in ("healthy", "degraded"):
        vector_stats = health_info.get("vector_store", {})
        llm_stats = health_info.get("llm", {})
        
        with st.expander("Diagnostic Metadata", expanded=False):
            st.write("**ChromaDB Collection:**", vector_stats.get("collection", "N/A"))
            st.write("**Indexed Chunks:**", vector_stats.get("total_chunks", "N/A"))
            st.write("**Ollama Model:**", llm_stats.get("model", "N/A"))
            st.write("**Ollama Status:**", "Reachable" if llm_stats.get("reachable") else "Offline")
            st.write("**Embedding Model:**", health_info.get("embedding_model", "N/A"))

    st.divider()
    
    st.subheader("Sample Questions")
    sample_queries = [
        "What are the four Coffman conditions for a deadlock?",
        "Explain the TCP 3-way handshake process.",
        "What is the difference between B-Tree and B+ Tree indexing?",
        "Why does Python have a Global Interpreter Lock (GIL)?",
        "What is the difference between Greedy algorithms and Dynamic Programming?"
    ]
    
    for sq in sample_queries:
        if st.button(sq, key=f"sq_{hash(sq)}", use_container_width=True):
            st.session_state.pending_query = sq

    st.divider()
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Header
st.markdown("""
<div class="header-container">
    <h1 class="header-title">📚 RAG-Powered Document Assistant</h1>
    <p class="header-subtitle">
        Document-grounded question answering powered by Sentence Transformers, ChromaDB, and Ollama.
    </p>
</div>
""", unsafe_allow_html=True)

# Render Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Display citations if available
        sources = message.get("sources", [])
        if sources:
            with st.expander(f"📖 Sources & Citations ({len(sources)} retrieved chunks)", expanded=False):
                for idx, src in enumerate(sources, start=1):
                    doc_name = src.get("document", "Unknown Document")
                    page_num = src.get("page", 1)
                    score = src.get("relevance_score")
                    snippet = src.get("snippet", "")
                    
                    score_text = f" • Distance: {score:.4f}" if score is not None else ""
                    st.markdown(f"**[{idx}] {doc_name} — Page {page_num}**{score_text}")
                    if snippet:
                        st.caption(f'"{snippet}"')

# Handle query submission
user_query = st.chat_input("Ask a question about the course documents...")

# Check if a sample query was clicked
if "pending_query" in st.session_state and st.session_state.pending_query:
    user_query = st.session_state.pending_query
    st.session_state.pending_query = None

if user_query:
    # Append user question to history
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Assistant response with spinner
    with st.chat_message("assistant"):
        with st.spinner("Searching document store and synthesizing answer..."):
            result = client.query_document_assistant(question=user_query, top_k=top_k)

        if result.get("success"):
            data = result["data"]
            answer = data.get("answer", "No answer was returned.")
            sources = data.get("sources", [])
            
            st.markdown(answer)
            
            if sources:
                with st.expander(f"📖 Sources & Citations ({len(sources)} retrieved chunks)", expanded=True):
                    for idx, src in enumerate(sources, start=1):
                        doc_name = src.get("document", "Unknown Document")
                        page_num = src.get("page", 1)
                        score = src.get("relevance_score")
                        snippet = src.get("snippet", "")
                        
                        score_text = f" • Distance: {score:.4f}" if score is not None else ""
                        st.markdown(f"**[{idx}] {doc_name} — Page {page_num}**{score_text}")
                        if snippet:
                            st.caption(f'"{snippet}"')
            
            # Save to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })
        else:
            error_type = result.get("error_type", "error")
            detail = result.get("detail", "An unknown error occurred.")
            
            error_msg = f"⚠️ **Error ({error_type})**: {detail}"
            st.error(error_msg)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg,
                "sources": []
            })
