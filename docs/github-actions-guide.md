# GitHub Actions 自動送信ガイド

毎日23:00に日報を自動メール送信する仕組みの解説と設定手順です。

## 1. 仕組みの概要

### 全体の流れ

```
┌─────────────────────────────────────────────────────────────┐
│                        毎日の流れ                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [あなた]                                                    │
│     │                                                       │
│     │ ① 日報を書く（Obsidian）                               │
│     ▼                                                       │
│  [GitHub]                                                   │
│     │  ← Obsidian Git が自動push                            │
│     │                                                       │
│     │ ② 23:00 JST になると...                               │
│     ▼                                                       │
│  [GitHub Actions]                                           │
│     │                                                       │
│     │ ③ 当日の日報ファイルを探す                             │
│     │    10_daily/2026/01/2026-01-17-日報.md                │
│     │                                                       │
│     │ ④ ファイル内容を読み込む                               │
│     │                                                       │
│     │ ⑤ Gmailでメール送信                                   │
│     ▼                                                       │
│  [受信者]                                                    │
│     　  日報メールが届く                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 使用する技術

| 技術 | 役割 |
|------|------|
| GitHub Actions | 自動実行の基盤（無料枠: 2000分/月） |
| cron スケジュール | 毎日23:00 JSTに実行をトリガー |
| Gmail SMTP | メール送信サーバー |
| GitHub Secrets | パスワード等の機密情報を安全に保存 |

## 2. ワークフローファイルの解説

`.github/workflows/send-daily-report.yml` の中身を解説します。

### 2.1 トリガー設定

```yaml
on:
  schedule:
    # 毎日 23:00 JST（= 14:00 UTC）に実行
    - cron: '0 14 * * *'
  workflow_dispatch:
    # 手動実行も可能にする
```

| 項目 | 説明 |
|------|------|
| `schedule` | 定期実行の設定 |
| `cron: '0 14 * * *'` | UTC 14:00 = JST 23:00 に毎日実行 |
| `workflow_dispatch` | GitHubの画面から手動実行を許可 |

**cron式の読み方**: `分 時 日 月 曜日`
- `0 14 * * *` = 毎日14時0分（UTC）

### 2.2 日付とファイルパスの生成

```yaml
- name: Set date and file path
  run: |
    YEAR=$(date '+%Y')
    MONTH=$(date '+%m')
    DATE=$(date '+%Y-%m-%d')
    FILE_PATH="10_daily/${YEAR}/${MONTH}/${DATE}-日報.md"
```

実行日が2026年1月17日の場合:
- `YEAR` = `2026`
- `MONTH` = `01`
- `DATE` = `2026-01-17`
- `FILE_PATH` = `10_daily/2026/01/2026-01-17-日報.md`

### 2.3 ファイル存在チェック

```yaml
- name: Check if daily report exists
  run: |
    if [ -f "$FILE_PATH" ]; then
      echo "✅ 日報ファイルが見つかりました"
    else
      echo "❌ 日報ファイルが見つかりません"
      exit 1  # エラー終了（メール送信しない）
    fi
```

日報ファイルがない日は、エラーで終了しメールは送信されません。

### 2.4 メール送信

```yaml
- name: Send email
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 587
    username: ${{ secrets.GMAIL_USER }}
    password: ${{ secrets.GMAIL_APP_PASSWORD }}
    subject: "[日報] ${{ steps.date.outputs.date }}"
    to: ${{ secrets.MAIL_TO }}
    from: ${{ secrets.GMAIL_USER }}
    body: |
      本日の日報をお送りします。
      ─────────────────────────────
      ${{ steps.read-file.outputs.content }}
      ─────────────────────────────
```

`${{ secrets.XXX }}` はGitHub Secretsに保存した値を参照します。

## 3. 設定手順

### 3.1 Gmailアプリパスワードの取得

通常のGmailパスワードは使用できません。専用の「アプリパスワード」が必要です。

#### ステップ1: 2段階認証を有効化

1. [Googleアカウント](https://myaccount.google.com/) にアクセス
2. 左メニュー「セキュリティ」をクリック
3. 「2段階認証プロセス」をクリック
4. 画面の指示に従って有効化

#### ステップ2: アプリパスワードを生成

1. [Googleアカウント](https://myaccount.google.com/) にアクセス
2. 左メニュー「セキュリティ」をクリック
3. 「2段階認証プロセス」をクリック
4. ページ下部の「アプリパスワード」をクリック
5. アプリ名に「GitHub Actions」と入力
6. 「作成」をクリック
7. 表示された **16文字のパスワード** をコピー

```
例: abcd efgh ijkl mnop
→ スペースを除去: abcdefghijklmnop
```

> ⚠️ このパスワードは一度しか表示されません。必ず保存してください。

### 3.2 GitHub Secretsの設定

リポジトリに機密情報を安全に保存します。

#### ステップ1: Secretsページを開く

1. GitHubで [https://github.com/yatami0/obsidian-vault](https://github.com/yatami0/obsidian-vault) を開く
2. 「**Settings**」タブをクリック
3. 左メニュー「**Secrets and variables**」→「**Actions**」をクリック

#### ステップ2: Secretsを追加

「**New repository secret**」ボタンをクリックして、以下の3つを追加します。

| Name | Value | 説明 |
|------|-------|------|
| `GMAIL_USER` | `your-email@gmail.com` | 送信元のGmailアドレス |
| `GMAIL_APP_PASSWORD` | `abcdefghijklmnop` | 手順3.1で取得したアプリパスワード |
| `MAIL_TO` | `recipient@example.com` | 送信先メールアドレス |

**追加方法（各Secretごとに繰り返す）**:
1. 「New repository secret」をクリック
2. 「Name」に名前を入力（例: `GMAIL_USER`）
3. 「Secret」に値を入力（例: `your-email@gmail.com`）
4. 「Add secret」をクリック

**複数の送信先に送る場合**:
```
recipient1@example.com,recipient2@example.com
```

### 3.3 ワークフローファイルの確認

以下のファイルがリポジトリに存在することを確認:

```
.github/workflows/send-daily-report.yml
```

## 4. 動作確認

### 4.1 手動でテスト実行

1. GitHubでリポジトリを開く
2. 「**Actions**」タブをクリック
3. 左メニュー「**日報メール送信**」をクリック
4. 「**Run workflow**」ボタンをクリック
5. ブランチを選択（`main` または `develop`）
6. 「**Run workflow**」をクリック

### 4.2 実行結果の確認

実行が開始されると、ワークフローの一覧に表示されます。

| アイコン | 状態 |
|---------|------|
| 🟡 黄色の丸 | 実行中 |
| ✅ 緑のチェック | 成功 |
| ❌ 赤のバツ | 失敗 |

#### 成功した場合
- 送信先メールアドレスに日報が届きます
- 件名: `[日報] 2026-01-17`

#### 失敗した場合
1. 失敗したワークフローをクリック
2. 「send-daily-report」をクリック
3. エラーが発生したステップを確認

## 5. よくあるエラーと対処法

### 「日報ファイルが見つかりません」

**原因**: 当日の日報ファイルがリポジトリにない

**対処法**:
1. ファイル名が正しいか確認: `YYYY-MM-DD-日報.md`
2. ファイルパスが正しいか確認: `10_daily/YYYY/MM/`
3. GitHubにpushされているか確認

### 「535-5.7.8 Username and Password not accepted」

**原因**: Gmailの認証エラー

**対処法**:
1. `GMAIL_USER` が正しいGmailアドレスか確認
2. `GMAIL_APP_PASSWORD` がアプリパスワード（16文字）か確認
3. 2段階認証が有効か確認
4. スペースが含まれていないか確認

### 「Resource not accessible by integration」

**原因**: ワークフローの権限が不足

**対処法**:
1. Settings → Actions → General を開く
2. 「Workflow permissions」で「Read and write permissions」を選択
3. 「Save」をクリック

### ワークフローが一覧に表示されない

**原因**: ワークフローファイルがデフォルトブランチにない

**対処法**:
1. `.github/workflows/send-daily-report.yml` が `main` ブランチにあるか確認
2. ない場合は `develop` から `main` にマージ

## 6. 送信スケジュールの変更

### 送信時刻を変更する

`.github/workflows/send-daily-report.yml` の cron 式を変更:

```yaml
schedule:
  - cron: '0 14 * * *'  # 23:00 JST
```

| 送信時刻（JST） | cron式（UTC） |
|----------------|---------------|
| 22:00 | `0 13 * * *` |
| 23:00 | `0 14 * * *` |
| 23:30 | `30 14 * * *` |
| 0:00（翌日） | `0 15 * * *` |

### 特定の曜日のみ送信

```yaml
# 平日のみ（月〜金）
- cron: '0 14 * * 1-5'

# 週末のみ（土日）
- cron: '0 14 * * 0,6'
```

## 7. 料金について

GitHub Actionsには無料枠があります。

| プラン | 無料枠 |
|--------|--------|
| Free | 2,000分/月 |
| Pro | 3,000分/月 |

日報送信は1回あたり約1分なので、毎日実行しても月30分程度。無料枠で十分です。
