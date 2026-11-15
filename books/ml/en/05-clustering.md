# 5. Clustering

Gathering similar data into groups (**clusters**) is called **clustering**. It is unsupervised learning, with no answers.

## k-means

1. Decide the number of clusters $k$ and place $k$ centers
2. Put each data point into the cluster of the nearest center
3. Take the mean of each cluster and make it the new center
4. Repeat steps 2–3 until the centers stop moving

```python
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans

X, y_true = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)
km = KMeans(n_clusters=4, n_init=10, random_state=0)
labels = km.fit_predict(X)
print(km.cluster_centers_)       # the 4 centers
```

`make_blobs` is a function that makes practice data with clumps (`n_samples`: number of points, `centers`: number of clumps, `cluster_std`: how spread out the clumps are).

## Agglomerative clustering

At first, each point is its own cluster, and then the most similar clusters are merged one after another. The order of merging drawn as a tree is called a **dendrogram**.

- The height at which you cut the tree decides the number of clusters. Cutting high gives a few large clusters
- The result depends on how clusters are merged (ward, average, complete and others). Ward picks the pair whose merging increases the variation within the cluster the least

```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import linkage, dendrogram

labels = AgglomerativeClustering(n_clusters=4).fit_predict(X)
Z = linkage(X, method="ward")            # a record of the merging order
dendrogram(Z, truncate_mode="level", p=5, no_labels=True)
```

## DBSCAN

It treats places where points are densely packed as clusters, and points with few other points around them as **noise** (outliers).

- `eps`: the radius within which points count as near
- `min_samples`: if there are this many points within radius `eps`, the point is a dense point (core point)
- Points you can reach from a core point are in the same cluster. Points that belong nowhere are noise (label −1)
- You do not have to decide the number of clusters, and it can find curved clusters too. It uses distances, so standardize first

```python
from sklearn.datasets import make_moons
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

X, _ = make_moons(n_samples=200, noise=0.08, random_state=0)    # two crescent moon shapes
labels = DBSCAN(eps=0.3, min_samples=5).fit_predict(StandardScaler().fit_transform(X))
print(sorted(set(labels.tolist())))       # [-1, 0, 1]: two clusters and noise (-1)
```

k-means cannot split these crescents into two well (because it splits into round shapes by distance from the centers).

## Comparing the three methods

| Method | Strengths | Weaknesses |
| --- | --- | --- |
| k-means | Simple and fast. Works on large data | You must decide $k$ in advance. Assumes round clusters of similar size. The result depends on the starting centers |
| Agglomerative | The dendrogram shows the hierarchy. You can choose the number later by where you cut the tree | Takes time and memory on large data. Once merged, clusters cannot be split again |
| DBSCAN | No need to decide the number. Finds any shape. Finds outliers | Choosing `eps` and `min_samples` is hard. Weak with data of uneven density and with high dimensions |

## Evaluating clustering

### When you have the answers

Cluster numbers (0, 1, 2, …) have no meaning, so you cannot compare them with accuracy. Use metrics that do not depend on how the numbers are assigned.

| Metric | Range | Meaning |
| --- | --- | --- |
| ARI (adjusted Rand index) | 1 is a perfect match, 0 is the same as random | How often two ways of splitting put the same pairs into the same cluster |
| NMI (normalized mutual information) | 0–1 | How much knowing one tells you about the other |

```python
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score

X, y_true = make_blobs(n_samples=100, centers=3, cluster_std=0.60, random_state=0)
pred = KMeans(n_clusters=3, n_init=10, random_state=0).fit_predict(X)
print("ARI:", adjusted_rand_score(y_true, pred))
print("NMI:", normalized_mutual_info_score(y_true, pred))
```

### When you have no answers

- In real situations, there are almost never answers. A person looks at what is in each cluster and checks whether the split is meaningful
- You can also use the silhouette score (`silhouette_score`) to see how tight the clusters are as a number. But a split with a good number is not always a useful split

### An example with face images (from my original notes)

I reduced face images to 100 components with PCA and then tried the three methods.

- With the default settings, DBSCAN labeled everything as noise. After tuning `eps`, it found faces too close to the camera, and faces with glasses or hats, as noise
- k-means and agglomerative clustering (10 clusters each) divided the cluster sizes differently, and the ARI between the two results was 0.09 — they hardly matched
- With agglomerative clustering at 40 clusters, I found clusters grouped by appearance, such as smiling, facing sideways and wearing glasses

## Summary

- k-means gathers points close to a center. You decide $k$, and it is good at round clusters
- Agglomerative clustering merges similar points one after another, and you can choose the number with the dendrogram
- DBSCAN makes dense areas into clusters and also finds outliers. Standardize and tune `eps`
- If you have answers, compare with ARI and NMI. If not, check by looking at the contents. It is good to try two or three methods and compare

## Exercises

```quiz
Q: Which method groups data into $k$ clusters around their centers?
A: k-means | kmeans
E: It is good at round clusters, and you choose $k$ first.

Q: In agglomerative clustering, what is the tree diagram of the merging order called?
A: dendrogram
E: You can pick the number of clusters from it.

Q: Which method makes clusters from dense regions and also finds outliers?
A: DBSCAN
E: Standardize, then tune `eps`.

Q: When true labels exist, name one three-letter measure for comparing them with the clusters.
A: ARI | NMI
E: Compare with ARI or NMI. Without labels, inspect the clusters yourself.
```
