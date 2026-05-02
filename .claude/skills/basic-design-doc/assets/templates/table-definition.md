# テーブル定義テンプレート

## テーブル一覧

| No. | テーブル論理名 | テーブル物理名 | 概要 |
|-----|--------------|--------------|------|
| 1 | ユーザーマスタ | m_users | システム利用ユーザーを管理する |
| 2 | 〇〇トランザクション | t_xxxx | 〇〇の処理履歴を記録する |

---

## {{テーブル論理名}}（{{テーブル物理名}}）

### テーブル概要

| 項目 | 内容 |
|------|------|
| テーブル論理名 | ユーザーマスタ |
| テーブル物理名 | m_users |
| スキーマ | public |
| エンジン / 文字コード | InnoDB / utf8mb4 |
| 概要 | システム利用ユーザーの認証情報・プロフィールを管理する |
| 備考 | 論理削除方式（deleted_at で管理） |

---

### カラム定義

| No. | 論理名 | 物理名 | データ型 | 桁数 | NOT NULL | PK | FK | デフォルト | 備考 |
|-----|--------|--------|----------|------|----------|----|----|------------|------|
| 1 | ユーザーID | user_id | BIGINT | - | ○ | ○ | - | AUTO_INCREMENT | サロゲートキー |
| 2 | メールアドレス | email | VARCHAR | 255 | ○ | - | - | - | ユニーク制約あり |
| 3 | パスワードハッシュ | password_hash | VARCHAR | 255 | ○ | - | - | - | bcrypt ハッシュ |
| 4 | 表示名 | display_name | VARCHAR | 100 | ○ | - | - | - | |
| 5 | ロール | role | ENUM | - | ○ | - | - | 'user' | 'admin','user','readonly' |
| 6 | 最終ログイン日時 | last_login_at | DATETIME | - | - | - | - | NULL | |
| 7 | 作成日時 | created_at | DATETIME | - | ○ | - | - | CURRENT_TIMESTAMP | |
| 8 | 更新日時 | updated_at | DATETIME | - | ○ | - | - | CURRENT_TIMESTAMP ON UPDATE | |
| 9 | 削除日時 | deleted_at | DATETIME | - | - | - | - | NULL | NULL = 有効レコード |

---

### インデックス定義

| インデックス名 | 種別 | 対象カラム | 目的 |
|--------------|------|-----------|------|
| PRIMARY | PRIMARY KEY | user_id | 主キー |
| uq_users_email | UNIQUE | email | メールアドレス重複防止 |
| idx_users_role | INDEX | role | ロール別検索の高速化 |
| idx_users_deleted_at | INDEX | deleted_at | 有効レコード絞り込みの高速化 |

---

### 外部キー定義

| FK名 | 本テーブルカラム | 参照テーブル | 参照カラム | ON DELETE | ON UPDATE |
|------|----------------|------------|----------|-----------|-----------|
| fk_orders_user_id | user_id | m_users | user_id | RESTRICT | CASCADE |

---

### DDL（参考）

```sql
CREATE TABLE m_users (
    user_id      BIGINT       NOT NULL AUTO_INCREMENT,
    email        VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    role         ENUM('admin','user','readonly') NOT NULL DEFAULT 'user',
    last_login_at DATETIME    NULL,
    created_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at   DATETIME     NULL,
    PRIMARY KEY (user_id),
    UNIQUE KEY uq_users_email (email),
    KEY idx_users_role (role),
    KEY idx_users_deleted_at (deleted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='ユーザーマスタ';
```

---

### CRUD マトリクス

| 機能ID | 画面ID | API-ID | 機能 / 画面 | SELECT | INSERT | UPDATE | DELETE |
|--------|--------|--------|-----------|--------|--------|--------|--------|
| FR-010 | SCR-USR-001 | API-010 | ユーザー一覧画面 | ○ | - | - | - |
| FR-011 | SCR-USR-002 | API-011 | ユーザー登録画面 | - | ○ | - | - |
| FR-012 | SCR-USR-003 | API-012 | ユーザー編集画面 | ○ | - | ○ | - |
| FR-013 | SCR-USR-003 | API-013 | ユーザー削除（論理） | - | - | ○（deleted_at 更新） | - |
| FR-001 | SCR-AUTH-001 | API-001 | ログイン処理 | ○ | - | ○（last_login_at 更新） | - |
