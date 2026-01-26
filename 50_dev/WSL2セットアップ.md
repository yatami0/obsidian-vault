#WSL2
[[WSL2の中身]]

## 初期セットアップ
### 1-1インストール
``` powershell
### WSL
wsl --install
### Ubntu
wsl --install -d Ubuntu
```
### 1-2. PC を再起動
インストール完了後、再起動
### 1-3. Ubuntu の初期設定

再起動後、自動的に Ubuntu が起動します。
``` powershell
Enter new UNIX username: あなたのユーザー名
New password: パスワード（入力しても表示されません）
Retype new password: もう一度パスワード

username:yunagi
pass:Yunagi98
```

## Ubuntuの設定

### パッケージ最新化
``` bash
sudo apt update && sudo apt upgrade -y
```
### 基本ツールをインストール
``` bash
sudo apt install -y curl git unzip build-essential
```
### Gitの初期設定
``` bash
git config --global user.name "yatami0"
git config --global user.email "koba327konohachi@gmail.com"
```

## Docker Desktop  の設定

### 3-1. Docker Desktop をダウンロード

[https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

「Download for Windows」をクリック

### 3-2. インストーラーを実行

ダウンロードした `Docker Desktop Installer.exe` を実行

インストール時のオプション：

- ✅ **Use WSL 2 instead of Hyper-V** ← 必ずチェック
- ✅ Add shortcut to desktop

### 3-3. PC を再起動

### 3-4. Docker Desktop を起動

初回起動時にサービス規約への同意を求められます。

### 3-5. WSL2 統合を確認

Docker Desktop → 設定（歯車アイコン）→ Resources → WSL Integration

- ✅ Enable integration with my default WSL distro
- ✅ Ubuntu にチェック

「Apply & Restart」をクリック

### 3-6. 動作確認

Ubuntu ターミナルで：

bash

````bash
docker --version
```
```
Docker version 27.x.x, build xxxxx
````

bash

```bash
docker run hello-world
```


## Miseのインストールと設定

## ステップ4: mise のインストール（バージョン管理）

### 4-1. mise をインストール

Ubuntu ターミナルで：

bash

```bash
curl https://mise.run | sh
```

### 4-2. シェルに mise を追加

bash

```bash
echo 'eval "$(~/.local/bin/mise activate bash)"' >> ~/.bashrc
source ~/.bashrc
```

### 4-3. 確認

bash

```bash
mise --version
```

## ステップ5: Node.js と pnpm のインストール

### 5-1. Node.js をインストール

bash

```bash
mise use --global node@22
```

### 5-2. pnpm をインストール

bash

```bash
mise use --global pnpm@10
```

### 5-3. 確認

bash

```bash
node --version   # v22.x.x
pnpm --version   # 9.x.x
```


## ステップ6: Claude Code のインストール

### 6-1. Claude Code をインストール

bash

```bash
npm install -g @anthropic-ai/claude-code
```

### 6-2. 確認

bash

```bash
claude --version
```

### 6-3. 初回起動と認証

bash

```bash
claude
```

初回起動時に Anthropic アカウントでの認証を求められます。表示される指示に従ってブラウザで認証してください。


git remote add origin https://github.com/yatami0/master-repo.git