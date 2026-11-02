---
name: cpp
description: C++ のコードを書く・直す・レビューするとき、または C++ プロジェクトの CMake・clang-tidy・clang-format を設定するときに使う。
---

# C++ の書き方

既存プロジェクトでは、そのプロジェクトの規格・設定・慣習を優先する。以下は既定の好み。

## スタイル
- [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html) に準拠する（clang-format は `BasedOnStyle: Google`）。ガイドにあることはここに書かない。
- ただし次の点はガイドと異なる、自分の流儀を優先する:
  - 名前付き関数はすべて trailing return type（`auto f(int x) -> T`）。ラムダの戻り値は推論に任せる。
  - ヘッダの拡張子は `.hh`、実装は `.cc`。
  - インクルードガードは `#pragma once`（ガイドの `<PROJECT>_<PATH>_<FILE>_H_` ではない）。`#pragma once` を強制する clang-tidy の check は upstream にないので、`llvm-header-guard` と `portability-avoid-pragma-once` を有効にしないことだけ守る。

## 規格と書き方
- 新規プロジェクトは、Nix で入る最新のコンパイラが対応する最新規格（例: `CMAKE_CXX_STANDARD 26`）で書き、新機能を積極的に使う。`CMAKE_CXX_EXTENSIONS OFF`。
- テンプレートを使ったジェネリックで modern な書き方を好む。型の制約は concepts / `requires`、分岐は `if constexpr`。

## ビルド
- ビルドシステムは CMake、ジェネレータは Ninja（`cmake -G Ninja`）を好む。
- ディレクトリ構成は、ルートに `CMakeLists.txt`、公開ヘッダを `include/`、実装を `src/` に置く形を好む。

## 警告とチェックはすべてエラー
- コンパイラ: `-Wall -Wextra -Werror -Wformat=2 -Wimplicit-fallthrough`。
- CMake で clang-tidy をビルドに組み込み、clang-tidy の警告もエラーにする:
  ```cmake
  set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
  find_program(CLANG_TIDY_EXECUTABLE clang-tidy REQUIRED)
  set(CMAKE_CXX_CLANG_TIDY "${CLANG_TIDY_EXECUTABLE};--quiet;--config-file=${PROJECT_SOURCE_DIR}/.clang-tidy")
  ```
- 警告やチェックを無効にするときは、範囲をできるだけ狭くし、理由をコメントで残す。エラーを消すために無効化で逃げない。

## `.clang-tidy` の基本形
```yaml
Checks: >-
  -*,
  clang-analyzer-core.*,
  clang-analyzer-cplusplus.*,
  clang-analyzer-unix.*,
  modernize-*,
  bugprone-*,
  cppcoreguidelines-*,
  readability-identifier-naming,
  -bugprone-easily-swappable-parameters,
  -cppcoreguidelines-avoid-magic-numbers,
  -cppcoreguidelines-owning-memory,
  -cppcoreguidelines-pro-bounds-constant-array-index,
  -cppcoreguidelines-pro-bounds-pointer-arithmetic
WarningsAsErrors: '*'
HeaderFilterRegex: '.*'
FormatStyle: file
CheckOptions:
  # 命名は Google C++ Style Guide に合わせる
  readability-identifier-naming.NamespaceCase: lower_case
  readability-identifier-naming.ClassCase: CamelCase
  readability-identifier-naming.StructCase: CamelCase
  readability-identifier-naming.EnumCase: CamelCase
  readability-identifier-naming.TypeAliasCase: CamelCase
  readability-identifier-naming.TypeAliasIgnoredRegexp: '^(.*_type|(const_)?iterator)$'
  readability-identifier-naming.TemplateParameterCase: CamelCase
  readability-identifier-naming.ConceptCase: CamelCase
  readability-identifier-naming.FunctionCase: CamelCase
  readability-identifier-naming.FunctionIgnoredRegexp: '^(get|swap)$'
  readability-identifier-naming.MethodCase: CamelCase
  # アクセサ（count()、set_count()）や begin/end などの snake_case はガイドで許されるので通す
  readability-identifier-naming.MethodIgnoredRegexp: '^[a-z][a-z0-9_]*$'
  readability-identifier-naming.VariableCase: lower_case
  readability-identifier-naming.ParameterCase: lower_case
  readability-identifier-naming.PrivateMemberCase: lower_case
  readability-identifier-naming.PrivateMemberSuffix: '_'
  readability-identifier-naming.ProtectedMemberCase: lower_case
  readability-identifier-naming.ProtectedMemberSuffix: '_'
  readability-identifier-naming.PublicMemberCase: lower_case
  readability-identifier-naming.ConstexprVariableCase: CamelCase
  readability-identifier-naming.ConstexprVariablePrefix: k
  readability-identifier-naming.GlobalConstantCase: CamelCase
  readability-identifier-naming.GlobalConstantPrefix: k
  readability-identifier-naming.StaticConstantCase: CamelCase
  readability-identifier-naming.StaticConstantPrefix: k
  readability-identifier-naming.EnumConstantCase: CamelCase
  readability-identifier-naming.EnumConstantPrefix: k
  readability-identifier-naming.MacroDefinitionCase: UPPER_CASE
  # 名前付き関数は trailing return type、ラムダは推論のまま
  modernize-use-trailing-return-type.TransformLambdas: none
```
