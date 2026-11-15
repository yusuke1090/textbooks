# 7. Linear maps

## Linear maps

When a map $f$ from a vector space $V$ to $W$ satisfies

$$f(\boldsymbol{a} + \boldsymbol{b}) = f(\boldsymbol{a}) + f(\boldsymbol{b}), \qquad f(k\boldsymbol{a}) = kf(\boldsymbol{a})$$

$f$ is called a **linear map** (when $V = W$, a **linear transformation**: the linear transformations of Chapter 3). It is the property that "adding and then mapping gives the same result as mapping and then adding".

- The map $f(\boldsymbol{x}) = A\boldsymbol{x}$ that multiplies by a matrix $A$ is a linear map
- Conversely, a linear map from $\mathbb{R}^n$ to $\mathbb{R}^m$ **can always be written as multiplication by some $m \times n$ matrix**. This matrix is called the **representation matrix**

### How to make the representation matrix

Just **arrange as columns** where the standard basis vectors $\boldsymbol{e}_1, \dots, \boldsymbol{e}_n$ go, $f(\boldsymbol{e}_1), \dots, f(\boldsymbol{e}_n)$ (the same idea as the linear transformations of Chapter 3).

$$A = \big(f(\boldsymbol{e}_1)\ \ f(\boldsymbol{e}_2)\ \cdots\ f(\boldsymbol{e}_n)\big)$$

### Example 7-1

Find the representation matrix of the linear map from $\mathbb{R}^3$ to $\mathbb{R}^2$ given by $f(x, y, z) = (x + 2y,\ y - z)$.

**Solution** $f(\boldsymbol{e}_1) = (1, 0)$, $f(\boldsymbol{e}_2) = (2, 1)$ and $f(\boldsymbol{e}_3) = (0, -1)$, so

$$A = \begin{pmatrix} 1 & 2 & 0 \\ 0 & 1 & -1 \end{pmatrix}$$

(Check: $A\begin{pmatrix} x \\ y \\ z \end{pmatrix} = \begin{pmatrix} x + 2y \\ y - z \end{pmatrix}$)

### Example 7-2

On $P_2$ (polynomials of degree 2 or less), differentiation $D(p) = p'$ is a linear map. Find its representation matrix with respect to the basis $1, x, x^2$.

**Solution** $D(1) = 0$, $D(x) = 1$ and $D(x^2) = 2x$. In coordinates with respect to the basis $1, x, x^2$, these are $(0, 0, 0)$, $(1, 0, 0)$ and $(0, 2, 0)$. Arranging them as columns,

$$\begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 2 \\ 0 & 0 & 0 \end{pmatrix}$$

For example, multiplying $3 + 4x + 5x^2$ (coordinates $(3, 4, 5)$) gives $(4, 10, 0)$, that is, $4 + 10x$. This matches the derivative. "**Even differentiation becomes a matrix calculation**" is the linear algebra way of seeing it.

## Kernel and image

For a linear map $f: V \to W$,

- **Kernel**: $\text{Ker}\,f = \{\boldsymbol{x} \in V \mid f(\boldsymbol{x}) = \boldsymbol{0}\}$ (everything mapped to $\boldsymbol{0}$)
- **Image**: $\text{Im}\,f = \{f(\boldsymbol{x}) \mid \boldsymbol{x} \in V\}$ (everything mapped to)

Both are subspaces. Written with a matrix $A$,

- $\text{Ker}\,f$ is the set of all solutions of the homogeneous system $A\boldsymbol{x} = \boldsymbol{0}$
- $\text{Im}\,f$ is the subspace **spanned by the column vectors** of $A$. Its dimension is $\text{rank}\,A$

## The rank–nullity theorem

When $f: V \to W$ is a linear map,

$$\dim(\text{Ker}\,f) + \dim(\text{Im}\,f) = \dim V$$

It means "what was squashed (the kernel) plus what remains (the image) gives the original dimension". Written with a matrix, for a matrix $A$ with $n$ columns,

$$(\text{number of free parameters in the solutions of } A\boldsymbol{x} = \boldsymbol{0}) + \text{rank}\,A = n$$

This is the same as "there are $n - \text{rank}\,A$ free parameters" in Chapter 4.

### Example 7-3

For the linear transformation given by $A = \begin{pmatrix} 1 & 2 & 3 \\ 2 & 4 & 6 \\ 1 & 1 & 1 \end{pmatrix}$, find bases and dimensions of Ker and Im.

**Solution** Doing row operations,

$$\begin{pmatrix} 1 & 2 & 3 \\ 2 & 4 & 6 \\ 1 & 1 & 1 \end{pmatrix} \to \begin{pmatrix} 1 & 2 & 3 \\ 0 & 0 & 0 \\ 0 & -1 & -2 \end{pmatrix} \to \begin{pmatrix} 1 & 2 & 3 \\ 0 & 1 & 2 \\ 0 & 0 & 0 \end{pmatrix}$$

$\text{rank}\,A = 2$.

- **Ker**: $y + 2z = 0$ and $x + 2y + 3z = 0$. Setting $z = t$ gives $y = -2t$ and $x = -2y - 3z = t$. $\text{Ker} = \{t(1, -2, 1)\}$, basis $(1, -2, 1)$, dimension **1**
- **Im**: In the echelon form, the pivots were in columns 1 and 2. Columns 1 and 2 of the original $A$, $(1, 2, 1)$ and $(2, 4, 1)$, are a basis; dimension **2**

$1 + 2 = 3$, so the rank–nullity theorem holds. This transformation **squashes** $\mathbb{R}^3$ **onto a plane**, and every point on the line $t(1, -2, 1)$ goes to $\boldsymbol{0}$.

> **Key point**: For a linear transformation $f: \mathbb{R}^n \to \mathbb{R}^n$, $\text{Ker}\,f = \{\boldsymbol{0}\}$ $\iff$ $\text{Im}\,f = \mathbb{R}^n$ $\iff$ $\det A \ne 0$ $\iff$ there is an inverse transformation. The list of "equivalent statements" in Chapter 4 has grown again.

## Changing the basis and the representation matrix

Even for the same linear transformation, the representation matrix changes with **which basis you look through**.

Let $P$ (the **change-of-basis matrix**) be the matrix with a new basis $\boldsymbol{p}_1, \dots, \boldsymbol{p}_n$ of $\mathbb{R}^n$ as its columns. A linear transformation whose representation matrix in the standard basis is $A$ then has the representation matrix

$$B = P^{-1}AP$$

in the new basis.

- Reason: coordinates $\boldsymbol{c}$ in the new basis are $P\boldsymbol{c}$ in the original coordinates. Multiply that by $A$ and go back to the new coordinates (multiply by $P^{-1}$)
- Matrices like $A$ and $P^{-1}AP$ that turn into each other by a change of basis are called **similar**. Similar matrices have the same determinant, trace, rank and eigenvalues (Chapter 8)

### Example 7-4

When $A = \begin{pmatrix} 4 & 1 \\ 2 & 3 \end{pmatrix}$ and the new basis is $\boldsymbol{p}_1 = (1, 1)$, $\boldsymbol{p}_2 = (1, -2)$, find $P^{-1}AP$.

**Solution** $P = \begin{pmatrix} 1 & 1 \\ 1 & -2 \end{pmatrix}$, $\det P = -3$, $P^{-1} = \dfrac{1}{3}\begin{pmatrix} 2 & 1 \\ 1 & -1 \end{pmatrix}$.

$$AP = \begin{pmatrix} 5 & 2 \\ 5 & -4 \end{pmatrix}, \qquad P^{-1}AP = \frac{1}{3}\begin{pmatrix} 10 + 5 & 4 - 4 \\ 5 - 5 & 2 + 4 \end{pmatrix} = \begin{pmatrix} 5 & 0 \\ 0 & 2 \end{pmatrix}$$

It became a **diagonal matrix**. Seen in this basis, $A$ was a very simple transformation: "5 times in the direction of $\boldsymbol{p}_1$, 2 times in the direction of $\boldsymbol{p}_2$". How to find such a "good basis" is the subject of the next chapter, eigenvalues and eigenvectors.

## Exercises

1. Is the map $f(x, y) = (x + 1, y)$ on $\mathbb{R}^2$ a linear map?
2. Find Ker and Im of $f(x, y) = (x + y,\ 2x + 2y)$.
3. When a $5 \times 7$ matrix $A$ has rank 4, what is the dimension of the solution space of $A\boldsymbol{x} = \boldsymbol{0}$?

## Answers to the exercises

1. $f(0, 0) = (1, 0) \ne (0, 0)$. A linear map always sends $\boldsymbol{0}$ to $\boldsymbol{0}$, so it is **not a linear map**
2. The representation matrix is $\begin{pmatrix} 1 & 1 \\ 2 & 2 \end{pmatrix}$, rank 1. Ker is the line $x + y = 0$, $\{t(1, -1)\}$ (dimension 1). Im is the line in the direction of $(1, 2)$, $\{s(1, 2)\}$ (dimension 1)
3. By the rank–nullity theorem, $7 - 4 = 3$
