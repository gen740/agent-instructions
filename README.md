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
git clone https://github.com/gen740/agent-instructions.git "$HOME/src/agent-instructions"
"$HOME/src/agent-instructions/scripts/link-codex.sh"
```

初回設定で、共通指示を `${CODEX_HOME:-$HOME/.codex}/AGENTS.md`、skills 全体を
`~/.agents/skills/agent-instructions` から参照する。
後者は `CODEX_HOME` に関係なく、Codex のユーザー用探索先 `~/.agents/skills` に置く。
他の skill と同居でき、既存のファイル・ディレクトリ・別のリンクは上書きしない。
衝突した場合はエラーで終了するので、内容を確認して手動で退避してから再実行する。

更新は次のコマンドで行う（クローン先が異なる場合は読み替える）。

```bash
git -C "$HOME/src/agent-instructions" pull --ff-only
```

既存 skill の編集だけでなく、新しい skill の追加もリンクの再実行なしで反映される。
Codex は変更されたローカル skill を検出する。表示されなければ Codex を再起動する。
これはローカルファイルの再読込であり、GitHub からの取得には上記の pull が必要。
探索先と symlink 対応は [公式ドキュメント](https://learn.chatgpt.com/docs/build-skills) を参照。

#### 旧スクリプトからの移行

旧スクリプトは `~/.codex/skills/<skill名>` に個別リンクを作っていたため、
**新しい skill の追加時には再実行が必要だった**。
既存クローンで pull 後、`scripts/link-codex.sh` を一度だけ再実行すると、新しい方式へ移行できる。
旧リンクや他の skill は削除しない。同じ実体への旧リンクが残っていても Codex は重複を除いて読み込む。
以後は pull だけでよく、CI から各 PC のリンクを変更したり、生成物を main に push したりする必要はない。

#### 検証

```bash
python3 -m unittest discover -s tests -v
CODEX_TEST_BINARY="$(command -v codex)" python3 -m unittest discover -s tests -v
```

前者は初回設定・再実行・衝突時の保全を検証する。
後者は隔離したホームで実際の Codex `skills/list` を呼び、
初回の探索、旧リンクとの同居、他の skill の保全、pull で追加した skill の探索を検証する。
モデル呼出しやログインは不要。CI では Codex CLI 0.166.0 を使って両方を実行する。
