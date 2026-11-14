# 7. Functions

## What you will learn

- Defining and calling functions, arguments and return values
- Function declarations (prototypes)
- Pass by value, default arguments and overloading

## What is a function?

A bundle of processing steps given a name is called a **function**. You do not have to write the same steps many times, and the program becomes easier to read.

```cpp
#include <iostream>
using namespace std;

// function definition
void buy()
{
    cout << "I bought a car.\n";
}

int main()
{
    buy();          // function call
    cout << "I'll buy one more.\n";
    buy();          // you can call it any number of times
    return 0;
}
```

When you call it, the program goes into the function, and when it finishes, it comes back to where it was called.

## Arguments and return values

| Term | Meaning |
| --- | --- |
| Argument | A value passed to a function. The variable on the definition side is called a **parameter** (formal argument), and the value passed by the caller an **actual argument** |
| Return value | The value a function gives back. Return it with `return value;`. The type of a function that returns nothing is `void` |

```cpp
int sum(int x, int y)      // takes two ints and returns an int
{
    return x + y;
}

int main()
{
    int ans = sum(5, 10);  // 15
    cout << "The total is " << ans << ".\n";
    return 0;
}
```

- When it hits `return`, the function ends there
- There is only one return value. To return many things, use a struct (Chapter 11) or references (Chapter 8)

## Function declarations (prototypes)

A function needs a definition or a **declaration** before it is used. If you want to write the definition after `main`, write just the declaration before it.

```cpp
int sum(int x, int y);     // declaration (prototype). Ends with ;

int main()
{
    cout << sum(5, 10) << "\n";
    return 0;
}

int sum(int x, int y)      // definition
{
    return x + y;
}
```

Declarations are usually collected in a header file (Chapter 10).

## Pass by value

A normal argument receives a **copy** of the value (**pass by value**). Changing the argument inside the function does not change the caller's variable.

```cpp
void swap(int x, int y)
{
    int tmp = x;
    x = y;
    y = tmp;          // swapped x and y... but only the copies
}

int main()
{
    int a = 1, b = 5;
    swap(a, b);
    cout << a << " " << b << "\n";    // 1 5 (not swapped)
    return 0;
}
```

To swap them, use pointers or references (Chapter 8).

## Default arguments

You can set a value to use when an argument is left out. Give default arguments **starting from the last argument**.

```cpp
double area(double width, double height = 1.0)
{
    return width * height;
}

area(3.0, 2.0);    // 6
area(3.0);         // 3 (height is 1.0)
```

## Overloading

If the **types or number** of arguments differ, you can make several functions with the same name (**overloading**).

```cpp
int maxOf(int x, int y)          { return (x > y) ? x : y; }
double maxOf(double x, double y) { return (x > y) ? x : y; }
int maxOf(int x, int y, int z)   { return maxOf(maxOf(x, y), z); }

maxOf(3, 8);         // int version
maxOf(2.5, 1.5);     // double version
maxOf(3, 8, 5);      // version with 3 arguments
```

> Functions that differ **only in their return type** cannot be overloaded (`int f(int)` and `double f(int)` is an error, because the caller cannot decide which one to use).

## Inline functions

Adding `inline` to a function asks the compiler to expand its body at the place where it is called. It is meant to make small functions faster, but today's compilers decide this by themselves even without it.

## Summary

- A function is "return type name(arguments) { processing }". Use `void` when it returns nothing
- It needs a declaration (prototype) before it is used
- Normal arguments are copies (pass by value). Default arguments go from the end
- Overloads must differ in the types or number of arguments. A different return type alone is not enough
