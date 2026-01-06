#!/bin/bash

# Test runner script

set -e

echo "🧪 Running tests..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run tests with coverage
pytest tests/ -v --cov=src --cov-report=html --cov-report=term

echo "✅ Tests complete!"
echo "📊 Coverage report available in htmlcov/index.html"

