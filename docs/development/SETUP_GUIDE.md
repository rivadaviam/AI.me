# Development Environment Setup Guide

## Prerequisites

- Python 3.11 or higher
- Git
- Docker and Docker Compose (optional)
- AWS Account (for Bedrock/Neptune)

## Quick Setup

### Automated Setup

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### Manual Setup

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd ikl
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run Tests**
   ```bash
   pytest
   ```

## IDE Setup

### VS Code

Recommended extensions:
- Python
- Pylance
- Black Formatter
- Ruff

### PyCharm

- Configure Python interpreter to use venv
- Enable code inspections
- Configure test runner

## Database Setup

### PostgreSQL (for audit)

```bash
# Install PostgreSQL
# Create database
createdb ai_me_db

# Run migrations (when available)
alembic upgrade head
```

### Neptune (for graphs)

Configure in `.env`:
```bash
NEPTUNE_ENDPOINT=your-endpoint
NEPTUNE_PORT=8182
```

## AWS Configuration

1. **Configure AWS CLI**
   ```bash
   aws configure
   ```

2. **Set Environment Variables**
   ```bash
   export AWS_ACCESS_KEY_ID=your-key
   export AWS_SECRET_ACCESS_KEY=your-secret
   export AWS_REGION=us-east-1
   ```

## Running the Application

```bash
# Development server
python -m src.api.main

# Or using uvicorn directly
uvicorn src.api.main:app --reload
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure virtual environment is activated
2. **AWS Errors**: Check credentials and permissions
3. **Database Errors**: Verify database is running and accessible

## References

- Quick Start: `docs/QUICKSTART.md`
- Coding Standards: `docs/development/CODING_STANDARDS.md`

