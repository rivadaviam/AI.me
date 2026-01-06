#!/bin/bash

# AI Agent Development Workflow Automation Script
# This script automates the development workflow for AI agents

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"

echo "🚀 Starting AI Agent Development Workflow"
echo "=========================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Check prerequisites
echo -e "\n${YELLOW}Step 1: Checking prerequisites...${NC}"
if [ ! -d "venv" ]; then
    echo -e "${RED}Virtual environment not found. Creating...${NC}"
    python3 -m venv venv
fi

source venv/bin/activate

if ! command -v pytest &> /dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Step 2: Run code quality checks
echo -e "\n${YELLOW}Step 2: Running code quality checks...${NC}"
echo "Formatting code..."
black --check src/ tests/ || {
    echo -e "${YELLOW}Code needs formatting. Running black...${NC}"
    black src/ tests/
}

echo "Linting code..."
ruff check src/ tests/ || {
    echo -e "${YELLOW}Linting issues found. Attempting auto-fix...${NC}"
    ruff check --fix src/ tests/
}

echo "Type checking..."
mypy src/ || echo -e "${YELLOW}Type checking issues found (non-blocking)${NC}"

# Step 3: Run tests
echo -e "\n${YELLOW}Step 3: Running tests...${NC}"
pytest tests/ -v --cov=src --cov-report=term-missing || {
    echo -e "${RED}Tests failed!${NC}"
    exit 1
}

# Step 4: Security check
echo -e "\n${YELLOW}Step 4: Running security checks...${NC}"
if command -v bandit &> /dev/null; then
    bandit -r src/ -f json -o security-report.json || echo -e "${YELLOW}Security issues found (review security-report.json)${NC}"
else
    echo "Bandit not installed. Skipping security check."
    echo "Install with: pip install bandit"
fi

# Step 5: Generate coverage report
echo -e "\n${YELLOW}Step 5: Generating coverage report...${NC}"
pytest --cov=src --cov-report=html
echo -e "${GREEN}Coverage report generated: htmlcov/index.html${NC}"

# Step 6: Check documentation
echo -e "\n${YELLOW}Step 6: Checking documentation...${NC}"
if [ -f "docs/tools/validate_docs.sh" ]; then
    bash docs/tools/validate_docs.sh || echo -e "${YELLOW}Documentation validation issues found${NC}"
fi

# Summary
echo -e "\n${GREEN}=========================================="
echo "Development Workflow Complete!"
echo "==========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Review test coverage: htmlcov/index.html"
echo "2. Review security report: security-report.json (if generated)"
echo "3. Commit your changes"
echo "4. Create a pull request"

