# Integration Guide

## Overview

This guide provides patterns and examples for integrating AI.me with external systems and services.

## Integration Patterns

### 1. Document Ingestion

#### Pattern: Batch Document Processing

Process multiple documents in batch:

```python
from src.services.graph_service import GraphService
from src.core.graph.processor import GraphProcessor
# ... other imports

# Initialize service
service = create_graph_service()

# Process documents
documents = [
    {"document_id": "doc-1", "content": "...", "metadata": {...}},
    {"document_id": "doc-2", "content": "...", "metadata": {...}},
]

results = []
for doc in documents:
    result = service.process_document(
        document_id=doc["document_id"],
        content=doc["content"],
        metadata=doc.get("metadata")
    )
    results.append(result)
```

#### Pattern: Real-time Document Processing

Process documents as they arrive:

```python
import asyncio
from src.api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

async def process_document_realtime(document):
    response = client.post(
        "/documents",
        json={
            "document_id": document["id"],
            "content": document["content"],
            "metadata": document.get("metadata", {})
        }
    )
    return response.json()
```

### 2. Query Integration

#### Pattern: Synchronous Query

```python
def query_graph_sync(query: str, filters: dict = None):
    client = TestClient(app)
    response = client.post(
        "/query",
        json={
            "query": query,
            "filters": filters or {}
        }
    )
    return response.json()
```

#### Pattern: Asynchronous Query with Callback

```python
import asyncio

async def query_graph_async(query: str, callback):
    client = TestClient(app)
    response = client.post("/query", json={"query": query})
    result = response.json()
    await callback(result)
    return result
```

### 3. Webhook Integration

#### Pattern: Document Processing Webhook

```python
from fastapi import FastAPI, Request
import httpx

app = FastAPI()

@app.post("/webhook/document-processed")
async def document_webhook(request: Request):
    data = await request.json()
    document_id = data["document_id"]
    graph_version = data["graph_version"]
    
    # Notify external system
    async with httpx.AsyncClient() as client:
        await client.post(
            "https://external-system.com/notify",
            json={
                "document_id": document_id,
                "status": "processed",
                "graph_version": graph_version
            }
        )
    
    return {"status": "ok"}
```

### 4. AWS Service Integration

#### AWS Bedrock Integration

```python
from src.integrations.aws.bedrock_client import BedrockClient

bedrock = BedrockClient(
    region_name="us-east-1",
    model_id="anthropic.claude-v2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

response = bedrock.invoke_model(
    prompt="What is AI?",
    system_prompt="You are a helpful assistant.",
    max_tokens=4096,
    temperature=0.7
)
```

#### AWS Neptune Integration

```python
from src.integrations.aws.neptune_client import NeptuneClient

neptune = NeptuneClient(
    endpoint="your-neptune-endpoint",
    port=8182,
    use_ssl=True,
    region_name="us-east-1"
)

# Add vertex
vertex_id = neptune.add_vertex(
    label="Document",
    properties={"name": "Test Document", "source": "test"}
)

# Add edge
edge_id = neptune.add_edge(
    from_vertex_id="vertex-1",
    to_vertex_id="vertex-2",
    label="RELATED_TO",
    properties={"weight": 0.8}
)
```

### 5. Database Integration

#### PostgreSQL Integration

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(bind=engine)

def store_audit_event(event_data):
    session = Session()
    try:
        # Store audit event in database
        audit_event = AuditEvent(**event_data)
        session.add(audit_event)
        session.commit()
    finally:
        session.close()
```

### 6. Message Queue Integration

#### Pattern: RabbitMQ Integration

```python
import pika

def publish_document_event(document_id, graph_version):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost')
    )
    channel = connection.channel()
    
    channel.queue_declare(queue='document_processed')
    
    channel.basic_publish(
        exchange='',
        routing_key='document_processed',
        body=json.dumps({
            "document_id": document_id,
            "graph_version": graph_version,
            "timestamp": datetime.utcnow().isoformat()
        })
    )
    
    connection.close()
```

#### Pattern: AWS SQS Integration

```python
import boto3

sqs = boto3.client('sqs', region_name='us-east-1')

def publish_to_sqs(queue_url, message):
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message)
    )
    return response['MessageId']
```

## Integration Examples

### Example 1: CMS Integration

Integrate with Content Management System:

```python
class CMSIntegration:
    def __init__(self, graph_service: GraphService):
        self.graph_service = graph_service
    
    def sync_cms_content(self, cms_client):
        """Sync content from CMS to graph"""
        articles = cms_client.get_all_articles()
        
        for article in articles:
            self.graph_service.process_document(
                document_id=f"cms-{article['id']}",
                content=article['content'],
                metadata={
                    "source": "cms",
                    "author": article['author'],
                    "published_at": article['published_at'],
                    "url": article['url']
                }
            )
```

### Example 2: Customer Support Integration

Integrate with customer support system:

```python
class SupportIntegration:
    def __init__(self, graph_service: GraphService):
        self.graph_service = graph_service
    
    def answer_support_query(self, query: str):
        """Answer customer support query using graph"""
        result = self.graph_service.query(
            query=query,
            filters={"source": "support_docs"}
        )
        
        return {
            "answer": result["answer"],
            "sources": result.get("sources", []),
            "confidence": result["validation"]["groundedness_score"]
        }
```

### Example 3: Research Platform Integration

Integrate with research platform:

```python
class ResearchIntegration:
    def __init__(self, graph_service: GraphService):
        self.graph_service = graph_service
    
    def query_research(self, research_query: str, date_range: dict):
        """Query research papers with temporal filtering"""
        result = self.graph_service.query(
            query=research_query,
            filters={
                "source": "research",
                "date_range": date_range,
                "min_groundedness": 0.8
            }
        )
        
        return {
            "answer": result["answer"],
            "papers": result.get("sources", []),
            "validation": result["validation"]
        }
```

## Error Handling

### Retry Pattern

```python
import time
from functools import wraps

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay * (attempt + 1))
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2)
def process_document_with_retry(document):
    return graph_service.process_document(**document)
```

### Circuit Breaker Pattern

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
    
    def call(self, func, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker is open")
        
        try:
            result = func(*args, **kwargs)
            if self.state == "half-open":
                self.state = "closed"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
            raise
```

## Best Practices

1. **Use Connection Pooling**: Reuse connections for external services
2. **Implement Retries**: Handle transient failures gracefully
3. **Monitor Integration Health**: Track integration metrics
4. **Handle Rate Limits**: Respect API rate limits
5. **Cache When Appropriate**: Cache frequently accessed data
6. **Log Integration Events**: Track all integration interactions
7. **Use Async When Possible**: Improve performance with async operations

## References

- API Specification: `docs/product/API_SPEC.md`
- Architecture: `docs/architecture/SYSTEM_ARCHITECTURE.md`
- Deployment: `docs/product/DEPLOYMENT.md`

