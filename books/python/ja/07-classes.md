# 7. クラス

## クラスとは

**クラス**は、データ（**属性**）と、それを使う機能（**メソッド**）をまとめた型です。クラスから作った実体を**インスタンス**（オブジェクト）といいます。

```python
class Cow:
    def __init__(self, name, parity):     # インスタンスを作るときに呼ばれる
        self.name = name                   # 属性
        self.parity = parity               # 産次
        self.records = []                  # 乳量の記録

    def add_milk(self, kg):                # メソッド
        self.records.append(kg)

    def average(self):
        if not self.records:
            return 0.0
        return sum(self.records) / len(self.records)

hanako = Cow("Hanako", 2)                  # インスタンスを作る
hanako.add_milk(32.5)
hanako.add_milk(33.5)
print(hanako.name, hanako.average())       # Hanako 33.0

momo = Cow("Momo", 1)                      # 別のインスタンス（データは別々）
```

- `__init__` は、インスタンスを作るときに自動で呼ばれる（C++ のコンストラクタにあたる）
- メソッドの最初の引数 `self` は、**そのインスタンス自身**。呼ぶときは書かない（`hanako.add_milk(32.5)`）
- `self.名前` に入れたものが、インスタンスごとの属性になる

## クラス変数

クラスの中、メソッドの外に書いた変数は、全部のインスタンスで共有されます。

```python
class Cow:
    count = 0                        # クラス変数（全部で1つ）

    def __init__(self, name):
        self.name = name             # インスタンス変数（1頭ずつ）
        Cow.count += 1

Cow("Hanako"); Cow("Momo")
print(Cow.count)                     # 2
```

## 特別なメソッド

`__名前__` の形のメソッドを作ると、Python の決まった動きに組みこめます。

```python
class Cow:
    def __init__(self, name, parity):
        self.name = name
        self.parity = parity

    def __str__(self):                       # print したときの見え方
        return f"{self.name}（{self.parity}産）"

    def __lt__(self, other):                 # < で比べる（sorted で並ぶ）
        return self.parity < other.parity

cows = [Cow("Hanako", 2), Cow("Momo", 1)]
print(cows[0])                               # Hanako（2産）
print([str(c) for c in sorted(cows)])        # ['Momo（1産）', 'Hanako（2産）']
```

## 継承

すでにあるクラスに機能を足した、新しいクラスを作れます。

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "…"

class Cow(Animal):                           # Animal を継承
    def __init__(self, name, parity):
        super().__init__(name)               # 親クラスの __init__ を呼ぶ
        self.parity = parity

    def speak(self):                         # 上書き（オーバーライド）
        return "モー"

for a in [Animal("?"), Cow("Hanako", 2)]:
    print(a.name, a.speak())                 # ? …  /  Hanako モー
```

- `super()` で親クラスのメソッドを呼ぶ
- 同じ名前のメソッドを書くと上書きされる。呼んだインスタンスのクラスのものが使われる

## 隠す（の約束）

Python には C++ の `private` のような仕組みはありません。名前を `_` で始めると「外から触らないで」という約束になります。

## dataclass

データを入れるだけのクラスなら、`@dataclass` を付けると `__init__` や `__repr__`（表示）、`==` での比較を自動で作ってくれます。

```python
from dataclasses import dataclass, field

@dataclass
class Cow:
    name: str
    parity: int = 1
    records: list[float] = field(default_factory=list)   # リストは field で

    def average(self) -> float:
        return sum(self.records) / len(self.records) if self.records else 0.0

c = Cow("Hanako", 2)
print(c)                     # Cow(name='Hanako', parity=2, records=[])
print(c == Cow("Hanako", 2)) # True
```

## まとめ

- `class 名前:` の中に `__init__(self, ...)` とメソッドを書く。`self` はインスタンス自身
- `self.x` はインスタンスごと、クラスの中に直接書いた変数は全部で共有
- `__str__` で表示の形を決める
- `class 子(親):` で継承し、`super().__init__()` で親の初期化を呼ぶ
- データを入れるだけなら `@dataclass`

## 練習問題

```quiz
Q: インスタンスを作るときに呼ばれる、初期化のメソッドの名前は何ですか。
A: __init__
E: `def __init__(self, ...):` と書きます。

Q: メソッドの最初の引数で、インスタンス自身を表すものは何ですか。
A: self
E: `self.x` はインスタンスごとの変数です。

Q: `print()` で表示したときの形を決める特別なメソッドは何ですか。
A: __str__
E: 文字列を返すように書きます。

Q: 子のクラスの `__init__` の中で、親の初期化を呼ぶ書き方は何ですか。
A: super().__init__() | super().__init__ | super()
E: `class 子(親):` で継承します。

Q: データを入れるだけのクラスを短く書くための、`@` で始まる飾りは何ですか。
A: @dataclass | dataclass
E: `__init__` などを自動で作ってくれます。
```
