# NXO Architecture

## Overview

NXO is designed as a graph-based metadata infrastructure that sits between data sources and LLM services, ensuring that AI responses are grounded, validated, and auditable.

## System Architecture

```
┌─────────────┐
│   Clients   │
│  (API/CLI)  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│         FastAPI Layer               │
│  (REST API, Request Validation)     │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│         Core Services               │
│  ┌──────────────┐  ┌──────────────┐│
│  │ Graph Builder│  │   Reasoning  ││
│  │              │  │    Engine    ││
│  └──────┬───────┘  └──────┬───────┘│
│         │                  │        │
│  ┌──────▼──────────────────▼───────┐│
│  │      Version Manager            ││
│  └─────────────────────────────────┘│
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│      Integration Layer              │
│  ┌──────────────┐  ┌──────────────┐│
│  │   Neptune    │  │   Bedrock    ││
│  │   (Graph DB) │  │   (LLM)      ││
│  └──────────────┘  └──────────────┘│
└─────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│      Audit & Logging                │
│  (CloudWatch, S3, Local)            │
└─────────────────────────────────────┘
```

## Data Flow

### 1. Graph Building Flow

```
Documents → Graph Builder → Entity Extraction → Graph DB (Neptune)
                                    ↓
                            Version Manager → Storage (S3)
```

### 2. Query Flow

```
User Query → Reasoning Engine → Subgraph Extraction → Filtering & Validation
                                                              ↓
                                    Bedrock ← Formatted Context ← Subgraph
                                        ↓
                                    Response
                                        ↓
                                    Audit Logger
```

## Key Design Decisions

### 1. Graph-First Architecture

- All knowledge is stored as a graph, not just embeddings
- Enables semantic reasoning and relationship traversal
- Supports versioning and temporal queries

### 2. Subgraph Validation

- Only validated, relevant subgraphs are used for responses
- Reduces hallucinations by limiting context
- Ensures temporal validity and source verification

### 3. Audit Trail

- Every query-response cycle is logged
- Reasoning steps are recorded
- Enables compliance and debugging

### 4. AWS Integration

- Built for AWS ecosystem (Bedrock, Neptune)
- Designed as a complement, not competitor
- Marketplace-ready distribution

## Component Details

### Graph Builder

**Responsibilities:**
- Convert documents to graph representation
- Extract entities and relationships
- Manage graph updates

**Key Methods:**
- `build_from_documents()`: Create graph from document collection
- `update_graph()`: Update existing graph with new data
- `_extract_entities_and_relations()`: NLP/entity extraction

### Reasoning Engine

**Responsibilities:**
- Extract query intent
- Find relevant nodes
- Apply filters (temporal, validity, source)
- Expand to connected subgraph
- Validate completeness

**Key Methods:**
- `get_applicable_subgraph()`: Main entry point
- `_apply_filters()`: Filter nodes by criteria
- `_expand_subgraph()`: Build connected subgraph
- `_validate_subgraph()`: Ensure completeness

### Version Manager

**Responsibilities:**
- Create graph versions
- Track changes over time
- Enable temporal queries
- Compare versions

**Key Methods:**
- `create_version()`: Create new version
- `get_latest_version()`: Get most recent version
- `compare_versions()`: Diff two versions

### Bedrock Client

**Responsibilities:**
- Generate responses from subgraphs
- Ensure groundedness
- Format prompts with context
- Handle different model types

**Key Methods:**
- `generate_response()`: Main generation method
- `_build_grounded_prompt()`: Create context-aware prompt
- `_format_subgraph_as_context()`: Convert graph to text

### Neptune Client

**Responsibilities:**
- Graph database operations
- Gremlin query execution
- Node and edge management
- Graph cloning for versioning

**Key Methods:**
- `add_node()`: Add node to graph
- `add_edge()`: Add edge to graph
- `search_nodes()`: Find nodes by criteria
- `get_node_edges()`: Get connected edges

## Scalability Considerations

1. **Graph Database**: Neptune scales horizontally
2. **API Layer**: FastAPI supports async operations
3. **Caching**: Subgraph caching for common queries
4. **Batch Processing**: Document ingestion in batches
5. **Streaming**: Real-time graph updates (future)

## Security Considerations

1. **Authentication**: API key or OAuth (to be implemented)
2. **Authorization**: Role-based access control (to be implemented)
3. **Data Encryption**: At rest and in transit
4. **Audit Logging**: All operations logged
5. **Input Validation**: Pydantic models validate all inputs

## Future Enhancements

1. **Multi-Graph Support**: Query across multiple graphs
2. **GraphQL API**: More flexible query interface
3. **Real-time Updates**: WebSocket support for live updates
4. **Advanced Reasoning**: More sophisticated reasoning algorithms
5. **Graph Visualization**: Web UI for graph exploration
6. **LLM Fine-tuning**: Custom models trained on graph structure

