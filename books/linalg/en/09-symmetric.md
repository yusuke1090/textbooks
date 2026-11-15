# 9. Inner product spaces and diagonalizing symmetric matrices

## Orthonormal bases

The dot product of Chapter 1 is defined in the same way in $\mathbb{R}^n$, by $\boldsymbol{a} \cdot \boldsymbol{b} = a_1b_1 + \cdots + a_nb_n$ (also written $(\boldsymbol{a}, \boldsymbol{b})$). A vector space with an inner product is called an **inner product space**.

A basis in which every pair is orthogonal and every vector has length 1 is called an **orthonormal basis**.

$$\boldsymbol{u}_i \cdot \boldsymbol{u}_j = \begin{cases} 1 & (i = j) \\ 0 & (i \ne j) \end{cases}$$

- The standard basis $\boldsymbol{e}_1, \dots, \boldsymbol{e}_n$ is an orthonormal basis
- Coordinates in an orthonormal basis are found **just by taking dot products**: $\boldsymbol{x} = (\boldsymbol{x} \cdot \boldsymbol{u}_1)\boldsymbol{u}_1 + \cdots + (\boldsymbol{x} \cdot \boldsymbol{u}_n)\boldsymbol{u}_n$. You do not have to solve a system of equations as in Example 6-4 of Chapter 6, which is very convenient

## The Gram–Schmidt process

This is a way to make an orthonormal basis from linearly independent vectors $\boldsymbol{a}_1, \boldsymbol{a}_2, \dots$. You keep subtracting the **projections** of Chapter 1.

1. $\boldsymbol{u}_1 = \dfrac{\boldsymbol{a}_1}{|\boldsymbol{a}_1|}$
2. $\boldsymbol{a}_2' = \boldsymbol{a}_2 - (\boldsymbol{a}_2 \cdot \boldsymbol{u}_1)\boldsymbol{u}_1$ (remove the component in the direction of $\boldsymbol{u}_1$), $\boldsymbol{u}_2 = \dfrac{\boldsymbol{a}_2'}{|\boldsymbol{a}_2'|}$
3. $\boldsymbol{a}_3' = \boldsymbol{a}_3 - (\boldsymbol{a}_3 \cdot \boldsymbol{u}_1)\boldsymbol{u}_1 - (\boldsymbol{a}_3 \cdot \boldsymbol{u}_2)\boldsymbol{u}_2$, $\boldsymbol{u}_3 = \dfrac{\boldsymbol{a}_3'}{|\boldsymbol{a}_3'|}$
4. And so on

### Example 9-1

Make an orthonormal basis from $\boldsymbol{a}_1 = (1, 1, 0)$, $\boldsymbol{a}_2 = (1, 0, 1)$ and $\boldsymbol{a}_3 = (0, 1, 1)$.

**Solution**

(1) From $|\boldsymbol{a}_1| = \sqrt{2}$, $\boldsymbol{u}_1 = \dfrac{1}{\sqrt{2}}(1, 1, 0)$.

(2) Since $\boldsymbol{a}_2 \cdot \boldsymbol{u}_1 = \dfrac{1}{\sqrt{2}}$,

$$\boldsymbol{a}_2' = (1, 0, 1) - \frac{1}{\sqrt{2}} \cdot \frac{1}{\sqrt{2}}(1, 1, 0) = \left(\frac{1}{2}, -\frac{1}{2}, 1\right) = \frac{1}{2}(1, -1, 2)$$

Making its length 1, $\boldsymbol{u}_2 = \dfrac{1}{\sqrt{6}}(1, -1, 2)$ (only the direction matters, so you can ignore the $\frac{1}{2}$).

(3) Since $\boldsymbol{a}_3 \cdot \boldsymbol{u}_1 = \dfrac{1}{\sqrt{2}}$ and $\boldsymbol{a}_3 \cdot \boldsymbol{u}_2 = \dfrac{-1 + 2}{\sqrt{6}} = \dfrac{1}{\sqrt{6}}$,

$$\boldsymbol{a}_3' = (0, 1, 1) - \frac{1}{2}(1, 1, 0) - \frac{1}{6}(1, -1, 2) = \left(-\frac{2}{3}, \frac{2}{3}, \frac{2}{3}\right)$$

$\boldsymbol{u}_3 = \dfrac{1}{\sqrt{3}}(-1, 1, 1)$.

Check: $\boldsymbol{u}_1 \cdot \boldsymbol{u}_3 \propto -1 + 1 + 0 = 0$, $\boldsymbol{u}_2 \cdot \boldsymbol{u}_3 \propto -1 - 1 + 2 = 0$.

> **Key point**: In the middle of the calculation, do not worry about fractions: **if the direction is the same, you may multiply by anything**. Just divide by the length at the end.

## Orthogonal matrices

A matrix $P$ with an orthonormal basis as its columns is called an **orthogonal matrix**. It has these properties.

- ${}^tP\,P = E$, that is, **$P^{-1} = {}^tP$** (the inverse is found just by transposing)
- It keeps dot products: $(P\boldsymbol{a}) \cdot (P\boldsymbol{b}) = \boldsymbol{a} \cdot \boldsymbol{b}$. So **it keeps both lengths and angles**
- $\det P = \pm 1$. $+1$ is a rotation; $-1$ is a rotation combined with a mirror

The rotation matrix of Chapter 3, $\begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$, is a typical orthogonal matrix.

## Diagonalizing real symmetric matrices

A symmetric matrix with real entries (${}^tA = A$) has these wonderful properties.

1. Its eigenvalues are **all real**
2. Eigenvectors for different eigenvalues are **orthogonal**
3. It can always be diagonalized by an **orthogonal matrix** $P$: ${}^tP\,A\,P = P^{-1}AP = $ a diagonal matrix

In Chapter 8 there were matrices that could not be diagonalized. With a symmetric matrix there is no such worry. What's more, you do not need to calculate $P^{-1}$ (${}^tP$ will do).

> **Steps**: (1) Find the eigenvalues. (2) Find the eigenvectors. (3) Within the same eigenvalue, make the eigenvectors orthogonal with Gram–Schmidt (eigenvectors for different eigenvalues are orthogonal already). (4) Make all of them length 1 and arrange them as columns.

### Example 9-2

Diagonalize $A = \begin{pmatrix} 2 & 1 & 1 \\ 1 & 2 & 1 \\ 1 & 1 & 2 \end{pmatrix}$ with an orthogonal matrix.

**Solution** The characteristic equation is (it is easiest to add rows 2 and 3 to row 1 and take out $(4 - \lambda)$)

$$\det(A - \lambda E) = -(\lambda - 4)(\lambda - 1)^2 = 0$$

The eigenvalues are $\lambda = 4$ and $1$ (a repeated root).

- $\lambda = 4$: eliminating $A - 4E = \begin{pmatrix} -2 & 1 & 1 \\ 1 & -2 & 1 \\ 1 & 1 & -2 \end{pmatrix}$ gives $x = y = z$. Eigenvector $(1, 1, 1)$
- $\lambda = 1$: from $A - E = \begin{pmatrix} 1 & 1 & 1 \\ 1 & 1 & 1 \\ 1 & 1 & 1 \end{pmatrix}$, $x + y + z = 0$. The space of eigenvectors is a plane (2-dimensional). Choose **two orthogonal ones** from it: $(1, -1, 0)$, and $(1, 1, -2)$, which is orthogonal to it and satisfies $x + y + z = 0$

Check: the three vectors $(1, 1, 1)$, $(1, -1, 0)$ and $(1, 1, -2)$ are mutually orthogonal (eigenvectors for $\lambda = 4$ and $\lambda = 1$ are orthogonal automatically). Dividing by their lengths and arranging them,

$$P = \begin{pmatrix} \frac{1}{\sqrt{3}} & \frac{1}{\sqrt{2}} & \frac{1}{\sqrt{6}} \\ \frac{1}{\sqrt{3}} & -\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{6}} \\ \frac{1}{\sqrt{3}} & 0 & -\frac{2}{\sqrt{6}} \end{pmatrix}, \qquad {}^tP\,A\,P = \begin{pmatrix} 4 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix}$$

## Quadratic forms

A second-degree expression like $ax^2 + 2bxy + cy^2$ (a **quadratic form**) can be written with a symmetric matrix.

$$ax^2 + 2bxy + cy^2 = \begin{pmatrix} x & y \end{pmatrix}\begin{pmatrix} a & b \\ b & c \end{pmatrix}\begin{pmatrix} x \\ y \end{pmatrix} = {}^t\boldsymbol{x}A\boldsymbol{x}$$

If you diagonalize $A$ with an orthogonal matrix $P$ and set $\boldsymbol{x} = P\boldsymbol{X}$ (rotating the coordinates),

$${}^t\boldsymbol{x}A\boldsymbol{x} = {}^t\boldsymbol{X}\,({}^tPAP)\,\boldsymbol{X} = \lambda_1X^2 + \lambda_2Y^2$$

and the $XY$ term disappears (the **standard form**).

### Example 9-3

What figure is the curve $5x^2 - 4xy + 2y^2 = 6$?

**Solution** $A = \begin{pmatrix} 5 & -2 \\ -2 & 2 \end{pmatrix}$. The characteristic equation is $(5 - \lambda)(2 - \lambda) - 4 = \lambda^2 - 7\lambda + 6 = (\lambda - 1)(\lambda - 6) = 0$, with eigenvalues $1, 6$.

- $\lambda = 1$: from $4x - 2y = 0$, $(1, 2)$; unit vector $\dfrac{1}{\sqrt{5}}(1, 2)$
- $\lambda = 6$: from $-x - 2y = 0$, $(-2, 1)$; unit vector $\dfrac{1}{\sqrt{5}}(-2, 1)$

Taking these two directions as the new $X$ and $Y$ axes,

$$X^2 + 6Y^2 = 6 \quad\text{that is}\quad \frac{X^2}{6} + Y^2 = 1$$

It is a **slanted ellipse** with semi-axis length $\sqrt{6}$ in the direction of $(1, 2)$ and length 1 in the direction of $(-2, 1)$.

![5x² − 4xy + 2y² = 6 is an ellipse whose axes point along the eigenvectors](images/en/ellipse.svg)

> **Key point**: The sign of a quadratic form's value is decided by the eigenvalues. If all eigenvalues are positive, it is always positive for $\boldsymbol{x} \ne \boldsymbol{0}$ (**positive definite**). The variance–covariance matrix in statistics is a positive definite (or positive semidefinite) symmetric matrix (Chapter 10).

## Exercises

1. Check that $\begin{pmatrix} \frac{3}{5} & -\frac{4}{5} \\ \frac{4}{5} & \frac{3}{5} \end{pmatrix}$ is an orthogonal matrix.
2. Diagonalize $A = \begin{pmatrix} 1 & 2 \\ 2 & 1 \end{pmatrix}$ with an orthogonal matrix.
3. What figure is $x^2 + 4xy + y^2 = 3$?

## Answers to the exercises

1. The dot product of the columns is $\frac{3}{5} \cdot (-\frac{4}{5}) + \frac{4}{5} \cdot \frac{3}{5} = 0$, and each length is $\sqrt{\frac{9}{25} + \frac{16}{25}} = 1$. They are orthonormal, so it is an orthogonal matrix ($\det = 1$, so a rotation)
2. From Exercise 1 of Chapter 8, the eigenvalues are $3, -1$ and the eigenvectors $(1, 1)$, $(1, -1)$. $P = \dfrac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$, ${}^tPAP = \begin{pmatrix} 3 & 0 \\ 0 & -1 \end{pmatrix}$
3. It is the matrix of exercise 2, so $3X^2 - Y^2 = 3$, that is, $X^2 - \dfrac{Y^2}{3} = 1$. A **hyperbola** with its axis in the direction of $(1, 1)$ (if an eigenvalue is negative, it is a hyperbola, not an ellipse)
