# 4. 前処理と次元削減

## この章でわかること

- 教師なし学習の2つの使い方
- スケール変換（標準化・正規化など）と、学習用・テスト用で同じ変換をすること
- 主成分分析（PCA）・NMF・t-SNE

## 教師なし学習とは

答え（ラベル）を使わずに、データだけから何かを取り出すのが教師なし学習です。

| 種類 | すること | 例 |
| --- | --- | --- |
| データの変換 | 扱いやすい形にする。教師あり学習の前処理にも使う | スケール変換、次元削減 |
| クラスタリング | 似たものをまとめる（5章） | 客のグループ分け、顔画像の分類 |

答えがないので、「うまくいったか」を数字で確かめにくいのが難しいところです。データを見ながら、探るように使います。

## スケール変換

特徴量の大きさ（単位）がばらばらだと、SVM・k-NN・ロジスティック回帰・PCA などは大きい特徴量に引っ張られます。そこで大きさをそろえます。

| 変換 | 式 | 結果 |
| --- | --- | --- |
| StandardScaler（標準化） | $(x - \mu) / \sigma$ | 平均 0、標準偏差 1 |
| MinMaxScaler | $(x - \min) / (\max - \min)$ | 0〜1 の範囲 |
| RobustScaler | $(x - \text{中央値}) / \text{IQR}$ | 外れ値に強い（IQR は 75% 点 − 25% 点） |
| Normalizer（正規化） | $x / \lVert x \rVert$ | サンプル（行）ごとに長さを 1 にする。文章のデータなど |

> 決定木・ランダムフォレスト・勾配ブースティングは、分け目で判断するのでスケール変換はいりません。目的変数（$y$）は、ふつう変換しません。

### 学習用とテスト用を同じように変換する

変換の基準（平均や最小・最大）は、**学習用データだけ**で決めて（`fit`）、同じ基準でテスト用データも変換します（`transform`）。

- テスト用を別に `fit` すると、2つのデータが別々の物差しで測られ、元の分布の関係がくずれる
- 先にデータを分けてから、変換を決める（全体で `fit` すると、テストの情報が学習にもれる）
- そのため、テスト用データは 0〜1 からはみ出すことがある。それで正しい

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

scaler = StandardScaler().fit(X_train)        # 学習用だけで基準を決める
X_train_s = scaler.transform(X_train)
X_test_s = scaler.transform(X_test)          # 同じ基準でテスト用も

print("そのまま:", SVC(C=100).fit(X_train, y_train).score(X_test, y_test))
print("標準化後:", SVC(C=100).fit(X_train_s, y_train).score(X_test_s, y_test))
```

元のノートでは、標準化で正解率が 0.94 から 0.96 に上がりました。`make_pipeline(StandardScaler(), SVC())` のようにパイプラインにすると、この手順を間違えずにできます（3章）。

## 主成分分析（PCA）

たくさんの特徴量を、情報（ばらつき）をなるべく残したまま、少ない数の新しい特徴量（**主成分**）にまとめます。

1. 特徴量の共分散行列を作る
2. その固有値と固有ベクトルを求める
3. 固有値（その方向のばらつき）が大きい順に、固有ベクトルの方向を主成分にする

- 30 個の特徴量の組み合わせを全部散布図で見ると 435 枚になるが、主成分2つにすれば1枚で見られる
- 主成分は元の特徴量の組み合わせなので、意味の解釈は難しい
- 大きさに引っ張られるので、先に標準化する

```python
from sklearn.decomposition import PCA

X_s = StandardScaler().fit_transform(X)
pca = PCA(n_components=2).fit(X_s)
X_pca = pca.transform(X_s)
print(X_s.shape, "→", X_pca.shape)                 # (569, 30) → (569, 2)
print("説明できたばらつきの割合:", pca.explained_variance_ratio_)
print(pca.components_.shape)                        # (2, 30): 主成分ごとの元の特徴量の重み
```

- 教師あり学習の前処理にも使える。そのときも、学習用で `fit` し、テスト用は `transform` するだけ
- `whiten=True` にすると、主成分ごとの大きさもそろえる（白色化）

元のノートでは、顔画像（Labeled Faces in the Wild、1枚が数千画素）の 1-NN の正解率が、画素のままでは 22%、PCA（100 成分・白色化）を通すと 30% に上がりました。

## 非負値行列因子分解（NMF）

値がすべて 0 以上のデータ（画像の明るさ、音、単語の数など）を、0 以上の2つの行列の積に分けます。

$$V \approx W H \qquad (V: m \times n,\; W: m \times r,\; H: r \times n)$$

- $r$ が成分の数。成分は「部品」のように足し合わせるだけ（引き算がない）なので、顔なら目・鼻のような部分、文章なら話題のような、意味のわかる成分になりやすい

```python
from sklearn.decomposition import NMF

nmf = NMF(n_components=15, init="nndsvd", max_iter=2000, random_state=0)
W = nmf.fit_transform(X)       # サンプルごとの、成分の量
H = nmf.components_            # 成分（部品）
```

## t-SNE

高い次元のデータが、実は低い次元の曲がった面（**多様体**）の上にあると考え、それを2次元に広げて見せる方法です（多様体学習）。

1. 高い次元で、点どうしの近さを確率で表す
2. 2次元でも、近さを確率で表す
3. 2つの確率の分布の差（KL 情報量）が小さくなるように、2次元の点を動かす

- 近いもの同士の関係を、よく残す。手書きの数字（`load_digits`）では、PCA では重なる数字が、t-SNE ではきれいに分かれる
- 新しいデータには使えない（`transform` がない）ので、データを**見る・探る**ためのもの。教師あり学習の前処理には使わない
- 大きなデータでは時間がかかる

```python
from sklearn.datasets import load_digits
from sklearn.manifold import TSNE

digits = load_digits()
X_tsne = TSNE(random_state=42).fit_transform(digits.data)
# X_tsne の2列を散布図にして、digits.target で色分けする
```

## まとめ

- 教師なし学習は、データの変換とクラスタリングに大きく分かれる
- スケール変換は学習用で fit し、同じ変換をテスト用にも使う。木のモデルにはいらない
- PCA はばらつきの大きい方向にまとめる。先に標準化する
- NMF は 0 以上の部品に分ける。t-SNE は見るための2次元の地図で、新しいデータには使えない

## 練習問題

```quiz
Q: スケール変換の `fit` は、学習用とテスト用のどちらのデータで行いますか。
A: 学習用 | 学習 | 訓練用 | training | train
E: 学習用で fit した同じ変換を、テスト用にも使います。

Q: ばらつきの大きい方向にデータをまとめる方法を、アルファベット3文字で何といいますか。
A: PCA | 主成分分析
E: 先に標準化しておきます。

Q: データを 0 以上の部品に分ける方法を、アルファベット3文字で何といいますか。
A: NMF | 非負値行列因子分解
E: 部品が足し算で組み合わさる、と考えるときに向きます。

Q: スケール変換がいらないモデルは、何を使ったモデルですか。
A: 木 | 決定木 | tree | trees
E: 決定木やランダムフォレストは、値の大きさの順だけを見るからです。
```
