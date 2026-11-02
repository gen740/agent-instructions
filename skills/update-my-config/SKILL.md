---
name: update-my-config
description: ユーザーが「今後は〜して」「この好みを覚えて」など、エージェントの振る舞いや好みを追加・変更したいときに使う。手元には保存せず、GitHub 上の gen740/agent-instructions への Pull Request として出す。
---

# 好みの更新

好みは手元に保存しない。正本は GitHub 上の `gen740/agent-instructions`。
`main` へ直接 push せず、必ず Pull Request を出す（`main` はルールで保護されている）。

1. 変更内容を短い箇条書きにしてユーザーに確認する。
2. 最新の `main` から作業ブランチを作り、編集する。
   - 全体に効く好み → `instructions.md`
   - 特定の作業手順 → `skills/<name>/SKILL.md` を新設
   - 特定のツール・モデル・プロジェクトに依存する内容は入れない（プロジェクト固有のものは各プロジェクトの `.agents` などへ）。
   - 秘密情報（API キー、トークンなど）は入れない。
3. PR を作る。本文には「何を・なぜ変えるか」を書く。
4. PR の URL をユーザーに伝える。マージはユーザーが判断する。勝手にマージしない。
