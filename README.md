# 🧠 mindmap-rag-gpt4

Beyond RAG: GPT-4 and Vector Databases (Upstash) for Mind Map Creation with Streamlit, NetworkX, and Plotly

## Overview

This project transforms traditional RAG (Retrieval-Augmented Generation) into an interactive mind map visualization. Instead of returning plain text answers, it extracts knowledge graphs from retrieved documents and displays them as interactive node-edge diagrams.

## Features

- **Document Ingestion**: Upload text documents, chunk them, and store embeddings in Upstash Vector
- **Semantic Search**: Query your documents using natural language
- **Knowledge Graph Extraction**: GPT-4 extracts entities and relationships from retrieved context
- **Interactive Mind Maps**: Visualize knowledge as an interactive graph using NetworkX and Plotly
- **Dark Theme UI**: Clean Streamlit interface with a modern dark visualization style

## Architecture

```
User Query → Embed → Upstash Vector Search → Retrieve Chunks
                                                    ↓
                                            GPT-4 Graph Extraction
                                                    ↓
                                            NetworkX Graph Building
                                                    ↓
                                            Plotly Mind Map Visualization
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/stiigg/mindmap-rag-gpt4.git
cd mindmap-rag-gpt4
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (create `.env` file):
```env
OPENAI_API_KEY=your_openai_api_key
UPSTASH_VECTOR_URL=your_upstash_vector_url
UPSTASH_VECTOR_TOKEN=your_upstash_vector_token
```

4. Run the application:
```bash
streamlit run app.py
```

## Project Structure

```
mindmap-rag-gpt4/
├── app.py              # Main Streamlit application
├── db.py               # SQLite database helpers
├── vector_store.py     # Upstash Vector operations
├── llm.py              # Text chunking and GPT-4 graph extraction
├── graph_viz.py        # NetworkX + Plotly visualization
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Requirements

- Python 3.9+
- OpenAI API key (for embeddings and GPT-4)
- Upstash Vector database (free tier available)

## Usage

1. **Ingest Documents**: Go to the "Ingest Documents" tab, enter a title and paste your document content
2. **Query & Mind Map**: Switch to "Query & Mind Map" tab, ask a question about your documents
3. **Explore**: Interact with the generated mind map - hover over nodes to see details

## Tech Stack

- **Streamlit**: Web UI framework
- **OpenAI**: Embeddings (text-embedding-3-small) and GPT-4o for graph extraction
- **Upstash Vector**: Serverless vector database for semantic search
- **NetworkX**: Graph data structure and layout algorithms
- **Plotly**: Interactive visualization
- **SQLite**: Local document and chunk metadata storage

## License

MIT License

## Acknowledgments

Inspired by the article "Beyond RAG: GPT-4 and Vector Databases for Mind Map Creation" on Medium.
