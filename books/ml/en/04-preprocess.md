# 4. Preprocessing and dimensionality reduction

## What you will learn

- The two ways unsupervised learning is used
- Scaling (standardization, normalization and others), and applying the same transformation to training and test data
- Principal component analysis (PCA), NMF and t-SNE

## What is unsupervised learning?

Unsupervised learning pulls something out of the data alone, without using answers (labels).

| Type | What it does | Examples |
| --- | --- | --- |
| Transforming the data | Puts it in an easier form. Also used as preprocessing for supervised learning | Scaling, dimensionality reduction |
| Clustering | Groups similar things together (Chapter 5) | Grouping customers, sorting face images |

Because there are no answers, the hard part is that it is difficult to check with numbers whether it "worked". You use it to explore, while looking at the data.

## Scaling

When features have very different sizes (units), SVM, k-NN, logistic regression, PCA and others get pulled toward the large features. So we put them on the same scale.

| Transformation | Formula | Result |
| --- | --- | --- |
| StandardScaler (standardization) | $(x - \mu) / \sigma$ | Mean 0, standard deviation 1 |
| MinMaxScaler | $(x - \min) / (\max - \min)$ | Range 0–1 |
| RobustScaler | $(x - \text{median}) / \text{IQR}$ | Robust to outliers (IQR is the 75% point − the 25% point) |
| Normalizer (normalization) | $x / \lVert x \rVert$ | Makes the length of each sample (row) 1. For text data and the like |

> Decision trees, random forests and gradient boosting decide by split points, so they do not need scaling. The target ($y$) is usually not transformed.

### Transform training and test data in the same way

Decide the basis of the transformation (the mean, or the minimum and maximum) **from the training data only** (`fit`), and transform the test data with the same basis (`transform`).

- If you `fit` the test data separately, the two datasets are measured with different rulers, and the relationship between their original distributions is broken
- Split the data first, then decide the transformation (if you `fit` on all the data, information from the test set leaks into training)
- This means the test data can go outside 0–1. That is correct

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

scaler = StandardScaler().fit(X_train)        # decide the basis from the training data only
X_train_s = scaler.transform(X_train)
X_test_s = scaler.transform(X_test)          # same basis for the test data

print("as is:", SVC(C=100).fit(X_train, y_train).score(X_test, y_test))
print("standardized:", SVC(C=100).fit(X_train_s, y_train).score(X_test_s, y_test))
```

In my original notes, standardization raised the accuracy from 0.94 to 0.96. If you make it a pipeline, as in `make_pipeline(StandardScaler(), SVC())`, you can follow this procedure without mistakes (Chapter 3).

## Principal component analysis (PCA)

It combines many features into a small number of new features (**principal components**), while keeping as much of the information (variation) as possible.

1. Build the covariance matrix of the features
2. Find its eigenvalues and eigenvectors
3. Take the eigenvector directions as principal components, in order of largest eigenvalue (the variation in that direction)

- Looking at every pair of 30 features as scatter plots would take 435 plots, but with two principal components you can see it in one
- Principal components are combinations of the original features, so their meaning is hard to interpret
- It gets pulled by size, so standardize first

```python
from sklearn.decomposition import PCA

X_s = StandardScaler().fit_transform(X)
pca = PCA(n_components=2).fit(X_s)
X_pca = pca.transform(X_s)
print(X_s.shape, "→", X_pca.shape)                 # (569, 30) → (569, 2)
print("share of variation explained:", pca.explained_variance_ratio_)
print(pca.components_.shape)                        # (2, 30): weights of the original features for each component
```

- It can also be used as preprocessing for supervised learning. Then too, `fit` on the training data and only `transform` the test data
- With `whiten=True`, the size of each principal component is also equalized (whitening)

In my original notes, the 1-NN accuracy on face images (Labeled Faces in the Wild, each image several thousand pixels) was 22% with raw pixels and rose to 30% after PCA (100 components, whitened).

## Non-negative matrix factorization (NMF)

It splits data whose values are all 0 or more (image brightness, sound, word counts and so on) into the product of two matrices whose values are also 0 or more.

$$V \approx W H \qquad (V: m \times n,\; W: m \times r,\; H: r \times n)$$

- $r$ is the number of components. Components are only added together like "parts" (there is no subtraction), so they tend to have a clear meaning — parts like eyes and noses for faces, or topics for text

```python
from sklearn.decomposition import NMF

nmf = NMF(n_components=15, init="nndsvd", max_iter=2000, random_state=0)
W = nmf.fit_transform(X)       # how much of each component each sample has
H = nmf.components_            # the components (parts)
```

## t-SNE

This method assumes that high-dimensional data actually lies on a curved low-dimensional surface (a **manifold**) and spreads it out in two dimensions so you can see it (manifold learning).

1. In the high dimension, express how close points are to each other as probabilities
2. In two dimensions, also express closeness as probabilities
3. Move the points in two dimensions so that the difference between the two probability distributions (the KL divergence) gets smaller

- It preserves the relationships between nearby points well. With handwritten digits (`load_digits`), digits that overlap with PCA separate cleanly with t-SNE
- It cannot be used on new data (there is no `transform`), so it is for **looking at and exploring** data. Do not use it as preprocessing for supervised learning
- It takes time on large data

```python
from sklearn.datasets import load_digits
from sklearn.manifold import TSNE

digits = load_digits()
X_tsne = TSNE(random_state=42).fit_transform(digits.data)
# make a scatter plot of the two columns of X_tsne, colored by digits.target
```

## Summary

- Unsupervised learning is broadly divided into data transformation and clustering
- Fit scaling on the training data and apply the same transformation to the test data. Tree models do not need it
- PCA combines features along the directions of largest variation. Standardize first
- NMF splits data into parts of 0 or more. t-SNE is a two-dimensional map for looking at data and cannot be used on new data

## Exercises

```quiz
Q: Do you `fit` a scaler on the training data or the test data?
A: training | training data | train
E: Fit on the training data, then apply the same transform to the test data.

Q: What three letters name the method that summarizes data along the directions of greatest spread?
A: PCA | principal component analysis
E: Standardize first.

Q: What three letters name the method that splits data into non-negative parts?
A: NMF | non-negative matrix factorization
E: It suits data made by adding parts together.

Q: Which kind of model does not need scaling?
A: tree | trees | tree-based | decision tree
E: Decision trees and random forests only look at the order of values.
```
