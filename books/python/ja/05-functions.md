# 5. 関数

## 関数を作る

```python
def average(values):
    """数のリストの平均を返す。"""        # 関数の説明（docstring）
    return sum(values) / len(values)

print(average([32.5, 28.0, 35.5]))     # 32.0
```

- `def 名前(引数):` で作り、中は字下げする
- `return 値` で値を返して、関数を終わる。`return` がなければ `None` を返す
- 最初の行の `"""…"""` は、その関数の説明（VS Code で関数にマウスを乗せると出る）

### 複数の値を返す

```python
def min_max(values):
    return min(values), max(values)    # タプルで返る

low, high = min_max([32.5, 28.0, 35.2])
```

## 引数

```python
def greet(name, greeting="こんにちは"):     # greeting にはデフォルトの値
    print(f"{greeting}、{name}さん")

greet("Taro")                         # こんにちは、Taroさん
greet("Taro", "おはよう")              # 位置で渡す
greet(greeting="こんばんは", name="Taro")   # キーワード（名前）で渡す。順番は自由
```

- デフォルトの値がある引数は、ない引数の**後ろ**に書く
- 引数が多い関数は、キーワードで渡すと読みやすい

> デフォルトの値に、リストのような変えられるものを使わないでください。`def add(x, items=[]):` と書くと、呼ぶたびに**同じリスト**が使い回されます。`items=None` にして、関数の中で `if items is None: items = []` とします。

### いくつでも受け取る

```python
def total(*values):            # 位置の引数をタプルで受け取る
    return sum(values)

def show(**info):              # キーワードの引数を辞書で受け取る
    for k, v in info.items():
        print(k, v)

total(1, 2, 3)                 # 6
show(name="Hanako", milk=32.5)
```

### 引数に渡したものを変えると

リストや辞書を渡して関数の中で中身を変えると、呼んだ側も変わります（同じものを指しているため。3章）。

```python
def add_cow(herd, name):
    herd.append(name)

herd = ["Hanako"]
add_cow(herd, "Momo")
print(herd)          # ['Hanako', 'Momo']
```

## スコープ

関数の中で作った変数は、関数の中だけで使えます（**ローカル変数**）。関数の外の変数（**グローバル変数**）は読めますが、代入すると新しいローカル変数になります。

```python
count = 0

def bad():
    count = 10         # 新しいローカル変数（外の count は 0 のまま）

def good(count):
    return count + 1   # 引数で受け取り、戻り値で返す

count = good(count)    # 1
```

`global count` と書けば外の変数を変えられますが、どこで変わったかわかりにくくなるので、引数と戻り値で受け渡しします。

## 型ヒント

引数と戻り値の型を書いておけます。動きは変わりませんが、VS Code が入力の補完やまちがいの指摘をしてくれます。

```python
def average(values: list[float]) -> float:
    return sum(values) / len(values)
```

## lambda（名前のない小さな関数）

`lambda 引数: 式` で、その場で小さな関数を作れます。並べかえの基準を渡すときによく使います。

```python
cows = [{"name": "Hanako", "milk": 32.5}, {"name": "Momo", "milk": 28.0}]
cows_sorted = sorted(cows, key=lambda c: c["milk"], reverse=True)   # 乳量の多い順
print([c["name"] for c in cows_sorted])    # ['Hanako', 'Momo']
```

## まとめ

- `def 名前(引数):` と `return`。最初に docstring で説明を書く
- 引数は位置・キーワードで渡せる。デフォルトの値に `[]` を使わない
- 関数の中の変数はローカル。値は引数と戻り値でやりとりする
- 型ヒントで読みやすく。`sorted(..., key=lambda x: ...)` で並べかえの基準を決める

## 練習問題

```quiz
Q: 次のコードは何を表示しますか。
| def area(w, h=2):
|     return w * h
| print(area(3) + area(3, h=4))
A: 18
E: area(3) は h=2 で 6、area(3, h=4) は 12。合わせて 18 です。

Q: 次のコードは何を表示しますか。
| cows = [("Hana", 30), ("Mimi", 25), ("Sora", 35)]
| print(sorted(cows, key=lambda c: c[1])[0][0])
A: Mimi
E: 2つめの値（乳の量）で小さい順に並べ、最初の名前を出しています。

Q: 関数の引数のデフォルトの値に使ってはいけない、変えられる入れ物の例は何ですか（記号2文字）。
A: [] | リスト | list
E: `[]` は関数を作ったときに1回だけ作られ、呼ぶたびに共有されてしまいます。

Q: 関数の最初に書く、関数の説明の文字列を何といいますか。
A: docstring | ドックストリング
E: `"""…"""` で書きます。
```
