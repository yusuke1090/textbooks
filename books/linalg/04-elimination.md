# 4. 連立1次方程式と掃き出し法

## この章でわかること

- 拡大係数行列と、行基本変形
- 掃き出し法（ガウスの消去法）で連立方程式を解く
- 階数（ランク）と、解の個数（1つ・無数・なし）
- 同次連立方程式
- 掃き出し法で逆行列を求める

## 行基本変形

連立方程式を解くときにしてよい操作は、次の3つです。

1. ある式を何倍かする（0倍はだめ）
2. ある式に、別の式の何倍かを足す
3. 2つの式を入れかえる

これを、係数と右辺だけを並べた**拡大係数行列** $(A \mid \boldsymbol{b})$ の**行**に対して行うのが**行基本変形**です。目標は、左下を全部0にした**階段行列**の形にすることです。

## 解がただ1つのとき

### 例題 4-1

次の連立方程式を、掃き出し法で解け。

$$\begin{cases} x + y + z = 6 \\ 2x + 3y + z = 11 \\ x - y + 2z = 5 \end{cases}$$

**解答** 拡大係数行列を作り、1列目の1（**ピボット**）を使って、その下を0にします。

$$\left(\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 2 & 3 & 1 & 11 \\ 1 & -1 & 2 & 5 \end{array}\right) \xrightarrow[\text{③} - \text{①}]{\text{②} - 2 \times \text{①}} \left(\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 0 & 1 & -1 & -1 \\ 0 & -2 & 1 & -1 \end{array}\right)$$

次に、2行目の1をピボットにして、その下を0にします。

$$\xrightarrow{\text{③} + 2 \times \text{②}} \left(\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 0 & 1 & -1 & -1 \\ 0 & 0 & -1 & -3 \end{array}\right)$$

これで階段行列になりました。下の行から順に解きます（後退代入）。

- 3行目: $-z = -3$ より $z = 3$
- 2行目: $y - z = -1$ より $y = 2$
- 1行目: $x + y + z = 6$ より $x = 1$

$(x, y, z) = (1, 2, 3)$。

> **ポイント**: さらに上の行も0になるまで掃き出すと、左側が単位行列 $E$ になり、右の列にそのまま答えが並びます（**行簡約形**）。手で解くときは、どちらでもかまいません。

$$\left(\begin{array}{ccc|c} 1 & 0 & 0 & 1 \\ 0 & 1 & 0 & 2 \\ 0 & 0 & 1 & 3 \end{array}\right)$$

## 階数（ランク）

行基本変形で階段行列にしたとき、**0でない行の数**を、その行列の**階数**（ランク）といい、$\text{rank}\,A$ と書きます。行基本変形のやり方によらず、ランクは同じ値になります。

ランクを使うと、連立方程式 $A\boldsymbol{x} = \boldsymbol{b}$（未知数が $n$ 個）の解の様子が、次のようにわかります。

| 条件 | 解 |
| --- | --- |
| $\text{rank}\,A = \text{rank}(A \mid \boldsymbol{b}) = n$ | ただ1つ |
| $\text{rank}\,A = \text{rank}(A \mid \boldsymbol{b}) < n$ | 無数（$n - \text{rank}\,A$ 個の自由な文字を使って表す） |
| $\text{rank}\,A < \text{rank}(A \mid \boldsymbol{b})$ | なし（「$0 = 1$」のような矛盾が出る） |

## 解が無数にあるとき

### 例題 4-2

$$\begin{cases} x + 2y - z = 3 \\ 2x + 4y + z = 9 \\ x + 2y + 2z = 6 \end{cases}$$

**解答**

$$\left(\begin{array}{ccc|c} 1 & 2 & -1 & 3 \\ 2 & 4 & 1 & 9 \\ 1 & 2 & 2 & 6 \end{array}\right) \xrightarrow[\text{③} - \text{①}]{\text{②} - 2 \times \text{①}} \left(\begin{array}{ccc|c} 1 & 2 & -1 & 3 \\ 0 & 0 & 3 & 3 \\ 0 & 0 & 3 & 3 \end{array}\right) \xrightarrow{\text{③} - \text{②}} \left(\begin{array}{ccc|c} 1 & 2 & -1 & 3 \\ 0 & 0 & 3 & 3 \\ 0 & 0 & 0 & 0 \end{array}\right)$$

$\text{rank}\,A = \text{rank}(A \mid \boldsymbol{b}) = 2 < 3$ なので、解は無数にあり、自由な文字は $3 - 2 = 1$ 個です。

- 2行目: $3z = 3$ より $z = 1$
- 1行目: $x + 2y - z = 3$ より $x = 4 - 2y$

$y = t$（$t$ は任意の実数）とおくと、

$$\begin{pmatrix} x \\ y \\ z \end{pmatrix} = \begin{pmatrix} 4 - 2t \\ t \\ 1 \end{pmatrix} = \begin{pmatrix} 4 \\ 0 \\ 1 \end{pmatrix} + t\begin{pmatrix} -2 \\ 1 \\ 0 \end{pmatrix}$$

解は、空間の中の**直線**になります。

## 解がないとき

### 例題 4-3

例題 4-2 の3つめの式の右辺を 7 に変えると、どうなるか。

**解答** 同じ変形で、最後が

$$\left(\begin{array}{ccc|c} 1 & 2 & -1 & 3 \\ 0 & 0 & 3 & 3 \\ 0 & 0 & 0 & 1 \end{array}\right)$$

となります。3行目は「$0x + 0y + 0z = 1$」で、成り立つ $x, y, z$ はありません。$\text{rank}\,A = 2 < \text{rank}(A \mid \boldsymbol{b}) = 3$ なので、**解なし**。

## 同次連立方程式

右辺が全部0の方程式 $A\boldsymbol{x} = \boldsymbol{0}$ を**同次連立方程式**といいます。

- $\boldsymbol{x} = \boldsymbol{0}$ は、いつでも解です（**自明な解**）
- $\boldsymbol{0}$ 以外の解（**非自明な解**）があるのは、$\text{rank}\,A < n$ のときだけです
- 正方行列なら、「非自明な解がある $\iff$ $\det A = 0$」（5章）。この事実が、8章の**固有値**を求める式のもとになります

## 掃き出し法で逆行列を求める

$n$ 次の正方行列 $A$ の右に単位行列 $E$ を並べ、左側が $E$ になるまで行基本変形をすると、右側が $A^{-1}$ になります。

$$(A \mid E) \longrightarrow (E \mid A^{-1})$$

途中で左側に0だけの行ができたら、$A$ は逆行列を持ちません（$\text{rank}\,A < n$）。

### 例題 4-4

$A = \begin{pmatrix} 1 & 2 & 1 \\ 2 & 5 & 2 \\ 1 & 2 & 2 \end{pmatrix}$ の逆行列を求めよ。

**解答**

$$\left(\begin{array}{ccc|ccc} 1 & 2 & 1 & 1 & 0 & 0 \\ 2 & 5 & 2 & 0 & 1 & 0 \\ 1 & 2 & 2 & 0 & 0 & 1 \end{array}\right) \xrightarrow[\text{③} - \text{①}]{\text{②} - 2 \times \text{①}} \left(\begin{array}{ccc|ccc} 1 & 2 & 1 & 1 & 0 & 0 \\ 0 & 1 & 0 & -2 & 1 & 0 \\ 0 & 0 & 1 & -1 & 0 & 1 \end{array}\right)$$

左下が0になりました。次は右上を0にします。

$$\xrightarrow{\text{①} - 2 \times \text{②} - \text{③}} \left(\begin{array}{ccc|ccc} 1 & 0 & 0 & 6 & -2 & -1 \\ 0 & 1 & 0 & -2 & 1 & 0 \\ 0 & 0 & 1 & -1 & 0 & 1 \end{array}\right)$$

$$A^{-1} = \begin{pmatrix} 6 & -2 & -1 \\ -2 & 1 & 0 \\ -1 & 0 & 1 \end{pmatrix}$$

確かめ: $A$ の1行目と $A^{-1}$ の1列目の内積は $6 - 4 - 1 = 1$、2列目とは $-2 + 2 + 0 = 0$…と、$AA^{-1} = E$ になります。

## まとめ: 正方行列 $A$ について同じ意味の言いかえ

$n$ 次の正方行列 $A$ について、次はすべて同じことを言っています（5章・6章で、さらに言いかえが増えます）。

- $A$ は逆行列を持つ
- $\text{rank}\,A = n$
- $A\boldsymbol{x} = \boldsymbol{b}$ は、どんな $\boldsymbol{b}$ に対しても、ただ1つの解を持つ
- $A\boldsymbol{x} = \boldsymbol{0}$ の解は $\boldsymbol{x} = \boldsymbol{0}$ だけ
- $\det A \ne 0$（5章）

## 練習問題

1. 掃き出し法で解け: $\begin{cases} x + 2y = 5 \\ 3x - y = 1 \end{cases}$
2. 次の行列のランクを求めよ: $\begin{pmatrix} 1 & 2 & 3 \\ 2 & 4 & 6 \\ 1 & 1 & 1 \end{pmatrix}$
3. 次の連立方程式が解を持つような $a$ を求め、そのときの解を求めよ: $\begin{cases} x + y = 1 \\ 2x + 2y = a \end{cases}$

## 練習問題の答え

1. $\left(\begin{array}{cc|c} 1 & 2 & 5 \\ 3 & -1 & 1 \end{array}\right) \to \left(\begin{array}{cc|c} 1 & 2 & 5 \\ 0 & -7 & -14 \end{array}\right)$ より $y = 2$、$x = 1$
2. 2行目 − 2×1行目 は全部0、3行目 − 1行目 は $(0, -1, -2)$。0でない行は2つなので、ランクは **2**
3. 2行目 − 2×1行目 で $(0, 0 \mid a - 2)$。解を持つのは $a = 2$ のとき。そのとき $x = 1 - t$、$y = t$（$t$ は任意）
