# 10. Large programs (scope, dynamic memory, splitting files)

## What you will learn

- Where a variable can be used (scope), and how long it lives (storage duration)
- Dynamic memory (new and delete)
- How to split a program into several files
- Namespaces

## Scope

The range where a variable can be used is called its **scope**.

| Variable | Where it is made | Where it can be used |
| --- | --- | --- |
| Local variable | Inside a function or block `{ }` | Only inside that block |
| Global variable | Outside functions | Anywhere in the file |

```cpp
int a = 0;            // global variable

void func()
{
    int a = 10;       // local variable (separate from the global a)
    cout << a << "\n";       // 10 (the closer one is used)
    cout << ::a << "\n";     // 0 (:: gives the global a)
}
```

- If the names are the same, the inner (local) variable wins. Adding `::` (the **scope resolution operator**) refers to the global one
- Global variables can be changed from anywhere, so mistakes are hard to find. Pass values through arguments and return values where you can

## Storage duration

| Variable | How long it lives |
| --- | --- |
| Local variable | Made when you enter the block, gone when you leave |
| Local variable with `static` | Initialized only once, the first time it is reached, and kept until the program ends |
| Global variable | From the start to the end of the program |

```cpp
void count()
{
    static int n = 0;    // set to 0 only once
    n++;
    cout << "call number " << n << "\n";
}
// count(); count(); count(); → call number 1, 2, 3
```

## Dynamic memory

Normally, the size of an array must be decided at compile time. If you want to decide the size from input after the program starts, borrow memory with `new` (**dynamic memory allocation**).

```cpp
int num = 0;
cout << "How many scores will you enter?\n";
cin >> num;

int* pT = new int[num];          // borrow room for num ints
for (int i = 0; i < num; i++) {
    cin >> pT[i];
}
// ...use it...
delete[] pT;                     // give it back (delete[] for arrays)
```

| Borrow | Give back |
| --- | --- |
| `int* p = new int;` | `delete p;` |
| `int* p = new int[n];` | `delete[] p;` |

- If you forget to give it back, unusable memory piles up (a **memory leak**)
- Using a pointer after giving its memory back causes crashes or strange values

In today's C++, you rarely write `new` and `delete` directly. Use `std::vector` (Chapter 9) for arrays, and `std::unique_ptr` (`#include <memory>`) for single things, and the memory is given back automatically.

```cpp
vector<int> t(num);              // num ints. Given back automatically when you leave the block
auto p = make_unique<int>(5);    // deleted automatically when you leave the block
```

## Splitting into files

Split a large program into files by role.

| File | What to write |
| --- | --- |
| Header file (`.h`) | Function declarations (prototypes), class declarations |
| Source file (`.cpp`) | Function definitions, `main` |

`myfunc.h`:

```cpp
#pragma once           // do not read this header twice (an include guard)

int maxOf(int x, int y);
```

`myfunc.cpp`:

```cpp
#include "myfunc.h"

int maxOf(int x, int y)
{
    return (x > y) ? x : y;
}
```

`main.cpp`:

```cpp
#include <iostream>
#include "myfunc.h"    // your own headers in " " (standard ones in < >)
using namespace std;

int main()
{
    cout << maxOf(3, 8) << "\n";
    return 0;
}
```

When compiling, list all the `.cpp` files (do not write the `.h` files).

```bash
g++ -std=c++17 -Wall -o app main.cpp myfunc.cpp
./app
```

- Instead of `#pragma once`, you can also wrap the header in `#ifndef MYFUNC_H` / `#define MYFUNC_H` / `#endif`
- To use a global variable from another file, declare it with `extern int count;`
- When you have more files, use a build tool such as CMake (the Raspberry Pi Pico development guide also uses it)

## Namespaces

To avoid name clashes, you can put names into a group.

```cpp
namespace farm {
    int count = 0;
    void hello() { cout << "farm's hello\n"; }
}

farm::hello();          // use it as namespace::name
```

The `std` in `std::cout` is also a namespace.

## Summary

- Local variables exist only inside their block. `::` refers to the global one. A `static` local variable keeps its value
- If you borrow with `new`, give it back with `delete` (`delete[]` for arrays). Today, use `vector` or `unique_ptr`
- Declarations go in headers (`.h`), definitions in sources (`.cpp`). Pass all the `.cpp` files to `g++`

## Exercises

```quiz
Q: What does this program print?
| void count() {
|     static int n = 0;
|     n++;
|     cout << n;
| }
| int main() { count(); count(); count(); }
A: 123 | 1 2 3
E: A `static` local variable keeps its value after the function returns.

Q: What do you use to give back memory for an array allocated with `new`?
A: delete[] | delete []
E: For a single object use `delete`. Today, use `vector` or `unique_ptr`.

Q: What extension do header files for declarations use?
A: .h | h | .hpp
E: Definitions go in source files (`.cpp`), and you pass all `.cpp` files to `g++`.

Q: Which symbol in front of a name refers to the global variable?
A: ::
E: `::x` means the global x, not a local with the same name.
```
