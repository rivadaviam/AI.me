# Graph Model Specification

## Overview

The graph model defines how knowledge is represented as a semantic graph in AI.me.

## Graph Structure

### Node Types

1. **Document Nodes**: Represent source documents
2. **Entity Nodes**: Represent extracted entities (people, places, concepts)
3. **Concept Nodes**: Represent abstract concepts
4. **Relationship Nodes**: Represent relationships between entities

### Edge Types

1. **CONTAINS**: Document contains entity
2. **RELATED_TO**: Entities are related
3. **DEPENDS_ON**: Dependency relationship
4. **VERSION_OF**: Version relationship
5. **DERIVED_FROM**: Derivation relationship

## Graph Ontology

### Namespace

```
http://ai.me/ontology/
```

### Core Classes

- `Document`: Source document
- `Entity`: Extracted entity
- `Concept`: Abstract concept
- `Relationship`: Relationship between entities

### Properties

- `source`: Source document ID
- `timestamp`: Creation timestamp
- `verified`: Verification status
- `confidence`: Confidence score
- `metadata`: Additional metadata

## Graph Construction

### Entity Extraction

Entities are extracted from documents using NLP:
- Named Entity Recognition (NER)
- Entity linking
- Entity disambiguation

### Relationship Extraction

Relationships are detected:
- Co-occurrence analysis
- Dependency parsing
- Semantic similarity

### Graph Building

1. Create document node
2. Create entity nodes
3. Create edges (document → entities)
4. Create edges (entity → entity)
5. Add metadata to nodes/edges

## Graph Storage

### NetworkX Representation

- In-memory graph structure
- Efficient for processing
- Supports complex queries

### Neptune Storage

- Persistent graph database
- Gremlin query support
- Scalable to large graphs

## Graph Queries

### Query Patterns

1. **Entity Lookup**: Find entity by ID
2. **Relationship Traversal**: Follow relationships
3. **Subgraph Extraction**: Extract relevant subgraph
4. **Path Finding**: Find paths between nodes

### Gremlin Examples

```gremlin
// Find all entities in a document
g.V().hasLabel('Document').has('id', 'doc-1').out('CONTAINS')

// Find related entities
g.V().has('id', 'entity-1').out('RELATED_TO')

// Find path between entities
g.V().has('id', 'entity-1').repeat(out()).until(has('id', 'entity-2')).path()
```

## References

- Component Specs: `docs/architecture/COMPONENT_SPECS.md`
- Data Flow: `docs/architecture/DATA_FLOW.md`
- Reasoning Engine: `docs/architecture/REASONING_ENGINE.md`

