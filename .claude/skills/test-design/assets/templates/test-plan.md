# テスト計画

## 1. 対象

| 項目 | 内容 |
|---|---|
| 対象機能 |  |
| 対象要件 |  |
| 対象設計 |  |
| 対象外 |  |

## 2. テスト方針

- 観点表を先に作成し、Must/高リスク観点からテストケース化する。
- 自動化可能な回帰観点は自動化する。
- 受入条件（AC-）に直結する観点は受入テストとして明示する。
- Must TC は test-design evidence が Completed になる前に全て実装済みにする（contracts §6）。未実装の Must TC は blocker_ids に記録し metrics.blockers に計上する。

## 3. テストレベル別範囲

| レベル | 対象 | 実施方法 | 自動化 |
|---|---|---|---|
| 単体 |  |  |  |
| 結合 |  |  |  |
| システム |  |  |  |
| 受入 |  |  |  |
| 性能 |  |  |  |
| セキュリティ |  |  |  |

## 4. Must TC 実装状態サマリ

| 状態 | 件数 |
|---|---|
| Implemented |  |
| Pending（ブロッカー登録済み） |  |
| 合計 Must TC |  |

## 5. トレーサビリティ

| 受入条件ID | 要件ID | 設計ID | 観点ID | TC-ID |
|---|---|---|---|---|
| AC-001 | FR-001 | API-001 | TV-USR-001 | TC-USR-001 |

## 6. リスク一覧

| RSK-ID | 内容 | 影響 | 対応方針 |
|---|---|---|---|
| RSK-001 |  |  |  |

## 7. 未確認事項（TBD）

| TBD-ID | 内容 | 確認先 | 影響 | 状態 | resolved_at | resolution |
|---|---|---|---|---|---|---|
| TBD-001 |  |  |  | Proposed |  |  |

> 未解消の TBD はすべて blocker として evidence の blocker_ids に追加すること（contracts §7）。
> TBD 解消時は resolved_at（ISO 8601）と resolution を記入し、evidence の notes に "TBD-NNN resolved: <解消内容>" を記録する。

## 8. 検証コマンド実行結果

```sh
python scripts/validate_traceability.py docs/traceability.json
python scripts/validate_evidence.py docs/evidence/test-design.evidence.json
```

| コマンド | 実行日時 | exit_code | 結果 |
|---|---|---|---|
| validate_traceability.py |  |  |  |
| validate_evidence.py |  |  |  |
