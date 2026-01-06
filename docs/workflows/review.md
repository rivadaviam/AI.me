# AI Agent Code Review Workflow

This document defines the automated code review process for AI agents to ensure code quality, security, and maintainability.

## Review Objectives

1. **Code Quality**: Ensure code follows standards and best practices
2. **Security**: Identify security vulnerabilities and risks
3. **Performance**: Check for performance issues and optimizations
4. **Documentation**: Verify adequate documentation exists
5. **Testing**: Ensure proper test coverage and quality

## Automated Review Checklist

### Code Quality

#### Structure and Organization
- [ ] Code follows project structure conventions
- [ ] Files are appropriately sized (<500 lines)
- [ ] Functions are focused and single-purpose
- [ ] Classes follow single responsibility principle
- [ ] No code duplication (DRY principle)

#### Style and Formatting
- [ ] Code follows PEP 8 style guide
- [ ] Type hints are used for all functions
- [ ] Docstrings are present for all public functions/classes
- [ ] Code is properly formatted (black, ruff)
- [ ] No unused imports or variables

#### Python Best Practices
- [ ] Proper use of context managers
- [ ] Exception handling is appropriate
- [ ] No hardcoded values (use constants/config)
- [ ] Proper use of async/await where applicable
- [ ] No blocking I/O in async functions

### Security

#### Input Validation
- [ ] All user inputs are validated
- [ ] SQL injection prevention (if applicable)
- [ ] XSS prevention (if applicable)
- [ ] Path traversal prevention
- [ ] Input sanitization where needed

#### Authentication & Authorization
- [ ] Authentication checks are in place
- [ ] Authorization is properly implemented
- [ ] No hardcoded credentials
- [ ] Secrets are not committed
- [ ] API keys are properly managed

#### Data Security
- [ ] Sensitive data is encrypted
- [ ] PII handling follows compliance requirements
- [ ] Audit logging for sensitive operations
- [ ] Proper error messages (no info leakage)

### Performance

#### Efficiency
- [ ] No N+1 query problems
- [ ] Proper use of caching where applicable
- [ ] Efficient algorithms and data structures
- [ ] No unnecessary database calls
- [ ] Proper pagination for large datasets

#### Resource Management
- [ ] Proper connection pooling
- [ ] Memory leaks prevented
- [ ] File handles properly closed
- [ ] Background tasks properly managed

### Documentation

#### Code Documentation
- [ ] All public functions have docstrings
- [ ] Complex logic has inline comments
- [ ] Type hints are complete
- [ ] Examples provided for complex functions

#### API Documentation
- [ ] API endpoints documented
- [ ] Request/response schemas documented
- [ ] Error responses documented
- [ ] Authentication requirements documented

### Testing

#### Test Coverage
- [ ] Unit tests for all new functions
- [ ] Integration tests for new features
- [ ] Edge cases are tested
- [ ] Error cases are tested
- [ ] Test coverage >80%

#### Test Quality
- [ ] Tests are independent
- [ ] Tests use appropriate fixtures
- [ ] Tests are readable and maintainable
- [ ] No flaky tests
- [ ] Tests follow naming conventions

## Review Process

### 1. Automated Checks

Run automated review tools:

```bash
# Code formatting
black --check src/ tests/

# Linting
ruff check src/ tests/

# Type checking
mypy src/

# Security scanning
bandit -r src/

# Test coverage
pytest --cov=src --cov-report=term-missing
```

### 2. Manual Review Points

Even with automation, check:

- Business logic correctness
- Edge cases handling
- Error messages clarity
- User experience impact
- Performance implications

### 3. Review Output

Generate review report:

```bash
./scripts/workflows/agent_review.sh
```

This generates:
- Code quality score
- Security issues list
- Performance concerns
- Documentation gaps
- Test coverage report

## Review Criteria

### Must Fix (Blocking)

- Security vulnerabilities
- Breaking changes without migration
- Test failures
- Code that doesn't compile
- Critical performance issues

### Should Fix (Non-blocking)

- Code style violations
- Missing documentation
- Low test coverage
- Performance optimizations
- Code duplication

### Nice to Have

- Additional test cases
- Documentation improvements
- Code refactoring suggestions
- Performance enhancements

## Review Comments Format

When leaving review comments:

```
[Category]: [Issue]

Description of the issue.

Suggested fix:
```python
# Example code
```

Reference: [link to standard/guideline]
```

Categories:
- `SECURITY`: Security issues
- `PERFORMANCE`: Performance concerns
- `QUALITY`: Code quality issues
- `DOCS`: Documentation issues
- `TEST`: Testing issues
- `STYLE`: Style violations

## Approval Criteria

A PR can be approved when:

1. All automated checks pass
2. No blocking issues remain
3. All reviewers approve
4. Tests are passing
5. Documentation is updated
6. Security review passed (if applicable)

## Review Tools

### Static Analysis
- `ruff`: Fast Python linter
- `mypy`: Static type checker
- `bandit`: Security linter
- `black`: Code formatter

### Testing
- `pytest`: Test framework
- `pytest-cov`: Coverage reporting
- `pytest-asyncio`: Async test support

### Documentation
- `pydocstyle`: Docstring style checker
- OpenAPI/Swagger: API documentation

## Common Issues and Solutions

### Issue: Missing Type Hints
**Solution**: Add type hints to all function signatures

### Issue: Security Vulnerability
**Solution**: Review security checklist and fix identified issues

### Issue: Low Test Coverage
**Solution**: Add tests for uncovered code paths

### Issue: Performance Problem
**Solution**: Profile code and optimize bottlenecks

### Issue: Documentation Missing
**Solution**: Add docstrings and update relevant docs

## Resources

- Security Guidelines: `docs/specs/SECURITY_SPEC.md`
- Coding Standards: `docs/development/CODING_STANDARDS.md`
- Testing Guide: `docs/development/TESTING_GUIDE.md`

