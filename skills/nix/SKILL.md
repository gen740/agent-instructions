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
- 他の flake を inputs に入れるときは、`inputs.<name>.inputs.nixpkgs.follows = "nixpkgs"` で nixpkgs を揃える。
- `flake.lock` は手で編集しない。更新は `nix flake update`（必要なら input を指定）で行う。
- フォーマットは `nixfmt`。`formatter` を出力に用意し、`nix fmt` で整える。

## `let ... in` は必要なときだけ
- `let` で名前を付けるのは、**複数行にわたる長い式を、複数回使う**ときだけ。
- 1回しか使わない式は、使う場所に直接書く。短い式は複数回使っても無理に `let` にしない。
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
