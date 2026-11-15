# 6. モジュール・ファイル・例外

## この章でわかること

- モジュールの読みこみ（import）と、自分のモジュールの作り方
- ファイルの読み書き（テキスト・CSV・JSON）
- 例外の受け止め方（try・except）と、よくあるエラー

## import

ほかのファイルに書かれた関数などを使えるようにします。

```python
import math                       # モジュール全体
print(math.sqrt(2))               # モジュール名.名前 で使う

from math import sqrt, pi         # 名前だけを取りこむ
print(sqrt(2), pi)

import numpy as np                # 短い別名を付ける（8章）
```

`from math import *` は、どこから来た名前かわからなくなるので使いません。

### よく使う標準ライブラリ

Python に、はじめから入っているモジュールです。

| モジュール | できること |
| --- | --- |
| `math` | 平方根・三角関数・対数 |
| `random` | 乱数、ランダムに選ぶ |
| `statistics` | 平均・中央値・標準偏差 |
| `datetime` | 日付と時刻 |
| `pathlib` | ファイルやフォルダの場所 |
| `csv`・`json` | CSV・JSON の読み書き |

```python
from datetime import date, timedelta

calving = date(2026, 4, 10)               # 分娩した日
print(calving + timedelta(days=280))      # 280 日後
print((date(2026, 11, 14) - calving).days)  # 何日たったか
```

ほかの人が作ったライブラリは、仮想環境に入って `pip install 名前` で入れます（1章）。

## 自分のモジュール

`.py` のファイルは、そのままモジュールになります。

`milklib.py`:

```python
def average(values):
    return sum(values) / len(values)

if __name__ == "__main__":
    # このファイルを直接動かしたときだけ実行される（import されたときは動かない）
    print(average([1, 2, 3]))
```

`main.py`（同じフォルダ）:

```python
import milklib
print(milklib.average([32.5, 28.0]))
```

`if __name__ == "__main__":` の中に、試しに動かすコードを書いておくと、import したときに勝手に動きません。

## ファイルの読み書き

```python
# 書く（"w" は新しく作る・上書き。"a" は後ろに足す）
with open("memo.txt", "w", encoding="utf-8") as f:
    f.write("Hanako,32.5\n")
    f.write("Momo,28.0\n")

# 読む
with open("memo.txt", encoding="utf-8") as f:
    for line in f:                       # 1行ずつ
        name, milk = line.strip().split(",")
        print(name, float(milk))
```

- `with` を使うと、ブロックを出たときに自動でファイルが閉じられる
- 日本語をふくむときは `encoding="utf-8"` を付ける
- 全部まとめて読むなら `f.read()`。パスの操作は `pathlib` が便利（`Path("data") / "memo.txt"`）

### CSV と JSON

```python
import csv, json

with open("cows.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "milk"])
    writer.writerow(["Hanako", 32.5])

with open("cows.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):        # 1行を、見出しをキーにした辞書で
        print(row["name"], row["milk"])  # 値は文字列

data = {"name": "Hanako", "milk": [32.5, 33.0]}
with open("cow.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
with open("cow.json", encoding="utf-8") as f:
    print(json.load(f)["milk"])
```

表のデータを分析するなら、pandas の `read_csv`（9章）のほうが楽です。

## 例外

実行中に起きたエラーを**例外**といいます。`try` で囲むと、例外が起きてもプログラムを止めずに受け止められます。

```python
s = input("乳量: ")
try:
    milk = float(s)
except ValueError:
    print(f"{s!r} は数ではありません")
else:
    print(f"{milk}kg を記録しました")      # 例外が起きなかったとき
finally:
    print("入力をおわります")              # どちらでも必ず
```

- `except` には、受け止める例外の種類を書く。何でも受け止める `except:` だけにすると、思わぬまちがいまで隠れてしまう
- `except (ValueError, KeyError) as e:` で、まとめて受け止めて中身（`e`）を見られる
- 自分で例外を起こすときは `raise ValueError("乳量はマイナスにできません")`

## よくあるエラー

| エラー | 意味 | よくある原因 |
| --- | --- | --- |
| `SyntaxError` | 書き方がおかしい | `:` や `)` の付け忘れ、全角の空白や記号 |
| `IndentationError` | 字下げがおかしい | 空白の数がそろっていない、タブと空白がまざっている |
| `NameError` | その名前がない | 変数名のつづりちがい、定義する前に使った |
| `TypeError` | 型が合わない | `"3" + 1`（文字列と数を足した）、引数の数がちがう |
| `ValueError` | 値がおかしい | `int("abc")` |
| `IndexError` | 番号が範囲の外 | 長さ 3 のリストの `[3]` |
| `KeyError` | 辞書にそのキーがない | `d["wieght"]`（つづりちがい）。`get` を使う |
| `AttributeError` | そのメソッドや属性がない | `None` に `.append` した、つづりちがい |
| `FileNotFoundError` | ファイルがない | 場所のまちがい。ターミナルの今いるフォルダを確かめる |
| `ModuleNotFoundError` | モジュールがない | `pip install` していない、VS Code で別の Python を選んでいる |
| `ZeroDivisionError` | 0 で割った | データが空で `len` が 0 |

## まとめ

- `import モジュール`、`from モジュール import 名前`、`import numpy as np`
- 自分の `.py` もモジュール。試しのコードは `if __name__ == "__main__":` の中に
- ファイルは `with open(..., encoding="utf-8") as f:` で読み書きする
- `try` / `except 種類:` で例外を受け止める。エラーの名前から原因を考える

## 練習問題

```quiz
Q: `import numpy as np` の `np` のように、短い名前を付けるキーワードは何ですか。
A: as
E: `from モジュール import 名前` で、名前だけを取り込むこともできます。

Q: 自分の `.py` の中で、直接実行したときだけ動かすコードを書く `if` の条件は何ですか。
A: __name__ == "__main__" | __name__ == '__main__' | if __name__ == "__main__":
E: ほかのファイルから import されたときは動きません。

Q: 存在しないファイルを `open` で開こうとしたときに出るエラーの名前は何ですか。
A: FileNotFoundError
E: `try` / `except FileNotFoundError:` で受け止められます。

Q: 次のコードは何を表示しますか。
| try:
|     n = int("abc")
| except ValueError:
|     n = -1
| print(n)
A: -1
E: "abc" は整数に変えられず、ValueError になります。
```
