# 6. Modules, files and exceptions

## import

This lets you use functions and other things written in another file.

```python
import math                       # the whole module
print(math.sqrt(2))               # use it as module.name

from math import sqrt, pi         # bring in just the names
print(sqrt(2), pi)

import numpy as np                # give it a short alias (Chapter 8)
```

Do not use `from math import *`, because then you cannot tell where names came from.

### Commonly used standard library modules

These modules come with Python.

| Module | What it can do |
| --- | --- |
| `math` | Square roots, trigonometry, logarithms |
| `random` | Random numbers, picking at random |
| `statistics` | Mean, median, standard deviation |
| `datetime` | Dates and times |
| `pathlib` | Locations of files and folders |
| `csv`, `json` | Reading and writing CSV and JSON |

```python
from datetime import date, timedelta

calving = date(2026, 4, 10)               # the day she calved
print(calving + timedelta(days=280))      # 280 days later
print((date(2026, 11, 14) - calving).days)  # how many days have passed
```

Libraries made by other people are installed with `pip install name` inside a virtual environment (Chapter 1).

## Your own modules

A `.py` file is a module as it is.

`milklib.py`:

```python
def average(values):
    return sum(values) / len(values)

if __name__ == "__main__":
    # runs only when you run this file directly (not when it is imported)
    print(average([1, 2, 3]))
```

`main.py` (in the same folder):

```python
import milklib
print(milklib.average([32.5, 28.0]))
```

If you put test code inside `if __name__ == "__main__":`, it does not run on its own when the file is imported.

## Reading and writing files

```python
# write ("w" creates a new file or overwrites; "a" adds to the end)
with open("memo.txt", "w", encoding="utf-8") as f:
    f.write("Hanako,32.5\n")
    f.write("Momo,28.0\n")

# read
with open("memo.txt", encoding="utf-8") as f:
    for line in f:                       # one line at a time
        name, milk = line.strip().split(",")
        print(name, float(milk))
```

- With `with`, the file is closed automatically when you leave the block
- When the text includes Japanese, add `encoding="utf-8"`
- To read everything at once, use `f.read()`. For working with paths, `pathlib` is handy (`Path("data") / "memo.txt"`)

### CSV and JSON

```python
import csv, json

with open("cows.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "milk"])
    writer.writerow(["Hanako", 32.5])

with open("cows.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):        # each row as a dictionary keyed by the headers
        print(row["name"], row["milk"])  # the values are strings

data = {"name": "Hanako", "milk": [32.5, 33.0]}
with open("cow.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
with open("cow.json", encoding="utf-8") as f:
    print(json.load(f)["milk"])
```

To analyze table data, pandas' `read_csv` (Chapter 9) is easier.

## Exceptions

An error that happens while the program runs is called an **exception**. If you wrap code in `try`, you can catch an exception without stopping the program.

```python
s = input("milk: ")
try:
    milk = float(s)
except ValueError:
    print(f"{s!r} is not a number")
else:
    print(f"recorded {milk}kg")            # when no exception happened
finally:
    print("input finished")                # always, either way
```

- After `except`, write the type of exception to catch. A bare `except:` that catches everything also hides unexpected mistakes
- With `except (ValueError, KeyError) as e:`, you can catch several types and look at the details (`e`)
- To raise an exception yourself: `raise ValueError("milk yield cannot be negative")`

## Common errors

| Error | Meaning | Common causes |
| --- | --- | --- |
| `SyntaxError` | Something is written wrong | A missing `:` or `)`, full-width (Japanese) spaces or symbols |
| `IndentationError` | The indentation is wrong | The number of spaces does not line up, tabs and spaces are mixed |
| `NameError` | That name does not exist | A typo in a variable name, using it before defining it |
| `TypeError` | The types do not match | `"3" + 1` (adding a string and a number), the wrong number of arguments |
| `ValueError` | The value is wrong | `int("abc")` |
| `IndexError` | The position is out of range | `[3]` on a list of length 3 |
| `KeyError` | The dictionary does not have that key | `d["wieght"]` (a typo). Use `get` |
| `AttributeError` | That method or attribute does not exist | Calling `.append` on `None`, a typo |
| `FileNotFoundError` | The file does not exist | The wrong location. Check which folder the terminal is in |
| `ModuleNotFoundError` | The module does not exist | You did not `pip install` it, or VS Code has a different Python selected |
| `ZeroDivisionError` | Divided by 0 | The data is empty, so `len` is 0 |

## Summary

- `import module`, `from module import name`, `import numpy as np`
- Your own `.py` files are modules too. Put test code inside `if __name__ == "__main__":`
- Read and write files with `with open(..., encoding="utf-8") as f:`
- Catch exceptions with `try` / `except Type:`. Use the error's name to work out the cause

## Exercises

```quiz
Q: Which keyword gives a module a short name, like `np` in `import numpy as np`?
A: as
E: `from module import name` imports just one name.

Q: In your own `.py` file, what `if` condition marks code that runs only when the file is run directly?
A: __name__ == "__main__" | __name__ == '__main__' | if __name__ == "__main__":
E: It does not run when another file imports it.

Q: What error do you get when you `open` a file that does not exist?
A: FileNotFoundError
E: Catch it with `try` / `except FileNotFoundError:`.

Q: What does this code print?
| try:
|     n = int("abc")
| except ValueError:
|     n = -1
| print(n)
A: -1
E: "abc" cannot become an integer, so ValueError is raised.
```
