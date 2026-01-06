# Contributing to NXO

Thank you for your interest in contributing to NXO! This document provides guidelines and instructions for contributing.

## Development Setup

1. **Fork and Clone**
   ```bash
   git clone <your-fork-url>
   cd nxo
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   make install-dev
   ```

4. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

## Development Workflow

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write code following the existing style
   - Add tests for new functionality
   - Update documentation as needed

3. **Run Tests**
   ```bash
   make test
   ```

4. **Check Code Quality**
   ```bash
   make lint
   make format
   ```

5. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

   Use conventional commit messages:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation
   - `test:` for tests
   - `refactor:` for refactoring
   - `chore:` for maintenance

6. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for all public functions/classes
- Maximum line length: 100 characters
- Use `black` for formatting
- Use `ruff` for linting

## Testing

- Write tests for all new functionality
- Aim for >80% code coverage
- Use `pytest` for testing
- Use `pytest-asyncio` for async tests

## Documentation

- Update README.md for user-facing changes
- Update ARCHITECTURE.md for architectural changes
- Add docstrings to all public APIs
- Include examples in docstrings

## Pull Request Process

1. Ensure all tests pass
2. Ensure code passes linting
3. Update documentation
4. Add a clear description of changes
5. Reference any related issues

## Questions?

If you have questions, please contact the development team or open an issue.

