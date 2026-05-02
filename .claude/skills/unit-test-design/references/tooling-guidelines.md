# 言語/ツール別方針

## 共通

- 既存テストランナー、mockライブラリ、fixture、命名規則を優先する。
- `CODING_RULES.md` がある場合はそれを正とする。
- 新規テストツールの導入は勝手に行わず、提案として扱う。

## TypeScript / JavaScript

候補:

- Jest
- Vitest
- Node.js built-in test runner

方針:

- `class` / `this` を前提にしたテストを書かない。
- 関数型DIまたはfactory patternを前提にし、class bindingに依存したテストで依存注入を難しくしない。
- Service factory に依存を注入し、Repository mockを渡す。
- 型安全なmockを優先する。
- `Date.now`、UUID、randomは直接固定せず、依存注入できる形を優先する。

## Python

候補:

- pytest
- unittest

方針:

- pytest fixture を優先する。
- monkeypatch は時刻・環境変数・外部IFの差し替えに限定する。
- Repositoryや外部IFは fixture/fake で差し替える。
- Ruff/pytest の既存設定を確認する。

## Java

候補:

- JUnit
- Mockito

方針:

- Serviceを中心にテストする。
- Repositoryはmockする。
- Spring Contextを起動するものは原則として結合テストに回す。

## Go

候補:

- `go test`
- testify

方針:

- interfaceでRepositoryを差し替える。
- table driven test を優先する。
- DB実体を使うものは結合テストに分ける。
