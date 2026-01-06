# NXO - Graph-Based Metadata Infrastructure for Agentic AI

NXO is a platform that converts documentation and data into versioned semantic graphs, applies reasoning to filter and validate applicable subgraphs, and integrates with LLM services (like AWS Bedrock) to generate responses strictly based on validated knowledge.

## 🎯 Problem Statement / Visión

Organizations adopting generative AI and autonomous agents face challenges with:
- **Hallucinations**: LLMs generating incorrect or fabricated information  
- **Lack of Context**: Superficial embeddings that miss semantic relationships  
- **Legal/Commercial Risks**: Unreliable information leading to compliance issues  
- **Temporal Validity**: Outdated information being used in responses

> **Visión:**  
> Hacer que los agentes autónomos sean fiables, auditables y alineados con la realidad mediante una capa de conocimiento y metadata que asegure precisión, validez temporal y trazabilidad.

NXO addresses these by providing a **knowledge and metadata layer** that ensures precision, temporal validity, and full traceability.

## 🏗️ Architecture / Arquitectura

### Core Components / Componentes principales

1. **Graph Processing / Graph Builder**  
   Conversión de documentación y datos en grafos semánticos versionados. Extracts entities and relationships, manages graph updates and versioning.

2. **Reasoning Engine**   
   Motor de razonamiento que filtra y valida subgrafos aplicables. Applies temporal, validity, and source filters to ensure completeness and consistency.

3. **Version Manager / Sistema de versionado**  
   Manages graph versions and snapshots for temporal traceability. Provides audit trail of changes and enables temporal queries.

4. **Audit Trail / Audit Logger**  
   Registro completo de cada paso para auditoría y análisis. Tracks query-response cycles and enables compliance and transparency.

5. **LLM Integration**  
   Integración con AWS Bedrock y otros servicios LLM. Generates responses strictly based on validated subgraphs for groundedness and auditability.

6. **API Layer**  
   API RESTful para integración con sistemas externos.

### Project Structure / Estructura del Proyecto

```
nxo/
├── nxo/                    # Main package / Paquete principal
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   ├── core/               # Core modules / Componentes núcleo
│   │   ├── graph_builder.py
│   │   ├── reasoning_engine.py
│   │   └── versioning.py
│   ├── integrations/       # External integrations / Integraciones externas
│   │   ├── bedrock.py      # AWS Bedrock
│   │   └── neptune.py      # AWS Neptune
│   ├── audit/              # Audit and logging / Auditoría
│   │   └── audit_logger.py
│   ├── api/                # API REST / FastAPI
│   │   ├── main.py
│   │   └── models.py
│   └── utils/              # Utilities / Utilidades
│       └── logger.py
├── tests/                  # Tests
├── pyproject.toml
├── requirements.txt
├── Makefile
└── README.md
```

## 🚀 Quick Start / Inicio Rápido

### Prerequisites / Prerrequisitos

- Python 3.10+
- AWS Account with Bedrock and Neptune access / Cuenta AWS (Bedrock, Neptune)
- Docker (opcional)

### Installation / Instalación

```bash
# Clone the repository / Clonar el repositorio
git clone <repository-url>
cd nxo

# Create virtual environment / Crear entorno virtual
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies / Instalar dependencias
pip install -r requirements.txt
# OR
make install-dev

# Configure environment variables / Configurar variables de entorno
cp .env.example .env
# Edit .env with your AWS credentials and configuration / Editar .env con tus credenciales y configuración
```

### Running the API / Uso Básico

```bash
# Run API server
python -m nxo.api.main

# OR
make run

# OR using Docker
docker-compose up
```

The API will be available at `http://localhost:8000`  
API documentation: `http://localhost:8000/docs`

## 📖 Usage / Ejemplo de Uso

### Building a Graph from Documents

```python
from nxo.core.graph_builder import GraphBuilder
from nxo.integrations.neptune import NeptuneClient

neptune = NeptuneClient()
builder = GraphBuilder(neptune)

documents = [
    {
        "id": "doc1",
        "title": "Product Documentation",
        "content": "NXO is a graph-based AI platform...",
        "created_at": "2024-01-01T00:00:00Z"
    }
]

graph_id = await builder.build_from_documents(
    documents=documents,
    metadata={"source": "docs", "version": "1.0"},
    version="v1.0"
)
```

### Querying with Grounded Responses

```python
from nxo.core.reasoning_engine import ReasoningEngine
from nxo.integrations.bedrock import BedrockClient

engine = ReasoningEngine(neptune)
bedrock = BedrockClient()

subgraph = await engine.get_applicable_subgraph(
    query="What is NXO?",
    graph_id=graph_id,
    filters={"valid_until": "2024-12-31"}
)

response = await bedrock.generate_response(
    prompt="What is NXO?",
    context={},
    subgraph=subgraph
)
```

### Using the REST API

#### Build a Graph

```bash
curl -X POST "http://localhost:8000/graphs" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      {
        "id": "doc1",
        "title": "Test Document",
        "content": "This is test content"
      }
    ],
    "metadata": {"source": "test"},
    "version": "v1.0"
  }'
```

#### Query the Graph

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is NXO?",
    "graph_id": "graph_2024-01-01T00:00:00_v1.0",
    "filters": {
      "valid_until": "2024-12-31"
    }
  }'
```

## 🔧 Configuration / Configuración

See `.env.example` for all available environment variables.  
Ver `.env.example` para todas las variables de entorno disponibles.

### Main Variables / Variables Principales

- `AWS_REGION`: AWS region
- `AWS_ACCESS_KEY_ID`: AWS access key
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `NEPTUNE_ENDPOINT`: Neptune database endpoint
- `BEDROCK_MODEL_ID`: Bedrock model ID
- `LOG_LEVEL`: Logging level

- **Graph Database**: (Neptune, Neo4j, in-memory)
- **Versioning**: Storage type (S3, local)
- **Audit**: Storage type (CloudWatch, S3, local)

## 🧪 Testing

```bash
make test
# or
pytest tests/ -v
# With coverage
pytest tests/ -v --cov=nxo --cov-report=html
```

## 📚 Documentación

La documentación completa está disponible en `docs/`.  
Full documentation available in the `docs/` directory.

## 🤝 Contribution / Contribución

This is a proprietary project. For contributions, please contact the development team.  
Este es un proyecto privado. Para contribuciones, contactar al equipo.

## 📝 License / Licencia

Proprietary - All rights reserved / Todos los derechos reservados

## 📧 Contact / Enlaces

For questions or support, please contact: info@ai.me

- [AWS Bedrock](https://aws.amazon.com/bedrock/)
- [AWS Neptune](https://aws.amazon.com/neptune/)

---

**Built for the future of Agentic AI** 🤖
