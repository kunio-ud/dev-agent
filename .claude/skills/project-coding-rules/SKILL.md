---
name: project-coding-rules
description: '各リポジトリ/プロジェクトのコーディングルールを作成・更新するスキル。リポジトリ構成、言語、フレームワーク、対象レイヤー（フロントエンド、バックエンド、API、DB、バッチ、IaC/CDK、テスト）、既存コード規約を調査し、実装前に参照できるCODING_RULES.mdや開発規約を整備する。Use when: コーディングルールを作りたい、開発規約を作りたい、リポジトリの実装ルールを整理したい、フロント/サーバー/CDKのルールを決めたい、実装前のプロジェクト規約を作りたい, coding rules, coding standards, development guidelines, repository conventions.'
argument-hint: '対象リポジトリ、技術スタック、または作成したい規約の範囲'
---

# プロジェクトコーディングルール作成スキル

## 目的

プロジェクトごとの実装ルールを、既存リポジトリの実態に合わせて文書化する。
このスキルは `implementation-coding` の前段として使い、実装時に「このリポジトリではどう書くべきか」を明確にする。

## 出力先

標準:

- `docs/development/CODING_RULES.md`

規模が大きい場合:

- `docs/development/CODING_RULES.md`
- `docs/development/FRONTEND_RULES.md`
- `docs/development/BACKEND_RULES.md`
- `docs/development/API_RULES.md`
- `docs/development/DB_RULES.md`
- `docs/development/TESTING_RULES.md`
- `docs/development/IAC_RULES.md`

既存の規約ファイルがある場合は、それを優先して更新する。

## 先に読む参照

- リポジトリ判定: [references/repository-detection.md](./references/repository-detection.md)
- ルール作成観点: [references/rule-categories.md](./references/rule-categories.md)
- 既定アーキテクチャ方針: [references/default-architecture-policy.md](./references/default-architecture-policy.md)
- テンプレート: [assets/templates/coding-rules.md](./assets/templates/coding-rules.md)

## 作成手順

1. **基本設計 2.4 アーキテクチャ方針・実装制約を読む（最優先・必須）**
   - 基本設計書に **2.4 アーキテクチャ方針・実装制約**（[basic-design-doc/architecture-policy.md](../basic-design-doc/assets/templates/architecture-policy.md)）が存在する場合は、**必須インプットとして取り込む**。本書（CODING_RULES.md）は 2.4 を「リポジトリ実装の具体形」に展開する立場であり、2.4 と矛盾する規約を作ってはならない。
   - 2.4 で合意済み: 採用ライブラリ（バージョン含む）、レイヤー責務、横断ライブラリの選定、エラー分類、テスト方針、セキュリティ方針
   - 本書で具体化する: 命名規則、ディレクトリ構成、エラーの実装形（クラス階層・throwの形）、ログフォーマット、import順序、Lint/Formatter設定、テストフレームワーク選定・assertionスタイル
   - **2.4 が無い／曖昧な場合**: 既存コードと「先に読む参照」の `default-architecture-policy.md` を根拠に、2.4 で決まっていてほしい事項を `【TODO(BLOCKER): 基本設計 2.4 で確認】` として残し、ユーザーに警告する。
   - **2.4 と既存コードが矛盾している場合**: 既存コードを正とせず、2.4 に従って規約を作り、既存コードが規約違反である旨をリスクとして報告する。判断はユーザーに委ねる。

2. **リポジトリ構成を判定する**
   - モノリポ/単一アプリ/ライブラリ/IaC専用/ドキュメント中心のどれかを見る。
   - `package.json`、`pyproject.toml`、`pom.xml`、`build.gradle`、`Cargo.toml`、`go.mod`、`*.csproj`、`cdk.json`、`terraform` などを確認する。
   2. **初期構築モード時の対応（空リポジトリ時）**:
      リポジトリが完全に空の場合、コーディングルールを作成する前に以下の **構成案を提案** する。ユーザーの合意が得られた場合のみ、これらを最小構成で出力し、その上で `CODING_RULES.md` を作成する。
      1. 推奨ディレクトリ構成（技術スタックに合わせた `src/` レイアウト）
      2. `package.json` / `pyproject.toml` 等の最小設定スケルトン
      3. Lint・Formatter設定ファイル（ESLint / Prettier / Ruff 等）
      4. CI/CDの最小ワークフロー（GitHub Actions 推奨）

2. **対象レイヤーを判定する**
   - フロントエンド、バックエンド、API、DB、バッチ、外部IF、IaC/CDK、テスト、CI/CD のどれを含むか整理する。

3. **既存コードの流儀を抽出する**
   - ディレクトリ構成、命名、責務分割、エラー処理、ログ、設定、テスト、型、バリデーションを確認する。
   - 推測ではなく、既存ファイル名・設定・テストから根拠を取る。

4. **ルールを分類して書く**
   - 全体共通ルールとレイヤー別ルールを分ける。
   - **基本設計 2.4 がある場合はそれを最優先で反映する**（採用ライブラリ・レイヤー責務・横断ライブラリ選定・エラー分類）。2.4 が無い場合のみ、`default-architecture-policy.md` の既定方針（リポジトリパターン、Service層に業務ロジック、関数型プログラミング）を採用する。
   - 「必須」「推奨」「禁止」「要確認」を明確にする。
   - 未確定事項は `【TODO: 確認事項】` として残す。

5. **実装スキルに渡せる形にする**
   - 実装時に読むべき規約ファイル、テストコマンド、ビルドコマンド、禁止事項を明記する。

## 判定する主な項目

| 項目 | 例 |
|---|---|
| リポジトリ形態 | monorepo、single app、library、IaC-only |
| 言語 | TypeScript、JavaScript、Python、Java、Go、Rust、C# |
| フロントエンド | React、Next.js、Vue、Angular、Vite |
| バックエンド | Node.js、FastAPI、Django、Spring Boot、Go API、ASP.NET |
| DB | Prisma、TypeORM、SQLAlchemy、Flyway、Liquibase、生SQL |
| IaC/CDK | AWS CDK、Terraform、CloudFormation、Serverless |
| テスト | Jest、Vitest、Playwright、pytest、JUnit、go test |
| CI/CD | GitHub Actions、GitLab CI、CodeBuild |

## 書き方の原則

- 既存コードから分かる事実を優先する。
- プロジェクト固有の明示的な上書きがない限り、既定アーキテクチャ方針を採用する。
- 推測でルールを作らない。判断できない場合は `未確認` とする。
- ルールは実装者が迷わない粒度で書く。
- 抽象論だけでなく、対象ディレクトリやコマンドを具体化する。
- ルールを増やしすぎず、実装時に守るべきものを優先する。

## 完了時の報告

- 作成/更新した規約ファイル
- `docs/evidence/coding-rules.evidence.json`（規約作成完了の証拠、成果物 hash、確認コマンド）
- 判定したリポジトリ形態・言語・対象レイヤー
- 既存コードから読み取った主なルール
- 未確認事項
- 実装時に読むべきファイル
