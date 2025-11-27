"""
Upstash Vector database operations for semantic search.
"""

import hashlib
from typing import List, Dict
from openai import OpenAI
from upstash_vector import Index

from db import add_chunk

def get_embedding(text: str, openai_key: str) -> List[float]:
    """Get embedding for text using OpenAI."""
    client = OpenAI(api_key=openai_key)
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def get_upstash_index(upstash_url: str, upstash_token: str) -> Index:
    """Get Upstash Vector index."""
    return Index(url=upstash_url, token=upstash_token)

def upsert_chunks(
    chunks: List[str],
    doc_id: int,
    doc_title: str,
    openai_key: str,
    upstash_url: str,
    upstash_token: str
):
    """Upsert chunks to Upstash Vector and SQLite."""
    index = get_upstash_index(upstash_url, upstash_token)
    
    vectors_to_upsert = []
    
    for i, chunk_text in enumerate(chunks):
        # Generate unique chunk ID
        chunk_id = hashlib.md5(f"{doc_id}_{i}_{chunk_text[:50]}".encode()).hexdigest()
        
        # Get embedding
        embedding = get_embedding(chunk_text, openai_key)
        
        # Store in SQLite
        add_chunk(chunk_id, doc_id, chunk_text, i)
        
        # Prepare for Upstash
        vectors_to_upsert.append({
            "id": chunk_id,
            "vector": embedding,
            "metadata": {
                "document_id": doc_id,
                "document_title": doc_title,
                "chunk_index": i,
                "text_preview": chunk_text[:200]
            }
        })
    
    # Batch upsert to Upstash
    if vectors_to_upsert:
        index.upsert(vectors=vectors_to_upsert)

def query_similar(
    query: str,
    top_k: int,
    openai_key: str,
    upstash_url: str,
    upstash_token: str
) -> List[Dict]:
    """Query similar chunks from Upstash Vector."""
    index = get_upstash_index(upstash_url, upstash_token)
    
    # Get query embedding
    query_embedding = get_embedding(query, openai_key)
    
    # Query Upstash
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    
    return [
        {
            "id": r.id,
            "score": r.score,
            "metadata": r.metadata
        }
        for r in results
    ]
