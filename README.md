# Obsidian Vault - 日報自動送信システム

このVaultは、Obsidianで日報を作成し、GitHub Actionsで毎日自動メール送信する仕組みです。

## ディレクトリ構成

```
obsidian-vault/
├── .github/
│   ├── workflows/              # GitHub Actions設定
│   │   └── send-daily-report.yml
│   └── scripts/                # 自動化スクリプト
│       └── send_daily_report.py  # メール送信スクリプト
├── 10_daily/                   # 日報フォルダ
│   └── YYYY/MM/                # 年/月で整理
│       └── YYYY-MM-DD.md
├── 20_poem/                    # ポエム・雑記
├── 30_tech-memo/               # 技術メモ
├── templates/                  # テンプレート
│   └── daily-template.md
└── docs/                       # ドキュメント
    ├── setup-guide.md          # 初期設定ガイド
    ├── ios-setup-guide.md      # iOSセットアップガイド
    └── usage-guide.md          # 運用ガイド
```

## クイックスタート

### Windows
1. [初期設定ガイド](docs/setup-guide.md) を読んでGitHub/Gmailの設定を行う
2. [運用ガイド](docs/usage-guide.md) を読んで日報の書き方を確認
3. Obsidianで日報を作成し、GitHubにpush

### iPhone
1. [初期設定ガイド](docs/setup-guide.md) でPATを取得
2. [iOSセットアップガイド](docs/ios-setup-guide.md) に従ってセットアップ

## 自動送信の仕様

### スケジュール
- 毎日 23:00（JST）に自動実行されます

### 送信対象
- **当日の日付のファイル** が存在する場合のみ送信
- ファイルパス: `10_daily/YYYY/MM/YYYY-MM-DD.md`
- 例: 2026年1月26日 → `10_daily/2026/01/2026-01-26.md`

### 送信方法
- Python標準ライブラリ（smtplib）で直接Gmail SMTP経由で送信
- サードパーティアクションに依存しない独自実装
- 複数の送信先がある場合、各受信者に個別送信（他の受信者のアドレスは見えません）

### スキップ条件
- 日報ファイルが存在しない場合、自動的にスキップ（エラーとして扱う）

## ドキュメント

- [初期設定ガイド](docs/setup-guide.md) - Gmail・GitHub Secrets・PATの設定
- [iOSセットアップガイド](docs/ios-setup-guide.md) - iPhoneでの詳細セットアップ手順
- [運用ガイド](docs/usage-guide.md) - 日報の書き方・Obsidian設定
