# 7. Regression analysis and OLS

## What you will learn

- The regression model and the error term
- The ordinary least squares (OLS) estimator
- Properties of the residuals
- The coefficient of determination $R^2$
- Multiple regression and calculating it in Python

## Regression model

A straight-line model that explains $y$ by $x$ is called a **simple regression model**.

$$y_i = \beta_0 + \beta_1 x_i + u_i$$

- $y$ is called the **dependent variable** (target variable), and $x$ the **explanatory variable**
- $\beta_0$ (intercept) and $\beta_1$ (slope) are what we want to know. $\beta_1$ means "when $x$ goes up by 1, how much $y$ goes up on average"
- $u_i$ is called the **error term**. It collects everything other than $x$ that moves $y$

## Ordinary least squares (OLS)

We choose the line that fits the data best, $\hat{y} = \hat\beta_0 + \hat\beta_1 x$, so that the sum of the squared **residuals** $\hat{u}_i = y_i - \hat{y}_i$ is as small as possible. This is called **ordinary least squares** (OLS).

$$\min_{\beta_0,\,\beta_1} \sum_{i=1}^{n} \left(y_i - \beta_0 - \beta_1 x_i\right)^2$$

![The data (points) and the OLS line. The vertical lines are the residuals, and OLS makes the sum of their squares as small as possible](images/en/ols.svg)

Solving this minimization gives the **OLS estimators**.

$$\hat\beta_1 = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2} = \frac{S_{xy}}{S_{xx}} \qquad \hat\beta_0 = \bar{y} - \hat\beta_1 \bar{x}$$

- The slope is "co-variation ÷ total variation of $x$". Using the correlation coefficient, $\hat\beta_1 = r \cdot s_y / s_x$
- With the data from Chapter 2 ($S_{xy} = 6$, $S_{xx} = 10$, $\bar{x} = 3$, $\bar{y} = 4$), $\hat\beta_1 = 0.6$ and $\hat\beta_0 = 4 - 0.6 \times 3 = 2.2$. The line is $\hat{y} = 2.2 + 0.6x$

## Properties of the residuals

A line found by OLS always has the following properties (they come from the conditions of the minimization).

| Property | Formula |
| --- | --- |
| The residuals add up to 0 | $\sum \hat{u}_i = 0$ |
| The residuals are uncorrelated with the explanatory variable | $\sum x_i \hat{u}_i = 0$ |
| The residuals are uncorrelated with the predicted values | $\sum \hat{y}_i \hat{u}_i = 0$ |
| The line passes through the point of means | $\bar{y} = \hat\beta_0 + \hat\beta_1 \bar{x}$ |

## Coefficient of determination

The total variation of $y$ can be split into the part explained by the line and the part left in the residuals.

$$\underbrace{\sum (y_i - \bar{y})^2}_{\text{TSS (total variation)}} = \underbrace{\sum (\hat{y}_i - \bar{y})^2}_{\text{ESS (explained variation)}} + \underbrace{\sum \hat{u}_i^2}_{\text{RSS (residual variation)}}$$

The share that is explained is the **coefficient of determination**.

$$R^2 = \frac{\text{ESS}}{\text{TSS}} = 1 - \frac{\text{RSS}}{\text{TSS}}$$

- It is between 0 and 1, and the closer to 1, the better the line fits
- In simple regression, it equals the square of the correlation coefficient ($R^2 = r^2$). For the Chapter 2 data, TSS = 6 and ESS = $0.6^2 \times 10 = 3.6$, so $R^2 = 0.6$
- A high $R^2$ is a different thing from a causal relationship (Chapter 8)

## Multiple regression

A model with two or more explanatory variables is called a **multiple regression model**.

$$y_i = \beta_0 + \beta_1 x_{1i} + \beta_2 x_{2i} + \cdots + \beta_k x_{ki} + u_i$$

- $\beta_1$ is "the effect of $x_1$ when the other explanatory variables are held fixed"
- In matrix form, the estimator is $\hat\beta = (X^\top X)^{-1} X^\top y$
- Adding explanatory variables always raises $R^2$, so also look at the **adjusted coefficient of determination**, which is adjusted for the number of variables

$$\bar{R}^2 = 1 - \frac{\text{RSS} / (n - k - 1)}{\text{TSS} / (n - 1)}$$

## Calculating in Python

With `statsmodels`, you get the coefficients, standard errors, t values and $R^2$ all at once (the Machine Learning Textbook uses `scikit-learn`'s `LinearRegression`).

```python
import numpy as np
import statsmodels.api as sm

x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 5, 4, 5])
X = sm.add_constant(x)          # add a column for the intercept
res = sm.OLS(y, X).fit()
print(res.params)               # [2.2 0.6]
print(res.rsquared)             # 0.6
print(res.summary())            # a table with standard errors, t values, p values and more
```

## Summary

- Regression model $y = \beta_0 + \beta_1 x + u$. The error term $u$ is every factor other than $x$
- OLS minimizes the sum of squared residuals. Slope $= S_{xy}/S_{xx}$, and the line passes through the point of means
- $R^2$ is the share of the total variation explained by the line. In multiple regression, also look at $\bar{R}^2$

## Exercises

```quiz
Q: Fit an OLS line to $x$ = 1, 2, 3, 4, 5 and $y$ = 2, 4, 5, 4, 5. What is the slope?
A: 0.6
E: $S_{xy} = 6$ and $S_{xx} = 10$, so the slope is $6/10 = 0.6$.

Q: What is the intercept of the line in the previous question?
A: 2.2
E: The line passes through the means (3, 4): $4 - 0.6 \times 3 = 2.2$.

Q: OLS (ordinary least squares) minimizes the sum of the squares of what?
A: residuals | residual | errors
E: A residual is the gap between the actual $y$ and the line.

Q: If $R^2 = 0.8$, what percent of the total variation does the line explain?
A: 80
E: $R^2$ is the share of the total variation explained by the line.

Q: In multiple regression, what is $\bar{R}^2$, which allows for the number of explanatory variables, called?
A: adjusted coefficient of determination | adjusted R2 | adjusted R-squared | adjusted
E: It corrects for $R^2$ rising just because variables are added.
```
