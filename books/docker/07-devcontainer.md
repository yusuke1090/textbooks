# 7. Dev Containers（コンテナの中で開発する）

## この章でわかること

- Dev Containers とは何か
- devcontainer.json を作って、コンテナの中でフォルダを開く
- 拡張機能・ライブラリ・ポートの設定、作り直し

## Dev Containers とは

VS Code の **Dev Containers** 拡張機能を使うと、VS Code の画面は手元のまま、**フォルダをコンテナの中で開いて**開発できます。ターミナル・Python・コンパイラ・拡張機能が、全部コンテナの中で動きます。

- パソコンに Python やライブラリを入れなくてよい。パソコンが汚れない
- プロジェクトごとに、ちがう版の Python や C++ のコンパイラを使える
- 設定ファイル（`.devcontainer/devcontainer.json`）を GitHub に入れておけば、ほかのパソコンでも同じ環境がすぐできる

## 始め方

1. VS Code で、開発したいフォルダを開く（例: `~/apps/py-study`）
2. **Ctrl + Shift + P** →「Dev Containers: Add Dev Container Configuration Files...」
3. 「Add configuration to workspace」→ 使いたいもの（例: **Python 3**）と版を選ぶ。追加の機能は、要らなければそのまま OK
4. `.devcontainer/devcontainer.json` ができる
5. 右下に出る「Reopen in Container」を押す（または Ctrl + Shift + P →「Dev Containers: Reopen in Container」）

はじめはイメージをもらうので、少し時間がかかります。左下に「Dev Container: Python 3」と出れば、コンテナの中です。ターミナルを開くと、コンテナの中のシェルになっています。

```bash
python --version      # コンテナの中の Python
pwd                   # /workspaces/py-study（手元のフォルダがつながっている）
```

手元のフォルダは、コンテナの `/workspaces/フォルダ名` につながっています（5章のバインドマウント）。ファイルを直すと、手元のファイルが直ります。

## devcontainer.json

```json
{
  "name": "py-study",
  "image": "mcr.microsoft.com/devcontainers/python:3.12",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-toolsai.jupyter"
      ]
    }
  },
  "postCreateCommand": "pip install -r requirements.txt",
  "forwardPorts": [5000]
}
```

| 項目 | 意味 |
| --- | --- |
| `image` | 使うイメージ。`mcr.microsoft.com/devcontainers/...` は、開発用に git などが入った Microsoft のイメージ |
| `customizations.vscode.extensions` | コンテナの中に入れる VS Code の拡張機能 |
| `postCreateCommand` | コンテナを作ったあとに1回実行するコマンド（ライブラリを入れるなど） |
| `forwardPorts` | コンテナのポートを、手元のパソコンにつなぐ（`localhost:5000` で開ける） |

C++ なら `mcr.microsoft.com/devcontainers/cpp`、Ubuntu だけなら `mcr.microsoft.com/devcontainers/base:ubuntu` などがあります。

### 自分の Dockerfile や Compose を使う

```json
{
  "name": "myapp",
  "build": { "dockerfile": "Dockerfile" }
}
```

```json
{
  "name": "counter",
  "dockerComposeFile": "../compose.yaml",
  "service": "web",
  "workspaceFolder": "/app"
}
```

Compose を使うと、データベースなどのコンテナも一緒に動きます（6章）。

## 変えたら作り直す

`devcontainer.json` や Dockerfile を変えたら、**Ctrl + Shift + P →「Dev Containers: Rebuild Container」**で作り直します。

## 手元にもどる

**Ctrl + Shift + P →「Dev Containers: Reopen Folder Locally」**で、ふつうの（手元の）フォルダにもどります。左下の「Dev Container」の所を押しても、メニューが出ます。

## git と GitHub

- コンテナの中でも `git` が使える。手元の git の名前・メールの設定は、自動でコンテナにも渡される
- SSH キー（GitHub の教科書の3章）は、手元の ssh-agent に登録してあれば、コンテナの中からも使える（`ssh-add ~/.ssh/id_ed25519`）
- `.devcontainer/` は GitHub に入れる。ほかのパソコンでクローンして開くと、「Reopen in Container」ですぐ同じ環境になる

## まとめ

- Dev Containers で、フォルダをコンテナの中で開いて開発する。パソコンが汚れない
- 「Add Dev Container Configuration Files」で `devcontainer.json` を作り、「Reopen in Container」で入る
- 拡張機能・`postCreateCommand`・`forwardPorts` を書いておく。変えたら「Rebuild Container」
- `.devcontainer/` を GitHub に入れれば、どこでも同じ環境
