# 8. NumPy（数の配列）

## この章でわかること

- NumPy の配列（ndarray）の作り方と、形・型
- for を使わない計算（ベクトル化）とブロードキャスト
- 集計と axis、取り出し方（スライス・条件）
- 行列の計算と乱数

NumPy は、数の配列をまとめて速く計算するライブラリです。pandas・matplotlib・scikit-learn も、中で NumPy を使っています。

```python
import numpy as np
```

## 配列を作る

```python
a = np.array([32.5, 28.0, 35.2, 25.8])          # リストから
m = np.array([[1, 2, 3], [4, 5, 6]])             # 2次元（2行3列）

print(a.shape, m.shape)      # (4,) (2, 3)  形
print(m.ndim, m.size)        # 2 6          次元の数・要素の数
print(a.dtype, m.dtype)      # float64 int64  型（全部の要素が同じ型）
```

| 関数 | 作るもの | 例 |
| --- | --- | --- |
| `np.zeros(形)` / `np.ones(形)` | 0 / 1 だらけ | `np.zeros((2, 3))` |
| `np.arange(始め, 終わり, 間隔)` | 等間隔（終わりは入らない） | `np.arange(0, 10, 2)` → `[0 2 4 6 8]` |
| `np.linspace(始め, 終わり, 個数)` | 個数を決めて等間隔（終わりも入る） | `np.linspace(0, 1, 5)` → `[0. 0.25 0.5 0.75 1.]` |
| `np.full(形, 値)` | 同じ値 | `np.full(3, 7)` |

## まとめて計算する

NumPy の配列は、`for` を書かずに、全部の要素をまとめて計算できます（**ベクトル化**）。リストを `for` で回すより、ずっと速く動きます。

```python
a = np.array([32.5, 28.0, 35.2, 25.8])
print(a * 2.2046)            # 全部をポンドに
print(a - a.mean())          # 平均との差
print(np.sqrt(a))            # 全部の平方根
print(a >= 30)               # [ True False  True False]
```

> リストの `*` は意味がちがいます。`[1, 2] * 2` は `[1, 2, 1, 2]`（くり返し）、`np.array([1, 2]) * 2` は `[2 4]` です。

### ブロードキャスト

形のちがう配列どうしでも、足りない向きをのばして計算してくれます。

```python
milk = np.array([[30, 32, 31],      # 牛ごと（行）× 日ごと（列）
                 [25, 27, 26]])
bonus = np.array([1, 0, 2])         # 日ごとの補正（3列ぶん）
print(milk + bonus)                 # 各行に [1, 0, 2] が足される
```

## 集計と axis

```python
milk = np.array([[30, 32, 31],
                 [25, 27, 26]])
print(milk.sum(), milk.mean(), milk.max())     # 全体: 171 28.5 32
print(milk.mean(axis=0))                       # 縦にまとめる（日ごと）: [27.5 29.5 28.5]
print(milk.mean(axis=1))                       # 横にまとめる（牛ごと）: [31. 26.]
print(milk.argmax(axis=1))                     # 牛ごとに一番多い日の番号: [1 1]
```

`axis=0` は「行の向きにつぶす（列ごとの結果）」、`axis=1` は「列の向きにつぶす（行ごとの結果）」です。`std`（標準偏差）・`min`・`argmin` なども同じです。

## 取り出す

```python
m = np.array([[1, 2, 3],
              [4, 5, 6]])
print(m[1, 2])        # 6（1行目・2列目。0 から数える）
print(m[0])           # [1 2 3]（0行目）
print(m[:, 1])        # [2 5]（全部の行の 1列目）
print(m[:, 1:])       # 1列目から後ろ

a = np.array([32.5, 28.0, 35.2, 25.8])
print(a[a >= 30])                    # 条件に合うものだけ: [32.5 35.2]
print(np.where(a >= 30, "多", "少")) # 条件で値を選ぶ
```

> スライス（`m[:, 1:]`）で取り出したものは、もとの配列と中身を共有しています。変えるともとも変わるので、別にしたいときは `.copy()` を付けます。

## 形を変える・行列の計算

```python
x = np.arange(6)            # [0 1 2 3 4 5]
y = x.reshape(2, 3)         # 2行3列に
print(y.T)                  # 転置（3行2列）
print(y @ y.T)              # 行列の積（@）
```

`*` は要素ごとのかけ算、`@` は行列の積です。

## 乱数

```python
rng = np.random.default_rng(0)            # 0 は種（同じ種なら毎回同じ乱数）
print(rng.normal(30, 3, size=5))          # 平均 30・標準偏差 3 の正規分布から 5 つ
print(rng.integers(1, 7, size=10))        # 1〜6 の整数（サイコロ）
print(rng.choice(["A", "B", "C"], size=3))
```

正規分布などの分布は、「統計の教科書」の5章で説明しています。

## まとめ

- `np.array` で作る。`shape`（形）と `dtype`（型）を見る
- `for` を書かずに `a * 2`・`a - a.mean()` のようにまとめて計算する
- 集計の `axis=0` は列ごと、`axis=1` は行ごと
- `m[行, 列]`・`a[a >= 30]` で取り出す。`@` は行列の積
- 乱数は `np.random.default_rng(種)` から

## 練習問題

```quiz
Q: 次のコードは何を表示しますか。
| import numpy as np
| a = np.array([[1, 2, 3], [4, 5, 6]])
| print(a.shape)
A: (2, 3) | 2, 3 | 2 3
E: 2行3列です。

Q: 次のコードは何を表示しますか。
| import numpy as np
| a = np.array([[1, 2, 3], [4, 5, 6]])
| print(a.sum(axis=0))
A: [5 7 9] | 5 7 9 | 5, 7, 9
E: `axis=0` は列ごと（縦に）足します。

Q: 次のコードは何を表示しますか。
| import numpy as np
| a = np.array([28, 35, 31, 26])
| print(a[a >= 30])
A: [35 31] | 35 31 | 35, 31
E: 条件を入れると、条件に合う値だけを取り出せます。

Q: NumPy で行列の積を表す記号は何ですか。
A: @
E: `*` は同じ位置どうしのかけ算です。
```
