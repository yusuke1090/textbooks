# 2. Matrices and their operations

## What is a matrix?

Numbers arranged in a rectangle are called a **matrix**. A horizontal line of numbers is a **row**, and a vertical line is a **column**.

$$A = \begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{pmatrix}$$

- This $A$ has 2 rows and 3 columns, so it is a **$2 \times 3$ matrix**
- The number in row $i$, column $j$ is called the **$(i, j)$ entry** and is written $a_{ij}$. In the example above, $a_{12} = 2$ and $a_{23} = 6$
- A matrix with the same number of rows and columns is called a **square matrix** ($n \times n$ is a square matrix of order $n$)
- A column vector can be thought of as an $n \times 1$ matrix, and a row vector as a $1 \times n$ matrix

How to remember: "**rows run across, columns stand up**", like the rows of seats in a theater and the columns holding up a building.

## Sum and scalar multiple

Matrices of the same shape can be added entry by entry. A scalar multiple multiplies every entry by $k$.

### Example 2-1

When $A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$ and $B = \begin{pmatrix} 2 & 0 \\ 1 & 3 \end{pmatrix}$, find $A + B$ and $2A - B$.

**Solution**

$$A + B = \begin{pmatrix} 3 & 2 \\ 4 & 7 \end{pmatrix}, \qquad 2A - B = \begin{pmatrix} 2-2 & 4-0 \\ 6-1 & 8-3 \end{pmatrix} = \begin{pmatrix} 0 & 4 \\ 5 & 5 \end{pmatrix}$$

## Product

The $(i, j)$ entry of the matrix product $AB$ is the **dot product** of "row $i$ of $A$" and "column $j$ of $B$".

$$\begin{pmatrix} a & b \\ c & d \end{pmatrix}\begin{pmatrix} p & q \\ r & s \end{pmatrix} = \begin{pmatrix} ap + br & aq + bs \\ cp + dr & cq + ds \end{pmatrix}$$

- When $A$ is $l \times m$ and $B$ is $m \times n$, the product $AB$ is $l \times n$. The product is defined only when **the number of columns of $A$ equals the number of rows of $B$**
- How to remember the shape: $(l \times \underline{m})(\underline{m} \times n) = (l \times n)$. The inner $m$ disappears

### Example 2-2

For $A$ and $B$ in Example 2-1, find $AB$ and $BA$.

**Solution**

$$AB = \begin{pmatrix} 1 \cdot 2 + 2 \cdot 1 & 1 \cdot 0 + 2 \cdot 3 \\ 3 \cdot 2 + 4 \cdot 1 & 3 \cdot 0 + 4 \cdot 3 \end{pmatrix} = \begin{pmatrix} 4 & 6 \\ 10 & 12 \end{pmatrix}$$

$$BA = \begin{pmatrix} 2 \cdot 1 + 0 \cdot 3 & 2 \cdot 2 + 0 \cdot 4 \\ 1 \cdot 1 + 3 \cdot 3 & 1 \cdot 2 + 3 \cdot 4 \end{pmatrix} = \begin{pmatrix} 2 & 4 \\ 10 & 14 \end{pmatrix}$$

$AB \ne BA$.

> **Key point**: For matrix products, **swapping the order usually changes the answer** (the commutative law does not hold). This is the biggest difference from calculating with numbers. However, the associative law $(AB)C = A(BC)$ and the distributive law $A(B + C) = AB + AC$ do hold.

### Example 2-3

When $C = \begin{pmatrix} 1 & 0 & 2 \\ -1 & 3 & 1 \end{pmatrix}$ and $D = \begin{pmatrix} 3 & 1 \\ 2 & 1 \\ 1 & 0 \end{pmatrix}$, find $CD$ and $DC$.

**Solution** $C$ is $2 \times 3$ and $D$ is $3 \times 2$, so $CD$ is $2 \times 2$ and $DC$ is $3 \times 3$.

$$CD = \begin{pmatrix} 3 + 0 + 2 & 1 + 0 + 0 \\ -3 + 6 + 1 & -1 + 3 + 0 \end{pmatrix} = \begin{pmatrix} 5 & 1 \\ 4 & 2 \end{pmatrix}$$

$$DC = \begin{pmatrix} 3 - 1 & 0 + 3 & 6 + 1 \\ 2 - 1 & 0 + 3 & 4 + 1 \\ 1 + 0 & 0 + 0 & 2 + 0 \end{pmatrix} = \begin{pmatrix} 2 & 3 & 7 \\ 1 & 3 & 5 \\ 1 & 0 & 2 \end{pmatrix}$$

Even the shape has changed.

### The product of a matrix and a vector

Matrix × column vector is used to write a system of equations compactly.

$$\begin{cases} 2x + y = 5 \\ x + 3y = 10 \end{cases} \iff \begin{pmatrix} 2 & 1 \\ 1 & 3 \end{pmatrix}\begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} 5 \\ 10 \end{pmatrix} \iff A\boldsymbol{x} = \boldsymbol{b}$$

This form "$A\boldsymbol{x} = \boldsymbol{b}$" is the starting point of linear algebra (Chapter 4).

## Special matrices

| Name | Symbol | Contents |
| --- | --- | --- |
| **Identity matrix** | $E$ (also written $I$) | Diagonal entries (top left to bottom right) are 1, the rest 0. $AE = EA = A$. Plays the role of the number "1" |
| **Zero matrix** | $O$ | All 0. $A + O = A$, $AO = O$. Plays the role of the number "0" |
| **Diagonal matrix** | $\text{diag}(d_1, \dots, d_n)$ | Everything except the diagonal is 0. Products and powers are easy (Chapter 8) |
| **Transpose** | ${}^tA$ (also written $A^T$) | Rows and columns swapped. The $(i, j)$ entry is $a_{ji}$ |
| **Symmetric matrix** | ${}^tA = A$ | Symmetric about the diagonal. Plays a big part in Chapter 9 |

### Zero divisors

With numbers, "if $ab = 0$ then $a = 0$ or $b = 0$", but this is not always true for matrices.

$$\begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}\begin{pmatrix} 1 & -1 \\ -1 & 1 \end{pmatrix} = \begin{pmatrix} 0 & 0 \\ 0 & 0 \end{pmatrix}$$

Neither is $O$, yet the product is $O$. So you must not think "$AB = O$, so $A = O$ or $B = O$".

### Properties of the transpose

- ${}^t({}^tA) = A$
- ${}^t(A + B) = {}^tA + {}^tB$
- ${}^t(AB) = {}^tB\,{}^tA$ (**the order is reversed**)

The last property is also used for least squares (the form ${}^tX X$) in Chapter 10.

## Exercises

1. Calculate $\begin{pmatrix} 2 & 1 \\ 0 & 3 \end{pmatrix}\begin{pmatrix} 1 & -1 \\ 2 & 4 \end{pmatrix}$.
2. When $A = \begin{pmatrix} 1 & 2 \\ 0 & 1 \end{pmatrix}$, find $A^2$ and $A^3$, and guess $A^n$.
3. For $A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$, check that $A\,{}^tA$ is a symmetric matrix.

## Answers to the exercises

1. $\begin{pmatrix} 2 + 2 & -2 + 4 \\ 0 + 6 & 0 + 12 \end{pmatrix} = \begin{pmatrix} 4 & 2 \\ 6 & 12 \end{pmatrix}$
2. $A^2 = \begin{pmatrix} 1 & 4 \\ 0 & 1 \end{pmatrix}$, $A^3 = \begin{pmatrix} 1 & 6 \\ 0 & 1 \end{pmatrix}$. $A^n = \begin{pmatrix} 1 & 2n \\ 0 & 1 \end{pmatrix}$ (can be shown by mathematical induction)
3. ${}^tA = \begin{pmatrix} 1 & 3 \\ 2 & 4 \end{pmatrix}$, so $A\,{}^tA = \begin{pmatrix} 1 + 4 & 3 + 8 \\ 3 + 8 & 9 + 16 \end{pmatrix} = \begin{pmatrix} 5 & 11 \\ 11 & 25 \end{pmatrix}$. It is symmetric (in general ${}^t(A\,{}^tA) = A\,{}^tA$)
