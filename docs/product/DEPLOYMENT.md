# Deployment Guide

## Overview

This guide covers deployment procedures for the AI.me platform across different environments.

## Prerequisites

- Docker and Docker Compose installed
- AWS Account with appropriate permissions
- AWS CLI configured
- Kubernetes cluster (for K8s deployment)

## Environment Configuration

### Environment Variables

Required environment variables (see `.env.example`):

```bash
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key

# Neptune Configuration
NEPTUNE_ENDPOINT=your-neptune-endpoint
NEPTUNE_PORT=8182

# Bedrock Configuration
BEDROCK_MODEL_ID=anthropic.claude-v2
BEDROCK_REGION=us-east-1

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Security
SECRET_KEY=your-secret-key
API_KEY=your-api-key
```

## Deployment Methods

### 1. Docker Deployment

#### Build Image

```bash
docker build -t ai-me:latest -f docker/Dockerfile .
```

#### Run Container

```bash
docker run -d \
  --name ai-me \
  -p 8000:8000 \
  --env-file .env \
  ai-me:latest
```

#### Docker Compose

```bash
docker-compose up -d
```

### 2. AWS ECS Deployment

#### Create ECS Task Definition

```json
{
  "family": "ai-me",
  "containerDefinitions": [{
    "name": "ai-me",
    "image": "your-ecr-repo/ai-me:latest",
    "portMappings": [{
      "containerPort": 8000,
      "protocol": "tcp"
    }],
    "environment": [
      {"name": "AWS_REGION", "value": "us-east-1"},
      {"name": "API_PORT", "value": "8000"}
    ],
    "secrets": [
      {"name": "AWS_ACCESS_KEY_ID", "valueFrom": "arn:aws:secretsmanager:..."},
      {"name": "AWS_SECRET_ACCESS_KEY", "valueFrom": "arn:aws:secretsmanager:..."}
    ]
  }],
  "requiresCompatibilities": ["FARGATE"],
  "networkMode": "awsvpc",
  "cpu": "512",
  "memory": "1024"
}
```

#### Deploy to ECS

```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
aws ecs create-service --cluster ai-me-cluster --service-name ai-me --task-definition ai-me
```

### 3. Kubernetes Deployment

#### Deployment Manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-me
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-me
  template:
    metadata:
      labels:
        app: ai-me
    spec:
      containers:
      - name: ai-me
        image: your-registry/ai-me:latest
        ports:
        - containerPort: 8000
        env:
        - name: AWS_REGION
          value: "us-east-1"
        envFrom:
        - secretRef:
            name: ai-me-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
```

#### Service Manifest

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ai-me-service
spec:
  selector:
    app: ai-me
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

#### Deploy

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

### 4. AWS Lambda Deployment (Serverless)

#### Lambda Function Configuration

```python
# lambda_handler.py
from src.api.main import app
from mangum import Mangum

handler = Mangum(app)
```

#### Serverless Framework

```yaml
# serverless.yml
service: ai-me

provider:
  name: aws
  runtime: python3.11
  region: us-east-1
  environment:
    AWS_REGION: ${self:provider.region}

functions:
  api:
    handler: lambda_handler.handler
    events:
      - http:
          path: /{proxy+}
          method: ANY
```

## Environment-Specific Configurations

### Development

```bash
# .env.development
API_RELOAD=true
LOG_LEVEL=DEBUG
ENABLE_VERSIONING=true
ENABLE_AUDIT_TRAIL=true
```

### Staging

```bash
# .env.staging
API_RELOAD=false
LOG_LEVEL=INFO
ENABLE_VERSIONING=true
ENABLE_AUDIT_TRAIL=true
```

### Production

```bash
# .env.production
API_RELOAD=false
LOG_LEVEL=WARNING
ENABLE_VERSIONING=true
ENABLE_AUDIT_TRAIL=true
CORS_ALLOWED_ORIGINS=https://app.ai.me
```

## Database Setup

### PostgreSQL

```bash
# Create database
createdb ai_me_db

# Run migrations
alembic upgrade head
```

### AWS Neptune

```bash
# Create Neptune cluster
aws neptune create-db-cluster \
  --db-cluster-identifier ai-me-cluster \
  --engine neptune \
  --engine-version 1.2.0.0
```

## Monitoring and Logging

### CloudWatch Integration

```python
import boto3
import logging
from watchtower import CloudWatchLogHandler

logger = logging.getLogger()
logger.addHandler(CloudWatchLogHandler(
    log_group='ai-me',
    stream_name='api'
))
```

### Health Checks

```bash
# Health check endpoint
curl http://localhost:8000/health
```

## Scaling

### Horizontal Scaling

- Use load balancer (ALB, NLB, or K8s Service)
- Deploy multiple instances
- Configure auto-scaling based on CPU/memory

### Vertical Scaling

- Increase container resources
- Optimize database connections
- Use connection pooling

## Backup and Recovery

### Database Backups

```bash
# PostgreSQL backup
pg_dump ai_me_db > backup.sql

# Neptune backup (automated via AWS)
aws neptune create-db-cluster-snapshot \
  --db-cluster-snapshot-identifier ai-me-snapshot
```

### Configuration Backups

```bash
# Backup environment configuration
cp .env .env.backup
```

## Security

### Secrets Management

Use AWS Secrets Manager:

```bash
aws secretsmanager create-secret \
  --name ai-me/credentials \
  --secret-string file://secrets.json
```

### Network Security

- Use VPC for network isolation
- Configure security groups
- Enable SSL/TLS
- Use API keys for authentication

## Troubleshooting

### Common Issues

1. **Connection Errors**: Check AWS credentials and network configuration
2. **Memory Issues**: Increase container memory limits
3. **Timeout Errors**: Adjust timeout settings and optimize queries
4. **Database Connection**: Verify database URL and credentials

### Logs

```bash
# Docker logs
docker logs ai-me

# Kubernetes logs
kubectl logs deployment/ai-me

# ECS logs
aws logs tail /ecs/ai-me --follow
```

## References

- Architecture: `docs/architecture/SYSTEM_ARCHITECTURE.md`
- API Specification: `docs/product/API_SPEC.md`
- Integration Guide: `docs/product/INTEGRATION_GUIDE.md`

