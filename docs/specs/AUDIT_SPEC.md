# Audit Trail Specification

## Overview

Specification for audit logging and traceability.

## Event Structure

### Required Fields

- `event_id`: Unique identifier
- `event_type`: Event type enum
- `timestamp`: ISO 8601 timestamp
- `details`: Event-specific details

### Optional Fields

- `user_id`: User identifier
- `session_id`: Session identifier
- `ip_address`: Client IP
- `user_agent`: Client user agent

## Event Types

### Graph Events
- `GRAPH_CREATED`: Graph created
- `GRAPH_UPDATED`: Graph updated
- `GRAPH_VERSIONED`: Graph versioned

### Query Events
- `LLM_QUERY`: Query received
- `LLM_RESPONSE`: Response generated
- `SUBGRAPH_EXTRACTED`: Subgraph extracted
- `SUBGRAPH_VALIDATED`: Subgraph validated

### System Events
- `REASONING_EXECUTED`: Reasoning executed
- `ERROR`: Error occurred

## Storage

### Database Schema

```sql
CREATE TABLE audit_events (
    event_id VARCHAR(255) PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    user_id VARCHAR(255),
    session_id VARCHAR(255),
    details JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_audit_session ON audit_events(session_id);
CREATE INDEX idx_audit_timestamp ON audit_events(timestamp);
CREATE INDEX idx_audit_user ON audit_events(user_id);
```

## Retention

- Active events: 90 days
- Archived events: 7 years (compliance)
- Deleted events: After retention period

## References

- Component Specs: `docs/architecture/COMPONENT_SPECS.md`
- Security Spec: `docs/specs/SECURITY_SPEC.md`

