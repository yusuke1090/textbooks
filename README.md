# 📚 教科書（textbooks）

いろいろなことを、章ごとにまとめて勉強するための教科書を集めたリポジトリ。

**サイト: https://yusuke1090.github.io/textbooks/**（スマホでも読める）

| 教科書 | 中身 | 言葉 |
| --- | --- | --- |
| [🐄 牛の教科書](https://yusuke1090.github.io/textbooks/?b=cow) | 乳牛のからだ・繁殖と1年1産・エサ・乳房炎・血乳・スマート酪農（13章と付録、図24枚と写真38枚） | 日本語・English |
| [🌾 畑作と米の教科書](https://yusuke1090.github.io/textbooks/?b=crops) | 稲の育ち方・苗・水と肥料・病害虫・収穫と流通、北海道の輪作・麦・大豆・じゃがいも・てんさい、土と肥料、スマート農業（12章と付録、写真51枚） | 日本語 |
| [🍓 ラズパイピコ開発ガイド](https://yusuke1090.github.io/textbooks/?b=pico) | Raspberry Pi Pico を C++ と VS Code で開発して、製品にするまで（17章と付録、写真10枚） | 日本語 |
| [🚁 ROS 2 と ArduPilot の教科書](https://yusuke1090.github.io/textbooks/?b=ros) | ROS 2 Jazzy の基本、ArduPilot の SITL・MAVLink、ROS 2 からドローンを飛ばす（AP_DDS）、Gazebo、Jetson・ラズパイ、安全と法律（12章と付録、図2枚と写真17枚） | 日本語 |
| [🐙 GitHub の教科書](https://yusuke1090.github.io/textbooks/?b=github) | git と GitHub の使い方。設定・SSH キー・ふだんの記録・戻し方・ブランチ・ラズパイからのクローン・VS Code での操作（9章と付録） | 日本語 |
| [🌍 アフリカの教科書](https://yusuke1090.github.io/textbooks/?b=africa) | アフリカの歴史・食べ物・文化・トレンドと、タンザニア・ケニア・マラウイの農業・酪農・IoT の会社・参入するなら（9章と付録、写真60枚） | 日本語 |
| [🇬🇧 イギリスの教科書](https://yusuke1090.github.io/textbooks/?b=uk) | イギリスの歴史・食べ物・文化・トレンドと、農業・酪農・アグリテックの会社・参入するなら（9章と付録、写真55枚） | 日本語 |
| [🛐 宗教の教科書](https://yusuke1090.github.io/textbooks/?b=religion) | 国ごとに多い宗教と、ユダヤ教・キリスト教・イスラム教・ヒンドゥー教・仏教・シク教・ジャイナ教・儒教・道教・神道の考え方・歴史・行事・暮らしの決まり（12章と付録、写真74枚） | 日本語 |
| [🐍 Python の教科書](https://yusuke1090.github.io/textbooks/?b=python) | Ubuntu と VS Code で始めて、値・入れ物・関数・クラス・ファイル・例外から NumPy・pandas・matplotlib まで（10章） | 日本語 |
| [📊 統計の教科書](https://yusuke1090.github.io/textbooks/?b=stats) | 分散・相関・確率分布・期待値から、中心極限定理・回帰分析（OLS）とその注意点まで（8章、図5枚） | 日本語 |
| [🤖 機械学習の教科書](https://yusuke1090.github.io/textbooks/?b=ml) | scikit-learn で回帰・分類・前処理・クラスタリング・特徴量・モデルの評価（7章、図4枚） | 日本語 |
| [⚙️ C++ の教科書](https://yusuke1090.github.io/textbooks/?b=cpp) | g++ と VS Code で、変数・関数・ポインタからクラス・継承・テンプレート・例外まで（15章と付録） | 日本語 |
| [🐳 Docker の教科書](https://yusuke1090.github.io/textbooks/?b=docker) | VS Code で Docker。コンテナ・Dockerfile・ボリューム・Compose・Dev Containers・ラズパイと Jetson（8章、図2枚） | 日本語 |

## 読む画面でできること

- **目次**: 部ごとに章が並ぶ。章の ▶ で小見出しが開き、押すとその見出しの所へ移る
- **◀ ▶** で前後の章へ。開き直すと、前に読んでいた章の、読んでいた所から出る
- **日本語 / English**（2つの言葉がある教科書）: 同じ章の、同じ見出しの所が出る
- **図**: 下に「図 9-1 説明」が付く。押すと大きく表示する（スマホでは横にずらしたり、指で拡大したりできる）
- **言葉の説明**: 本文の点線の言葉（用語集にある言葉。章ごとに最初の1回）や、コードの関数・引数・コマンドを押すと、吹き出しで意味が出る
- **付箋・線・メモ**: 文字を選ぶと、線（黄・ピンク・緑・青）・📝 メモ・📌 付箋・🔤 訳すのボタンが出る。🔖 で一覧を開き、押すとその場所へ飛ぶ
- **コード**: 「コピー」ボタンで写せる
- **数式**: `math` を付けた教科書（統計・機械学習）は、`$…$` の式を [KaTeX](https://katex.org/) で表示する（そのときだけ cdnjs から読み込む）
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
2. `books.json` に1つ足す（`id`・`icon`・`group`・`langs`・`title`・`desc`。本棚は `group`（プログラミング・データ・道具・農業・地域）ごとに見出しを付けて、books.json の順に並ぶので、同じ分野の、読む順のところに入れる。あれば `home`（戻り先）・`note`（下に出す注意）・`glossary`・`terms`・`math`（数式を使うなら `true`））
3. 手元で見て確かめてから push する

```json
{"id": "soil", "icon": "🌱", "langs": ["ja"], "title": {"ja": "土の教科書"}, "desc": {"ja": "土の成り立ち、肥料、土壌診断"}}
```

### 章の書き方

- 見出しは `#`（章の題名）・`##`（目次に出る小見出し）・`###`・`####`
- 段落、箇条書き（2文字下げで入れ子）、番号付きの手順（途中に図をはさんでも `4.` から続けられる）、表（縦線は `\|`）、引用（`>`、注意書き）、**太字**、リンク、`コード`、`---`（区切り）
- 1行だけの画像 `![説明](images/名前.svg)` は図になり、「図 章-番号 説明」が付く。動画（mp4・webm・YouTube の URL）も同じ書き方
- コードは ```` ```cpp ```` ・ ```` ```python ```` ・ ```` ```bash ```` など。```` ```cpp run ```` はそのままビルドできるプログラム、```` ```python run ```` は Pico Studio で試せる MicroPython（ラベルが変わる）
- 数式（`math: true` の教科書）: 文の中は `$x^2$`、別の行に出すものは `$$…$$` を**1行で**書く。表の中では `|` の代わりに `\lvert` `\rvert`
- 2つの言葉がある教科書は、`ja/` と `en/` に同じファイル名で書き、**見出しの数と順番、図の順番をそろえる**（切り替えるときに見出しの番号で場所を合わせるため）
- 写真は Wikimedia Commons から借りる（CC0・パブリックドメイン・CC BY・CC BY-SA だけ）。`books/<id>/photos.json` に並べて `python3 tools/fetch_photos.py <id>` を動かすと、幅 960 px の JPEG にして `images/` に入れ、付録「写真の出典」（ふつうは `c-photos.md`）を作り直す

## 教科書ごとのメモ

### 🐄 牛の教科書（books/cow）

- 図24枚。グラフと絵の19枚は `python3 tools/make_cow_figures.py` で作る（数値は本文の目安から作ったイメージ）。残りの5枚（胃・1年1産・エサの種類・サイレージの作り方・大腸菌の乳房炎）は SVG を直接書いている
- 本文の用語の説明（`terms.json`）は、付録A（用語集）の表から `python3 tools/make_terms.py cow` で作る。用語集を直したら作り直す
- 2026-11-13 に [スマート農業News](https://github.com/yusuke1090/smart-agri-news) から移した。前の `cow.html` は、ここへの移動の案内になっている

### 🌾 畑作と米の教科書（books/crops）

- 2026-11-15 に作った。第1部 米（1〜6章）、第2部 畑作（7〜10章）、第3部 土とスマート農業（11〜12章）。米の値段と政策（令和の米騒動、2027年度からの水田政策）は、そのときにウェブで調べたもの。出典は付録B
- 写真は `photos.json` に並べ、`python3 tools/fetch_photos.py crops` で取ってくる

### 🍓 ラズパイピコ開発ガイド（books/pico）

- [Pico Studio](https://github.com/yusuke1090/pico-studio) のヘッダの「📚 ガイド」から開く。Pico Studio のテスト（下）は `~/apps/textbooks/books/pico` を読む（別の場所なら `PICO_GUIDE`）
- 2026-11-13 に Pico Studio の `guide/` から移した
- ```` ```cpp run ```` のプログラムが本物の Pico SDK でビルドできるかは、Pico Studio の `python3 tests/build_guide_cpp.py pico pico2` で確かめる
- コードの言葉の説明は `glossary.json`（キーの書き方は Pico Studio の README の「ガイドの書き方」）

### 🚁 ROS 2 と ArduPilot の教科書（books/ros）

- 2026-11-15 に作った。Ubuntu 24.04 ＋ ROS 2 Jazzy が前提。ArduPilot の DDS のトピック・サービス・QoS・`/ap/cmd_vel` の座標は、ArduPilot の公式ドキュメントとソースコード（`libraries/AP_DDS/`）で確かめた。出典は付録B
- この環境には ROS 2 と ArduPilot の SITL がないので、ROS 2 のコードは文法だけを確かめた。8章の pymavlink のコードは、MAVLink を返す偽物の機体を相手に最後まで動くことを確かめた
- 図2枚は `python3 tools/make_ros_figures.py`、写真は `python3 tools/fetch_photos.py ros` で作る

### 🐙 GitHub の教科書（books/github）

- 2026-11-14 に、ラズパイピコ開発ガイドの「付録F. git と GitHub の使い方」を分けて作った。ピコのガイドの3章・4章は、ここへのリンクになっている
- コマンドの言葉の説明は `glossary.json`（ピコのガイドの `glossary.json` から、git・ssh・gh などを写したもの）
- 9章の VS Code の画面の図（`images/vscode-*.svg`、6枚）は `python3 tools/make_github_figures.py` で作る

### 🌍 アフリカの教科書（books/africa）

- 2026-11-14 に作った。数字と会社の状況は、そのときにウェブで調べたもの。出典は付録B（`b-sources.md`）にまとめ、直すときは出典も一緒に直す

### 🇬🇧 イギリスの教科書（books/uk）

- 2026-11-14 に、アフリカの教科書と同じ形（国のこと → 農業と酪農 → 参入するなら）で作った。数字・政治・会社の状況は、そのときにウェブで調べたもの。出典は付録B（`b-sources.md`）
- 写真は `photos.json` に並べ、`python3 tools/fetch_photos.py uk` で Wikimedia Commons から取ってくる。付録C（`c-photos.md`、写真の出典）もこれで作り直す

### 🛐 宗教の教科書（books/religion）

- 2026-11-15 に作った。信者の数は Pew Research Center の2020年の推計（2025年発表）にそろえ、日本は文化庁『宗教年鑑』と Pew の調査を並べている。出典は付録B（`b-sources.md`）
- 宗教の説明は「信じている人はこう考える」の形で書き、どれが正しいかは決めない。争いの話は、宗教だけでなく土地・民族・政治が重なることを書く
- 写真は `photos.json` と `python3 tools/fetch_photos.py religion`。本棚の分野は「文化」

### 🐍 Python の教科書（books/python）

- 2026-11-14 に作った。もとになるノートはなく、ほかの教科書（統計・機械学習）の前に読む入門として書いた
- コードは、NumPy・pandas・matplotlib を入れた仮想環境で、章ごとに上から実行して確かめた

### 📊 統計の教科書（books/stats）

- 2026-11-14 に、学習ノート [超基礎統計](https://note.com/k_1090/n/n920f21843b93)・[計量経済学の自分用まとめ](https://note.com/k_1090/n/n98bcfaa3190b)（見出しと画像だけのもの）をもとに、式と計算の例を足して作った
- 図5枚（`images/`）は `python3 tools/make_study_figures.py` で作る（式から計算したもの）

### 🤖 機械学習の教科書（books/ml）

- 2026-11-14 に、『Pythonではじめる機械学習』の [学習ノート](https://note.com/k_1090/n/nca53389e754b) をもとに作った。ノートの誤り（TPR は適合率ではなく再現率、`get_dummies` の列の選び方、PCA はテストデータにも使える、など）は直してある
- コードは scikit-learn 1.9 で確かめた（ロジスティック回帰の L1・L2 は `l1_ratio`、SVM の AUC は `decision_function`）
- 図4枚は `python3 tools/make_study_figures.py` で作る

### ⚙️ C++ の教科書（books/cpp）

- 2026-11-14 に、『やさしいC++ 第5版』の [学習ノート](https://note.com/k_1090/n/n9ca36fcc9a8a) をもとに作った。ノートの誤り（`case 値:` のコロン、クラスの宣言の `};`、戻り値の型だけのオーバーロードはできない、など）は直し、`std::string`・`std::vector` などの今の書き方を足した
- `main` のあるプログラムは、g++（`-std=c++17 -Wall`）でコンパイルと実行を確かめた

### 🐳 Docker の教科書（books/docker）

- 2026-11-14 に作った。VS Code（Container Tools・Dev Containers の拡張機能）で触る前提
- 図2枚（仮想マシンとの比較、Dockerfile からコンテナまで）は `python3 tools/make_study_figures.py` で作る
