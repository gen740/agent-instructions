# agent-instructions

コーディングエージェント共通の、個人的な好み・指示・skill の正本。
特定のツールやモデルに依存しない内容だけを置き、各ツールの手元にあるのは取ってきたコピーとして扱う。

## 構成

| パス | 内容 |
|---|---|
| `instructions.md` | 共通の指示（system.md 相当） |
| `skills/*/SKILL.md` | 共通の skill |
| `.claude-plugin/`, `hooks/`, `scripts/` | ツールごとの読み込み用アダプタ |

## 変更の流れ

1. エージェントに「今後は〜して」と頼む → skill `update-my-config` に従って PR が出る
2. 自分で確認してマージする（`main` への直接 push はルールで禁止）
3. 各ツールに反映する（下記）

## ツール別の読み込み方

### Claude Code

```bash
claude plugin marketplace add gen740/agent-instructions
claude plugin install my-prefs@agent-instructions
```

反映: `claude plugin marketplace update agent-instructions`
（`version` を固定していないので、コミットごとに更新として扱われる）

### Codex

```bash
git clone https://github.com/gen740/agent-instructions.git /work/agent-instructions
/work/agent-instructions/scripts/link-codex.sh
```

反映: `git -C /work/agent-instructions pull`（リンクなので再実行不要）
