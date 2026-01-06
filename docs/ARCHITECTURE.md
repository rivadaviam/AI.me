# Architecture Overview

## System Architecture

AI.me es una infraestructura de metadata basada en grafos diseñada para hacer que los agentes autónomos sean fiables, auditables y alineados con la realidad.

### Componentes Principales

#### 1. Graph Processing (`src/core/graph/`)
- **GraphProcessor**: Convierte documentación y datos en grafos semánticos versionados
- Utiliza NetworkX para representación de grafos
- Soporta RDF para interoperabilidad semántica

#### 2. Reasoning Engine (`src/core/reasoning/`)
- **ReasoningEngine**: Motor de razonamiento que filtra y valida subgrafos aplicables
- Calcula scores de groundedness
- Valida completitud, conectividad y verificación de fuentes

#### 3. Versioning System (`src/core/versioning/`)
- **VersionManager**: Sistema de versionado para trazabilidad temporal
- Soporta versiones major, minor, patch y temporales
- Valida validez temporal de versiones

#### 4. Audit Trail (`src/core/audit/`)
- **AuditLogger**: Registro completo de todas las operaciones
- Trazabilidad completa para compliance
- Soporte para análisis y debugging

#### 5. AWS Integrations (`src/integrations/aws/`)
- **BedrockClient**: Integración con AWS Bedrock para LLM
- **NeptuneClient**: Integración con AWS Neptune para almacenamiento de grafos

#### 6. LLM Service (`src/integrations/llm/`)
- Abstracción sobre servicios LLM
- Soporte para múltiples proveedores (Bedrock, OpenAI, etc.)

#### 7. API Layer (`src/api/`)
- FastAPI REST API
- Endpoints para procesamiento de documentos y queries
- Health checks y monitoring

#### 8. Services (`src/services/`)
- **GraphService**: Lógica de negocio que orquesta todos los componentes
- Procesamiento end-to-end desde documentos hasta respuestas grounded

## Flujo de Datos

### Procesamiento de Documentos
1. Documento → GraphProcessor → Grafo Semántico
2. VersionManager → Crea versión del grafo
3. AuditLogger → Registra evento

### Query y Respuesta
1. Query → ReasoningEngine → Filtra subgrafo relevante
2. ReasoningEngine → Valida subgrafo (groundedness)
3. Subgrafo → LLM Service → Genera respuesta grounded
4. AuditLogger → Registra todo el proceso

## Integraciones

### AWS Bedrock
- Modelos Claude, Titan, etc.
- Configuración vía variables de entorno
- Soporte para system prompts y context

### AWS Neptune
- Almacenamiento de grafos a escala
- Queries Gremlin
- IAM authentication

## Escalabilidad

- Arquitectura modular y desacoplada
- Preparado para horizontal scaling
- Caching de subgrafos frecuentes
- Async/await para operaciones I/O

## Seguridad

- Audit trail completo
- Versionado para trazabilidad
- Validación de groundedness
- API keys y authentication (a implementar)

