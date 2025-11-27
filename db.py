"""
SQLite database helpers for document and chunk storage.
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

DB_PATH = "mindmap_rag.db"

def get_connection():
    """Get SQLite connection."""
    return sqlite3.connect(DB_PATH)

def init_db():
    """Initialize the database with required tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Documents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Chunks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id TEXT PRIMARY KEY,
            document_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            chunk_index INTEGER NOT NULL,
            FOREIGN KEY (document_id) REFERENCES documents(id)
        )
    """)
    
    conn.commit()
    conn.close()

def add_document(title: str, content: str) -> int:
    """Add a document and return its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO documents (title, content) VALUES (?, ?)",
        (title, content)
    )
    
    doc_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return doc_id

def add_chunk(chunk_id: str, document_id: int, text: str, chunk_index: int):
    """Add a chunk to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT OR REPLACE INTO chunks (id, document_id, text, chunk_index) VALUES (?, ?, ?, ?)",
        (chunk_id, document_id, text, chunk_index)
    )
    
    conn.commit()
    conn.close()

def get_all_documents() -> List[Dict]:
    """Get all documents."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, title, content, created_at FROM documents ORDER BY created_at DESC")
    rows = cursor.fetchall()
    
    conn.close()
    
    return [
        {"id": r[0], "title": r[1], "content": r[2], "created_at": r[3]}
        for r in rows
    ]

def get_chunks_by_ids(chunk_ids: List[str]) -> List[Dict]:
    """Get chunks by their IDs."""
    if not chunk_ids:
        return []
    
    conn = get_connection()
    cursor = conn.cursor()
    
    placeholders = ",".join(["?" for _ in chunk_ids])
    cursor.execute(f"SELECT id, document_id, text, chunk_index FROM chunks WHERE id IN ({placeholders})", chunk_ids)
    rows = cursor.fetchall()
    
    conn.close()
    
    return [
        {"id": r[0], "document_id": r[1], "text": r[2], "chunk_index": r[3]}
        for r in rows
    ]
