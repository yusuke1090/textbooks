# 10. matplotlib (graphs)

## What you will learn

- The idea of Figures and Axes
- Line plots, scatter plots, bar charts, histograms and box plots
- Displaying Japanese, placing several graphs side by side, and saving as an image

```python
import matplotlib.pyplot as plt
```

## Figures and Axes

In matplotlib, you place **Axes** (one graph) on a **Figure** (the whole sheet of paper) and draw on them. The usual way today is to make both with `plt.subplots()` and draw on `ax`.

```python
import numpy as np

days = np.arange(1, 31)
milk = 30 + 3 * np.sin(days / 5) + np.random.default_rng(0).normal(0, 0.8, 30)

fig, ax = plt.subplots(figsize=(6, 3.5))      # 6 inches wide, 3.5 high
ax.plot(days, milk, marker="o", label="Hanako")
ax.set_xlabel("Day")
ax.set_ylabel("Milk (kg)")
ax.set_title("Daily milk yield")
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()                            # tidy up so text does not overlap
plt.show()                                    # show it on screen
```

## Various graphs

| Graph | How to write it | Good for |
| --- | --- | --- |
| Line | `ax.plot(x, y)` | Change over time |
| Scatter | `ax.scatter(x, y)` | The relationship between two numbers |
| Bar | `ax.bar(names, values)` (`barh` for horizontal) | Comparing categories |
| Histogram | `ax.hist(values, bins=10)` | Distribution (where values are common) |
| Box plot | `ax.boxplot([values1, values2])` | Comparing distributions, outliers |

```python
rng = np.random.default_rng(1)
parity = rng.integers(1, 5, 50)
milk = 25 + 2.5 * parity + rng.normal(0, 3, 50)

fig, axes = plt.subplots(1, 3, figsize=(11, 3.2))    # 1 row, 3 columns
axes[0].scatter(parity, milk, alpha=0.6)
axes[0].set_xlabel("Parity"); axes[0].set_ylabel("Milk (kg)")
axes[1].hist(milk, bins=10, edgecolor="white")
axes[1].set_xlabel("Milk (kg)")
axes[2].bar(["A", "B", "C"], [31.2, 28.5, 33.0])
axes[2].set_ylabel("Mean milk (kg)")
fig.tight_layout()
plt.show()
```

When you arrange graphs with `plt.subplots(rows, columns)`, `axes` becomes an array, and you draw on each one, like `axes[0]` (with two or more rows, `axes[0, 1]`).

## Displaying Japanese

As is, Japanese text shows up as □. On Ubuntu, install a Japanese font and specify it.

```bash
sudo apt install fonts-noto-cjk
```

```python
plt.rcParams["font.family"] = "Noto Sans CJK JP"
```

If it is still □ after installing the font, delete `~/.cache/matplotlib` so it reloads. Writing the axis labels in English is another option.

## Saving as an image

```python
fig.savefig("milk.png", dpi=150, bbox_inches="tight")   # save with the margins trimmed
```

- Save before `plt.show()` (after `show` closes it, an empty figure may be saved)
- When there is no screen, as on a Raspberry Pi or Jetson connected over ssh, save instead of `show`, and open the image in VS Code to look at it
- Saving as `.svg` or `.pdf` keeps it sharp even when zoomed in

## Drawing from pandas

pandas tables can be drawn directly with `plot` (it uses matplotlib inside).

```python
import pandas as pd

df = pd.DataFrame({"day": days, "milk": 30 + 3 * np.sin(days / 5)})
ax = df.plot(x="day", y="milk", figsize=(6, 3))
ax.set_ylabel("Milk (kg)")
df["milk"].plot.hist(bins=10)
```

## Jupyter and VS Code

- In an `.ipynb` (Chapter 1), the graph appears right below the cell
- In a normal `.py`, `plt.show()` opens a separate window. When you close it, the program continues

## Summary

- Create with `fig, ax = plt.subplots()` and draw with `ax.plot`, `ax.scatter` and so on
- Add axis labels, a title and a legend (`legend`). Tidy up with `tight_layout`
- For Japanese, install `fonts-noto-cjk` and set `font.family`
- Save with `fig.savefig("name.png", dpi=150, bbox_inches="tight")`
