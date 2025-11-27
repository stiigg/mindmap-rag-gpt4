"""
Mind Map RAG Application
Beyond RAG: GPT-4 and Vector Databases for Mind Map Creation
"""

import streamlit as st
from dotenv import load_dotenv
import os

from db import init_db, add_document, get_all_documents, get_chunks_by_ids
from vector_store import upsert_chunks, query_similar
from llm import chunk_text, extract_graph_with_gpt
from graph_viz import build_plotly_figure

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Mind Map RAG",
    page_icon="🧠",
    layout="wide"
)

# Initialize database
init_db()

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    openai_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    upstash_url = st.text_input("Upstash Vector URL", value=os.getenv("UPSTASH_VECTOR_URL", ""))
    upstash_token = st.text_input("Upstash Vector Token", type="password", value=os.getenv("UPSTASH_VECTOR_TOKEN", ""))
    
    st.divider()
    
    top_k = st.slider("Number of chunks to retrieve", 5, 20, 10)
    max_nodes = st.slider("Max nodes in mind map", 10, 30, 15)

# Main tabs
tab1, tab2, tab3 = st.tabs(["📄 Ingest Documents", "🔍 Query & Mind Map", "📚 Browse Data"])

# Tab 1: Document Ingestion
with tab1:
    st.header("📄 Ingest Documents")
    
    doc_title = st.text_input("Document Title")
    doc_content = st.text_area("Document Content", height=300)
    
    if st.button("Ingest Document", type="primary"):
        if doc_title and doc_content and openai_key and upstash_url and upstash_token:
            with st.spinner("Processing document..."):
                # Add to SQLite
                doc_id = add_document(doc_title, doc_content)
                
                # Chunk the text
                chunks = chunk_text(doc_content)
                
                # Upsert to Upstash Vector
                upsert_chunks(
                    chunks=chunks,
                    doc_id=doc_id,
                    doc_title=doc_title,
                    openai_key=openai_key,
                    upstash_url=upstash_url,
                    upstash_token=upstash_token
                )
                
            st.success(f"✅ Document '{doc_title}' ingested with {len(chunks)} chunks!")
        else:
            st.error("Please fill in all fields and API keys")

# Tab 2: Query and Mind Map
with tab2:
    st.header("🔍 Query & Generate Mind Map")
    
    query = st.text_input("Enter your question")
    
    if st.button("Generate Mind Map", type="primary"):
        if query and openai_key and upstash_url and upstash_token:
            with st.spinner("Searching and building mind map..."):
                # Query similar chunks
                results = query_similar(
                    query=query,
                    top_k=top_k,
                    openai_key=openai_key,
                    upstash_url=upstash_url,
                    upstash_token=upstash_token
                )
                
                if results:
                    # Get chunk texts
                    chunk_ids = [r["id"] for r in results]
                    chunks_data = get_chunks_by_ids(chunk_ids)
                    context = "\n\n".join([c["text"] for c in chunks_data])
                    
                    # Extract graph with GPT-4
                    graph_data = extract_graph_with_gpt(
                        question=query,
                        context=context,
                        max_nodes=max_nodes,
                        openai_key=openai_key
                    )
                    
                    if graph_data:
                        # Build and display the mind map
                        fig = build_plotly_figure(graph_data)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Show raw JSON in expander
                        with st.expander("View Graph JSON"):
                            st.json(graph_data)
                    else:
                        st.warning("Could not extract graph from context")
                else:
                    st.warning("No relevant chunks found")
        else:
            st.error("Please enter a query and configure API keys")

# Tab 3: Browse Data
with tab3:
    st.header("📚 Browse Documents")
    
    docs = get_all_documents()
    if docs:
        for doc in docs:
            with st.expander(f"📄 {doc['title']} (ID: {doc['id']})"):
                st.write(f"**Created:** {doc['created_at']}")
                st.write(doc['content'][:500] + "..." if len(doc['content']) > 500 else doc['content'])
    else:
        st.info("No documents ingested yet")

# Footer
st.divider()
st.caption("Mind Map RAG - Beyond RAG with GPT-4 and Upstash Vector")
