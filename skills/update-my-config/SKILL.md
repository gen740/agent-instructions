---
name: update-my-config
description: ユーザーが「今後は〜して」「この好みを覚えて」など、エージェントの振る舞いや好みを追加・変更したいときに使う。手元には保存せず、GitHub 上の gen740/agent-instructions への Pull Request として出す。
---

# 好みの更新

好みは手元に保存しない。正本は GitHub 上の `gen740/agent-instructions`。
`main` へ直接 push せず、必ず Pull Request を出す（`main` はルールで保護されている）。

1. 変更内容を短い箇条書きにしてユーザーに確認する。
<<<<<<< HEAD
2. 手元のクローン（例: `/work/agent-instructions`）で `main` を最新にし、作業ブランチを切る。
   クローンがなければ `gh repo clone gen740/agent-instructions` する。
3. 編集する。
||||||| 4745fc3
2. agent-instructions の手元のクローンがあればそこを、なければクローンしてから編集する。
=======
2. 最新の `main` から作業ブランチを作り、編集する。
>>>>>>> origin/main
   - 全体に効く好み → `instructions.md`
   - 特定の作業手順 → `skills/<name>/SKILL.md` を新設
<<<<<<< HEAD
   - 特定のツール・モデル・プロジェクトに依存する内容は入れない（プロジェクト固有のものは各プロジェクトの `.agents` などへ）。
   - 秘密情報（キー、トークン、メールアドレス、個人のパス）は入れない。
4. `.claude-plugin/plugin.json` の `version` のパッチ番号を上げる（プラグインとして取り込むツールが更新を検知するため）。
5. コミットして push し、`gh pr create` で PR を出す。本文には「何を・なぜ変えるか」を書く。
6. PR の URL をユーザーに伝える。マージはユーザーが判断する。勝手にマージしない。
||||||| 4745fc3
3. Claude Code 側に反映するため `.claude-plugin/plugin.json` の `version` を上げる。
4. 差分を見せ、ユーザーの了承を得てからコミット・push する。
5. 反映方法を伝える：Claude Code はプラグインの更新、Codex はクローンを `git pull`。
=======
   - 特定のツール・モデル・プロジェクトに依存する内容は入れない（プロジェクト固有のものは各プロジェクトの `.agents` などへ）。
   - 秘密情報（API キー、トークンなど）は入れない。
3. `.claude-plugin/plugin.json` の `version` を上げる（プラグインとして取り込むツールが更新を検知するため）。
4. PR を作る。本文には「何を・なぜ変えるか」を書く。
5. PR の URL をユーザーに伝える。マージはユーザーが判断する。勝手にマージしない。
>>>>>>> origin/main
