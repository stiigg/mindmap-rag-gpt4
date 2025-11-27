"""
LLM operations: text chunking and GPT-4 graph extraction.
"""

import json
from typing import List, Dict, Optional
from openai import OpenAI

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = start + chunk_size
        chunk = text[start:end]
        
        # Try to break at sentence boundary
        if end < text_len:
            last_period = chunk.rfind('.')
            last_newline = chunk.rfind('\n')
            break_point = max(last_period, last_newline)
            if break_point > chunk_size // 2:
                chunk = chunk[:break_point + 1]
                end = start + break_point + 1
        
        chunks.append(chunk.strip())
        start = end - overlap
    
    return [c for c in chunks if c]

def extract_graph_with_gpt(
    question: str,
    context: str,
    max_nodes: int,
    openai_key: str
) -> Optional[Dict]:
    """Extract knowledge graph from context using GPT-4."""
    
    client = OpenAI(api_key=openai_key)
    
    system_prompt = """You are a knowledge graph extraction assistant. 
Given a question and context, extract key concepts (nodes) and relationships (edges).

Output ONLY valid JSON with this structure:
{
    "nodes": [
        {"id": "n1", "label": "Concept Name", "type": "Concept|Person|Organization|Tool|Method|Dataset"}
    ],
    "edges": [
        {"source": "n1", "target": "n2", "label": "relationship_type"}
    ]
}

Rules:
- Extract 10-20 most relevant nodes
- Use short, clear labels
- Include diverse relationship types (uses, contains, relates_to, part_of, etc.)
- Ensure all edge source/target IDs exist in nodes
- Output ONLY the JSON, no explanations"""

    user_prompt = f"""Question: {question}

Context:
{context[:8000]}

Extract a knowledge graph with up to {max_nodes} nodes that answers the question."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        
        content = response.choices[0].message.content.strip()
        
        # Try to parse JSON
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        
        graph_data = json.loads(content)
        
        # Validate structure
        if "nodes" in graph_data and "edges" in graph_data:
            return graph_data
        
        return None
        
    except Exception as e:
        print(f"Error extracting graph: {e}")
        return None
