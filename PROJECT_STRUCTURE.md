# Estructura del Proyecto

```
ikl/
├── src/                          # Código fuente principal
│   ├── __init__.py
│   ├── api/                      # Capa API REST
│   │   ├── __init__.py
│   │   └── main.py              # FastAPI application
│   ├── core/                     # Módulos core del sistema
│   │   ├── __init__.py
│   │   ├── graph/                # Procesamiento de grafos
│   │   │   ├── __init__.py
│   │   │   └── processor.py     # GraphProcessor
│   │   ├── reasoning/            # Motor de razonamiento
│   │   │   ├── __init__.py
│   │   │   └── engine.py         # ReasoningEngine
│   │   ├── versioning/           # Sistema de versionado
│   │   │   ├── __init__.py
│   │   │   └── manager.py        # VersionManager
│   │   └── audit/                # Sistema de auditoría
│   │       ├── __init__.py
│   │       └── logger.py         # AuditLogger
│   ├── integrations/             # Integraciones externas
│   │   ├── __init__.py
│   │   ├── aws/                  # Integraciones AWS
│   │   │   ├── __init__.py
│   │   │   ├── bedrock_client.py # Cliente AWS Bedrock
│   │   │   └── neptune_client.py # Cliente AWS Neptune
│   │   └── llm/                  # Abstracciones LLM
│   │       ├── __init__.py
│   │       └── service.py        # LLMService abstraction
│   ├── services/                 # Servicios de negocio
│   │   ├── __init__.py
│   │   └── graph_service.py      # GraphService (orquestador)
│   └── utils/                    # Utilidades
│       ├── __init__.py
│       └── config.py             # Configuración
├── tests/                        # Tests
│   ├── __init__.py
│   ├── test_graph_processor.py
│   └── test_reasoning_engine.py
├── docs/                         # Documentación
│   ├── ARCHITECTURE.md
│   └── QUICKSTART.md
├── examples/                     # Ejemplos de uso
│   └── example_usage.py
├── scripts/                      # Scripts de utilidad
│   ├── setup.sh
│   └── run_tests.sh
├── docker/                       # Configuraciones Docker
│   └── Dockerfile
├── .env.example                  # Template de variables de entorno
├── .gitignore
├── .dockerignore
├── docker-compose.yml            # Docker Compose configuration
├── Makefile                      # Comandos útiles
├── pyproject.toml                # Configuración del proyecto
├── requirements.txt              # Dependencias Python
└── README.md                     # Documentación principal
```

## Componentes Clave

### Core Modules (`src/core/`)

1. **Graph Processing** (`graph/processor.py`)
   - Convierte documentos en grafos semánticos
   - Utiliza NetworkX y RDFLib
   - Extracción de entidades y relaciones

2. **Reasoning Engine** (`reasoning/engine.py`)
   - Filtra y valida subgrafos aplicables
   - Calcula scores de groundedness
   - Validación de completitud y conectividad

3. **Versioning** (`versioning/manager.py`)
   - Sistema de versionado temporal
   - Trazabilidad de cambios
   - Validación de validez temporal

4. **Audit Trail** (`audit/logger.py`)
   - Registro completo de operaciones
   - Trazabilidad para compliance
   - Análisis y debugging

### Integrations (`src/integrations/`)

1. **AWS Bedrock** (`aws/bedrock_client.py`)
   - Integración con modelos LLM de AWS
   - Soporte para Claude, Titan, etc.
   - System prompts y context injection

2. **AWS Neptune** (`aws/neptune_client.py`)
   - Almacenamiento de grafos a escala
   - Queries Gremlin
   - IAM authentication

3. **LLM Service** (`llm/service.py`)
   - Abstracción sobre servicios LLM
   - Factory pattern para múltiples proveedores

### Services (`src/services/`)

1. **Graph Service** (`graph_service.py`)
   - Orquesta todos los componentes
   - Flujo end-to-end: documento → grafo → query → respuesta
   - Integración con audit trail

### API (`src/api/`)

1. **FastAPI Application** (`main.py`)
   - REST API para procesamiento y queries
   - Health checks
   - Documentación automática (Swagger)

## Flujos Principales

### Procesamiento de Documentos
```
Documento → GraphProcessor → Grafo Semántico → VersionManager → AuditLogger
```

### Query y Respuesta
```
Query → ReasoningEngine (filtra) → ReasoningEngine (valida) → 
LLM Service (genera) → AuditLogger (registra)
```

## Próximos Pasos de Desarrollo

1. **NLP Integration**: Implementar extracción real de entidades con spaCy
2. **Neptune Persistence**: Conectar con Neptune para almacenamiento persistente
3. **Advanced Reasoning**: Reglas de validación más sofisticadas
4. **Caching**: Implementar cache de subgrafos frecuentes
5. **Authentication**: Agregar autenticación y autorización
6. **Monitoring**: Integrar con CloudWatch, Prometheus, etc.
7. **Batch Processing**: Soporte para procesamiento en lote

