# 7. 線形写像

## この章でわかること

- 線形写像と、その表現行列
- 核（Ker）と像（Im）
- 次元定理
- 基底を取りかえると、表現行列はどう変わるか（$P^{-1}AP$）

## 線形写像

ベクトル空間 $V$ から $W$ への写像 $f$ が、

$$f(\boldsymbol{a} + \boldsymbol{b}) = f(\boldsymbol{a}) + f(\boldsymbol{b}), \qquad f(k\boldsymbol{a}) = kf(\boldsymbol{a})$$

を満たすとき、$f$ を**線形写像**といいます（$V = W$ のときは**線形変換**。3章の1次変換）。「足してから写しても、写してから足しても同じ」という性質です。

- 行列 $A$ をかける写像 $f(\boldsymbol{x}) = A\boldsymbol{x}$ は、線形写像です
- 逆に、$\mathbb{R}^n$ から $\mathbb{R}^m$ への線形写像は、**必ずある $m \times n$ 行列をかける形で書けます**。この行列を**表現行列**といいます

### 表現行列の作り方

標準基底 $\boldsymbol{e}_1, \dots, \boldsymbol{e}_n$ の行き先 $f(\boldsymbol{e}_1), \dots, f(\boldsymbol{e}_n)$ を、**列に並べる**だけです（3章の1次変換と同じ考え方）。

$$A = \big(f(\boldsymbol{e}_1)\ \ f(\boldsymbol{e}_2)\ \cdots\ f(\boldsymbol{e}_n)\big)$$

### 例題 7-1

$f(x, y, z) = (x + 2y,\ y - z)$ で決まる $\mathbb{R}^3$ から $\mathbb{R}^2$ への線形写像の表現行列を求めよ。

**解答** $f(\boldsymbol{e}_1) = (1, 0)$、$f(\boldsymbol{e}_2) = (2, 1)$、$f(\boldsymbol{e}_3) = (0, -1)$ なので、

$$A = \begin{pmatrix} 1 & 2 & 0 \\ 0 & 1 & -1 \end{pmatrix}$$

（確かめ: $A\begin{pmatrix} x \\ y \\ z \end{pmatrix} = \begin{pmatrix} x + 2y \\ y - z \end{pmatrix}$）

### 例題 7-2

$P_2$（2次以下の多項式）で、微分 $D(p) = p'$ は線形写像である。基底 $1, x, x^2$ についての表現行列を求めよ。

**解答** $D(1) = 0$、$D(x) = 1$、$D(x^2) = 2x$。これを基底 $1, x, x^2$ の座標で書くと、$(0, 0, 0)$、$(1, 0, 0)$、$(0, 2, 0)$。列に並べて、

$$\begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 2 \\ 0 & 0 & 0 \end{pmatrix}$$

例えば $3 + 4x + 5x^2$（座標 $(3, 4, 5)$）にかけると $(4, 10, 0)$、つまり $4 + 10x$。微分の答えと一致します。**微分も行列の計算になる**、というのが線形代数の見方です。

## 核と像

線形写像 $f: V \to W$ について、

- **核**: $\text{Ker}\,f = \{\boldsymbol{x} \in V \mid f(\boldsymbol{x}) = \boldsymbol{0}\}$（$\boldsymbol{0}$ に写されるものの全体）
- **像**: $\text{Im}\,f = \{f(\boldsymbol{x}) \mid \boldsymbol{x} \in V\}$（写った先の全体）

どちらも部分空間になります。行列 $A$ で書くと、

- $\text{Ker}\,f$ は、同次連立方程式 $A\boldsymbol{x} = \boldsymbol{0}$ の解の全体
- $\text{Im}\,f$ は、$A$ の**列ベクトルで生成される**部分空間。その次元は $\text{rank}\,A$

## 次元定理

$f: V \to W$ が線形写像のとき、

$$\dim(\text{Ker}\,f) + \dim(\text{Im}\,f) = \dim V$$

「つぶれた分（核）と、残った分（像）を合わせると、もとの次元になる」という意味です。行列で書くと、$n$ 列の行列 $A$ について、

$$(A\boldsymbol{x} = \boldsymbol{0} \text{ の解の自由な文字の数}) + \text{rank}\,A = n$$

4章の「自由な文字は $n - \text{rank}\,A$ 個」と同じことです。

### 例題 7-3

$A = \begin{pmatrix} 1 & 2 & 3 \\ 2 & 4 & 6 \\ 1 & 1 & 1 \end{pmatrix}$ で決まる線形変換について、$\text{Ker}$ と $\text{Im}$ の基底と次元を求めよ。

**解答** 行基本変形をすると、

$$\begin{pmatrix} 1 & 2 & 3 \\ 2 & 4 & 6 \\ 1 & 1 & 1 \end{pmatrix} \to \begin{pmatrix} 1 & 2 & 3 \\ 0 & 0 & 0 \\ 0 & -1 & -2 \end{pmatrix} \to \begin{pmatrix} 1 & 2 & 3 \\ 0 & 1 & 2 \\ 0 & 0 & 0 \end{pmatrix}$$

$\text{rank}\,A = 2$。

- **Ker**: $y + 2z = 0$、$x + 2y + 3z = 0$。$z = t$ とおくと $y = -2t$、$x = -2y - 3z = t$。$\text{Ker} = \{t(1, -2, 1)\}$、基底 $(1, -2, 1)$、次元 **1**
- **Im**: 階段行列で、ピボットがあったのは1列目と2列目。もとの $A$ の1列目と2列目 $(1, 2, 1)$、$(2, 4, 1)$ が基底で、次元 **2**

$1 + 2 = 3$ で、次元定理が成り立っています。$\mathbb{R}^3$ が、この変換で**平面につぶされ**、直線 $t(1, -2, 1)$ の上の点は全部 $\boldsymbol{0}$ に行く、ということです。

> **ポイント**: 線形変換 $f: \mathbb{R}^n \to \mathbb{R}^n$ で、$\text{Ker}\,f = \{\boldsymbol{0}\}$ $\iff$ $\text{Im}\,f = \mathbb{R}^n$ $\iff$ $\det A \ne 0$ $\iff$ 逆変換がある。4章の「言いかえ」の一覧が、さらに増えました。

## 基底の取りかえと表現行列

同じ線形変換でも、**どの基底で見るか**で、表現行列は変わります。

$\mathbb{R}^n$ の新しい基底 $\boldsymbol{p}_1, \dots, \boldsymbol{p}_n$ を列に並べた行列を $P$（**基底の変換行列**）とすると、標準基底での表現行列が $A$ の線形変換は、新しい基底では

$$B = P^{-1}AP$$

という表現行列になります。

- 理由: 新しい基底での座標 $\boldsymbol{c}$ は、もとの座標で $P\boldsymbol{c}$。それに $A$ をかけて、また新しい座標に戻す（$P^{-1}$ をかける）
- $A$ と $P^{-1}AP$ のように、基底の取りかえで移りあう行列どうしを**相似**といいます。相似な行列は、行列式・トレース・ランク・固有値（8章）が同じです

### 例題 7-4

$A = \begin{pmatrix} 4 & 1 \\ 2 & 3 \end{pmatrix}$、新しい基底 $\boldsymbol{p}_1 = (1, 1)$、$\boldsymbol{p}_2 = (1, -2)$ のとき、$P^{-1}AP$ を求めよ。

**解答** $P = \begin{pmatrix} 1 & 1 \\ 1 & -2 \end{pmatrix}$、$\det P = -3$、$P^{-1} = \dfrac{1}{3}\begin{pmatrix} 2 & 1 \\ 1 & -1 \end{pmatrix}$。

$$AP = \begin{pmatrix} 5 & 2 \\ 5 & -4 \end{pmatrix}, \qquad P^{-1}AP = \frac{1}{3}\begin{pmatrix} 10 + 5 & 4 - 4 \\ 5 - 5 & 2 + 4 \end{pmatrix} = \begin{pmatrix} 5 & 0 \\ 0 & 2 \end{pmatrix}$$

**対角行列**になりました。$A$ は、この基底で見ると「$\boldsymbol{p}_1$ の方向に5倍、$\boldsymbol{p}_2$ の方向に2倍」という、とても単純な変換だったのです。この「うまい基底」の見つけ方が、次の8章の固有値と固有ベクトルです。

## 練習問題

1. $\mathbb{R}^2$ の写像 $f(x, y) = (x + 1, y)$ は線形写像か。
2. $f(x, y) = (x + y,\ 2x + 2y)$ の Ker と Im を求めよ。
3. $5 \times 7$ 行列 $A$ のランクが4のとき、$A\boldsymbol{x} = \boldsymbol{0}$ の解の空間の次元はいくつか。

## 練習問題の答え

1. $f(0, 0) = (1, 0) \ne (0, 0)$。線形写像は必ず $\boldsymbol{0}$ を $\boldsymbol{0}$ に写すので、**線形写像ではない**
2. 表現行列 $\begin{pmatrix} 1 & 1 \\ 2 & 2 \end{pmatrix}$、ランク1。Ker は $x + y = 0$ の直線 $\{t(1, -1)\}$（次元1）。Im は $(1, 2)$ の方向の直線 $\{s(1, 2)\}$（次元1）
3. 次元定理より $7 - 4 = 3$
