# 9. pandas（表のデータ）

## この章でわかること

- Series と DataFrame
- CSV の読み書きと、データの中身の確かめ方
- 列・行の取り出し、条件で絞る、列を足す
- 並べかえ、グループごとの集計、欠けた値、表をつなぐ

pandas は、Excel のような表のデータを Python で扱うライブラリです。

```python
import pandas as pd
```

## Series と DataFrame

| もの | 形 | たとえ |
| --- | --- | --- |
| `Series` | 1列（名前の付いた1次元の配列） | 表の1列 |
| `DataFrame` | 表（列の集まり） | Excel のシート |

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

左の 0〜4 は行の名前（**インデックス**）です。`None` は `NaN`（欠けた値）になります。

## CSV の読み書き

```python
df.to_csv("cows.csv", index=False)       # 書く（インデックスは書かない）
df = pd.read_csv("cows.csv")             # 読む
```

- Excel で作った日本語の CSV は、`pd.read_csv("a.csv", encoding="cp932")` で読めることが多い
- Excel のファイルは `pd.read_excel("a.xlsx")`（`pip install openpyxl` が要る）

## 中身を確かめる

| 書き方 | わかること |
| --- | --- |
| `df.head()` / `df.tail()` | 最初・最後の 5 行 |
| `df.shape` | （行の数, 列の数） |
| `df.info()` | 列ごとの型と、欠けていない値の数 |
| `df.describe()` | 数の列の、個数・平均・標準偏差・最小・四分位・最大 |
| `df["barn"].value_counts()` | 値ごとの個数 |
| `df.isna().sum()` | 列ごとの欠けた値の数 |

読みこんだら、まずこれで中身を見ます。

## 取り出す

```python
df["milk"]                     # 1列（Series）
df[["name", "milk"]]           # 複数の列（DataFrame）。[[ ]] と二重にする

df.loc[0, "name"]              # 行の名前・列の名前で: 'Hanako'
df.loc[0:2, ["name", "milk"]]  # loc のスライスは終わりも入る（0, 1, 2 行）
df.iloc[0, 0]                  # 位置（番号）で: 'Hanako'
df.iloc[:3, :2]                # 先頭 3 行・2 列（終わりは入らない）
```

## 条件で絞る

```python
df[df["milk"] >= 30]                              # 乳量 30 以上
df[(df["barn"] == "B") & (df["parity"] >= 2)]     # かつ（&）。条件は ( ) で囲む
df[(df["parity"] == 1) | (df["milk"] < 26)]       # または（|）
df[df["name"].isin(["Momo", "Yuki"])]             # どれかに当てはまる
df.query("barn == 'B' and parity >= 2")           # 文字で書くこともできる
```

`and`・`or` ではなく `&`・`|` を使います。

## 列を足す・変える

```python
df["milk_lb"] = df["milk"] * 2.2046                        # 計算した列
df["level"] = df["milk"].apply(lambda m: "多" if m >= 30 else "少")
df = df.rename(columns={"milk": "milk_kg"})                # 列の名前を変える
df = df.drop(columns=["milk_lb"])                          # 列を消す
```

> 絞りこんだ表の列を変えると、`SettingWithCopyWarning` が出ることがあります。`sub = df[df["barn"] == "A"].copy()` のように `.copy()` してから変えるか、`df.loc[条件, "列"] = 値` で、もとの表を直接変えます。

## 並べかえ

```python
df.sort_values("milk_kg", ascending=False)        # 乳量の多い順
df.sort_values(["barn", "parity"])                # 牛舎、次に産次の順
```

## グループごとの集計

```python
df.groupby("barn")["milk_kg"].mean()              # 牛舎ごとの平均乳量
df.groupby("barn").agg(頭数=("name", "count"),
                       平均=("milk_kg", "mean"),
                       最大=("milk_kg", "max"))
pd.crosstab(df["barn"], df["parity"])             # 牛舎 × 産次 の頭数の表
```

`mean` などは、欠けた値（NaN）を飛ばして計算します。

## 欠けた値

```python
df["milk_kg"].isna()                    # 欠けているか（True / False）
df.dropna(subset=["milk_kg"])           # 乳量が欠けた行を消す
df["milk_kg"].fillna(df["milk_kg"].mean())   # 平均でうめる
```

消すか、うめるか、何でうめるかは、データの意味を考えて決めます。

## 表をつなぐ

```python
births = pd.DataFrame({"name": ["Hanako", "Momo"],
                       "calving": ["2026-04-10", "2026-06-01"]})
merged = df.merge(births, on="name", how="left")     # name で横につなぐ
merged["calving"] = pd.to_datetime(merged["calving"])   # 日付の型にする
merged["days"] = (pd.Timestamp("2026-11-14") - merged["calving"]).dt.days
pd.concat([df, df])                                  # 縦につなぐ
```

`how="left"` は、左の表の行を全部残します（相手にない行は NaN）。`"inner"` は両方にある行だけです。

## まとめ

- 表は `DataFrame`、1列は `Series`。読んだら `head`・`info`・`describe` で確かめる
- 列は `df["列"]`、行と列は `loc`（名前）・`iloc`（位置）
- 条件は `df[(条件1) & (条件2)]`。変えるときは `.copy()` か `loc`
- `sort_values`・`groupby(...).agg(...)`・`merge` で並べ、まとめ、つなぐ

## 練習問題

```quiz
Q: pandas で、表全体を表す型は何ですか。
A: DataFrame | データフレーム
E: 1列は `Series` です。

Q: 行と列を「名前」で取り出すのは `loc` です。「位置（番号）」で取り出すのは何ですか。
A: iloc
E: `df.iloc[0, 1]` のように番号で指定します。

Q: 次のコードは何を表示しますか。
| import pandas as pd
| df = pd.DataFrame({"farm": ["A", "B", "A"], "milk": [30, 20, 40]})
| print(df.groupby("farm")["milk"].mean()["A"])
A: 35.0 | 35
E: 牧場 A の (30 + 40) / 2 = 35.0 です。

Q: 2つの表を、同じ列の値でつなぐ関数は何ですか。
A: merge | pd.merge
E: `pd.merge(左, 右, on="列")` のように書きます。
```
