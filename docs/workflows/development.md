# AI Agent Development Workflow

This document provides a step-by-step guide for AI agents to develop new features for the AI.me platform.

## Overview

The development workflow ensures consistent, high-quality code that follows project standards and integrates seamlessly with existing components.

## Workflow Steps

### 1. Understand Requirements

Before starting development:

- Read the feature specification or issue description
- Review related documentation in `docs/product/` and `docs/architecture/`
- Understand the business context from `docs/business/`
- Check existing similar implementations for patterns

### 2. Plan Implementation

- Identify affected components
- Review component specifications in `docs/architecture/COMPONENT_SPECS.md`
- Plan data flow changes (see `docs/architecture/DATA_FLOW.md`)
- Consider integration points (see `docs/product/INTEGRATION_GUIDE.md`)
- Identify test requirements

### 3. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation updates

### 4. Development Guidelines

#### Code Structure

Follow the existing project structure:
```
src/
├── core/          # Core business logic
├── integrations/  # External service integrations
├── services/      # Service layer orchestration
├── api/           # API endpoints
└── utils/         # Utility functions
```

#### Code Standards

- Follow Python PEP 8 style guide
- Use type hints for all function signatures
- Write docstrings for all classes and functions
- Keep functions focused and single-purpose
- Maximum function length: 50 lines
- Maximum class length: 300 lines

#### Integration Patterns

When integrating with existing components:

1. **Graph Processing**: Use `GraphProcessor` from `src/core/graph/processor.py`
2. **Reasoning**: Use `ReasoningEngine` from `src/core/reasoning/engine.py`
3. **Versioning**: Use `VersionManager` from `src/core/versioning/manager.py`
4. **Audit**: Use `AuditLogger` from `src/core/audit/logger.py`
5. **LLM Services**: Use `LLMServiceFactory` from `src/integrations/llm/service.py`

#### Error Handling

- Use specific exception types
- Log errors with context
- Return meaningful error messages
- Follow existing error handling patterns

### 5. Write Tests

Before writing implementation code:

1. Write unit tests in `tests/`
2. Follow naming: `test_<module>_<functionality>.py`
3. Aim for >80% code coverage
4. Test both success and failure cases
5. Use fixtures for common test data

Test structure:
```python
def test_feature_should_do_something():
    # Arrange
    # Act
    # Assert
```

### 6. Implement Feature

- Write clean, readable code
- Add logging at appropriate levels
- Follow existing patterns
- Ensure backward compatibility
- Update related documentation

### 7. Run Tests Locally

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_your_feature.py -v

# Run with coverage
pytest --cov=src --cov-report=html
```

### 8. Code Quality Checks

```bash
# Format code
make format

# Lint code
make lint

# Type checking
mypy src/
```

### 9. Update Documentation

Update relevant documentation:

- API documentation if endpoints changed
- Architecture docs if components changed
- Integration guide if integration patterns changed
- Update `docs/agents/data/` JSON files if needed

### 10. Commit Changes

Commit message format:
```
<type>: <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Maintenance

Example:
```
feat: Add entity extraction to graph processor

- Implement NLP-based entity extraction using spaCy
- Add entity relationship detection
- Update graph processor to include entities

Closes #123
```

### 11. Create Pull Request

PR requirements:

- Clear title and description
- Link to related issues
- List of changes
- Test results
- Screenshots/diagrams if applicable
- Reviewers assigned

### 12. Address Review Feedback

- Respond to all comments
- Make requested changes
- Update tests if needed
- Re-run all checks

## Development Checklist

- [ ] Requirements understood
- [ ] Implementation planned
- [ ] Feature branch created
- [ ] Tests written
- [ ] Code implemented
- [ ] Tests passing
- [ ] Code formatted and linted
- [ ] Documentation updated
- [ ] Changes committed
- [ ] PR created
- [ ] Review feedback addressed

## Common Patterns

### Adding a New API Endpoint

1. Define request/response models in `src/api/main.py`
2. Create endpoint function
3. Add service method in `src/services/`
4. Update API documentation
5. Add tests

### Adding a New Integration

1. Create client in `src/integrations/`
2. Add configuration in `src/utils/config.py`
3. Update `.env.example`
4. Add integration tests
5. Update integration guide

### Modifying Core Components

1. Review component spec in `docs/architecture/COMPONENT_SPECS.md`
2. Understand current implementation
3. Plan backward-compatible changes
4. Update component documentation
5. Add migration guide if breaking changes

## Resources

- Coding Standards: `docs/development/CODING_STANDARDS.md`
- Testing Guide: `docs/development/TESTING_GUIDE.md`
- Architecture: `docs/architecture/`
- API Spec: `docs/product/API_SPEC.md`

