---
name: waterfall-delivery-cycle
description: 'ウォーターフォール型の開発サイクルをオーケストレーションする入口スキル。要件定義、基本設計、コーディングルール、実装、単体テスト設計、テスト設計、テスト実施報告、リリース判定、運用設計の各スキルをフェーズ判定・成果物確認・完了条件確認・トレーサビリティ維持の観点でつなぐ。Use when: 案件を進めたい、ウォーターフォールで進めたい、Epicをリリース可能な状態まで進めたい、次に何をすべきか判断したい、開発工程を管理したい, waterfall delivery, delivery cycle, phase gate, orchestration.'
argument-hint: '対象案件名、Epic名、現在の成果物、または進めたいフェーズ'
---

# ウォーターフォール開発サイクルスキル

## 目的

ユーザーが個別スキルを明示しなくても、案件の現在地を判定し、次に使うべきスキルと成果物を整理する。
このスキルは成果物そのものを詳細に作り込むのではなく、工程全体の入口、フェーズゲート、トレーサビリティ管理を担当する。
**本スキルは「エージェント間連携契約（Waterfall Contracts）」に基づき、JSON 構造化データを正本とした自律的なフェーズ管理を行う。**

## 対象サイクル

```text
requirements-definition-doc
  -> basic-design-doc
  -> unit-test-design（設計先行）
  -> project-coding-rules
  -> implementation-coding
  -> unit-test-design（差分確認）
  -> test-design
  -> test-execution-report
  -> operation-design-doc
  -> release-readiness
```

## 主な役割

- 現在フェーズを判定する。
- 前工程の成果物が足りているか確認する。
- 次に使うべきスキルを選ぶ。
- フェーズごとの完了条件を確認する。
- 未決事項、リスク、ブロッカーを次工程に引き継ぐ。
- 要件ID、設計ID、実装、テスト観点、テスト結果、リリース判定のトレーサビリティを維持する。

## フェーズと対応スキル

| フェーズ | 対応スキル | 主な成果物 |
|---|---|---|
| 要件定義 | `requirements-definition-doc` | 要件定義書、要件一覧、受入条件、TBD |
| 基本設計 | `basic-design-doc` | 基本設計書、画面/API/DB/処理フロー |
| 単体テスト設計 | `unit-test-design` | 基本設計起点のUT観点、UTケース、結合テストへ回す観点 |
| 実装標準化 | `project-coding-rules` | `CODING_RULES.md` |
| 実装 | `implementation-coding` | 実装コード、実装結果メモ |
| 単体テスト差分確認 | `unit-test-design` | 実装後のUT観点状態更新、UTコード対応レビュー |
| テスト設計 | `test-design` | テスト観点表、テストケース、テスト計画 |
| テスト実施 | `test-execution-report` | テスト結果、証跡、障害一覧 |
| 運用設計 | `operation-design-doc` | 運用設計書、監視、Runbook |
| リリース判定 | `release-readiness` | Go/No-Go、残リスク、切戻し確認 |

## 使い方

ユーザー指示例:

- この案件を進めて。
- このEpicをリリース可能な状態まで進めて。
- 今どのフェーズか判断して。
- 次に必要な成果物を教えて。
- フェーズゲートを確認して。

## 箱の範囲

- フェーズ判定
- 必要成果物チェック
- 次スキル選択
- フェーズゲート確認
- 全体トレーサビリティ確認
- リスク/TBD引き継ぎ

## フェーズゲート（次工程へ進む前の必須条件）

工程を跨ぐ際は以下のゲートを満たしているか確認する。**満たしていない場合は次工程に進まず、前工程に差し戻す。**

| ゲート | 条件 | 満たさない場合の対応 |
|--------|------|------------------|
| 要件定義 → 基本設計 | 要件IDが採番済み、受入条件が定義済み、優先度合意済み | `requirements-definition-doc` に戻る |
| **基本設計 → 単体テスト設計／コーディングルール** | **(1) `2.4 アーキテクチャ方針・実装制約` の方針合意が完成（採用ライブラリのバージョン、レイヤー責務、横断ライブラリの「選定」が具体的に記載／【TODO】が無い）／ (2) TODO 集約レポートに `BLOCKER` が 0 件／ (3) `openapi.yaml` が SSoT として存在し `x-api-id`・`operationId` が全 operation に付与済み／ (4) 主要シーケンス図に準正常系を含む** | `basic-design-doc` に戻して該当章を補強。BLOCKERは顧客／PM確認 |
| **コーディングルール → 実装** | **(1) `CODING_RULES.md` が基本設計 2.4 を具体化済み（命名規則・ディレクトリ構成・エラー実装形・ログフォーマット・Lint設定・テストツールが記載）／ (2) 2.4 とのズレが無い／ (3) 実装で使うコマンド（test / build / lint）が明記されている** | `project-coding-rules` に戻る。2.4 とズレている場合は、案件方針が変わったのか規約の不備かを切り分け、必要なら 2.4 側を改訂 |
| 実装 → テスト設計 | 実装完了、UT緑、要件IDと実装の対応がメモ化済み | `implementation-coding` に戻る |
| テスト実施 → 運用設計 | Must テスト全消化、未解決障害が許容内、運用設計に必要な NFR/ログ/監視観点が揃っている | `test-execution-report` または `test-design` に戻る |
| 運用設計 → リリース判定 | Runbook、監視・アラート、バックアップ/リストア、切戻し手順が作成され、運用リハーサル evidence がある | `operation-design-doc` に戻る |

## 共通契約

フェーズ間の引き継ぎは [references/contracts.md](./references/contracts.md) を正とする。

- `docs/traceability.json`: 要件、設計、テストの ID とリンクの正本。
- `docs/evidence/{phase}.evidence.json`: 各フェーズ完了の証拠パケット。
- `schemas/traceability.schema.json`: traceability の最低限の構造検証。
- `schemas/evidence.schema.json`: evidence packet の最低限の構造検証。
- `scripts/validate_traceability.py`: ID 重複、リンク参照、AC から TC への到達性を検証。
- `scripts/validate_evidence.py`: evidence schema、artifact sha256、blocker、command 結果を検証。

フェーズゲートでは Markdown を直接信用しない。`docs/traceability.json` と対象フェーズまでの `docs/evidence/*.evidence.json` を検証し、Markdown は人間向けビューとして扱う。

## コンテキスト管理方針

プロジェクトが中規模化するほど、AIに全ドキュメントを一度に渡すとハルシネーション・記憶喪失が増える。
各スキル呼び出し時は以下を徹底する。

- **スコープを絞る**: AIに渡すのは「対象フェーズの成果物」と「関連IDの差分」のみ。設計書全体、要件定義書全体をまとめて渡さない。
- **ID参照で繋ぐ**: 処理フローID、要件ID、設計IDを引数に指定し、AIが該当箇所だけを参照できるようにする。
- **1スキル＝1フォーカス**: 1回の呼び出しで扱う機能単位、APIエンドポイント単位、Serviceファイル単位を小さく保つ。
- **設計変更の同期プロトコル**: 実装中に設計変更が発生した場合、変更を `【設計変更: 変更内容と根拠】` で実装メモに記録してから、`basic-design-doc` の差分モードで設計書を更新する。設計書とコードの乖離（ドリフト）は発生した時点で即座に解消する。
- **ドリフト検知**: `unit-test-design（差分確認）` の Step 3 でコードと基本設計の不整合を検知したら、設計書修正を先に行い、UTケースの期待結果をコードから推測しない。
- **実装スキルからのエスカレーション受け**: `implementation-coding` が「設計から逸脱せざるを得ない」と判断して停止した場合、本スキルが受けて `basic-design-doc` の差分モードで設計書を改訂してから実装を再開させる。逸脱を実装側だけで吸収させない。

## 将来追加するテンプレート

- [assets/templates/delivery-cycle-tracker.md](./assets/templates/delivery-cycle-tracker.md)
- [assets/templates/phase-gate-checklist.md](./assets/templates/phase-gate-checklist.md)
- [assets/templates/traceability-overview.md](./assets/templates/traceability-overview.md)
