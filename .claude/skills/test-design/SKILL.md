---
name: test-design
description: '要件定義・基本設計・実装コード・既存テストからテスト観点を抽出し、テストレベル、優先度、自動化方針、テストケースへ落とし込むスキル。単体、結合、システム、受入、性能、セキュリティ、外部IF、バッチ、DB、画面、APIの観点をトレーサビリティ付きで整理する。Use when: テスト観点を出したい、テスト設計したい、結合テスト観点を作りたい、システムテスト観点を作りたい、受入テストを整理したい、要件定義や基本設計からテストケースを作りたい、既存テストの不足を洗い出したい, test design, test viewpoints, test cases, integration test, system test, acceptance test.'
argument-hint: '対象機能名、要件ID/設計ID、またはテスト対象の概要'
---

# テスト設計スキル

## 目的

要件定義・基本設計・実装コード・既存テストを入力として、品質を担保するための**テスト観点**を抽出する。
本スキルは、いきなりテストケースを書かず、まず観点表を作り、テストレベル・優先度・自動化可否を決めてからテストケースに落とす。

## 位置づけ

推奨工程:

`requirements-definition-doc` → `basic-design-doc` → `unit-test-design（設計先行）` → `project-coding-rules` → `implementation-coding` → `unit-test-design（差分確認）` → `test-design` → `test-execution-report`

実装前にも使える。その場合は、要件定義・基本設計から先に結合/システム/受入観点を作る。単体観点は `unit-test-design` で先行設計し、実装後にコード/既存テストとの差分で補強する。

## 実行モード

| モード | 起動タイミング | 実行ステップ | 出力状態 |
|---|---|---|---|
| 設計先行モード | 基本設計完了直後（実装前） | 1〜4, 6 | 観点表・テスト計画のみ。テストケース化は Must 観点に絞る。状態=Designed |
| 実装後差分確認モード | `unit-test-design（差分確認）` 完了後 | 全ステップ | 観点差分補強、ケース実装状態を Implemented/Pending に更新 |

## 入力優先度

| 優先度 | 入力 | 使い方 |
|---|---|---|
| 1 | 要件定義書 | BR/FR/NFR/AC/制約から確認すべき品質を抽出する |
| 2 | 基本設計書 | 画面/API/DB/処理フロー/外部IF/バッチから具体パターンを抽出する |
| 3 | unit-test-design 完了報告 | UTで設計済み/実装済み/実行済みの範囲と、結合/システム/受入へ回す観点を引き継ぐ（直前工程の正規引き継ぎ） |
| 4 | 実装コード | 実際の分岐、例外、権限、データ操作、外部呼び出しを補完する |
| 5 | 既存テスト | 既存で確認済みの範囲と不足観点を分ける |
| 6 | コーディングルール | テスト配置、命名、実行コマンド、自動化方針を確認する |

入力が不足していても作業を止めない。ただし、受入条件・セキュリティ要件・データ破壊リスク・外部IFの責任分界が不明な場合は確認事項として明示し、`TBD-NNN` ID を採番して `docs/traceability.json` に記録する。

`unit-test-design` が存在しない場合は、単体観点も自身で抽出するか、`unit-test-design` の先行実施を提案する。

## 先に読む参照

- テスト観点カタログ: [references/test-viewpoints.md](./references/test-viewpoints.md)
- テストレベル定義: [references/test-levels.md](./references/test-levels.md)
- リスクベース優先度: [references/risk-based-prioritization.md](./references/risk-based-prioritization.md)
- エージェント間連携契約: [../waterfall-delivery-cycle/references/contracts.md](../waterfall-delivery-cycle/references/contracts.md)

## 作成手順

1. **対象を固定する**
   - 対象要件ID、設計ID、画面/API/DB/バッチ/外部IF、対象外を明確にする。
   - ID はすべて [エージェント間連携契約](../waterfall-delivery-cycle/references/contracts.md) の体系に従う。

2. **入力から観点を抽出する**
   - 要件定義から「何を満たすべきか」を抽出する。
   - 基本設計から「どこをどう確認するか」を抽出する。
   - `unit-test-design` の完了報告がある場合は、「結合テストへ回す観点」を結合/システム/受入テスト候補として優先的に取り込む。
   - 実装コードから「実際に分岐・例外・副作用がある箇所」を補完する。
   - 既存テストから「確認済み/不足」を分ける。

3. **観点表を作る**
   - 観点ID（`TV-{機能略称}-NNN` 形式を推奨）、対象要件、対象AC、対象設計、観点、リスク（高/中/低 + `RSK-NNN`）、テストレベル、自動化可否、優先度、状態（Designed/Implemented/Executed）、TBD-ID を書く。
   - 最初の成果物はテストケースではなく観点表にする。
   - 機能・レイヤー（画面/API/DB/バッチ）が大きい場合は機能単位でファイルを分割する。

4. **テストレベルを割り当てる**
   - 単体、結合、システム、受入、性能、セキュリティなどに分ける。
   - 同じ観点を複数レベルで重複確認しすぎない。
   - `unit-test-design` で確認済みの範囲は単体レベルに割り当て済みとし、結合/システムでの単体重複を避ける。ただし、複数コンポーネントをまたぐ確認が必要なものは別観点として立てる。

5. **テストケースへ落とす**
   - Must/高リスク観点からテストケース化する。
   - 前提、操作、期待結果（対応する基本設計IDを根拠として明記）、テストデータ、自動化可否、対応AC-ID、対応テスト関数/ファイルを明記する。
   - **Must 優先度のTCは、test-design evidence が Completed になる前に対応するテスト関数またはスクリプトが実装済みでなければならない（contracts §6）。**
     - 後フェーズに送る場合は `RSK-NNN` または `TBD-NNN` として `blocker_ids` に記録し、`metrics.blockers` をインクリメントする。
     - 「代替済み」「省略」「他ケースで代替」などのメモ行はTC表に含めない。代替・除外の記録は「除外観点」節（別セクション）に移す。
   - Should/Could 優先度のTCは未実装のまま次フェーズへ送ることができるが、`docs/traceability.json` に `status: Pending` で残す。

6. **TBD を管理する**
   - 受入条件・セキュリティ要件・データ破壊リスク・外部IF責任分界が不明な場合は `TBD-NNN` を採番する。
   - TBD が解消された場合は `docs/traceability.json` の `status: Resolved`、`resolved_at`（ISO 8601）、`resolution` を記入し、evidence の `notes` に `"TBD-NNN resolved: <解消内容>"` を記録する（contracts §7）。
   - 未解消のTBDはすべて blocker として evidence の `blocker_ids` に追加し、`metrics.blockers` に計上する。

7. **トレーサビリティを確認する**
   - `docs/traceability.json` に TV-/TC-ID を追加し、以下を埋める:
     - `tests[].id`（TV- または TC-）
     - `tests[].traces_to`（AC-ID, FR-ID, NFR-ID 等）
     - `tests[].priority`（Must/Should/Could）
     - `tests[].status`（Designed/Implemented/Pending）
   - AC から TV/TC への到達性を `scripts/validate_traceability.py` で確認する。
   - 要件に対して観点がないもの、観点に対してテストケースがないものを明示する。

## 出力テンプレート

- テスト観点表: [assets/templates/test-viewpoint-matrix.md](./assets/templates/test-viewpoint-matrix.md)
- テストケース: [assets/templates/test-cases.md](./assets/templates/test-cases.md)
- テスト計画: [assets/templates/test-plan.md](./assets/templates/test-plan.md)

## 完了報告

- 作成した観点表/テストケース/テスト計画
- `docs/traceability.json` 更新（TV-/TC-ID の追加と紐付け、AC→TV→TC 到達性確認済み）
- `docs/evidence/test-design.evidence.json` を以下の仕様で作成し、`scripts/validate_evidence.py` を Pass させる:
  - `phase: "test-design"`
  - `status`: "Completed"（Must TC 全実装済み、blockers=0）または "Blocked"
  - `metrics.blockers`（未解消TBD + Must 未実装TC の件数）、`metrics.todos`
  - `metrics.test_count / test_success / test_failure / test_pending`（合計一致必須）
  - `artifacts[]`: 各成果物ファイルを sha256 ハッシュ付きで登録
  - `blocker_ids[]`: `TBD-NNN` / `RSK-NNN` を列挙
  - `commands[]`: `scripts/validate_traceability.py`、`scripts/validate_evidence.py` の実行結果を含める
- `unit-test-design` で設計済み/実装済み/実行済みの観点（引き継ぎ元）
- 高リスク観点（RSK-ID 付き）
- 自動化候補
- Must TC の実装状態サマリ（実装済み件数 / 合計 Must TC 件数）
- 未解消 TBD 一覧
- 要件または設計に不足している情報
