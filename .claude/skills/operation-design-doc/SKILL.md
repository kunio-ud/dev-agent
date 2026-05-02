---
name: operation-design-doc
description: '本番運用に必要な運用設計書を作成・更新するスキル。監視、ログ、アラート、バックアップ、障害対応、権限管理、定期作業、SLA、運用引継ぎを扱う。Use when: 運用設計書を作りたい、監視設計したい、障害対応手順を作りたい、バックアップやログ運用を整理したい、運用引継ぎしたい, operation design, runbook, monitoring, alerting, incident response.'
argument-hint: '対象システム、運用対象、非機能要件、またはリリース対象'
---

# 運用設計書作成スキル

## 目的

要件定義書（非機能要件）、基本設計書、および実装・テスト結果をもとに、本番運用に必要な運用設計を整理する。
本スキルは単なるドキュメント作成だけでなく、**「運用開始が可能であること」を証明（`docs/evidence/operation-design.evidence.json`）**し、リリース判定へ繋ぐ。

## 位置づけ

`test-execution-report` → `operation-design-doc` → `release-readiness`

## 入力として確認する情報

- 要件定義書（11章 非機能要件：可用性、性能、セキュリティ目標）
- 基本設計書（8章 非機能要件：測定方法、9章 エラー設計）
- `docs/traceability.json`（非機能要件 NFR-ID の達成状況）
- `docs/evidence/test-execution.evidence.json`（テスト結果：性能テストやセキュリティテストの Pass 状態）

## 作成手順

1. **監視・アラート設計**
   - 監視対象、閾値、アラート通知先、初動対応を定義する。

2. **Runbook（手順書）の作成**
   - 障害発生時の切り分け手順、バックアップ、リストア、定期メンテナス手順を明記する。

3. **運用テスト/リハーサルの実施**
   - 設計した手順で実際に運用（監視、復旧等）ができるかを確認する。

4. **運用エビデンス（`docs/evidence/operation-design.evidence.json`）の作成**
   - `phase` を `operation-design` に設定。
   - `artifacts` に運用設計書、Runbook のパス、`sha256` hash を含める。
   - `metrics.blockers` に「運用上の未決事項」の件数を計上する。
   - `commands[]` に運用リハーサル、監視疎通、バックアップ/リストア確認などの実行結果を記録する。

## 出力先

- 標準: `docs/07_operation-design/` 配下（プロジェクトの慣例があればそれを優先）

## 完了報告

- 運用設計書
- Runbook（運用手順書）
- 監視・アラート定義
- `docs/evidence/operation-design.evidence.json`（リリース判定の必須入力）
- 運用上の残課題
