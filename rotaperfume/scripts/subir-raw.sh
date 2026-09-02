#!/usr/bin/env bash
set -euo pipefail

profile="${1:-}"
if [[ -z "$profile" ]]; then
  echo "Uso: $0 <profile>" >&2
  exit 2
fi

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
data_dir="$repo_root/dados"
if [[ ! -d "$data_dir/erp" || ! -d "$data_dir/crm" ]]; then
  python3 "$repo_root/material/gerar_dataset.py" --saida "$data_dir" --seed 42
fi

for system in erp crm; do
  databricks fs cp --recursive --overwrite \
    "$data_dir/$system" \
    "dbfs:/Volumes/lakehouse_rotaperfume/bronze/raw/$system" \
    --profile "$profile"
done
