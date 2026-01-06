#!/bin/bash

# Auto-update Specifications from Code

set -e

echo "Updating specifications from code..."

# Update API schema
python3 <<EOF
from src.api.main import app
import json

# Update API schema JSON
with open("docs/agents/data/api_schema.json", "w") as f:
    json.dump(app.openapi(), f, indent=2)

print("API schema updated")
EOF

# Update component map (if tool exists)
# This would require parsing the codebase
# For now, manual update is required

echo "Specifications updated!"

