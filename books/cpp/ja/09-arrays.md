# 9. 配列と文字列

## 配列

同じ型の値をまとめて入れておく箱の並びを**配列**といいます。

```cpp
int test[5] = {80, 60, 22, 50, 75};    // 5 つの int を入れる配列

for (int i = 0; i < 5; i++) {
    cout << i + 1 << "番目の人の点数は" << test[i] << "です。\n";
}
```

- 1つ1つの箱を**要素**、`[ ]` の中の番号を**添字**という
- 添字は **0 から**始まる。`test[5]` の配列で使えるのは `test[0]`〜`test[4]`
- 範囲の外（`test[5]`）を使ってもコンパイルは通るが、ほかのメモリをこわして、おかしな動きや落ちる原因になる
- 要素の数は `sizeof(test) / sizeof(test[0])` でわかる（配列全体の大きさ ÷ 1つの大きさ）

### 並べかえ（バブルソート）

となり同士を比べて、大きいほうを後ろへ送ることをくり返します。

```cpp
const int NUM = 5;
int test[NUM] = {80, 60, 22, 50, 75};

for (int s = 0; s < NUM - 1; s++) {
    for (int t = s + 1; t < NUM; t++) {
        if (test[t] > test[s]) {        // 大きい順にする
            int tmp = test[t];
            test[t] = test[s];
            test[s] = tmp;
        }
    }
}
// test は {80, 75, 60, 50, 22}
```

ふだんは、標準ライブラリの `std::sort` を使います（`#include <algorithm>`）。

```cpp
sort(test, test + NUM);                       // 小さい順
sort(test, test + NUM, greater<int>());       // 大きい順
```

## 多次元配列

```cpp
int score[2][3] = {
    {80, 60, 22},     // 1 人目の 3 教科
    {50, 75, 90},     // 2 人目の 3 教科
};
cout << score[1][2] << "\n";    // 90
```

## 配列とポインタ

配列の名前は、**先頭の要素のアドレス**として使えます。

```cpp
int test[5] = {80, 60, 22, 50, 75};
int* p = test;            // &test[0] と同じ

cout << *p << "\n";       // 80
cout << *(p + 1) << "\n"; // 60（p + 1 は、次の要素のアドレス）
cout << p[2] << "\n";     // 22（ポインタにも [ ] が使える）
```

`p + 1` は、アドレスを 1 バイトではなく、**要素1つ分**（int なら 4 バイト）進めます。

### 配列を関数に渡す

配列を引数にすると、先頭のアドレスが渡されます。要素の数はわからないので、一緒に渡します。

```cpp
double avg(const int t[], int n)     // const int* t と同じ
{
    int sum = 0;
    for (int i = 0; i < n; i++) sum += t[i];
    return static_cast<double>(sum) / n;
}

avg(test, 5);    // 57.4
```

アドレスが渡るので、`const` を付けないと、関数の中から呼んだ側の配列を変えられます。

## 文字列

### char の配列（C の文字列）

C 言語から続く書き方では、文字列は `char` の配列で、最後に終わりの印 `'\0'` が入ります。

```cpp
char str[] = "Hello";    // 'H' 'e' 'l' 'l' 'o' '\0' の 6 文字分
cout << str << "\n";
cout << strlen(str) << "\n";     // 5（'\0' は数えない。#include <cstring>）
```

- 長さは `strlen`、コピーは `strcpy`、つなぐのは `strcat`、比べるのは `strcmp`
- 配列の大きさを超えて書きこむと、メモリをこわす。`=` で代入や、`==` で比べることはできない

### std::string（今の C++ ではこちら）

`#include <string>` の `std::string` を使うと、長さを気にせず、ふつうの値のように扱えます。

```cpp
#include <string>

string name = "Taro";
string msg = "Hello, " + name;       // + でつなぐ
cout << msg << " (" << msg.size() << "文字)\n";   // Hello, Taro (11文字)
if (name == "Taro") cout << "同じです\n";        // == で比べられる

string line;
getline(cin, line);                  // 空白を含む1行を読む
```

## std::vector（大きさの変わる配列）

`#include <vector>` の `std::vector` は、あとから要素を足せる配列です。

```cpp
#include <vector>

vector<int> test = {80, 60, 22};
test.push_back(50);                  // 後ろに足す
cout << test.size() << "\n";         // 4
for (int t : test) cout << t << " "; // 80 60 22 50
```

範囲の外は `test.at(10)` のように `at` で取り出すと、エラー（例外、15章）で知らせてくれます。

## まとめ

- 配列の添字は 0 から。範囲の外を使わない
- 配列名は先頭のアドレス。関数には要素数と一緒に渡す
- 文字列は `std::string`、大きさの変わる配列は `std::vector` を使うと安全で楽

## 練習問題

```quiz
Q: `int a[5];` の最後の要素の添字はいくつですか。
A: 4
E: 添字は 0 から数えるので、0〜4 です。

Q: 次のコードは何を表示しますか。
| int a[] = {4, 7, 1, 9};
| int m = a[0];
| for (int x : a) if (x > m) m = x;
| cout << m;
A: 9
E: 範囲 for 文で、いちばん大きい値を探しています。

Q: 次のコードは何を表示しますか。
| vector<int> v = {1, 2, 3};
| v.push_back(4);
| cout << v.size();
A: 4
E: `push_back` で後ろに1つ足しています。

Q: 今の C++ で文字列を扱うときに使う、標準ライブラリの型は何ですか。
A: std::string | string
E: char の配列（C の文字列）より安全で楽です。
```
