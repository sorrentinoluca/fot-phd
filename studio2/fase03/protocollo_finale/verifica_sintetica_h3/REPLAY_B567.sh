#!/usr/bin/env bash
set -euo pipefail

output_dir="${1:?uso: REPLAY_B567.sh /percorso/assoluto/output-nuovo}"
repo_root="$(git rev-parse --show-toplevel)"
artifact_dir="studio2/fase03/protocollo_finale/verifica_sintetica_h3"
frozen_commit="b465f90373debfe4ae252389cda4b13154a0e13b"
temporary_dir="$(mktemp -d)"
trap 'rm -rf "$temporary_dir"' EXIT

git show "$frozen_commit:$artifact_dir/run_verifica_sintetica_h3.py" > "$temporary_dir/run_verifica_sintetica_h3.py"
git show "$frozen_commit:$artifact_dir/SCENARI_TARGET.jsonl" > "$temporary_dir/SCENARI_TARGET.jsonl"

test "$(shasum -a 256 "$temporary_dir/run_verifica_sintetica_h3.py" | awk '{print $1}')" = \
  "847bc294948303a1d4763cc223893eeffc167c42f4e3b1540f73ed31feb53c5f"
test "$(shasum -a 256 "$temporary_dir/SCENARI_TARGET.jsonl" | awk '{print $1}')" = \
  "51711d6e3352296f704393601a3b94cc3e2966e7b728ad13da4b12cfe6dad74f"

uv run --no-project --with numpy==2.5.2 --with scipy==1.17.1 python \
  "$temporary_dir/run_verifica_sintetica_h3.py" run \
  --manifest "$temporary_dir/SCENARI_TARGET.jsonl" --output "$output_dir"
uv run --no-project --with numpy==2.5.2 --with scipy==1.17.1 python \
  "$repo_root/$artifact_dir/run_verifica_sintetica_h3.py" aggregate \
  --manifest "$temporary_dir/SCENARI_TARGET.jsonl" --output "$output_dir"
