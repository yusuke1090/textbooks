# 付録A. 公式のまとめ

## ベクトル（1章）

| 項目 | 式 |
| --- | --- |
| 大きさ | $\lvert\boldsymbol{a}\rvert = \sqrt{a_1^2 + a_2^2 + a_3^2}$ |
| 内積 | $\boldsymbol{a} \cdot \boldsymbol{b} = a_1b_1 + a_2b_2 + a_3b_3 = \lvert\boldsymbol{a}\rvert\lvert\boldsymbol{b}\rvert\cos\theta$ |
| 直交 | $\boldsymbol{a} \cdot \boldsymbol{b} = 0$ |
| 正射影 | $\dfrac{\boldsymbol{a} \cdot \boldsymbol{b}}{\lvert\boldsymbol{a}\rvert^2}\boldsymbol{a}$ |
| 外積 | $(a_2b_3 - a_3b_2,\ a_3b_1 - a_1b_3,\ a_1b_2 - a_2b_1)$。大きさは平行四辺形の面積 |

## 行列（2・3章）

| 項目 | 式 |
| --- | --- |
| 積の形 | $(l \times m)(m \times n) = (l \times n)$ |
| 交換法則 | 一般に $AB \ne BA$ |
| 転置 | ${}^t(AB) = {}^tB\,{}^tA$ |
| 2次の逆行列 | $\dfrac{1}{ad - bc}\begin{pmatrix} d & -b \\ -c & a \end{pmatrix}$（$ad - bc \ne 0$） |
| 積の逆行列 | $(AB)^{-1} = B^{-1}A^{-1}$ |
| ケーリー・ハミルトン | $A^2 - (a + d)A + (ad - bc)E = O$ |
| 回転 | $\begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$ |
| 合成変換 | あとからする変換の行列を**左**にかける |

## 連立方程式とランク（4章）

| 条件 | 解 |
| --- | --- |
| $\text{rank}\,A = \text{rank}(A \mid \boldsymbol{b}) = n$ | ただ1つ |
| $\text{rank}\,A = \text{rank}(A \mid \boldsymbol{b}) < n$ | 無数（自由な文字 $n - \text{rank}\,A$ 個） |
| $\text{rank}\,A < \text{rank}(A \mid \boldsymbol{b})$ | なし |

逆行列: $(A \mid E) \to (E \mid A^{-1})$

## 行列式（5章）

| 項目 | 式・性質 |
| --- | --- |
| 2次 | $ad - bc$ |
| 3次 | サラスの方法 |
| 行の入れかえ | 符号が変わる |
| 1行を $k$ 倍 | $k$ 倍 |
| 行に別の行の定数倍を足す | 変わらない |
| 転置 | 変わらない |
| 積 | $\det(AB) = \det A \det B$ |
| 余因子展開 | $\det A = \sum_j a_{ij}\tilde{a}_{ij}$、$\tilde{a}_{ij} = (-1)^{i+j}D_{ij}$ |
| 逆行列 | $A^{-1} = \dfrac{1}{\det A}\tilde{A}$ |
| クラメル | $x_j = \dfrac{\det A_j}{\det A}$ |

## ベクトル空間と線形写像（6・7章）

| 項目 | 式・性質 |
| --- | --- |
| 1次独立の判定 | 並べた行列のランク = ベクトルの数（正方なら $\det \ne 0$） |
| 次元 | 基底のベクトルの数 |
| 表現行列 | 基底の行き先を列に並べる |
| 次元定理 | $\dim \text{Ker}\,f + \dim \text{Im}\,f = \dim V$ |
| 基底の取りかえ | $B = P^{-1}AP$ |

## 固有値と対角化（8・9章）

| 項目 | 式・性質 |
| --- | --- |
| 固有方程式 | $\det(A - \lambda E) = 0$ |
| 固有値の和・積 | 和 $= \text{tr}\,A$、積 $= \det A$ |
| 対角化 | $P^{-1}AP = \text{diag}(\lambda_1, \dots, \lambda_n)$（$P$ は固有ベクトルを並べる） |
| $n$ 乗 | $A^n = PD^nP^{-1}$ |
| 直交行列 | ${}^tPP = E$、$P^{-1} = {}^tP$、$\det P = \pm1$ |
| 実対称行列 | 固有値は実数、固有ベクトルは直交、直交行列で必ず対角化できる |
| 2次形式 | ${}^t\boldsymbol{x}A\boldsymbol{x} \to \lambda_1X^2 + \lambda_2Y^2$ |
| 正規方程式 | ${}^tXX\boldsymbol{\beta} = {}^tX\boldsymbol{y}$ |

## 正方行列 $A$（$n$ 次）について、同じ意味の言いかえ

- $A$ は逆行列を持つ
- $\det A \ne 0$
- $\text{rank}\,A = n$
- $A$ の列（行）ベクトルは1次独立
- $A\boldsymbol{x} = \boldsymbol{0}$ の解は $\boldsymbol{0}$ だけ（$\text{Ker} = \{\boldsymbol{0}\}$）
- どんな $\boldsymbol{b}$ にも、$A\boldsymbol{x} = \boldsymbol{b}$ の解がただ1つある
- 0 は $A$ の固有値ではない
