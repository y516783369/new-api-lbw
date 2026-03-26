#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 4 ]; then
  echo "Usage: $0 <new-api-root> <panel-domain> <api-domain> <output-dir>"
  echo "Example: $0 /opt/new-api panel.example.com api.example.com /opt/new-api-bootstrap"
  exit 1
fi

NEW_API_ROOT="$1"
PANEL_DOMAIN="$2"
API_DOMAIN="$3"
OUTPUT_DIR="$4"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$OUTPUT_DIR"

python3 "$SCRIPT_DIR/prepare_instance.py" \
  --new-api-root "$NEW_API_ROOT" \
  --panel-domain "$PANEL_DOMAIN" \
  --api-domain "$API_DOMAIN" \
  --output-dir "$OUTPUT_DIR"

echo
echo "Next steps:"
echo "1. Review $OUTPUT_DIR/compose.yml"
echo "2. Run docker compose with that file"
echo "3. Apply the generated Caddy files"
echo "4. Run bootstrap.sh after one-api.db exists"
