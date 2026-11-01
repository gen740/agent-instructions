#!/usr/bin/env bash
# Codex に agent-instructions を読ませる: ~/.codex/AGENTS.md と ~/.codex/skills/* をこのクローンへのリンクにする
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
codex_home="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$codex_home/skills"

link() {
  local src="$1" dst="$2"
  if [[ -e "$dst" && ! -L "$dst" ]]; then
    echo "skip: $dst は既存のファイルです（手動で退避してください）" >&2
    return
  fi
  ln -sfn "$src" "$dst"
  echo "linked: $dst -> $src"
}

link "$repo/instructions.md" "$codex_home/AGENTS.md"
for skill in "$repo"/skills/*/; do
  link "${skill%/}" "$codex_home/skills/$(basename "$skill")"
done
