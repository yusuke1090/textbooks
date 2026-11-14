# Appendix A. Python and C++ side by side

For people who know Python, this shows how to write the same things in C++.

## Basics

| Task | Python | C++ |
| --- | --- | --- |
| How to run | `python3 a.py` | `g++ -std=c++17 -o a a.cpp` → `./a` |
| Show on screen | `print("x =", x)` | `cout << "x = " << x << "\n";` |
| Input | `n = int(input())` | `int n; cin >> n;` |
| Comment | `# note` | `// note` |
| End of statement | Newline | `;` |
| Block | Indentation | `{ }` |
| Variable | `x = 3` (no type) | `int x = 3;` (with a type; `auto x = 3;` also works) |
| True/false | `True` / `False` | `true` / `false` |
| Nothing | `None` | `nullptr` (for pointers) |
| Integer division | `7 // 2` → 3 | `7 / 2` → 3 |
| Decimal division | `7 / 2` → 3.5 | `7.0 / 2` → 3.5 |
| Power | `2 ** 10` | `pow(2, 10)` (`<cmath>`) |
| And, or, not | `and` `or` `not` | `&&` `\|\|` `!` |

## Flow

| Task | Python | C++ |
| --- | --- | --- |
| Branching | `if a > 0:` / `elif` / `else:` | `if (a > 0) { } else if () { } else { }` |
| Loop a number of times | `for i in range(5):` | `for (int i = 0; i < 5; i++) { }` |
| Go through the contents | `for x in xs:` | `for (auto x : xs) { }` |
| Loop on a condition | `while n != 0:` | `while (n != 0) { }` |
| Choose a value | `a if c else b` | `c ? a : b` |
| Branch many ways | `match` | `switch` / `case 1:` / `break;` |

## Data

| Task | Python | C++ |
| --- | --- | --- |
| String | `s = "abc"` | `string s = "abc";` |
| Length | `len(s)` | `s.size()` |
| List | `xs = [1, 2, 3]` | `vector<int> xs = {1, 2, 3};` |
| Add to the end | `xs.append(4)` | `xs.push_back(4);` |
| Dictionary | `d = {"a": 1}` | `map<string, int> d = {{"a", 1}};` |
| Sort | `xs.sort()` | `sort(xs.begin(), xs.end());` |
| Pair (tuple) | `(1, "a")` | `pair<int, string>(1, "a")`, `tuple` |

## Functions and classes

| Task | Python | C++ |
| --- | --- | --- |
| Function | `def add(x, y): return x + y` | `int add(int x, int y) { return x + y; }` |
| Default argument | `def f(x, y=1):` | `int f(int x, int y = 1)` |
| Class | `class Car:` | `class Car { … };` |
| Initialization | `def __init__(self, n):` | `Car(int n) : num(n) {}` (constructor) |
| The object itself | `self.num` | `this->num` (usually just `num`) |
| Hiding | `_num` (only a convention) | `private:` |
| Inheritance | `class RacingCar(Car):` | `class RacingCar : public Car` |
| Overriding | Define with the same name | `virtual` and `override` |
| Exceptions | `try:` / `except ValueError as e:` / `raise` | `try { } catch (const exception& e) { }` / `throw` |

## Big differences

- **Types**: C++ decides variable types at compile time. Mistakes are found before the program runs
- **Speed**: C++ is turned into machine code before it runs, so it is much faster. It even runs on microcontrollers (Raspberry Pi Pico)
- **Memory**: Python cleans up automatically. In C++, if you `new`, you `delete` (today, make it automatic with `vector` or `unique_ptr`)
- **Arguments**: In Python, passing a list or the like shares its contents. In C++, it is normally a copy (pass by value). To share, use a reference (`&`)
