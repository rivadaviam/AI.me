#!/bin/bash

# Documentation Validation Script

set -e

echo "Validating documentation..."

# Check for required files
REQUIRED_FILES=(
    "README.md"
    "docs/ARCHITECTURE.md"
    "docs/QUICKSTART.md"
    "docs/product/PRODUCT_SPEC.md"
    "docs/product/API_SPEC.md"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "ERROR: Missing required file: $file"
        exit 1
    fi
done

# Validate markdown syntax (if markdownlint is available)
if command -v markdownlint &> /dev/null; then
    markdownlint docs/**/*.md || echo "Markdown linting issues found"
fi

echo "Documentation validation complete!"

