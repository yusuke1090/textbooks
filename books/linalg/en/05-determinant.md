# 5. Determinants

## What you will learn in this chapter

- Determinants of order 2 and 3 (the rule of Sarrus)
- Properties of determinants (how row operations change them)
- Cofactor expansion, and calculating determinants of order 4 and higher
- Finding the inverse with the adjugate matrix
- Cramer's rule

## Determinants of order 2 and 3

For a square matrix $A$ we define a single number $\det A$ (also written $\lvert A \rvert$). This is called the **determinant**.

$$\begin{vmatrix} a & b \\ c & d \end{vmatrix} = ad - bc$$

A determinant of order 3 can be calculated with the **rule of Sarrus**. Add the products along the three down-right diagonals and subtract the products along the three down-left diagonals.

$$\begin{vmatrix} a_{11} & a_{12} & a_{13} \\ a_{21} & a_{22} & a_{23} \\ a_{31} & a_{32} & a_{33} \end{vmatrix} = a_{11}a_{22}a_{33} + a_{12}a_{23}a_{31} + a_{13}a_{21}a_{32} - a_{13}a_{22}a_{31} - a_{12}a_{21}a_{33} - a_{11}a_{23}a_{32}$$

### Example 5-1

Find $\begin{vmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 10 \end{vmatrix}$.

**Solution**

$$1 \cdot 5 \cdot 10 + 2 \cdot 6 \cdot 7 + 3 \cdot 4 \cdot 8 - 3 \cdot 5 \cdot 7 - 2 \cdot 4 \cdot 10 - 1 \cdot 6 \cdot 8 = 50 + 84 + 96 - 105 - 80 - 48 = -3$$

> **Note**: The rule of Sarrus **only works up to order 3**. For order 4 and higher, use the properties below and cofactor expansion.

### What the determinant means

- Order 2: the (signed) **area of the parallelogram** made by the two column vectors. The "area scale factor" of Chapter 3
- Order 3: the (signed) **volume of the parallelepiped** made by the three column vectors
- $\det A = 0$ means the column vectors are "squashed" (they lie in a plane or on a line). That is why there is no inverse

## Properties of determinants

This is the most important part of calculating determinants.

| Operation | What happens to the determinant |
| --- | --- |
| Swap two rows | The sign changes ($\times(-1)$) |
| Multiply one row by $k$ | Multiplied by $k$ |
| Add a multiple of another row to a row | **Unchanged** |
| Transpose (${}^tA$) | Unchanged (so everything also holds with "row" read as "column") |
| Two rows are the same (or proportional) | 0 |
| A row is all 0 | 0 |
| Upper triangular matrix (all 0 below the diagonal) | The product of the diagonal entries |
| Product $AB$ | $\det(AB) = \det A \cdot \det B$ |

- The basic plan is to use "adding a multiple of another row to a row does not change it" to make more 0s, as in the elimination of Chapter 4, and then calculate
- The last property also gives $\det(A^{-1}) = \dfrac{1}{\det A}$

## Cofactor expansion

Let $D_{ij}$ be the determinant of order $(n - 1)$ obtained by removing row $i$ and column $j$ from an $n \times n$ matrix $A$. With a sign attached,

$$\tilde{a}_{ij} = (-1)^{i+j} D_{ij}$$

is called the **$(i, j)$ cofactor**. The sign $(-1)^{i+j}$ follows a checkerboard pattern with $+$ at the top left.

$$\begin{pmatrix} + & - & + & \cdots \\ - & + & - & \cdots \\ + & - & + & \cdots \\ \vdots & & & \ddots \end{pmatrix}$$

For any one row (or column), the following holds (**cofactor expansion**).

$$\det A = a_{i1}\tilde{a}_{i1} + a_{i2}\tilde{a}_{i2} + \cdots + a_{in}\tilde{a}_{in}$$

A determinant of order $n$ becomes a calculation of determinants of order $(n - 1)$. It is easiest to **expand along a row or column with many 0s**.

### Example 5-2

Find $\begin{vmatrix} 1 & 2 & 0 & 1 \\ 2 & 5 & 1 & 2 \\ 0 & 1 & 3 & 1 \\ 1 & 2 & 1 & 3 \end{vmatrix}$.

**Solution** First, use the 1 in column 1 to make the entries below it in column 1 equal to 0 (the determinant does not change).

$$\begin{vmatrix} 1 & 2 & 0 & 1 \\ 2 & 5 & 1 & 2 \\ 0 & 1 & 3 & 1 \\ 1 & 2 & 1 & 3 \end{vmatrix} \overset{\text{②} - 2\times\text{①},\ \text{④} - \text{①}}{=} \begin{vmatrix} 1 & 2 & 0 & 1 \\ 0 & 1 & 1 & 0 \\ 0 & 1 & 3 & 1 \\ 0 & 0 & 1 & 2 \end{vmatrix}$$

Expanding along column 1, only the $(1, 1)$ entry is nonzero, so

$$= 1 \cdot (-1)^{1+1}\begin{vmatrix} 1 & 1 & 0 \\ 1 & 3 & 1 \\ 0 & 1 & 2 \end{vmatrix} = 1 \cdot 3 \cdot 2 + 1 \cdot 1 \cdot 0 + 0 - 0 - 1 \cdot 1 \cdot 2 - 1 \cdot 1 \cdot 1 = 6 - 2 - 1 = 3$$

### Example 5-3 (the Vandermonde determinant)

Show that $\begin{vmatrix} 1 & 1 & 1 \\ a & b & c \\ a^2 & b^2 & c^2 \end{vmatrix} = (b - a)(c - a)(c - b)$.

**Solution** Subtract column 1 from columns 2 and 3 (column operations have the same properties).

$$\begin{vmatrix} 1 & 0 & 0 \\ a & b - a & c - a \\ a^2 & b^2 - a^2 & c^2 - a^2 \end{vmatrix} = \begin{vmatrix} b - a & c - a \\ (b-a)(b+a) & (c-a)(c+a) \end{vmatrix}$$

(expanding along row 1). Taking $(b - a)$ and $(c - a)$ out of the two columns,

$$= (b - a)(c - a)\begin{vmatrix} 1 & 1 \\ b + a & c + a \end{vmatrix} = (b - a)(c - a)(c - b)$$

This shows it is not 0 when $a, b, c$ are all different.

## The adjugate matrix and the inverse

The matrix made by arranging the cofactors $\tilde{a}_{ij}$ and **transposing** is called the **adjugate matrix** $\tilde{A}$ (its $(i, j)$ entry is $\tilde{a}_{ji}$).

$$A^{-1} = \frac{1}{\det A}\tilde{A}$$

The formula for the 2×2 inverse (Chapter 3) is the order-2 case of this formula.

### Example 5-4

Find the inverse of $A = \begin{pmatrix} 2 & 1 & 1 \\ 1 & 2 & 1 \\ 1 & 1 & 2 \end{pmatrix}$ using the adjugate matrix.

**Solution** By the rule of Sarrus, $\det A = 8 + 1 + 1 - 2 - 2 - 2 = 4$. Calculating the cofactors,

$$\tilde{a}_{11} = \begin{vmatrix} 2 & 1 \\ 1 & 2 \end{vmatrix} = 3, \quad \tilde{a}_{12} = -\begin{vmatrix} 1 & 1 \\ 1 & 2 \end{vmatrix} = -1, \quad \tilde{a}_{13} = \begin{vmatrix} 1 & 2 \\ 1 & 1 \end{vmatrix} = -1$$

$A$ is symmetric, so the rest are found in the same way:

$$A^{-1} = \frac{1}{4}\begin{pmatrix} 3 & -1 & -1 \\ -1 & 3 & -1 \\ -1 & -1 & 3 \end{pmatrix}$$

> **Key point**: For matrices larger than 3×3, the elimination of Chapter 4 takes less calculation than the adjugate matrix. The adjugate formula is important for showing that "an inverse exists only when $\det A \ne 0$".

## Cramer's rule

The solution of $A\boldsymbol{x} = \boldsymbol{b}$ ($\det A \ne 0$) is

$$x_j = \frac{\det A_j}{\det A}$$

where $A_j$ is $A$ with its column $j$ replaced by $\boldsymbol{b}$.

### Example 5-5

Solve with Cramer's rule: $\begin{cases} 2x + y = 5 \\ x + 3y = 10 \end{cases}$

**Solution** $\det A = 6 - 1 = 5$.

$$x = \frac{1}{5}\begin{vmatrix} 5 & 1 \\ 10 & 3 \end{vmatrix} = \frac{15 - 10}{5} = 1, \qquad y = \frac{1}{5}\begin{vmatrix} 2 & 5 \\ 1 & 10 \end{vmatrix} = \frac{20 - 5}{5} = 3$$

## Exercises

1. Find $\begin{vmatrix} 2 & 0 & 1 \\ 1 & 3 & 2 \\ 1 & 1 & 1 \end{vmatrix}$.
2. Find $\begin{vmatrix} 1 & 2 & 3 & 4 \\ 0 & 2 & 3 & 4 \\ 0 & 0 & 3 & 4 \\ 0 & 0 & 0 & 4 \end{vmatrix}$.
3. For a 3×3 square matrix $A$ with $\det A = 3$, find $\det(2A)$ and $\det(A^{-1})$.
4. Find $\lambda$ such that $\begin{vmatrix} 1 - \lambda & 2 \\ 3 & 2 - \lambda \end{vmatrix} = 0$.

## Answers to the exercises

1. $2 \cdot 3 \cdot 1 + 0 + 1 \cdot 1 \cdot 1 - 1 \cdot 3 \cdot 1 - 0 - 2 \cdot 2 \cdot 1 = 6 + 1 - 3 - 4 = 0$
2. It is upper triangular, so it is the product of the diagonal entries, $1 \cdot 2 \cdot 3 \cdot 4 = 24$
3. Each of the three rows is doubled, so $\det(2A) = 2^3 \cdot 3 = 24$. $\det(A^{-1}) = \dfrac{1}{3}$
4. $(1 - \lambda)(2 - \lambda) - 6 = \lambda^2 - 3\lambda - 4 = (\lambda - 4)(\lambda + 1) = 0$, so $\lambda = 4, -1$ (the same form as the eigenvalue calculation in Chapter 8)
