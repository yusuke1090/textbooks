# 6. Docker Compose（複数のコンテナ）

## Compose とは

Web アプリとデータベースのように、いくつかのコンテナを組み合わせるとき、`docker run` を長いオプション付きで何回も打つのは大変です。**Docker Compose** は、それを `compose.yaml` という1つのファイルに書いておき、1つのコマンドでまとめて動かす道具です。

## 作るもの

4章の Flask のアプリに、数を数えるデータベース（Redis）をつなぎます。ページを開くたびに数が増えます。

```text
counter/
├── app.py
├── requirements.txt
├── Dockerfile          ← 4章と同じ
└── compose.yaml
```

`app.py`:

```python
import os
from flask import Flask
import redis

app = Flask(__name__)
r = redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"), port=6379)

@app.route("/")
def hello():
    n = r.incr("hits")          # 1 増やして、その数を返す
    return f"このページは {n} 回見られました。\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

`requirements.txt`:

```text
flask
redis
```

`compose.yaml`:

```yaml
services:
  web:                      # サービスの名前（コンテナ同士はこの名前でつながる）
    build: .                # この場所の Dockerfile からイメージを作る
    ports:
      - "5000:5000"         # docker run -p と同じ
    environment:
      - REDIS_HOST=redis    # つなぐ先は、サービスの名前「redis」
    depends_on:
      - redis               # redis を先に起動する
  redis:
    image: redis:7          # Docker Hub のイメージをそのまま使う
    volumes:
      - redis-data:/data    # 数をボリュームに残す

volumes:
  redis-data:
```

- YAML は、字下げ（空白）でまとまりを表す。タブは使えない
- 同じ compose.yaml のサービスは、同じネットワークに入り、**サービスの名前**で相手につながる（`redis` という名前が、そのまま相手の場所になる）
- 古い書き方の先頭の `version: "3"` は、今は要らない

## 動かす

```bash
docker compose up -d --build     # 作って、まとめて後ろで動かす
curl http://localhost:5000       # このページは 1 回見られました。
curl http://localhost:5000       # このページは 2 回見られました。
```

| コマンド | すること |
| --- | --- |
| `docker compose up -d` | まとめて動かす（`--build` でイメージを作り直す） |
| `docker compose ps` | 動いているサービスの一覧 |
| `docker compose logs -f web` | web のログを見続ける（Ctrl + C で抜ける） |
| `docker compose exec redis redis-cli` | redis のコンテナの中でコマンドを打つ |
| `docker compose restart web` | web だけ再起動する |
| `docker compose down` | まとめて止めて、コンテナを消す（ボリュームは残る） |
| `docker compose down -v` | ボリュームも消す（データも消える） |

VS Code では、`compose.yaml` を右クリック →「Compose Up」・「Compose Down」でもできます。クジラのアイコンの CONTAINERS では、プロジェクトの名前（フォルダ名）でまとまって表示されます。

## 開発中はバインドマウントと組み合わせる

コードを直すたびに作り直すのが手間なら、手元のフォルダをつなぎ、Flask の自動の読み直しを使います。

```yaml
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - REDIS_HOST=redis
    volumes:
      - .:/app                                   # 手元のフォルダを /app につなぐ
    command: flask --app app run --host 0.0.0.0 --port 5000 --debug   # 直すと自動で読み直す
    depends_on:
      - redis
  redis:
    image: redis:7
```

`command` は、Dockerfile の `CMD` を上書きします。

## まとめ

- `compose.yaml` の `services` に、コンテナを並べて書く。`build` か `image`、`ports`・`environment`・`volumes`
- コンテナ同士は、サービスの名前でつながる
- `docker compose up -d --build` で動かし、`down` で片付ける（`-v` はデータも消す）
- 開発中は `volumes: - .:/app` で手元のコードをつなぐ

## 練習問題

```quiz
Q: Compose で、コンテナを並べて書くファイルの名前は何ですか。
A: compose.yaml | compose.yml | docker-compose.yml
E: `services` の下に、コンテナを1つずつ書きます。

Q: Compose のコンテナ同士は、何でつながりますか。
A: サービスの名前 | サービス名 | 名前 | service name
E: 例えば `db` というサービスには、ホスト名 `db` でつながります。

Q: Compose で、作り直してから後ろで動かすコマンドは何ですか。
A: docker compose up -d --build | up -d --build
E: 片付けるのは `docker compose down` です。

Q: `docker compose down` に付けると、ボリュームのデータも消すオプションは何ですか。
A: -v | --volumes
E: 消すと戻らないので、気をつけて使います。
```
