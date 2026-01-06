# AI.me - Graph-Based Metadata Infrastructure for Agentic AI

Infraestructura de metadata basada en grafos que convierte documentación y datos en grafos semánticos versionados, aplica razonamiento para validar subgrafos aplicables, e integra con servicios LLM para generar respuestas grounded y auditables.

## 🎯 Visión

Hacer que los agentes autónomos sean fiables, auditables y alineados con la realidad mediante una capa de conocimiento y metadata que asegure precisión, validez temporal y trazabilidad.

## 🏗️ Arquitectura

- **Graph Processing**: Conversión de documentación y datos en grafos semánticos versionados
- **Reasoning Engine**: Motor de razonamiento que filtra y valida subgrafos aplicables
- **LLM Integration**: Integración con AWS Bedrock y otros servicios LLM
- **Versioning System**: Sistema de versionado para trazabilidad temporal
- **Audit Trail**: Registro completo de cada paso para auditoría y análisis
- **API Layer**: API RESTful para integración con sistemas externos

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.11+
- Docker y Docker Compose (opcional)
- AWS Account (para Bedrock y Neptune)

### Instalación

```bash
# Clonar el repositorio
git clone <repository-url>
cd ikl

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales AWS y configuraciones
```

### Uso Básico

```bash
# Ejecutar el servidor API
python -m src.api.main

# O usando Docker
docker-compose up
```

## 📁 Estructura del Proyecto

```
ikl/
├── src/
│   ├── core/              # Módulos core del sistema
│   │   ├── graph/         # Procesamiento de grafos
│   │   ├── reasoning/     # Motor de razonamiento
│   │   ├── versioning/    # Sistema de versionado
│   │   └── audit/         # Sistema de auditoría
│   ├── integrations/      # Integraciones externas
│   │   ├── aws/           # AWS Bedrock, Neptune
│   │   └── llm/           # Abstracciones LLM
│   ├── api/               # API REST
│   ├── services/          # Servicios de negocio
│   └── utils/             # Utilidades
├── tests/                 # Tests
├── docs/                  # Documentación
├── docker/                # Configuraciones Docker
└── scripts/               # Scripts de utilidad
```

## 🔧 Configuración

Ver `.env.example` para todas las variables de entorno disponibles.

### Variables Principales

- `AWS_REGION`: Región de AWS
- `AWS_ACCESS_KEY_ID`: Access Key de AWS
- `AWS_SECRET_ACCESS_KEY`: Secret Key de AWS
- `NEPTUNE_ENDPOINT`: Endpoint de Neptune
- `BEDROCK_MODEL_ID`: Model ID de Bedrock a usar
- `LOG_LEVEL`: Nivel de logging

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=src --cov-report=html
```

## 📚 Documentación

La documentación completa está disponible en `docs/`.

## 🤝 Contribución

Este es un proyecto privado. Para contribuciones, contactar al equipo.

## 📄 Licencia

Proprietary - Todos los derechos reservados

## 🔗 Enlaces

- [AWS Bedrock](https://aws.amazon.com/bedrock/)
- [AWS Neptune](https://aws.amazon.com/neptune/)
