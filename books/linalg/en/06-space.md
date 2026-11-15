# 6. Vector spaces

## What you will learn in this chapter

- Vector spaces (collections where you can add and multiply by scalars)
- Subspaces
- Linear combinations, linear independence and dependence, and how to test them
- Bases and dimension
- Coordinates with respect to a basis

From here things get a little more abstract. The idea of this chapter is to forget "arrows" and think of anything as a vector if "**you can add it and multiply it by scalars, and the usual rules of calculation hold**".

## Vector spaces

When, in a set $V$, you can form sums $\boldsymbol{a} + \boldsymbol{b}$ and scalar multiples $k\boldsymbol{a}$, the results are again in $V$, and rules like the following hold, $V$ is called a **vector space** (linear space).

- Addition is commutative and associative, there is a zero vector $\boldsymbol{0}$, and there is $-\boldsymbol{a}$
- $k(\boldsymbol{a} + \boldsymbol{b}) = k\boldsymbol{a} + k\boldsymbol{b}$, $(k + l)\boldsymbol{a} = k\boldsymbol{a} + l\boldsymbol{a}$, $(kl)\boldsymbol{a} = k(l\boldsymbol{a})$, $1\boldsymbol{a} = \boldsymbol{a}$

Examples:

| Vector space | Contents |
| --- | --- |
| $\mathbb{R}^n$ | Lists of $n$ real numbers |
| All $2 \times 2$ matrices | Sums and scalar multiples of matrices |
| All polynomials of degree 2 or less, $P_2$ | $a + bx + cx^2$. Sums and scalar multiples of polynomials |
| All solutions of $A\boldsymbol{x} = \boldsymbol{0}$ | Adding solutions or multiplying them by scalars gives solutions again |

## Subspaces

When a part $W$ of a vector space $V$ is **closed under addition and scalar multiplication** on its own (the results are again in $W$), $W$ is called a **subspace** of $V$.

> **How to test**: Check these three. (1) $\boldsymbol{0} \in W$, (2) if $\boldsymbol{a}, \boldsymbol{b} \in W$ then $\boldsymbol{a} + \boldsymbol{b} \in W$, (3) if $\boldsymbol{a} \in W$ then $k\boldsymbol{a} \in W$

### Example 6-1

Are the following sets in $\mathbb{R}^3$ subspaces?

(1) $W_1 = \{(x, y, z) \mid x + y + z = 0\}$　(2) $W_2 = \{(x, y, z) \mid x + y + z = 1\}$

**Solution**

(1) $\boldsymbol{0} = (0, 0, 0)$ is in it, since $0 + 0 + 0 = 0$. If $\boldsymbol{a}, \boldsymbol{b} \in W_1$, the sums of their components are each 0, so the sum of the components of $\boldsymbol{a} + \boldsymbol{b}$ is $0 + 0 = 0$, and that of $k\boldsymbol{a}$ is $k \cdot 0 = 0$. So it is **a subspace** (a plane through the origin).

(2) $(0, 0, 0)$ is not in it, since $0 \ne 1$. So it is **not a subspace** (a plane not through the origin).

> **Key point**: A subspace always **passes through the origin**. The subspaces of $\mathbb{R}^3$ are of only four kinds: $\{\boldsymbol{0}\}$, lines through the origin, planes through the origin, and all of $\mathbb{R}^3$.

## Linear combinations and linear independence

A sum of scalar multiples of vectors $\boldsymbol{a}_1, \dots, \boldsymbol{a}_k$,

$$c_1\boldsymbol{a}_1 + c_2\boldsymbol{a}_2 + \cdots + c_k\boldsymbol{a}_k$$

is called a **linear combination**. If

$$c_1\boldsymbol{a}_1 + c_2\boldsymbol{a}_2 + \cdots + c_k\boldsymbol{a}_k = \boldsymbol{0}$$

holds only when $c_1 = c_2 = \cdots = c_k = 0$, then $\boldsymbol{a}_1, \dots, \boldsymbol{a}_k$ are **linearly independent**; otherwise they are **linearly dependent**.

- Linearly dependent = one of them can be written as a linear combination of the rest (there is a "wasted vector")
- Linearly independent = none of them can be replaced by the others

### How to test

If you make the matrix $A = (\boldsymbol{a}_1\ \boldsymbol{a}_2\ \cdots\ \boldsymbol{a}_k)$ by **arranging the vectors as columns**, the equation above is the homogeneous system $A\boldsymbol{c} = \boldsymbol{0}$ (Chapter 4).

- If $\text{rank}\,A = k$ (the number of vectors), they are linearly independent; if smaller, linearly dependent
- For $n$ vectors of dimension $n$, $\det A \ne 0 \iff$ linearly independent

### Example 6-2

Are the following vectors linearly independent?

(1) $\boldsymbol{a}_1 = (1, 2, 1)$, $\boldsymbol{a}_2 = (2, 1, 0)$, $\boldsymbol{a}_3 = (1, -1, -1)$
(2) $\boldsymbol{b}_1 = (1, 1, 0)$, $\boldsymbol{b}_2 = (0, 1, 1)$, $\boldsymbol{b}_3 = (1, 0, 1)$

**Solution**

(1) The determinant with them as columns is

$$\begin{vmatrix} 1 & 2 & 1 \\ 2 & 1 & -1 \\ 1 & 0 & -1 \end{vmatrix} = (-1) + (-2) + 0 - 1 - (-4) - 0 = 0$$

so they are **linearly dependent**. In fact, $\boldsymbol{a}_3 = \boldsymbol{a}_2 - \boldsymbol{a}_1$.

(2)

$$\begin{vmatrix} 1 & 0 & 1 \\ 1 & 1 & 0 \\ 0 & 1 & 1 \end{vmatrix} = 1 + 0 + 1 - 0 - 0 - 0 = 2 \ne 0$$

so they are **linearly independent**.

## Bases and dimension

When vectors $\boldsymbol{v}_1, \dots, \boldsymbol{v}_n$ of a vector space $V$

1. are linearly independent, and
2. every vector of $V$ can be written as a linear combination of them (they **span** $V$),

$\{\boldsymbol{v}_1, \dots, \boldsymbol{v}_n\}$ is called a **basis** of $V$. There are many ways to choose a basis, but **the number of vectors $n$ is always the same**, and it is called the **dimension** of $V$ ($\dim V$).

- An example of a basis of $\mathbb{R}^3$: $\boldsymbol{e}_1 = (1, 0, 0)$, $\boldsymbol{e}_2 = (0, 1, 0)$, $\boldsymbol{e}_3 = (0, 0, 1)$ (the **standard basis**). $\dim \mathbb{R}^3 = 3$
- $\boldsymbol{b}_1, \boldsymbol{b}_2, \boldsymbol{b}_3$ in Example 6-2 (2) are also a basis of $\mathbb{R}^3$
- An example of a basis of $P_2$ (polynomials of degree 2 or less): $1, x, x^2$. $\dim P_2 = 3$

### Example 6-3

Find a basis and the dimension of $W = \{(x, y, z) \mid x + y + z = 0\}$.

**Solution** For points satisfying $x + y + z = 0$, setting $y = s$ and $z = t$ gives $x = -s - t$, so

$$\begin{pmatrix} x \\ y \\ z \end{pmatrix} = s\begin{pmatrix} -1 \\ 1 \\ 0 \end{pmatrix} + t\begin{pmatrix} -1 \\ 0 \\ 1 \end{pmatrix}$$

These two vectors span $W$ and are linearly independent (neither is a scalar multiple of the other). So a basis is $\{(-1, 1, 0),\ (-1, 0, 1)\}$ and $\dim W = 2$ (a plane through the origin).

> **Key point**: The dimension of the subspace spanned by some vectors equals the **rank** of the matrix made by arranging them.

## Coordinates with respect to a basis

Given a basis $\{\boldsymbol{v}_1, \dots, \boldsymbol{v}_n\}$, every vector $\boldsymbol{x}$ can be written in exactly one way as $\boldsymbol{x} = c_1\boldsymbol{v}_1 + \cdots + c_n\boldsymbol{v}_n$. $(c_1, \dots, c_n)$ are called the **coordinates** with respect to that basis.

### Example 6-4

Write $\boldsymbol{x} = (3, 2, 1)$ as a linear combination of the basis $\boldsymbol{b}_1 = (1, 1, 0)$, $\boldsymbol{b}_2 = (0, 1, 1)$, $\boldsymbol{b}_3 = (1, 0, 1)$.

**Solution** Writing $c_1\boldsymbol{b}_1 + c_2\boldsymbol{b}_2 + c_3\boldsymbol{b}_3 = \boldsymbol{x}$ in components,

$$c_1 + c_3 = 3, \qquad c_1 + c_2 = 2, \qquad c_2 + c_3 = 1$$

Adding all three gives $2(c_1 + c_2 + c_3) = 6$, so $c_1 + c_2 + c_3 = 3$. Subtracting each equation gives $c_2 = 0$, $c_3 = 1$ and $c_1 = 2$.

$$\boldsymbol{x} = 2\boldsymbol{b}_1 + 0\boldsymbol{b}_2 + 1\boldsymbol{b}_3$$

Even for the same vector, changing the basis changes the coordinates. Choosing well "**which basis to look through**" is the idea behind diagonalization in Chapters 8 and 9.

## Exercises

1. Is the set $W = \{(x, y) \mid y = x^2\}$ in $\mathbb{R}^2$ a subspace?
2. Find $k$ so that $(1, 2)$ and $(3, k)$ are linearly dependent.
3. Find the dimension of the subspace spanned by $(1, 0, 1)$, $(2, 1, 0)$ and $(0, 1, -2)$.
4. Are the vectors $1 + x$, $x + x^2$ and $1 + x^2$ of $P_2$ linearly independent?

## Answers to the exercises

1. $(1, 1) \in W$, but twice it, $(2, 2)$, is not in it since $2 \ne 2^2$. **Not a subspace**
2. From $\begin{vmatrix} 1 & 3 \\ 2 & k \end{vmatrix} = k - 6 = 0$, $k = 6$
3. The determinant of the matrix with them as columns, $\begin{pmatrix} 1 & 2 & 0 \\ 0 & 1 & 1 \\ 1 & 0 & -2 \end{pmatrix}$, is $-2 + 2 + 0 - 0 - 0 - 0 = 0$. The rank is 2 ($(0, 1, -2) = (2, 1, 0) - 2(1, 0, 1)$). The dimension is **2**
4. Listing the coefficients gives $(1, 1, 0)$, $(0, 1, 1)$, $(1, 0, 1)$ (the coefficients of the constant, $x$ and $x^2$). This is the same as Example 6-2 (2), with determinant $2 \ne 0$. **Linearly independent**
