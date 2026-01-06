#!/bin/bash

# AI Agent Code Review Workflow Automation Script
# This script automates the code review process for AI agents

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"

echo "🔍 Starting AI Agent Code Review Workflow"
echo "========================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

REVIEW_REPORT="review-report-$(date +%Y%m%d-%H%M%S).json"

# Initialize review report
cat > "$REVIEW_REPORT" <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "checks": {}
}
EOF

source venv/bin/activate 2>/dev/null || {
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
}

# Function to add check result to report
add_check_result() {
    local check_name=$1
    local status=$2
    local details=$3
    
    python3 <<EOF
import json
import sys

with open("$REVIEW_REPORT", "r") as f:
    report = json.load(f)

report["checks"]["$check_name"] = {
    "status": "$status",
    "details": "$details"
}

with open("$REVIEW_REPORT", "w") as f:
    json.dump(report, f, indent=2)
EOF
}

# Code Quality Checks
echo -e "\n${BLUE}Code Quality Checks${NC}"
echo "-------------------"

echo -n "Checking code formatting... "
if black --check src/ tests/ &>/dev/null; then
    echo -e "${GREEN}✓${NC}"
    add_check_result "code_formatting" "pass" "Code is properly formatted"
else
    echo -e "${RED}✗${NC}"
    add_check_result "code_formatting" "fail" "Code needs formatting (run: black src/ tests/)"
fi

echo -n "Checking code style... "
if ruff check src/ tests/ &>/dev/null; then
    echo -e "${GREEN}✓${NC}"
    add_check_result "code_style" "pass" "No style violations found"
else
    echo -e "${YELLOW}⚠${NC}"
    ruff check src/ tests/ 2>&1 | head -5
    add_check_result "code_style" "warning" "Style violations found"
fi

echo -n "Type checking... "
if mypy src/ &>/dev/null; then
    echo -e "${GREEN}✓${NC}"
    add_check_result "type_checking" "pass" "Type checking passed"
else
    echo -e "${YELLOW}⚠${NC}"
    add_check_result "type_checking" "warning" "Type checking issues found"
fi

# Security Checks
echo -e "\n${BLUE}Security Checks${NC}"
echo "---------------"

if command -v bandit &> /dev/null; then
    echo -n "Running security scan... "
    if bandit -r src/ -ll &>/dev/null; then
        echo -e "${GREEN}✓${NC}"
        add_check_result "security_scan" "pass" "No security issues found"
    else
        echo -e "${YELLOW}⚠${NC}"
        bandit -r src/ -ll 2>&1 | head -10
        add_check_result "security_scan" "warning" "Security issues found (review output)"
    fi
else
    echo -e "${YELLOW}Bandit not installed. Skipping security check.${NC}"
    add_check_result "security_scan" "skipped" "Bandit not installed"
fi

# Test Coverage
echo -e "\n${BLUE}Test Coverage${NC}"
echo "-------------"

echo -n "Running tests with coverage... "
COVERAGE_OUTPUT=$(pytest --cov=src --cov-report=term-missing -q 2>&1 || true)
COVERAGE_PERCENT=$(echo "$COVERAGE_OUTPUT" | grep "TOTAL" | awk '{print $NF}' | sed 's/%//' || echo "0")

if [ -n "$COVERAGE_PERCENT" ] && [ "$COVERAGE_PERCENT" != "0" ]; then
    if (( $(echo "$COVERAGE_PERCENT >= 80" | bc -l) )); then
        echo -e "${GREEN}✓${NC} (${COVERAGE_PERCENT}%)"
        add_check_result "test_coverage" "pass" "Coverage: ${COVERAGE_PERCENT}%"
    else
        echo -e "${YELLOW}⚠${NC} (${COVERAGE_PERCENT}% - target: 80%)"
        add_check_result "test_coverage" "warning" "Coverage below target: ${COVERAGE_PERCENT}%"
    fi
else
    echo -e "${RED}✗${NC}"
    add_check_result "test_coverage" "fail" "Could not determine coverage"
fi

# Documentation Checks
echo -e "\n${BLUE}Documentation Checks${NC}"
echo "-------------------"

echo -n "Checking docstrings... "
if command -v pydocstyle &> /dev/null; then
    if pydocstyle src/ --convention=google &>/dev/null; then
        echo -e "${GREEN}✓${NC}"
        add_check_result "docstrings" "pass" "Docstrings are properly formatted"
    else
        echo -e "${YELLOW}⚠${NC}"
        add_check_result "docstrings" "warning" "Some docstrings need improvement"
    fi
else
    echo -e "${YELLOW}pydocstyle not installed. Skipping.${NC}"
    add_check_result "docstrings" "skipped" "pydocstyle not installed"
fi

# Generate Summary
echo -e "\n${BLUE}Review Summary${NC}"
echo "--------------"

python3 <<EOF
import json

with open("$REVIEW_REPORT", "r") as f:
    report = json.load(f)

passed = sum(1 for check in report["checks"].values() if check["status"] == "pass")
warnings = sum(1 for check in report["checks"].values() if check["status"] == "warning")
failed = sum(1 for check in report["checks"].values() if check["status"] == "fail")

print(f"Passed: {passed}")
print(f"Warnings: {warnings}")
print(f"Failed: {failed}")
print(f"\nFull report: $REVIEW_REPORT")
EOF

echo -e "\n${GREEN}Review workflow complete!${NC}"
echo "Review report saved to: $REVIEW_REPORT"

