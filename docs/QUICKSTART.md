# Quick Start Guide

## Prerrequisitos

- Python 3.11 o superior
- AWS Account con acceso a Bedrock (y opcionalmente Neptune)
- Docker y Docker Compose (opcional)

## Instalación Rápida

### Opción 1: Setup Automático

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### Opción 2: Manual

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
pip install -e ".[dev]"

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales
```

## Configuración

Edita el archivo `.env` con tus credenciales AWS:

```bash
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=tu-access-key
AWS_SECRET_ACCESS_KEY=tu-secret-key
BEDROCK_MODEL_ID=anthropic.claude-v2
```

## Ejecutar la Aplicación

### Desarrollo Local

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar servidor
make run
# O directamente:
python -m src.api.main
```

La API estará disponible en `http://localhost:8000`

### Docker

```bash
# Construir y ejecutar
make docker-build
make docker-up

# Ver logs
docker-compose logs -f
```

## Uso de la API

### Procesar un Documento

```bash
curl -X POST "http://localhost:8000/documents" \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "doc-1",
    "content": "Este es un documento de prueba sobre inteligencia artificial.",
    "metadata": {
      "source": "test",
      "author": "AI.me Team"
    }
  }'
```

### Hacer una Query

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "¿Qué es la inteligencia artificial?",
    "filters": {}
  }'
```

### Ver Documentación de la API

Visita `http://localhost:8000/docs` para la documentación interactiva de Swagger.

## Testing

```bash
# Ejecutar todos los tests
make test

# O con el script
chmod +x scripts/run_tests.sh
./scripts/run_tests.sh
```

## Desarrollo

### Formatear Código

```bash
make format
```

### Linting

```bash
make lint
```

## Próximos Pasos

1. Integrar con AWS Neptune para almacenamiento persistente de grafos
2. Implementar extracción de entidades con NLP (spaCy, NER)
3. Mejorar el motor de razonamiento con reglas más sofisticadas
4. Agregar autenticación y autorización
5. Implementar caching de subgrafos

## Troubleshooting

### Error: AWS Credentials not found
- Verifica que `.env` tenga las credenciales correctas
- O configura AWS CLI: `aws configure`

### Error: Bedrock model not available
- Verifica que el modelo esté disponible en tu región
- Lista modelos disponibles: `aws bedrock list-foundation-models`

### Error: Port already in use
- Cambia el puerto en `.env`: `API_PORT=8001`

