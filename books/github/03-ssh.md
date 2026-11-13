# 3. SSH キーで GitHub とつなぐ

## この章でわかること

- GitHub とつなぐ2つの方法（SSH キーと HTTPS）
- SSH キーの作り方と、GitHub への登録
- つながるかの確かめ方
- HTTPS で使っていたリポジトリを SSH に切り替える方法

## つなぐ方法を選ぶ

非公開のリポジトリをクローンしたり、プッシュしたりするには、PC が「自分である」ことを GitHub に示す必要があります。**GitHub のパスワードは使えません**（打っても断られます）。方法は2つあります。

| 方法 | リポジトリの URL | 準備 | 向いているとき |
| --- | --- | --- | --- |
| **SSH キー**（おすすめ） | `git@github.com:ユーザー名/collar.git` | 鍵を作って GitHub に登録する（下） | ふだんの開発。ラズパイ・Jetson など、ブラウザがない機械 |
| HTTPS と gh | `https://github.com/ユーザー名/collar.git` | `gh auth login` で、ブラウザからログインする | 手早く始めたいとき。VS Code の Publish to GitHub もこちら |

どちらでも、できることは同じです。1つの PC で両方を使ってもかまいません。この教科書では SSH キーを使います。

## SSH キーとは

![SSH キーで GitHub とつなぐ](images/git-ssh-keys.svg)

SSH キーは、**秘密鍵**と**公開鍵**の2つで1組のファイルです。

| ファイル | 中身 | 扱い |
| --- | --- | --- |
| `~/.ssh/id_ed25519` | 秘密鍵 | **誰にも渡さない。** ほかの機械にコピーしない、GitHub にも上げない |
| `~/.ssh/id_ed25519.pub` | 公開鍵（`.pub` は public の略） | 渡してよい。GitHub に登録する |

GitHub は、登録された公開鍵と組になる秘密鍵を持っている機械だけを、自分として通します。
鍵は**機械ごとに1組**作ります（PC・ノート PC・ラズパイ・Jetson でそれぞれ）。どれかをなくしたら、GitHub の一覧からその鍵だけを消せば、ほかの機械はそのまま使えます。

## 1. 鍵があるか確かめる

```bash
ls ~/.ssh
```

`id_ed25519` と `id_ed25519.pub` があれば、もう作ってあります。「3. GitHub に公開鍵を登録する」に進みます。
`No such file or directory` と出たり、`known_hosts` や `authorized_keys` しかなかったりすれば、次で作ります。

## 2. 鍵を作る

```bash
ssh-keygen -t ed25519 -C "main-pc"
```

次のように聞かれます。

| 聞かれること | 答え方 |
| --- | --- |
| `Enter file in which to save the key (/home/ユーザー名/.ssh/id_ed25519):` | そのまま Enter（決まった場所に作る） |
| `Enter passphrase (empty for no passphrase):` | パスフレーズ（鍵のパスワード）を打つ。画面には何も出ない。PC を盗まれても、鍵を使われないようにするため |
| `Enter same passphrase again:` | もう一度、同じものを打つ |

`The key's randomart image is:` のあとに、四角い模様が出れば完了です。

- `-t ed25519` は鍵の種類です。いまのおすすめの種類で、短くて安全です
- `-C` は鍵に付けるメモです。どの機械の鍵かがわかる名前にします（GitHub の一覧で見分けるため）
- 画面のないラズパイなどで、自動で `git pull` させたいときは、パスフレーズを空（Enter だけ）にします。その代わり、その鍵は「読むだけ」で登録します（8章のデプロイキー）

## 3. GitHub に公開鍵を登録する

公開鍵の中身を表示します。

```bash
cat ~/.ssh/id_ed25519.pub
```

`ssh-ed25519 AAAAC3Nza…（長い文字）… main-pc` のような1行が出ます。これを全部コピーします（ターミナルでは Ctrl + Shift + C）。

1. GitHub の右上の自分のアイコン → **Settings** → 左の **SSH and GPG keys** を開く
2. **New SSH key** を押す
3. **Title** に、どの機械の鍵かを書く（例: `main-pc`）。**Key type** は **Authentication Key** のまま
4. **Key** に、コピーした1行を貼り付ける
5. **Add SSH key** を押す（パスワードや2段階認証を聞かれたら答える）

> **`.pub` が付いていないほう（秘密鍵）を貼らないでください。** 秘密鍵は `-----BEGIN OPENSSH PRIVATE KEY-----` で始まります。
> もし貼ってしまったら、GitHub からその鍵を消し、2. からやり直して新しい鍵を作ります。

### gh でまとめて登録する

gh を使うなら、ログインのときに SSH を選ぶと、鍵の登録（鍵がなければ作成も）までまとめてできます。

```bash
gh auth login
```

| 聞かれること | 選ぶもの |
| --- | --- |
| どこの GitHub か | **GitHub.com** |
| git の操作に使う方法（protocol） | **SSH** |
| 公開鍵を上げるか（鍵がなければ、作るか） | `~/.ssh/id_ed25519.pub` を選ぶ（作るときは、パスフレーズと Title を聞かれる） |
| ログインの方法 | **Login with a web browser** → 出てきた8文字のコードを、開いたブラウザに入れる |

- `gh auth status` で、ログインできているかと、使う方法（`Git operations protocol: ssh`）が出ます
- すでに HTTPS でログインしていて、SSH に変えたいときは `gh config set git_protocol ssh` を打ちます。このあと gh で作る・クローンするリポジトリが、SSH の URL になります

## 4. つながるか確かめる

```bash
ssh -T git@github.com
```

初めてのときは、次のように聞かれます。

```text
The authenticity of host 'github.com (…)' can't be established.
ED25519 key fingerprint is SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

`SHA256:` のあとが GitHub の [SSH key fingerprints](https://docs.github.com/ja/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints) のページに載っているものと同じなら、`yes` と打ちます。
相手が本物の GitHub かを確かめるためのもので、聞かれるのは最初の1回だけです（`~/.ssh/known_hosts` に覚えます）。パスフレーズを聞かれたら、2. で決めたものを打ちます。

```text
Hi ユーザー名! You've successfully authenticated, but GitHub does not provide shell access.
```

と出れば成功です。後ろの「shell access は使えない」は、GitHub にログインしてコマンドを打つことはできない、という意味で、git は使えます。
`Permission denied (publickey).` と出たら、付録A「よくあるエラー」を見ます。

## 5. パスフレーズを毎回聞かれないようにする

Ubuntu のデスクトップでは、鍵を覚えておく係（ssh-agent）が動いています。毎回パスフレーズを聞かれるときは、`~/.ssh/config` に次の2行を書きます（`nano ~/.ssh/config`）。

```text
Host *
    AddKeysToAgent yes
```

最初の1回だけパスフレーズを打てば、ログアウトするまでは聞かれなくなります。`ssh-add -l` で、覚えている鍵が出ます。

## HTTPS で使っていたリポジトリを SSH に切り替える

`git clone https://…` でクローンしたリポジトリや、VS Code の Publish to GitHub で置いたリポジトリは、HTTPS の URL になっています。SSH に変えるときは、次のようにします。

```bash
cd ~/apps/collar
git remote -v
git remote set-url origin git@github.com:ユーザー名/collar.git
git remote -v
```

`git remote -v` で、`origin` の URL が `git@github.com:…` に変わったことを確かめます。

## まとめ

- GitHub のパスワードでは、クローン・プッシュできない。SSH キーか、`gh auth login` を使う
- SSH キーは機械ごとに1組。秘密鍵は渡さず、公開鍵（`.pub`）を GitHub に登録する
- `ssh -T git@github.com` で確かめる
