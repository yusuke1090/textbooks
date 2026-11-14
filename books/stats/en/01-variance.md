# 1. How spread out data is (variance and standard deviation)

## What you will learn

- The mean and deviations
- Total variation (sum of squared deviations), variance and standard deviation
- The difference between variance divided by $n$ and unbiased variance divided by $n-1$

This textbook is based on my study notes ([超基礎統計 (Very basic statistics)](https://note.com/k_1090/n/n920f21843b93) and [計量経済学の自分用まとめ (My econometrics summary)](https://note.com/k_1090/n/n98bcfaa3190b)), with explanations of the formulas and worked examples added. For how to write Python, see the "Python Textbook".

## Mean and deviation

The **mean** (sample mean) of $n$ data values $x_1, x_2, \dots, x_n$ is the sum of all the values divided by $n$.

$$\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i$$

How far each value is from the mean is called its **deviation**: $x_i - \bar{x}$.
The deviations always add up to 0, so to measure the spread we square the deviations first and then add them.

## Total variation and variance

The sum of the squared deviations is called the **total variation** (sum of squared deviations).

$$S_{xx} = \sum_{i=1}^{n} (x_i - \bar{x})^2$$

The total variation grows as you have more data, so we divide it by the number of values. This is the **variance**.

$$s^2 = \frac{1}{n}\sum_{i=1}^{n} (x_i - \bar{x})^2 = \frac{S_{xx}}{n}$$

The unit of the variance is squared (cm becomes cm²), so we take the square root to get back to the original unit. This is the **standard deviation**: $s = \sqrt{s^2}$.

### Worked example

Let's calculate with the data 2, 4, 4, 4, 5, 5, 7, 9 ($n=8$).

| $x_i$ | 2 | 4 | 4 | 4 | 5 | 5 | 7 | 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Deviation $x_i-\bar{x}$ | −3 | −1 | −1 | −1 | 0 | 0 | 2 | 4 |
| Squared deviation | 9 | 1 | 1 | 1 | 0 | 0 | 4 | 16 |

- Mean $\bar{x} = 40/8 = 5$
- Total variation $S_{xx} = 32$
- Variance $s^2 = 32/8 = 4$, standard deviation $s = 2$

You can also calculate the variance as "mean of the squares − square of the mean": $s^2 = \overline{x^2} - \bar{x}^2 = 29 - 25 = 4$.

## Unbiased variance (dividing by n − 1)

When you use the data you have (a **sample**) to estimate the variance of a larger group (the **population**), divide by $n-1$ instead of $n$. This is called the **unbiased variance**.

$$s^2_{\text{unbiased}} = \frac{1}{n-1}\sum_{i=1}^{n} (x_i - \bar{x})^2$$

- The deviations are measured from the sample mean $\bar{x}$, not from the population mean, so dividing by $n$ gives a value a little smaller than the population variance. Dividing by $n-1$ corrects this
- $n-1$ is called the **degrees of freedom** (there is one constraint — the deviations add up to 0 — so only $n-1$ of them can move freely)
- In the example above, it is $32/7 \approx 4.57$

> Different software divides by different numbers. NumPy's `np.var(x)` divides by $n$, and pandas' `df.var()` divides by $n-1$.

```python
import numpy as np
import pandas as pd

x = np.array([2, 4, 4, 4, 5, 5, 7, 9])
print(x.mean())            # 5.0
print(np.var(x))           # 4.0 (divided by n)
print(np.var(x, ddof=1))   # 4.571... (divided by n-1)
print(np.std(x))           # 2.0
print(pd.Series(x).var())  # 4.571... (pandas uses n-1 by default)
```

## Summary

- Square the deviations $x_i-\bar{x}$ and add them to get the total variation; divide by the number of values to get the variance
- The standard deviation is the square root of the variance, in the same unit as the data
- To estimate the population variance, divide by $n-1$ (unbiased variance). Check which one your software uses by default
