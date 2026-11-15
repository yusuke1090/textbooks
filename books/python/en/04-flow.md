# 4. Branching and loops

## What you will learn

- if, elif, else and indentation
- for, with range, enumerate and zip
- while, break and continue

## The if statement

```python
milk = 32.5

if milk >= 35:
    print("very high")
elif milk >= 25:
    print("normal")
else:
    print("low")
print("done")
```

- Put a `:` (colon) after the condition
- **Indent** the statements inside (usually 4 spaces). Everything at the same indentation is one block. If the indentation does not line up, you get an `IndentationError`
- Conditions are checked from the top, and only the first one that matches is run

### Choosing a value in one line

```python
label = "high" if milk >= 30 else "low"
```

### Values treated as false

You can also write values that are not true/false in an `if` condition. `0`, `0.0`, `""` (an empty string), `[]`, `{}` and `None` are treated as false, and everything else as true.

```python
names = []
if not names:
    print("there are no cows yet")
```

## The for statement

It takes out the contents of a container one at a time.

```python
for m in [32.5, 28.0, 35.2]:
    print(m)
```

### range

Use it to loop a fixed number of times.

| How to write it | Numbers you get |
| --- | --- |
| `range(5)` | 0, 1, 2, 3, 4 |
| `range(1, 6)` | 1, 2, 3, 4, 5 |
| `range(0, 10, 2)` | 0, 2, 4, 6, 8 |
| `range(5, 0, -1)` | 5, 4, 3, 2, 1 |

```python
for i in range(1, 10):
    for j in range(1, 10):
        print(i * j, end="\t")     # end gives a tab instead of a newline
    print()                        # newline (a times table)
```

### enumerate and zip

```python
names = ["Hanako", "Momo", "Sakura"]
milk = [32.5, 28.0, 35.2]

for i, name in enumerate(names, start=1):    # with numbers
    print(i, name)

for name, m in zip(names, milk):             # two side by side
    print(f"{name}: {m}kg")
```

When you want numbers, `enumerate` is more Pythonic than writing `for i in range(len(names)):`.

## The while statement

It repeats while the condition is true.

```python
total = 0
while True:
    s = input("milk (empty to finish): ")
    if s == "":
        break               # end the loop
    total += float(s)
print("total", total)
```

## break and continue

| Statement | What it does |
| --- | --- |
| `break` | Ends the loop immediately |
| `continue` | Skips the rest of this round and goes to the next |

```python
for n in range(1, 11):
    if n == 7:
        break
    if n % 2 == 0:
        continue
    print(n)          # 1 3 5
```

If it never stops, press **Ctrl + C** in the terminal.

## The match statement

You can use it to branch many ways on one value (from Python 3.10).

```python
command = "start"
match command:
    case "start":
        print("starting")
    case "stop" | "quit":
        print("stopping")
    case _:
        print("unknown")            # when nothing matches
```

## Summary

- After `if condition:`, indent. Branch with `elif` and `else`
- `for x in container:`. For a number of times use `range`, for numbers use `enumerate`, to go side by side use `zip`
- `while` repeats while the condition holds. `break` ends it, `continue` goes to the next round

## Exercises

```quiz
Q: What does this code print?
| print(list(range(1, 10, 3)))
A: [1, 4, 7] | 1, 4, 7
E: Start at 1, step by 3, stop before 10.

Q: What does this code print?
| total = 0
| for i in range(5):
|     if i == 3:
|         continue
|     total += i
| print(total)
A: 7
E: 0 + 1 + 2 + 4 = 7. `continue` skips only 3.

Q: Which function gives you the index and the value together in a `for` loop?
A: enumerate | enumerate()
E: To loop over two containers side by side, use `zip`.

Q: Which statement ends a loop right there?
A: break
E: `continue` skips just the current turn.
```
