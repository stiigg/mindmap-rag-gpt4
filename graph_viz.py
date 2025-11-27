"""
Graph visualization using NetworkX and Plotly.
"""

from typing import Dict
import networkx as nx
import plotly.graph_objects as go

# Color mapping for node types
NODE_COLORS = {
    "Concept": "#4ECDC4",
    "Person": "#FF6B6B",
    "Organization": "#45B7D1",
    "Tool": "#96CEB4",
    "Method": "#FFEAA7",
    "Dataset": "#DDA0DD",
    "default": "#95A5A6"
}

def build_plotly_figure(graph_data: Dict) -> go.Figure:
    """Build an interactive Plotly figure from graph data."""
    
    nodes = graph_data.get("nodes", [])
    edges = graph_data.get("edges", [])
    
    if not nodes:
        return go.Figure()
    
    # Build NetworkX graph
    G = nx.DiGraph()
    
    for node in nodes:
        G.add_node(
            node["id"],
            label=node.get("label", node["id"]),
            type=node.get("type", "Concept")
        )
    
    for edge in edges:
        if edge["source"] in G.nodes and edge["target"] in G.nodes:
            G.add_edge(
                edge["source"],
                edge["target"],
                label=edge.get("label", "")
            )
    
    # Compute layout
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # Create edge traces
    edge_x = []
    edge_y = []
    edge_labels = []
    
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        
        # Edge label position (midpoint)
        mid_x = (x0 + x1) / 2
        mid_y = (y0 + y1) / 2
        edge_labels.append({
            "x": mid_x,
            "y": mid_y,
            "label": edge[2].get("label", "")
        })
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1.5, color="#888"),
        hoverinfo="none",
        mode="lines"
    )
    
    # Create node traces
    node_x = []
    node_y = []
    node_text = []
    node_colors = []
    
    for node_id in G.nodes():
        x, y = pos[node_id]
        node_x.append(x)
        node_y.append(y)
        
        node_data = G.nodes[node_id]
        label = node_data.get("label", node_id)
        node_type = node_data.get("type", "Concept")
        
        node_text.append(f"{label}<br>Type: {node_type}")
        node_colors.append(NODE_COLORS.get(node_type, NODE_COLORS["default"]))
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode="markers+text",
        hoverinfo="text",
        text=[G.nodes[n].get("label", n) for n in G.nodes()],
        textposition="top center",
        textfont=dict(size=10, color="white"),
        hovertext=node_text,
        marker=dict(
            size=25,
            color=node_colors,
            line=dict(width=2, color="white")
        )
    )
    
    # Create figure
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="Knowledge Mind Map",
            titlefont=dict(size=16, color="white"),
            showlegend=False,
            hovermode="closest",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor="#1a1a2e",
            paper_bgcolor="#1a1a2e",
            margin=dict(b=20, l=5, r=5, t=40)
        )
    )
    
    # Add edge labels as annotations
    for el in edge_labels:
        if el["label"]:
            fig.add_annotation(
                x=el["x"], y=el["y"],
                text=el["label"],
                showarrow=False,
                font=dict(size=8, color="#aaa"),
                bgcolor="rgba(0,0,0,0.5)"
            )
    
    return fig
