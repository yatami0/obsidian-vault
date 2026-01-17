# Obsidian Vault - 日報自動送信システム

このVaultは、Obsidianで日報を作成し、GitHub Actionsで毎日自動メール送信する仕組みです。

## ディレクトリ構成

```
obsidian-vault/
├── .github/workflows/     # GitHub Actions設定
│   └── send-daily-report.yml
├── 10_daily/              # 日報フォルダ
│   └── YYYY/MM/           # 年/月で整理
│       └── YYYY-MM-DD-日報.md
├── 20_poem/               # ポエム・雑記
├── 30_tech-memo/          # 技術メモ
├── templates/             # テンプレート
│   └── daily-template.md
└── docs/                  # ドキュメント
    ├── setup-guide.md     # 初期設定ガイド
    ├── ios-setup-guide.md # iOSセットアップガイド
    ├── github-actions-guide.md # GitHub Actions解説
    └── usage-guide.md     # 運用ガイド
```

## クイックスタート

### Windows
1. [初期設定ガイド](docs/setup-guide.md) を読んでGitHub/Gmailの設定を行う
2. [運用ガイド](docs/usage-guide.md) を読んで日報の書き方を確認
3. Obsidianで日報を作成し、GitHubにpush

### iPhone
1. [初期設定ガイド](docs/setup-guide.md) でPATを取得
2. [iOSセットアップガイド](docs/ios-setup-guide.md) に従ってセットアップ

## 自動送信スケジュール

- 毎日 23:00（JST）に当日の日報がメール送信されます
- 日報ファイルがない日はスキップされます

## ドキュメント

- [初期設定ガイド](docs/setup-guide.md) - Gmail・GitHub Secrets・PATの設定
- [iOSセットアップガイド](docs/ios-setup-guide.md) - iPhoneでの詳細セットアップ手順
- [GitHub Actions解説](docs/github-actions-guide.md) - 自動送信の仕組みと設定手順
- [運用ガイド](docs/usage-guide.md) - 日報の書き方・Obsidian設定
