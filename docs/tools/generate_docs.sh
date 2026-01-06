#!/bin/bash

# Documentation Generation Script

set -e

echo "Generating documentation..."

# Generate API documentation from code
if command -v sphinx-apidoc &> /dev/null; then
    sphinx-apidoc -o docs/api src/
fi

# Generate OpenAPI schema
python3 <<EOF
from src.api.main import app
import json

with open("docs/agents/data/api_schema.json", "w") as f:
    json.dump(app.openapi(), f, indent=2)
EOF

echo "Documentation generated!"

