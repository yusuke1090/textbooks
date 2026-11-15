# 9. pandas (table data)

pandas is a library for handling table data, like Excel, in Python.

```python
import pandas as pd
```

## Series and DataFrame

| Thing | Shape | Comparison |
| --- | --- | --- |
| `Series` | One column (a 1-dimensional array with names) | One column of a table |
| `DataFrame` | A table (a collection of columns) | An Excel sheet |

```python
df = pd.DataFrame({
    "name":   ["Hanako", "Momo", "Sakura", "Yuki", "Hana"],
    "barn":   ["A", "A", "B", "B", "B"],
    "parity": [2, 1, 3, 2, 1],
    "milk":   [32.5, 28.0, 35.2, None, 25.8],
})
print(df)
```

```text
     name barn  parity  milk
0  Hanako    A       2  32.5
1    Momo    A       1  28.0
2  Sakura    B       3  35.2
3    Yuki    B       2   NaN
4    Hana    B       1  25.8
```

The 0–4 on the left are the row names (the **index**). `None` becomes `NaN` (a missing value).

## Reading and writing CSV

```python
df.to_csv("cows.csv", index=False)       # write (without the index)
df = pd.read_csv("cows.csv")             # read
```

- Japanese CSV files made in Excel can often be read with `pd.read_csv("a.csv", encoding="cp932")`
- Excel files: `pd.read_excel("a.xlsx")` (needs `pip install openpyxl`)

## Checking the contents

| How to write it | What it tells you |
| --- | --- |
| `df.head()` / `df.tail()` | The first / last 5 rows |
| `df.shape` | (number of rows, number of columns) |
| `df.info()` | The type of each column and the number of non-missing values |
| `df.describe()` | For numeric columns: count, mean, standard deviation, min, quartiles, max |
| `df["barn"].value_counts()` | The count of each value |
| `df.isna().sum()` | The number of missing values in each column |

After loading data, look at it with these first.

## Taking out data

```python
df["milk"]                     # one column (Series)
df[["name", "milk"]]           # several columns (DataFrame). Use double [[ ]]

df.loc[0, "name"]              # by row name and column name: 'Hanako'
df.loc[0:2, ["name", "milk"]]  # a loc slice includes the end (rows 0, 1, 2)
df.iloc[0, 0]                  # by position (number): 'Hanako'
df.iloc[:3, :2]                # first 3 rows, 2 columns (the end is not included)
```

## Filtering by conditions

```python
df[df["milk"] >= 30]                              # milk 30 or more
df[(df["barn"] == "B") & (df["parity"] >= 2)]     # and (&). Wrap each condition in ( )
df[(df["parity"] == 1) | (df["milk"] < 26)]       # or (|)
df[df["name"].isin(["Momo", "Yuki"])]             # matches any of these
df.query("barn == 'B' and parity >= 2")           # you can also write it as text
```

Use `&` and `|`, not `and` and `or`.

## Adding and changing columns

```python
df["milk_lb"] = df["milk"] * 2.2046                        # a calculated column
df["level"] = df["milk"].apply(lambda m: "high" if m >= 30 else "low")
df = df.rename(columns={"milk": "milk_kg"})                # rename a column
df = df.drop(columns=["milk_lb"])                          # remove a column
```

> If you change a column of a filtered table, you may get a `SettingWithCopyWarning`. Either `.copy()` first, as in `sub = df[df["barn"] == "A"].copy()`, or change the original table directly with `df.loc[condition, "column"] = value`.

## Sorting

```python
df.sort_values("milk_kg", ascending=False)        # highest milk first
df.sort_values(["barn", "parity"])                # by barn, then by parity
```

## Aggregating by group

```python
df.groupby("barn")["milk_kg"].mean()              # mean milk yield per barn
df.groupby("barn").agg(cows=("name", "count"),
                       mean=("milk_kg", "mean"),
                       max=("milk_kg", "max"))
pd.crosstab(df["barn"], df["parity"])             # a table of cow counts, barn × parity
```

`mean` and the like skip missing values (NaN) when calculating.

## Missing values

```python
df["milk_kg"].isna()                    # whether it is missing (True / False)
df.dropna(subset=["milk_kg"])           # remove rows where milk is missing
df["milk_kg"].fillna(df["milk_kg"].mean())   # fill with the mean
```

Decide whether to remove or fill, and what to fill with, by thinking about what the data means.

## Joining tables

```python
births = pd.DataFrame({"name": ["Hanako", "Momo"],
                       "calving": ["2026-04-10", "2026-06-01"]})
merged = df.merge(births, on="name", how="left")     # join side by side on name
merged["calving"] = pd.to_datetime(merged["calving"])   # make it a date type
merged["days"] = (pd.Timestamp("2026-11-14") - merged["calving"]).dt.days
pd.concat([df, df])                                  # stack vertically
```

`how="left"` keeps every row of the left table (rows missing from the other become NaN). `"inner"` keeps only rows that are in both.

## Summary

- A table is a `DataFrame`, one column is a `Series`. After loading, check with `head`, `info` and `describe`
- Columns are `df["column"]`; rows and columns are `loc` (names) and `iloc` (positions)
- Conditions are `df[(condition1) & (condition2)]`. When changing values, use `.copy()` or `loc`
- Sort, summarize and join with `sort_values`, `groupby(...).agg(...)` and `merge`

## Exercises

```quiz
Q: In pandas, what type represents a whole table?
A: DataFrame
E: A single column is a `Series`.

Q: `loc` selects rows and columns by name. Which selects them by position (number)?
A: iloc
E: For example `df.iloc[0, 1]`.

Q: What does this code print?
| import pandas as pd
| df = pd.DataFrame({"farm": ["A", "B", "A"], "milk": [30, 20, 40]})
| print(df.groupby("farm")["milk"].mean()["A"])
A: 35.0 | 35
E: Farm A: (30 + 40) / 2 = 35.0.

Q: Which function joins two tables on matching column values?
A: merge | pd.merge
E: Write `pd.merge(left, right, on="column")`.
```
