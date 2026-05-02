# テスト観点表

| 観点ID | 入力根拠 | 対象要件 | 対象AC | 対象設計 | 観点 | リスク | RSK-ID | テストレベル | 自動化 | 優先度 | 状態 | TBD-ID | 備考 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TV-USR-001 | 要件定義 | FR-001 | AC-001 | API-001 | 正常に登録できる | 高 | RSK-001 | 結合 | Yes | Must | Designed | | |
| TV-USR-002 | 基本設計 | FR-001 | AC-001 | FLOW-001 | 例外時にロールバックされる | 高 | RSK-001 | 結合 | Yes | Must | Designed | | |
| TV-USR-003 | 非機能 | NFR-SEC-001 | AC-002 | SCR-USR-001 | 権限なしユーザーが操作できない | 高 | RSK-002 | システム | Yes | Must | Designed | | |
| TV-MIG-001 | 要件定義 | MIG-001 | AC-003 | FLOW-002 | 移行後のデータ整合性が正しい | 高 | RSK-003 | システム | No | Must | Designed | TBD-001 | 移行ツール仕様確認待ち |

## RSK-ID 採番ルール

- リスク=**高** の観点は必ず `RSK-NNN` を採番し、test-plan §6 のリスク一覧と一致させる。
- リスク=中/低 はプロジェクト判断で採番可。採番しない場合は RSK-ID 列を空欄のままにする。

## 状態定義

| 状態 | 意味 |
|---|---|
| Designed | 観点のみ定義済み。テストケース/テストコード未作成 |
| Implemented | 対応するテスト関数またはスクリプトが実装済み |
| Executed | テスト実行済み（Pass/Fail は test-execution-report で記録） |

## 優先度定義（contracts §6 参照）

| 優先度 | 意味 | Must TC の制約 |
|---|---|---|
| Must | リリース/検収に必須 | test-design evidence Completed までに Implemented 必須 |
| Should | 重要。後続対応可 | status=Pending で次フェーズへ送ることができる |
| Could | 余力があれば確認 | status=Pending で次フェーズへ送ることができる |
