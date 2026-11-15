# 8. 別の機械からクローンする

## 方法を選ぶ

ラズパイ・Jetson・別の PC で、GitHub の**非公開**のリポジトリを取ってくるには、その機械も GitHub に「自分である」ことを示す必要があります。使い方に合わせて選びます。

| 方法 | できること | 向いているとき |
| --- | --- | --- |
| **その機械で鍵を作って、アカウントに登録** | 自分の全部のリポジトリを、クローン・プッシュできる | 別の PC で開発する |
| **デプロイキー**（そのリポジトリだけに登録） | 1つのリポジトリだけ。ふつうは読むだけ | ラズパイ・Jetson で、決まったプログラムを取ってきて動かすだけ |
| **ssh -A で、PC の鍵を貸す** | ssh でログインしている間だけ、PC の鍵を使う | ラズパイで一時的にクローンしたい。機械に鍵を置きたくない |
| **GitHub を通さず、PC から直接** | 同じ LAN の中で、PC のリポジトリをクローンする | GitHub に置きたくない・インターネットがない |

## 別の PC で開発する

その PC で、3章の「1. 鍵があるか確かめる」〜「4. つながるか確かめる」をします。`-C` と Title には、その PC がわかる名前（例: `laptop`）を付けます。
そのあと、4章の「GitHub にあるリポジトリから始める（クローン）」のとおりにクローンします。2台目の PC でも、2章の名前とメールアドレスの設定を忘れずにします。

## ラズパイ・Jetson に読むだけの鍵を置く（デプロイキー）

ラズパイや Jetson では、コードを取ってきて動かすだけで、そこから GitHub に送ることはふつうありません。
そのときは、そのリポジトリだけに使える、読むだけの鍵（デプロイキー）にします。鍵を盗まれても、ほかのリポジトリや書き込みには使われません。

まず、ラズパイにログインして、鍵を作ります。

```bash
ssh pi@raspberrypi.local
ssh-keygen -t ed25519 -C "raspi-collar" -f ~/.ssh/collar_deploy -N ""
cat ~/.ssh/collar_deploy.pub
```

- `-f` は鍵のファイルの名前です。リポジトリごとに鍵を分けるので、決まった名前（`id_ed25519`）ではなく、わかる名前にします
- `-N ""` は、パスフレーズを空にします。自動で `git pull` できるようにするためです

出てきた1行を、GitHub に登録します。

1. GitHub で、リポジトリ（`collar`）のページの **Settings** → 左の **Deploy keys** を開く
2. **Add deploy key** を押す
3. **Title** に `raspi`、**Key** に1行を貼り付ける
4. **Allow write access は ☐ のまま**（読むだけ）にして、**Add key** を押す

次に、ラズパイの `~/.ssh/config` に、この鍵を使う「あだ名」を書きます（`nano ~/.ssh/config`）。

```text
Host github-collar
    HostName github.com
    User git
    IdentityFile ~/.ssh/collar_deploy
    IdentitiesOnly yes
```

あだ名を使って確かめて、クローンします。

```bash
ssh -T git@github-collar
git clone git@github-collar:ユーザー名/collar.git ~/collar
```

`ssh -T` で `Hi ユーザー名/collar! You've successfully authenticated…` と出れば、つながっています（デプロイキーでは、リポジトリの名前が出ます）。
新しいコードを取ってくるときは、`cd ~/collar` で移って `git pull` です。

- `github-collar` は「github.com に、`collar_deploy` の鍵でつなぐ」という意味のあだ名です。`git@github.com:` の代わりに `git@github-collar:` と書きます
- 1つのデプロイキーは、1つのリポジトリにしか登録できません。2つ目のリポジトリには、別の鍵（例: `logger_deploy`）と別のあだ名（例: `github-logger`）を作ります
- 鍵をもう使わないときは、GitHub の Deploy keys から消します

## ssh -A で PC の鍵を貸す

PC からラズパイに ssh でログインするときに `-A` を付けると、ログインしている間だけ、PC の鍵で GitHub につながります。秘密鍵は、ラズパイにはコピーされません。

```bash
ssh -A pi@raspberrypi.local
ssh -T git@github.com
git clone git@github.com:ユーザー名/collar.git
```

- 1行目は PC で、2行目からはラズパイの中で打ちます
- PC の鍵が ssh-agent に入っている必要があります（PC で `ssh-add -l` を打つと、鍵が出る）
- 自分だけが管理している機械で使います。ほかの人も管理者になれる機械では、その人に鍵を使われるおそれがあるので使いません

## GitHub を通さずに、PC から直接クローンする

同じ LAN の中なら、GitHub に置かなくても、PC のリポジトリを ssh で直接クローンできます。PC を、ssh でログインできる機械にします。

1. PC に、ssh のサーバーを入れる（入れると、自動で動き始める）

```bash
sudo apt install openssh-server
hostname
```

`hostname` で出た名前に `.local` を付けたもの（例: `main-pc.local`）で、同じ LAN のほかの機械からつながります。つながらないときは、`hostname -I` で出た IP アドレス（例: `192.168.1.20`）を使います。

2. ラズパイなど、クローンしたい機械で鍵を作り、PC に登録する

```bash
ssh-keygen -t ed25519 -C "raspi"
ssh-copy-id ユーザー名@main-pc.local
ssh ユーザー名@main-pc.local
```

`ssh-copy-id` で、PC のログインのパスワードを1回だけ聞かれます。公開鍵が、PC の `~/.ssh/authorized_keys` に足されます。
3行目でパスワードなしにログインできれば成功です。`exit` で戻ります。

3. クローンする

```bash
git clone ユーザー名@main-pc.local:apps/collar
```

`:` のあとは、PC のホームフォルダからの場所です。取ってきたあとは、`git pull` で PC の新しいコミットを取り込めます。

### ラズパイからも送りたいとき

PC の作業フォルダ（`~/apps/collar`）には、ほかの機械から直接プッシュできません（`refusing to update checked out branch` と出ます）。両方から送りたいときは、PC に「置き場だけのリポジトリ」（bare リポジトリ）を作り、GitHub の代わりにします。

```bash
git clone --bare ~/apps/collar ~/git/collar.git
cd ~/apps/collar
git remote add lan ~/git/collar.git
```

- PC では `git push lan main` で置き場に送り、`git pull lan main` で取り込みます
- ほかの機械では `git clone ユーザー名@main-pc.local:git/collar.git` でクローンし、ふつうに `git push`・`git pull` します
- `--bare` は、作業フォルダのない、記録だけのリポジトリです（GitHub の中にあるのと同じ形）

> この方法は、PC の電源が入っていて、同じ LAN にいるときだけ使えます。ふだんは GitHub を使うほうが簡単です。
> PC に ssh でログインできるようになるので、PC のパスワードは推測されにくいものにします。使わなくなったら `sudo apt remove openssh-server` で止めます。

## まとめ

- 別の PC で開発するなら、その PC でも鍵を作って GitHub に登録する
- ラズパイ・Jetson で取ってくるだけなら、読むだけのデプロイキー
- GitHub を通さないなら、PC に ssh でつないでクローンする

## 練習問題

```quiz
Q: ラズパイ・Jetson で取ってくるだけのときに使う、1つのリポジトリを読むだけの鍵を何といいますか。
A: デプロイキー | デプロイ・キー | deploy key
E: 書き込みはできないので、機械をなくしても被害が小さくすみます。

Q: PC の鍵をつないだ先の機械に貸す、ssh のオプションは何ですか。
A: -A | ssh -A
E: つないでいる間だけ、PC の鍵を使えます。

Q: 別の PC で開発するなら、その PC でも何を作って GitHub に登録しますか。
A: 鍵 | SSH キー | SSHキー | ssh key | key
E: 機械ごとに1組の鍵を作ります。
```
