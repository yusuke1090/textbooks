# 付録A. よくあるエラー

## エラーと直し方

| エラー | 意味と対処 |
| --- | --- |
| `Permission denied (publickey).` | GitHub（や PC）が鍵を受け付けない。① `ls ~/.ssh` で鍵があるか ② GitHub の SSH keys に、その機械の `.pub` の中身が登録されているか ③ `ssh-add -l` で鍵が入っているか、を確かめる。`ssh -vT git@github.com` で、どの鍵を試したかが出る |
| `Host key verification failed.` | 相手（github.com や PC）を確かめられなかった。初めてのときに `yes` と打たなかったなど。`ssh -T git@github.com` を打って、`yes` と答え直す |
| `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!` | 前につないだときと、相手の鍵が変わった。ラズパイの OS を入れ直したときに出る。自分で入れ直したとわかっているなら `ssh-keygen -R raspberrypi.local` で古い記録を消す。心当たりがなければ、つながない |
| `ssh: connect to host … port 22: Connection refused` | 相手で ssh のサーバーが動いていない。PC なら `sudo apt install openssh-server` |
| `remote: Support for password authentication was removed` | HTTPS の URL で、GitHub のパスワードを打った。`gh auth login` でログインするか、SSH の URL に変える（`git remote set-url`。3章） |
| `ERROR: Repository not found.` | URL のつづりがちがうか、その鍵（アカウント）では見られないリポジトリ。デプロイキーなら、あだ名とリポジトリの組み合わせを確かめる |
| `fatal: not a git repository` | git のリポジトリではないフォルダにいる。`cd ~/apps/collar` のように移る |
| `Author identity unknown` | 名前とメールアドレスが登録されていない。2章の設定をする |
| `error: src refspec main does not match any` | まだ1回もコミットしていない。または、ブランチの名前が `master` になっている（`git branch` で確かめ、`git branch -m master main` で変える） |
| `! [rejected] main -> main (fetch first)` | GitHub に、手元にないコミットがある（別の PC でプッシュした）。`git pull` してから `git push` |
| `fatal: Need to specify how to reconcile divergent branches.` | 両方で変えていて、まとめ方が決まっていない。`git config --global pull.rebase false` を打って、もう一度 `git pull` |
| `CONFLICT (content): Merge conflict in …` | 同じ所を両方で変えていた。7章の「両方で変えていたとき」 |
| `fatal: refusing to merge unrelated histories` | README などを付けて GitHub で作ったリポジトリに、手元のものをつなごうとした。`git pull origin main --allow-unrelated-histories` でまとめてから `git push` |
| `fatal: remote origin already exists.` | origin がもう登録されている。`git remote set-url origin URL` で URL を変える |
| `error: Your local changes to the following files would be overwritten` | コミットしていない変更があって、pull やブランチの切り替えができない。コミットするか、`git stash` でよける |
| `refusing to update checked out branch` | PC の作業フォルダに、直接プッシュした。8章の「ラズパイからも送りたいとき」の bare リポジトリを使う |
| `this exceeds GitHub's file size limit of 100.00 MB` | 大きすぎるファイルをコミットした。直前のコミットなら `git rm --cached ファイル名` → `.gitignore` に書く → `git commit --amend --no-edit` → `git push` |
| 画面の下に `:` や `(END)` が出て止まった | `git log`・`git diff` の表示の途中。`q` で終わる |
| 見慣れない画面（エディタ）が開いた | コミットやマージの説明を書く画面。nano なら Ctrl + O → Enter → Ctrl + X。vim なら `:wq` と打って Enter |
