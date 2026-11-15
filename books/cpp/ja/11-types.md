# 11. 型を作る（typedef・enum・構造体）

## typedef と using

型に別の名前を付けられます。

```cpp
typedef unsigned long long ID;    // 古い書き方
using Score = int;                // C++11 からの書き方（同じ意味）

ID cowId = 1234567890;
Score s = 80;
```

## 列挙型

決まったいくつかの値に、名前を付けた型です。

```cpp
enum Week { SUN, MON, TUE, WED, THU, FRI, SAT };   // 0, 1, 2, … が順に付く

Week w = MON;
if (w == MON) cout << "月曜日\n";
```

`enum class` を使うと、名前がほかとぶつからず、整数とまちがえて使うこともなくなります（今はこちらがおすすめ）。

```cpp
enum class Color { Red, Green, Blue };

Color c = Color::Red;         // 型名:: を付けて使う
// int n = c;                 // エラー（勝手に整数にならない）
int n = static_cast<int>(c);  // 0（数がほしいときはキャスト）
```

## 構造体

ちがう型の値を、1つにまとめた型です。

```cpp
struct Car {
    int num;         // ナンバー（メンバ）
    double gas;      // ガソリンの量（メンバ）
};                   // 最後の ; を忘れない

int main()
{
    Car car1;
    car1.num = 1234;          // . （ドット演算子）でメンバを使う
    car1.gas = 25.5;

    Car car2 = {4567, 30.0};  // まとめて初期化

    cout << "ナンバーは" << car1.num << "、ガソリンは" << car1.gas << "です。\n";
    cout << "2台目のナンバーは" << car2.num << "です。\n";
    return 0;
}
```

- 構造体の中の変数を**メンバ**という
- 同じ構造体どうしなら、`car2 = car1;` で全部のメンバをまとめて代入できる

### 構造体を関数に渡す

値渡しだと全部コピーされるので、参照で渡すのがふつうです。

```cpp
void show(const Car& c)        // 見るだけなら const 参照
{
    cout << c.num << " " << c.gas << "\n";
}

void refuel(Car& c, double amount)    // 中身を変えるなら参照
{
    c.gas += amount;
}
```

### 構造体のポインタ

ポインタからメンバを使うときは、`->`（**アロー演算子**）を使います。

```cpp
Car car1 = {1234, 25.5};
Car* pCar = &car1;

pCar->gas = 30.0;          // (*pCar).gas = 30.0; と同じ
cout << pCar->num << "\n";
```

## 共用体

`union` は、いくつかのメンバが同じメモリを使う型です。一度に使えるのは1つのメンバだけです。メモリを節約したいとき（マイコンなど）に使うことがありますが、ふだんはあまり使いません。

## まとめ

- `using 別名 = 型;` で型に名前を付ける
- 決まった値の組は `enum class`
- 構造体は `struct 名前 { メンバ };`。`.` でメンバ、ポインタからは `->`
- 構造体を渡すときは参照（変えないなら `const`）
- 次の章のクラスは、構造体に「機能（関数）」を足したもの

## 練習問題

```quiz
Q: 型に別の名前を付ける、今の C++ の書き方は何ですか（`??? 別名 = 型;`）。
A: using
E: 昔の書き方は `typedef` です。

Q: 決まった値の組（色・季節など）を表す、型の安全な列挙型の書き方は何ですか。
A: enum class
E: `enum class Color { Red, Green };` のように書きます。

Q: 構造体のポインタからメンバを使うときの記号は何ですか。
A: ->
E: ふつうの構造体の変数からは `.` を使います。
```
