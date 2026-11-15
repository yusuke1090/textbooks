# 3. Variables and types

## What you will learn

- Declaring, assigning and initializing variables
- The kinds of types and their sizes
- How to read input from the keyboard (cin)

## Variables

A box that holds a value is called a **variable**. In C++, before using one, you decide its **type** (the kind of value it holds) and its name (a **declaration**).

```cpp
int num;          // declaration: make a variable num that holds an integer
num = 3;          // assignment: put 3 into num
int count = 10;   // initialization: put in a value when making it
num = count;      // put in the value of another variable (num becomes 10)
```

- `=` does not mean "equals"; it means "put the value on the right into the variable on the left"
- The value of an uninitialized variable is undefined (you cannot know what is in it). Initialize it when you make it

### Rules for names (identifiers)

- You can use letters, digits and `_` (underscore)
- A name cannot start with a digit (`1st` is not allowed; `first1` is fine)
- **Keywords** such as `int` and `return` cannot be used
- Upper and lower case are different (`num` and `Num` are different variables)

## Types

| Type | What it holds | Typical size | Typical range |
| --- | --- | --- | --- |
| `bool` | True/false (`true` / `false`) | 1 byte | |
| `char` | One character (1 byte) | 1 byte | −128 to 127 |
| `short` | Integer | 2 bytes | −32768 to 32767 |
| `int` | Integer (normally use this) | 4 bytes | About ±2.1 billion |
| `long long` | Large integer | 8 bytes | About ±9.2 × 10¹⁸ |
| `float` | Decimal (single precision) | 4 bytes | About 7 significant digits |
| `double` | Decimal (double precision; normally use this) | 8 bytes | About 15 significant digits |

- Adding `unsigned`, as in `unsigned int`, allows only 0 and above, but doubles the positive range
- Sizes can differ between environments. You can check with `sizeof(int)`

```cpp
cout << "int is " << sizeof(int) << " bytes\n";       // int is 4 bytes
```

### const and auto

```cpp
const double PI = 3.14159;   // const: cannot be changed later (trying to gives an error)
auto n = 10;                 // auto: let the compiler decide the type from the value (becomes int)
auto x = 2.5;                // becomes double
```

## Reading input from the keyboard (cin)

```cpp
#include <iostream>
using namespace std;

int main()
{
    int num = 0;
    cout << "Please enter an integer.\n";
    cin >> num;
    cout << num << " was entered.\n";
    return 0;
}
```

- `cin >> variable` puts the value typed on the keyboard into the variable (watch the direction of `>>`; `cout` uses `<<`)
- With `cin >> a >> b;`, you can read two values separated by a space, one after the other

## Summary

- Make a variable with "type name = initial value;". Always initialize it
- Integers are `int`, decimals `double`, true/false `bool`, one character `char`
- Values that do not change are `const`. Read input with `cin >> variable`

## Exercises

```quiz
Q: Which type does this book use for decimal numbers?
A: double
E: Integers are `int`, true/false is `bool`, one character is `char`.

Q: Which keyword before the type makes a value that cannot change?
A: const
E: For example `const int MAX = 100;`.

Q: What reads a value from the keyboard into a variable (`??? >> x;`)?
A: cin
E: Printing to the screen uses `cout`.

Q: Which keyword lets the compiler choose the type from the initial value?
A: auto
E: With `auto x = 3.5;`, x becomes a double.
```
