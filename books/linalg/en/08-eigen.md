# 8. Eigenvalues and eigenvectors

## What you will learn in this chapter

- What eigenvalues and eigenvectors mean
- Finding eigenvalues with the characteristic equation, and then eigenvectors
- Diagonalization and when it is possible
- Finding $A^n$ by diagonalization

## Eigenvalues and eigenvectors

For a square matrix $A$, a number $\lambda$ such that

$$A\boldsymbol{x} = \lambda\boldsymbol{x} \qquad (\boldsymbol{x} \ne \boldsymbol{0})$$

is called an **eigenvalue** of $A$, and $\boldsymbol{x}$ is called an **eigenvector** for $\lambda$.

![Eigenvectors of A = (4 1; 2 3). (1, 1) becomes 5 times and (1, −2) 2 times longer, without changing direction](images/en/eigen.svg)

- An ordinary vector changes direction when multiplied by $A$. But **an eigenvector keeps its direction; only its length is multiplied by $\lambda$**
- Eigenvectors are like the "axes" of the linear transformation. In Example 7-4 of Chapter 7, $A$ looked like "5 times in the direction of $(1, 1)$, 2 times in the direction of $(1, -2)$" because these two are eigenvectors
- Any multiple of an eigenvector is again an eigenvector (only the direction matters)

## How to find eigenvalues

Rearranging $A\boldsymbol{x} = \lambda\boldsymbol{x}$ gives $(A - \lambda E)\boldsymbol{x} = \boldsymbol{0}$. The condition for this to have a solution $\boldsymbol{x} \ne \boldsymbol{0}$ is (Chapters 4 and 5)

$$\det(A - \lambda E) = 0$$

This is called the **characteristic equation**. For an $n \times n$ matrix, it is an equation of degree $n$ in $\lambda$.

> **Steps**: (1) Solve the characteristic equation $\det(A - \lambda E) = 0$ to get the eigenvalues $\lambda$. (2) For each $\lambda$, solve $(A - \lambda E)\boldsymbol{x} = \boldsymbol{0}$ to get the eigenvectors.

### Example 8-1

Find the eigenvalues and eigenvectors of $A = \begin{pmatrix} 4 & 1 \\ 2 & 3 \end{pmatrix}$.

**Solution** The characteristic equation is

$$\begin{vmatrix} 4 - \lambda & 1 \\ 2 & 3 - \lambda \end{vmatrix} = (4 - \lambda)(3 - \lambda) - 2 = \lambda^2 - 7\lambda + 10 = (\lambda - 2)(\lambda - 5) = 0$$

The eigenvalues are $\lambda = 5, 2$.

When $\lambda = 5$: from $(A - 5E)\boldsymbol{x} = \begin{pmatrix} -1 & 1 \\ 2 & -2 \end{pmatrix}\begin{pmatrix} x \\ y \end{pmatrix} = \boldsymbol{0}$, $-x + y = 0$. The eigenvectors are $t\begin{pmatrix} 1 \\ 1 \end{pmatrix}$ ($t \ne 0$).

When $\lambda = 2$: from $(A - 2E)\boldsymbol{x} = \begin{pmatrix} 2 & 1 \\ 2 & 1 \end{pmatrix}\begin{pmatrix} x \\ y \end{pmatrix} = \boldsymbol{0}$, $2x + y = 0$. The eigenvectors are $t\begin{pmatrix} 1 \\ -2 \end{pmatrix}$ ($t \ne 0$).

> **Key point**: The two rows of $(A - \lambda E)$ are always proportional (because the determinant is 0). If they are not proportional, your eigenvalue calculation is wrong. This makes a good check.

For a 2×2 matrix, the characteristic equation is $\lambda^2 - (\text{tr}\,A)\lambda + \det A = 0$. It is the same form as the Cayley–Hamilton formula in Chapter 3. Also, in general,

- The sum of the eigenvalues $= \text{tr}\,A$ (example: $5 + 2 = 7 = 4 + 3$)
- The product of the eigenvalues $= \det A$ (example: $5 \times 2 = 10 = 12 - 2$)

### Example 8-2

Find the eigenvalues and eigenvectors of $A = \begin{pmatrix} 1 & 2 & 0 \\ 0 & 3 & 0 \\ 2 & -4 & 2 \end{pmatrix}$.

**Solution** Expanding along column 3 (it has two 0s),

$$\det(A - \lambda E) = \begin{vmatrix} 1 - \lambda & 2 & 0 \\ 0 & 3 - \lambda & 0 \\ 2 & -4 & 2 - \lambda \end{vmatrix} = (2 - \lambda)\begin{vmatrix} 1 - \lambda & 2 \\ 0 & 3 - \lambda \end{vmatrix} = (1 - \lambda)(2 - \lambda)(3 - \lambda)$$

The eigenvalues are $\lambda = 1, 2, 3$.

- $\lambda = 1$: from $A - E = \begin{pmatrix} 0 & 2 & 0 \\ 0 & 2 & 0 \\ 2 & -4 & 1 \end{pmatrix}$, $y = 0$ and $2x + z = 0$. Eigenvectors $t(1, 0, -2)$
- $\lambda = 2$: from $A - 2E = \begin{pmatrix} -1 & 2 & 0 \\ 0 & 1 & 0 \\ 2 & -4 & 0 \end{pmatrix}$, $y = 0$ and $x = 0$. Eigenvectors $t(0, 0, 1)$
- $\lambda = 3$: from $A - 3E = \begin{pmatrix} -2 & 2 & 0 \\ 0 & 0 & 0 \\ 2 & -4 & -1 \end{pmatrix}$, $x = y$, and from $2x - 4y - z = 0$, $z = -2y$. Eigenvectors $t(1, 1, -2)$

Check: $A(1, 1, -2) = (1 + 2,\ 3,\ 2 - 4 - 4) = (3, 3, -6) = 3(1, 1, -2)$.

## Diagonalization

When an $n \times n$ square matrix $A$ has $n$ linearly independent eigenvectors $\boldsymbol{p}_1, \dots, \boldsymbol{p}_n$ (eigenvalues $\lambda_1, \dots, \lambda_n$), using $P = (\boldsymbol{p}_1\ \cdots\ \boldsymbol{p}_n)$ with them as columns, it can be made into a **diagonal matrix**:

$$P^{-1}AP = \begin{pmatrix} \lambda_1 & & \\ & \ddots & \\ & & \lambda_n \end{pmatrix}$$

This is called **diagonalization** (in terms of the change of basis in Chapter 7, it means choosing the eigenvectors as the basis).

- If the eigenvalues are **all different**, the eigenvectors are automatically linearly independent, so it can always be diagonalized
- When eigenvalues repeat (a repeated root), it can be diagonalized if you can take as many linearly independent eigenvectors for that eigenvalue as its multiplicity, and cannot otherwise

### An example that cannot be diagonalized

The characteristic equation of $A = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}$ is $(1 - \lambda)^2 = 0$, and the eigenvalue is $\lambda = 1$ (a repeated root). From $(A - E)\boldsymbol{x} = \begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}\boldsymbol{x} = \boldsymbol{0}$, $y = 0$, so the eigenvectors are only in the one direction $t(1, 0)$. You cannot take two linearly independent eigenvectors, so it **cannot be diagonalized**.

### Example 8-3

Diagonalize $A = \begin{pmatrix} 4 & 1 \\ 2 & 3 \end{pmatrix}$ and find $A^n$.

**Solution** From Example 8-1, setting $P = \begin{pmatrix} 1 & 1 \\ 1 & -2 \end{pmatrix}$,

$$P^{-1}AP = \begin{pmatrix} 5 & 0 \\ 0 & 2 \end{pmatrix} = D$$

(as calculated in Example 7-4 of Chapter 7). Since $A = PDP^{-1}$,

$$A^n = (PDP^{-1})(PDP^{-1})\cdots(PDP^{-1}) = PD^nP^{-1}$$

The key is that all the $P^{-1}P$ in the middle become $E$ and disappear. The $n$th power of a diagonal matrix just raises the diagonal entries to the $n$th power, so

$$A^n = \begin{pmatrix} 1 & 1 \\ 1 & -2 \end{pmatrix}\begin{pmatrix} 5^n & 0 \\ 0 & 2^n \end{pmatrix}\frac{1}{3}\begin{pmatrix} 2 & 1 \\ 1 & -1 \end{pmatrix} = \frac{1}{3}\begin{pmatrix} 2 \cdot 5^n + 2^n & 5^n - 2^n \\ 2 \cdot 5^n - 2^{n+1} & 5^n + 2^{n+1} \end{pmatrix}$$

Check: for $n = 1$, $\dfrac{1}{3}\begin{pmatrix} 12 & 3 \\ 6 & 9 \end{pmatrix} = \begin{pmatrix} 4 & 1 \\ 2 & 3 \end{pmatrix} = A$.

> **Key point**: Diagonalization says "seen in good coordinates, a matrix is just stretching and shrinking in each direction". It is a tool with a very wide range of uses: calculating $A^n$, recurrence relations (sequences), differential equations, Markov chains, principal component analysis in machine learning (Chapter 10) and more.

### Application: simultaneous recurrences

A system of recurrences like $a_{n+1} = 4a_n + b_n$, $b_{n+1} = 2a_n + 3b_n$, $a_1 = 1$, $b_1 = 0$ can be written

$$\begin{pmatrix} a_{n+1} \\ b_{n+1} \end{pmatrix} = A\begin{pmatrix} a_n \\ b_n \end{pmatrix} \quad\text{so}\quad \begin{pmatrix} a_n \\ b_n \end{pmatrix} = A^{n-1}\begin{pmatrix} 1 \\ 0 \end{pmatrix}$$

so from the first column of $A^{n-1}$ in Example 8-3 you get $a_n = \dfrac{2 \cdot 5^{n-1} + 2^{n-1}}{3}$ and $b_n = \dfrac{2 \cdot 5^{n-1} - 2^{n}}{3}$.

## Exercises

1. Find the eigenvalues and eigenvectors of $\begin{pmatrix} 1 & 2 \\ 2 & 1 \end{pmatrix}$.
2. Diagonalize $\begin{pmatrix} 2 & 1 \\ 0 & 3 \end{pmatrix}$ (give $P$ and $P^{-1}AP$).
3. When the eigenvalues of a 3×3 square matrix $A$ are $1, 2, 4$, find $\det A$ and $\text{tr}\,A$.

## Answers to the exercises

1. From $(1 - \lambda)^2 - 4 = 0$, $\lambda = 3, -1$. $\lambda = 3$: $t(1, 1)$; $\lambda = -1$: $t(1, -1)$
2. The eigenvalues are the diagonal entries $2, 3$ (a triangular matrix). $\lambda = 2$: from $(A - 2E) = \begin{pmatrix} 0 & 1 \\ 0 & 1 \end{pmatrix}$, $y = 0$, $t(1, 0)$. $\lambda = 3$: from $\begin{pmatrix} -1 & 1 \\ 0 & 0 \end{pmatrix}$, $x = y$, $t(1, 1)$. $P = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}$, $P^{-1}AP = \begin{pmatrix} 2 & 0 \\ 0 & 3 \end{pmatrix}$
3. $\det A = 1 \cdot 2 \cdot 4 = 8$, $\text{tr}\,A = 1 + 2 + 4 = 7$
