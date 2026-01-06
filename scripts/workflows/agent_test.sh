#!/bin/bash

# AI Agent Testing Workflow Automation Script
# This script automates the testing workflow for AI agents

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"

echo "🧪 Starting AI Agent Testing Workflow"
echo "======================================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

source venv/bin/activate 2>/dev/null || {
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
}

TEST_REPORT_DIR="test-reports"
mkdir -p "$TEST_REPORT_DIR"

TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Function to run tests with category
run_test_category() {
    local category=$1
    local test_path=$2
    local report_file="$TEST_REPORT_DIR/${category}-${TIMESTAMP}.xml"
    
    echo -e "\n${BLUE}Running $category tests...${NC}"
    
    if [ -d "$test_path" ] || [ -f "$test_path" ]; then
        pytest "$test_path" \
            -v \
            --junitxml="$report_file" \
            --cov=src \
            --cov-report=term-missing \
            --cov-report=html:"$TEST_REPORT_DIR/${category}-coverage" || {
            echo -e "${RED}$category tests failed!${NC}"
            return 1
        }
        echo -e "${GREEN}✓ $category tests passed${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠ No $category tests found at $test_path${NC}"
        return 0
    fi
}

# Run unit tests
run_test_category "unit" "tests/unit" || UNIT_FAILED=1
run_test_category "unit" "tests/test_*.py" || UNIT_FAILED=1

# Run integration tests
run_test_category "integration" "tests/integration" || INTEGRATION_FAILED=1

# Run E2E tests
run_test_category "e2e" "tests/e2e" || E2E_FAILED=1

# Generate overall coverage report
echo -e "\n${BLUE}Generating overall coverage report...${NC}"
pytest --cov=src --cov-report=html:"$TEST_REPORT_DIR/coverage" --cov-report=term

# Check coverage threshold
COVERAGE_THRESHOLD=80
COVERAGE_PERCENT=$(pytest --cov=src --cov-report=term -q 2>&1 | grep "TOTAL" | awk '{print $NF}' | sed 's/%//' || echo "0")

if [ -n "$COVERAGE_PERCENT" ] && [ "$COVERAGE_PERCENT" != "0" ]; then
    if (( $(echo "$COVERAGE_PERCENT >= $COVERAGE_THRESHOLD" | bc -l 2>/dev/null || echo "0") )); then
        echo -e "${GREEN}✓ Coverage: ${COVERAGE_PERCENT}% (target: ${COVERAGE_THRESHOLD}%)${NC}"
    else
        echo -e "${YELLOW}⚠ Coverage: ${COVERAGE_PERCENT}% (target: ${COVERAGE_THRESHOLD}%)${NC}"
    fi
fi

# Summary
echo -e "\n${BLUE}Test Summary${NC}"
echo "------------"

if [ -z "$UNIT_FAILED" ] && [ -z "$INTEGRATION_FAILED" ] && [ -z "$E2E_FAILED" ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo ""
    echo "Test reports:"
    echo "  - Unit tests: $TEST_REPORT_DIR/unit-${TIMESTAMP}.xml"
    echo "  - Integration tests: $TEST_REPORT_DIR/integration-${TIMESTAMP}.xml"
    echo "  - E2E tests: $TEST_REPORT_DIR/e2e-${TIMESTAMP}.xml"
    echo "  - Coverage report: $TEST_REPORT_DIR/coverage/index.html"
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    [ -n "$UNIT_FAILED" ] && echo "  - Unit tests failed"
    [ -n "$INTEGRATION_FAILED" ] && echo "  - Integration tests failed"
    [ -n "$E2E_FAILED" ] && echo "  - E2E tests failed"
    exit 1
fi

