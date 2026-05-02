---
name: test-execution-report
description: 'テスト設計に基づいてテスト実施結果、証跡、失敗、障害票、再テスト、未実施、残リスクを整理するスキル。Use when: テスト結果をまとめたい、テスト実施報告を作りたい、証跡を整理したい、バグ一覧を作りたい、再テスト状況を整理したい, test execution report, test results, QA report.'
argument-hint: '対象テスト計画、観点表、テスト結果、またはリリース対象'
---

# テスト実施報告スキル

## 目的

`test-design` または `unit-test-design` で作成した観点表・テストケースに対して、実施結果と証跡を整理し、品質の現状を可視化する。
本スキルは「エビデンス」を収集し、`docs/traceability.json` の結果を更新し、`docs/evidence/test-execution.evidence.json` を出力してリリース判定へ繋ぐ。

## 位置づけ

`test-design` → `test-execution-report` → `operation-design-doc` → `release-readiness`

## 入力として確認する情報

- `docs/traceability.json`（テストケース ID 一覧）
- `test-design` / `unit-test-design` の成果物（テストケース、期待結果）
- 実際のテスト実施結果、ログ、スクリーンショット、障害管理ツールのエントリ

## 作成手順

1. **結果の記録**
   - 各テストケース（TC- / UT-）に対して、Pass / Fail / Pending を記録する。
   - `docs/traceability.json` の `tests` 配下の `result` を更新する。

2. **障害の整理**
   - Fail のケースに対し、障害内容、再現手順、修正状況をまとめる。
   - 修正済みのものは再テスト結果を付与する。

3. **エビデンスの集約**
   - テスト実施の証拠（ログファイル、実行コマンド結果、画像等）を整理する。

4. **証拠パッケージ（`docs/evidence/test-execution.evidence.json`）の作成**
   - `metrics` に `test_count`, `test_success`, `test_failure` を記入する。
   - 未解決の `blockers`（クリティカルな障害）件数と `blocker_ids` を明記する。
   - `artifacts` に証跡ファイル群のパス、`sha256` hash を含める。
   - `commands[]` にテスト実行コマンド、`exit_code`、`status`、要約を含める。

## 完了報告

- テスト実施報告書（サマリ）
- 障害一覧（Defect List）
- 更新された `docs/traceability.json`
- `docs/evidence/test-execution.evidence.json`（リリース判定の主入力）
- 残リスク（未実施・未解決事項の影響範囲）
