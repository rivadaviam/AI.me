# LLM Integration Specification

## Overview

Specification for LLM service integration patterns.

## Integration Pattern

### Context Injection

1. Convert subgraph to context format
2. Format context as text
3. Inject into system prompt
4. Send to LLM

### Response Formatting

1. Parse LLM response
2. Extract answer text
3. Extract metadata
4. Format response

## Supported Providers

### AWS Bedrock

- Models: Claude, Titan
- Authentication: AWS IAM
- Configuration: Via environment variables

### OpenAI (Planned)

- Models: GPT-4, GPT-3.5
- Authentication: API key
- Configuration: Via environment variables

## Context Format

### Structure

```
Context:
- Entity 1: [description]
- Entity 2: [description]
- Relationship: Entity 1 → Entity 2

User: [query]
```

## Error Handling

- Retry on transient failures
- Fallback to alternative models
- Graceful degradation

## References

- API Spec: `docs/product/API_SPEC.md`
- Integration Guide: `docs/product/INTEGRATION_GUIDE.md`

