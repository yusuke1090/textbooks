# 2. Values, variables and strings

## What you will learn

- Numbers, strings and true/false values, and how to calculate
- How to create variables and name them
- Working with strings, and f-strings
- Input and converting types

## Printing to the screen, and comments

```python
print("milk", 32.5, "kg")     # milk 32.5 kg (separating with , adds a space)
print("A", "B", sep="-")      # A-B
# this is a comment (Python does not read it)
```

## Types of values

| Type | Meaning | Examples |
| --- | --- | --- |
| `int` | Integer | `3`, `-10`, `1_000_000` (you can separate digits with `_`) |
| `float` | Decimal number | `3.14`, `1.5e3` (1500.0) |
| `str` | String | `"Hello"`, `'cow'` |
| `bool` | True/false | `True`, `False` |
| `None` | Nothing | `None` |

`type(value)` tells you the type.

```python
print(type(3), type(3.0), type("3"))    # <class 'int'> <class 'float'> <class 'str'>
```

## Calculating

| Operator | Meaning | Example | Result |
| --- | --- | --- | --- |
| `+` `-` `*` | Add, subtract, multiply | `7 * 2` | 14 |
| `/` | Divide (always a decimal) | `7 / 2` | 3.5 |
| `//` | Divide and round down | `7 // 2` | 3 |
| `%` | Remainder | `7 % 2` | 1 |
| `**` | Power | `2 ** 10` | 1024 |

> Decimals are stored as close values in binary, so `0.1 + 0.2` becomes `0.30000000000000004`. When comparing, use `round(x, 2)` or `math.isclose`.

## Variables

```python
milk = 32.5          # create it (assignment). You do not write the type
milk = milk + 1.5    # 34.0
milk += 1.5          # 35.5 (the same as milk = milk + 1.5)
a, b = 1, 2          # two at once
a, b = b, a          # swap (a is 2, b is 1)
```

- Names can use letters, digits and `_` (but cannot start with a digit). Japanese also works, but English letters are normal
- Join words with `_` (`milk_per_day`). Values that do not change are in capitals (`MAX_COWS = 100`)
- Upper and lower case are different

## Strings

```python
s = "Holstein"
print(len(s))         # 8 (length)
print(s[0], s[-1])    # H n (counting from 0; -1 is the last)
print(s[0:4])         # Hols (from 0 up to just before 4; a slice)
print(s[4:])          # tein
print("cow" * 3)      # cowcowcow
print("Hol" + "stein")
```

You cannot change just one character of a string afterwards (`s[0] = "h"` is an error). Make a new string with the change.

| Method | What it does | Example → result |
| --- | --- | --- |
| `upper()` / `lower()` | Upper case / lower case | `"abc".upper()` → `"ABC"` |
| `strip()` | Remove spaces and newlines at both ends | `" a \n".strip()` → `"a"` |
| `split(separator)` | Split into a list | `"a,b,c".split(",")` → `["a", "b", "c"]` |
| `separator.join(list)` | Join | `"-".join(["a", "b"])` → `"a-b"` |
| `replace(old, new)` | Replace | `"2026/11".replace("/", "-")` → `"2026-11"` |
| `startswith(text)` | Whether it starts with | `"cow01".startswith("cow")` → `True` |
| `in` | Whether it contains | `"st" in "Holstein"` → `True` |

### f-strings

Inside `{ }` in `f"..."`, you can put variables and expressions.

```python
name, milk = "Hanako", 32.456
print(f"{name}'s milk yield is {milk} kg")   # Hanako's milk yield is 32.456 kg
print(f"{milk:.1f}")                     # 32.5 (1 decimal place)
print(f"{1234567:,}")                    # 1,234,567
print(f"{0.123:.1%}")                    # 12.3%
print(f"{milk=}")                        # milk=32.456 (handy for checking)
```

## Input and converting types

A value entered with `input()` is always a **string**. Convert it when you calculate.

```python
age = input("How old? ")       # a string like "5"
age = int(age)                  # make it an integer
print(age + 1)
```

| Function | Converts to | Example |
| --- | --- | --- |
| `int()` | Integer | `int("5")` → 5, `int(3.9)` → 3 |
| `float()` | Decimal | `float("3.5")` → 3.5 |
| `str()` | String | `str(10)` → `"10"` |

If it cannot be converted, as in `int("abc")`, you get a `ValueError` (Chapter 6 explains how to catch it).

## Comparison and logic

```python
milk = 32
print(milk >= 30)                    # True
print(25 <= milk < 35)               # True (you can chain them)
print(milk > 30 and milk < 40)       # and
print(milk < 10 or milk > 50)        # or
print(not milk > 30)                 # not
```

Equal is `==`, and not equal is `!=`.

## Summary

- Integer `int`, decimal `float`, string `str`, true/false `bool`. `/` always gives a decimal, `//` rounds down
- Create variables without writing the type. Use `snake_case` for names
- Take parts of strings with `[0]` and `[1:3]`, and work with them using `split`, `join`, `strip` and so on
- Put values into text with f-strings (`f"{x:.1f}"`). `input()` gives a string, so convert it with `int()` and the like

## Exercises

```quiz
Q: What does this code print?
| print(7 // 2)
A: 3
E: `//` is floor division.

Q: What does this code print?
| print(7 / 2)
A: 3.5
E: `/` always gives a float.

Q: What does this code print?
| s = "Holstein"
| print(s[1:3])
A: ol
E: `[1:3]` goes from index 1 up to, but not including, index 3. Indexes start at 0.

Q: What does this code print?
| x = 28.456
| print(f"{x:.1f}")
A: 28.5
E: `:.1f` shows one digit after the decimal point (rounded).

Q: What type is the value you get from `input()`?
A: str | string
E: Convert it with `int()` or `float()` to use it as a number.
```
