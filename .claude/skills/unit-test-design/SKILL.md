---
name: unit-test-design
description: '基本設計書を主入力として単体テスト観点を先行設計し、実装後はコード差分から漏れを補強するスキル。Service、純粋関数、Repository mock/fake/DB込み判断、validation、例外、境界値、権限、時刻依存、Result/EitherなどをUTケースへ落とし込む。Use when: 基本設計から単体テストを設計したい、UT観点を出したい、実装前にエッジケースを洗い出したい、Serviceのテストを作りたい、実装コードからテスト漏れをレビューしたい、unit test design, unit testing, service tests.'
argument-hint: '対象Service/関数/ファイル、または関連要件ID・基本設計ID'
---

# 単体テスト設計スキル

## 目的

基本設計書を主入力として、単体テストで確認すべき観点を実装前に抽出する。
実装後はコード差分を入力として、基本設計起点のUT観点に漏れや状態更新がないかを確認する。
特に Service に置かれる基本設計の処理、関数型実装の分岐、Repository差し替え、入力検証、例外、境界値を対象にする。

## 位置づけ

`requirements-definition-doc` → `basic-design-doc` → `unit-test-design（設計先行）` → `project-coding-rules` → `implementation-coding` → `unit-test-design（差分確認）` → `test-design`

`test-design` が要件・基本設計を起点に結合/システム/受入まで見るのに対し、本スキルは基本設計を起点に単体テストへ落とす。
実装コードは正本ではなく、実装後の漏れ確認、状態更新、追加観点抽出に使う。

## 先に読む参照

- UT観点カタログ: [references/unit-test-viewpoints.md](./references/unit-test-viewpoints.md)
- Mock/Stub方針: [references/mock-guidelines.md](./references/mock-guidelines.md)
- 言語/ツール別方針: [references/tooling-guidelines.md](./references/tooling-guidelines.md)

## 入力として確認する情報

- 関連する要件ID、基本設計ID、処理フローID
- 基本設計書の画面/API/処理フロー/入力/出力/エラー/権限/状態遷移
- 対象ファイル、Service、関数、Repository
- `implementation-coding` 完了報告（実装後差分確認時のみ。変更ファイル、未実行の検証、残リスク）
- `docs/development/CODING_RULES.md`
- 既存テストの配置、命名、テストヘルパー
- テストランナー、mockライブラリ、実行コマンド

不足していても作業は進める。ただし、期待結果、エラー仕様、Repositoryの責務、外部副作用の扱いが不明な場合は確認事項として明示する。

## 実行モード

- 設計先行モード: 基本設計直後に使う。Step 1,2,4,5,6,8 を実行し、状態は原則 `設計済み` にする。実装コード、実装結果、実行結果を推測しない。
- 実装後差分確認モード: `implementation-coding` 後に使う。Step 3,7 を含め、状態を `設計済み` / `実装済み` / `実行済み` / `未実行` に更新する。

## 作成手順

1. **対象を固定する**
   - 基本設計ID、処理フローID、Service/関数/ファイル単位で対象を決める。
   - 単体テストの範囲外、結合テストに回す観点を分ける。

2. **基本設計から観点を抽出する**
   - 処理フロー、入力、戻り値、分岐、例外、Result/Either、validation、権限、状態変化を見る。
   - Repository、外部IF、時刻、UUID、random、環境変数などの副作用候補を抽出する。
   - 期待結果は基本設計ID、処理フローID、入出力定義を根拠に書く。根拠がない期待結果は断定せず、未確認事項に回す。

3. **実装後に差分確認する**
   - 実装コードは、基本設計起点のUT観点に対する漏れ、状態更新、追加分岐の確認に使う。
   - 実装コードだけを根拠に期待結果を作らない。コードと基本設計が不一致の場合は未確認事項または設計/実装不整合として明示する。

4. **依存の確認方法を決める**
   - Service UTでは Repository/外部IF/時刻/UUID/random を mock/stub/fake にする選択肢を検討する。
   - DB制約、ORM mapping、transaction、楽観ロック、外部IF接続そのものは結合テストに回す。
   - DB込みでないと有意義に確認できない観点は、UTに無理に閉じ込めず、DB込みテスト（原則として結合テスト扱い）へ回す観点として明示する。

5. **UT観点表を作る**
   - 関数、分岐、入力、mock、期待結果、優先度を整理する。
   - 正常系だけでなく、失敗系と境界値を必ず含める。
   - 観点表は機能単位、画面/API単位、Service単位、処理フローID単位でファイル分割する。複数機能を1つの巨大なMarkdown表に集約しない。

6. **UTケースへ落とす**
   - 既存テストのスタイルに合わせてテストケース名、配置、fixtureを決める。
   - Must観点からケース化する。テストコード実装まで依頼された場合は、Must観点を優先して実装し、実行できる場合のみカバレッジを確認する。

7. **網羅レビューを行う**
   - UT観点IDごとに対応するUTケース、テストコード、実行状態を確認する。
   - `設計済み` だがUTケースがない観点、`実装済み` だが未実行の観点を明示する。
   - テストコード側には、可能な範囲でUT観点IDまたはUT-IDをテスト名、コメント、describe/context名に残す。
   - 観点表にないテストは、追加観点として取り込むか、不要テスト候補として分類する。

8. **test-designへ引き継ぐ**
   - 単体で確認しない観点を結合/システム/受入の候補として明示する。
   - UT観点表テンプレートの「結合テストへ回す観点」表を、`test-design` への引き継ぎ入力として使う。

## 出力判断

- ユーザーが「観点を出して」「UT観点を整理して」と依頼した場合は、UT観点表のみを出す。
- ユーザーが「テストケースを作って」と依頼した場合は、UT観点表とUTケース表を出す。
- ユーザーが「実装方針まで」と依頼した場合は、UT観点表、UTケース表、UT実装メモを出す。
- ユーザーが「テストコードまで」と依頼した場合は、実際にテストコードも作成し、実行可否を報告する。
- 指示が曖昧な場合は、まずUT観点表を出し、UTケース表へ進めてよいか確認する。

## 優先度定義

優先度の定義は UT観点カタログ [references/unit-test-viewpoints.md](./references/unit-test-viewpoints.md) を正とする。

## 出力テンプレート

- UT観点表: [assets/templates/unit-test-viewpoints.md](./assets/templates/unit-test-viewpoints.md)
- UTケース表: [assets/templates/unit-test-cases.md](./assets/templates/unit-test-cases.md)
- UT実装メモ: [assets/templates/unit-test-implementation-note.md](./assets/templates/unit-test-implementation-note.md)

## カバーする観点

- 関数別UT観点
- Service別UT観点
- Repository mock/stub/fake/DB込み判断
- 純粋関数の境界値
- 例外/Result/Either の失敗系
- 時刻、UUID、random、外部IFの差し替え
- テスト配置、fixture、依存差し替えなどのUT実装方針
- 観点表とテストコードの対応レビュー
- 機能単位のUT観点ファイル分割

## UTと結合テストの境界

- 単体テスト: Service/関数の分岐、業務判断、validation、Repository呼び出し方。
- 結合テスト: 実DB、ORM mapping、transaction、楽観ロック、外部IFとの接続、API経由の確認。
- 迷ったら、副作用をmockして意味が保てるものはUT、副作用そのものを確認するものは結合テストにする。

## 完了報告

- 作成したUT観点/UTケース
- `traceability.json` 更新（UT-ID の追加と紐付け）
- `evidence.json`（単体テスト完了の証拠、カバレッジ等）
- 各UT観点の状態: 設計済み / 実装済み / 実行済み / 未実行
- 追加/更新すべきテストファイル
- mock/stub/fake/DB込みにした依存・理由
- 結合/システムテストに回す観点
- 未確認事項
