# 15. Applying classes (operators, templates and exceptions)

## What you will learn

- Operator overloading
- Conversion functions and converting constructors
- Templates (function templates and class templates)
- Exception handling (try, throw, catch)
- The standard library (STL)

## Operator overloading

You can make operators such as `+` and `<<` work with your own classes too. Write a function whose name is `operator` plus the operator.

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
    Point& operator++()                        // prefix ++
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

- `p1 + p2` is the same as calling `p1.operator+(p2)`
- When **the left side is an int**, as in `10 + p1`, it cannot be a member function (you cannot make member functions for int). Make it a normal function outside the class
- A function marked `friend` can use `private` members even though it is not a member
- Keep an operator's meaning close to its original meaning (adding, for `+`). Giving it a completely different meaning makes code hard to read

## Conversion functions and converting constructors

| Direction | What to make |
| --- | --- |
| Another type → your class | A constructor with one argument (a **converting constructor**) |
| Your class → another type | A function called `operator Type()` (a **conversion function**). Do not write a return type |

```cpp
class Number {
private:
    int n;

public:
    Number(int v) : n(v) {}                // converting constructor: int → Number
    operator int() const { return n; }     // conversion function: Number → int
};

int main()
{
    Number num = 10;       // a Number is made from an int
    int i = num;           // the Number turns into an int
    cout << i + 5 << "\n"; // 15
    return 0;
}
```

If conversions happen on their own, they can happen in unexpected places and cause mistakes. When you do not want automatic conversion, add `explicit` (`explicit Number(int v)`).

## Templates

Functions and classes that differ only in type can be combined into one "pattern".

### Function templates

In Chapter 7, we wrote separate `maxOf` functions for `int` and `double`. With a template, one is enough.

```cpp
template <typename T>
T maxOf(T x, T y)
{
    return (x > y) ? x : y;
}

int main()
{
    cout << maxOf(3, 8) << "\n";              // T is int
    cout << maxOf(2.5, 1.5) << "\n";          // T is double
    cout << maxOf<double>(3, 2.5) << "\n";    // you can also specify the type
    return 0;
}
```

The compiler makes a function for each type you use.

### Class templates

```cpp
template <typename T>
class Box {
private:
    T value;

public:
    Box(T v) : value(v) {}
    T get() const { return value; }
};

Box<int> b1(5);                 // a Box that holds an int
Box<string> b2("hello");        // a Box that holds a string
```

The `vector<int>` in Chapter 9 is also a class template like this.

## Exception handling

A problem that happens while the program runs (an index out of range, a file that cannot be opened and so on) is called an **exception**. You throw an exception with `throw`, and catch exceptions that happen inside `try` with `catch`.

```cpp
#include <iostream>
#include <stdexcept>
using namespace std;

double divide(int a, int b)
{
    if (b == 0) {
        throw invalid_argument("cannot divide by 0");   // throw an exception
    }
    return static_cast<double>(a) / b;
}

int main()
{
    try {
        cout << divide(10, 4) << "\n";     // 2.5
        cout << divide(10, 0) << "\n";     // the exception happens here
        cout << "this line is not run\n";
    } catch (const invalid_argument& e) {
        cout << "Error: " << e.what() << "\n";
    }
    cout << "continuing\n";
    return 0;
}
```

```text
2.5
Error: cannot divide by 0
continuing
```

- When an exception happens, the rest of the processing is skipped and control moves to a matching `catch`
- `catch (const exception& e)` catches all standard exceptions. `catch (...)` catches anything
- If there is no `catch` anywhere to receive it, the program stops
- `vector`'s `at()` throws `out_of_range` when you go out of range

## The standard library (STL)

The containers and tools you use often are all in the standard library. Before making your own, look here first.

| Name | Header | What it is |
| --- | --- | --- |
| `string` | `<string>` | Strings |
| `vector` | `<vector>` | Arrays whose size can change |
| `map` | `<map>` | Key–value pairs (close to Python's dict) |
| `sort`, `find`, `max_element` | `<algorithm>` | Sorting, searching, finding the largest |
| `unique_ptr` | `<memory>` | A pointer that is deleted automatically |

```cpp
#include <map>

map<string, int> milk;          // cow's name → milk yield
milk["Hanako"] = 32;
milk["Momo"] = 28;
for (const auto& [name, kg] : milk) {        // C++17
    cout << name << ": " << kg << " kg\n";   // printed in order of name
}
```

## Summary

- Overload operators with `operator+` and the like. When the left side is not your class, make it a function outside (`friend`)
- Change types with converting constructors and conversion functions. Stop unwanted conversions with `explicit`
- Combine functions and classes that differ only in type with `template <typename T>`
- Throw with `throw`, and catch with `try` / `catch`
- For containers and tools, use the standard library first (`string`, `vector`, `map`, `algorithm`)

## Exercises

```quiz
Q: How do you write one function or class for many types (`??? <typename T>`)?
A: template
E: For example `template <typename T> T max2(T a, T b)`.

Q: Which keyword throws an exception?
A: throw
E: Catch it with `try` / `catch`.

Q: What does this code print?
| try {
|     throw runtime_error("no milk");
| } catch (const exception& e) {
|     cout << e.what();
| }
A: no milk
E: `what()` returns the message stored in the exception.

Q: Which keyword on a constructor stops unwanted automatic type conversion?
A: explicit
E: It stops a converting constructor being used without you noticing.
```
