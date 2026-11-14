# 4. Dockerfile でイメージを作る

## この章でわかること

- Dockerfile の書き方（FROM・WORKDIR・COPY・RUN・CMD）
- イメージを作って（build）動かす
- レイヤーとキャッシュ、.dockerignore
- イメージを Docker Hub に置く

## 作るもの

Python の小さな Web アプリ（Flask）をイメージにします。VS Code で、次のファイルを作ります。

```text
myapp/
├── app.py
├── requirements.txt
├── Dockerfile
└── .dockerignore
```

`app.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from Docker!\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

`requirements.txt`:

```text
flask
```

> `host="0.0.0.0"` が大事です。`127.0.0.1`（Flask の標準）のままだと、コンテナの**中から**しかつながらず、パソコンのブラウザから見えません。

## Dockerfile

ファイル名は `Dockerfile`（拡張子なし）です。VS Code の Container Tools が、書き方の補完や説明を出してくれます。

```dockerfile
# もとにするイメージ
FROM python:3.12-slim

# コンテナの中の作業フォルダ（なければ作られる）
WORKDIR /app

# 先にライブラリの一覧だけをコピーして入れる（キャッシュのため。後で説明）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリのファイルをコピーする
COPY . .

# このコンテナが使うポート（説明のため。実際につなぐのは docker run -p）
EXPOSE 5000

# コンテナを動かしたときに実行するコマンド
CMD ["python", "app.py"]
```

| 命令 | 意味 |
| --- | --- |
| `FROM` | もとにするイメージ。最初に1つ書く |
| `WORKDIR` | 作業フォルダ。この後の命令は、ここで実行される |
| `COPY 元 先` | パソコンのファイルを、イメージの中にコピーする |
| `RUN` | イメージを作るときに、コマンドを実行する（ライブラリを入れるなど） |
| `ENV 名前=値` | 環境変数を決める |
| `EXPOSE` | 使うポートを書いておく |
| `CMD` | コンテナを動かしたときのコマンド。最後に1つ |

`RUN` は**イメージを作るとき**、`CMD` は**コンテナを動かすとき**に実行されます。

## イメージを作って動かす

`myapp` のフォルダで実行します。

```bash
docker build -t myapp .                          # . の Dockerfile から、myapp という名前で作る
docker images                                    # myapp ができている
docker run -d --name myapp -p 5000:5000 myapp    # 動かす
curl http://localhost:5000                       # Hello from Docker!
```

- `-t 名前:タグ` で名前を付ける（タグを省くと `latest`）。`-t myapp:1.0` のように版を付けておくとよい
- 最後の `.` は、Dockerfile のあるフォルダ（ここにあるファイルが COPY できる範囲になる）
- VS Code では、`Dockerfile` を右クリック →「Build Image...」でも作れる

### コードを直したら

イメージは作ったときのままです。`app.py` を直したら、作り直して、コンテナも作り直します。

```bash
docker rm -f myapp
docker build -t myapp .
docker run -d --name myapp -p 5000:5000 myapp
```

毎回これをするのは手間なので、開発中は Compose（6章）や Dev Containers（7章）を使います。

## レイヤーとキャッシュ

イメージは、命令1つごとの**レイヤー**（層）の重なりでできています。作り直すとき、変わっていない命令のレイヤーは、前のもの（**キャッシュ**）を使うので速くなります。ある命令が変わると、**それより後ろは全部**作り直しになります。

| 順番 | よくない書き方 | よい書き方 |
| --- | --- | --- |
| 1 | `COPY . .` | `COPY requirements.txt .` |
| 2 | `RUN pip install -r requirements.txt` | `RUN pip install -r requirements.txt` |
| 3 | | `COPY . .` |
| `app.py` を直したとき | `COPY . .` が変わるので、pip install もやり直し（遅い） | pip install はキャッシュを使い、`COPY . .` だけやり直し（速い） |

変わりにくいものを前に、変わりやすいものを後ろに書きます。

## .dockerignore

`COPY . .` で、要らないものまでイメージに入れないように、`.dockerignore` に書いておきます（`.gitignore` と同じ書き方）。

```text
.venv/
__pycache__/
*.pyc
.git/
.env
```

`.env`（パスワードなど。5章）をイメージに入れないことも大切です。

## イメージを置く（Docker Hub）

作ったイメージを、ほかのパソコンやラズパイで使うために、レジストリに置けます。

```bash
docker login                                 # Docker Hub のアカウントで入る
docker tag myapp:latest ユーザー名/myapp:1.0  # 置く場所の名前を付ける
docker push ユーザー名/myapp:1.0
# ほかのパソコンで
docker pull ユーザー名/myapp:1.0
```

GitHub の Container Registry（`ghcr.io`）にも置けます。公開したくないものは、非公開のリポジトリにします。

## まとめ

- Dockerfile は `FROM` → `WORKDIR` → `COPY` → `RUN` → `CMD`
- `docker build -t 名前 .` で作り、`docker run` で動かす。コードを直したら作り直す
- アプリは `0.0.0.0` で待ち受ける
- 変わりにくいもの（ライブラリ）を前に書くと、キャッシュで速くなる。要らないものは `.dockerignore`
