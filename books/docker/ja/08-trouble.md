# 8. 困ったとき・後片付け・ラズパイと Jetson

## よくあるエラー

| 出るメッセージ | 原因 | 直し方 |
| --- | --- | --- |
| `permission denied while trying to connect to the Docker daemon socket` | `docker` グループに入っていない、または入ったあとログインし直していない | `sudo usermod -aG docker $USER` のあと、ログインし直す（2章） |
| `Cannot connect to the Docker daemon` | Docker が動いていない | `sudo systemctl start docker`（起動時に自動にするなら `enable`） |
| `port is already allocated` / `address already in use` | そのポートを、ほかのコンテナやアプリが使っている | `docker ps` で探して止めるか、`-p 8081:80` のように手元のポートを変える |
| `The container name "/web" is already in use` | 同じ名前のコンテナが（止まっていても）ある | `docker rm -f web` で消してから |
| `exec format error` / `no matching manifest for linux/arm64` | パソコンとイメージの CPU の種類（アーキテクチャ）がちがう | 下の「ラズパイと Jetson」 |
| `no space left on device` | イメージやコンテナがたまって、ディスクがいっぱい | 下の「後片付け」 |
| ブラウザでつながらない | アプリが `127.0.0.1` で待っている、`-p` を付け忘れた | アプリを `0.0.0.0` で待たせる（4章）。`docker ps` の PORTS を見る |
| コードを直したのに変わらない | イメージが古いまま | `docker compose up -d --build`、またはバインドマウントを使う（5章） |
| コンテナがすぐ止まる | `CMD` のコマンドが終わった、エラーで落ちた | `docker logs 名前` で理由を見る |

まず `docker logs 名前` でログを見て、それから中に入って（`docker exec -it 名前 bash`、`bash` がなければ `sh`）確かめます。VS Code なら、クジラのアイコンから「View Logs」「Attach Shell」です。

## 後片付け

イメージやコンテナは、気づくとディスクをたくさん使っています。

```bash
docker system df             # 何がどれだけ使っているか
docker container prune       # 止まっているコンテナを全部消す
docker image prune           # 名前のない（古くなった）イメージを消す
docker image prune -a        # 使っていないイメージを全部消す（次に使うとき、またもらう）
docker volume prune          # 使っていないボリュームを消す（データも消える。注意）
docker system prune          # コンテナ・ネットワーク・名前のないイメージなどをまとめて
```

`prune` は確かめてから消しますが、ボリュームのデータは元にもどせません。大事なデータのボリュームは、名前を見てから消します。

## ラズパイと Jetson

### CPU の種類（アーキテクチャ）

| 機械 | アーキテクチャ |
| --- | --- |
| ふつうのパソコン | `amd64`（x86_64） |
| ラズパイ（64 ビットの OS）・Jetson | `arm64`（aarch64） |

イメージは、アーキテクチャごとに作られています。Python・Ubuntu・nginx・Redis などの公式イメージは、両方の版があるので、ラズパイでも同じ名前で動きます。自分で作ったイメージは、動かす機械と同じアーキテクチャで作ります。

- 一番かんたんなのは、**ラズパイや Jetson の上で `docker build` する**こと
- パソコンで arm64 用を作るなら、buildx を使う（QEMU という仕組みで、ほかの CPU のふりをするので遅い）

```bash
docker run --privileged --rm tonistiigi/binfmt --install arm64   # 1回だけ（QEMU を入れる）
docker buildx build --platform linux/arm64 -t ユーザー名/myapp:arm64 --push .
```

### ラズパイ

Raspberry Pi OS（64 ビット）では、Docker の公式の手順（Debian 用）で入れられます。手軽な方法として、公式のインストール用スクリプトもあります。

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER      # このあとログインし直す
```

メモリが少ない機種では、軽いイメージ（`-slim`・`alpine`）を使います。

### Jetson

- JetPack に、Docker と NVIDIA のコンテナ用の仕組み（GPU をコンテナから使うためのもの）が入っている
- GPU を使うときは `docker run --runtime nvidia ...` のように付ける
- イメージは、Jetson の **L4T（JetPack）の版に合ったもの**を使う。版は `cat /etc/nv_tegra_release` で確かめる。NVIDIA の NGC（`nvcr.io`）に、L4T 用のイメージがある

### VS Code から使う

VS Code の **Remote - SSH**（GitHub の教科書の9章）でラズパイや Jetson につなぐと、クジラのアイコンにはつないだ先のコンテナが出ます。Dev Containers の「Reopen in Container」も、つないだ先のコンテナで開けます。

## まとめ

- まず `docker logs` を見る。ポートの重なり・名前の重なり・グループの入り直しが多い
- `docker system df` で確かめて、`prune` で片付ける。ボリュームのデータは消すと戻らない
- ラズパイ・Jetson は arm64。その上で build するか、`buildx --platform linux/arm64`
- Jetson で GPU を使うときは `--runtime nvidia` と、L4T の版に合ったイメージ

## 練習問題

```quiz
Q: コンテナがうまく動かないとき、まず見るコマンドは何ですか。
A: docker logs | logs
E: ポートの重なり・名前の重なり・グループの入り直しが多い原因です。

Q: ラズパイや Jetson の CPU の種類（アーキテクチャ）は何ですか。
A: arm64 | aarch64 | ARM
E: パソコン（amd64）で作るなら `buildx --platform linux/arm64` を使います。

Q: 使っていないイメージやコンテナを片付けるときに使う言葉は何ですか（`docker system ???`）。
A: prune
E: 先に `docker system df` で、どれだけ使っているかを確かめます。

Q: Jetson で GPU を使うときに `docker run` に付けるオプションは何ですか。
A: --runtime nvidia | --runtime=nvidia
E: L4T の版に合ったイメージを使います。
```
