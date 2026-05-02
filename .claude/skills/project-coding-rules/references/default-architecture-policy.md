# 既定アーキテクチャ方針

## 位置づけ

この方針は、プロジェクト固有の明示的な上書きがない限り採用する標準方針。
既存コードが異なる方針で統一されている場合は、既存方式を壊さず、変更方針として差分・移行要否を明記する。

## サーバーサイド

### 必須: リポジトリパターン

サーバーサイドでは、データアクセスをサービス層に直接書かず、リポジトリ層に分離する。

標準責務:

| 層 | 責務 |
|---|---|
| Controller / Handler / Route | HTTP、CLI、イベントなど入出力境界。認証済みユーザー、リクエスト、レスポンスの扱い |
| Service | 基本設計書の処理・業務ロジック・ユースケース実行 |
| Repository | DB、外部ストレージ、永続化、検索条件、トランザクション境界の補助 |
| Mapper / DTO / Schema | 入出力変換、バリデーション、型変換 |

ルール:

- Service に基本設計の処理フロー・業務判断を置く。
- Repository は業務判断を持たない。
- Controller/Handler は薄く保ち、業務判断を書かない。
- DB/ORM/SQL の詳細を Service から隠す。
- テストでは Service を中心に業務ロジックを検証し、Repository は差し替え可能にする。

## 関数型プログラミング方針

言語に関わらず、関数型プログラミング寄りに実装する。

優先する:

- 純粋関数
- 明示的な引数と戻り値
- immutable なデータ
- 副作用の局所化
- 小さな関数の合成
- 早期returnやResult型/Either型相当による明示的なエラー表現
- 依存はグローバル参照ではなく引数・ファクトリ・DIで渡す

避ける:

- 暗黙の共有状態
- グローバル mutable state
- 巨大な手続き関数
- 継承中心の設計
- 副作用が見えない helper
- テストしにくい singleton

## TypeScript / JavaScript

### 禁止

- `class`
- `this`
- class 継承
- インスタンス状態に依存する設計

### 推奨

- 関数と plain object で実装する。
- 型は `type` / `interface` で表現する。
- Service は関数として定義する。
- Repository は関数群または plain object の関数プロパティとして定義する。
- 依存は factory 関数で注入する。

例:

```ts
type UserRepository = {
  findById: (id: string) => Promise<User | null>;
};

type CreateUserServiceDeps = {
  userRepository: UserRepository;
};

export const createUserService = ({ userRepository }: CreateUserServiceDeps) => ({
  getUser: async (id: string) => {
    const user = await userRepository.findById(id);
    if (!user) return { ok: false as const, error: "USER_NOT_FOUND" };
    return { ok: true as const, value: user };
  },
});
```

## 例外

以下は例外として許容するが、理由をコーディングルールに明記する。

- フレームワークが class を強制する場合。
- ORM、CDK、テストフレームワークなど外部APIが class 前提の場合。
- 既存コードが class ベースで統一され、局所変更での混在が危険な場合。

例外時も、業務ロジックは可能な限り関数として切り出す。
