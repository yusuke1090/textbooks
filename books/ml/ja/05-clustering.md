# 5. クラスタリング

## この章でわかること

- k-means・凝集型クラスタリング・DBSCAN のしくみと使い方
- それぞれの長所と短所
- クラスタリングの評価（ARI など）

似たデータを集めて、グループ（**クラスタ**）に分けることを**クラスタリング**といいます。答えのない教師なし学習です。

## k-means

1. クラスタの数 $k$ を決め、中心を $k$ 個置く
2. それぞれのデータを、一番近い中心のクラスタに入れる
3. クラスタごとに平均をとり、それを新しい中心にする
4. 中心が動かなくなるまで 2〜3 をくり返す

```python
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans

X, y_true = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)
km = KMeans(n_clusters=4, n_init=10, random_state=0)
labels = km.fit_predict(X)
print(km.cluster_centers_)       # 4 つの中心
```

`make_blobs` は、かたまりのある練習用のデータを作る関数です（`n_samples`: 点の数、`centers`: かたまりの数、`cluster_std`: かたまりの広がり）。

## 凝集型クラスタリング

最初は1点ずつを1つのクラスタとし、一番似たクラスタ同士を順に合わせていきます。合わせた順を木の形にしたものを**デンドログラム**といいます。

- 木をどの高さで切るかで、クラスタの数が決まる。高い所で切ると、少ない大きなクラスタになる
- 合わせ方（ward・average・complete など）で結果が変わる。ward は、合わせたときにクラスタの中のばらつきの増え方が一番小さい組を選ぶ

```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import linkage, dendrogram

labels = AgglomerativeClustering(n_clusters=4).fit_predict(X)
Z = linkage(X, method="ward")            # 合わせた順の記録
dendrogram(Z, truncate_mode="level", p=5, no_labels=True)
```

## DBSCAN

点が密に集まっている所をクラスタとし、まわりにほかの点が少ない点は**ノイズ**（外れ値）とします。

- `eps`: 近くとみなす半径
- `min_samples`: 半径 `eps` の中にこれだけの点があれば、密な点（コア点）とする
- コア点からたどれる点は同じクラスタ。どこにも入らない点はノイズ（ラベル −1）
- クラスタの数を決めなくてよく、曲がった形のクラスタも見つけられる。距離を使うので、先に標準化する

```python
from sklearn.datasets import make_moons
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

X, _ = make_moons(n_samples=200, noise=0.08, random_state=0)    # 2つの三日月の形
labels = DBSCAN(eps=0.3, min_samples=5).fit_predict(StandardScaler().fit_transform(X))
print(sorted(set(labels.tolist())))       # [-1, 0, 1]: 2つのクラスタと、ノイズ（-1）
```

k-means では、この三日月を2つにうまく分けられません（中心からの距離で、丸く分けるため）。

## 3つの方法の比べ方

| 方法 | 長所 | 短所 |
| --- | --- | --- |
| k-means | 簡単で速い。大きなデータでも使える | $k$ を先に決める必要がある。丸い・同じくらいの大きさのクラスタを前提とする。最初の中心で結果が変わる |
| 凝集型 | デンドログラムで階層がわかる。木を切る高さで数を後から選べる | 大きなデータでは時間とメモリがかかる。一度合わせたら戻せない |
| DBSCAN | 数を決めなくてよい。どんな形でも見つかる。外れ値がわかる | `eps` と `min_samples` を決めるのが難しい。密度がばらばらなデータや高い次元に弱い |

## クラスタリングの評価

### 答えがあるとき

クラスタの番号（0, 1, 2…）には意味がないので、正解率（accuracy）では比べられません。番号の付け方によらない指標を使います。

| 指標 | 範囲 | 意味 |
| --- | --- | --- |
| ARI（調整ランド指数） | 1 が完全に一致、0 がでたらめと同じ | 2つの分け方が、どれだけ同じ組み合わせを同じクラスタに入れているか |
| NMI（正規化相互情報量） | 0〜1 | 一方がわかると、もう一方がどれだけわかるか |

```python
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score

X, y_true = make_blobs(n_samples=100, centers=3, cluster_std=0.60, random_state=0)
pred = KMeans(n_clusters=3, n_init=10, random_state=0).fit_predict(X)
print("ARI:", adjusted_rand_score(y_true, pred))
print("NMI:", normalized_mutual_info_score(y_true, pred))
```

### 答えがないとき

- 実際の場面では答えがないことがほとんど。クラスタの中身を見て、意味のある分け方かを人が確かめる
- シルエット係数（`silhouette_score`）で、クラスタのまとまり具合を数字で見ることもできる。ただし、数字がよい分け方が、役に立つ分け方とは限らない

### 顔画像での例（元のノートより）

顔画像を PCA で 100 成分にしてから、3つの方法を試しました。

- DBSCAN は、標準の設定では全部がノイズになった。`eps` を調整すると、カメラに近すぎる顔や、眼鏡・帽子の顔がノイズとして見つかった
- k-means と凝集型（それぞれ 10 クラスタ）は、クラスタの大きさの分かれ方がちがい、2つの結果の ARI は 0.09 とほとんど一致しなかった
- 凝集型を 40 クラスタにすると、笑顔・横向き・眼鏡のように、見た目の特徴でまとまるクラスタが見つかった

## まとめ

- k-means は中心に近いものを集める。$k$ を決め、丸いクラスタが得意
- 凝集型は似たものを順に合わせ、デンドログラムで数を選べる
- DBSCAN は密な所をクラスタにし、外れ値も見つける。標準化して `eps` を調整する
- 答えがあれば ARI・NMI で比べる。なければ中身を見て確かめる。2〜3 の方法を試して比べるとよい

## 練習問題

```quiz
Q: 中心に近いものを集めて $k$ 個のクラスタに分ける方法は何ですか。
A: k-means | kmeans | k平均法 | k-平均法
E: 丸いクラスタが得意で、$k$ を先に決めます。

Q: 凝集型クラスタリングで、合わせていく順番を木の形で表した図を何といいますか。
A: デンドログラム | 樹形図 | dendrogram
E: 図を見て、クラスタの数を選べます。

Q: 密な所をクラスタにし、外れ値も見つける方法は何ですか。
A: DBSCAN
E: 標準化して `eps` を調整します。

Q: 答えがあるときに、クラスタリングの結果と比べる指標を、アルファベット3文字で1つ答えてください。
A: ARI | NMI
E: ARI か NMI で比べます。答えがないときは中身を見て確かめます。
```
