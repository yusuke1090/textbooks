# 付録A. Python との対応表

Python を知っている人のために、同じことを C++ でどう書くかを並べます。

## 基本

| すること | Python | C++ |
| --- | --- | --- |
| 動かし方 | `python3 a.py` | `g++ -std=c++17 -o a a.cpp` → `./a` |
| 画面に出す | `print("x =", x)` | `cout << "x = " << x << "\n";` |
| 入力 | `n = int(input())` | `int n; cin >> n;` |
| コメント | `# メモ` | `// メモ` |
| 文の終わり | 改行 | `;` |
| ブロック | 字下げ（インデント） | `{ }` |
| 変数 | `x = 3`（型を書かない） | `int x = 3;`（型を書く。`auto x = 3;` も可） |
| 真偽 | `True` / `False` | `true` / `false` |
| 何もない | `None` | `nullptr`（ポインタ） |
| 整数の割り算 | `7 // 2` → 3 | `7 / 2` → 3 |
| 小数の割り算 | `7 / 2` → 3.5 | `7.0 / 2` → 3.5 |
| べき乗 | `2 ** 10` | `pow(2, 10)`（`<cmath>`） |
| かつ・または・でない | `and` `or` `not` | `&&` `\|\|` `!` |

## 流れ

| すること | Python | C++ |
| --- | --- | --- |
| 条件分岐 | `if a > 0:` / `elif` / `else:` | `if (a > 0) { } else if () { } else { }` |
| 回数の繰り返し | `for i in range(5):` | `for (int i = 0; i < 5; i++) { }` |
| 中身を順に | `for x in xs:` | `for (auto x : xs) { }` |
| 条件の繰り返し | `while n != 0:` | `while (n != 0) { }` |
| 値を選ぶ | `a if c else b` | `c ? a : b` |
| 多くに分ける | `match` | `switch` / `case 1:` / `break;` |

## データ

| すること | Python | C++ |
| --- | --- | --- |
| 文字列 | `s = "abc"` | `string s = "abc";` |
| 長さ | `len(s)` | `s.size()` |
| リスト | `xs = [1, 2, 3]` | `vector<int> xs = {1, 2, 3};` |
| 後ろに足す | `xs.append(4)` | `xs.push_back(4);` |
| 辞書 | `d = {"a": 1}` | `map<string, int> d = {{"a", 1}};` |
| 並べかえ | `xs.sort()` | `sort(xs.begin(), xs.end());` |
| 組（タプル） | `(1, "a")` | `pair<int, string>(1, "a")`、`tuple` |

## 関数とクラス

| すること | Python | C++ |
| --- | --- | --- |
| 関数 | `def add(x, y): return x + y` | `int add(int x, int y) { return x + y; }` |
| デフォルト引数 | `def f(x, y=1):` | `int f(int x, int y = 1)` |
| クラス | `class Car:` | `class Car { … };` |
| 初期化 | `def __init__(self, n):` | `Car(int n) : num(n) {}`（コンストラクタ） |
| 自分自身 | `self.num` | `this->num`（ふつうは `num` だけ） |
| 隠す | `_num`（習慣だけ） | `private:` |
| 継承 | `class RacingCar(Car):` | `class RacingCar : public Car` |
| 上書き | 同じ名前で定義 | `virtual` と `override` |
| 例外 | `try:` / `except ValueError as e:` / `raise` | `try { } catch (const exception& e) { }` / `throw` |

## 大きなちがい

- **型**: C++ は変数の型をコンパイルのときに決める。まちがいは実行の前にわかる
- **速さ**: C++ は機械語にしてから動かすので、ずっと速い。マイコン（ラズパイピコ）でも動く
- **メモリ**: Python は自動で片付ける。C++ は、`new` したら `delete`（今は `vector` や `unique_ptr` で自動にする）
- **引数**: Python は、リストなどを渡すと中身を共有する。C++ はふつうコピー（値渡し）。共有したいときは参照（`&`）
