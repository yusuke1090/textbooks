# 14. Extending classes (inheritance and virtual functions)

## What you will learn

- Inheritance (making a new class that adds features to an existing one)
- protected, and how to call the base class's constructor
- Overriding and virtual functions
- Abstract classes

## Inheritance

Making a new class with added members based on an existing class is called **inheritance**.

| Term | Meaning | Example |
| --- | --- | --- |
| Base class (parent class) | The original class | `Car` |
| Derived class (child class) | The class made by inheriting | `RacingCar` |

A derived class inherits the members of the base class and adds its own.

```cpp
class Car {
protected:                     // usable from derived classes
    int num;
    double gas;

public:
    Car(int n, double g) : num(n), gas(g) {}
    virtual ~Car() {}
    virtual void show() const
    {
        cout << "The number is " << num << ", and the gas is " << gas << ".\n";
    }
};

class RacingCar : public Car { // inherit from Car
private:
    int course;                // an added member

public:
    RacingCar(int n, double g, int c) : Car(n, g), course(c) {}
    void show() const override // override the base class's show
    {
        cout << "The racing car's number is " << num << ", the gas is " << gas
             << ", and the course number is " << course << ".\n";
    }
};
```

### Access specifiers

| Specifier | The class itself | Derived classes | Outside |
| --- | --- | --- | --- |
| `public` | ○ | ○ | ○ |
| `protected` | ○ | ○ | × |
| `private` | ○ | × | × |

The `public` in `class RacingCar : public Car` means the base class's public members stay public in the derived class. You normally inherit with `public`.

### The base class's constructor

When you make an object of a derived class, **the base class's constructor** is called first. You choose which one to call in the initializer list (`: Car(n, g)`). If you do not, the base class's constructor with no arguments is called. Destructors are called in the reverse order (derived → base).

## Overriding

Redefining, in a derived class, a member function with **the same name and the same arguments** as in the base class is called **overriding**.

> Making a function with the same name but **different arguments** is overloading (Chapter 7). The names are similar, but they are different things.

If you add `override`, you get an error when the base class has no such function (when you got the name or arguments wrong).

## Virtual functions

A pointer (or reference) to the base class can point to an object of a derived class. When you call a function through that pointer:

- For a normal function, the function of **the pointer's type** (the base class) is called
- For a **virtual function** marked `virtual`, the function of **the actual object** (the derived class) is called

```cpp
int main()
{
    Car* cars[2];
    cars[0] = new Car(1234, 20.5);
    cars[1] = new RacingCar(4567, 30.0, 5);

    for (Car* c : cars) {
        c->show();     // each class's own show is called
    }
    for (Car* c : cars) {
        delete c;
    }
    return 0;
}
```

```text
The number is 1234, and the gas is 20.5.
The racing car's number is 4567, the gas is 30, and the course number is 5.
```

Behaving differently for each object with the same call is called **polymorphism**. You can put many kinds of things together in one array and treat them the same way.

> So that the derived class's destructor is also called when you `delete` through a base class pointer, add `virtual` to the destructor of classes meant to be inherited (`virtual ~Car() {}`).

## Abstract classes

A virtual function marked `= 0` is called a **pure virtual function**. It has no body, and derived classes must override it. A class with a pure virtual function is called an **abstract class**, and you cannot make objects of it. It is used to state only the rule "you must have this function".

```cpp
class Vehicle {
public:
    virtual void show() const = 0;   // pure virtual function
    virtual ~Vehicle() {}
};

class Bike : public Vehicle {
public:
    void show() const override { cout << "This is a bicycle.\n"; }
};

// Vehicle v;     // error (you cannot make an object of an abstract class)
Bike b;           // OK
```

## Multiple inheritance

In C++, you can inherit from two or more classes (`class C : public A, public B`). It gets complicated — for example, members with the same name become ambiguous — so use it only to add abstract classes (classes that are just rules).

## Summary

- Inherit with `class Derived : public Base`. Call the base class's constructor in the initializer list
- Members you want derived classes to use are `protected`
- Add `override` when overriding, and `virtual` to the base class's function
- With virtual functions, the derived class's function is called through a base class pointer. Make the destructor `virtual` too
- An abstract class with an `= 0` pure virtual function cannot have objects

## Exercises

```quiz
Q: Which access specifier lets derived classes use a member but not outside code?
A: protected
E: `private` members cannot be used even by derived classes.

Q: What does this program print?
| class Animal {
| public:
|     virtual void cry() { cout << "..."; }
|     virtual ~Animal() {}
| };
| class Cow : public Animal {
| public:
|     void cry() override { cout << "moo"; }
| };
| int main() {
|     Animal* p = new Cow;
|     p->cry();
|     delete p;
| }
A: moo
E: Because it is virtual, the derived class's function is called through a base pointer.

Q: What is a class with a pure virtual function (`= 0`), which cannot be made into objects, called?
A: abstract class | abstract
E: Use it through derived classes that define the function.

Q: Which keyword do you add when a derived class replaces a base class function?
A: override
E: The base class function needs `virtual`.
```
