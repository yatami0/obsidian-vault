[[WSL2セットアップ]]
## いま提案されている構成の意味

提案のステップ4〜6あたりは、こういう役割分担になっています。[mise.jdx+1](https://mise.jdx.dev/faq.html)

- WSL(Ubuntu)
    
    - mise: Node / pnpm など「開発者として使うツール」のバージョン管理。[zenn+1](https://zenn.dev/tazzae999jp/articles/a645ec56ea8613)
        
    - Node 22 + pnpm 9: Next.js プロジェクトを動かすためのランタイム（現状はホストWSLで動かしている）。[[zenn](https://zenn.dev/hiro345/articles/20260113_development)]​
        
    - `npm install -g @anthropic-ai/claude-code`: Claude Code CLI を、WSL側の Node/npm 上に入れている。[[code.claude](https://code.claude.com/docs/en/settings)]​
        

この段階では、アプリも開発ツールも全部「WSL ホストの上に直接載せている」状態です。ここから「アプリ実行だけコンテナに落としていく」と考えると整理しやすいです。[docker+2](https://docs.docker.com/desktop/features/wsl/use-wsl/)

## Docker とどう分担するか

あなたのやりたい「開発環境ごとに Docker で管理したい」を当てはめると、最終的な狙いはこうだと思います。[docker.ubitools+3](https://docker.ubitools.com/desktop/features/wsl/)

- アプリ（Next.js / API / DB など）の実行環境
    
    - → Docker コンテナの中（`FROM node:22` などでバージョン固定）。
        
- ホスト（WSL）の役割
    
    - → Docker CLI、VS Code / Claude Code、git、軽いツールだけ。
        
    - 必要なら Node も入っているが、「ホストで直接アプリを走らせない」方向に寄せていく。
        

このとき mise は、

- 「ホスト（WSL）に置いておくツール」をキレイにするためのバージョンマネージャ
    
- 例:
    
    - `mise use --global node@22` → Claude Code CLI や軽いスクリプト用。
        
    - devcontainer を使うための補助ツール（npm製 CLI など）。[mise.jdx+2](https://mise.jdx.dev/dev-tools/backends/npm.html)
        

という使い方になります。

## どこで何のバージョンを持つか整理

ややこしいポイントを表にするとこんな感じです。

|場所|何が入るか|誰がバージョン管理するか|
|---|---|---|
|Windows|Docker Desktop, VS Code 本体|Windows 側のインストーラ。[docker+1](https://docs.docker.com/desktop/features/wsl/use-wsl/)|
|WSL(ホスト)|mise, git, Claude Code CLI, 必要最小限の Node 等|mise（＋apt）で管理。[zenn+1](https://zenn.dev/tazzae999jp/articles/a645ec56ea8613)|
|Docker コンテナ|Python / Node / DB / ランタイム一式|Dockerfile（イメージタグ）で固定。[docker+2](https://www.docker.com/blog/master-docker-vs-code-supercharge-your-dev-workflow/)|

「Python とか Node のバージョンもコンテナの中」という理解は正しくて、「ホスト側はそれを操作するための最低限だけ持っておく」と考えるとスッキリします。[code.visualstudio+2](https://code.visualstudio.com/docs/devcontainers/containers)

## このガイドからどう発展させるか

今のステップは「まず WSL 上で全部動くところまで」をゴールにしているので、次の段階でこう発展させるイメージです。[docker+3](https://www.docker.com/blog/master-docker-vs-code-supercharge-your-dev-workflow/)

1. いまの `test-app` を devcontainer / Docker に載せ替える
    
    - Dockerfile で `FROM node:22-alpine` などを指定。
        
    - `docker-compose` や `devcontainer.json` でコンテナ起動。
        
2. VS Code から「コンテナの中に接続して開発」に切り替える
    
    - 左下が「Dev Container: 〜」表示になるやつ。[zenn+1](https://zenn.dev/streamwest1629/articles/vscode_wanderer-in-devcontainer)
        
3. Next.js の `pnpm dev` はコンテナの中で実行
    
    - ホストWSLの Node / pnpm は「予備・ユーティリティ」的な位置付けにしていく。
        

こうすると、「本番に近い環境は常に Docker」「ホストは軽く保つ」「mise はホスト側のツールを整理する役」ときれいに分かれます。[docker+3](https://docs.docker.com/desktop/features/wsl/use-wsl/)

---

もし「このガイドをベースに、次は devcontainer まで含めた構成図とファイル例を出してほしい」なら、

- Next.js + Postgres くらいの想定で、
    
- `Dockerfile` / `docker-compose.yml` / `.devcontainer/devcontainer.json`  
    まで一式サンプルを書きます。