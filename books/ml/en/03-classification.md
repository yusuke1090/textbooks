# 3. Classification models

## What you will learn

- Typical models for binary classification and their features
- Logistic regression, SVM, decision trees, random forests, gradient boosting and LightGBM
- Multiclass classification and neural networks

Predicting which of two classes something belongs to is called **binary classification** (defective or good, fraudulent transaction or not, benign or malignant). In this chapter, we compare models on scikit-learn's breast cancer data (whether a tumor is benign or malignant). The ROC curve and AUC used for evaluation are explained in detail in Chapter 7.

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
```

`stratify=y` keeps the ratio of benign to malignant the same in the training and test sets.

## Logistic regression

Its name says "regression", but it is a **classification** model. It turns a weighted sum of the features into a probability between 0 and 1 with the sigmoid function.

$$P(y = 1 \mid x) = \frac{1}{1 + e^{-(w \cdot x + b)}}$$

- $w \cdot x$ is the dot product of the weights and the features, and $b$ is the intercept
- If the probability is above a threshold (usually 0.5), it predicts 1
- From the weights, you can see which features push in which direction (easy to explain)

```python
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=10000))
model.fit(X_train, y_train)
prob = model.predict_proba(X_test)[:, 1]     # probability of being 1
print("AUC:", roc_auc_score(y_test, prob))
```

> **Pass probabilities, not labels, to AUC.** If you pass 0/1 labels, as in `roc_auc_score(y_test, model.predict(X_test))`, you get a value for one fixed threshold, and the AUC comes out lower (in my original notes, 0.9977 became 0.9464).

## Support vector machine (SVM)

It draws the boundary between two classes that leaves the largest gap (**margin**). The data points closest to the boundary are called **support vectors**, and they alone decide the boundary.

- **Kernel method**: by thinking in a higher dimension that adds things like squared features, it can draw curved boundaries too. Try the RBF kernel first
- Main settings: `C` (the larger, the fewer mistakes it allows, and the more complex the boundary) and `gamma` (the larger, the more detailed the boundary). If either is too large, it overfits
- It is sensitive to differences in the scale of features, so standardization (Chapter 4) is a must

```python
from sklearn.svm import SVC

svm = make_pipeline(StandardScaler(), SVC(kernel="rbf", C=1.0))
svm.fit(X_train, y_train)
print("AUC:", roc_auc_score(y_test, svm.decision_function(X_test)))
```

SVM does not give probabilities, so pass the distance from the boundary (`decision_function`) to AUC. AUC only looks at the order of "how likely to be 1", so it can be calculated without probabilities (but not with 0/1 labels).

## Decision tree

It splits the data in the shape of a tree by asking Yes/No questions one after another, such as "Is feature A 3.5 or less?"

| Name | Meaning |
| --- | --- |
| Root node | The top. The first question |
| Internal node | A question along the way |
| Branch | A line connecting nodes (Yes / No) |
| Leaf node | The bottom. The final answer |

- You can see the flow of decisions in a diagram, so it is easy to explain. No standardization needed
- If you make it deep, it can fit the training data as closely as you like, so it overfits easily. Hold it back with `max_depth` (maximum depth) or `min_samples_split` (number of samples needed to split)

```python
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import classification_report

tree = DecisionTreeClassifier(max_depth=5, min_samples_split=10, random_state=42)
tree.fit(X_train, y_train)
print(classification_report(y_test, tree.predict(X_test)))
plot_tree(tree, filled=True, rounded=True, max_depth=2)   # draw only the top two levels
```

The precision, recall and F1 in `classification_report` are explained in Chapter 7.

## Random forest

It builds many slightly different decision trees and answers by their majority vote (the average of their probabilities). It overfits less than a single tree and needs few settings, so it is a good model to try first.

- Each tree uses different data: from the training data, it picks the same number of samples again, allowing the same one to be picked more than once (**bootstrap**; for example, [1, 2, 3, 4] → [2, 2, 3, 3])
- At each split of a tree, it randomly limits which features can be used (`max_features`)
- Main setting: the number of trees `n_estimators` (more is more stable, but slower)

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

rf = RandomForestClassifier(n_estimators=100, random_state=1)
scores = cross_val_score(rf, X_train, y_train, cv=5, scoring="roc_auc")
print("cross-validation AUC:", scores.mean().round(3), "±", scores.std().round(3))
rf.fit(X_train, y_train)
```

If the AUC on the test data comes out at exactly 1, it may just be luck. Use cross-validation (Chapter 7) to check whether the score stays stable when the split changes.

From the trained model, you can see which features mattered for the decision (**feature importance**).

```python
import pandas as pd
names = load_breast_cancer().feature_names
imp = pd.Series(rf.feature_importances_, index=names).sort_values()
imp.tail(10).plot.barh(title="Feature Importance using Random Forest")
```

## Gradient boosting

It builds shallow trees (weak learners) one after another, and each new tree corrects the mistakes of the previous ones. When its settings are tuned well, it is often more accurate than a random forest, but it is sensitive to its settings and takes longer to train. Try a random forest first, and use this when you want to push further.

- `n_estimators`: the number of trees
- `learning_rate`: how much each tree corrects. The smaller, the more careful (and the more trees you need)
- `max_depth`: the depth of the trees (shallow, around 2–5)

```python
from sklearn.ensemble import GradientBoostingClassifier

gb = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=1)
gb.fit(X_train, y_train)
print("AUC:", roc_auc_score(y_test, gb.predict_proba(X_test)[:, 1]))
```

### LightGBM

A fast gradient boosting library released by Microsoft in 2016 (`pip install lightgbm`). It is fast because it searches for split points using histograms and grows only the leaves that are worth growing. It is still widely used for large tabular data problems.

```python
import lightgbm as lgb

lgbm = lgb.LGBMClassifier(n_estimators=100, learning_rate=0.1, random_state=1)
lgbm.fit(X_train, y_train)
print("AUC:", roc_auc_score(y_test, lgbm.predict_proba(X_test)[:, 1]))
```

## A rough guide to choosing a model

| Model | Strengths | Weaknesses and cautions |
| --- | --- | --- |
| Logistic regression | Fast. Easy to explain with weights. Strong on data that a straight line can separate | Weak with curved boundaries. Standardize |
| SVM | Can draw curved boundaries | Standardization is a must. Slow on large data |
| Decision tree | Can be explained with a diagram. No standardization needed | Overfits easily |
| Random forest | Few settings and robust. Shows feature importance | Hard to explain what is inside |
| Gradient boosting, LightGBM | Very accurate | Sensitive to settings. Watch out for overfitting |

## Multiclass classification and neural networks

- **Multiclass classification** into three or more classes (such as iris species) works as is with most of the models so far. scikit-learn handles it internally, for example by splitting it into "one class vs. the rest"
- Evaluate it with a confusion matrix and multiclass F1 (Chapter 7)
- You can also use neural networks (`sklearn.neural_network.MLPClassifier`). For large data such as images and audio, use a deep learning library such as PyTorch

## Summary

- Logistic regression is a classification model that gives probabilities. Pass probabilities to AUC
- SVM maximizes the margin. Kernels give curved boundaries, and standardization is a must
- Decision trees are easy to explain but overfit easily. Random forests are robust thanks to the majority vote of many trees
- Gradient boosting and LightGBM correct the mistakes of previous trees. Very accurate, but be careful with the settings
- Try logistic regression and a random forest first, compare them, then fine-tune

## Exercises

```quiz
Q: What is the width between the boundary and the nearest data points, which SVM maximizes?
A: margin | the margin
E: Standardization is a must for SVM.

Q: Which model builds many decision trees and takes a majority vote?
A: random forest | random forests
E: It overfits less than a single tree.

Q: When computing AUC, what do you pass instead of the labels from `predict`?
A: probabilities | probability | predict_proba
E: Logistic regression is a classifier that gives probabilities.

Q: What method adds trees one by one, each fixing the errors of the last?
A: gradient boosting | boosting
E: LightGBM is in this family. It is accurate but needs careful settings.
```
