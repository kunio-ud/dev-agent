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
| 非機能要件 | `NFR-{分類}-` | `requirements-definition-doc` |
| 受入条件 | `AC-` | `requirements-definition-doc` |
| 画面要件 | `SCRR-` | `requirements-definition-doc` |
| 帳票要件 | `RPT-` | `requirements-definition-doc` |
| 通知要件 | `NTF-` | `requirements-definition-doc` |
| バッチ要件 | `BAT-` | `requirements-definition-doc` |
| データ要件 | `DR-` | `requirements-definition-doc` |
| 外部連携要件 | `IR-` | `requirements-definition-doc` |
| 移行要件 | `MIG-` | `requirements-definition-doc` |
| 制約 | `CON-` | `requirements-definition-doc` |
| 画面設計 | `SCR-{モジュール}-` | `basic-design-doc` |
| API設計 | `API-` | `basic-design-doc` |
| テーブル定義 | `TBL-` | `basic-design-doc` |
| 処理フロー | `FLOW-` | `basic-design-doc` |
| エラーコード | `ERR-{分類}-` | `basic-design-doc` |
| 単体テスト観点 | `UTV-` | `unit-test-design` |
| 単体テストケース | `UT-` | `unit-test-design` |
| テスト観点 | `TV-` | `test-design` |
| テストケース | `TC-` | `test-design` / `unit-test-design` |
| テストデータ | `TD-` / `UTF-` | `test-design` / `unit-test-design` |
| 未決事項 | `TBD-` | 各エージェント（発見者） |
| リスク | `RSK-` | 各エージェント（発見者） |

## 3. エージェント間インターフェース（Artifacts）

### 3.1 Traceability (traceability.json)
- **役割**: 要件からテスト結果までのライフサイクル全域の紐付けを管理する。
- **更新タイミング**: 要件定義、基本設計、単体テスト設計、実装、テスト設計の各完了時。
- **スキーマ**: `schemas/traceability.schema.json`

### 3.2 Evidence (evidence.json)
- **役割**: 各フェーズの「完了の証明」を格納する。
- **配置**: 原則 `docs/evidence/{phase}.evidence.json`。単一ファイルに集約する場合はフェーズごとの packet を失わない形式にする。
- **更新タイミング**: 各スキルの完了報告時。
- **スキーマ**: `schemas/evidence.schema.json`
- **主要項目**: `metrics.blockers`、`blocker_ids`、テスト成功数、カバレッジ、`commands[]`、成果物 `artifacts[]` の sha256 hash。

## 4. フェーズゲート判定プロトコル
`waterfall-delivery-cycle`（オーケストレーター）は、以下の手順でフェーズ移行を判定する。

1. **形式チェック**: `docs/traceability.json` および `docs/evidence/{phase}.evidence.json` がスキーマに適合しているか。
2. **論理チェック**: 
   - 前工程の ID がすべて次工程の ID にマップされているか。
   - 各フェーズの `docs/evidence/{phase}.evidence.json` の `metrics.blockers` が 0 件であるか。
   - `blocker_ids` が空であるか。
   - 必須の成果物（Markdown, OpenAPI等）が存在し、`artifacts[].hash` が実ファイルの sha256 と一致するか。
   - `commands[]` の必須検証コマンドが `status: Pass` かつ `exit_code: 0` であるか。
3. **Go/No-Go 判定**: 上記がすべて Pass した場合のみ次工程を起動する。

## 5. ドキュメント同期ルール
- Markdown は **JSON から生成されるビュー** である。
- エージェントはまず JSON を更新し、その後に Markdown の表を同期させなければならない。
- 人間による修正が Markdown に入った場合、オーケストレーターは JSON との乖離（Drift）を検知し、エージェントに同期を促す。

## 6. テストケース表（TC）の記載ルール

- TC 表の各行は、実際に存在するテスト関数またはスクリプトに対応していなければならない。
- 「代替済み」「省略」「他ケースで代替」などのメモ行は TC 表に含めない。代替・除外の記録は「除外観点」節（別セクション）に移す。
- Must 優先度の TC は test-design フェーズの evidence が Completed になる前に全て実装済みでなければならない。
  「未実装 → Phase X」は Must TC には禁止。Must TC を後フェーズに送る場合は blocker として記録し、`metrics.blockers > 0` とする。
- Should/Nice 優先度の TC は未実装のまま次フェーズへ送ることができるが、traceability.json に状態 `Pending` で残し、release-readiness で判断する。

## 7. TBD 解消トラッキングルール

- TBD が `Proposed` から `Resolved` になる場合、そのフェーズの evidence.json の `notes` フィールドに `"TBD-NNN resolved: <解消内容>"` を記録する。
- traceability.json の該当 TBD の `status` を `Resolved` に更新する際、`resolved_at`（ISO 8601）と `resolution`（解消内容の要約）フィールドを付与する。
- TBD が Resolved にならないまま次フェーズの evidence が Completed になってはならない。
  未解消 TBD はブロッカー相当（`blocker_ids` に追加し `metrics.blockers` に計上）として扱う。

## 8. 検証スクリプト
- `scripts/validate_traceability.py <traceability.json>` で ID 形式、重複、リンク参照の存在、AC から TC への到達性を検証する。
- `scripts/validate_evidence.py <evidence.json>` で schema、artifact hash、blocker 件数、command 結果を検証する。
- JSON Schema は構造の最低限を担保する。ID 参照整合性とファイル hash は必ず検証スクリプトで確認する。
