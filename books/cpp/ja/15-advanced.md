# 15. クラスの応用（演算子・テンプレート・例外）

## 演算子のオーバーロード

自分で作ったクラスにも、`+` や `<<` などの演算子を使えるようにできます。`operator` と演算子を名前にした関数を作ります。

```cpp
class Point {
private:
    int x, y;

public:
    Point(int a = 0, int b = 0) : x(a), y(b) {}

    Point operator+(const Point& p) const      // Point + Point
    {
        return Point(x + p.x, y + p.y);
    }
    Point operator+(int n) const               // Point + int
    {
        return Point(x + n, y + n);
    }
    Point& operator++()                        // 前置の ++
    {
        ++x;
        ++y;
        return *this;
    }

    friend Point operator+(int n, const Point& p);           // int + Point
    friend ostream& operator<<(ostream& os, const Point& p); // cout << Point
};

Point operator+(int n, const Point& p)
{
    return Point(p.x + n, p.y + n);
}

ostream& operator<<(ostream& os, const Point& p)
{
    return os << "(" << p.x << ", " << p.y << ")";
}

int main()
{
    Point p1(1, 2), p2(3, 4);
    cout << p1 + p2 << "\n";    // (4, 6)
    cout << p1 + 10 << "\n";    // (11, 12)
    cout << 10 + p1 << "\n";    // (11, 12)
    ++p1;
    cout << p1 << "\n";         // (2, 3)
    return 0;
}
```

- `p1 + p2` は、`p1.operator+(p2)` を呼ぶのと同じ
- `10 + p1` のように**左が int**のときは、メンバ関数にできない（int のメンバ関数は作れない）。クラスの外にふつうの関数として作る
- `friend` を付けた関数は、メンバでなくても `private` のメンバを使える
- 演算子の意味は、もとの意味（`+` なら足す）に近くしておく。まったくちがう意味にすると読みにくい

## 変換関数と変換コンストラクタ

| 方向 | 作るもの |
| --- | --- |
| ほかの型 → 自分のクラス | 引数が1つのコンストラクタ（**変換コンストラクタ**） |
| 自分のクラス → ほかの型 | `operator 型()` という関数（**変換関数**）。戻り値の型は書かない |

```cpp
class Number {
private:
    int n;

public:
    Number(int v) : n(v) {}                // 変換コンストラクタ: int → Number
    operator int() const { return n; }     // 変換関数: Number → int
};

int main()
{
    Number num = 10;       // int から Number が作られる
    int i = num;           // Number から int に変わる
    cout << i + 5 << "\n"; // 15
    return 0;
}
```

勝手に変わると、思わぬ所で変換が起きてまちがいのもとになります。自動で変えたくないときは `explicit` を付けます（`explicit Number(int v)`）。

## テンプレート

型だけがちがう関数やクラスを、1つの「型紙」にまとめられます。

### 関数テンプレート

7章では、`int` 用と `double` 用の `maxOf` を別々に書きました。テンプレートなら1つですみます。

```cpp
template <typename T>
T maxOf(T x, T y)
{
    return (x > y) ? x : y;
}

int main()
{
    cout << maxOf(3, 8) << "\n";              // T は int
    cout << maxOf(2.5, 1.5) << "\n";          // T は double
    cout << maxOf<double>(3, 2.5) << "\n";    // 型を指定することもできる
    return 0;
}
```

使った型ごとに、コンパイラが関数を作ってくれます。

### クラステンプレート

```cpp
template <typename T>
class Box {
private:
    T value;

public:
    Box(T v) : value(v) {}
    T get() const { return value; }
};

Box<int> b1(5);                 // int を入れる Box
Box<string> b2("hello");        // string を入れる Box
```

9章の `vector<int>` も、このクラステンプレートです。

## 例外処理

実行中に起きたまちがい（範囲の外の添字、ファイルが開けない、など）を**例外**といいます。`throw` で例外を投げ、`try` の中で起きた例外を `catch` で受け取ります。

```cpp
#include <iostream>
#include <stdexcept>
using namespace std;

double divide(int a, int b)
{
    if (b == 0) {
        throw invalid_argument("0 では割れません");   // 例外を投げる
    }
    return static_cast<double>(a) / b;
}

int main()
{
    try {
        cout << divide(10, 4) << "\n";     // 2.5
        cout << divide(10, 0) << "\n";     // ここで例外が起きる
        cout << "ここは実行されない\n";
    } catch (const invalid_argument& e) {
        cout << "エラー: " << e.what() << "\n";
    }
    cout << "続けます\n";
    return 0;
}
```

```text
2.5
エラー: 0 では割れません
続けます
```

- 例外が起きると、残りの処理を飛ばして、合う `catch` に移る
- `catch (const exception& e)` と書くと、標準の例外をまとめて受け取れる。`catch (...)` は何でも受け取る
- 受け取る `catch` がどこにもないと、プログラムは止まる
- `vector` の `at()` は、範囲の外で `out_of_range` を投げる

## 標準ライブラリ（STL）

よく使う入れ物（コンテナ）と道具は、標準ライブラリにそろっています。自分で作る前に、まずこれを探します。

| 名前 | ヘッダ | 中身 |
| --- | --- | --- |
| `string` | `<string>` | 文字列 |
| `vector` | `<vector>` | 大きさの変わる配列 |
| `map` | `<map>` | キーと値の組（Python の dict に近い） |
| `sort`、`find`、`max_element` | `<algorithm>` | 並べかえ、さがす、一番大きいもの |
| `unique_ptr` | `<memory>` | 自動で delete されるポインタ |

```cpp
#include <map>

map<string, int> milk;          // 牛の名前 → 乳量
milk["Hanako"] = 32;
milk["Momo"] = 28;
for (const auto& [name, kg] : milk) {        // C++17
    cout << name << ": " << kg << " kg\n";   // 名前の順に出る
}
```

## まとめ

- `operator+` などで演算子をオーバーロードする。左が自分のクラスでないときは、外の関数（`friend`）にする
- 変換コンストラクタ・変換関数で型を変える。勝手な変換を止めるには `explicit`
- `template <typename T>` で、型だけちがう関数・クラスをまとめる
- `throw` で投げ、`try` / `catch` で受け取る
- 入れ物や道具は、まず標準ライブラリ（`string`・`vector`・`map`・`algorithm`）を使う

## 練習問題

```quiz
Q: 型だけちがう関数やクラスを1つにまとめる書き方は何ですか（`??? <typename T>`）。
A: template
E: `template <typename T> T max2(T a, T b)` のように書きます。

Q: 例外を投げるキーワードは何ですか。
A: throw
E: `try` / `catch` で受け取ります。

Q: 次のコードは何を表示しますか。
| try {
|     throw runtime_error("no milk");
| } catch (const exception& e) {
|     cout << e.what();
| }
A: no milk
E: `what()` で、例外に入れた文字を取り出せます。

Q: 勝手な型の変換を止めるために、コンストラクタに付けるキーワードは何ですか。
A: explicit
E: 変換コンストラクタが知らないうちに使われるのを防ぎます。
```
