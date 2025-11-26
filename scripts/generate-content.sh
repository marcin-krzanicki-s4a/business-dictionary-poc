#!/bin/bash

# S4A Business Dictionary - Content Generator
# Automatically generates Hugo content files (.md) from YAML data files
# Usage: ./scripts/generate-content.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🚀 S4A Dictionary Content Generator"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if yq is installed
if ! command -v yq &> /dev/null; then
    echo "❌ Error: 'yq' is not installed."
    echo "   Install with: brew install yq"
    exit 1
fi

cd "$PROJECT_ROOT"

# Counter for generated files
OBJECTS_GENERATED=0
VIEWS_GENERATED=0
PERSPECTIVES_GENERATED=0

echo ""
echo "📦 Generating Object content files..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Generate content files for Objects
for yaml_file in data/objects/*.yaml; do
    if [ -f "$yaml_file" ]; then
        # Extract object name from filename (e.g., AIRLINE.yaml -> AIRLINE)
        object_id=$(basename "$yaml_file" .yaml)
        
        # Convert to lowercase for URL (e.g., AIRLINE -> airline)
        object_slug=$(echo "$object_id" | tr '[:upper:]' '[:lower:]')
        
        # Extract data from YAML
        object_name=$(yq '.Name' "$yaml_file")
        object_definition=$(yq '.BusinessDefinition' "$yaml_file")
        
        # Create content file
        content_file="content/objects/${object_slug}.md"
        
        cat > "$content_file" <<EOF
---
title: "${object_name}"
description: "Definition of the ${object_name} business object."
---
EOF
        
        echo "  ✅ Generated: $content_file (from $object_id.yaml)"
        ((OBJECTS_GENERATED++))
    fi
done

echo ""
echo "🖼️  Generating View content files..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Generate content files for Views
for yaml_file in data/views/*.yaml; do
    if [ -f "$yaml_file" ]; then
        # Extract view name from filename (e.g., AirlineOperations_DashboardView.yaml)
        view_id=$(basename "$yaml_file" .yaml)
        
        # Extract data from YAML
        view_description=$(yq '.Description' "$yaml_file")
        view_platform=$(yq '.Platform' "$yaml_file")
        
        # Create a title from the view ID (e.g., AirlineOperations_DashboardView -> Airline Operations Dashboard View)
        view_title=$(echo "$view_id" | sed 's/_/ /g')
        
        # Create content file
        content_file="content/views/${view_id}.md"
        
        cat > "$content_file" <<EOF
---
title: "${view_title}"
description: "${view_description}"
---
EOF
        
        echo "  ✅ Generated: $content_file (from $view_id.yaml)"
        ((VIEWS_GENERATED++))
    fi
done

echo ""
echo "🔍 Generating Perspective content files..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Generate content files for Perspectives
# Iterate through all objects and their SystemPerspectives
for yaml_file in data/objects/*.yaml; do
    if [ -f "$yaml_file" ]; then
        object_id=$(basename "$yaml_file" .yaml)
        
        # Get all perspective names from this object
        perspective_names=$(yq '.SystemPerspectives | keys | .[]' "$yaml_file" 2>/dev/null || echo "")
        
        if [ -n "$perspective_names" ]; then
            while IFS= read -r perspective_name; do
                # Remove quotes from perspective name
                perspective_name=$(echo "$perspective_name" | tr -d '"')
                
                # Create a slug for the perspective (e.g., "Route Management" -> "route-management")
                perspective_slug=$(echo "$perspective_name" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
                
                # Create a filename (e.g., "airline-route-management.md")
                object_slug=$(echo "$object_id" | tr '[:upper:]' '[:lower:]')
                filename="${object_slug}-${perspective_slug}.md"
                
                # Create content file
                content_file="content/perspectives/${filename}"
                
                cat > "$content_file" <<EOF
---
title: "${perspective_name}"
object_id: "${object_id}"
perspective_id: "${perspective_name}"
---
EOF
                
                echo "  ✅ Generated: $content_file (${object_id} -> ${perspective_name})"
                ((PERSPECTIVES_GENERATED++))
            done <<< "$perspective_names"
        fi
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Content generation complete!"
echo ""
echo "📊 Summary:"
echo "   • Objects:      ${OBJECTS_GENERATED} files generated"
echo "   • Views:        ${VIEWS_GENERATED} files generated"
echo "   • Perspectives: ${PERSPECTIVES_GENERATED} files generated"
echo "   • Total:        $((OBJECTS_GENERATED + VIEWS_GENERATED + PERSPECTIVES_GENERATED)) files"
echo ""
echo "💡 Next steps:"
echo "   1. Review generated files in content/ directories"
echo "   2. Run 'hugo server' to preview changes"
echo "   3. Run 'hugo build' to build the site"
echo ""
