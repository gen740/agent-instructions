#!/usr/bin/env bash
# Codex 用: 共通指示と skills 全体をこのクローンへのリンクにする
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
codex_home="${CODEX_HOME:-$HOME/.codex}"
user_skills="$HOME/.agents/skills"

check_link() {
  local src="$1" dst="$2"
  if [[ -L "$dst" && "$(readlink "$dst")" == "$src" ]]; then
    return 0
  fi
  if [[ -e "$dst" || -L "$dst" ]]; then
    echo "conflict: $dst は既存のファイルまたはリンクです（手動で確認・退避してください）" >&2
    return 1
  fi
}

link() {
  local src="$1" dst="$2"
  if [[ -L "$dst" && "$(readlink "$dst")" == "$src" ]]; then
    echo "already linked: $dst -> $src"
    return 0
  fi
  ln -s "$src" "$dst"
  echo "linked: $dst -> $src"
}

# どちらかが衝突する場合、既存設定を変更せずに終了する。
check_link "$repo/instructions.md" "$codex_home/AGENTS.md"
check_link "$repo/skills" "$user_skills/agent-instructions"
mkdir -p "$codex_home" "$user_skills"
link "$repo/instructions.md" "$codex_home/AGENTS.md"
# Codex はこのディレクトリリンクの配下も探索する。skill 追加時の再リンクは不要。
link "$repo/skills" "$user_skills/agent-instructions"
