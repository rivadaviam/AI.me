# Data Model Specification

## Overview

This document describes the data models, schemas, and structures used throughout the AI.me platform.

## Core Data Models

### Document

Represents a document to be processed into a graph.

```python
{
    "document_id": str,          # Unique identifier (1-255 chars)
    "content": str,              # Document content
    "metadata": {
        "source": str,           # Source identifier
        "author": str,           # Author name
        "topic": str,            # Topic/category
        "created_at": datetime,   # ISO 8601 format
        "expires_at": datetime,  # Optional expiration
        "tags": List[str],       # Tags for categorization
        "language": str          # Language code (ISO 639-1)
    }
}
```

### Graph Node

Represents a node in the semantic graph.

```python
{
    "id": str,                   # Node identifier
    "label": str,                # Node label/type
    "properties": {
        "name": str,             # Node name
        "type": str,             # Entity type
        "source": str,           # Source document
        "timestamp": datetime,   # Creation timestamp
        "verified": bool,        # Verification status
        "metadata": dict         # Additional metadata
    },
    "relationships": List[str]   # Related node IDs
}
```

### Graph Edge

Represents a relationship between nodes.

```python
{
    "id": str,                   # Edge identifier
    "source": str,              # Source node ID
    "target": str,              # Target node ID
    "relationship": str,        # Relationship type
    "properties": {
        "weight": float,        # Relationship strength
        "confidence": float,    # Confidence score
        "timestamp": datetime,  # Creation timestamp
        "metadata": dict        # Additional metadata
    }
}
```

### Graph Version

Represents a versioned snapshot of a graph.

```python
{
    "version_id": str,          # Version identifier
    "graph_id": str,            # Graph identifier
    "version_number": int,      # Sequential version number
    "version_type": str,        # "major", "minor", "patch", "temporal"
    "created_at": datetime,     # Version creation time
    "metadata": {
        "changes": List[str],   # List of changes
        "author": str,          # Version author
        "expires_at": datetime   # Optional expiration
    }
}
```

### Query Request

Request structure for graph queries.

```python
{
    "query": str,                # Query string (1-1000 chars)
    "graph_id": str,            # Optional specific graph
    "filters": {
        "source": str,          # Filter by source
        "valid_until": datetime, # Temporal validity filter
        "min_groundedness": float, # Minimum groundedness (0.0-1.0)
        "node_types": List[str], # Filter by node types
        "date_range": {
            "start": datetime,
            "end": datetime
        }
    }
}
```

### Query Response

Response structure for graph queries.

```python
{
    "answer": str,               # Generated answer
    "model": str,                # LLM model used
    "validation": {
        "is_valid": bool,       # Validation result
        "groundedness_score": float, # 0.0-1.0
        "issues": List[str],    # Validation issues
        "warnings": List[str]   # Validation warnings
    },
    "subgraph_size": int,       # Number of nodes in subgraph
    "query_event_id": str,      # Audit event ID
    "sources": List[str]        # Source document IDs
}
```

### Audit Event

Represents an audit log entry.

```python
{
    "event_id": str,            # Unique event identifier
    "event_type": str,         # Event type enum
    "timestamp": datetime,     # Event timestamp (ISO 8601)
    "user_id": str,            # User identifier
    "session_id": str,         # Session identifier
    "details": {
        # Event-specific details
        "query": str,          # For query events
        "document_id": str,    # For document events
        "graph_version": str,  # For graph events
        # ... other fields
    }
}
```

## Event Types

```python
class AuditEventType(Enum):
    GRAPH_CREATED = "graph_created"
    GRAPH_UPDATED = "graph_updated"
    GRAPH_VERSIONED = "graph_versioned"
    SUBGRAPH_EXTRACTED = "subgraph_extracted"
    SUBGRAPH_VALIDATED = "subgraph_validated"
    LLM_QUERY = "llm_query"
    LLM_RESPONSE = "llm_response"
    REASONING_EXECUTED = "reasoning_executed"
    ERROR = "error"
```

## Validation Metadata

Structure for subgraph validation results.

```python
{
    "is_valid": bool,           # Overall validation result
    "groundedness_score": float, # 0.0-1.0
    "issues": List[str],        # Blocking issues
    "warnings": List[str],      # Non-blocking warnings
    "metadata_score": float,   # Metadata completeness (0.0-1.0)
    "connectivity_score": float, # Graph connectivity (0.0-1.0)
    "verification_score": float  # Source verification (0.0-1.0)
}
```

## API Request/Response Models

### DocumentRequest

```python
class DocumentRequest(BaseModel):
    document_id: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    metadata: Optional[Dict[str, Any]] = None
```

### DocumentResponse

```python
class DocumentResponse(BaseModel):
    document_id: str
    graph_version: str
    version_id: str
    status: str
```

### QueryRequest

```python
class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    graph_id: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None
```

### QueryResponse

```python
class QueryResponse(BaseModel):
    answer: str
    model: str
    validation: Dict[str, Any]
    subgraph_size: int
    query_event_id: str
```

## Database Schemas

### Graph Storage (Neptune)

**Vertex Schema**:
- `id`: String (primary key)
- `label`: String
- `properties`: Map<String, Any>
- `created_at`: DateTime
- `updated_at`: DateTime

**Edge Schema**:
- `id`: String (primary key)
- `label`: String (relationship type)
- `from`: String (source vertex ID)
- `to`: String (target vertex ID)
- `properties`: Map<String, Any>
- `created_at`: DateTime

### Audit Storage

**Audit Events Table**:
- `event_id`: String (primary key)
- `event_type`: String
- `timestamp`: DateTime
- `user_id`: String
- `session_id`: String
- `details`: JSON
- `created_at`: DateTime (indexed)

## Data Constraints

### Document
- `document_id`: Required, unique, 1-255 characters
- `content`: Required, minimum 1 character
- `metadata`: Optional, must be valid JSON

### Query
- `query`: Required, 1-1000 characters
- `filters`: Optional, must be valid JSON object

### Graph Node
- `id`: Required, unique
- `label`: Required, non-empty string
- `properties`: Optional, must be valid JSON object

### Graph Edge
- `source`: Required, must reference existing node
- `target`: Required, must reference existing node
- `relationship`: Required, non-empty string

## Data Validation Rules

1. **Document IDs**: Must be unique within a tenant
2. **Graph Versions**: Must be sequential
3. **Timestamps**: Must be ISO 8601 format
4. **Groundedness Scores**: Must be between 0.0 and 1.0
5. **Query Length**: Maximum 1000 characters
6. **Node IDs**: Must be valid URI or UUID format

## References

- API Specification: `docs/product/API_SPEC.md`
- Graph Model: `docs/architecture/GRAPH_MODEL.md`
- System Architecture: `docs/architecture/SYSTEM_ARCHITECTURE.md`

