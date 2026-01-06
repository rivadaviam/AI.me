"""Pydantic models for API requests and responses."""

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime


class Document(BaseModel):
    """Document model for graph building."""

    id: str
    title: str
    content: str
    created_at: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class Node(BaseModel):
    """Graph node model."""

    id: str
    type: str
    properties: Dict[str, Any]


class Edge(BaseModel):
    """Graph edge model."""

    source: str
    target: str
    type: str
    properties: Optional[Dict[str, Any]] = None


class Subgraph(BaseModel):
    """Subgraph model."""

    nodes: List[Node]
    edges: List[Edge]


class BuildGraphRequest(BaseModel):
    """Request to build a graph from documents."""

    documents: List[Document]
    metadata: Optional[Dict[str, Any]] = None
    version: Optional[str] = None


class BuildGraphResponse(BaseModel):
    """Response from graph building."""

    graph_id: str
    status: str
    node_count: Optional[int] = None
    edge_count: Optional[int] = None


class QueryRequest(BaseModel):
    """Request to query the graph."""

    query: str = Field(..., description="User query or question")
    graph_id: str = Field(..., description="ID of the graph to query")
    context: Optional[Dict[str, Any]] = None
    filters: Optional[Dict[str, Any]] = None


class QueryResponse(BaseModel):
    """Response from a query."""

    response: str
    subgraph: Subgraph
    metadata: Dict[str, Any]
    audit_id: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class UpdateGraphRequest(BaseModel):
    """Request to update a graph."""

    updates: Dict[str, Any]
    new_version: Optional[str] = None


class VersionInfo(BaseModel):
    """Version information model."""

    version_id: str
    graph_id: str
    created_at: str
    metadata: Dict[str, Any]

