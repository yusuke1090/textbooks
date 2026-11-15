# 3. 分類のモデル

2つのうちどちらかを当てるものを **2値分類**（不良品か良品か、異常な取引か、良性か悪性か）といいます。この章では、scikit-learn の乳がんのデータ（腫瘍が良性か悪性か）で、モデルを比べます。評価に使う ROC 曲線と AUC は、7章でくわしく説明します。

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
```

`stratify=y` で、学習用とテスト用の良性・悪性の割合をそろえます。

## ロジスティック回帰

名前に「回帰」と付きますが、**分類**のモデルです。特徴量の重み付きの和を、シグモイド関数で 0〜1 の確率に変えます。

$$P(y = 1 \mid x) = \frac{1}{1 + e^{-(w \cdot x + b)}}$$

- $w \cdot x$ は重みと特徴量の内積、$b$ は切片
- 確率がしきい値（ふつう 0.5）を超えたら 1 と判定する
- 重みを見れば、どの特徴量がどちらの向きに効くかがわかる（説明しやすい）

```python
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=10000))
model.fit(X_train, y_train)
prob = model.predict_proba(X_test)[:, 1]     # 1 である確率
print("AUC:", roc_auc_score(y_test, prob))
```

> **AUC には、ラベルではなく確率を渡します。** `roc_auc_score(y_test, model.predict(X_test))` のように 0/1 のラベルを渡すと、しきい値を1つに決めた値になり、AUC が低く出ます（元のノートでは 0.9977 が 0.9464 になった）。

## サポートベクトルマシン（SVM）

2つのクラスの間に、一番すき間（**マージン**）が大きくなる境界を引きます。境界に一番近いデータを**サポートベクトル**といい、境界はこれだけで決まります。

- **カーネル法**: 特徴量の2乗などを足した高い次元で考えることで、曲がった境界も引ける。まずは RBF カーネルを試す
- 主な設定: `C`（大きいほど誤りを許さず、境界が複雑になる）と `gamma`（大きいほど細かい境界になる）。どちらも大きすぎると過学習
- 特徴量の大きさの差に弱いので、標準化（4章）が必須

```python
from sklearn.svm import SVC

svm = make_pipeline(StandardScaler(), SVC(kernel="rbf", C=1.0))
svm.fit(X_train, y_train)
print("AUC:", roc_auc_score(y_test, svm.decision_function(X_test)))
```

SVM は確率を出さないので、AUC には境界からの距離（`decision_function`）を渡します。AUC は「1 らしさ」の順番だけを見るので、確率でなくても計算できます（0/1 のラベルはだめ）。

## 決定木

「特徴量 A が 3.5 以下か」のような Yes/No の質問を重ねて、木の形で分けていきます。

| 名前 | 意味 |
| --- | --- |
| ルートノード | 一番上。最初の質問 |
| 内部ノード | 途中の質問 |
| 枝 | ノードをつなぐ線（Yes / No） |
| リーフノード（葉） | 一番下。最後の答え |

- 判断の流れが図でわかるので、説明しやすい。標準化はいらない
- 深くするといくらでも学習データに合わせられ、過学習しやすい。`max_depth`（深さの上限）や `min_samples_split`（分けるのに要るサンプル数）で抑える

```python
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import classification_report

tree = DecisionTreeClassifier(max_depth=5, min_samples_split=10, random_state=42)
tree.fit(X_train, y_train)
print(classification_report(y_test, tree.predict(X_test)))
plot_tree(tree, filled=True, rounded=True, max_depth=2)   # 上の2段だけ描く
```

`classification_report` の適合率・再現率・F1 は、7章で説明します。

## ランダムフォレスト

少しずつちがう決定木をたくさん作り、その多数決（確率の平均）で答えます。1本の木より過学習しにくく、設定もあまり要らないので、まず試すとよいモデルです。

- 木ごとにちがうデータを使う: 学習データから、同じものを何度選んでもよいとして同じ数だけ選び直す（**ブートストラップ**。例: [1, 2, 3, 4] → [2, 2, 3, 3]）
- 木の分かれ目ごとに、使える特徴量をランダムに絞る（`max_features`）
- 主な設定: 木の数 `n_estimators`（多いほど安定、遅くなる）

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

rf = RandomForestClassifier(n_estimators=100, random_state=1)
scores = cross_val_score(rf, X_train, y_train, cv=5, scoring="roc_auc")
print("交差検証の AUC:", scores.mean().round(3), "±", scores.std().round(3))
rf.fit(X_train, y_train)
```

テストデータで AUC がちょうど 1 になるようなときは、たまたまかもしれません。交差検証（7章）で、分け方を変えても成績が安定しているかを確かめます。

学んだモデルからは、どの特徴量が判定に効いたか（**特徴量の重要度**）がわかります。

```python
import pandas as pd
names = load_breast_cancer().feature_names
imp = pd.Series(rf.feature_importances_, index=names).sort_values()
imp.tail(10).plot.barh(title="Feature Importance using Random Forest")
```

## 勾配ブースティング

浅い木（弱い学習器）を順番に作り、前の木の誤りを次の木が直していきます。設定がうまく合うとランダムフォレストより当たることが多い一方、設定に敏感で、学ぶのに時間がかかります。まずランダムフォレストを試し、もっと詰めたいときに使います。

- `n_estimators`: 木の数
- `learning_rate`: 1本の木がどれだけ直すか。小さいほど慎重（木を多く要る）
- `max_depth`: 木の深さ（浅く、2〜5 くらい）

```python
from sklearn.ensemble import GradientBoostingClassifier

gb = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=1)
gb.fit(X_train, y_train)
print("AUC:", roc_auc_score(y_test, gb.predict_proba(X_test)[:, 1]))
```

### LightGBM

マイクロソフトが 2016 年に公開した、速い勾配ブースティングです（`pip install lightgbm`）。分け目をヒストグラムで探し、伸ばすとよい葉だけを伸ばすことで速くしています。大きなデータの表形式の問題では、今もよく使われます。

```python
import lightgbm as lgb

lgbm = lgb.LGBMClassifier(n_estimators=100, learning_rate=0.1, random_state=1)
lgbm.fit(X_train, y_train)
print("AUC:", roc_auc_score(y_test, lgbm.predict_proba(X_test)[:, 1]))
```

## モデルの選び方の目安

| モデル | 強み | 弱み・注意 |
| --- | --- | --- |
| ロジスティック回帰 | 速い。重みで説明しやすい。直線で分けられるデータに強い | 曲がった境界は苦手。標準化する |
| SVM | 曲がった境界も引ける | 標準化が必須。大きなデータでは遅い |
| 決定木 | 図で説明できる。標準化不要 | 過学習しやすい |
| ランダムフォレスト | 設定が少なくて丈夫。重要度がわかる | 中身は説明しにくい |
| 勾配ブースティング・LightGBM | よく当たる | 設定に敏感。過学習に注意 |

## 多クラス分類とニューラルネットワーク

- 3つ以上に分ける**多クラス分類**（アイリスの品種など）も、ここまでのモデルの多くでそのまま使える。scikit-learn が内部で「1つのクラス 対 それ以外」などに分けて扱う
- 評価は混同行列と、多クラスの F1（7章）で見る
- ニューラルネットワーク（`sklearn.neural_network.MLPClassifier`）も使える。画像や音声のような大きなデータでは、PyTorch などの深層学習のライブラリを使う

## まとめ

- ロジスティック回帰は確率を出す分類のモデル。AUC には確率を渡す
- SVM はマージンを最大にする。カーネルで曲がった境界、標準化が必須
- 決定木は説明しやすいが過学習しやすい。ランダムフォレストは木の多数決で丈夫
- 勾配ブースティング・LightGBM は前の木の誤りを直していく。よく当たるが設定に注意
- まずロジスティック回帰とランダムフォレストを試し、比べてから詰める

## 練習問題

```quiz
Q: SVM が最大にする、境界と一番近いデータとの間の幅を何といいますか。
A: マージン | margin
E: SVM は標準化が必須です。

Q: 決定木をたくさん作って、多数決で当てるモデルを何といいますか。
A: ランダムフォレスト | random forest
E: 1本の決定木より過学習しにくく、丈夫です。

Q: AUC を計算するとき、`predict` の結果（ラベル）ではなく何を渡しますか。
A: 確率 | かくりつ | probability | predict_proba
E: ロジスティック回帰は確率を出せる分類のモデルです。

Q: 前の木の誤りを直すように、木を順に足していく方法を何といいますか。
A: 勾配ブースティング | ブースティング | gradient boosting
E: LightGBM もこの仲間です。よく当たりますが、設定に注意が要ります。
```
