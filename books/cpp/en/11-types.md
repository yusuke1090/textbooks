# 11. Making types (typedef, enum, structs)

## typedef and using

You can give a type another name.

```cpp
typedef unsigned long long ID;    // the old way
using Score = int;                // the way since C++11 (same meaning)

ID cowId = 1234567890;
Score s = 80;
```

## Enumerations

A type that gives names to a fixed set of values.

```cpp
enum Week { SUN, MON, TUE, WED, THU, FRI, SAT };   // numbered 0, 1, 2, ... in order

Week w = MON;
if (w == MON) cout << "Monday\n";
```

With `enum class`, the names do not clash with others, and you cannot mistakenly use them as integers (this is recommended today).

```cpp
enum class Color { Red, Green, Blue };

Color c = Color::Red;         // use it with TypeName::
// int n = c;                 // error (it does not turn into an integer by itself)
int n = static_cast<int>(c);  // 0 (cast when you want the number)
```

## Structs

A type that bundles values of different types into one.

```cpp
struct Car {
    int num;         // license number (a member)
    double gas;      // amount of gasoline (a member)
};                   // do not forget the final ;

int main()
{
    Car car1;
    car1.num = 1234;          // use members with . (the dot operator)
    car1.gas = 25.5;

    Car car2 = {4567, 30.0};  // initialize all at once

    cout << "The number is " << car1.num << ", and the gas is " << car1.gas << ".\n";
    cout << "The second car's number is " << car2.num << ".\n";
    return 0;
}
```

- The variables inside a struct are called **members**
- Between the same kind of struct, `car2 = car1;` assigns all members at once

### Passing a struct to a function

Passing by value copies everything, so passing by reference is normal.

```cpp
void show(const Car& c)        // a const reference if you only look at it
{
    cout << c.num << " " << c.gas << "\n";
}

void refuel(Car& c, double amount)    // a reference if you change its contents
{
    c.gas += amount;
}
```

### Pointers to structs

To use a member through a pointer, use `->` (the **arrow operator**).

```cpp
Car car1 = {1234, 25.5};
Car* pCar = &car1;

pCar->gas = 30.0;          // the same as (*pCar).gas = 30.0;
cout << pCar->num << "\n";
```

## Unions

A `union` is a type whose members share the same memory. Only one member can be used at a time. It is sometimes used to save memory (on microcontrollers, for example), but it is not used much day to day.

## Summary

- Give a type a name with `using Alias = Type;`
- For a fixed set of values, use `enum class`
- A struct is `struct Name { members };`. Use members with `.`, or `->` from a pointer
- Pass structs by reference (`const` if you do not change them)
- The class in the next chapter is a struct with "features (functions)" added

## Exercises

```quiz
Q: What is the modern C++ way to give a type another name (`??? Alias = Type;`)?
A: using
E: The old way is `typedef`.

Q: How do you write a type-safe enumeration for a fixed set of values (colors, seasons and so on)?
A: enum class
E: For example `enum class Color { Red, Green };`.

Q: Which operator accesses a member through a pointer to a struct?
A: ->
E: With a normal struct variable, use `.`.
```
