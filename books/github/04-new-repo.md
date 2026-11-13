# 4. 新しくリポジトリを作る

## この章でわかること

- 手元のフォルダをリポジトリにして、最初のコミットをする方法
- GitHub に置き場を作って送る、3つの方法
- GitHub にあるリポジトリを手元にコピーする方法（クローン）

流れは「手元でリポジトリにして、最初のコミットをする → GitHub に置き場を作って、送る」です。置き場の作り方は3つあり、どれでも同じものができます。

| 方法 | すること | 向いているとき |
| --- | --- | --- |
| VS Code の **Publish to GitHub** | ソース管理のボタンを押す | VS Code で作ったプロジェクトを、そのまま置く |
| **gh repo create** | コマンド1行 | ターミナルで作業しているとき |
| **GitHub の画面で作ってつなぐ** | ブラウザで作り、`git remote add` でつなぐ | gh を入れていない PC。git だけでできる |

VS Code の拡張機能（「Raspberry Pi Pico」など）で作ったプロジェクトは、まだ git のリポジトリになっていません（`.gitignore` だけはできています）。

## 1. 手元でリポジトリにする

```bash
cd ~/apps/collar
git init
```

`Initialized empty Git repository in /home/ユーザー名/apps/collar/.git/` と出ます。

`.gitignore` がなければ作ります（`nano .gitignore`）。C++ のプロジェクトなら、次のようにします。

```text
# ビルドしてできたもの
build/
# パスワードなど（5章の「上げてはいけないもの」）
secrets.h
# Python で使うもの
__pycache__/
.venv/
```

## 2. 最初のコミットをする

```bash
git add .
git status
git commit -m "最初のバージョン"
```

`git status` で、`Changes to be committed:` の一覧を見ます。`build/` や、パスワードの入ったファイルがないことを確かめてから、コミットします。

## 3. GitHub に置く

次の A か B の、どちらかでします（VS Code の Publish to GitHub を押してもかまいません）。

### A. gh で作る

```bash
gh repo create collar --private --source=. --push
```

GitHub に `collar` という非公開のリポジトリを作り、`origin` として登録し、最初のコミットまで送ります。

### B. GitHub の画面で作ってつなぐ

1. GitHub の右上の **＋** → **New repository** を押す
2. **Repository name** に `collar` と書き、**Private** を選ぶ
3. README・.gitignore・license は**付けない**（空のリポジトリにする。手元のものと食い違わないように）
4. **Create repository** を押す
5. 出てきた画面で **SSH** を選び、`git@github.com:ユーザー名/collar.git` をコピーする

```bash
git remote add origin git@github.com:ユーザー名/collar.git
git push -u origin main
```

- `git remote add origin URL` で、GitHub のリポジトリを `origin` という名前で登録します
- `-u` は「この先は、`git push` と `git pull` だけで、origin の main とやり取りする」と覚えさせます。最初の1回だけ付けます

## 4. 置けたか確かめる

ブラウザで `https://github.com/ユーザー名/collar` を開き、ファイルが並んでいれば完了です（`gh repo view --web` でも開けます）。
README.md を置いておくと、このページの下に表示されます。何のプログラムか・どの機械で動くか・ビルドのしかたを書いておくと、あとで自分が助かります。

## GitHub にあるリポジトリから始める（クローン）

別の PC で続きを開発するときや、ほかの人のリポジトリを使うときです。

```bash
cd ~/apps
git clone git@github.com:ユーザー名/collar.git
cd collar
code .
```

- `gh repo clone collar` でも同じです（自分のリポジトリなら、ユーザー名を省けます）
- 公開されているリポジトリ（pico-examples など）は、ログインしなくても HTTPS の URL でクローンできます
- フォルダの名前は、リポジトリの名前（`collar`）になります

## まとめ

- `git init` → 最初のコミット → `gh repo create`（または GitHub の画面で作って `git remote add`）→ `git push -u origin main`
- 最初のコミットの前に `git status` で、`build/` やパスワードが入っていないか確かめる
- 別の PC では `git clone` で始める
