# Appendix A. Summary of formulas

## Vectors (Chapter 1)

| Item | Formula |
| --- | --- |
| Magnitude | $\lvert\boldsymbol{a}\rvert = \sqrt{a_1^2 + a_2^2 + a_3^2}$ |
| Dot product | $\boldsymbol{a} \cdot \boldsymbol{b} = a_1b_1 + a_2b_2 + a_3b_3 = \lvert\boldsymbol{a}\rvert\lvert\boldsymbol{b}\rvert\cos\theta$ |
| Orthogonal | $\boldsymbol{a} \cdot \boldsymbol{b} = 0$ |
| Projection | $\dfrac{\boldsymbol{a} \cdot \boldsymbol{b}}{\lvert\boldsymbol{a}\rvert^2}\boldsymbol{a}$ |
| Cross product | $(a_2b_3 - a_3b_2,\ a_3b_1 - a_1b_3,\ a_1b_2 - a_2b_1)$. Its magnitude is the area of the parallelogram |

## Matrices (Chapters 2 and 3)

| Item | Formula |
| --- | --- |
| Shape of a product | $(l \times m)(m \times n) = (l \times n)$ |
| Commutative law | In general $AB \ne BA$ |
| Transpose | ${}^t(AB) = {}^tB\,{}^tA$ |
| 2×2 inverse | $\dfrac{1}{ad - bc}\begin{pmatrix} d & -b \\ -c & a \end{pmatrix}$ ($ad - bc \ne 0$) |
| Inverse of a product | $(AB)^{-1} = B^{-1}A^{-1}$ |
| Cayley–Hamilton | $A^2 - (a + d)A + (ad - bc)E = O$ |
| Rotation | $\begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$ |
| Composite transformation | Multiply the matrix of the later transformation on the **left** |

## Systems of equations and rank (Chapter 4)

| Condition | Solutions |
| --- | --- |
| $\text{rank}\,A = \text{rank}(A \mid \boldsymbol{b}) = n$ | Exactly one |
| $\text{rank}\,A = \text{rank}(A \mid \boldsymbol{b}) < n$ | Infinitely many ($n - \text{rank}\,A$ free parameters) |
| $\text{rank}\,A < \text{rank}(A \mid \boldsymbol{b})$ | None |

Inverse: $(A \mid E) \to (E \mid A^{-1})$

## Determinants (Chapter 5)

| Item | Formula / property |
| --- | --- |
| Order 2 | $ad - bc$ |
| Order 3 | Rule of Sarrus |
| Swapping rows | The sign changes |
| Multiplying a row by $k$ | Multiplied by $k$ |
| Adding a multiple of another row to a row | Unchanged |
| Transpose | Unchanged |
| Product | $\det(AB) = \det A \det B$ |
| Cofactor expansion | $\det A = \sum_j a_{ij}\tilde{a}_{ij}$, $\tilde{a}_{ij} = (-1)^{i+j}D_{ij}$ |
| Inverse | $A^{-1} = \dfrac{1}{\det A}\tilde{A}$ |
| Cramer | $x_j = \dfrac{\det A_j}{\det A}$ |

## Vector spaces and linear maps (Chapters 6 and 7)

| Item | Formula / property |
| --- | --- |
| Testing linear independence | Rank of the arranged matrix = number of vectors ($\det \ne 0$ if square) |
| Dimension | The number of vectors in a basis |
| Representation matrix | Arrange where the basis vectors go as columns |
| Rank–nullity theorem | $\dim \text{Ker}\,f + \dim \text{Im}\,f = \dim V$ |
| Change of basis | $B = P^{-1}AP$ |

## Eigenvalues and diagonalization (Chapters 8 and 9)

| Item | Formula / property |
| --- | --- |
| Characteristic equation | $\det(A - \lambda E) = 0$ |
| Sum and product of eigenvalues | Sum $= \text{tr}\,A$, product $= \det A$ |
| Diagonalization | $P^{-1}AP = \text{diag}(\lambda_1, \dots, \lambda_n)$ ($P$ has the eigenvectors as columns) |
| $n$th power | $A^n = PD^nP^{-1}$ |
| Orthogonal matrix | ${}^tPP = E$, $P^{-1} = {}^tP$, $\det P = \pm1$ |
| Real symmetric matrix | Real eigenvalues, orthogonal eigenvectors, always diagonalizable by an orthogonal matrix |
| Quadratic form | ${}^t\boldsymbol{x}A\boldsymbol{x} \to \lambda_1X^2 + \lambda_2Y^2$ |
| Normal equations | ${}^tXX\boldsymbol{\beta} = {}^tX\boldsymbol{y}$ |

## Equivalent statements for an $n \times n$ square matrix $A$

- $A$ has an inverse
- $\det A \ne 0$
- $\text{rank}\,A = n$
- The column (row) vectors of $A$ are linearly independent
- The only solution of $A\boldsymbol{x} = \boldsymbol{0}$ is $\boldsymbol{0}$ ($\text{Ker} = \{\boldsymbol{0}\}$)
- For every $\boldsymbol{b}$, $A\boldsymbol{x} = \boldsymbol{b}$ has exactly one solution
- 0 is not an eigenvalue of $A$
