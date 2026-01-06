#!/bin/bash

# AI Agent Full Development Cycle Workflow
# This script runs the complete development cycle: dev -> review -> test

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"

echo "🔄 Starting AI Agent Full Development Cycle"
echo "==========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step 1: Development workflow
echo -e "${BLUE}Step 1: Development Workflow${NC}"
echo "================================"
if bash "$SCRIPT_DIR/agent_dev.sh"; then
    echo -e "${GREEN}✓ Development workflow passed${NC}"
else
    echo -e "${RED}✗ Development workflow failed${NC}"
    exit 1
fi

echo ""
echo ""

# Step 2: Code review
echo -e "${BLUE}Step 2: Code Review${NC}"
echo "=================="
if bash "$SCRIPT_DIR/agent_review.sh"; then
    echo -e "${GREEN}✓ Code review passed${NC}"
else
    echo -e "${YELLOW}⚠ Code review completed with warnings${NC}"
fi

echo ""
echo ""

# Step 3: Testing
echo -e "${BLUE}Step 3: Testing${NC}"
echo "============="
if bash "$SCRIPT_DIR/agent_test.sh"; then
    echo -e "${GREEN}✓ Testing passed${NC}"
else
    echo -e "${RED}✗ Testing failed${NC}"
    exit 1
fi

echo ""
echo ""

# Final summary
echo -e "${GREEN}==========================================="
echo "Full Development Cycle Complete!"
echo "===========================================${NC}"
echo ""
echo "All workflows completed successfully."
echo ""
echo "Next steps:"
echo "1. Review test coverage reports"
echo "2. Review code review report"
echo "3. Commit your changes"
echo "4. Create pull request"

