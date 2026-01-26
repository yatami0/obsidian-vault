# 初期設定ガイド

日報自動送信システムを利用するための初期設定手順です。

## システム概要

- **メール送信**: Python標準ライブラリ（smtplib）でGmail SMTP経由
- **実行環境**: GitHub Actions（Python 3.11）
- **必要な設定**: GitHub Secrets（Gmail認証情報と送信先）のみ
- **追加インストール**: 不要（Python標準ライブラリのみ使用）

## 1. Gmailアプリパスワードの取得

Gmail経由でメール送信するため、アプリパスワードを取得します。

### 1.1 2段階認証を有効化

1. [Googleアカウント](https://myaccount.google.com/) にアクセス
2. 左メニューから「セキュリティ」を選択
3. 「Googleへのログイン」セクションで「2段階認証プロセス」をクリック
4. 画面の指示に従って2段階認証を有効化

### 1.2 アプリパスワードを生成

1. [Googleアカウント](https://myaccount.google.com/) にアクセス
2. 左メニューから「セキュリティ」を選択
3. 「Googleへのログイン」セクションで「アプリパスワード」をクリック
4. アプリ名に「日報送信」などを入力
5. 「作成」をクリック
6. 表示された16文字のパスワードをコピー（スペースは除去）

> **注意**: このパスワードは一度しか表示されません。必ず安全な場所に保存してください。

## 2. GitHub Personal Access Token（PAT）の取得

iOSのObsidian Gitプラグインで認証するために必要です。

### 2.1 トークンを生成

1. [GitHub](https://github.com) にログイン
2. 右上のプロフィールアイコン → 「Settings」をクリック
3. 左メニュー下部の「Developer settings」をクリック
4. 「Personal access tokens」→「Tokens (classic)」を選択
5. 「Generate new token」→「Generate new token (classic)」をクリック

### 2.2 トークンの設定

| 項目 | 設定値 |
|------|--------|
| Note | `Obsidian Git` など分かりやすい名前 |
| Expiration | 「No expiration」または任意の期限 |
| Scopes | `repo`（フルアクセス）と `workflow` の両方にチェック |

> **重要**: `workflow`スコープがないと、GitHub Actionsのワークフローファイルをpushできません。

6. 「Generate token」をクリック
7. 表示されたトークン（`ghp_`で始まる文字列）をコピー

> **注意**: このトークンは一度しか表示されません。必ず安全な場所に保存してください。

### 2.3 Obsidian Gitに設定

Windows/iOS両方で同じ設定を行います。

1. Obsidianの設定 → コミュニティプラグイン → Obsidian Git → 設定
2. 「Authentication/Commit Author」セクションで:
   - **Username**: GitHubのユーザー名
   - **Password/Personal access token**: 手順2.2で取得したPAT

## 3. GitHub Secretsの設定（メール送信用）

リポジトリにシークレット（機密情報）を設定します。

### 3.1 Secretsページを開く

1. GitHubでこのリポジトリを開く
2. 「Settings」タブをクリック
3. 左メニューから「Secrets and variables」→「Actions」を選択

### 3.2 必要なSecretsを追加

「New repository secret」ボタンをクリックして、以下の3つを追加します。

| Name | Value | 説明 |
|------|-------|------|
| `GMAIL_USER` | your-email@gmail.com | 送信元Gmailアドレス |
| `GMAIL_APP_PASSWORD` | xxxxxxxxxxxx | 手順1.2で取得したアプリパスワード |
| `MAIL_TO` | recipient@example.com | 送信先メールアドレス |

**複数の送信先に送る場合:**

カンマ区切りで複数指定できます。**各送信先に個別送信される**ため、他の受信者のアドレスは見えません。

```
recipient1@example.com,recipient2@example.com,recipient3@example.com
```

送信の挙動:
- 各受信者に1通ずつ個別にメールが送信されます
- 他の受信者のメールアドレスは一切見えません（完全に独立した送信）
- 1件の送信が失敗しても、他の送信先への送信は継続されます

## 4. iOSでのVault設定

### 4.1 新規セットアップ（リポジトリをクローン）

1. iOSでObsidianアプリを開く
2. 「Create new vault」でVaultを作成（名前は任意）
3. コミュニティプラグインを有効化し、Obsidian Gitをインストール
4. Obsidian Git設定でUsername/PATを入力（手順2.3参照）
5. コマンドパレット（下にスワイプ）→「Obsidian Git: Clone an existing remote repo」
6. リポジトリURLを入力: `https://github.com/ユーザー名/リポジトリ名.git`

### 4.2 既存Vaultがある場合

Windowsで先にセットアップしている場合は、iOSでクローンするだけで同期できます。

## 5. 動作確認

### 5.1 手動でワークフローを実行

1. GitHubでこのリポジトリを開く
2. 「Actions」タブをクリック
3. 左メニューから「日報メール送信」を選択
4. 「Run workflow」ボタンをクリック
5. 「Run workflow」で実行

### 5.2 結果を確認

- 成功: 送信先にメールが届きます
- 失敗: エラーログを確認して設定を見直してください

よくあるエラー:
- `日報ファイルが見つかりません` → 当日の日報ファイルを作成してpushしてください
- `❌ 認証エラー: Gmail のユーザー名またはアプリパスワードが正しくありません` → アプリパスワードを確認してください
- `必要な環境変数が設定されていません` → GitHub Secretsの設定を確認してください

## 6. トラブルシューティング

### アプリパスワードが作成できない

- 2段階認証が有効になっているか確認
- 職場や学校のGoogleアカウントでは制限されている場合があります

### メールが届かない

1. 迷惑メールフォルダを確認
2. GitHub Actionsのログでエラーを確認
3. Secretsの値が正しいか確認（コピペ時の余分なスペースに注意）

### ワークフローが動かない

1. `.github/workflows/send-daily-report.yml` がmainブランチにあるか確認
2. リポジトリの Settings → Actions → General で「Allow all actions」が選択されているか確認

### iOSでpush/pullできない

1. PATの有効期限が切れていないか確認
2. PATのスコープに`repo`が含まれているか確認
3. Obsidian Git設定のUsername/PATが正しいか確認
4. リポジトリURLがHTTPS形式か確認（SSH形式は使用不可）
