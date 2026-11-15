# 6. 特徴量エンジニアリング

特定のアルゴリズムに合う、一番よいデータの表し方を探すことを**特徴量エンジニアリング**といいます。モデルを変えるより、特徴量を工夫するほうが成績が上がることもよくあります。

## 特徴量の種類

| 種類 | 値 | 例 |
| --- | --- | --- |
| 連続データ | どんな数でもとれる | 気温、長さ、重さ、時間 |
| 離散データ | とびとびの数 | 回数、サイコロの目 |
| カテゴリーデータ | 順番のないラベル | 血液型、品種、色 |

連続データはスケール変換（4章）を、カテゴリーデータは次のダミー変数を使って、モデルが扱える数にします。

## ダミー変数（one-hot）

カテゴリーを、「そのカテゴリーなら 1、ちがえば 0」の列に分けます。

```python
import pandas as pd

df = pd.DataFrame({"color": ["red", "blue", "green", "blue", "red"],
                   "size": ["S", "M", "L", "M", "S"]})
print(pd.get_dummies(df[["color", "size"]]).astype(int))
```

| color_blue | color_green | color_red | size_L | size_M | size_S |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 0 | 0 | 1 |
| 1 | 0 | 0 | 0 | 1 | 0 |

- 複数の列を選ぶときは `df[["color", "size"]]`（角かっこを二重にする）
- 線形回帰などでは、全部の列を入れると「どれか1つが必ず 1」という一直線の関係ができる（多重共線性）。`drop_first=True` で1列減らす
- 学習用とテスト用で列がそろうように、scikit-learn の `OneHotEncoder(handle_unknown="ignore")` を使う方法もある

## ビニング

連続データを、区間（ビン）に区切ってカテゴリーにします。直線のモデルでも、曲がった関係を表せるようになります。

```python
import numpy as np
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(0)
X = rng.uniform(0, 10, size=(100, 1))
y = 2 * np.sin(X).ravel() + rng.normal(0, 0.5, 100)     # 曲がった関係

kb = KBinsDiscretizer(n_bins=5, encode="onehot-dense", strategy="uniform")
X_bin = kb.fit_transform(X)
print(LinearRegression().fit(X, y).score(X, y))          # 直線のまま: 低い
print(LinearRegression().fit(X_bin, y).score(X_bin, y))  # ビンにすると: 上がる
```

pandas でも区切れます。

| 関数 | 区切り方 | 使うとき |
| --- | --- | --- |
| `pd.cut(x, bins=[0, 3, 6, 9])` | 決めた境目で区切る（標準では左を含まず右を含む） | 境目を自分で決めたいとき。範囲の外は NaN になる |
| `pd.qcut(x, q=3)` | それぞれの区間に同じくらいの数が入るように区切る | 数をそろえたいとき。同じ値が別のビンに分かれることがある |

## 指標スコア（目的変数を使った変換）

2値分類で、特徴量の区間（またはカテゴリー）ごとに、目的変数の割合から作る数です。目的が 1 のもの（不正・異常など）を「黒」、0 のものを「白」と呼びます。

1. 特徴量をビンに分ける（性別のようなカテゴリーならそのまま）
2. ビンごとに、黒と白の割合を数える
3. 黒の割合を白の割合で割り、自然対数をとる

$$\text{指標スコア} = \ln \frac{\text{ビンの中の黒の割合}}{\text{ビンの中の白の割合}}$$

- 黒が多いビンほど大きな値になり、対数をとるので、ロジスティック回帰のような直線のモデルとよく合う
- 目的変数を使って作るので、**学習用データだけで計算する**（テストデータを使うと答えをカンニングしたことになる）。データが少ないビンは値が不安定になるので、ビンをまとめる

```python
import numpy as np
import pandas as pd

def index_score(x, y, bins):
    """ビンごとの ln(黒の割合 / 白の割合)。x: 特徴量、y: 0/1 の目的変数（学習用データ）"""
    b = pd.cut(x, bins, right=False)
    t = pd.crosstab(b, y, normalize="index")      # ビンごとの白(0)・黒(1)の割合
    return np.log(t[1] / t[0])
```

## 特徴量の選び方

特徴量が多すぎると、過学習・多重共線性・説明のしにくさが問題になります。

### 単変量で見る

特徴量を1つずつ使ってモデルを作り、効き方（重み・$R^2$・AUC など）を比べます。簡単ですが、1つずつ見るので、ほかの変数とのからみ（統計の教科書の8章の欠落変数バイアス）は見えません。

### 重要度で選ぶ

ランダムフォレストの `feature_importances_`（3章）を見て、重要度の低いものを外します。アイリスでは、花弁の幅（約 0.48）・花弁の長さ（約 0.42）が高く、がくの長さ（約 0.08）・がくの幅（約 0.02）は低くなります。

### ステップワイズ法

特徴量を1つずつ足したり外したりして、成績が一番よくなる組み合わせを自動で探します。scikit-learn では、交差検証と組み合わせた `RFECV`（重要度の低いものから順に外す）が使えます。

```python
from sklearn.datasets import load_iris
from sklearn.feature_selection import RFECV
from sklearn.ensemble import RandomForestClassifier

iris = load_iris()
rfecv = RFECV(RandomForestClassifier(random_state=42), step=1, cv=5, scoring="accuracy")
rfecv.fit(iris.data, iris.target)
print("選ばれた特徴量:", [n for n, s in zip(iris.feature_names, rfecv.support_) if s])
```

自動なので楽ですが、相関の高い特徴量があると大事なものを外すことがあります。結果を見て、必要なものを手で足します。

### 正則化で選ぶ

L1 正則化（Lasso、2章）は、効かない特徴量の重みを 0 にします。重みが 0 でないものだけを残せば、特徴量を選べます。

```python
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

X_s = StandardScaler().fit_transform(iris.data)       # 重みを比べるので標準化する
sel = SelectFromModel(LogisticRegression(l1_ratio=1, solver="saga", C=0.5, max_iter=10000))
sel.fit(X_s, iris.target)
print("残った特徴量:", [n for n, s in zip(iris.feature_names, sel.get_support()) if s])
# がくの長さが外れ、ほかの 3 つが残る
```

> scikit-learn 1.8 から、ロジスティック回帰の L1 は `l1_ratio=1`（L2 は `0`）で指定します。1.7 までは `penalty="l1"` と書きました。

## まとめ

- 連続はスケール変換、カテゴリーはダミー変数。ビニングで曲がった関係も直線のモデルで表せる
- 指標スコアは目的変数の割合から作る。学習用データだけで計算する
- 特徴量は、単変量・重要度・ステップワイズ（RFECV）・L1 正則化で選ぶ。自動の結果は人が確かめる

## 練習問題

```quiz
Q: カテゴリーの値を、0 と 1 の列に分けて表す変数を何といいますか。
A: ダミー変数 | ダミー | one-hot | ワンホット
E: pandas の `get_dummies` で作れます。

Q: 連続の値をいくつかの区間に分けることを何といいますか。
A: ビニング | binning | ビン分割
E: 曲がった関係も、直線のモデルで表せるようになります。

Q: 目的変数の割合から作る指標スコアは、どのデータだけで計算しますか。
A: 学習用 | 学習 | 学習用データ | training | train
E: テスト用の答えを使うと、答えが漏れてしまいます。

Q: 交差検証で特徴量を1つずつ減らして選ぶ、scikit-learn のクラスは何ですか。
A: RFECV
E: ステップワイズ法の一つです。自動の結果は人が確かめます。
```
