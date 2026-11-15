# 6. ベクトル空間

## この章でわかること

- ベクトル空間（和と実数倍ができる集まり）
- 部分空間
- 1次結合・1次独立・1次従属と、その判定
- 基底と次元
- 基底についての座標

ここから少し抽象的になります。「矢印」を忘れて、「**足し算と実数倍ができて、ふつうの計算の規則が成り立つもの**」なら、何でもベクトルと考える、というのがこの章の考え方です。

## ベクトル空間

集合 $V$ の中で、和 $\boldsymbol{a} + \boldsymbol{b}$ と実数倍 $k\boldsymbol{a}$ ができて、その結果がまた $V$ に入り、次のような規則が成り立つとき、$V$ を**ベクトル空間**（線形空間）といいます。

- 和の交換法則・結合法則、零ベクトル $\boldsymbol{0}$ がある、$-\boldsymbol{a}$ がある
- $k(\boldsymbol{a} + \boldsymbol{b}) = k\boldsymbol{a} + k\boldsymbol{b}$、$(k + l)\boldsymbol{a} = k\boldsymbol{a} + l\boldsymbol{a}$、$(kl)\boldsymbol{a} = k(l\boldsymbol{a})$、$1\boldsymbol{a} = \boldsymbol{a}$

例:

| ベクトル空間 | 中身 |
| --- | --- |
| $\mathbb{R}^n$ | $n$ 個の実数の並び |
| $2 \times 2$ 行列の全体 | 行列の和と実数倍 |
| 2次以下の多項式の全体 $P_2$ | $a + bx + cx^2$。多項式の和と実数倍 |
| $A\boldsymbol{x} = \boldsymbol{0}$ の解の全体 | 解どうしを足しても、実数倍しても、また解 |

## 部分空間

ベクトル空間 $V$ の一部分 $W$ が、それだけで**和と実数倍について閉じている**（計算した結果がまた $W$ に入る）とき、$W$ を $V$ の**部分空間**といいます。

> **判定のしかた**: 次の3つを確かめる。(1) $\boldsymbol{0} \in W$、(2) $\boldsymbol{a}, \boldsymbol{b} \in W$ なら $\boldsymbol{a} + \boldsymbol{b} \in W$、(3) $\boldsymbol{a} \in W$ なら $k\boldsymbol{a} \in W$

### 例題 6-1

$\mathbb{R}^3$ の次の集合は、部分空間か。

(1) $W_1 = \{(x, y, z) \mid x + y + z = 0\}$　(2) $W_2 = \{(x, y, z) \mid x + y + z = 1\}$

**解答**

(1) $\boldsymbol{0} = (0, 0, 0)$ は $0 + 0 + 0 = 0$ で入る。$\boldsymbol{a}, \boldsymbol{b} \in W_1$ なら、成分の和はそれぞれ0なので、$\boldsymbol{a} + \boldsymbol{b}$ の成分の和も $0 + 0 = 0$、$k\boldsymbol{a}$ の成分の和も $k \cdot 0 = 0$。よって**部分空間**（原点を通る平面）。

(2) $(0, 0, 0)$ は $0 \ne 1$ で入らない。よって**部分空間ではない**（原点を通らない平面）。

> **ポイント**: 部分空間は、必ず**原点を通る**。$\mathbb{R}^3$ の部分空間は、$\{\boldsymbol{0}\}$・原点を通る直線・原点を通る平面・$\mathbb{R}^3$ 全体、の4種類だけです。

## 1次結合と1次独立

ベクトル $\boldsymbol{a}_1, \dots, \boldsymbol{a}_k$ の実数倍の和

$$c_1\boldsymbol{a}_1 + c_2\boldsymbol{a}_2 + \cdots + c_k\boldsymbol{a}_k$$

を**1次結合**といいます。

$$c_1\boldsymbol{a}_1 + c_2\boldsymbol{a}_2 + \cdots + c_k\boldsymbol{a}_k = \boldsymbol{0}$$

となるのが $c_1 = c_2 = \cdots = c_k = 0$ のときだけなら、$\boldsymbol{a}_1, \dots, \boldsymbol{a}_k$ は**1次独立**、そうでなければ**1次従属**といいます。

- 1次従属 = どれか1つが、残りの1次結合で書ける（「むだなベクトル」がある）
- 1次独立 = どれも、ほかのもので代わりができない

### 判定のしかた

ベクトルを**列に並べた行列** $A = (\boldsymbol{a}_1\ \boldsymbol{a}_2\ \cdots\ \boldsymbol{a}_k)$ を作ると、上の式は $A\boldsymbol{c} = \boldsymbol{0}$ という同次連立方程式です（4章）。

- $\text{rank}\,A = k$（ベクトルの数）なら 1次独立、それより小さければ 1次従属
- $n$ 個の $n$ 次元のベクトルなら、$\det A \ne 0 \iff$ 1次独立

### 例題 6-2

次のベクトルは1次独立か。

(1) $\boldsymbol{a}_1 = (1, 2, 1)$、$\boldsymbol{a}_2 = (2, 1, 0)$、$\boldsymbol{a}_3 = (1, -1, -1)$
(2) $\boldsymbol{b}_1 = (1, 1, 0)$、$\boldsymbol{b}_2 = (0, 1, 1)$、$\boldsymbol{b}_3 = (1, 0, 1)$

**解答**

(1) 列に並べた行列式は

$$\begin{vmatrix} 1 & 2 & 1 \\ 2 & 1 & -1 \\ 1 & 0 & -1 \end{vmatrix} = (-1) + (-2) + 0 - 1 - (-4) - 0 = 0$$

なので**1次従属**。実際、$\boldsymbol{a}_3 = \boldsymbol{a}_2 - \boldsymbol{a}_1$ になっています。

(2)

$$\begin{vmatrix} 1 & 0 & 1 \\ 1 & 1 & 0 \\ 0 & 1 & 1 \end{vmatrix} = 1 + 0 + 1 - 0 - 0 - 0 = 2 \ne 0$$

なので**1次独立**。

## 基底と次元

ベクトル空間 $V$ のベクトル $\boldsymbol{v}_1, \dots, \boldsymbol{v}_n$ が

1. 1次独立で、
2. $V$ のどのベクトルも、それらの1次結合で書ける（$V$ を**生成する**）

とき、$\{\boldsymbol{v}_1, \dots, \boldsymbol{v}_n\}$ を $V$ の**基底**といいます。基底の取り方はいろいろありますが、**ベクトルの個数 $n$ はいつも同じ**で、これを $V$ の**次元**（$\dim V$）といいます。

- $\mathbb{R}^3$ の基底の例: $\boldsymbol{e}_1 = (1, 0, 0)$、$\boldsymbol{e}_2 = (0, 1, 0)$、$\boldsymbol{e}_3 = (0, 0, 1)$（**標準基底**）。$\dim \mathbb{R}^3 = 3$
- 例題 6-2 (2) の $\boldsymbol{b}_1, \boldsymbol{b}_2, \boldsymbol{b}_3$ も $\mathbb{R}^3$ の基底
- $P_2$（2次以下の多項式）の基底の例: $1, x, x^2$。$\dim P_2 = 3$

### 例題 6-3

$W = \{(x, y, z) \mid x + y + z = 0\}$ の基底と次元を求めよ。

**解答** $x + y + z = 0$ を満たす点は、$y = s$、$z = t$ とおくと $x = -s - t$ なので、

$$\begin{pmatrix} x \\ y \\ z \end{pmatrix} = s\begin{pmatrix} -1 \\ 1 \\ 0 \end{pmatrix} + t\begin{pmatrix} -1 \\ 0 \\ 1 \end{pmatrix}$$

この2つのベクトルは $W$ を生成し、1次独立（片方がもう片方の実数倍ではない）。よって基底は $\{(-1, 1, 0),\ (-1, 0, 1)\}$、$\dim W = 2$（原点を通る平面）。

> **ポイント**: いくつかのベクトルで生成される部分空間の次元は、それらを並べた行列の**ランク**に等しい。

## 基底についての座標

基底 $\{\boldsymbol{v}_1, \dots, \boldsymbol{v}_n\}$ があると、どのベクトル $\boldsymbol{x}$ も、ただ1通りに $\boldsymbol{x} = c_1\boldsymbol{v}_1 + \cdots + c_n\boldsymbol{v}_n$ と書けます。$(c_1, \dots, c_n)$ を、その基底についての**座標**といいます。

### 例題 6-4

$\boldsymbol{x} = (3, 2, 1)$ を、基底 $\boldsymbol{b}_1 = (1, 1, 0)$、$\boldsymbol{b}_2 = (0, 1, 1)$、$\boldsymbol{b}_3 = (1, 0, 1)$ の1次結合で表せ。

**解答** $c_1\boldsymbol{b}_1 + c_2\boldsymbol{b}_2 + c_3\boldsymbol{b}_3 = \boldsymbol{x}$ を成分で書くと、

$$c_1 + c_3 = 3, \qquad c_1 + c_2 = 2, \qquad c_2 + c_3 = 1$$

3つを足すと $2(c_1 + c_2 + c_3) = 6$ なので $c_1 + c_2 + c_3 = 3$。それぞれの式を引いて、$c_2 = 0$、$c_3 = 1$、$c_1 = 2$。

$$\boldsymbol{x} = 2\boldsymbol{b}_1 + 0\boldsymbol{b}_2 + 1\boldsymbol{b}_3$$

同じベクトルでも、基底を変えると座標が変わります。「**どの基底で見るか**」を上手に選ぶことが、8章・9章の対角化の考え方です。

## 練習問題

1. $\mathbb{R}^2$ の集合 $W = \{(x, y) \mid y = x^2\}$ は部分空間か。
2. $(1, 2)$、$(3, k)$ が1次従属になる $k$ を求めよ。
3. $(1, 0, 1)$、$(2, 1, 0)$、$(0, 1, -2)$ で生成される部分空間の次元を求めよ。
4. $P_2$ のベクトル $1 + x$、$x + x^2$、$1 + x^2$ は1次独立か。

## 練習問題の答え

1. $(1, 1) \in W$ だが、2倍の $(2, 2)$ は $2 \ne 2^2$ で入らない。**部分空間ではない**
2. $\begin{vmatrix} 1 & 3 \\ 2 & k \end{vmatrix} = k - 6 = 0$ より $k = 6$
3. 列に並べた行列 $\begin{pmatrix} 1 & 2 & 0 \\ 0 & 1 & 1 \\ 1 & 0 & -2 \end{pmatrix}$ の行列式は $-2 + 2 + 0 - 0 - 0 - 0 = 0$。ランクは2（$(0, 1, -2) = (2, 1, 0) - 2(1, 0, 1)$）。次元は **2**
4. 係数を並べると $(1, 1, 0)$、$(0, 1, 1)$、$(1, 0, 1)$（定数・$x$・$x^2$ の係数）。例題 6-2 (2) と同じで行列式 $2 \ne 0$。**1次独立**
