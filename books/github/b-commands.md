# 付録B. コマンドの一覧

## よく使うコマンド

| やること | コマンド |
| --- | --- |
| 名前とメールアドレスを登録する（最初だけ） | `git config --global user.name "名前"`、`git config --global user.email "アドレス"` |
| SSH キーを作る（機械ごとに最初だけ） | `ssh-keygen -t ed25519 -C "機械の名前"` |
| 公開鍵を表示する | `cat ~/.ssh/id_ed25519.pub` |
| GitHub につながるか確かめる | `ssh -T git@github.com` |
| gh でログインする | `gh auth login` |
| 今のフォルダをリポジトリにする | `git init` |
| GitHub に作って送る | `gh repo create 名前 --private --source=. --push` |
| GitHub の置き場とつなぐ | `git remote add origin git@github.com:ユーザー名/名前.git` → `git push -u origin main` |
| つないでいる先を見る・変える | `git remote -v`、`git remote set-url origin URL` |
| クローンする | `git clone git@github.com:ユーザー名/名前.git` |
| 状態を見る | `git status` |
| 変更を見る | `git diff`、`git diff --staged` |
| 記録する | `git add .` → `git commit -m "説明"` |
| 送る・取り込む | `git push`、`git pull` |
| 歴史を見る | `git log --oneline`、`git show コミットの番号` |
| 変更を捨てる | `git restore ファイル名` |
| 取り消すコミットを作る | `git revert コミットの番号` |
| 一時的によける・戻す | `git stash`、`git stash pop` |
| ブランチを作る・移る・取り込む | `git switch -c 名前`、`git switch 名前`、`git merge 名前` |
| 印（タグ）を付ける | `git tag v1.0.0` → `git push --tags` |
