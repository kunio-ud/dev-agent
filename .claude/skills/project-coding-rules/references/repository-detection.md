# リポジトリ判定

## 最初に見るファイル

| ファイル | 判定できること |
|---|---|
| `package.json` | Node.js/フロントエンド/バックエンド、scripts、依存 |
| `pnpm-workspace.yaml`, `turbo.json`, `nx.json` | monorepo |
| `pyproject.toml`, `requirements.txt`, `poetry.lock` | Python |
| `pom.xml`, `build.gradle` | Java |
| `go.mod` | Go |
| `Cargo.toml` | Rust |
| `*.csproj`, `*.sln` | .NET |
| `cdk.json` | AWS CDK |
| `main.tf`, `versions.tf` | Terraform |
| `.github/workflows/*` | CI/CD |
| `Dockerfile`, `docker-compose.yml` | コンテナ構成 |

## レイヤー判定

### フロントエンド

兆候:
- `src/components`, `src/pages`, `app`, `pages`, `vite.config.*`, `next.config.*`
- React/Vue/Angular/Svelte 依存
- Playwright/Cypress/Vitest/Jest の UI テスト

確認するルール:
- コンポーネント配置、状態管理、フォーム、API呼び出し、スタイル、アクセシビリティ。

### バックエンド/API

兆候:
- `routes`, `controllers`, `services`, `handlers`, `api`, `server`
- OpenAPI、GraphQL、REST、RPC

確認するルール:
- ルーティング、DTO/schema、バリデーション、認証認可、エラー、ログ、トランザクション。

### DB

兆候:
- `migrations`, `schema.prisma`, `models`, `entities`, `repositories`
- SQLファイル、ORM、マイグレーションツール

確認するルール:
- マイグレーション命名、ロールバック、既存データ、インデックス、トランザクション。

### バッチ/外部IF

兆候:
- `jobs`, `tasks`, `batch`, `workers`, `queues`, `cron`
- ファイル連携、SQS、EventBridge、Kafka、外部APIクライアント

確認するルール:
- 冪等性、リトライ、タイムアウト、監査ログ、異常時通知、再実行。

### IaC/CDK

兆候:
- `cdk.json`, `lib/*Stack*`, `bin/*`, `constructs`, `main.tf`

確認するルール:
- Stack/Construct分割、環境差分、命名、タグ、権限、Secret管理、変更セット確認。
