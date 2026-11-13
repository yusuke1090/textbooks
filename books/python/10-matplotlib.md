# 10. matplotlib（グラフ）

## この章でわかること

- 図（Figure）と軸（Axes）の考え方
- 折れ線・散布図・棒・ヒストグラム・箱ひげ図
- 日本語の表示、複数のグラフを並べる、画像に保存する

```python
import matplotlib.pyplot as plt
```

## 図と軸

matplotlib では、**Figure**（図全体の紙）の上に、**Axes**（1つのグラフ）を置いて描きます。`plt.subplots()` で両方を作り、`ax` に描くのが今のふつうの書き方です。

```python
import numpy as np

days = np.arange(1, 31)
milk = 30 + 3 * np.sin(days / 5) + np.random.default_rng(0).normal(0, 0.8, 30)

fig, ax = plt.subplots(figsize=(6, 3.5))      # 横 6・縦 3.5 インチ
ax.plot(days, milk, marker="o", label="Hanako")
ax.set_xlabel("Day")
ax.set_ylabel("Milk (kg)")
ax.set_title("Daily milk yield")
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()                            # 文字が重ならないように整える
plt.show()                                    # 画面に出す
```

## いろいろなグラフ

| グラフ | 書き方 | 向いているもの |
| --- | --- | --- |
| 折れ線 | `ax.plot(x, y)` | 時間の変化 |
| 散布図 | `ax.scatter(x, y)` | 2つの数の関係 |
| 棒 | `ax.bar(名前, 値)`（横向きは `barh`） | 種類ごとの比較 |
| ヒストグラム | `ax.hist(値, bins=10)` | 分布（どのあたりに多いか） |
| 箱ひげ図 | `ax.boxplot([値1, 値2])` | 分布の比較、外れ値 |

```python
rng = np.random.default_rng(1)
parity = rng.integers(1, 5, 50)
milk = 25 + 2.5 * parity + rng.normal(0, 3, 50)

fig, axes = plt.subplots(1, 3, figsize=(11, 3.2))    # 1行3列に並べる
axes[0].scatter(parity, milk, alpha=0.6)
axes[0].set_xlabel("Parity"); axes[0].set_ylabel("Milk (kg)")
axes[1].hist(milk, bins=10, edgecolor="white")
axes[1].set_xlabel("Milk (kg)")
axes[2].bar(["A", "B", "C"], [31.2, 28.5, 33.0])
axes[2].set_ylabel("Mean milk (kg)")
fig.tight_layout()
plt.show()
```

`plt.subplots(行, 列)` で並べると、`axes` は配列になり、`axes[0]` のように1つずつ描きます（2行以上なら `axes[0, 1]`）。

## 日本語を表示する

そのままでは日本語が □ になります。Ubuntu なら日本語のフォントを入れて、指定します。

```bash
sudo apt install fonts-noto-cjk
```

```python
plt.rcParams["font.family"] = "Noto Sans CJK JP"
```

フォントを入れたあと、まだ □ のときは、`~/.cache/matplotlib` を消して読み直させます。軸の名前を英語にしておくのも手です。

## 画像に保存する

```python
fig.savefig("milk.png", dpi=150, bbox_inches="tight")   # 余白を切りつめて保存
```

- `plt.show()` の前に保存する（`show` で閉じたあとは空の図が保存されることがある）
- ssh でつないだラズパイや Jetson のように画面がないときは、`show` の代わりに保存して、VS Code で画像を開いて見る
- `.svg` や `.pdf` で保存すると、拡大してもぼやけない

## pandas から描く

pandas の表は、そのまま `plot` で描けます（中で matplotlib を使っています）。

```python
import pandas as pd

df = pd.DataFrame({"day": days, "milk": 30 + 3 * np.sin(days / 5)})
ax = df.plot(x="day", y="milk", figsize=(6, 3))
ax.set_ylabel("Milk (kg)")
df["milk"].plot.hist(bins=10)
```

## Jupyter と VS Code

- `.ipynb`（1章）では、グラフがセルのすぐ下に出る
- ふつうの `.py` では、`plt.show()` で別の窓が開く。閉じると続きが動く

## まとめ

- `fig, ax = plt.subplots()` で作り、`ax.plot`・`ax.scatter` などで描く
- 軸の名前・タイトル・凡例（`legend`）を付ける。`tight_layout` で整える
- 日本語は `fonts-noto-cjk` を入れて `font.family` を指定する
- `fig.savefig("名前.png", dpi=150, bbox_inches="tight")` で保存する
