# Testing Guide

## Overview

Comprehensive guide for writing and running tests.

## Test Structure

### Unit Tests

Location: `tests/unit/` or `tests/test_<module>.py`

```python
def test_graph_processor_processes_document():
    processor = GraphProcessor()
    result = processor.process_document("doc-1", "content")
    assert result is not None
```

### Integration Tests

Location: `tests/integration/`

```python
def test_graph_service_end_to_end():
    service = create_test_service()
    result = service.process_document(...)
    assert result["status"] == "processed"
```

## Running Tests

```bash
# All tests
pytest

# Specific file
pytest tests/test_graph_processor.py

# With coverage
pytest --cov=src --cov-report=html
```

## Test Fixtures

Use pytest fixtures for common setup:

```python
@pytest.fixture
def graph_processor():
    return GraphProcessor()
```

## Best Practices

1. Test one thing per test
2. Use descriptive test names
3. Keep tests independent
4. Use fixtures for setup
5. Mock external dependencies

## References

- Testing Workflow: `docs/workflows/testing.md`

