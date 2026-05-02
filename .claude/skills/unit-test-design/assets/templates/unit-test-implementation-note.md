# Unit Test Implementation Note

## テスト配置

| 項目 | 内容 |
|---|---|
| テストランナー |  |
| テストファイル |  |
| 実行コマンド |  |
| 依存差し替え/DB利用方針 |  |

## 依存差し替え

| 依存 | 差し替え方法 | 理由 |
|---|---|---|
| Repository | mock/stub/fake/DB込み | Serviceの業務判断、状態変化、DB制約/ORM mappingのどれを確認するかで選ぶため |
| now/UUID/random | stub | テストを安定させるため |

## テストコード作成方針

- UTはServiceまたは純粋関数単位でファイルを分ける。
- fixtureは既存規約を優先し、共通化しすぎず各テストのGivenが読める粒度にする。
- Repository、外部IF、時刻、UUID、randomは依存注入で差し替える。DB制約やORM mappingが品質リスクの場合はDB込みテスト（原則として結合テスト扱い）として明示する。

## 未確認事項

| ID | 内容 | 影響 |
|---|---|---|
| TBD-001 |  |  |
