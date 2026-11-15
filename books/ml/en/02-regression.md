# 2. Supervised learning and regression

## Classification and regression

| Type | What it predicts | Examples |
| --- | --- | --- |
| Classification | A category (separate values) | Benign or malignant, species, behavior |
| Regression | A number (continuous values) | Wind speed, milk yield, price |

Even when you want to predict a number, depending on the data, it can work better to turn it into a classification such as "high, normal, low".

## Generalization and overfitting

Predicting well on new data too is called **generalization**.

![Underfitting, a good fit and overfitting](images/en/fit.svg)

| State | Training data | New data | Cause |
| --- | --- | --- | --- |
| Underfitting | Poor | Poor | The model is too simple |
| Good fit | Good | Good | |
| Overfitting | Very good | Poor | The model is too complex and has memorized the quirks (noise) of the training data |

If there is a large gap between the scores on the training data and the test data, suspect overfitting.

## How to proceed with supervised learning

1. Split the data into training and test sets
2. Train the model on the training data
3. Check its score on the test data
4. Select, transform or create features (Chapter 6), and change the model's settings (hyperparameters) (Chapter 7)
5. Go back to step 2 and repeat

## Linear regression

This model assumes a straight-line (flat-plane) relationship between the target $y$ and the features $x_1, \dots, x_k$. It is the same as Chapter 7 (OLS) of the Statistics Textbook.

$$\hat{y} = w_0 + w_1 x_1 + w_2 x_2 + \cdots + w_k x_k$$

- One feature is simple regression; two or more is multiple regression
- The weights $w$ are chosen so that the sum of the squared differences between predictions and answers is as small as possible

In my original notes, I used Hungarian weather data (Kaggle's "Weather in Szeged 2006-2016") to predict wind speed from six features such as temperature, humidity and air pressure. Here we try the same flow with the diabetes data that comes with scikit-learn.

```python
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

X, y = load_diabetes(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print("MSE:", mean_squared_error(y_test, y_pred))
print("R2 (train):", model.score(X_train, y_train))
print("R2 (test):", r2_score(y_test, y_pred))
print("weights:", model.coef_, "intercept:", model.intercept_)
```

### Evaluating regression

| Metric | Formula | How to read it |
| --- | --- | --- |
| Mean squared error (MSE) | $\frac{1}{n}\sum (y_i - \hat{y}_i)^2$ | Smaller is better. The unit is squared (its square root is the RMSE) |
| Coefficient of determination ($R^2$) | $1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$ | Closer to 1 is better. How much better it is than predicting with the mean |

- Both are used to compare models with each other
- Also draw a scatter plot of predictions against answers to see where the model misses
- One split alone involves luck, so it is good to check with cross-validation (Chapter 7)

## Regularization (Lasso and Ridge)

When there are many features, the following happens.

- The model overfits easily
- It is hard to explain which features matter
- If features are highly correlated with each other (**multicollinearity**), the weights become unstable (Chapter 8 of the Statistics Textbook)

So, to keep the weights from getting too large, we add a penalty for "the size of the weights" to the error and minimize the total. This is called **regularization**.

$$\text{Ridge (L2):}\quad \sum_i (y_i - \hat{y}_i)^2 + \alpha \sum_j w_j^2$$

$$\text{Lasso (L1):}\quad \sum_i (y_i - \hat{y}_i)^2 + \alpha \sum_j \lvert w_j \rvert$$

| | Ridge (L2) | Lasso (L1) |
| --- | --- | --- |
| Penalty | Sum of squared weights | Sum of absolute weights |
| Weights | Makes all of them a little smaller | Makes some exactly 0 (selects features) |
| Good when | Many features each matter a little | Only a few features matter |

- The larger $\alpha$, the stronger the penalty and the simpler the model
- A mix of the two is called Elastic Net
- When regularizing, put the features on the same scale (standardization, Chapter 4)

```python
from sklearn.linear_model import Lasso, Ridge

ridge = Ridge(alpha=1.0).fit(X_train, y_train)
lasso = Lasso(alpha=0.1).fit(X_train, y_train)
print("weights that Lasso set to 0:", (lasso.coef_ == 0).sum())
```

> Logistic regression (Chapter 3), which is used for classification, also has L2 regularization on by default in scikit-learn (its strength is `C`; the smaller, the stronger).

## Summary

- Classification predicts a category; regression predicts a number
- Overfitting is when the model does well only on the training data and poorly on new data
- Repeat: split → train → check → change features or settings
- Evaluate linear regression with MSE and $R^2$
- Holding the weights down with regularization (Ridge, Lasso) makes the model more robust to overfitting and multicollinearity. Lasso can select features

## Exercises

```quiz
Q: Guessing a category is classification. What is guessing a number called?
A: regression
E: Predicting milk yield or a price is regression.

Q: What is it called when a model fits the training data well but fails on new data?
A: overfitting | over-fitting
E: Regularization and fewer features help prevent it.

Q: What three letters name the mean of squared errors used to judge regression?
A: MSE | mean squared error
E: Smaller is better. Look at $R^2$ too.

Q: Which regularization can set weights to 0 and so select features: Ridge or Lasso?
A: Lasso
E: Lasso (L1) sets the weights of useless features to 0.
```
