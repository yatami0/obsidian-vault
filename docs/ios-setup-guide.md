# iOS セットアップガイド

iPhoneでObsidian Gitを使用して、Windows PCと日報を同期する手順です。

## 前提条件

- GitHubアカウントを持っている
- Personal Access Token（PAT）を取得済み（[初期設定ガイド](setup-guide.md)のセクション2参照）
- Windows PCでリポジトリをGitHubにpush済み

## 1. Obsidianアプリのインストール

1. App Storeを開く
2. 「Obsidian」で検索
3. 「Obsidian - Connected Notes」をインストール（無料）

## 2. Vaultの作成

1. Obsidianアプリを開く
2. 「Create new vault」をタップ
3. Vault name: 任意の名前（例: `daily-notes`）
4. 「Store in iCloud」は**オフ**にする（Gitで管理するため）
5. 「Create」をタップ

## 3. コミュニティプラグインの有効化

1. 左下の歯車アイコン（設定）をタップ
2. 「Community plugins」をタップ
3. 「Restricted mode」の「Turn on community plugins」をタップ
4. 警告が表示されたら「Turn on community plugins」をタップ

## 4. Obsidian Gitプラグインのインストール

1. 「Community plugins」画面で「Browse」をタップ
2. 検索欄に「Obsidian Git」と入力
3. 「Obsidian Git」（作者: Vinzent03）をタップ
4. 「Install」をタップ
5. インストール完了後「Enable」をタップ

## 5. Obsidian Gitの設定

### 5.1 設定画面を開く

1. 設定画面に戻る
2. 左メニューを下にスクロール
3. 「Community plugins」セクションの「Obsidian Git」をタップ

### 5.2 認証情報の設定

「Authentication/Commit Author」セクションで以下を入力:

| 項目 | 入力値 |
|------|--------|
| Username | GitHubのユーザー名（例: `yatami0`） |
| Password/Personal access token | 取得したPAT（`ghp_`で始まる文字列） |
| Author name | コミットに表示する名前（任意） |
| Author email | GitHubに登録したメールアドレス |

### 5.3 自動同期の設定

「Automatic」セクションで以下を設定:

| 項目 | 推奨値 | 説明 |
|------|--------|------|
| Split automatic commit and push | オン | コミットとプッシュを分離 |
| Vault backup interval (minutes) | 10 | 自動コミット間隔 |
| Auto pull interval (minutes) | 10 | 自動プル間隔 |
| Auto push interval (minutes) | 10 | 自動プッシュ間隔 |
| Commit message | `auto: {{date}}` | コミットメッセージ形式 |
| Pull updates on startup | オン | 起動時に自動プル |
| Push on backup | オン | バックアップ時にプッシュ |

## 6. リポジトリのクローン

### 6.1 コマンドパレットを開く

1. 設定画面を閉じる（左上の×または画面外をタップ）
2. 画面を**下にスワイプ**してコマンドパレットを開く

### 6.2 クローンコマンドを実行

1. 検索欄に「clone」と入力
2. 「Obsidian Git: Clone an existing remote repo」をタップ

### 6.3 リポジトリURLを入力

ダイアログが表示されます:
```
Enter remote URL
```

1. 以下の形式でURLを入力:
   ```
   https://github.com/yatami0/obsidian-vault.git
   ```
   （自分のリポジトリURLに置き換えてください）
2. 「OK」をタップ

### 6.4 クローン先ディレクトリを選択

次のダイアログが表示されます:
```
Enter directory for clone. It needs to be empty or not existent.
```

**2つの選択肢があります:**

#### 選択肢A: Vault直下にクローン（推奨）

1. 入力欄を**空のまま**にする、または `.` （ドット）を入力
2. 「OK」をタップ

→ リポジトリの内容がVaultのルートに直接展開されます

### 6.5 .obsidianフォルダの確認ダイアログ

選択肢Aを選ぶと、次の警告が表示されます:

```
DELETE ALL YOUR LOCAL CONFIG AND PLUGINS?

To avoid conflicts, the local .obsidian directory needs to be deleted.
This will delete all local config and plugins, but they will be restored from the remote repo.
```

**意味**: 競合を避けるため、ローカルの設定（.obsidianフォルダ）を削除してリポジトリの設定で上書きします。

**選択:**

| ボタン | 動作 | いつ選ぶか |
|--------|------|-----------|
| **Yes（推奨）** | ローカルの設定を削除し、リポジトリの設定を使用 | 通常はこちら |
| No | ローカルの設定を保持 | ローカル設定を残したい場合 |

> **注意**: 「Yes」を選ぶと、先ほど設定したObsidian Gitの認証情報（PAT）も削除されます。クローン完了後に**再度認証情報を設定**する必要があります（セクション5.2参照）。

#### 選択肢B: サブフォルダにクローン

1. フォルダ名を入力（例: `my-notes`）
2. 「OK」をタップ

→ Vault内に `my-notes` フォルダが作成され、その中にクローンされます

> **推奨**: 選択肢A（空欄または `.`）を選んでください。Vault全体をリポジトリとして管理できます。

### 6.6 Depthの設定（オプション）

次のダイアログが表示される場合があります:
```
Depth: Specify the number of commits to include. Leave empty for full history.
```

1. **空欄のまま**「OK」をタップ（フル履歴をクローン）
   - または `1` を入力（最新コミットのみ、高速だが履歴なし）

### 6.7 クローンの実行と完了

1. クローンが開始されます
2. 右上に進行状況が表示されます:
   ```
   Cloning from https://github.com/...
   ```
3. 完了すると以下のメッセージが表示されます:
   ```
   Cloned repository. You may need to reload the plugin.
   ```

### 6.8 Obsidianを再起動

**重要**: クローン後は必ず再起動が必要です。

1. Obsidianアプリを完全に終了する
   - iPhoneのアプリスイッチャーを開く（下から上にスワイプして止める）
   - Obsidianを上にスワイプして終了
2. Obsidianを再度開く

または、アプリ内で再読み込み:
1. コマンドパレットを開く（下にスワイプ）
2. 「Reload app without saving」と入力して実行

### 6.9 認証情報を再設定（重要）

「Yes」を選んで.obsidianを削除した場合、認証情報も消えています。

1. 設定（歯車アイコン）を開く
2. Community plugins → Obsidian Git をタップ
3. 「Authentication/Commit Author」セクションで再入力:
   - **Username**: GitHubのユーザー名
   - **Password/Personal access token**: PAT（`ghp_`で始まる文字列）

## 7. 動作確認

### 7.1 ファイルが同期されているか確認

1. 左サイドバーを開く（左端からスワイプ）
2. `10_daily/`フォルダが表示されていることを確認
3. 既存の日報ファイルが表示されていることを確認

### 7.2 手動で同期をテスト

1. コマンドパレットを開く（下にスワイプ）
2. 「Obsidian Git: Pull」を実行 → 最新の変更を取得
3. 何かファイルを編集
4. 「Obsidian Git: Commit all changes」を実行
5. 「Obsidian Git: Push」を実行
6. GitHubで変更が反映されているか確認

## 8. 日々の使い方

### 基本操作

| 操作 | 方法 |
|------|------|
| コマンドパレットを開く | 画面を下にスワイプ |
| 手動でプル | コマンドパレット → 「Git: Pull」 |
| 手動でプッシュ | コマンドパレット → 「Git: Push」 |
| 変更をコミット | コマンドパレット → 「Git: Commit」 |

### 推奨ワークフロー

```
1. Obsidianを開く（自動でpull）
2. 日報を作成・編集
3. アプリを閉じる or バックグラウンドに移動
   → 自動でcommit & push
```

## 9. トラブルシューティング

### クローンが失敗する

**エラー**: `Authentication failed`
- PATが正しく入力されているか確認
- PATに`repo`と`workflow`スコープがあるか確認
- PATの有効期限が切れていないか確認

**エラー**: `Repository not found`
- リポジトリURLが正しいか確認（HTTPS形式）
- リポジトリがプライベートの場合、PATに適切な権限があるか確認

**エラー**: `Directory is not empty`
- 選択肢A（空欄）を選んだ場合、Vault内にファイルがあると失敗します
- 解決策1: 新しい空のVaultを作成してやり直す
- 解決策2: サブフォルダ名を入力する（選択肢B）

**クローン中にフリーズ・クラッシュする**
- リポジトリが大きすぎる可能性があります
- Depth に `1` を入力して、最新コミットのみクローンを試す
- Wi-Fi接続が安定しているか確認

### クローン後にファイルが見えない

1. Obsidianを完全に再起動したか確認
2. 左サイドバーを開いてフォルダ構造を確認
3. サブフォルダにクローンした場合、そのフォルダ内を確認

### 認証情報を再入力するよう求められる

クローン後に認証情報がリセットされることがあります:
1. 設定 → Community plugins → Obsidian Git
2. Authentication セクションでUsername/PATを再入力

### プッシュが失敗する

**エラー**: `Failed to push`
1. まずプルを実行: コマンドパレット → 「Git: Pull」
2. 競合がある場合は解決してから再度プッシュ

### 同期が遅い・動作が不安定

- Obsidian Gitはモバイルでは完全に安定していません
- リポジトリが大きい場合は動作が遅くなります
- 重要な変更は手動でcommit/pushすることを推奨

### 設定がリセットされた

クローン後に設定がリセットされた場合:
1. 設定 → Community plugins → Obsidian Git
2. 認証情報を再入力（セクション5.2参照）

## 10. 便利な設定（オプション）

### モバイル用の追加設定

Obsidian Git設定の「Miscellaneous」セクション:

| 項目 | 推奨値 | 説明 |
|------|--------|------|
| Disable notifications | オフ | 同期状況を通知で確認 |
| Show status bar | オン | ステータスバーに同期状態表示 |

### ショートカットの設定

よく使うコマンドにショートカットを設定できます:

1. 設定 → Hotkeys
2. 「Obsidian Git」で検索
3. 「Git: Pull」「Git: Push」などにショートカットを割り当て
