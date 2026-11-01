---
name: cpp
description: C++ のコードを書く・直す・レビューするとき、または C++ プロジェクトの CMake・clang-tidy・clang-format を設定するときに使う。
---

# C++ の書き方

既存プロジェクトでは、そのプロジェクトの規格・設定・慣習を優先する。以下は既定の好み。

## 規格と書き方
- 新規プロジェクトは、Nix で入る最新のコンパイラが対応する最新規格（例: `CMAKE_CXX_STANDARD 26`）で書き、新機能を積極的に使う。`CMAKE_CXX_EXTENSIONS OFF`。
- テンプレートを使ったジェネリックで modern な書き方を好む。型の制約は SFINAE ではなく concepts / `requires` で書く。分岐は `if constexpr`。
- 名前付き関数は trailing return type（`auto f(int x) -> T`）。ラムダの戻り値は推論に任せる。
- 標準ライブラリの modern な機能を優先する: ranges / views、`std::span`、`std::optional`、`std::variant` + `std::visit`、designated initializers、`[[nodiscard]]`、`std::jthread` など。
- 所有権は `std::unique_ptr` などで表し、生の `new` / `delete` は使わない。

## 命名とファイル
- 型・concept・テンプレート引数は `CamelCase`。関数・メソッド・変数・メンバは `lower_case`。private / protected メンバは末尾に `_`。
- ヘッダは `.hh`（`#pragma once`）、実装は `.cc`。
- フォーマットは clang-format（`BasedOnStyle: Google` をベース）。

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
  readability-identifier-naming.ClassCase: CamelCase
  readability-identifier-naming.StructCase: CamelCase
  readability-identifier-naming.EnumCase: CamelCase
  readability-identifier-naming.TemplateParameterCase: CamelCase
  readability-identifier-naming.ConceptCase: CamelCase
  readability-identifier-naming.FunctionCase: lower_case
  readability-identifier-naming.MethodCase: lower_case
  readability-identifier-naming.PrivateMemberCase: lower_case
  readability-identifier-naming.PrivateMemberSuffix: '_'
  readability-identifier-naming.ProtectedMemberCase: lower_case
  readability-identifier-naming.ProtectedMemberSuffix: '_'
  readability-identifier-naming.PublicMemberCase: lower_case
  # 名前付き関数は trailing return type、ラムダは推論のまま
  modernize-use-trailing-return-type.TransformLambdas: none
```
