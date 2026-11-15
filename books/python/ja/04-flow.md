# 4. 条件分岐と繰り返し

## この章でわかること

- if・elif・else と字下げ
- for と range・enumerate・zip
- while、break と continue

## if 文

```python
milk = 32.5

if milk >= 35:
    print("とても多い")
elif milk >= 25:
    print("ふつう")
else:
    print("少ない")
print("おわり")
```

- 条件の後ろに `:`（コロン）を付ける
- 中の文は**字下げ**（ふつうは空白 4 つ）する。字下げがそろっている所までが1つのまとまり。そろっていないと `IndentationError`
- 上から順に調べ、最初に当てはまったものだけを実行する

### 1行で値を選ぶ

```python
label = "多い" if milk >= 30 else "少ない"
```

### 偽とみなされる値

`if` の条件に、真偽でない値も書けます。`0`・`0.0`・`""`（空の文字列）・`[]`・`{}`・`None` は偽、それ以外は真とみなされます。

```python
names = []
if not names:
    print("まだ1頭もいません")
```

## for 文

入れ物の中身を1つずつ取り出します。

```python
for m in [32.5, 28.0, 35.2]:
    print(m)
```

### range

決まった回数を回すときに使います。

| 書き方 | 出てくる数 |
| --- | --- |
| `range(5)` | 0, 1, 2, 3, 4 |
| `range(1, 6)` | 1, 2, 3, 4, 5 |
| `range(0, 10, 2)` | 0, 2, 4, 6, 8 |
| `range(5, 0, -1)` | 5, 4, 3, 2, 1 |

```python
for i in range(1, 10):
    for j in range(1, 10):
        print(i * j, end="\t")     # end で改行の代わりにタブ
    print()                        # 改行（九九の表）
```

### enumerate と zip

```python
names = ["Hanako", "Momo", "Sakura"]
milk = [32.5, 28.0, 35.2]

for i, name in enumerate(names, start=1):    # 番号を付けて
    print(i, name)

for name, m in zip(names, milk):             # 2つを並べて
    print(f"{name}: {m}kg")
```

番号がほしいときに `for i in range(len(names)):` と書くより、`enumerate` のほうが Python らしい書き方です。

## while 文

条件が真の間、繰り返します。

```python
total = 0
while True:
    s = input("乳量（空で終わり）: ")
    if s == "":
        break               # 繰り返しを終わる
    total += float(s)
print("合計", total)
```

## break と continue

| 文 | すること |
| --- | --- |
| `break` | 繰り返しをすぐに終わる |
| `continue` | その回の残りを飛ばして、次の回へ |

```python
for n in range(1, 11):
    if n == 7:
        break
    if n % 2 == 0:
        continue
    print(n)          # 1 3 5
```

止まらなくなったら、ターミナルで **Ctrl + C** を押します。

## match 文

1つの値で、たくさんに分けるときに使えます（Python 3.10 から）。

```python
command = "start"
match command:
    case "start":
        print("始めます")
    case "stop" | "quit":
        print("止めます")
    case _:
        print("わかりません")       # どれにも当てはまらないとき
```

## まとめ

- `if 条件:` の後ろは字下げ。`elif`・`else` で分ける
- `for x in 入れ物:`。回数なら `range`、番号付きは `enumerate`、並べるなら `zip`
- `while` は条件の間くり返す。`break` で終わり、`continue` で次へ

## 練習問題

```quiz
Q: 次のコードは何を表示しますか。
| print(list(range(1, 10, 3)))
A: [1, 4, 7] | 1, 4, 7
E: 1 から始めて 3 ずつ、10 の手前までです。

Q: 次のコードは何を表示しますか。
| total = 0
| for i in range(5):
|     if i == 3:
|         continue
|     total += i
| print(total)
A: 7
E: 0 + 1 + 2 + 4 = 7。`continue` で 3 だけ飛ばしています。

Q: `for` で、番号と値を一緒に取り出すときに使う関数は何ですか。
A: enumerate | enumerate()
E: 2つの入れ物を並べて回すときは `zip` です。

Q: ループをそこで終わらせる文は何ですか。
A: break
E: `continue` は、その回だけ飛ばして次へ進みます。
```
