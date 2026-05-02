# エージェント間連携契約（Waterfall Contracts）

## 1. 目的
本ドキュメントは、ウォーターフォール開発サイクルにおける各特化型エージェント（スキル）間のデータ交換プロトコルを定義する。
自然言語（Markdown）による曖昧な引継ぎを廃し、構造化データ（JSON）を「正本」とすることで、自律的なフェーズゲート判定とトレーサビリティを維持する。

## 2. 共通ID体系（Master ID System）
全エージェントは以下のID体系を厳守しなければならない。

| 種別 | プレフィックス | 定義主体（エージェント） |
|---|---|---|
| 業務要件 | `BR-` | `requirements-definition-doc` |
| 機能要件 | `FR-` | `requirements-definition-doc` |
| 非機能要件 | `NFR-` | `requirements-definition-doc` |
| 受入条件 | `AC-` | `requirements-definition-doc` |
| 画面設計 | `SCR-` | `basic-design-doc` |
| API設計 | `API-` | `basic-design-doc` |
| テーブル定義 | `TBL-` | `basic-design-doc` |
| 処理フロー | `FLOW-` | `basic-design-doc` |
| 単体テスト観点 | `UT-` | `unit-test-design` |
| テスト観点 | `TV-` | `test-design` |
| テストケース | `TC-` | `test-design` / `unit-test-design` |
| 未決事項 | `TBD-` | 各エージェント（発見者） |
| リスク | `RSK-` | 各エージェント（発見者） |

## 3. エージェント間インターフェース（Artifacts）

### 3.1 Traceability (traceability.json)
- **役割**: 要件からテスト結果までのライフサイクル全域の紐付けを管理する。
- **更新タイミング**: 要件定義、基本設計、単体テスト設計、実装、テスト設計の各完了時。
- **スキーマ**: `schemas/traceability.schema.json`

### 3.2 Evidence (evidence.json)
- **役割**: 各フェーズの「完了の証明」を格納する。
- **更新タイミング**: 各スキルの完了報告時。
- **スキーマ**: `schemas/evidence.schema.json`
- **主要項目**: BLOCKER件数、テスト成功数、カバレッジ、検証コマンド、成果物ハッシュ。

## 4. フェーズゲート判定プロトコル
`waterfall-delivery-cycle`（オーケストレーター）は、以下の手順でフェーズ移行を判定する。

1. **形式チェック**: `traceability.json` および `evidence.json` がスキーマに適合しているか。
2. **論理チェック**: 
   - 前工程の ID がすべて次工程の ID にマップされているか。
   - `evidence.json` の `blockers` が 0 件であるか。
   - 必須の成果物（Markdown, OpenAPI等）が存在するか。
3. **Go/No-Go 判定**: 上記がすべて Pass した場合のみ次工程を起動する。

## 5. ドキュメント同期ルール
- Markdown は **JSON から生成されるビュー** である。
- エージェントはまず JSON を更新し、その後に Markdown の表を同期させなければならない。
- 人間による修正が Markdown に入った場合、オーケストレーターは JSON との乖離（Drift）を検知し、エージェントに同期を促す。
