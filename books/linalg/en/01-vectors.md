# 1. Vectors

## What you will learn in this chapter

- The components of a vector; sum, difference and scalar multiple
- The magnitude of a vector and unit vectors
- The dot product, the angle between two vectors, and orthogonality
- Orthogonal projection
- The cross product of space vectors

This textbook covers the linear algebra taught in the first and second years of university, working through examples one at a time. It is written so that you can read it if you know high-school math (vectors, quadratic equations, trigonometric functions). Each chapter ends with exercises and answers. Calculations in Python (NumPy) are collected in Chapter 10.

## What is a vector?

A **vector** is a quantity with a "direction" and a "magnitude". We draw it as an arrow and write it with components (coordinates).

$$\boldsymbol{a} = \begin{pmatrix} 2 \\ 1 \end{pmatrix} \quad\text{or}\quad \boldsymbol{a} = (2, 1)$$

- A vector in the plane has 2 numbers; a vector in space has 3. In general, a list of $n$ numbers is called an **$n$-dimensional vector**, and the set of all of them is written $\mathbb{R}^n$
- In linear algebra, vectors are basically **written vertically** (column vectors). To save space they are sometimes written horizontally
- If the direction and magnitude are the same, it is the same vector wherever you draw it. Usually we draw it from the origin

## Sum, difference and scalar multiple

Calculate component by component.

$$\boldsymbol{a} + \boldsymbol{b} = \begin{pmatrix} a_1 + b_1 \\ a_2 + b_2 \end{pmatrix}, \qquad k\boldsymbol{a} = \begin{pmatrix} k a_1 \\ k a_2 \end{pmatrix}$$

![The sum of vectors. The diagonal of the parallelogram made by a and b is a + b](images/en/vectors.svg)

### Example 1-1

When $\boldsymbol{a} = (2, 1)$ and $\boldsymbol{b} = (1, 3)$, find $\boldsymbol{a} + \boldsymbol{b}$ and $2\boldsymbol{a} - \boldsymbol{b}$.

**Solution**

$$\boldsymbol{a} + \boldsymbol{b} = (2+1,\ 1+3) = (3, 4)$$

$$2\boldsymbol{a} - \boldsymbol{b} = (4-1,\ 2-3) = (3, -1)$$

> **Key point**: The sum is "the diagonal of the parallelogram", and a scalar multiple is "stretched $k$ times in the same direction (the opposite direction if $k<0$)". Picture the figure, but do the calculation with components.

## Magnitude and unit vectors

The **magnitude** (length, norm) of a vector $\boldsymbol{a} = (a_1, a_2)$ is found with the Pythagorean theorem.

$$|\boldsymbol{a}| = \sqrt{a_1^2 + a_2^2}$$

In space, $|\boldsymbol{a}| = \sqrt{a_1^2 + a_2^2 + a_3^2}$. A vector of magnitude 1 is called a **unit vector**, and the unit vector in the same direction as $\boldsymbol{a}$ is $\dfrac{\boldsymbol{a}}{|\boldsymbol{a}|}$.

### Example 1-2

Find the magnitude of $\boldsymbol{a} = (3, 4)$ and the unit vector in the same direction.

**Solution** $|\boldsymbol{a}| = \sqrt{9 + 16} = 5$. The unit vector is $\dfrac{1}{5}(3, 4) = \left(\dfrac{3}{5}, \dfrac{4}{5}\right)$.

## The dot product

The **dot product** (inner product) of two vectors is the sum of the products of their components. The answer is not a vector but a **number** (a scalar).

$$\boldsymbol{a} \cdot \boldsymbol{b} = a_1 b_1 + a_2 b_2 \quad(\text{in space} + a_3 b_3)$$

The dot product has another form. If $\theta$ is the angle between the two vectors,

$$\boldsymbol{a} \cdot \boldsymbol{b} = |\boldsymbol{a}||\boldsymbol{b}|\cos\theta$$

Combining the two, you can find the angle from the components.

$$\cos\theta = \frac{\boldsymbol{a} \cdot \boldsymbol{b}}{|\boldsymbol{a}||\boldsymbol{b}|}$$

### Example 1-3

Find the angle $\theta$ between $\boldsymbol{a} = (2, 1)$ and $\boldsymbol{b} = (1, 3)$.

**Solution**

$$\boldsymbol{a} \cdot \boldsymbol{b} = 2 \cdot 1 + 1 \cdot 3 = 5, \quad |\boldsymbol{a}| = \sqrt{5}, \quad |\boldsymbol{b}| = \sqrt{10}$$

$$\cos\theta = \frac{5}{\sqrt{5}\sqrt{10}} = \frac{5}{\sqrt{50}} = \frac{5}{5\sqrt{2}} = \frac{1}{\sqrt{2}}$$

Since $0 \le \theta \le \pi$, $\theta = \dfrac{\pi}{4}$ ($45°$).

### Orthogonality

When $\boldsymbol{a} \ne \boldsymbol{0}$ and $\boldsymbol{b} \ne \boldsymbol{0}$,

$$\boldsymbol{a} \perp \boldsymbol{b} \iff \boldsymbol{a} \cdot \boldsymbol{b} = 0$$

This is because $\cos 90° = 0$. "If the dot product is 0, they are orthogonal" is an important tool you will use from here on.

### Example 1-4

Show that $\boldsymbol{a} = (1, 2, 2)$ and $\boldsymbol{b} = (2, 1, -2)$ are orthogonal.

**Solution** $\boldsymbol{a} \cdot \boldsymbol{b} = 1 \cdot 2 + 2 \cdot 1 + 2 \cdot (-2) = 2 + 2 - 4 = 0$. So they are orthogonal.

### Properties of the dot product

- $\boldsymbol{a} \cdot \boldsymbol{b} = \boldsymbol{b} \cdot \boldsymbol{a}$ (commutative law)
- $\boldsymbol{a} \cdot (\boldsymbol{b} + \boldsymbol{c}) = \boldsymbol{a} \cdot \boldsymbol{b} + \boldsymbol{a} \cdot \boldsymbol{c}$ (distributive law)
- $(k\boldsymbol{a}) \cdot \boldsymbol{b} = k(\boldsymbol{a} \cdot \boldsymbol{b})$
- $\boldsymbol{a} \cdot \boldsymbol{a} = |\boldsymbol{a}|^2 \ge 0$ (equality only when $\boldsymbol{a} = \boldsymbol{0}$)

These four properties are the basis for extending the "inner product" to general vector spaces in Chapter 9.

## Orthogonal projection

The "shadow" cast by vector $\boldsymbol{b}$ when light shines onto the direction of $\boldsymbol{a}$ is called the **orthogonal projection** of $\boldsymbol{b}$ onto $\boldsymbol{a}$.

$$\text{proj}_{\boldsymbol{a}}\,\boldsymbol{b} = \frac{\boldsymbol{a} \cdot \boldsymbol{b}}{|\boldsymbol{a}|^2}\,\boldsymbol{a}$$

![The projection of b onto a. The remaining part (red dotted line) is orthogonal to a](images/en/projection.svg)

### Example 1-5

When $\boldsymbol{a} = (2, 1)$ and $\boldsymbol{b} = (1, 3)$, find the projection of $\boldsymbol{b}$ onto $\boldsymbol{a}$, and check that the remainder $\boldsymbol{b} - \text{proj}_{\boldsymbol{a}}\boldsymbol{b}$ is orthogonal to $\boldsymbol{a}$.

**Solution** Since $\boldsymbol{a} \cdot \boldsymbol{b} = 5$ and $|\boldsymbol{a}|^2 = 5$,

$$\text{proj}_{\boldsymbol{a}}\,\boldsymbol{b} = \frac{5}{5}(2, 1) = (2, 1)$$

The remainder is $(1, 3) - (2, 1) = (-1, 2)$, and its dot product with $\boldsymbol{a}$ is $2 \cdot (-1) + 1 \cdot 2 = 0$. They are orthogonal.

> **Key point**: Projection is the operation of "splitting a vector into a component in one direction and a component at right angles to it". The Gram–Schmidt process in Chapter 9 and least squares in Chapter 10 extend this idea.

## The cross product (space vectors)

The **cross product** of space vectors $\boldsymbol{a} = (a_1, a_2, a_3)$ and $\boldsymbol{b} = (b_1, b_2, b_3)$ is the following vector.

$$\boldsymbol{a} \times \boldsymbol{b} = (a_2 b_3 - a_3 b_2,\ a_3 b_1 - a_1 b_3,\ a_1 b_2 - a_2 b_1)$$

- $\boldsymbol{a} \times \boldsymbol{b}$ is **orthogonal** to both $\boldsymbol{a}$ and $\boldsymbol{b}$
- Its magnitude $|\boldsymbol{a} \times \boldsymbol{b}|$ is the **area of the parallelogram** made by $\boldsymbol{a}$ and $\boldsymbol{b}$
- Its direction is the way a right-handed screw moves when turned from $\boldsymbol{a}$ to $\boldsymbol{b}$. $\boldsymbol{b} \times \boldsymbol{a} = -\boldsymbol{a} \times \boldsymbol{b}$

How to remember: write the components vertically twice, hide the first row and "cross-multiply", then do the second row, the third row and so on in order (you will see this again with determinants in Chapter 5).

### Example 1-6

Find the cross product of $\boldsymbol{a} = (1, 2, 0)$ and $\boldsymbol{b} = (0, 1, 3)$, and find the area of the parallelogram made by the two vectors.

**Solution**

$$\boldsymbol{a} \times \boldsymbol{b} = (2 \cdot 3 - 0 \cdot 1,\ 0 \cdot 0 - 1 \cdot 3,\ 1 \cdot 1 - 2 \cdot 0) = (6, -3, 1)$$

Check: $\boldsymbol{a} \cdot (6, -3, 1) = 6 - 6 + 0 = 0$ and $\boldsymbol{b} \cdot (6, -3, 1) = 0 - 3 + 3 = 0$. It is orthogonal to both.

The area is $|(6, -3, 1)| = \sqrt{36 + 9 + 1} = \sqrt{46}$.

## Exercises

1. When $\boldsymbol{a} = (1, -2)$ and $\boldsymbol{b} = (3, 1)$, find $3\boldsymbol{a} + 2\boldsymbol{b}$ and $|\boldsymbol{a} - \boldsymbol{b}|$.
2. Find the angle between $\boldsymbol{a} = (1, 1, 0)$ and $\boldsymbol{b} = (1, 0, 1)$.
3. Find $k$ so that $(1, k, 2)$ and $(3, 1, -1)$ are orthogonal.
4. Find the unit vectors orthogonal to both $\boldsymbol{a} = (1, 1, 1)$ and $\boldsymbol{b} = (1, 2, 3)$.

## Answers to the exercises

1. $3\boldsymbol{a} + 2\boldsymbol{b} = (3 + 6,\ -6 + 2) = (9, -4)$. Since $\boldsymbol{a} - \boldsymbol{b} = (-2, -3)$, $|\boldsymbol{a} - \boldsymbol{b}| = \sqrt{4 + 9} = \sqrt{13}$
2. $\boldsymbol{a} \cdot \boldsymbol{b} = 1$ and $|\boldsymbol{a}| = |\boldsymbol{b}| = \sqrt{2}$, so $\cos\theta = \dfrac{1}{2}$ and $\theta = \dfrac{\pi}{3}$ ($60°$)
3. From $3 + k - 2 = 0$, $k = -1$
4. The cross product is $\boldsymbol{a} \times \boldsymbol{b} = (1 \cdot 3 - 1 \cdot 2,\ 1 \cdot 1 - 1 \cdot 3,\ 1 \cdot 2 - 1 \cdot 1) = (1, -2, 1)$. Dividing by its magnitude $\sqrt{6}$ gives $\pm\dfrac{1}{\sqrt{6}}(1, -2, 1)$
