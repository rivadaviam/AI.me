# Project Structure

```
ikl/
├── src/                          # Main source code
│   ├── __init__.py
│   ├── api/                      # REST API layer
│   │   ├── __init__.py
│   │   └── main.py              # FastAPI application
│   ├── core/                     # Core system modules
│   │   ├── __init__.py
│   │   ├── graph/                # Graph processing
│   │   │   ├── __init__.py
│   │   │   └── processor.py     # GraphProcessor
│   │   ├── reasoning/            # Reasoning engine
│   │   │   ├── __init__.py
│   │   │   └── engine.py         # ReasoningEngine
│   │   ├── versioning/           # Versioning system
│   │   │   ├── __init__.py
│   │   │   └── manager.py        # VersionManager
│   │   └── audit/                # Audit system
│   │       ├── __init__.py
│   │       └── logger.py         # AuditLogger
│   ├── integrations/             # External integrations
│   │   ├── __init__.py
│   │   ├── aws/                  # AWS integrations
│   │   │   ├── __init__.py
│   │   │   ├── bedrock_client.py # AWS Bedrock client
│   │   │   └── neptune_client.py # AWS Neptune client
│   │   └── llm/                  # LLM abstractions
│   │       ├── __init__.py
│   │       └── service.py        # LLMService abstraction
│   ├── services/                 # Business services
│   │   ├── __init__.py
│   │   └── graph_service.py      # GraphService (orchestrator)
│   └── utils/                    # Utilities
│       ├── __init__.py
│       └── config.py             # Configuration
├── tests/                        # Tests
│   ├── __init__.py
│   ├── test_graph_processor.py
│   └── test_reasoning_engine.py
├── docs/                         # Documentation
│   ├── ARCHITECTURE.md
│   └── QUICKSTART.md
├── examples/                     # Usage examples
│   └── example_usage.py
├── scripts/                      # Utility scripts
│   ├── setup.sh
│   └── run_tests.sh
├── docker/                       # Docker configurations
│   └── Dockerfile
├── .env.example                  # Environment variables template
├── .gitignore
├── .dockerignore
├── docker-compose.yml            # Docker Compose configuration
├── Makefile                      # Useful commands
├── pyproject.toml                # Project configuration
├── requirements.txt              # Python dependencies
└── README.md                     # Main documentation
```

## Key Components

### Core Modules (`src/core/`)

1. **Graph Processing** (`graph/processor.py`)
   - Converts documents into semantic graphs
   - Uses NetworkX and RDFLib
   - Entity and relationship extraction

2. **Reasoning Engine** (`reasoning/engine.py`)
   - Filters and validates applicable subgraphs
   - Calculates groundedness scores
   - Completeness and connectivity validation

3. **Versioning** (`versioning/manager.py`)
   - Temporal versioning system
   - Change traceability
   - Temporal validity validation

4. **Audit Trail** (`audit/logger.py`)
   - Complete operation logging
   - Traceability for compliance
   - Analysis and debugging

### Integrations (`src/integrations/`)

1. **AWS Bedrock** (`aws/bedrock_client.py`)
   - Integration with AWS LLM models
   - Support for Claude, Titan, etc.
   - System prompts and context injection

2. **AWS Neptune** (`aws/neptune_client.py`)
   - Graph storage at scale
   - Gremlin queries
   - IAM authentication

3. **LLM Service** (`llm/service.py`)
   - Abstraction over LLM services
   - Factory pattern for multiple providers

### Services (`src/services/`)

1. **Graph Service** (`graph_service.py`)
   - Orchestrates all components
   - End-to-end flow: document → graph → query → response
   - Integration with audit trail

### API (`src/api/`)

1. **FastAPI Application** (`main.py`)
   - REST API for processing and queries
   - Health checks
   - Automatic documentation (Swagger)

## Main Flows

### Document Processing
```
Document → GraphProcessor → Semantic Graph → VersionManager → AuditLogger
```

### Query and Response
```
Query → ReasoningEngine (filters) → ReasoningEngine (validates) → 
LLM Service (generates) → AuditLogger (logs)
```

## Next Development Steps

1. **NLP Integration**: Implement real entity extraction with spaCy
2. **Neptune Persistence**: Connect with Neptune for persistent storage
3. **Advanced Reasoning**: More sophisticated validation rules
4. **Caching**: Implement cache for frequent subgraphs
5. **Authentication**: Add authentication and authorization
6. **Monitoring**: Integrate with CloudWatch, Prometheus, etc.
7. **Batch Processing**: Support for batch processing
