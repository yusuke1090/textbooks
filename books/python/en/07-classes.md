# 7. Classes

## What you will learn

- Classes and instances, `__init__` and `self`
- Methods, and `__str__`
- Inheritance and `super()`
- dataclass

## What is a class?

A **class** is a type that bundles data (**attributes**) with the functions that use it (**methods**). A concrete thing made from a class is called an **instance** (object).

```python
class Cow:
    def __init__(self, name, parity):     # called when an instance is made
        self.name = name                   # attribute
        self.parity = parity               # number of calvings
        self.records = []                  # milk yield records

    def add_milk(self, kg):                # method
        self.records.append(kg)

    def average(self):
        if not self.records:
            return 0.0
        return sum(self.records) / len(self.records)

hanako = Cow("Hanako", 2)                  # make an instance
hanako.add_milk(32.5)
hanako.add_milk(33.5)
print(hanako.name, hanako.average())       # Hanako 33.0

momo = Cow("Momo", 1)                      # another instance (its data is separate)
```

- `__init__` is called automatically when an instance is made (it corresponds to a C++ constructor)
- The first argument of a method, `self`, is **the instance itself**. You do not write it when calling (`hanako.add_milk(32.5)`)
- What you put in `self.name` becomes an attribute of each instance

## Class variables

A variable written inside the class but outside the methods is shared by all instances.

```python
class Cow:
    count = 0                        # class variable (one for all)

    def __init__(self, name):
        self.name = name             # instance variable (one per cow)
        Cow.count += 1

Cow("Hanako"); Cow("Momo")
print(Cow.count)                     # 2
```

## Special methods

If you write methods of the form `__name__`, you can plug into Python's built-in behavior.

```python
class Cow:
    def __init__(self, name, parity):
        self.name = name
        self.parity = parity

    def __str__(self):                       # how it looks when printed
        return f"{self.name} (parity {self.parity})"

    def __lt__(self, other):                 # compare with < (so sorted works)
        return self.parity < other.parity

cows = [Cow("Hanako", 2), Cow("Momo", 1)]
print(cows[0])                               # Hanako (parity 2)
print([str(c) for c in sorted(cows)])        # ['Momo (parity 1)', 'Hanako (parity 2)']
```

## Inheritance

You can make a new class that adds features to an existing class.

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "…"

class Cow(Animal):                           # inherit from Animal
    def __init__(self, name, parity):
        super().__init__(name)               # call the parent class's __init__
        self.parity = parity

    def speak(self):                         # replace it (override)
        return "Moo"

for a in [Animal("?"), Cow("Hanako", 2)]:
    print(a.name, a.speak())                 # ? …  /  Hanako Moo
```

- `super()` calls the parent class's method
- Writing a method with the same name replaces it. The one from the class of the instance you called it on is used

## Hiding (by agreement)

Python has no mechanism like C++'s `private`. Starting a name with `_` is an agreement meaning "please do not touch this from outside".

## dataclass

For a class that just holds data, adding `@dataclass` automatically creates `__init__`, `__repr__` (display) and comparison with `==`.

```python
from dataclasses import dataclass, field

@dataclass
class Cow:
    name: str
    parity: int = 1
    records: list[float] = field(default_factory=list)   # lists go through field

    def average(self) -> float:
        return sum(self.records) / len(self.records) if self.records else 0.0

c = Cow("Hanako", 2)
print(c)                     # Cow(name='Hanako', parity=2, records=[])
print(c == Cow("Hanako", 2)) # True
```

## Summary

- Inside `class Name:`, write `__init__(self, ...)` and the methods. `self` is the instance itself
- `self.x` belongs to each instance; a variable written directly in the class is shared by all
- `__str__` decides how it is displayed
- Inherit with `class Child(Parent):`, and call the parent's initialization with `super().__init__()`
- For a class that just holds data, use `@dataclass`

## Exercises

```quiz
Q: What is the name of the method called when an instance is created?
A: __init__
E: Write `def __init__(self, ...):`.

Q: What is the first parameter of a method, which refers to the instance itself?
A: self
E: `self.x` is a variable that belongs to each instance.

Q: Which special method decides how an object looks when you `print()` it?
A: __str__
E: It should return a string.

Q: How do you call the parent's initializer inside a child class's `__init__`?
A: super().__init__() | super().__init__ | super()
E: Inherit with `class Child(Parent):`.

Q: Which decorator, starting with `@`, makes a class that just holds data?
A: @dataclass | dataclass
E: It writes `__init__` and more for you.
```
