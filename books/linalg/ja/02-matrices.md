# 2. 行列とその計算

## この章でわかること

- 行列の形（$m \times n$ 行列）と成分
- 和・実数倍・積
- 積は順番を変えると答えが変わる（$AB \ne BA$）
- 単位行列・零行列・転置行列・対称行列

## 行列とは

数を長方形に並べたものを**行列**といいます。横の並びを**行**、縦の並びを**列**と呼びます。

$$A = \begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{pmatrix}$$

- この $A$ は2行3列なので **$2 \times 3$ 行列**です
- $i$ 行 $j$ 列の数を **$(i, j)$ 成分**といい、$a_{ij}$ と書きます。上の例で $a_{12} = 2$、$a_{23} = 6$
- 行と列の数が同じ行列を**正方行列**といいます（$n \times n$ なら $n$ 次の正方行列）
- 列ベクトルは $n \times 1$ 行列、行ベクトルは $1 \times n$ 行列と考えられます

覚え方: 「**行は横、列は縦**」。「行」の字の右側の二本線は横、「列」の字の右側の「りっとう」は縦、と覚えるとよいでしょう。

## 和と実数倍

同じ形の行列どうしなら、成分ごとに足せます。実数倍は、すべての成分を $k$ 倍します。

### 例題 2-1

$A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$、$B = \begin{pmatrix} 2 & 0 \\ 1 & 3 \end{pmatrix}$ のとき、$A + B$ と $2A - B$ を求めよ。

**解答**

$$A + B = \begin{pmatrix} 3 & 2 \\ 4 & 7 \end{pmatrix}, \qquad 2A - B = \begin{pmatrix} 2-2 & 4-0 \\ 6-1 & 8-3 \end{pmatrix} = \begin{pmatrix} 0 & 4 \\ 5 & 5 \end{pmatrix}$$

## 積

行列の積 $AB$ の $(i, j)$ 成分は、「$A$ の $i$ 行」と「$B$ の $j$ 列」の**内積**です。

$$\begin{pmatrix} a & b \\ c & d \end{pmatrix}\begin{pmatrix} p & q \\ r & s \end{pmatrix} = \begin{pmatrix} ap + br & aq + bs \\ cp + dr & cq + ds \end{pmatrix}$$

- $A$ が $l \times m$、$B$ が $m \times n$ のとき、積 $AB$ は $l \times n$ になります。**$A$ の列の数と $B$ の行の数が同じ**ときだけ、積が定義されます
- 形の覚え方: $(l \times \underline{m})(\underline{m} \times n) = (l \times n)$。内側の $m$ が消える

### 例題 2-2

例題 2-1 の $A$、$B$ について、$AB$ と $BA$ を求めよ。

**解答**

$$AB = \begin{pmatrix} 1 \cdot 2 + 2 \cdot 1 & 1 \cdot 0 + 2 \cdot 3 \\ 3 \cdot 2 + 4 \cdot 1 & 3 \cdot 0 + 4 \cdot 3 \end{pmatrix} = \begin{pmatrix} 4 & 6 \\ 10 & 12 \end{pmatrix}$$

$$BA = \begin{pmatrix} 2 \cdot 1 + 0 \cdot 3 & 2 \cdot 2 + 0 \cdot 4 \\ 1 \cdot 1 + 3 \cdot 3 & 1 \cdot 2 + 3 \cdot 4 \end{pmatrix} = \begin{pmatrix} 2 & 4 \\ 10 & 14 \end{pmatrix}$$

$AB \ne BA$ です。

> **ポイント**: 行列の積は、ふつう**順番を入れかえると答えが変わる**（交換法則が成り立たない）。数の計算とのいちばん大きなちがいです。ただし、結合法則 $(AB)C = A(BC)$ と分配法則 $A(B + C) = AB + AC$ は成り立ちます。

### 例題 2-3

$C = \begin{pmatrix} 1 & 0 & 2 \\ -1 & 3 & 1 \end{pmatrix}$、$D = \begin{pmatrix} 3 & 1 \\ 2 & 1 \\ 1 & 0 \end{pmatrix}$ のとき、$CD$ と $DC$ を求めよ。

**解答** $C$ は $2 \times 3$、$D$ は $3 \times 2$ なので、$CD$ は $2 \times 2$、$DC$ は $3 \times 3$ です。

$$CD = \begin{pmatrix} 3 + 0 + 2 & 1 + 0 + 0 \\ -3 + 6 + 1 & -1 + 3 + 0 \end{pmatrix} = \begin{pmatrix} 5 & 1 \\ 4 & 2 \end{pmatrix}$$

$$DC = \begin{pmatrix} 3 - 1 & 0 + 3 & 6 + 1 \\ 2 - 1 & 0 + 3 & 4 + 1 \\ 1 + 0 & 0 + 0 & 2 + 0 \end{pmatrix} = \begin{pmatrix} 2 & 3 & 7 \\ 1 & 3 & 5 \\ 1 & 0 & 2 \end{pmatrix}$$

形まで変わってしまいました。

### 行列とベクトルの積

行列 × 列ベクトルは、連立方程式をまとめて書くのに使います。

$$\begin{cases} 2x + y = 5 \\ x + 3y = 10 \end{cases} \iff \begin{pmatrix} 2 & 1 \\ 1 & 3 \end{pmatrix}\begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} 5 \\ 10 \end{pmatrix} \iff A\boldsymbol{x} = \boldsymbol{b}$$

この「$A\boldsymbol{x} = \boldsymbol{b}$」の形が、線形代数の出発点です（4章）。

## 特別な行列

| 名前 | 記号 | 中身 |
| --- | --- | --- |
| **単位行列** | $E$（$I$ とも書く） | 対角成分（左上から右下）が1、ほかが0。$AE = EA = A$。数の「1」の役目 |
| **零行列** | $O$ | すべて0。$A + O = A$、$AO = O$。数の「0」の役目 |
| **対角行列** | $\text{diag}(d_1, \dots, d_n)$ | 対角成分以外が0。積と累乗の計算が楽（8章） |
| **転置行列** | ${}^tA$（$A^T$ とも書く） | 行と列を入れかえたもの。$(i, j)$ 成分が $a_{ji}$ |
| **対称行列** | ${}^tA = A$ | 対角線について対称。9章で大活躍する |

### 零因子

数では「$ab = 0$ なら $a = 0$ または $b = 0$」ですが、行列ではそうとは限りません。

$$\begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}\begin{pmatrix} 1 & -1 \\ -1 & 1 \end{pmatrix} = \begin{pmatrix} 0 & 0 \\ 0 & 0 \end{pmatrix}$$

どちらも $O$ ではないのに、積が $O$ になります。だから「$AB = O$ だから $A = O$ か $B = O$」と考えてはいけません。

### 転置の性質

- ${}^t({}^tA) = A$
- ${}^t(A + B) = {}^tA + {}^tB$
- ${}^t(AB) = {}^tB\,{}^tA$（**順番が逆になる**）

最後の性質は、10章の最小二乗法（${}^tX X$ の形）でも使います。

## 練習問題

1. $\begin{pmatrix} 2 & 1 \\ 0 & 3 \end{pmatrix}\begin{pmatrix} 1 & -1 \\ 2 & 4 \end{pmatrix}$ を計算せよ。
2. $A = \begin{pmatrix} 1 & 2 \\ 0 & 1 \end{pmatrix}$ のとき、$A^2$、$A^3$ を求め、$A^n$ を推測せよ。
3. $A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$ について、$A\,{}^tA$ が対称行列になることを確かめよ。

## 練習問題の答え

1. $\begin{pmatrix} 2 + 2 & -2 + 4 \\ 0 + 6 & 0 + 12 \end{pmatrix} = \begin{pmatrix} 4 & 2 \\ 6 & 12 \end{pmatrix}$
2. $A^2 = \begin{pmatrix} 1 & 4 \\ 0 & 1 \end{pmatrix}$、$A^3 = \begin{pmatrix} 1 & 6 \\ 0 & 1 \end{pmatrix}$。$A^n = \begin{pmatrix} 1 & 2n \\ 0 & 1 \end{pmatrix}$（数学的帰納法で示せる）
3. ${}^tA = \begin{pmatrix} 1 & 3 \\ 2 & 4 \end{pmatrix}$ なので $A\,{}^tA = \begin{pmatrix} 1 + 4 & 3 + 8 \\ 3 + 8 & 9 + 16 \end{pmatrix} = \begin{pmatrix} 5 & 11 \\ 11 & 25 \end{pmatrix}$。対称になっている（一般に ${}^t(A\,{}^tA) = A\,{}^tA$）
