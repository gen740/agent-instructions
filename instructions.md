# 共通の指示

特定のツールやモデルに依存しない、エージェント共通の好み・指示の正本。
各ツールへの読み込み方は README の「ツール別の読み込み方」を参照。

## 好み・指示の置き場所
- ユーザー個人の好みや指示（どのプロジェクトでも効くもの）の正本はこのリポジトリ（GitHub 上の gen740/agent-instructions）。
  エージェント自身のメモリ機能や、各ツールのユーザー設定（設定ディレクトリ内の指示ファイルなど）には書き込まない。
  追加・変更は、このリポジトリへの Pull Request として提案する。手順は skill `update-my-config` を参照。
- プロジェクト固有の指示は、そのプロジェクトのリポジトリ（`.agents` など）に置く。

## ツールとパッケージ
- グローバルにパッケージをインストールしない（`brew install`、`pip install`、`npm install -g`、`cargo install`、`nix profile install` など）。
- 一時的に使うだけなら `nix run nixpkgs#<pkg>` や `nix shell nixpkgs#<pkg> -c <cmd>` を使う。
- プロジェクトで継続的に使うものは、そのプロジェクトの flake の devShell に追加する。
