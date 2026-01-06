# AI.me - Graph-Based Metadata Infrastructure for Agentic AI

Graph-based metadata infrastructure that converts documentation and data into versioned semantic graphs, applies reasoning to validate applicable subgraphs, and integrates with LLM services to generate grounded and auditable responses.

## 🎯 Vision

Making autonomous agents reliable, auditable, and aligned with reality through a knowledge and metadata layer that ensures precision, temporal validity, and traceability.

## 🏗️ Architecture

- **Graph Processing**: Conversion of documentation and data into versioned semantic graphs
- **Reasoning Engine**: Reasoning engine that filters and validates applicable subgraphs
- **LLM Integration**: Integration with AWS Bedrock and other LLM services
- **Versioning System**: Versioning system for temporal traceability
- **Audit Trail**: Complete logging of every step for auditing and analysis
- **API Layer**: RESTful API for integration with external systems

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose (optional)
- AWS Account (for Bedrock and Neptune)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd ikl

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your AWS credentials and configurations
```

### Basic Usage

```bash
# Run the API server
python -m src.api.main

# Or using Docker
docker-compose up
```

## 📁 Project Structure

```
ikl/
├── src/
│   ├── core/              # Core system modules
│   │   ├── graph/         # Graph processing
│   │   ├── reasoning/     # Reasoning engine
│   │   ├── versioning/    # Versioning system
│   │   └── audit/         # Audit system
│   ├── integrations/      # External integrations
│   │   ├── aws/           # AWS Bedrock, Neptune
│   │   └── llm/           # LLM abstractions
│   ├── api/               # REST API
│   ├── services/          # Business services
│   └── utils/             # Utilities
├── tests/                 # Tests
├── docs/                  # Documentation
├── docker/                # Docker configurations
└── scripts/               # Utility scripts
```

## 🔧 Configuration

See `.env.example` for all available environment variables.

### Main Variables

- `AWS_REGION`: AWS region
- `AWS_ACCESS_KEY_ID`: AWS access key
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `NEPTUNE_ENDPOINT`: Neptune endpoint
- `BEDROCK_MODEL_ID`: Bedrock model ID to use
- `LOG_LEVEL`: Logging level

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=src --cov-report=html
```

## 📚 Documentation

Full documentation is available in `docs/`.

## 🤝 Contributing

This is a private project. For contributions, please contact the team.

## 📄 License

Proprietary - All rights reserved

## 🔗 Links

- [AWS Bedrock](https://aws.amazon.com/bedrock/)
- [AWS Neptune](https://aws.amazon.com/neptune/)
