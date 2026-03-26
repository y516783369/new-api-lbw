#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 3 ]; then
  echo "Usage: $0 <new-api-root> <panel-base> <api-base>"
  echo "Example: $0 /opt/new-api https://panel.example.com https://api.example.com/v1"
  exit 1
fi

NEW_API_ROOT="$1"
PANEL_BASE="$2"
API_BASE="$3"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BRANDING_SRC="$SCRIPT_DIR/branding"
BRANDING_DST="$NEW_API_ROOT/branding"
DB_PATH="$NEW_API_ROOT/data/one-api.db"

mkdir -p "$BRANDING_DST"
cp -f "$BRANDING_SRC"/* "$BRANDING_DST"/

python3 "$SCRIPT_DIR/apply_runtime.py" \
  --db "$DB_PATH" \
  --branding-dir "$BRANDING_SRC" \
  --panel-base "$PANEL_BASE" \
  --api-base "$API_BASE"

echo "NovaMesh branding and runtime options applied."
echo "Branding copied to: $BRANDING_DST"
echo "Database updated: $DB_PATH"
