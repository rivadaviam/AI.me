# AI Agent Testing Workflow

This document defines the testing strategy and workflow for AI agents to ensure comprehensive test coverage and quality.

## Testing Philosophy

- **Test-Driven Development**: Write tests before implementation when possible
- **Comprehensive Coverage**: Aim for >80% code coverage
- **Fast Feedback**: Tests should run quickly
- **Reliability**: Tests should be deterministic and not flaky
- **Maintainability**: Tests should be easy to understand and update

## Test Strategy

### Test Pyramid

```
        /\
       /  \      E2E Tests (Few)
      /____\
     /      \    Integration Tests (Some)
    /________\
   /          \   Unit Tests (Many)
  /____________\
```

### Test Types

#### 1. Unit Tests

**Purpose**: Test individual functions and classes in isolation

**Location**: `tests/unit/` or `tests/test_<module>.py`

**Coverage**: 
- All public functions
- Edge cases
- Error conditions
- Boundary conditions

**Example**:
```python
def test_graph_processor_processes_document():
    processor = GraphProcessor()
    result = processor.process_document(
        document_id="test-1",
        content="Test content"
    )
    assert result is not None
    assert "test-1" in result
```

#### 2. Integration Tests

**Purpose**: Test component interactions

**Location**: `tests/integration/`

**Coverage**:
- Component interactions
- Service integrations
- Database operations
- External API calls (mocked)

**Example**:
```python
def test_graph_service_end_to_end():
    service = create_test_service()
    result = service.process_document(...)
    query_result = service.query(...)
    assert query_result["answer"] is not None
```

#### 3. End-to-End Tests

**Purpose**: Test complete user workflows

**Location**: `tests/e2e/`

**Coverage**:
- Complete user journeys
- API workflows
- Error recovery

**Example**:
```python
def test_document_to_query_workflow():
    # Process document
    response = client.post("/documents", json={...})
    # Query graph
    query_response = client.post("/query", json={...})
    assert query_response.status_code == 200
```

## Test Requirements

### Coverage Requirements

- **Minimum**: 80% overall coverage
- **Critical paths**: 100% coverage
- **New code**: 100% coverage required

### Test Data Management

#### Fixtures

Use pytest fixtures for common test data:

```python
@pytest.fixture
def sample_document():
    return {
        "document_id": "test-doc-1",
        "content": "Test content",
        "metadata": {"source": "test"}
    }
```

#### Test Databases

- Use in-memory databases for unit tests
- Use test database instances for integration tests
- Clean up after each test

#### Mocking

Mock external dependencies:

```python
@patch('src.integrations.aws.bedrock_client.BedrockClient')
def test_with_mocked_bedrock(mock_bedrock):
    mock_bedrock.return_value.invoke_model.return_value = {...}
    # Test code
```

### Test Organization

```
tests/
├── unit/
│   ├── test_graph_processor.py
│   ├── test_reasoning_engine.py
│   └── ...
├── integration/
│   ├── test_graph_service.py
│   ├── test_api_endpoints.py
│   └── ...
├── e2e/
│   ├── test_document_workflow.py
│   └── ...
├── fixtures/
│   ├── conftest.py
│   └── test_data.py
└── helpers/
    └── test_utils.py
```

## Testing Workflow

### 1. Before Implementation

- Write test cases for the feature
- Define expected behavior
- Identify edge cases
- Plan test data requirements

### 2. During Development

- Run tests frequently
- Fix failing tests immediately
- Add tests for bugs found
- Keep tests passing

### 3. Before Commit

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test category
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/

# Run with verbose output
pytest -v

# Run with output capture disabled
pytest -s
```

### 4. CI/CD Integration

Tests run automatically on:
- Pull request creation
- Push to main branch
- Scheduled nightly runs

## Test Guidelines

### Naming Conventions

- Test files: `test_<module_name>.py`
- Test functions: `test_<functionality>_<expected_behavior>`
- Test classes: `Test<ComponentName>`

### Test Structure

Follow AAA pattern:

```python
def test_feature_should_work():
    # Arrange - Set up test data and dependencies
    processor = GraphProcessor()
    document = create_test_document()
    
    # Act - Execute the functionality
    result = processor.process_document(...)
    
    # Assert - Verify the results
    assert result is not None
    assert result["status"] == "processed"
```

### Best Practices

1. **Isolation**: Each test should be independent
2. **Deterministic**: Tests should produce same results every time
3. **Fast**: Unit tests should run in milliseconds
4. **Clear**: Test names should describe what they test
5. **Focused**: One assertion per test concept

### Anti-Patterns to Avoid

- ❌ Testing implementation details
- ❌ Shared mutable state between tests
- ❌ Tests that depend on execution order
- ❌ Slow tests in unit test suite
- ❌ Tests without assertions

## Test Data

### Creating Test Data

```python
# Use factories for complex objects
def create_test_graph():
    graph = nx.MultiDiGraph()
    graph.add_node("node1", data="test")
    return graph

# Use fixtures for reusable data
@pytest.fixture
def test_graph():
    return create_test_graph()
```

### Test Data Cleanup

```python
@pytest.fixture(autouse=True)
def cleanup():
    yield
    # Cleanup code runs after test
    cleanup_test_data()
```

## Performance Testing

### Load Testing

Test system under load:

```python
def test_api_handles_concurrent_requests():
    # Test concurrent requests
    results = asyncio.gather(*[
        client.post("/query", json={...})
        for _ in range(100)
    ])
    assert all(r.status_code == 200 for r in results)
```

### Benchmarking

Track performance over time:

```python
def test_processing_performance(benchmark):
    result = benchmark(processor.process_document, ...)
    assert result is not None
```

## Test Reporting

### Coverage Reports

Generate HTML coverage report:

```bash
pytest --cov=src --cov-report=html
# Open htmlcov/index.html
```

### Test Results

View test results:
- Console output for quick feedback
- JUnit XML for CI/CD integration
- HTML reports for detailed analysis

## Continuous Integration

### GitHub Actions

Tests run automatically on:
- Every pull request
- Every push to main
- Scheduled runs

### Test Environment

- Isolated test environment
- Test database
- Mocked external services
- Clean state for each run

## Troubleshooting

### Flaky Tests

If tests are flaky:
1. Check for race conditions
2. Verify test isolation
3. Check for timing dependencies
4. Review shared state

### Slow Tests

To speed up tests:
1. Use fixtures efficiently
2. Mock slow operations
3. Run tests in parallel
4. Optimize test data setup

### Debugging Tests

```bash
# Run with debugger
pytest --pdb

# Run with verbose output
pytest -vv

# Run specific test
pytest tests/test_specific.py::test_function
```

## Resources

- Testing Guide: `docs/development/TESTING_GUIDE.md`
- Test Examples: `tests/`
- CI Configuration: `.github/workflows/ci.yml`

