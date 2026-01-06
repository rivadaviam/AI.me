# Coding Standards

## Python Style Guide

Follow PEP 8 with project-specific modifications.

## Code Formatting

### Black Configuration

- Line length: 100 characters
- Target version: Python 3.11+

### Import Organization

1. Standard library imports
2. Third-party imports
3. Local application imports

## Naming Conventions

### Variables and Functions
- Use `snake_case`
- Be descriptive
- Avoid abbreviations

### Classes
- Use `PascalCase`
- Be descriptive

### Constants
- Use `UPPER_SNAKE_CASE`

## Type Hints

Always use type hints:

```python
def process_document(
    document_id: str,
    content: str,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    ...
```

## Docstrings

Use Google-style docstrings:

```python
def process_document(document_id: str, content: str) -> str:
    """
    Process a document into a semantic graph.

    Args:
        document_id: Unique identifier for the document
        content: Document content to process

    Returns:
        Graph version identifier
    """
```

## Error Handling

- Use specific exception types
- Log errors with context
- Return meaningful error messages

## Testing

- Write tests for all public functions
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)

## References

- Testing Guide: `docs/development/TESTING_GUIDE.md`
- Contributing: `docs/development/CONTRIBUTING.md`

