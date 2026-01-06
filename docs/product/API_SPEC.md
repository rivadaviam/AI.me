# API Specification

## Overview

The AI.me API provides RESTful endpoints for document processing, graph querying, and audit trail access. All endpoints return JSON responses and use standard HTTP status codes.

## Base URL

```
Production: https://api.ai.me/v1
Development: http://localhost:8000
```

## Authentication

Currently, the API uses API keys passed in the `Authorization` header:

```
Authorization: Bearer <api_key>
```

Future versions will support OAuth 2.0 and AWS IAM authentication.

## Endpoints

### Health Check

#### GET /health

Check API health status.

**Response**:
```json
{
  "status": "healthy"
}
```

**Status Codes**:
- `200 OK`: Service is healthy
- `503 Service Unavailable`: Service is unavailable

---

### Root

#### GET /

Get API information.

**Response**:
```json
{
  "name": "AI.me - Graph-Based Metadata Infrastructure",
  "version": "0.1.0",
  "status": "running"
}
```

---

### Document Processing

#### POST /documents

Process a document into a semantic graph.

**Request Body**:
```json
{
  "document_id": "string (required, 1-255 chars)",
  "content": "string (required, min 1 char)",
  "metadata": {
    "source": "string",
    "author": "string",
    "topic": "string",
    "created_at": "ISO 8601 datetime",
    "expires_at": "ISO 8601 datetime"
  }
}
```

**Response** (200 OK):
```json
{
  "document_id": "doc-123",
  "graph_version": "doc-123:2024-01-01T12:00:00",
  "version_id": "doc-123:v1",
  "status": "processed"
}
```

**Status Codes**:
- `200 OK`: Document processed successfully
- `400 Bad Request`: Invalid input
- `500 Internal Server Error`: Processing failed

**Example**:
```bash
curl -X POST "http://localhost:8000/documents" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <api_key>" \
  -d '{
    "document_id": "doc-1",
    "content": "Artificial Intelligence is transforming industries...",
    "metadata": {
      "source": "internal",
      "author": "AI.me Team"
    }
  }'
```

---

### Query Graph

#### POST /query

Query the graph and get a grounded response.

**Request Body**:
```json
{
  "query": "string (required, 1-1000 chars)",
  "graph_id": "string (optional)",
  "filters": {
    "source": "string",
    "valid_until": "ISO 8601 datetime",
    "min_groundedness": 0.7
  }
}
```

**Response** (200 OK):
```json
{
  "answer": "string",
  "model": "anthropic.claude-v2",
  "validation": {
    "is_valid": true,
    "groundedness_score": 0.85,
    "issues": [],
    "warnings": []
  },
  "subgraph_size": 42,
  "query_event_id": "event_1234567890"
}
```

**Status Codes**:
- `200 OK`: Query processed successfully
- `400 Bad Request`: Invalid query
- `503 Service Unavailable`: Service temporarily unavailable
- `500 Internal Server Error`: Processing failed

**Example**:
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <api_key>" \
  -d '{
    "query": "What is artificial intelligence?",
    "filters": {
      "min_groundedness": 0.7
    }
  }'
```

---

### Audit Trail

#### GET /audit/{session_id}

Get audit trace for a session.

**Path Parameters**:
- `session_id` (string, required): Session identifier

**Response** (200 OK):
```json
{
  "session_id": "session-123",
  "events": [
    {
      "event_id": "event_1234567890",
      "event_type": "llm_query",
      "timestamp": "2024-01-01T12:00:00Z",
      "user_id": "user-123",
      "details": {
        "query": "What is AI?",
        "graph_id": "graph-123"
      }
    },
    {
      "event_id": "event_1234567891",
      "event_type": "llm_response",
      "timestamp": "2024-01-01T12:00:01Z",
      "user_id": "user-123",
      "details": {
        "query_event_id": "event_1234567890",
        "response_length": 150,
        "model": "anthropic.claude-v2"
      }
    }
  ]
}
```

**Status Codes**:
- `200 OK`: Audit trace retrieved
- `404 Not Found`: Session not found
- `500 Internal Server Error`: Retrieval failed

**Example**:
```bash
curl -X GET "http://localhost:8000/audit/session-123" \
  -H "Authorization: Bearer <api_key>"
```

---

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Status Codes

- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Service temporarily unavailable

## Rate Limiting

Rate limits (to be implemented):
- 100 requests per minute per API key
- 1000 requests per hour per API key
- Burst: 10 requests per second

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1609459200
```

## Pagination

For endpoints returning lists (future):

```
GET /documents?page=1&page_size=20
```

Response includes pagination metadata:
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

## OpenAPI/Swagger

Interactive API documentation is available at:
- Development: `http://localhost:8000/docs`
- Swagger JSON: `http://localhost:8000/openapi.json`

## SDKs and Libraries

Official SDKs (planned):
- Python SDK
- JavaScript/TypeScript SDK
- Go SDK

## Versioning

API versioning:
- Current version: `v1`
- Version specified in URL: `/v1/...`
- Deprecation notices in response headers

## Webhooks

Webhook support (planned):
- Document processing complete
- Query response ready
- Error notifications

## References

- Product Specification: `docs/product/PRODUCT_SPEC.md`
- Integration Guide: `docs/product/INTEGRATION_GUIDE.md`
- Architecture: `docs/architecture/SYSTEM_ARCHITECTURE.md`

