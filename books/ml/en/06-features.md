# 6. Feature engineering

## What you will learn

- Types of features
- Dummy variables (one-hot) and binning
- Index scores (transformations that use the target)
- How to select features (univariate, importance, stepwise, regularization)

Searching for the best way to represent the data for a particular algorithm is called **feature engineering**. Working on the features often improves the score more than changing the model.

## Types of features

| Type | Values | Examples |
| --- | --- | --- |
| Continuous data | Can take any number | Temperature, length, weight, time |
| Discrete data | Separate numbers | Counts, the number on a die |
| Categorical data | Labels with no order | Blood type, breed, color |

Turn continuous data into numbers the model can handle with scaling (Chapter 4), and categorical data with the dummy variables below.

## Dummy variables (one-hot)

Split a category into columns that are "1 if it is that category, 0 if not".

```python
import pandas as pd

df = pd.DataFrame({"color": ["red", "blue", "green", "blue", "red"],
                   "size": ["S", "M", "L", "M", "S"]})
print(pd.get_dummies(df[["color", "size"]]).astype(int))
```

| color_blue | color_green | color_red | size_L | size_M | size_S |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 0 | 0 | 1 |
| 1 | 0 | 0 | 0 | 1 | 0 |

- To select several columns, write `df[["color", "size"]]` (with double square brackets)
- In linear regression and similar models, including every column creates an exact straight-line relationship: "exactly one of them is always 1" (multicollinearity). Drop one column with `drop_first=True`
- To make sure the training and test sets get the same columns, you can also use scikit-learn's `OneHotEncoder(handle_unknown="ignore")`

## Binning

Cut continuous data into ranges (bins) to make it categorical. Even a straight-line model can then express a curved relationship.

```python
import numpy as np
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(0)
X = rng.uniform(0, 10, size=(100, 1))
y = 2 * np.sin(X).ravel() + rng.normal(0, 0.5, 100)     # a curved relationship

kb = KBinsDiscretizer(n_bins=5, encode="onehot-dense", strategy="uniform")
X_bin = kb.fit_transform(X)
print(LinearRegression().fit(X, y).score(X, y))          # straight line as is: low
print(LinearRegression().fit(X_bin, y).score(X_bin, y))  # with bins: higher
```

You can also cut data with pandas.

| Function | How it cuts | When to use it |
| --- | --- | --- |
| `pd.cut(x, bins=[0, 3, 6, 9])` | At the boundaries you choose (by default, the left edge is excluded and the right edge included) | When you want to decide the boundaries yourself. Values out of range become NaN |
| `pd.qcut(x, q=3)` | So that each range has about the same number of values | When you want equal counts. The same value may end up in different bins |

## Index score (a transformation that uses the target)

In binary classification, this is a number made for each range (or category) of a feature from the share of the target. Cases where the target is 1 (fraud, abnormal and so on) are called "black", and cases where it is 0 "white".

1. Divide the feature into bins (for a category such as sex, use it as is)
2. For each bin, count the shares of black and white
3. Divide the share of black by the share of white, and take the natural log

$$\text{Index score} = \ln \frac{\text{share of black in the bin}}{\text{share of white in the bin}}$$

- The more black a bin has, the larger the value, and because it takes the log, it fits well with straight-line models such as logistic regression
- It is made using the target, so **calculate it from the training data only** (using the test data would be cheating by looking at the answers). Bins with little data give unstable values, so merge bins

```python
import numpy as np
import pandas as pd

def index_score(x, y, bins):
    """ln(share of black / share of white) for each bin. x: feature, y: 0/1 target (training data)"""
    b = pd.cut(x, bins, right=False)
    t = pd.crosstab(b, y, normalize="index")      # share of white (0) and black (1) in each bin
    return np.log(t[1] / t[0])
```

## Selecting features

With too many features, overfitting, multicollinearity and difficulty of explanation become problems.

### Looking at one feature at a time

Build a model using one feature at a time and compare how much each matters (weights, $R^2$, AUC and so on). It is simple, but because you look at them one by one, you cannot see how they interact with other variables (omitted variable bias, Chapter 8 of the Statistics Textbook).

### Selecting by importance

Look at a random forest's `feature_importances_` (Chapter 3) and drop the features with low importance. For irises, petal width (about 0.48) and petal length (about 0.42) are high, and sepal length (about 0.08) and sepal width (about 0.02) are low.

### Stepwise selection

It adds and removes features one at a time and automatically searches for the combination that gives the best score. In scikit-learn, you can use `RFECV`, which combines this with cross-validation (it removes features starting from the least important).

```python
from sklearn.datasets import load_iris
from sklearn.feature_selection import RFECV
from sklearn.ensemble import RandomForestClassifier

iris = load_iris()
rfecv = RFECV(RandomForestClassifier(random_state=42), step=1, cv=5, scoring="accuracy")
rfecv.fit(iris.data, iris.target)
print("selected features:", [n for n, s in zip(iris.feature_names, rfecv.support_) if s])
```

Because it is automatic, it is easy, but when features are highly correlated, it may drop an important one. Look at the result and add back what you need by hand.

### Selecting with regularization

L1 regularization (Lasso, Chapter 2) sets the weights of features that do not matter to 0. If you keep only the features whose weights are not 0, you have selected features.

```python
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

X_s = StandardScaler().fit_transform(iris.data)       # standardize, because we compare weights
sel = SelectFromModel(LogisticRegression(l1_ratio=1, solver="saga", C=0.5, max_iter=10000))
sel.fit(X_s, iris.target)
print("remaining features:", [n for n, s in zip(iris.feature_names, sel.get_support()) if s])
# sepal length is dropped, and the other 3 remain
```

> Since scikit-learn 1.8, L1 for logistic regression is specified with `l1_ratio=1` (L2 is `0`). Up to 1.7, you wrote `penalty="l1"`.

## Summary

- Scale continuous data; use dummy variables for categories. Binning lets a straight-line model express curved relationships
- The index score is made from the share of the target. Calculate it from the training data only
- Select features by looking at one at a time, by importance, stepwise (RFECV) or with L1 regularization. A person should check automatic results

## Exercises

```quiz
Q: What do we call variables that turn categories into columns of 0 and 1?
A: dummy variables | dummy | one-hot | dummies
E: pandas `get_dummies` makes them.

Q: What is splitting continuous values into ranges called?
A: binning
E: It lets a linear model show a curved relationship.

Q: Which data do you use to compute a target-based score?
A: training | training data | train
E: Using the test answers leaks the answer.

Q: Which scikit-learn class selects features by removing them one at a time with cross-validation?
A: RFECV
E: It is a stepwise method. People should check the automatic result.
```
