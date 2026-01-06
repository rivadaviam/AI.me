# Quick Start Guide

## Prerequisites

- Python 3.11 or higher
- AWS Account with access to Bedrock (and optionally Neptune)
- Docker and Docker Compose (optional)

## Quick Installation

### Option 1: Automatic Setup

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### Option 2: Manual

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e ".[dev]"

# Configure environment variables
cp .env.example .env
# Edit .env with your credentials
```

## Configuration

Edit the `.env` file with your AWS credentials:

```bash
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
BEDROCK_MODEL_ID=anthropic.claude-v2
```

## Running the Application

### Local Development

```bash
# Activate virtual environment
source venv/bin/activate

# Run server
make run
# Or directly:
python -m src.api.main
```

The API will be available at `http://localhost:8000`

### Docker

```bash
# Build and run
make docker-build
make docker-up

# View logs
docker-compose logs -f
```

## API Usage

### Process a Document

```bash
curl -X POST "http://localhost:8000/documents" \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "doc-1",
    "content": "This is a test document about artificial intelligence.",
    "metadata": {
      "source": "test",
      "author": "AI.me Team"
    }
  }'
```

### Make a Query

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is artificial intelligence?",
    "filters": {}
  }'
```

### View API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger documentation.

## Testing

```bash
# Run all tests
make test

# Or with the script
chmod +x scripts/run_tests.sh
./scripts/run_tests.sh
```

## Development

### Format Code

```bash
make format
```

### Linting

```bash
make lint
```

## Next Steps

1. Integrate with AWS Neptune for persistent graph storage
2. Implement entity extraction with NLP (spaCy, NER)
3. Improve the reasoning engine with more sophisticated rules
4. Add authentication and authorization
5. Implement caching of subgraphs

## Additional Resources

### Development
- [Setup Guide](development/SETUP_GUIDE.md) - Detailed development environment setup
- [Coding Standards](development/CODING_STANDARDS.md) - Code style and standards
- [Testing Guide](development/TESTING_GUIDE.md) - Testing strategies and examples
- [Contributing](development/CONTRIBUTING.md) - Contribution guidelines
- [Troubleshooting](development/TROUBLESHOOTING.md) - Common issues and solutions

### Documentation
- [Product Specification](product/PRODUCT_SPEC.md) - Complete product specification
- [API Specification](product/API_SPEC.md) - Detailed API documentation
- [Integration Guide](product/INTEGRATION_GUIDE.md) - Integration patterns
- [Deployment Guide](product/DEPLOYMENT.md) - Deployment procedures

### AI Agent Workflows
- [Development Workflow](workflows/development.md) - AI agent development guide
- [Code Review Workflow](workflows/review.md) - Automated review process
- [Testing Workflow](workflows/testing.md) - Testing strategy and workflow

## Troubleshooting

### Error: AWS Credentials not found
- Verify that `.env` has the correct credentials
- Or configure AWS CLI: `aws configure`

### Error: Bedrock model not available
- Verify that the model is available in your region
- List available models: `aws bedrock list-foundation-models`

### Error: Port already in use
- Change the port in `.env`: `API_PORT=8001`
