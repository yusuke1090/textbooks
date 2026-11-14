# 4. Operators

## What you will learn

- The four arithmetic operations, and a caution about integer division
- Assignment operators and increments
- Comparison and logical operators, and precedence
- Converting types (casts)

## Expressions and operators

Something that combines values and symbols, like `a + 5`, is called an **expression**. `+` is called an **operator**, and `a` and `5` are called **operands**.

## Arithmetic operators

| Operator | Meaning | Example (`a = 7`, `b = 2`) |
| --- | --- | --- |
| `+` | Add | `a + b` → 9 |
| `-` | Subtract | `a - b` → 5 |
| `*` | Multiply | `a * b` → 14 |
| `/` | Divide | `a / b` → **3** (integer by integer drops the decimal part) |
| `%` | Remainder | `a % b` → 1 |

> When you divide an integer by an integer, everything after the decimal point is thrown away. `7 / 2` is 3, and `7.0 / 2` is 3.5.

## Assignment operators

You can write a calculation and an assignment together.

| How to write it | Same meaning |
| --- | --- |
| `x += 10` | `x = x + 10` |
| `x -= 10` | `x = x - 10` |
| `x *= 10` | `x = x * 10` |
| `x /= 10` | `x = x / 10` |
| `x %= 10` | `x = x % 10` |

```cpp
int x = 30;
x -= 10;
cout << x << "\n";     // 20
```

## Increment and decrement

`++` adds 1 and `--` subtracts 1. Whether you put them before or after changes the value of the expression.

```cpp
int a = 1;
int b = ++a;   // prefix: increase first, then use → a is 2, b is 2
int c = 1;
int d = c++;   // postfix: use first, then increase → c is 2, d is 1
```

When a line has only `++` (`a++;`), either way is the same.

## Comparison operators and logical operators

The result of a comparison is `true` (correct) or `false` (not correct). These are used for branching in Chapter 5.

| Operator | Meaning |
| --- | --- |
| `==` | Equal (careful: `=` is assignment) |
| `!=` | Not equal |
| `>`, `>=` | Greater than, greater than or equal |
| `<`, `<=` | Less than, less than or equal |
| `&&` | And (true if both are true) |
| `\|\|` | Or (true if either is true) |
| `!` | Not (swaps true and false) |

```cpp
int score = 75;
bool pass = (score >= 60) && (score <= 100);   // true
```

## Precedence

As in arithmetic, `*` and `/` are calculated before `+` and `-`. Here are the main ones, in the order they are calculated.

| Order | Operators |
| --- | --- |
| 1 | `++` `--` (postfix), `()` (function call) |
| 2 | `++` `--` (prefix), `!`, `-` (sign), `sizeof` |
| 3 | `*` `/` `%` |
| 4 | `+` `-` |
| 5 | `<<` `>>` |
| 6 | `<` `<=` `>` `>=` |
| 7 | `==` `!=` |
| 8 | `&&` |
| 9 | `\|\|` |
| 10 | `?:` (Chapter 5) |
| 11 | Assignments such as `=` and `+=` |

When in doubt, add `( )`. It also makes the code easier to read.

## Type conversion

### Automatic conversion

When you calculate with values of different types, they are converted to the larger type first (`int + double` is `double`). If you put a larger type into a smaller type, the part that does not fit is lost.

```cpp
double d = 3.9;
int i = d;        // 3 (the decimal part is thrown away)
```

### Casts

Changing a type by specifying it yourself is called a **cast**.

```cpp
int sum = 7, n = 2;
cout << sum / n << "\n";                          // 3
cout << static_cast<double>(sum) / n << "\n";     // 3.5
cout << (double)sum / n << "\n";                  // 3.5 (the old way)
```

## Summary

- `+ - * / %`. Integer `/` integer drops the decimal part
- `x -= 10` is `x = x - 10`. With `++`, prefix and postfix give different expression values
- Equal is `==`. `&&` (and), `||` (or), `!` (not)
- To calculate with decimals, cast with `static_cast<double>(...)`
