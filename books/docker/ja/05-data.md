# 5. データと設定（ボリューム・環境変数）

## この章でわかること

- コンテナを消してもデータを残す方法（ボリューム・バインドマウント）
- 手元のフォルダをコンテナから使う
- 環境変数と .env で設定を渡す

## データを残す2つの方法

コンテナの中のファイルは、コンテナを消すと消えます（3章）。残したいものは、コンテナの外に置きます。

| 方法 | 書き方 | 置き場所 | 向いているもの |
| --- | --- | --- | --- |
| **ボリューム** | `-v 名前:/コンテナの場所` | Docker が管理する場所 | データベースのデータなど、コンテナが使うデータ |
| **バインドマウント** | `-v /パソコンの場所:/コンテナの場所` | パソコンのフォルダそのもの | 開発中のコード、読みこむデータ、結果の書き出し |

`:` の左が**名前**ならボリューム、`/` や `./` で始まる**場所**ならバインドマウントです。

## ボリューム

```bash
docker volume create pgdata
docker run -d --name db -e POSTGRES_PASSWORD=secret -v pgdata:/var/lib/postgresql/data postgres:16
docker rm -f db                                      # コンテナを消しても
docker run -d --name db -e POSTGRES_PASSWORD=secret -v pgdata:/var/lib/postgresql/data postgres:16
# 前のデータが残っている
```

- `docker volume ls` で一覧、`docker volume rm 名前` で消す（中のデータも消える）
- VS Code では、クジラのアイコンの VOLUMES に出る

## バインドマウント

パソコンのフォルダを、コンテナの中から見えるようにします。片方で変えると、もう片方にもすぐ反映されます。

```bash
cd ~/apps/docker-study
echo 'print("手元のファイルを、コンテナの Python で動かす")' > hello.py
docker run --rm -v "$(pwd)":/work -w /work python:3.12-slim python hello.py
```

- `$(pwd)` は今いるフォルダ。`"` で囲むと、空白の入った場所でも大丈夫
- `-w /work` は、コンテナの中の作業フォルダ
- VS Code で `hello.py` を直して、もう一度実行すると、すぐ反映される（イメージを作り直さなくてよい）

### ファイルの持ち主に注意

コンテナの中は root（管理者）で動くことが多いので、コンテナが書いたファイルは、パソコン側で root の持ち物になり、ふつうに消せなくなることがあります。自分のユーザーで動かすと防げます。

```bash
docker run --rm -v "$(pwd)":/work -w /work --user "$(id -u):$(id -g)" python:3.12-slim \
  python -c "open('out.txt', 'w').write('ok')"
ls -l out.txt          # 自分の持ち物になっている
```

## 環境変数で設定を渡す

パスワード・つなぐ先・時刻の地域など、場所によって変わる設定は、イメージに入れずに**環境変数**で渡します。

```bash
docker run --rm -e TZ=Asia/Tokyo -e GREETING=こんにちは python:3.12-slim \
  python -c "import os; print(os.environ['GREETING'])"
```

アプリの中では、Python なら `os.environ.get("名前", "なかったときの値")` で読みます。

### .env ファイル

数が多いときは、ファイルにまとめます。

`.env`:

```text
POSTGRES_PASSWORD=secret
TZ=Asia/Tokyo
```

```bash
docker run --rm --env-file .env postgres:16 env | grep TZ
```

> パスワードの入った `.env` は、`.gitignore` と `.dockerignore` に入れて、GitHub やイメージに入らないようにします。

## まとめ

- 消えて困るデータは、ボリューム（`-v 名前:/場所`）かバインドマウント（`-v "$(pwd)":/場所`）に置く
- バインドマウントなら、手元のコードを直してすぐコンテナで試せる。`--user "$(id -u):$(id -g)"` で持ち主をそろえる
- 設定は `-e` や `--env-file .env` で渡す。`.env` は GitHub に上げない

## 練習問題

```quiz
Q: Docker が管理する、名前を付けてデータを残す場所を何といいますか。
A: ボリューム | volume
E: `-v 名前:/場所` でつなぎます。

Q: 手元のフォルダをそのままコンテナにつなぐ方法を何といいますか。
A: バインドマウント | bind mount
E: 手元のコードを直して、すぐコンテナで試せます。

Q: `docker run` で、環境変数を1つ渡すオプションは何ですか。
A: -e | --env
E: たくさんなら `--env-file .env` です。

Q: パスワードなどを書いた、GitHub に上げてはいけないファイルの名前は何ですか。
A: .env | env
E: `.gitignore` に書いておきます。
```
