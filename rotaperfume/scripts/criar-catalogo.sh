#!/usr/bin/env bash
set -euo pipefail

profile="${1:-}"
if [[ -z "$profile" ]]; then
  echo "Uso: $0 <profile>" >&2
  exit 2
fi

# No Free Edition, Default Storage sem managed location faz a API do UC
# retornar INVALID_STATE; a criação equivalente por SQL funciona.
databricks experimental aitools tools query \
  --profile "$profile" \
  "CREATE CATALOG IF NOT EXISTS lakehouse_rotaperfume COMMENT 'Catalogo principal do projeto Rota Perfume'"
