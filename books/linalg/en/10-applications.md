# 10. NumPy, and connections to statistics and machine learning

## What you will learn in this chapter

- Calculating with matrices in NumPy
- Least squares (regression analysis) is "projection" and "the normal equations"
- Principal component analysis is "the eigenvalues and eigenvectors of the variance–covariance matrix"
- An outline of the singular value decomposition (SVD)

Regression analysis (OLS) in the "Statistics Textbook" and dimensionality reduction (PCA) in the "Machine Learning Textbook" are built from the linear algebra in this textbook. The code was checked with NumPy 2.5 (for how to write Python, see the "Python Textbook").

## Calculating with matrices in NumPy

```python
import numpy as np

A = np.array([[4.0, 1.0],
              [2.0, 3.0]])
b = np.array([5.0, 6.0])

print(A @ A)                     # matrix product (careful: * is the entry-by-entry product)
print(A.T)                       # transpose
print(np.linalg.det(A))          # determinant
print(np.linalg.inv(A))          # inverse
print(np.linalg.solve(A, b))     # solve A x = b
print(np.linalg.matrix_rank(A))  # rank

vals, vecs = np.linalg.eig(A)    # eigenvalues and eigenvectors (columns)
print(vals)
print(vecs)
```

```text
[[18.  7.]
 [14. 11.]]
[[4. 2.]
 [1. 3.]]
10.000000000000002
[[ 0.3 -0.1]
 [-0.2  0.4]]
[0.9 1.4]
2
[5.+0.j 2.+0.j]
[[ 0.70710678+0.j -0.4472136 +0.j]
 [ 0.70710678+0.j  0.89442719+0.j]]
```

- The determinant comes out as `10.000000000000002` because of the computer's rounding error with decimals. $\det A = 12 - 2 = 10$
- The eigenvalues 5 and 2 are the same as in Example 8-1 of Chapter 8. The eigenvectors come out **scaled to length 1**: $(0.707, 0.707) = \frac{1}{\sqrt{2}}(1, 1)$ and $(-0.447, 0.894) = \frac{1}{\sqrt{5}}(-1, 2)$. They point the same way as $(1, 1)$ and $(1, -2)$ in Chapter 8 (−1 times an eigenvector is the same eigenvector)
- In NumPy 2.5, `eig` returns eigenvalues in complex form (with imaginary part 0), like `5.+0.j`, even when they are real. **For symmetric matrices, use `np.linalg.eigh`**: it returns real values, sorted smallest first
- For systems of equations, use `solve(A, b)` rather than `inv(A) @ b` (it is faster, with smaller errors)

## Least squares and the normal equations

Consider regression analysis, which fits a line $y = \beta_0 + \beta_1x$ to data. For the data $(1, 2)$, $(2, 3)$, $(3, 5)$, $(4, 6)$,

$$\begin{pmatrix} 1 & 1 \\ 1 & 2 \\ 1 & 3 \\ 1 & 4 \end{pmatrix}\begin{pmatrix} \beta_0 \\ \beta_1 \end{pmatrix} \approx \begin{pmatrix} 2 \\ 3 \\ 5 \\ 6 \end{pmatrix} \qquad (X\boldsymbol{\beta} \approx \boldsymbol{y})$$

There are 4 equations and 2 unknowns, so there is no exact solution ("no solution" in Chapter 4). So we choose the $\boldsymbol{\beta}$ that makes the length (squared) of the **residual** $\boldsymbol{y} - X\boldsymbol{\beta}$ smallest.

### Thinking with projection

$X\boldsymbol{\beta}$ is a linear combination of the column vectors of $X$, so it moves within the subspace spanned by the columns of $X$ ($\text{Im}$ in Chapter 7). The point closest to $\boldsymbol{y}$ is the **projection** of $\boldsymbol{y}$ onto that subspace (an extension of projection in Chapter 1). At that point, the residual is **orthogonal** to the subspace.

$${}^tX(\boldsymbol{y} - X\boldsymbol{\beta}) = \boldsymbol{0} \quad\Longrightarrow\quad {}^tX X\boldsymbol{\beta} = {}^tX\boldsymbol{y}$$

These are called the **normal equations**. If ${}^tXX$ has an inverse, $\boldsymbol{\beta} = ({}^tXX)^{-1}\,{}^tX\boldsymbol{y}$.

### Example 10-1

Find the regression line for the data above.

**Solution**

$${}^tXX = \begin{pmatrix} 4 & 10 \\ 10 & 30 \end{pmatrix}, \qquad {}^tX\boldsymbol{y} = \begin{pmatrix} 16 \\ 47 \end{pmatrix}$$

Since $\det({}^tXX) = 120 - 100 = 20$ (the inverse formula of Chapter 3),

$$\boldsymbol{\beta} = \frac{1}{20}\begin{pmatrix} 30 & -10 \\ -10 & 4 \end{pmatrix}\begin{pmatrix} 16 \\ 47 \end{pmatrix} = \frac{1}{20}\begin{pmatrix} 10 \\ 28 \end{pmatrix} = \begin{pmatrix} 0.5 \\ 1.4 \end{pmatrix}$$

The regression line is $y = 0.5 + 1.4x$.

![Least squares. The line with the smallest sum of squared residuals (red dotted lines)](images/en/least-squares.svg)

```python
import numpy as np

x = np.array([1, 2, 3, 4])
y = np.array([2, 3, 5, 6])
X = np.column_stack([np.ones_like(x), x])    # column 1 is 1s for the intercept

beta = np.linalg.solve(X.T @ X, X.T @ y)     # normal equations XᵀX β = Xᵀy
print(beta)

beta2, *_ = np.linalg.lstsq(X, y, rcond=None)  # usually use this (numerically stable)
print(beta2)

r = y - X @ beta                             # residuals
print(X.T @ r)                               # the residuals are orthogonal to the columns of X (almost 0)
```

```text
[0.5 1.4]
[0.5 1.4]
[2.66453526e-15 5.77315973e-15]
```

- The last line is the dot products of the residuals with the columns of $X$: 0 apart from rounding error. This confirms that **the residuals are orthogonal**
- If the explanatory variables are too similar (**multicollinearity**), the columns of $X$ are almost linearly dependent, the determinant of ${}^tXX$ gets close to 0, and $\boldsymbol{\beta}$ swings wildly. This is what Chapter 8 of the "Statistics Textbook" looks like from the linear algebra side

## Principal component analysis (PCA)

This is a way to **summarize** data with many items using a few axes.

1. Subtract the mean of the data (move the center to the origin)
2. Make the **variance–covariance matrix** $C$ (a symmetric matrix)
3. Find the eigenvalues and eigenvectors of $C$ (diagonalizing a symmetric matrix, Chapter 9)
4. The eigenvectors sorted by eigenvalue, largest first, are **the axes of the first principal component, the second, and so on**. The eigenvalue is the **variance** (amount of spread) in the direction of that axis

Remember the ellipse figure in Chapter 9. When data points spread out like a slanted ellipse, its **long axis** is the first principal component.

```python
import numpy as np

# daily milk yield (kg) and feed eaten (kg) of 5 cows
data = np.array([[25, 18],
                 [30, 21],
                 [28, 20],
                 [35, 24],
                 [32, 23]], dtype=float)

C = np.cov(data, rowvar=False)        # variance–covariance matrix (symmetric)
print(C)

vals, vecs = np.linalg.eigh(C)        # for symmetric matrices; eigenvalues sorted smallest first
order = vals.argsort()[::-1]          # re-sort largest first
vals, vecs = vals[order], vecs[:, order]
vecs = vecs * np.sign(vecs[0])       # align directions (−1 times an eigenvector is the same)
print(vals)
print(vecs)
print(vals / vals.sum())              # explained variance ratio (share of total spread each axis explains)

centered = data - data.mean(axis=0)
score = centered @ vecs[:, 0]         # first principal component scores (summarized in 1 dimension)
print(score.round(2))
```

```text
[[14.5  9. ]
 [ 9.   5.7]]
[20.11798383  0.08201617]
[[ 0.84829539  0.52952331]
 [ 0.52952331 -0.84829539]]
[0.99593979 0.00406021]
[-5.94 -0.11 -2.33  5.72  2.65]
```

- The first principal component's axis points along $(0.85, 0.53)$ (the direction where both milk and feed are larger). Its explained variance ratio is **99.6%**, meaning these two items can be explained almost entirely by one axis: "eat a lot, give a lot"
- The last line summarizes the 5 cows in one number each. The 4th cow (35 kg of milk) is largest, and the 1st (25 kg) is smallest
- When the items have different units (kg and °C, for example), standardize first (mean 0, variance 1). scikit-learn's `PCA` does this calculation inside (see the "Machine Learning Textbook")

## The singular value decomposition (SVD)

There is a decomposition that always works, even for matrices that are not square or cannot be diagonalized.

$$A = U\Sigma\,{}^tV$$

- $U$ and $V$ are orthogonal matrices, and $\Sigma$ has the **singular values** ($\sigma_1 \ge \sigma_2 \ge \cdots \ge 0$) on its diagonal
- Meaning: any linear transformation can be split into "rotation (${}^tV$) → stretching and shrinking along each axis ($\Sigma$) → rotation ($U$)"
- Keeping only the large singular values approximates a matrix with less data (image compression, recommendation systems, noise removal). In practice, PCA is also calculated with the SVD of the data matrix
- In NumPy, `U, s, Vt = np.linalg.svd(A)`

## What to learn next

- **Jordan normal form**: a form close to diagonal for matrices that cannot be diagonalized
- **The matrix exponential** $e^{At}$: systems of differential equations (control engineering; the theory behind controlling drones with ROS 2 and ArduPilot)
- **Numerical linear algebra**: ways to calculate with large matrices quickly and accurately (LU decomposition, QR decomposition, iterative methods)
