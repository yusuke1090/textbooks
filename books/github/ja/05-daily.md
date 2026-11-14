# 5. ふだんの記録

## この章でわかること

- 作業の始めと終わりに打つコマンド
- `git status` の見方
- GitHub に上げてはいけないもの

## 始めと終わりに打つもの

作業を始めるときと、終わったときに、次の順に打ちます。

```bash
git pull
git status
git diff
git add .
git commit -m "I2C の読み取りを足した"
git push
```

| コマンド | すること |
| --- | --- |
| `git pull` | GitHub の新しい分を取り込む。別の PC でも作業しているなら、始める前に必ず |
| `git status` | 変えたファイルと、ステージに入れたファイルの一覧。**迷ったら、まずこれ** |
| `git diff` | ステージに入れていない変更を、行ごとに見る（`-` が消した行、`+` が足した行） |
| `git diff --staged` | ステージに入れた変更を見る（コミットする前の最後の確認） |
| `git add ファイル名` | そのファイルだけをステージに入れる |
| `git add .` | 変えたファイルを全部、ステージに入れる |
| `git commit -m "説明"` | 記録する |
| `git push` | GitHub に送る |
| `git log --oneline` | コミットの一覧（新しいものが上） |
| `git log -p ファイル名` | そのファイルの、変更の歴史 |
| `git show コミットの番号` | そのコミットで、何を変えたか |

- `git log` や `git diff` の表示が長いと、`:` が出て止まります。矢印キーで動かし、`q` で終わります
- **コミットの番号**は、`3d3b5db` のような英数字です。`git log --oneline` の左の列に出ます。コマンドでは、最初の7文字ほどを書けば通じます
- 1つのコミットには、1つのこと（「I2C の読み取りを足した」「LED のピンを変えた」）を入れます。あとで探すときや、戻すときに楽です
- 出荷したバージョンなど、あとで戻りたいコミットには、`git tag v1.0.0` → `git push --tags` で印（タグ）を付けます

## git status の見方

`git status` は、次のように出ます。

```text
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
        modified:   collar.cpp

Changes not staged for commit:
        modified:   CMakeLists.txt

Untracked files:
        mpu6050.h
```

| 見出し | 意味 |
| --- | --- |
| `Changes to be committed` | ステージに入っている。次のコミットに入る |
| `Changes not staged for commit` | 変えたが、まだステージに入れていない |
| `Untracked files` | git がまだ知らない、新しいファイル。`git add` するまで記録されない |
| `Your branch is ahead of 'origin/main' by 2 commits` | まだ GitHub に送っていないコミットが2つある。`git push` する |

## 上げてはいけないもの

| もの | どうするか |
| --- | --- |
| WiFi のパスワード・サーバーのパスワード・API キー | 別のファイルに分けて、`.gitignore` に入れる（下） |
| ビルドしてできたもの（`build/`、`.uf2`） | `.gitignore` に入れる。ソースからいつでも作り直せる |
| 大きなデータ（何十 MB もの CSV、動画） | `.gitignore` に入れる。GitHub は 100MB を超えるファイルを受け付けない |

たとえば Pico W で WiFi を使うときは、パスワードを `secrets.h` に書いて `.gitignore` に入れ、中身を空にした見本（`secrets.example.h`）だけを上げます。

```cpp
// secrets.h（git に上げない。secrets.example.h をコピーして作る）
#pragma once
#define WIFI_SSID     "my-wifi"
#define WIFI_PASSWORD "ここにパスワード"
```

- **一度プッシュしたものは、あとで消しても歴史に残ります。** パスワードを上げてしまったら、パスワードのほうを変えます
- すでに記録してしまったファイルを、記録から外すには `git rm --cached secrets.h`（PC のファイルは消えない）→ `.gitignore` に書く → コミット、とします。フォルダなら `git rm -r --cached build` です

## まとめ

- 始める前に `git pull`、終わったら `add` → `commit` → `push`
- 迷ったら `git status`
- パスワードと `build/` は上げない。`.gitignore` に書く
