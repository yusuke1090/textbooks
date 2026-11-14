# 7. Evaluating models

## What you will learn

- Cross-validation and group cross-validation
- Grid search, and the three datasets: training, validation and test
- Metrics for binary classification (confusion matrix, accuracy, precision, recall, F1, ROC/AUC, AR value, AIC)
- Metrics for multiclass classification

## Cross-validation

If you split into training and test data only once, the split may happen to be a good (or bad) one. **Cross-validation** divides the data into $k$ parts and trains and evaluates $k$ times, switching which part is used for evaluation.

![5-fold cross-validation](images/en/kfold.svg)

- Usually split into 5–10 parts
- Judge how good the model is by the mean of the scores, and how stable it is by their spread

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_breast_cancer(return_X_y=True)
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
scores = cross_val_score(model, X, y, cv=cv, scoring="roc_auc")
print(scores, scores.mean())
```

- `KFold(n_splits=5, shuffle=True, random_state=0)`: splits into 5. `shuffle` mixes the data before splitting
- For classification, `StratifiedKFold` keeps the class ratio the same in every part

### Group cross-validation

When the data comes in groups — like faces of the same person or data from the same cow — make sure the same group is not in both training and evaluation. If it is, the model looks better than it will on a new person (cow).

```python
from sklearn.model_selection import GroupKFold

groups = cow_ids          # the cow's ID for each sample, for example
scores = cross_val_score(model, X_cows, y_cows, cv=GroupKFold(n_splits=4), groups=groups)
```

## Grid search

A model's settings (**hyperparameters**, such as SVM's `C` or a tree's depth) are not decided automatically from the data. **Grid search** tries every combination of candidates and picks the best one.

If you measure the final score on the data you used to choose the settings, it looks too good. Split the data into three.

| Data | What it is used for |
| --- | --- |
| Training | Training the model |
| Validation | Choosing the settings (the evaluation part of cross-validation plays this role) |
| Test | Measuring the score just once, at the very end |

```python
from sklearn.model_selection import GridSearchCV, train_test_split

X_trval, X_test, y_trval, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
grid = GridSearchCV(
    make_pipeline(StandardScaler(), LogisticRegression(solver="liblinear", max_iter=1000)),
    {"logisticregression__C": [0.01, 0.1, 1, 10, 100], "logisticregression__l1_ratio": [0, 1]},   # 0 is L2, 1 is L1
    cv=5, scoring="roc_auc")
grid.fit(X_trval, y_trval)              # choose by cross-validation within training + validation
print("best settings:", grid.best_params_, "validation AUC:", round(grid.best_score_, 3))
print("test AUC:", grid.score(X_test, y_test))   # the model retrained with the chosen settings, just once at the end
```

## Metrics for binary classification

### The trap of accuracy

Accuracy is the share of correct answers. But if 95% of the data is normal, simply answering "normal" for everything gives 95% accuracy — without finding a single abnormal case. For imbalanced data, use the following metrics.

### Confusion matrix

![Confusion matrix](images/en/confusion.svg)

| Term | Meaning |
| --- | --- |
| TP (true positive) | Actually 1, predicted 1 |
| TN (true negative) | Actually 0, predicted 0 |
| FP (false positive) | Actually 0, wrongly predicted 1 (a false alarm) |
| FN (false negative) | Actually 1, missed as 0 |

### Precision, recall and F1

$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN} \qquad \text{Precision} = \frac{TP}{TP + FP} \qquad \text{Recall} = \frac{TP}{TP + FN}$$

$$F_1 = \frac{2 \times \text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

| Metric | Meaning | Important when |
| --- | --- | --- |
| Precision | Of the cases predicted 1, the share that really were 1 | You want fewer false alarms (FP). Many false reports are a problem |
| Recall | Of the real 1s, the share that were found | You want fewer misses (FN). Finding disease or fraud |
| F1 | The harmonic mean of precision and recall | You want to see both together as one number |

> In Japanese, the word 精度 ("accuracy") is used to mean accuracy, precision or recall. Check with the formula.

In my original notes, when I split irises into two classes, "versicolor or not", accuracy was 0.73, but recall for versicolor was 0.31 and F1 was 0.40. Looking at accuracy alone, you would not notice how many it misses.

```python
from sklearn.metrics import confusion_matrix, classification_report

model.fit(X_trval, y_trval)
y_pred = model.predict(X_test)
print(confusion_matrix(y_test, y_pred))        # [[TN, FP], [FN, TP]]
print(classification_report(y_test, y_pred))
```

### ROC curve and AUC

![ROC curve and AUC](images/en/roc.svg)

- The ROC curve plots the **true positive rate** TPR $= TP/(TP+FN)$ (the same as recall) against the **false positive rate** FPR $= FP/(FP+TN)$ while moving the threshold for predicting 1
- The closer to the upper left, the better. The point closest to the upper left is a candidate for the threshold
- The area under the curve is the **AUC**. 0.5 is random and 1 is perfect. As a rough guide, 0.7 or more is often usable
- AUC combines all thresholds into one value, so you can compare models without deciding a threshold. If AUC changes when you change the threshold, something is wrong, such as passing labels (0/1) (Chapter 3)

```python
from sklearn.metrics import roc_curve, roc_auc_score

prob = model.predict_proba(X_test)[:, 1]
fpr, tpr, thresholds = roc_curve(y_test, prob)
print("AUC:", roc_auc_score(y_test, prob))
```

### AR value (Gini coefficient)

In finance, such as credit models, the **AR value** (Accuracy Ratio, also called the Gini coefficient) is often used instead of AUC. It is scaled so that random is 0 and perfect is 1.

$$\text{AR} = 2 \times \text{AUC} - 1$$

If the AUC is 0.8, the AR is 0.6.

### AIC

**AIC** (Akaike information criterion) is a metric that balances how well the model fits against how complex it is. The smaller, the better the model.

$$\text{AIC} = 2k - 2\ln L$$

- $k$ is the number of parameters (weights and intercept), and $L$ is the likelihood (the probability of getting the data under that model)
- Adding features improves the fit ($\ln L$), but increases the $2k$ penalty. If the scores are about the same, choose the simpler model with the smaller AIC
- Calculate it from the fit on the data you trained on (training data). For regularized models, treat it as a rough guide
- scikit-learn has no function that gives AIC, so calculate it from the log loss, or use `statsmodels` logistic regression (`.aic`)

```python
from sklearn.metrics import log_loss

prob_tr = model.predict_proba(X_trval)[:, 1]
log_l = -log_loss(y_trval, prob_tr, normalize=False)    # log-likelihood on the training data
k = model[-1].coef_.size + 1                            # number of weights + intercept
print("AIC:", 2 * k - 2 * log_l)
```

## Metrics for multiclass classification

With three or more classes, the confusion matrix becomes a table of number of classes × number of classes. F1 is calculated for each class, and you choose how to combine them.

| Averaging | Calculation | Good when |
| --- | --- | --- |
| macro | Average the per-class F1 with equal weights | Every class matters about equally |
| micro | Add up TP, FP and FN over all classes, then calculate | You want overall correctness. Large classes count more |
| weighted | Average the per-class F1 weighted by the number of samples | You want to take the imbalance into account |

```python
from sklearn.metrics import f1_score
f1_score(y_true, y_pred, average="macro")   # you can also choose "micro" or "weighted"
```

## Summary

- Cross-validation reduces the luck of the split. For data in groups, use group cross-validation
- Choose settings with grid search. Separate training, validation and test data, and use the test data only once at the end
- For imbalanced data, look at precision, recall, F1 and AUC instead of accuracy. The true positive rate is the same as recall
- AR value $= 2\,\text{AUC} - 1$. AIC balances fit against complexity
- For multiclass, use macro, micro or weighted F1
