---
name: update-my-config
description: ユーザーが「今後は〜して」「この好みを覚えて」など、エージェントの振る舞いや好みを追加・変更したいときに使う。ローカルに保存せず、GitHub 上の agent-instructions リポジトリへの変更として扱う。
---

# 好みの更新

ユーザーの好みはローカルに保存しない。正本は GitHub 上の agent-instructions リポジトリ。

1. 変更内容を短い箇条書きにしてユーザーに確認する。
2. agent-instructions の手元のクローンがあればそこを、なければクローンしてから編集する。
   - 全体に効く好み → `instructions.md`
   - 特定の作業手順 → `skills/<name>/SKILL.md` を新設
3. Claude Code 側に反映するため `.claude-plugin/plugin.json` の `version` を上げる。
4. 差分を見せ、ユーザーの了承を得てからコミット・push する。
5. 反映方法を伝える：Claude Code はプラグインの更新、Codex はクローンを `git pull`。
