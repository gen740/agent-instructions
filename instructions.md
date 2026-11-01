# 共通の好み（Claude Code / Codex 共通）

このファイルが好みの正本です。Claude Code にはプラグインの SessionStart フックで、
Codex には `~/.codex/AGENTS.md` へのシンボリックリンクで読み込まれます。

## コミュニケーション
- 日本語で返答する。コード・コマンド・識別子は原文のまま。

## 好みの保存場所
- 好み・指示・カスタマイズをローカル（エージェントのメモリファイル、`~/.claude/`、`~/.codex/` の設定など）に直接書き込まない。
- 好みを追加・変更したいと言われたら、このリポジトリ（GitHub 上の agent-instructions）への変更として提案する。
  詳しい手順は skill `update-my-config` を参照。
