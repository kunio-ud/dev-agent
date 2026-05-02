# Mock / Stub / Fake 方針

## 原則

- Service UTでは、Repository、外部IF、時刻、UUID、random、メール/通知を差し替えるか、fake/DB込みにするかを目的に応じて選ぶ。
- mockは「何回呼ばれたか」より「期待する業務結果」を優先する。
- 呼び出し検証は、重要な副作用や永続化がある場合に限定する。
- DB制約、ORM mapping、transaction、外部キー制約を検出したい場合は、mockに閉じずDB込みテスト（原則として結合テスト扱い）へ回す。

## 使い分け

| 種類 | 用途 |
|---|---|
| Mock | 呼び出し有無、引数、副作用を検証する |
| Stub | 固定の戻り値を返す |
| Fake | 軽量な実装で状態を持たせる。Serviceが同一Repositoryを複数回呼ぶ場合に、インメモリで状態を表現する |
| Spy | 実装を使いながら呼び出しを観測する |

## Repository mock / fake / DB込み判断

業務分岐だけを確認したい場合は mock/stub を使う。Serviceが同一Repositoryを複数回呼び、状態変化を見たい場合は fake を使う。DB制約やORM mappingが品質リスクの場合は、DB込みテスト（原則として結合テスト扱い）へ回す。

mock/stubで最低限用意する戻り値:

- 正常に1件返る。
- 見つからない。
- 空配列。
- 重複が見つかる。
- Repositoryが例外を投げる。

## 外部IF mock

最低限用意する戻り値:

- 成功。
- timeout。
- 4xx相当。
- 5xx相当。
- retry後成功。
- retry上限超過。

retry制御がServiceにある場合は、Service UTでretry回数、最終結果、エラー変換を確認する。
retry制御が外部IFラッパーに閉じている場合は、Service UTではラッパーの戻り値だけをstubし、retry詳細はラッパー側のUTまたは結合テストへ分ける。

## 避けること

- 実装詳細に密着しすぎたmock。
- すべての内部関数呼び出しを検証するテスト。
- テストの目的に合わない場面でDBや外部APIを直接使うこと。
- ランダム値や現在時刻に依存した不安定なテスト。
