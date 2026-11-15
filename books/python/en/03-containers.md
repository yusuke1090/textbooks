# 3. Containers for data (lists, tuples, dictionaries and sets)

## Four containers

| Container | How to write it | Order | Can be changed later | Main use |
| --- | --- | --- | --- | --- |
| List `list` | `[1, 2, 3]` | Yes | Yes | Data in a row |
| Tuple `tuple` | `(1, 2, 3)` | Yes | No | Groups that do not change (coordinates, returning several values from a function) |
| Dictionary `dict` | `{"a": 1, "b": 2}` | Order of insertion | Yes | Looking up values by name (key) |
| Set `set` | `{1, 2, 3}` | No | Yes | Removing duplicates, quickly checking whether something is included |

## Lists

```python
milk = [32.5, 28.0, 35.2]
milk.append(25.8)        # add to the end → [32.5, 28.0, 35.2, 25.8]
milk.insert(0, 30.0)     # insert at position 0
x = milk.pop()           # take out the last one (25.8)
milk.remove(28.0)        # remove that value
print(len(milk), milk[0], milk[-1], milk[1:3])
print(35.2 in milk)      # True
print(sum(milk), max(milk), min(milk))
```

- Positions (indexes) start from 0. `[-1]` is the last
- A slice `[start:end]` goes up to **just before** the end. `[::2]` is every other one, `[::-1]` is reversed
- Sorting: `milk.sort()` sorts that list itself. `sorted(milk)` returns a new list. For largest first, use `reverse=True`
- Lists can contain lists too (`table = [[1, 2], [3, 4]]`; `table[1][0]` is 3)

### Watch out for pointing to the same thing

```python
a = [1, 2, 3]
b = a            # b points to "the same list" as a (not a copy)
b.append(4)
print(a)         # [1, 2, 3, 4] (a changes too)

c = a.copy()     # make a separate list (a[:] or list(a) does the same)
c.append(5)
print(a)         # [1, 2, 3, 4] (a does not change)
```

## Tuples

```python
point = (35.6, 139.7)     # latitude and longitude
lat, lon = point          # receive them separately (unpacking)
print(lat)
```

Once made, they cannot be changed. If you make things that should not change into tuples, you will not change them by mistake.

## Dictionaries

Pairs of keys (names) and values.

```python
cow = {"name": "Hanako", "parity": 2, "milk": 32.5}
print(cow["name"])               # Hanako
cow["milk"] = 33.0               # change
cow["barn"] = "A"                # add
del cow["parity"]                # delete
print(cow.get("weight"))         # None (no error even if the key is missing)
print(cow.get("weight", 0))      # 0 (you can decide the value when it is missing)
print("name" in cow)             # True (whether the key exists)

for key, value in cow.items():   # keys and values in turn
    print(key, value)
```

- Looking up a missing key with `[ ]`, as in `cow["weight"]`, gives a `KeyError`
- `cow.keys()`, `cow.values()` and `cow.items()` give lists of keys, values and pairs
- A list of dictionaries (`[{"name": ...}, {"name": ...}]`), like a list of cows, is also common. When table data gets large, use pandas (Chapter 9)

## Sets

```python
a = {"A", "B", "C"}
b = {"B", "C", "D"}
print(a | b)       # union: {'A', 'B', 'C', 'D'}
print(a & b)       # intersection: {'B', 'C'}
print(a - b)       # difference: {'A'}
print(set([1, 1, 2, 3, 3]))   # {1, 2, 3} (duplicates removed)
```

An empty set is `set()` (`{}` is an empty dictionary).

## Comprehensions

You can write a `for` that builds a list in one line.

```python
milk = [32.5, 28.0, 35.2, 25.8]
high = [m for m in milk if m >= 30]        # [32.5, 35.2]
lb = [round(m * 2.2046, 1) for m in milk]  # convert to pounds
squares = {n: n ** 2 for n in range(4)}    # dictionaries too: {0: 0, 1: 1, 2: 4, 3: 9}
```

The form is `[expression for variable in container if condition]`. If it gets long and complicated, write a normal `for` (Chapter 4).

## Summary

- A list if it changes, a tuple if it does not, a dictionary to look up by name, a set to remove duplicates
- `b = a` is not a copy; it points to the same thing. Use `a.copy()` to make a separate one
- Look up keys that may be missing safely with `get`
- Comprehensions like `[m for m in milk if m >= 30]` let you write things briefly

## Exercises

```quiz
Q: What does this code print?
| a = [1, 2, 3]
| b = a
| b.append(4)
| print(len(a))
A: 4
E: `b = a` is not a copy; both names point to the same list. Use `a.copy()` to make a separate one.

Q: What does this code print?
| milk = [28, 31, 25, 33]
| print([m for m in milk if m >= 30])
A: [31, 33] | 31, 33
E: The comprehension keeps only values of 30 or more.

Q: What does this code print?
| print(len({3, 1, 3, 2, 1}))
A: 3
E: A set removes duplicates, leaving {1, 2, 3}.

Q: Which dictionary method looks up a key safely, without an error if it is missing?
A: get | .get | get()
E: You can give a default, as in `d.get("key", 0)`.
```
