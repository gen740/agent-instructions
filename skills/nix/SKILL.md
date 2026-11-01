---
name: nix
description: Nix の式（flake.nix、パッケージ定義、開発シェル、NixOS / nix-darwin モジュールなど）を書く・直す・レビューするときに使う。
---

# Nix の書き方

既存プロジェクトでは、そのプロジェクトの構成と慣習を優先する。以下は既定の好み。

## flake と flake-parts
- 必ず flake を使う。`nix-env -i`、チャンネル、`nix-shell` / `default.nix` だけの構成にはしない。
- outputs は flake-parts（`flake-parts.lib.mkFlake { inherit inputs; } { ... }`）で書き、システムごとの出力は `perSystem` に置く。
- 出力が増えたら `flake.nix` に詰め込まず、`./nix/*.nix` に分けて `imports` で読み込む。パッケージは `pkgs.callPackage ./nix/<name>.nix { }` で呼ぶ。
- inputs に入れた flake が自分の `nixpkgs` input を持つ場合は、`inputs.<name>.inputs.nixpkgs.follows = "nixpkgs"` で揃える。その input を持たない flake には付けない（存在しない input への `follows` を機械的に足さない）。
- `flake.lock` は手で編集しない。更新は `nix flake update`（必要なら input を指定）で行う。
- フォーマットは `nixfmt`。`formatter` を出力に用意し、`nix fmt` で整える。

## `let ... in` を乱用しない
- 一箇所でしか使わない値を、わざわざ `let` に外出ししない。使う場所に直接書く。
- `let` を使うのは、長い式を複数回使うときや、数段のネストをまとめて読みやすくなるときなど、名前を付ける意味があるとき。
- 属性セットから取り出すだけなら `inherit (x) a b;` を使う。

```nix
# 悪い例: 1回しか使わない値まで let に入れている
let
  src = ./.;
  version = "0.1.0";
in
stdenv.mkDerivation { pname = "app"; inherit src version; }

# 良い例
stdenv.mkDerivation {
  pname = "app";
  version = "0.1.0";
  src = ./.;
}
```

## その他
- `overrideAttrs` やパッチ、バージョン固定など、理由が自明でない変更には「なぜそうするか」をコメントで残す。
