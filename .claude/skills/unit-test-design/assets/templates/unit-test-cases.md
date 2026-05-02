# Unit Test Cases

| UT-ID | UT観点ID | テスト名 | Given | When | Then | Mock/Stub/Fake/DB | 優先度 | 状態 |
|---|---|---|---|---|---|---|---|---|
| UT-001 | UTV-001 | 正常に登録できる | 必須入力が揃い、Repositoryが未登録を返す | `createUser({ name: "Taro", email: "test@example.com" })` を呼ぶ | 登録結果を返し、Repository.saveが1回呼ばれる | Repository.find: none / Repository.save: success | Must | 設計済み |
| UT-002 | UTV-002 | 必須項目未入力はエラーになる | nameが空の入力を用意する | `createUser({ name: "", email: "test@example.com" })` を呼ぶ | validation errorを返し、Repositoryは呼ばれない | Repository: not called | Must | 設計済み |
| UT-003 | UTV-003 | Repository例外を業務エラーへ変換する | Repository.saveが例外を投げる | `createUser(validInput)` を呼ぶ | 想定したResult/Either errorを返す | Repository.save: throws | Must | 設計済み |

## Fixture / Test Data

| ID | 内容 | 使用UT |
|---|---|---|
| UTF-001 | 正常系の最小入力 | UT-001 |
| UTF-002 | 必須項目が空の入力 | UT-002 |
| UTF-003 | Repository例外を発生させる入力 | UT-003 |
