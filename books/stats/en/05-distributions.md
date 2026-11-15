# 5. Common distributions (normal, χ², t, F)

## Normal distribution

The density function of the **normal distribution** $N(\mu, \sigma^2)$ with mean $\mu$ and variance $\sigma^2$ looks like this.

$$f(x) = \frac{1}{\sqrt{2\pi}\,\sigma} \exp\!\left(-\frac{(x - \mu)^2}{2\sigma^2}\right)$$

![The standard normal distribution, and the share within ±1σ and ±2σ of the mean](images/en/normal.svg)

- A bell shape, symmetric around the mean
- About 68% falls within the mean ±1σ, about 95% within ±2σ (exactly ±1.96σ), and about 99.7% within ±3σ
- If you add normally distributed variables or multiply one by a constant, the result is still normal
- Standardizing with $Z = (X-\mu)/\sigma$ gives the standard normal distribution $N(0,1)$
- Measurement errors and averages of many things come close to a normal distribution (the central limit theorem in Chapter 6)

## χ² (chi-squared) distribution

This is the distribution of the sum of squares of independent $Z_1, \dots, Z_k$ that follow the standard normal distribution. $k$ is called the **degrees of freedom**.

$$W = Z_1^2 + Z_2^2 + \cdots + Z_k^2 \sim \chi^2(k)$$

![How the shape of the χ² distribution changes with the degrees of freedom](images/en/chi2.svg)

- It only takes values of 0 or more and has a long tail to the right. Its mean is $k$ and its variance is $2k$
- For the unbiased variance $s^2$ calculated from a sample from a normal distribution, $\dfrac{(n-1)s^2}{\sigma^2} \sim \chi^2(n-1)$
- Uses: tests of variance, goodness-of-fit tests, tests of independence in cross tables

## t distribution

This distribution is built from a standard normal $Z$ and an independent $W$ that follows $\chi^2(k)$.

$$T = \frac{Z}{\sqrt{W / k}} \sim t(k)$$

![The t distribution and the standard normal distribution (the fewer the degrees of freedom, the heavier the tails)](images/en/t.svg)

- Symmetric around 0, with heavier tails than the normal distribution. As the degrees of freedom grow, it approaches the standard normal distribution
- Used when you do not know the population variance and use the sample standard deviation $s$ instead

$$\frac{\bar{X} - \mu}{s / \sqrt{n}} \sim t(n-1)$$

- Uses: tests and confidence intervals for a mean, t values of regression coefficients (Chapter 8)

## F distribution

This is the distribution of the ratio of two independent χ² variables, each divided by its degrees of freedom.

$$F = \frac{W_1 / k_1}{W_2 / k_2} \sim F(k_1, k_2)$$

- It takes values of 0 or more and has a long tail to the right
- Uses: tests of the ratio of two variances, the F test in regression analysis that checks "whether none of the explanatory variables are useful", analysis of variance
- The square of a t variable follows an F distribution: $T^2 \sim F(1, k)$

## How the four distributions are related

| Distribution | How it is built | Common uses |
| --- | --- | --- |
| Normal $N(\mu,\sigma^2)$ | (the base) | Errors, distribution of a mean |
| $\chi^2(k)$ | Add $k$ squared standard normals | Variance, goodness of fit |
| $t(k)$ | Standard normal ÷ $\sqrt{\chi^2/k}$ | Means, regression coefficients |
| $F(k_1,k_2)$ | $(\chi^2/k_1) ÷ (\chi^2/k_2)$ | Ratio of variances, the regression as a whole |

## Getting values in Python

Use `ppf` (the inverse of the distribution function: the point below which a given percentage falls) and `cdf` (the distribution function) in `scipy.stats`.

```python
from scipy import stats

print(stats.norm.ppf(0.975))         # 1.959... (the two-sided 5% point)
print(stats.t.ppf(0.975, df=10))     # 2.228... (t with 10 degrees of freedom)
print(stats.chi2.ppf(0.95, df=5))    # 11.07...
print(stats.f.ppf(0.95, 2, 10))      # 4.102...
print(stats.norm.cdf(1) - stats.norm.cdf(-1))   # 0.682... (share within ±1σ)
```

## Summary

- For the normal distribution, 68% falls within ±1σ and 95% within ±1.96σ
- χ² is a sum of squared standard normals, t is a standard normal divided by a χ², and F is a ratio of two χ²
- The t distribution approaches the normal distribution when the degrees of freedom are large. When you use $s$, think in terms of the t distribution

## Exercises

```quiz
Q: About what percent of a normal distribution lies within ±1σ of the mean?
A: 68
E: Within ±1.96σ it is 95%.

Q: Within ± how many σ of the mean does 95% of a normal distribution lie?
A: 1.96
E: This number is used for confidence intervals.

Q: As the degrees of freedom grow, the t distribution approaches which distribution?
A: normal | normal distribution | standard normal
E: When you use $s$ instead of the population SD, think in terms of t.

Q: Which distribution does a sum of squared standard normal values follow?
A: chi-square | χ² | chi-squared | chi square
E: t is a standard normal divided by a χ²; F is a ratio of two χ².
```
