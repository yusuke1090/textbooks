# 8. Pitfalls of OLS (multicollinearity and omitted variable bias)

## What you will learn

- How the population regression relates to OLS on a sample
- The assumptions OLS needs to work well, and the t values of coefficients
- Multicollinearity
- Omitted variable bias

## Thinking about OLS in the population and the sample

We assume that in the population there is a true relationship $y = \beta_0 + \beta_1 x + u$ (the **population regression**). The $\hat\beta_0, \hat\beta_1$ you calculate by OLS from your sample are estimates of it. If you take a new sample, $\hat\beta_1$ also changes, so $\hat\beta_1$ is a random variable too.

For $\hat\beta_1$ to hit the true $\beta_1$ on average (to be **unbiased**), you need the following assumptions.

| Assumption | Meaning |
| --- | --- |
| Linear | The relationship in the population has the form $\beta_0 + \beta_1 x + u$ |
| Random sampling | The sample is chosen at random from the population |
| $x$ varies | If every $x$ is the same, the slope cannot be determined |
| **$E[u \mid x] = 0$** | The error term (factors other than $x$) is unrelated to $x$. This is the most important one, and the easiest to break |

If, in addition, the variance of the error is the same whatever $x$ is (**homoskedasticity**), OLS has the smallest spread of all unbiased estimators (the Gauss–Markov theorem).

### Standard error and t value of a coefficient

$$V[\hat\beta_1] = \frac{\sigma^2}{\sum (x_i - \bar{x})^2}$$

- The more $x$ varies and the more data you have, the more precisely the slope can be estimated
- Estimating $\sigma^2$ from the residuals and taking the square root gives the **standard error** $\mathrm{se}(\hat\beta_1)$
- **t value** $= \hat\beta_1 / \mathrm{se}(\hat\beta_1)$. If its absolute value is larger than roughly 2, it is hard to say "$\beta_1 = 0$ (there is no effect)" (the t distribution in Chapter 5)

## Multicollinearity

In multiple regression, when explanatory variables are very highly correlated with each other, this is called **multicollinearity**.

- Examples: including both a cow's "weight" and "height", or both the "maximum" and "average" temperature
- The standard errors of the coefficients become large, and their values and signs change a lot from one dataset to another (you cannot tell which variable the effect belongs to)
- The quality of the predictions ($R^2$) does not get much worse, so it is easy to miss
- If there is an exact straight-line relationship (for example "the total" and "all of its parts", or including a dummy variable for every category), it cannot be calculated at all

| How to check | What it is |
| --- | --- |
| Correlation matrix | Look at the correlation coefficients between the explanatory variables (Chapter 2) |
| VIF | $\mathrm{VIF}_j = 1 / (1 - R_j^2)$, where $R_j^2$ is the coefficient of determination when you regress $x_j$ on the other explanatory variables. Be careful if it is over 10 |

What to do: merge similar variables into one or combine them (principal components, for example), use regularization (Ridge; see the Machine Learning Textbook), or get more data.

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor
# X is the matrix (DataFrame) of explanatory variables, including the intercept column
vif = [variance_inflation_factor(X.values, j) for j in range(X.shape[1])]
```

## Omitted variable bias

If you forget to include a variable that really affects $y$, the coefficients of the variables you kept are shifted. This is called **omitted variable bias** (OVB).

If the true model is $y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + u$ but you regress $y$ on $x_1$ alone without $x_2$, the slope $\tilde\beta_1$ is shifted like this.

$$E[\tilde\beta_1] = \beta_1 + \beta_2\,\delta_1$$

$\delta_1$ is the slope when you regress $x_2$ on $x_1$ (the relationship between $x_1$ and $x_2$).

| | $x_1$ and $x_2$ positively correlated | Negatively correlated |
| --- | --- | --- |
| $\beta_2 > 0$ | Shifted up (overestimated) | Shifted down (underestimated) |
| $\beta_2 < 0$ | Shifted down | Shifted up |

- Example: if you regress wages on years of education without including "ability", the effect of education comes out too large, because ability is positively related to both education and wages
- Example: if you regress a cow's milk yield on "amount of feed" without including "body size", the effect of feed comes out too large, because big cows eat more and also give more milk
- If the omitted variable is unrelated to $x_1$ ($\delta_1 = 0$) or does not affect $y$ ($\beta_2 = 0$), there is no shift
- When a variable is omitted, the assumption $E[u \mid x] = 0$ is broken (the omitted variable goes into the error term and is related to $x$)

What to do: include that variable, include a close substitute (a proxy variable), remove differences between individuals using data that measures the same individuals many times (panel data), or use instrumental variables.

## Summary

- OLS on a sample estimates the population regression. It is unbiased if $E[u\mid x]=0$ holds
- t value $= \hat\beta/\mathrm{se}$. How much $x$ varies and how much data you have decide how precise the estimate is
- Multicollinearity: when explanatory variables are highly correlated, the coefficients are unstable. Check with a correlation matrix and VIF
- Omitted variable bias: if you leave out a variable that matters, the shift is $\beta_2\delta_1$. You can judge its direction from the table
