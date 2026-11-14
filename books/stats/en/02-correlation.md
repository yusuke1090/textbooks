# 2. The relationship between two variables (covariance and correlation)

## What you will learn

- Co-variation and covariance
- The correlation coefficient and how to read it
- Things to watch out for when looking at correlation

## Co-variation and covariance

To measure whether two kinds of data $(x_i, y_i)$ go up and down together, multiply their deviations.

$$S_{xy} = \sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})$$

This is called the **co-variation**, and dividing it by the number of values gives the **covariance**.

$$s_{xy} = \frac{1}{n}\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})$$

| Where the point is | Deviation of $x$ | Deviation of $y$ | Product |
| --- | --- | --- | --- |
| Upper right (both above the mean) | + | + | + |
| Lower left (both below the mean) | − | − | + |
| Lower right, upper left | Different signs | | − |

- If most points are upper right and lower left (they rise together), the covariance is **positive**
- If most points are lower right and upper left (when one rises, the other falls), it is **negative**
- If there is no relationship, it is close to 0

## Correlation coefficient

The covariance depends on the units (cm × kg, for example), so you cannot compare its size. Dividing it by both standard deviations gives the **correlation coefficient**.

$$r = \frac{s_{xy}}{s_x\, s_y} = \frac{S_{xy}}{\sqrt{S_{xx}\,S_{yy}}}$$

- It always lies in $-1 \le r \le 1$, so you can compare it regardless of units
- $r = 1$ is a straight line going up to the right, and $r=-1$ is a straight line going down to the right
- As a rough guide, people often read $|r|$ of 0.7 or more as strong, 0.4–0.7 as moderate, and 0.2 or less as almost no relationship

### Worked example

| $x$ | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- |
| $y$ | 2 | 4 | 5 | 4 | 5 |

- $\bar{x} = 3$, $\bar{y} = 4$
- $S_{xy} = (-2)(-2) + (-1)(0) + 0 \cdot 1 + 1 \cdot 0 + 2 \cdot 1 = 6$
- $S_{xx} = 10$, $S_{yy} = 6$
- $r = 6 / \sqrt{10 \times 6} \approx 0.77$ (a strong positive correlation)

We will use the same data for regression analysis in Chapter 7.

```python
import numpy as np
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 5, 4, 5])
print(np.cov(x, y, ddof=0)[0, 1])   # 1.2 (covariance, divided by n)
print(np.corrcoef(x, y)[0, 1])      # 0.7745...
```

## Things to watch out for

- **It only measures straight-line relationships**: even with a U-shaped relationship, $r$ can be close to 0. Always look at a scatter plot too
- **It is sensitive to outliers**: one point far away from the others can change $r$ a lot
- **Correlation is not causation**: temperature and ice cream sales are correlated, and so are temperature and drowning accidents. Ice cream and drowning are also correlated, but the cause is the temperature (a **spurious correlation**)
- If explanatory variables are too highly correlated with each other, regression analysis does not work well (multicollinearity, Chapter 8)

## Summary

- Multiply the deviations and add them to get the co-variation; per value, it is the covariance. Its sign tells you whether the two rise or fall together
- The correlation coefficient is the covariance divided by the standard deviations. It lies between −1 and 1 and can be compared regardless of units
- It only measures straight-line relationships. Look at a scatter plot, watch out for outliers, and keep it separate from causation
