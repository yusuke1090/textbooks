# 6. Sample mean, the law of large numbers and the central limit theorem

## What you will learn

- Population and sample
- The expected value and variance of the sample mean (standard error)
- The law of large numbers and the central limit theorem
- Confidence intervals for a mean

## Population and sample

The whole group you want to know about is called the **population**, and the part you actually take out and examine is called the **sample**. We usually do not know the population mean $\mu$ or variance $\sigma^2$, so we estimate them from the sample.

| | Population | Sample |
| --- | --- | --- |
| Example | Milk yield of every dairy cow in Japan | Milk yield of the 100 cows you checked |
| Mean | Population mean $\mu$ (what you want to know) | Sample mean $\bar{X}$ (you can calculate it) |
| Variance | Population variance $\sigma^2$ | Unbiased variance $s^2$ |

## Properties of the sample mean

The sample mean $\bar{X} = \frac{1}{n}\sum X_i$ of $X_1, \dots, X_n$ drawn independently from the population is also a random variable whose value changes each time you draw. From the rules in Chapter 4, we know the following.

$$E[\bar{X}] = \mu \qquad V[\bar{X}] = \frac{\sigma^2}{n}$$

- Its expected value equals the population mean (it is **unbiased**). On average, it is right
- Its variance gets smaller in inverse proportion to $n$. If you have four times as much data, the spread (standard deviation) is halved
- The standard deviation of the sample mean, $\sigma/\sqrt{n}$, is called the **standard error**

## Law of large numbers

As the sample size $n$ grows, the sample mean gets as close as you like to the population mean.

$$\bar{X} \to \mu \quad (n \to \infty)$$

If you roll a die many times and take the average, it gets closer and closer to 3.5. It is a guarantee that if you examine enough, the mean will be right.

## Central limit theorem

Whatever the shape of the original distribution (as long as its variance is finite), the distribution of the sample mean approaches a normal distribution when $n$ is large.

$$\frac{\bar{X} - \mu}{\sigma / \sqrt{n}} \;\to\; N(0, 1) \quad (n \to \infty)$$

![Even for a distribution with a long tail to the right, the distribution of the mean approaches a normal distribution as you average more values](images/en/clt.svg)

- Even if the original distribution is skewed, with $n$ of about 30 you can often treat the mean as almost normally distributed
- That is why you can make inferences about a mean using the normal distribution (Chapter 5)

## Confidence interval for a mean

From the central limit theorem, the sample mean falls within $\mu \pm 1.96\,\sigma/\sqrt{n}$ with 95% probability. Turning this around gives the **95% confidence interval** for the population mean.

$$\bar{x} \pm 1.96 \times \frac{\sigma}{\sqrt{n}}$$

When you do not know $\sigma$, use the sample's $s$, and use the t distribution value $t_{0.975}(n-1)$ instead of 1.96 (Chapter 5).

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(0)
x = rng.exponential(scale=2.0, size=50)        # a distribution with a long right tail (population mean is 2)
mean, s, n = x.mean(), x.std(ddof=1), len(x)
t = stats.t.ppf(0.975, df=n - 1)
print(f"mean {mean:.2f}, 95% confidence interval {mean - t*s/np.sqrt(n):.2f} to {mean + t*s/np.sqrt(n):.2f}")
```

## Summary

- The sample mean is an unbiased estimate of the population mean. Its spread (standard error) is $\sigma/\sqrt{n}$
- Law of large numbers: if you examine enough, the sample mean approaches the population mean
- Central limit theorem: whatever the original distribution, the sample mean is almost normally distributed
- The 95% confidence interval is $\bar{x} \pm 1.96\,\sigma/\sqrt{n}$ (if you do not know $\sigma$, use $s$ and the t distribution)
