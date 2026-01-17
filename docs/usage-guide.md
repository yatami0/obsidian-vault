# 運用ガイド

Obsidianで日報を作成し、自動送信するまでの日々の運用方法です。

## 1. 日報の書き方

### 1.1 ファイル命名規則

日報ファイルは以下の形式で作成します。

```
10_daily/YYYY/MM/YYYY-MM-DD-日報.md
```

例: 2026年1月17日の日報
```
10_daily/2026/01/2026-01-17-日報.md
```

### 1.2 日報テンプレート

`templates/daily-template.md` を使用します。

```markdown
# YYYY-MM-DD 日報

## やったこと
-

## 学び・気づき
-

## 明日やること
-

## メモ

```

## 2. Obsidianの推奨設定

### 2.1 Templaterプラグイン（推奨）

テンプレートから自動的に日報を作成できます。

1. 設定 → コミュニティプラグイン → Templater をインストール
2. Templaterの設定:
   - Template folder location: `templates`
   - 日付形式を設定

### 2.2 Daily Notesプラグイン（代替）

Obsidian標準のDaily Notesでも運用可能です。

1. 設定 → コアプラグイン → Daily Notes を有効化
2. 設定:
   - New file location: `10_daily/{{date:YYYY}}/{{date:MM}}`
   - Template file location: `templates/daily-template`
   - Date format: `YYYY-MM-DD-日報`

### 2.3 Obsidian Gitプラグイン（Windows/iOS共通）

自動的にGitHubへpushできます。Windows・iOS両方で動作します。

#### インストール

1. 設定 → コミュニティプラグイン → Obsidian Git をインストール

#### 推奨設定

| 設定項目 | 値 | 説明 |
|---------|-----|------|
| Auto pull interval | 10分 | 自動的にリモートから取得 |
| Auto push interval | 10分 | 自動的にリモートへ送信 |
| Auto commit interval | 10分 | 自動的にコミット作成 |

#### 認証設定（重要）

iOSで使用するには **Personal Access Token（PAT）** が必要です。

1. [初期設定ガイド](setup-guide.md) の「GitHub Personal Access Token」セクションを参照
2. Obsidian Git設定画面で:
   - Authentication/Commit Author → Username: GitHubユーザー名
   - Authentication/Commit Author → Password/Personal access token: 取得したPAT

#### iOS固有の注意点

- **SSH認証は使用不可** → HTTPS + PAT を使用してください
- 大きなリポジトリでは動作が不安定になる場合があります
- 初回クローンは時間がかかることがあります

## 3. 日々のワークフロー

### 毎日の流れ

```
1. Obsidianを開く（自動でpull）
2. 新しい日報ファイルを作成（Templaterまたは手動）
3. 日報を記入
4. 保存（Obsidian Gitで自動push）
5. 23:00に自動でメール送信
```

### 手動でGitHubにpushする場合（Windows）

```bash
cd /path/to/obsidian-vault
git add .
git commit -m "日報 YYYY-MM-DD"
git push
```

## 4. フォルダの使い分け

| フォルダ | 用途 | 例 |
|---------|------|-----|
| `10_daily/` | 日報 | 毎日の業務報告 |
| `20_poem/` | ポエム・雑記 | 思いついたこと、アイデア |
| `30_tech-memo/` | 技術メモ | 調べたこと、手順書 |

## 5. 注意事項

### 日報が送信されない場合

- ファイル名が正しい形式か確認: `YYYY-MM-DD-日報.md`
- ファイルパスが正しいか確認: `10_daily/YYYY/MM/`
- GitHubにpushされているか確認

### 23:00までにpushする

自動送信は毎日23:00（JST）に実行されます。それまでに日報をGitHubにpushしてください。

### 機密情報に注意

日報はGitHubリポジトリに保存されます。プライベートリポジトリでも、機密性の高い情報（パスワード、個人情報など）は記載しないでください。

### 同期の競合が発生した場合

Windows/iPhoneで同時に編集すると競合が発生することがあります。

1. 片方のデバイスで編集を完了してからもう一方を開く
2. 競合ファイルが生成された場合は手動でマージ
