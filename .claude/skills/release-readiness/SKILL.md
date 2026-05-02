---
name: release-readiness
description: 'リリース可否を判定するために、要件充足、Mustテスト消化、未解決障害、移行、切戻し、運用引継ぎ、残リスクを確認するスキル。Use when: リリース判定したい、リリース準備を確認したい、移行判定したい、Go/No-Go判断をしたい、残リスクを整理したい, release readiness, go no-go, deployment readiness.'
argument-hint: 'リリース対象、テスト結果、障害一覧、または移行計画'
---

# リリース判定スキル

## 目的

要件定義（AC-）、基本設計、テスト結果、および運用設計をもとに、対象 Epic/機能が本番リリース可能な状態かを判定する（Go/No-Go 判断）。
本スキルは **`docs/traceability.json` および各フェーズの `docs/evidence/{phase}.evidence.json` を機械的に検証**し、主観ではなくデータに基づいた最終合意を支援する。

## 位置づけ

`operation-design-doc` → `release-readiness`（最終フェーズ）

## 入力として確認する情報（SSoT）

1. **`docs/traceability.json`**: 
   - 全 `FR-` / `NFR-` が `SCR-` / `API-` / `FLOW-` / `BAT-` 等に紐付いているか。
   - 全 `AC-` に対応する `TC-` が `Pass` になっているか。
2. **各フェーズの `docs/evidence/{phase}.evidence.json`**:
   - `metrics.blockers` が全フェーズで 0 件であるか。
   - `blocker_ids` が全フェーズで空であるか。
   - テスト成功率が目標（100%）に達しているか。
   - 運用設計（Runbook, 監視）が完了しているか。
   - `artifacts[].hash` が実ファイルの sha256 と一致しているか。
   - 必須 `commands[]` が `status: Pass` かつ `exit_code: 0` であるか。

## 判定手順

1. **トレーサビリティ検証**
   - 未実装の要件、未実施のテストがないかを `docs/traceability.json` から抽出する。

2. **エビデンス検証**
   - 各フェーズエージェントが提出した `docs/evidence/{phase}.evidence.json` を突合する。
   - 成果物ハッシュの整合性を確認し、ドキュメントの改ざんや未更新がないかを確認する。

3. **移行・切戻しプランの確認**
   - リリース当日、万が一の際の切戻し（Rollback）手順が具体的かつ検証済みかを確認する。

4. **Go/No-Go 判定**
   - 上記を総合し、Go（リリース可能） / No-Go（リリース不可） / Conditional Go（条件付きリリース）を判定する。

## 完了報告

- リリース判定報告書（Go/No-Go Report）
- リリース判定チェックリスト結果
- 最終的な `docs/evidence/release-readiness.evidence.json`（リリース判定結果を格納）
- 次回以降の改善申し送り事項
