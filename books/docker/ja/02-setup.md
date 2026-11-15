# 2. 準備（Ubuntu と VS Code）

## Docker を入れる

Ubuntu のパッケージで入れるのが手軽です。

```bash
sudo apt update
sudo apt install docker.io docker-compose-v2 docker-buildx
```

| パッケージ | 中身 |
| --- | --- |
| `docker.io` | Docker の本体（Docker Engine） |
| `docker-compose-v2` | `docker compose`（6章） |
| `docker-buildx` | イメージを作る道具の新しい版（4章） |

もっと新しい版がほしいときは、Docker の公式サイトの「Install Docker Engine on Ubuntu」の手順で、Docker の apt リポジトリから入れます（パッケージ名が `docker-ce` などに変わります。両方は入れません）。

> Windows や Mac では **Docker Desktop** を入れます。この教科書のコマンドは、そのまま使えます。

## sudo なしで使えるようにする

はじめは `docker` のコマンドに `sudo` が要ります。自分を `docker` グループに入れると、なしで使えます。

```bash
sudo usermod -aG docker $USER
```

**一度ログアウトして、入り直します**（パソコンの再起動でもよい）。そのあと確かめます。

```bash
docker run hello-world
docker compose version
```

`Hello from Docker!` が出れば成功です。

> `docker` グループに入ると、root（管理者）と同じくらい強いことができます。自分だけが使うパソコンで設定します。

Docker は、パソコンを起動すると自動で動きます。動いていないときは `sudo systemctl start docker` で始めます。

## VS Code の拡張機能

VS Code の拡張機能（左の四角が4つのアイコン）で、次の2つを入れます。

| 拡張機能 | 作者 | できること |
| --- | --- | --- |
| **Container Tools**（「Docker」で検索。前の名前は Docker） | Microsoft | 左にクジラのアイコンが出る。コンテナ・イメージ・ボリュームの一覧と操作、Dockerfile・compose.yaml の入力の補完 |
| **Dev Containers** | Microsoft | コンテナの中のフォルダを VS Code で開いて開発する（7章） |

クジラのアイコンを押すと、次の一覧が出ます。右クリックで、止める・消す・ログを見る・中に入る（Attach Shell）などができます。

| 一覧 | 中身 |
| --- | --- |
| CONTAINERS | 動いている・止まっているコンテナ |
| IMAGES | 手元にあるイメージ |
| REGISTRIES | Docker Hub などにつなぐ |
| VOLUMES | データを残す場所（5章） |
| NETWORKS | コンテナ同士をつなぐネットワーク |

この教科書では、コマンドをターミナル（**Ctrl + `**）で打ち、結果を左の一覧でも確かめる、という進め方をします。

## 練習用のフォルダ

```bash
mkdir -p ~/apps/docker-study
cd ~/apps/docker-study
code .
```

## まとめ

- `sudo apt install docker.io docker-compose-v2 docker-buildx` で入れる
- `sudo usermod -aG docker $USER` のあと、ログインし直すと sudo なしで使える
- `docker run hello-world` で確かめる
- VS Code には Container Tools と Dev Containers を入れる

## 練習問題

```quiz
Q: Docker を sudo なしで使うために、自分を入れるグループの名前は何ですか。
A: docker
E: `sudo usermod -aG docker $USER` のあと、ログインし直します。

Q: Docker が動くかを確かめるときに動かす、テスト用のイメージの名前は何ですか。
A: hello-world | hello world
E: `docker run hello-world` で、あいさつの文が出れば動いています。

Q: VS Code で、フォルダをコンテナの中で開いて開発するための拡張機能は何ですか。
A: Dev Containers | DevContainers
E: もう1つ、Container Tools も入れます。
```
