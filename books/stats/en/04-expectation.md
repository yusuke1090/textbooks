# 4. Expected value and variance

## What you will learn

- Expected value and the rules for calculating it
- Variance and standard deviation (for random variables)
- Standardization, skewness and kurtosis
- Covariance, correlation coefficient and conditional expectation

Chapters 1 and 2 were calculations on the data you have. In this chapter, we think about the same things for random variables (distributions).

## Expected value

The "mean" of a random variable is called its **expected value**, written $E[X]$ or $\mu$.

$$E[X] = \sum_x x\,P(X = x) \qquad E[X] = \int x\,f(x)\,dx$$

For a die, $E[X] = (1+2+3+4+5+6) \times \frac{1}{6} = 3.5$.

| Rule | Meaning |
| --- | --- |
| $E[aX + b] = aE[X] + b$ | If you multiply and add, the expected value changes in the same way |
| $E[X + Y] = E[X] + E[Y]$ | A sum can always be split |
| $E[XY] = E[X]\,E[Y]$ | Only when $X$ and $Y$ are independent |

## Variance and standard deviation

The expected value of the squared distance from the expected value is the **variance**.

$$V[X] = E\big[(X - \mu)^2\big] = E[X^2] - (E[X])^2$$

For a die, $E[X^2] = 91/6$, so $V[X] = 91/6 - 3.5^2 = 35/12 \approx 2.92$, and the standard deviation is $\sqrt{35/12} \approx 1.71$.

| Rule | Meaning |
| --- | --- |
| $V[aX + b] = a^2 V[X]$ | An added constant does not affect the variance. Multiplying has a squared effect |
| $V[X + Y] = V[X] + V[Y] + 2\,\mathrm{Cov}(X, Y)$ | If they are independent, the covariance is 0, so the variances simply add |

## Standardization, skewness and kurtosis

Subtracting the mean and dividing by the standard deviation is called **standardization**. The standardized $Z$ has mean 0 and variance 1, so you can compare things measured in different units. (The Japanese *hensachi* score is the standardized value multiplied by 10, plus 50.)

$$Z = \frac{X - \mu}{\sigma}$$

| Measure | Formula | What it tells you |
| --- | --- | --- |
| Skewness | $E[Z^3]$ | Lopsidedness. Positive when there is a long tail to the right (such as income) |
| Kurtosis | $E[Z^4]$ | How heavy the tails are / how peaked it is. 3 for the normal distribution |

> Kurtosis is often shown with 3 subtracted so that the normal distribution is 0 (excess kurtosis). `scipy.stats.kurtosis` returns the value with 3 subtracted by default.

## Covariance and correlation coefficient

$$\mathrm{Cov}(X, Y) = E\big[(X - \mu_X)(Y - \mu_Y)\big] = E[XY] - E[X]\,E[Y]$$

$$\rho = \frac{\mathrm{Cov}(X, Y)}{\sigma_X\,\sigma_Y}$$

- If they are independent, $\mathrm{Cov}(X, Y) = 0$. But a covariance of 0 does not always mean independence (there may be a relationship that is not a straight line)
- The correlation coefficient $\rho$ is between −1 and 1. The $r$ in Chapter 2 is this, calculated from data

## Conditional expectation

The expected value of a conditional distribution (Chapter 3) is called the **conditional expectation**.

$$E[Y \mid X = x] = \sum_y y\,P(Y = y \mid X = x)$$

- The mean of $Y$ for each $x$, like "the average weight of people who are 170 cm tall"
- As you change $x$, $E[Y \mid X = x]$ becomes a function of $x$. Expressing it as a straight line is regression analysis (Chapter 7)
- **Law of iterated expectations**: $E\big[E[Y \mid X]\big] = E[Y]$ (if you average the mean for each $x$, weighted by how likely each $x$ is, you get the overall mean)

## Symbols for population and sample

| | Population (distribution) | Sample (calculated from data) |
| --- | --- | --- |
| Mean | $\mu = E[X]$ | $\bar{x}$ |
| Variance | $\sigma^2 = V[X]$ | $s^2$ |
| Covariance | $\mathrm{Cov}(X, Y)$ | $s_{xy}$ |
| Correlation coefficient | $\rho$ | $r$ |

## Summary

- The expected value is a mean weighted by probability. A sum can always be split
- The variance is $E[X^2]-(E[X])^2$. Multiplying by a constant has a squared effect, and for independent variables the variance of a sum is the sum of the variances
- Standardizing gives mean 0 and variance 1. Skewness is lopsidedness, kurtosis is how heavy the tails are
- Seeing the conditional expectation $E[Y\mid X=x]$ as a function of $x$ leads to the idea of regression

## Exercises

```quiz
Q: What is the expected value of one roll of a die?
A: 3.5
E: (1 + 2 + 3 + 4 + 5 + 6) ÷ 6 = 3.5.

Q: If $E[X]=2$ and $E[X^2]=7$, what is $V[X]$?
A: 3
E: $V[X] = E[X^2] - (E[X])^2 = 7 - 4 = 3$.

Q: If $V[X]=4$, what is $V[3X]$?
A: 36
E: A constant factor is squared: $9 \times 4 = 36$.

Q: $X$ and $Y$ are independent, with $V[X]=2$ and $V[Y]=3$. What is $V[X+Y]$?
A: 5
E: For independent variables, the variance of the sum is the sum of the variances.

Q: What is the variance of a standardized random variable?
A: 1
E: Standardizing gives mean 0 and variance 1.
```
