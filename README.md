# 📚 教科書（textbooks）

いろいろなことを、章ごとにまとめて勉強するための教科書を集めたリポジトリ。

**サイト: https://yusuke1090.github.io/textbooks/**（スマホでも読める）

| 教科書 | 中身 | 言葉 |
| --- | --- | --- |
| [🐄 牛の教科書](https://yusuke1090.github.io/textbooks/?b=cow) | 乳牛のからだ・繁殖と1年1産・エサ・乳房炎・血乳・スマート酪農（13章と付録、図24枚） | 日本語・English |
| [🍓 ラズパイピコ開発ガイド](https://yusuke1090.github.io/textbooks/?b=pico) | Raspberry Pi Pico を C++ と VS Code で開発して、製品にするまで（17章と付録） | 日本語 |
| [🐙 GitHub の教科書](https://yusuke1090.github.io/textbooks/?b=github) | git と GitHub の使い方。設定・SSH キー・ふだんの記録・戻し方・ブランチ・ラズパイからのクローン・VS Code での操作（9章と付録） | 日本語 |

## 読む画面でできること

- **目次**: 部ごとに章が並ぶ。章の ▶ で小見出しが開き、押すとその見出しの所へ移る
- **◀ ▶** で前後の章へ。開き直すと、前に読んでいた章の、読んでいた所から出る
- **日本語 / English**（2つの言葉がある教科書）: 同じ章の、同じ見出しの所が出る
- **図**: 下に「図 9-1 説明」が付く。押すと大きく表示する（スマホでは横にずらしたり、指で拡大したりできる）
- **言葉の説明**: 本文の点線の言葉（用語集にある言葉。章ごとに最初の1回）や、コードの関数・引数・コマンドを押すと、吹き出しで意味が出る
- **付箋・線・メモ**: 文字を選ぶと、線（黄・ピンク・緑・青）・📝 メモ・📌 付箋・🔤 訳すのボタンが出る。🔖 で一覧を開き、押すとその場所へ飛ぶ
- **コード**: 「コピー」ボタンで写せる
- **🔤 訳す**: 英語の単語や文を、日本語に訳す（[スマート農業News](https://github.com/yusuke1090/smart-agri-news) の `translate.js` を読み込んで使う）

付箋・線・メモと、読んでいた所は、見ているブラウザの `localStorage` に保存する（`textbooks-notes`、`textbooks-pos-<教科書>`）。iPhone と PC では別々。
場所は「選んだ文字・前後の文字・だいたいの位置」で覚えるので、本文を直しても、その文字が残っていれば同じ所に付く。

## 手元で見る

```sh
cd ~/apps/textbooks
python3 -m http.server 8000      # http://localhost:8000 を開く
```

ファイルを直接開く（file://）と、章を読み込めない。必ずサーバーを通して開く。

## しくみ

```
index.html        本棚（教科書の一覧）と、読む画面（?b=cow のとき）を1つのページで
books.json        本棚に並べる教科書（id・アイコン・題名・説明・言葉・戻り先など）
books/<id>/
  chapters.json   章の順番・部・題名（2つの言葉があるときは {"ja": …, "en": …}）
  ja/ en/         章の Markdown（2つの言葉があるとき）。1つの言葉なら books/<id>/ に直接
  images/         図
  glossary.json   コードの言葉の説明（あれば）
  terms.json      本文の用語の説明（あれば。tools/make_terms.py で用語集の章から作る）
tools/            図や用語の一覧を作るスクリプト
```

- サイトは GitHub Pages（main ブランチの一番上）でそのまま公開する。作り直す手順はない（push すれば1分ほどで出る）
- `.nojekyll` があるので、Markdown は変換されずにそのまま配られる
- アドレス: `?b=cow`（教科書）、`#ch=9`（章。目次の並び順の番号）、`&lang=en`（言葉）

## 教科書を足す

1. `books/<id>/` を作り、章の Markdown と `chapters.json` を置く
2. `books.json` に1つ足す（`id`・`icon`・`langs`・`title`・`desc`。あれば `home`（戻り先）・`note`（下に出す注意）・`glossary`・`terms`）
3. 手元で見て確かめてから push する

```json
{"id": "soil", "icon": "🌱", "langs": ["ja"], "title": {"ja": "土の教科書"}, "desc": {"ja": "土の成り立ち、肥料、土壌診断"}}
```

### 章の書き方

- 見出しは `#`（章の題名）・`##`（目次に出る小見出し）・`###`・`####`
- 段落、箇条書き（2文字下げで入れ子）、番号付きの手順（途中に図をはさんでも `4.` から続けられる）、表（縦線は `\|`）、引用（`>`、注意書き）、**太字**、リンク、`コード`、`---`（区切り）
- 1行だけの画像 `![説明](images/名前.svg)` は図になり、「図 章-番号 説明」が付く。動画（mp4・webm・YouTube の URL）も同じ書き方
- コードは ```` ```cpp ```` ・ ```` ```python ```` ・ ```` ```bash ```` など。```` ```cpp run ```` はそのままビルドできるプログラム、```` ```python run ```` は Pico Studio で試せる MicroPython（ラベルが変わる）
- 2つの言葉がある教科書は、`ja/` と `en/` に同じファイル名で書き、**見出しの数と順番、図の順番をそろえる**（切り替えるときに見出しの番号で場所を合わせるため）

## 教科書ごとのメモ

### 🐄 牛の教科書（books/cow）

- 図24枚。グラフと絵の19枚は `python3 tools/make_cow_figures.py` で作る（数値は本文の目安から作ったイメージ）。残りの5枚（胃・1年1産・エサの種類・サイレージの作り方・大腸菌の乳房炎）は SVG を直接書いている
- 本文の用語の説明（`terms.json`）は、付録A（用語集）の表から `python3 tools/make_terms.py cow` で作る。用語集を直したら作り直す
- 2026-11-13 に [スマート農業News](https://github.com/yusuke1090/smart-agri-news) から移した。前の `cow.html` は、ここへの移動の案内になっている

### 🍓 ラズパイピコ開発ガイド（books/pico）

- [Pico Studio](https://github.com/yusuke1090/pico-studio) の画面の横に出るガイドの本体。Pico Studio は `~/apps/textbooks/books/pico` を読む（別の場所なら `PICO_GUIDE`）
- 2026-11-13 に Pico Studio の `guide/` から移した
- ```` ```cpp run ```` のプログラムが本物の Pico SDK でビルドできるかは、Pico Studio の `python3 tests/build_guide_cpp.py pico pico2` で確かめる
- コードの言葉の説明は `glossary.json`（キーの書き方は Pico Studio の README の「ガイドの書き方」）

### 🐙 GitHub の教科書（books/github）

- 2026-11-14 に、ラズパイピコ開発ガイドの「付録F. git と GitHub の使い方」を分けて作った。ピコのガイドの3章・4章は、ここへのリンクになっている
- コマンドの言葉の説明は `glossary.json`（ピコのガイドの `glossary.json` から、git・ssh・gh などを写したもの）
- 9章の VS Code の画面の図（`images/vscode-*.svg`、6枚）は `python3 tools/make_github_figures.py` で作る
