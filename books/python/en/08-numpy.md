# 8. NumPy (arrays of numbers)

## What you will learn

- How to make NumPy arrays (ndarray), and their shape and type
- Calculating without for (vectorization) and broadcasting
- Aggregation and axis, and ways to take out values (slices and conditions)
- Matrix calculations and random numbers

NumPy is a library for calculating arrays of numbers all at once, fast. pandas, matplotlib and scikit-learn also use NumPy inside.

```python
import numpy as np
```

## Making arrays

```python
a = np.array([32.5, 28.0, 35.2, 25.8])          # from a list
m = np.array([[1, 2, 3], [4, 5, 6]])             # 2-dimensional (2 rows, 3 columns)

print(a.shape, m.shape)      # (4,) (2, 3)  shape
print(m.ndim, m.size)        # 2 6          number of dimensions, number of elements
print(a.dtype, m.dtype)      # float64 int64  type (all elements have the same type)
```

| Function | What it makes | Example |
| --- | --- | --- |
| `np.zeros(shape)` / `np.ones(shape)` | All 0s / all 1s | `np.zeros((2, 3))` |
| `np.arange(start, stop, step)` | Evenly spaced (the stop is not included) | `np.arange(0, 10, 2)` → `[0 2 4 6 8]` |
| `np.linspace(start, stop, count)` | Evenly spaced with a set count (the stop is included) | `np.linspace(0, 1, 5)` → `[0. 0.25 0.5 0.75 1.]` |
| `np.full(shape, value)` | All the same value | `np.full(3, 7)` |

## Calculating all at once

With NumPy arrays, you can calculate on all the elements at once without writing `for` (**vectorization**). It runs much faster than looping over a list with `for`.

```python
a = np.array([32.5, 28.0, 35.2, 25.8])
print(a * 2.2046)            # all of them in pounds
print(a - a.mean())          # difference from the mean
print(np.sqrt(a))            # square root of each
print(a >= 30)               # [ True False  True False]
```

> `*` means something different for lists. `[1, 2] * 2` is `[1, 2, 1, 2]` (repetition), while `np.array([1, 2]) * 2` is `[2 4]`.

### Broadcasting

Even with arrays of different shapes, NumPy stretches them along the missing direction and calculates.

```python
milk = np.array([[30, 32, 31],      # per cow (rows) × per day (columns)
                 [25, 27, 26]])
bonus = np.array([1, 0, 2])         # a correction for each day (3 columns)
print(milk + bonus)                 # [1, 0, 2] is added to each row
```

## Aggregation and axis

```python
milk = np.array([[30, 32, 31],
                 [25, 27, 26]])
print(milk.sum(), milk.mean(), milk.max())     # overall: 171 28.5 32
print(milk.mean(axis=0))                       # collapse vertically (per day): [27.5 29.5 28.5]
print(milk.mean(axis=1))                       # collapse horizontally (per cow): [31. 26.]
print(milk.argmax(axis=1))                     # for each cow, the index of the highest day: [1 1]
```

`axis=0` means "collapse along the rows (a result for each column)", and `axis=1` means "collapse along the columns (a result for each row)". The same goes for `std` (standard deviation), `min`, `argmin` and others.

## Taking out values

```python
m = np.array([[1, 2, 3],
              [4, 5, 6]])
print(m[1, 2])        # 6 (row 1, column 2; counting from 0)
print(m[0])           # [1 2 3] (row 0)
print(m[:, 1])        # [2 5] (column 1 of every row)
print(m[:, 1:])       # from column 1 onward

a = np.array([32.5, 28.0, 35.2, 25.8])
print(a[a >= 30])                    # only those that meet the condition: [32.5 35.2]
print(np.where(a >= 30, "high", "low")) # choose values by a condition
```

> What you take out with a slice (`m[:, 1:]`) shares its contents with the original array. Changing it also changes the original, so add `.copy()` when you want a separate one.

## Changing shape and matrix calculations

```python
x = np.arange(6)            # [0 1 2 3 4 5]
y = x.reshape(2, 3)         # into 2 rows and 3 columns
print(y.T)                  # transpose (3 rows, 2 columns)
print(y @ y.T)              # matrix product (@)
```

`*` multiplies element by element, and `@` is the matrix product.

## Random numbers

```python
rng = np.random.default_rng(0)            # 0 is the seed (the same seed gives the same numbers every time)
print(rng.normal(30, 3, size=5))          # 5 values from a normal distribution with mean 30, SD 3
print(rng.integers(1, 7, size=10))        # integers 1–6 (a die)
print(rng.choice(["A", "B", "C"], size=3))
```

Distributions such as the normal distribution are explained in Chapter 5 of the "Statistics Textbook".

## Summary

- Make arrays with `np.array`. Look at `shape` and `dtype`
- Calculate all at once without `for`, as in `a * 2` and `a - a.mean()`
- In aggregation, `axis=0` gives a result per column and `axis=1` per row
- Take out values with `m[row, column]` and `a[a >= 30]`. `@` is the matrix product
- Random numbers come from `np.random.default_rng(seed)`
