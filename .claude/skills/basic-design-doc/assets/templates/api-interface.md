# インターフェース設計テンプレート（API設計方針書）

> **位置づけ**: API の**物理的な定義（パス、IO、ステータスコード）は [openapi.yaml](./openapi-template.yaml) を Single Source of Truth (SSoT) とする**。本ドキュメントは OpenAPI に書けない／書きにくい「設計方針」「採用根拠」「横断ルール」のみを扱う。
>
> **API一覧表は本ドキュメントに手書きしない。** 必要な場合は OpenAPI から自動生成する（後述「API一覧の生成」参照）。

---

## 1. API設計方針

本プロジェクトでは、API設計に **OpenAPI 3.1 (YAML)** を採用する。

| 項目 | 採用方針 |
|------|---------|
| 仕様記述 | OpenAPI 3.1 (YAML) を SSoT |
| 閲覧UI | Redoc（静的HTML生成） |
| モック | Prism / Mockoon 等（OpenAPI から自動生成） |
| 型生成 | TypeScript: `openapi-typescript` 等で自動生成 |
| Lint | Spectral でルール強制 |

### ファイル構成

| 規模 | 構成 |
|------|------|
| 小（〜30 API） | 単一 `docs/design/openapi.yaml` |
| 中・大（30 API 超） | `docs/design/openapi.yaml`（root）＋ `docs/design/api/{tag}.yaml` を `$ref` で参照 |

---

## 2. ID と OpenAPI の紐付け規則

| 識別子 | 定義場所 | 用途 |
|--------|---------|------|
| `API-XXX` | OpenAPI の `x-api-id` 拡張プロパティ | 基本設計書全体（画面設計・処理フロー・テスト）からのトレーサビリティ |
| `operationId`（キャメルケース） | OpenAPI の `operationId` | 実装側の関数名・型名・SDK生成時のシンボル |

```yaml
/auth/login:
  post:
    operationId: login          # ← 実装側で使う
    x-api-id: API-001           # ← 設計書全体からの参照ID
```

> **ルール**: 全 operation に `x-api-id` と `operationId` の両方を必ず付与する。Spectral 等の Lint で機械的に強制すること。

---

## 3. API一覧の生成（手書き禁止）

API一覧表は OpenAPI から自動生成する。**Markdown に手書きで一覧を作らないこと**（更新漏れの主原因になるため）。

### 生成方法（例）

| 用途 | コマンド例 |
|------|-----------|
| Redoc 静的HTML | `npx @redocly/cli build-docs openapi.yaml` |
| 一覧表（Markdown） | `yq` / `jq` で `paths` を抽出し表に整形（CIで生成して `docs/design/generated/api-list.md` に出力） |
| TypeScript 型 | `npx openapi-typescript openapi.yaml -o src/types/api.ts` |

> **CIで自動生成・自動コミット**するのが理想。最低でも、PR時に手元で再生成して差分が出ないことを Lint チェックする。

---

## 4. 共通仕様（OpenAPI `components` で定義）

OpenAPI の `components` セクションで一度だけ定義し、各 operation から `$ref` で参照する。本書はその設計**方針**のみ記載する（実体は YAML 側）。

### 4.1 認証

| 項目 | 方針 |
|------|------|
| 認証方式 | Bearer Token (JWT) |
| トークン有効期限 | アクセストークン 15分 / リフレッシュトークン 7日 |
| トークン取得 | `POST /auth/login`（API-001） |
| Authorization ヘッダ | `Authorization: Bearer {token}` |
| 認証不要エンドポイント | OpenAPI 側で `security: []` を明示 |

### 4.2 共通エラーレスポンス

全 4xx / 5xx で以下の構造を返す（OpenAPI の `components.schemas.ErrorResponse` で定義）：

```json
{
  "error": {
    "code": "ERR-AUTH-001",
    "message": "ユーザー向けメッセージ",
    "details": [{ "field": "loginId", "message": "必須項目です" }]
  }
}
```

- `code` は [error-design.md](./error-design.md) の `ERR-XXX` と一致させる
- `message` はユーザー向け表示文言。多言語化する場合はクライアント側で `code` から解決する

### 4.3 ページネーション

| 項目 | 方針 |
|------|------|
| 方式 | `limit` / `offset` 方式（カーソル方式は大量データAPIのみ） |
| デフォルト | `limit=20`、最大 `limit=100` |
| レスポンス | `{ items: [...], total: N, limit: 20, offset: 0 }` |

### 4.4 日付・時刻

| 項目 | 方針 |
|------|------|
| 送受信フォーマット | ISO 8601 UTC: `YYYY-MM-DDTHH:mm:ss.sssZ` |
| タイムゾーン | サーバー側は常に UTC で保管・処理。表示のみクライアント側で JST 変換 |

### 4.5 バージョニング

| 項目 | 方針 |
|------|------|
| パスバージョン | `/v1/...` 形式 |
| 破壊的変更時 | `/v2/...` を新設し、旧バージョンは最低 6 ヶ月並行稼働 |

### 4.6 レート制限・冪等性

| 項目 | 方針 |
|------|------|
| レート制限 | 認証済みユーザー: 600 req/min、未認証: 60 req/min |
| 超過時 | HTTP 429、`Retry-After` ヘッダで再開時刻を返す |
| 冪等性 | 更新系（POST/PUT/PATCH/DELETE）は `Idempotency-Key` ヘッダを許容 |

---

## 5. 設計時の意思決定ログ（Why の記録）

OpenAPI には書きにくい「なぜそう設計したか」をここに残す。

| 決定事項 | 採用案 | 棄却案 | 理由 |
|---------|-------|--------|------|
| 認証方式 | JWT | セッションCookie | モバイル／SPA両対応、ステートレスでスケール容易 |
| ページネーション | offset 方式 | カーソル方式 | 業務系で「N件目に飛ぶ」要件があるため |
| ... | ... | ... | ... |

---

## 6. 処理シーケンスとの連動

複雑な API（複数テーブル更新／外部システム連携／非同期処理）は、必ず [process-flow.md](./process-flow.md) のシーケンス図で動的振る舞いを定義する。

**シーケンス図に必ず含めること**:
- ハッピーパス
- **最低 1 つ以上の準正常系（バリデーションエラー／認可失敗／外部システムタイムアウト等）**
- データ更新がある場合のトランザクション境界

---

## チェックリスト（自己レビュー）

- [ ] OpenAPI が SSoT であり、本書には API一覧を手書きしていないか
- [ ] 全 operation に `x-api-id` と `operationId` の両方が付与されているか
- [ ] 共通エラーレスポンスが `components.schemas.ErrorResponse` として一度だけ定義されているか
- [ ] 認証・ページネーション・日付フォーマットが本書で方針化されているか
- [ ] 主要 API のシーケンス図に準正常系が含まれているか（[process-flow.md](./process-flow.md) 参照）
