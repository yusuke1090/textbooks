# 7. ブランチで試す

## この章でわかること

- ブランチを分けて試し、main に取り込む方法
- 両方で同じ所を変えてしまったとき（コンフリクト）の直し方

## ブランチを分ける

動いている main を壊さずに、大きな変更（省電力の工夫を入れる、センサーを替える、など）を試したいときは、ブランチを分けます。
1人で開発していて、小さな変更をこまめにコミットするだけなら、main だけでもかまいません。

```bash
git switch -c try-sleep
git add .
git commit -m "スリープを試す"
git push -u origin try-sleep
```

`try-sleep` という枝を作って移り、そこでコミットします。main はそのまま残っています。

うまくいったら、main に取り込みます。

```bash
git switch main
git merge try-sleep
git push
git branch -d try-sleep
git push origin --delete try-sleep
```

やめるときは、main に戻って枝を消します（`-D` は取り込んでいない枝も消す）。

```bash
git switch main
git branch -D try-sleep
```

| コマンド | 意味 |
| --- | --- |
| `git branch` | ブランチの一覧。`*` が付いているのが、今いるブランチ |
| `git switch -c 名前` | 新しいブランチを作って、そこに移る |
| `git switch 名前` | そのブランチに移る。作業フォルダのファイルが、そのブランチの状態に変わる |
| `git merge 名前` | 今いるブランチに、そのブランチの変更を取り込む |
| `git branch -d 名前` | 取り込み済みのブランチを消す |

- VS Code では、左下に今のブランチの名前が出ています。押すと、切り替えと作成ができます
- ブランチを移る前に、変更をコミットするか、`git stash` でよけておきます
- GitHub では、ブランチから **Pull Request** を作り、変更を見比べてから main に取り込むこともできます（何人かで開発するとき）

## 両方で変えていたとき（コンフリクト）

2台の PC で同じファイルの同じ所を変えてから `git pull` や `git merge` をすると、どちらを残すか git が決められず、次のように出ます。

```text
CONFLICT (content): Merge conflict in collar.cpp
Automatic merge failed; fix conflicts and then commit the result.
```

ファイルの中に、両方の内容が印付きで入っています。

```text
<<<<<<< HEAD
const int SAMPLE_HZ = 50;
=======
const int SAMPLE_HZ = 100;
>>>>>>> 9f8e7d6
```

`<<<<<<<` から `=======` までが手元、`=======` から `>>>>>>>` までが取り込もうとした側です。

1. VS Code でファイルを開くと、印の上に **Accept Current Change**（手元を残す）・**Accept Incoming Change**（取り込む側を残す）・**Accept Both Changes**（両方）が出る。押すか、手で書き直して、印の3行を消す
2. ビルドして、動くか確かめる
3. `git add collar.cpp` → `git commit` → `git push`

- `git commit` で nano が開いたら、説明はそのままで、Ctrl + O → Enter（保存）→ Ctrl + X（閉じる）
- やめて、取り込む前に戻すときは `git merge --abort`
- 違う所を変えていただけなら、git が自動でまとめます（そのときも、まとめた記録の説明を書くために nano が開くので、同じように保存して閉じます）
- 防ぐには、作業を始める前に `git pull`、終わったら `git push` をくせにします

## まとめ

- 大きな変更は `git switch -c` で枝を分けて試し、うまくいったら `git merge` で main に取り込む
- コンフリクトは、残すほうを選んで印の3行を消し、`add` → `commit` → `push`
- 始める前に `git pull`、終わったら `git push` で防ぐ
