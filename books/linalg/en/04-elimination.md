# 4. Systems of linear equations and elimination

## What you will learn in this chapter

- The augmented matrix and elementary row operations
- Solving systems of equations by elimination (Gaussian elimination)
- Rank and the number of solutions (one, infinitely many, none)
- Homogeneous systems
- Finding the inverse by elimination

## Elementary row operations

When solving a system of equations, you may do the following three operations.

1. Multiply an equation by some number (not 0)
2. Add a multiple of another equation to an equation
3. Swap two equations

Doing these on the **rows** of the **augmented matrix** $(A \mid \boldsymbol{b})$, which lists only the coefficients and the right-hand sides, is called **elementary row operations**. The goal is to reach **row echelon form**, with everything in the lower left made 0.

## When there is exactly one solution

### Example 4-1

Solve the following system by elimination.

$$\begin{cases} x + y + z = 6 \\ 2x + 3y + z = 11 \\ x - y + 2z = 5 \end{cases}$$

**Solution** Make the augmented matrix, and use the 1 in the first column (the **pivot**) to make the entries below it 0.

$$\left(\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 2 & 3 & 1 & 11 \\ 1 & -1 & 2 & 5 \end{array}\right) \xrightarrow[\text{③} - \text{①}]{\text{②} - 2 \times \text{①}} \left(\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 0 & 1 & -1 & -1 \\ 0 & -2 & 1 & -1 \end{array}\right)$$

Next, use the 1 in row 2 as the pivot and make the entry below it 0.

$$\xrightarrow{\text{③} + 2 \times \text{②}} \left(\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 0 & 1 & -1 & -1 \\ 0 & 0 & -1 & -3 \end{array}\right)$$

This is now in row echelon form. Solve from the bottom row up (back substitution).

- Row 3: from $-z = -3$, $z = 3$
- Row 2: from $y - z = -1$, $y = 2$
- Row 1: from $x + y + z = 6$, $x = 1$

$(x, y, z) = (1, 2, 3)$.

> **Key point**: If you keep eliminating until the upper rows are 0 too, the left side becomes the identity matrix $E$ and the answers line up in the right column (**reduced row echelon form**). When solving by hand, either way is fine.

$$\left(\begin{array}{ccc|c} 1 & 0 & 0 & 1 \\ 0 & 1 & 0 & 2 \\ 0 & 0 & 1 & 3 \end{array}\right)$$

## Rank

When a matrix is put in row echelon form by elementary row operations, the **number of nonzero rows** is called the **rank** of the matrix and is written $\text{rank}\,A$. The rank is the same no matter how you do the row operations.

Using the rank, you can tell what the solutions of a system $A\boldsymbol{x} = \boldsymbol{b}$ ($n$ unknowns) look like.

| Condition | Solutions |
| --- | --- |
| $\text{rank}\,A = \text{rank}(A \mid \boldsymbol{b}) = n$ | Exactly one |
| $\text{rank}\,A = \text{rank}(A \mid \boldsymbol{b}) < n$ | Infinitely many (written with $n - \text{rank}\,A$ free parameters) |
| $\text{rank}\,A < \text{rank}(A \mid \boldsymbol{b})$ | None (a contradiction like "$0 = 1$" appears) |

## When there are infinitely many solutions

### Example 4-2

$$\begin{cases} x + 2y - z = 3 \\ 2x + 4y + z = 9 \\ x + 2y + 2z = 6 \end{cases}$$

**Solution**

$$\left(\begin{array}{ccc|c} 1 & 2 & -1 & 3 \\ 2 & 4 & 1 & 9 \\ 1 & 2 & 2 & 6 \end{array}\right) \xrightarrow[\text{③} - \text{①}]{\text{②} - 2 \times \text{①}} \left(\begin{array}{ccc|c} 1 & 2 & -1 & 3 \\ 0 & 0 & 3 & 3 \\ 0 & 0 & 3 & 3 \end{array}\right) \xrightarrow{\text{③} - \text{②}} \left(\begin{array}{ccc|c} 1 & 2 & -1 & 3 \\ 0 & 0 & 3 & 3 \\ 0 & 0 & 0 & 0 \end{array}\right)$$

$\text{rank}\,A = \text{rank}(A \mid \boldsymbol{b}) = 2 < 3$, so there are infinitely many solutions with $3 - 2 = 1$ free parameter.

- Row 2: from $3z = 3$, $z = 1$
- Row 1: from $x + 2y - z = 3$, $x = 4 - 2y$

Setting $y = t$ ($t$ any real number),

$$\begin{pmatrix} x \\ y \\ z \end{pmatrix} = \begin{pmatrix} 4 - 2t \\ t \\ 1 \end{pmatrix} = \begin{pmatrix} 4 \\ 0 \\ 1 \end{pmatrix} + t\begin{pmatrix} -2 \\ 1 \\ 0 \end{pmatrix}$$

The solutions form a **line** in space.

## When there is no solution

### Example 4-3

What happens if the right-hand side of the third equation in Example 4-2 is changed to 7?

**Solution** With the same operations, the end result is

$$\left(\begin{array}{ccc|c} 1 & 2 & -1 & 3 \\ 0 & 0 & 3 & 3 \\ 0 & 0 & 0 & 1 \end{array}\right)$$

Row 3 says "$0x + 0y + 0z = 1$", and no $x, y, z$ satisfy it. Since $\text{rank}\,A = 2 < \text{rank}(A \mid \boldsymbol{b}) = 3$, there is **no solution**.

## Homogeneous systems

A system $A\boldsymbol{x} = \boldsymbol{0}$ whose right-hand sides are all 0 is called a **homogeneous system**.

- $\boldsymbol{x} = \boldsymbol{0}$ is always a solution (the **trivial solution**)
- There are solutions other than $\boldsymbol{0}$ (**nontrivial solutions**) only when $\text{rank}\,A < n$
- For a square matrix, "there is a nontrivial solution $\iff$ $\det A = 0$" (Chapter 5). This fact is the basis of the equation for finding **eigenvalues** in Chapter 8

## Finding the inverse by elimination

Put the identity matrix $E$ to the right of an $n \times n$ square matrix $A$, and do row operations until the left side becomes $E$; the right side then becomes $A^{-1}$.

$$(A \mid E) \longrightarrow (E \mid A^{-1})$$

If a row of all 0s appears on the left along the way, $A$ has no inverse ($\text{rank}\,A < n$).

### Example 4-4

Find the inverse of $A = \begin{pmatrix} 1 & 2 & 1 \\ 2 & 5 & 2 \\ 1 & 2 & 2 \end{pmatrix}$.

**Solution**

$$\left(\begin{array}{ccc|ccc} 1 & 2 & 1 & 1 & 0 & 0 \\ 2 & 5 & 2 & 0 & 1 & 0 \\ 1 & 2 & 2 & 0 & 0 & 1 \end{array}\right) \xrightarrow[\text{③} - \text{①}]{\text{②} - 2 \times \text{①}} \left(\begin{array}{ccc|ccc} 1 & 2 & 1 & 1 & 0 & 0 \\ 0 & 1 & 0 & -2 & 1 & 0 \\ 0 & 0 & 1 & -1 & 0 & 1 \end{array}\right)$$

The lower left is now 0. Next, make the upper right 0.

$$\xrightarrow{\text{①} - 2 \times \text{②} - \text{③}} \left(\begin{array}{ccc|ccc} 1 & 0 & 0 & 6 & -2 & -1 \\ 0 & 1 & 0 & -2 & 1 & 0 \\ 0 & 0 & 1 & -1 & 0 & 1 \end{array}\right)$$

$$A^{-1} = \begin{pmatrix} 6 & -2 & -1 \\ -2 & 1 & 0 \\ -1 & 0 & 1 \end{pmatrix}$$

Check: the dot product of row 1 of $A$ and column 1 of $A^{-1}$ is $6 - 4 - 1 = 1$, with column 2 it is $-2 + 2 + 0 = 0$, and so on, giving $AA^{-1} = E$.

## Summary: equivalent statements for a square matrix $A$

For an $n \times n$ square matrix $A$, the following all say the same thing (more equivalent statements are added in Chapters 5 and 6).

- $A$ has an inverse
- $\text{rank}\,A = n$
- $A\boldsymbol{x} = \boldsymbol{b}$ has exactly one solution for every $\boldsymbol{b}$
- The only solution of $A\boldsymbol{x} = \boldsymbol{0}$ is $\boldsymbol{x} = \boldsymbol{0}$
- $\det A \ne 0$ (Chapter 5)

## Exercises

1. Solve by elimination: $\begin{cases} x + 2y = 5 \\ 3x - y = 1 \end{cases}$
2. Find the rank of the following matrix: $\begin{pmatrix} 1 & 2 & 3 \\ 2 & 4 & 6 \\ 1 & 1 & 1 \end{pmatrix}$
3. Find $a$ so that the following system has solutions, and find the solutions in that case: $\begin{cases} x + y = 1 \\ 2x + 2y = a \end{cases}$

## Answers to the exercises

1. $\left(\begin{array}{cc|c} 1 & 2 & 5 \\ 3 & -1 & 1 \end{array}\right) \to \left(\begin{array}{cc|c} 1 & 2 & 5 \\ 0 & -7 & -14 \end{array}\right)$, so $y = 2$ and $x = 1$
2. Row 2 − 2 × row 1 is all 0, and row 3 − row 1 is $(0, -1, -2)$. There are two nonzero rows, so the rank is **2**
3. Row 2 − 2 × row 1 gives $(0, 0 \mid a - 2)$. There are solutions when $a = 2$. Then $x = 1 - t$, $y = t$ ($t$ arbitrary)
