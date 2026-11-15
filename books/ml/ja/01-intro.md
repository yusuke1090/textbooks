# 1. 機械学習とは（アイリスの分類）

## この章でわかること

- 機械学習で解ける問題（教師あり・教師なし）
- モデルを作る前にデータを知ること
- scikit-learn の使い方の流れ（アイリスの分類）

この教科書は、『Pythonではじめる機械学習』（Andreas C. Müller・Sarah Guido 著、オライリー・ジャパン）を読んでまとめた [学習ノート](https://note.com/k_1090/n/nca53389e754b) をもとにしています。Python の書き方は「Python の教科書」を見てください。

## 機械学習で解ける問題

| 種類 | 何をするか | 例 |
| --- | --- | --- |
| 教師あり学習 | 答え（ラベル）の付いたデータから、答えを当てる規則を学ぶ | 手書きの数字を読む、腫瘍が良性か悪性かを判定する、不正な取引を見つける、牛の行動を判定する |
| 教師なし学習 | 答えのないデータから、まとまりや構造を見つける | 好みの似た客をグループに分ける、ブログの話題を見つける |

教師あり学習は、さらに2つに分かれます（2章・3章）。

- **分類**: 答えが種類（良性・悪性、歩く・寝る）
- **回帰**: 答えが数（乳量、風速、価格）

## タスクとデータを知る

モデルを作る前に、次のことを確かめます。

- 何を当てたいのか、答えのデータはあるか
- 必要なデータはそろっているか、要らないデータはどれか
- どのアルゴリズムが合いそうか

> 簡単な集計（平均やグラフ）だけで解ける問題もあります。いきなり機械学習を使わず、まずデータを見ます。

## なぜ Python か

- 最新のアルゴリズムが入ったライブラリが多い（scikit-learn、LightGBM、PyTorch など）
- 書きやすく、初心者にもわかりやすい
- 大きな会社も使っていて、開発と更新が活発

この教科書では **scikit-learn** を使います。入っているかは次で確かめます。

```python
import sklearn
print(sklearn.__version__)
```

入っていなければ `pip install scikit-learn`（Anaconda なら `conda install scikit-learn`）で入れます。

## アイリスの分類

アヤメ（iris）の花の4つの寸法から、3つの品種のどれかを当てます。答えの付いたデータから学ぶので、教師あり学習の分類です。

### データを読む

```python
from sklearn.datasets import load_iris

iris = load_iris()
print(iris.keys())           # data, target, target_names, feature_names, DESCR など
print(iris.feature_names)    # がくの長さ・幅、花弁の長さ・幅（cm）
print(iris.target_names)     # ['setosa' 'versicolor' 'virginica']
print(iris.data.shape)       # (150, 4): 150 本の花、4 つの特徴量
```

- 1つの花（1行）を**サンプル**、寸法の1つ1つ（列）を**特徴量**、当てたい品種を**ラベル**（目的変数）といいます

### 学習用とテスト用に分ける

学習に使ったデータで正解率を測っても、意味がありません（覚えているだけかもしれない）。学習に使わないデータを取っておき、それで確かめます。

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, random_state=0)
print(X_train.shape, X_test.shape)   # (112, 4) (38, 4): 75% と 25%
```

- 標準では 75% を学習用、25% をテスト用にする（`test_size` で変えられる）
- `random_state` は分け方を決める乱数の種。同じ数にすると、何回やっても同じ分け方になる

学ぶ前に、特徴量どうしの散布図（ペアプロット）でデータを見ておきます。花弁の長さと幅で、品種がよく分かれていることがわかります。

```python
import pandas as pd
import seaborn as sns

df = pd.DataFrame(X_train, columns=iris.feature_names)
df["target"] = y_train
sns.pairplot(df, hue="target")
```

seaborn は、matplotlib をもとにしたグラフのライブラリです（`pip install seaborn`）。

### k-最近傍法で学んで当てる

**k-最近傍法**（k-NN）は、新しいデータに一番近い $k$ 個の学習データを見て、多い品種を答えにする方法です。

```python
from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=1)   # 一番近い1つで決める
knn.fit(X_train, y_train)                   # 学ぶ
y_pred = knn.predict(X_test)                # 当てる
print("Test set score:", knn.score(X_test, y_test))   # 0.97（97% 当たった）
```

scikit-learn では、どのモデルも **作る → `fit` で学ぶ → `predict` で当てる → `score` で確かめる** の同じ流れで使えます。

## まとめ

- 教師あり学習（分類・回帰）と、教師なし学習がある
- まずデータを見る。集計だけで解けることもある
- データは学習用とテスト用に分け、テスト用で確かめる
- scikit-learn は「作る → fit → predict → score」の流れ

## 練習問題

```quiz
Q: 正解（ラベル）の付いたデータから学ぶ機械学習を何といいますか。
A: 教師あり学習 | 教師あり | supervised learning
E: 正解のないデータから学ぶのは、教師なし学習です。

Q: scikit-learn で、モデルにデータを学ばせるメソッドは何ですか。
A: fit | fit()
E: 「作る → fit → predict → score」の流れです。

Q: 学んだモデルで、新しいデータの答えを当てるメソッドは何ですか。
A: predict | predict()
E: 正解率などは `score` で出します。

Q: データを学習用ともう1つに分けて、モデルの確かめに使います。もう1つは何用ですか。
A: テスト用 | テスト | test
E: 学習に使っていないデータで確かめないと、本当の力はわかりません。

Q: いちばん近い $k$ 個のデータの多数決で当てる方法を何といいますか。
A: k-最近傍法 | k最近傍法 | k近傍法 | kNN | k-NN | k-nearest neighbors
E: アイリスの分類の例で使いました。
```
