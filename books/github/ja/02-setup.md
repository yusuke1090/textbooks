# 2. 最初に1回だけする設定

## この章でわかること

- git と gh の入れ方
- コミットに入る名前とメールアドレスの登録
- GitHub のアカウントの用意

## git と gh を入れる

```bash
sudo apt install git gh
git --version
```

`git version 2.…` と出れば入っています。

## 名前とメールアドレスを登録する

コミットには、誰が記録したかとして、名前とメールアドレスが入ります。PC ごとに、最初に1回だけ設定します。

```bash
git config --global user.name "Taro Yamada"
git config --global user.email "12345678+ユーザー名@users.noreply.github.com"
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global core.editor nano
git config --global --list
```

| 設定 | 意味 |
| --- | --- |
| `user.name` | コミットに入る名前。GitHub のユーザー名でも、本名でもよい |
| `user.email` | コミットに入るメールアドレス。GitHub に置くと、コミットを見た人に見える |
| `init.defaultBranch main` | 新しく作るリポジトリの最初のブランチを `main` にする（GitHub と合わせる） |
| `pull.rebase false` | `git pull` のとき、両方で変えていたら「マージ」でまとめる（7章の「両方で変えていたとき」） |
| `core.editor nano` | コミットの説明を書くときなどに開くエディタを、nano にする |

- メールアドレスを人に見せたくないときは、GitHub の **Settings → Emails** の「Keep my email addresses private」に ☑ を入れ、そこに出ている `数字+ユーザー名@users.noreply.github.com` を使います
- 最後の `git config --global --list` で、設定した内容が出ます。設定は `~/.gitconfig` に入ります
- `--global` は「この PC の、このユーザーの全部のリポジトリ」という意味です

## GitHub のアカウント

[github.com](https://github.com) でアカウントを作ります（無料）。非公開のリポジトリも無料で作れます。
**2段階認証**（ログインのときに、スマホのアプリなどでもう1つ確かめる）も設定しておきます。GitHub の **Settings → Password and authentication** にあります。

## まとめ

- `sudo apt install git gh` で入れる
- PC ごとに最初に1回、名前・メールアドレス・`main` を設定する
- GitHub のアカウントには2段階認証を付ける

## 練習問題

```quiz
Q: Ubuntu で git と gh を入れるコマンドは `sudo apt install` のあとに何と書きますか。
A: git gh | gh git
E: `sudo apt install git gh` で入れます。

Q: PC ごとに最初に1回、名前・メールアドレスと、もう1つ何を設定しますか（最初のブランチの名前）。
A: main
E: 最初のブランチの名前を `main` にします。

Q: GitHub のアカウントを守るために付ける、パスワードのほかにもう1つ確かめる仕組みを何といいますか。
A: 2段階認証 | 二段階認証 | 2要素認証 | 二要素認証 | 2FA
E: スマホのアプリなどで、もう1つ確かめます。
```
