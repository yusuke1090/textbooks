# 1. What is machine learning? (classifying irises)

## What you will learn

- The problems machine learning can solve (supervised and unsupervised)
- Getting to know your data before building a model
- The basic flow of scikit-learn (classifying irises)

This textbook is based on my [study notes](https://note.com/k_1090/n/nca53389e754b) on *Introduction to Machine Learning with Python* (Andreas C. Müller and Sarah Guido, O'Reilly). For how to write Python, see the "Python Textbook".

## Problems machine learning can solve

| Type | What it does | Examples |
| --- | --- | --- |
| Supervised learning | Learns rules for predicting the answer from data that has answers (labels) | Reading handwritten digits, judging whether a tumor is benign or malignant, finding fraudulent transactions, recognizing a cow's behavior |
| Unsupervised learning | Finds groups or structure in data without answers | Grouping customers with similar tastes, finding the topics of blog posts |

Supervised learning is further divided into two kinds (Chapters 2 and 3).

- **Classification**: the answer is a category (benign or malignant, walking or lying down)
- **Regression**: the answer is a number (milk yield, wind speed, price)

## Know the task and the data

Before building a model, check the following.

- What do you want to predict, and do you have data with the answers?
- Do you have the data you need, and which data do you not need?
- Which algorithms are likely to fit?

> Some problems can be solved with simple summaries (averages and graphs) alone. Do not jump straight to machine learning; look at the data first.

## Why Python?

- There are many libraries with the latest algorithms (scikit-learn, LightGBM, PyTorch and others)
- It is easy to write and easy for beginners to understand
- Large companies use it too, and development and updates are active

This textbook uses **scikit-learn**. Check whether it is installed like this.

```python
import sklearn
print(sklearn.__version__)
```

If it is not installed, install it with `pip install scikit-learn` (with Anaconda, `conda install scikit-learn`).

## Classifying irises

From four measurements of an iris flower, we predict which of three species it is. Because we learn from data that has answers, this is classification in supervised learning.

### Loading the data

```python
from sklearn.datasets import load_iris

iris = load_iris()
print(iris.keys())           # data, target, target_names, feature_names, DESCR and more
print(iris.feature_names)    # sepal length and width, petal length and width (cm)
print(iris.target_names)     # ['setosa' 'versicolor' 'virginica']
print(iris.data.shape)       # (150, 4): 150 flowers, 4 features
```

- One flower (one row) is called a **sample**, each measurement (column) a **feature**, and the species we want to predict the **label** (target variable)

### Splitting into training and test data

Measuring accuracy on the data you trained on means nothing (the model might just have memorized it). Keep some data aside that you do not train on, and check with it.

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, random_state=0)
print(X_train.shape, X_test.shape)   # (112, 4) (38, 4): 75% and 25%
```

- By default, 75% goes to training and 25% to testing (you can change this with `test_size`)
- `random_state` is the seed of the random numbers that decide the split. With the same number, you get the same split every time

Before learning, look at the data with scatter plots of each pair of features (a pair plot). You can see that petal length and width separate the species well.

```python
import pandas as pd
import seaborn as sns

df = pd.DataFrame(X_train, columns=iris.feature_names)
df["target"] = y_train
sns.pairplot(df, hue="target")
```

seaborn is a graph library built on matplotlib (`pip install seaborn`).

### Learning and predicting with k-nearest neighbors

**k-nearest neighbors** (k-NN) looks at the $k$ training samples closest to a new sample and answers with the most common species among them.

```python
from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=1)   # decide by the single closest one
knn.fit(X_train, y_train)                   # learn
y_pred = knn.predict(X_test)                # predict
print("Test set score:", knn.score(X_test, y_test))   # 0.97 (97% correct)
```

In scikit-learn, every model is used in the same flow: **create it → learn with `fit` → predict with `predict` → check with `score`**.

## Summary

- There is supervised learning (classification and regression) and unsupervised learning
- Look at the data first. Sometimes a summary is enough
- Split the data into training and test sets, and check with the test set
- scikit-learn follows the flow "create → fit → predict → score"

## Exercises

```quiz
Q: What is machine learning from data with correct answers (labels) called?
A: supervised learning | supervised
E: Learning from data without answers is unsupervised learning.

Q: Which scikit-learn method makes the model learn from data?
A: fit | fit()
E: The flow is "create → fit → predict → score".

Q: Which method uses a trained model to guess answers for new data?
A: predict | predict()
E: `score` gives accuracy and similar measures.

Q: Data is split into a training set and what other set to check the model?
A: test | test set | testing
E: You only learn the model's real ability on data it did not learn from.

Q: What method guesses by a majority vote of the $k$ closest data points?
A: k-nearest neighbors | k-nearest neighbours | kNN | k-NN | nearest neighbors
E: We used it to classify irises.
```
