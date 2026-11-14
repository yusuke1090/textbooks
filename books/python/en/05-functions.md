# 5. Functions

## What you will learn

- How to make functions (def and return)
- Ways to pass arguments (positional, keyword, default, variable-length)
- Scope, type hints and lambda

## Making a function

```python
def average(values):
    """Return the mean of a list of numbers."""   # the function's description (docstring)
    return sum(values) / len(values)

print(average([32.5, 28.0, 35.5]))     # 32.0
```

- Make it with `def name(arguments):`, and indent the inside
- `return value` returns a value and ends the function. Without `return`, it returns `None`
- The `"""…"""` on the first line is the function's description (it appears when you hover over the function in VS Code)

### Returning several values

```python
def min_max(values):
    return min(values), max(values)    # returned as a tuple

low, high = min_max([32.5, 28.0, 35.2])
```

## Arguments

```python
def greet(name, greeting="Hello"):       # greeting has a default value
    print(f"{greeting}, {name}")

greet("Taro")                         # Hello, Taro
greet("Taro", "Good morning")          # passed by position
greet(greeting="Good evening", name="Taro")   # passed by keyword (name). Any order
```

- Arguments with default values go **after** those without
- For functions with many arguments, passing by keyword is easier to read

> Do not use something changeable, like a list, as a default value. If you write `def add(x, items=[]):`, **the same list** is reused every time you call it. Use `items=None` and, inside the function, `if items is None: items = []`.

### Taking any number of arguments

```python
def total(*values):            # receive positional arguments as a tuple
    return sum(values)

def show(**info):              # receive keyword arguments as a dictionary
    for k, v in info.items():
        print(k, v)

total(1, 2, 3)                 # 6
show(name="Hanako", milk=32.5)
```

### Changing what you passed in

If you pass a list or dictionary and change its contents inside the function, the caller's one changes too (because they point to the same thing; Chapter 3).

```python
def add_cow(herd, name):
    herd.append(name)

herd = ["Hanako"]
add_cow(herd, "Momo")
print(herd)          # ['Hanako', 'Momo']
```

## Scope

Variables made inside a function can only be used inside the function (**local variables**). Variables outside the function (**global variables**) can be read, but assigning to one makes a new local variable.

```python
count = 0

def bad():
    count = 10         # a new local variable (the outer count stays 0)

def good(count):
    return count + 1   # receive it as an argument and give it back as the return value

count = good(count)    # 1
```

Writing `global count` lets you change the outer variable, but then it is hard to see where it changed, so pass values through arguments and return values.

## Type hints

You can write the types of arguments and the return value. They do not change how the code runs, but VS Code uses them to complete your typing and point out mistakes.

```python
def average(values: list[float]) -> float:
    return sum(values) / len(values)
```

## lambda (small unnamed functions)

`lambda arguments: expression` makes a small function on the spot. It is often used to pass the key for sorting.

```python
cows = [{"name": "Hanako", "milk": 32.5}, {"name": "Momo", "milk": 28.0}]
cows_sorted = sorted(cows, key=lambda c: c["milk"], reverse=True)   # highest milk first
print([c["name"] for c in cows_sorted])    # ['Hanako', 'Momo']
```

## Summary

- `def name(arguments):` and `return`. Write a docstring description first
- Arguments can be passed by position or keyword. Do not use `[]` as a default value
- Variables inside a function are local. Pass values through arguments and return values
- Type hints make code easier to read. Set the sort key with `sorted(..., key=lambda x: ...)`
