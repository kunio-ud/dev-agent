# テストケース

| TC-ID | 観点ID | 対象AC | テストレベル | 前提 | 操作/入力 | 期待結果（根拠設計ID） | テストデータ | 自動化 | 優先度 | 実装状態 | テスト関数/ファイル |
|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-USR-001 | TV-USR-001 | AC-001 | 結合 | ユーザーが認証済み | POST /users {name: "test"} | HTTP 201、users テーブルに1件追加（API-001 §3.1） | TD-001 | Yes | Must | Implemented | `tests/integration/users.test.ts#createUser_normal` |
| TC-USR-002 | TV-USR-002 | AC-001 | 結合 | DB接続エラーを注入 | POST /users | HTTP 500、DBにレコードなし（FLOW-001 §4.3） | TD-002 | Yes | Must | Pending | — |
| TC-USR-003 | TV-USR-003 | AC-002 | システム | 未認証ユーザーでブラウザ操作 | /admin にアクセス | 403 または ログイン画面へリダイレクト（SCR-USR-001 §2.1） | TD-003 | Yes | Must | Implemented | `tests/e2e/auth.spec.ts#unauthorized_redirect` |

## 除外観点

| 観点ID | 除外理由 | 代替確認方法 |
|---|---|---|
| （除外した観点があればここに記載） | | |

## テストデータ

| データID | 内容 | 使用ケース |
|---|---|---|
| TD-001 | 正常ユーザー（name: "test", role: "user"） | TC-USR-001 |
| TD-002 | DBエラー注入設定（接続プールを枯渇させる） | TC-USR-002 |
| TD-003 | 未認証セッション（Cookieなし） | TC-USR-003 |

## Must TC 実装状態サマリ

| 状態 | 件数 |
|---|---|
| Implemented | 2 |
| Pending（ブロッカー登録済み） | 1 |
| 合計 Must TC | 3 |

> Pending の TC は `docs/evidence/test-design.evidence.json` の `blocker_ids` に記録し、`metrics.blockers` に計上すること（contracts §6）。
