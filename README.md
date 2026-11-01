# agent-instructions

Claude Code と Codex で共有する、個人の好み・指示・skill の正本。
編集はこのリポジトリだけで行い、各ツールの手元にあるのは取ってきたコピーとして扱う。

## 構成

| パス | 内容 |
|---|---|
| `instructions.md` | 共通の好み（system.md 相当） |
| `skills/*/SKILL.md` | 共通の skill |
| `.claude-plugin/` | Claude Code 用プラグイン + マーケットプレイス定義 |
| `hooks/hooks.json` | SessionStart で `instructions.md` を読み込ませる |
| `scripts/link-codex.sh` | Codex 用に `~/.codex` へリンクを張る |

## Claude Code に入れる

```bash
claude plugin marketplace add gen740/agent-instructions
claude plugin install my-prefs@agent-instructions
```

更新を反映するときは `.claude-plugin/plugin.json` の `version` を上げて push し、
`claude plugin marketplace update agent-instructions` を実行する。

## Codex に入れる

```bash
git clone https://github.com/gen740/agent-instructions.git ~/src/agent-instructions
~/src/agent-instructions/scripts/link-codex.sh
```

更新は `git -C ~/src/agent-instructions pull` だけ（リンクなので再実行不要）。
