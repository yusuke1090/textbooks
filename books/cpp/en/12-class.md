# 12. Class basics

## What you will learn

- Classes and objects (instances)
- Member variables and member functions
- public and private (encapsulation)

## What is a class?

A **class** is a type that bundles data (**member variables**) with the features that use that data (**member functions**). For a "Car" class, the license number and the amount of gasoline are the data, and "show" and "refuel" are the features.

The way of building programs with classes is called **object-oriented programming**.

## Declaring a class

```cpp
class Car {
public:
    int num;           // member variables
    double gas;

    void show();       // declaration of a member function
};                     // do not forget the final ;

// definition of the member function (with ClassName::)
void Car::show()
{
    cout << "The number is " << num << ".\n";
    cout << "The gas is " << gas << ".\n";
}
```

- The `::` in `Car::show` means "show of the Car class"
- Inside a member function, you can use the same object's member variables directly (`num`, `gas`)

## Making objects

A class is a "blueprint". A concrete thing made from the blueprint is called an **object** (an **instance**). You can make many objects from one class.

```cpp
int main()
{
    Car car1;              // make car1, an object of the Car class
    car1.num = 1234;
    car1.gas = 25.5;
    car1.show();           // call a member function

    Car car2;              // another object (its data is separate from car1)
    car2.num = 4567;
    car2.gas = 30.0;
    car2.show();
    return 0;
}
```

## public and private

You can decide whether members can be used from outside.

| Specifier | Where it can be used |
| --- | --- |
| `public` | Anywhere |
| `private` | Only inside the class's member functions (an error from outside) |

The usual way is to make the data `private` so it can only be changed through `public` member functions (**encapsulation**). This prevents strange values from getting in.

```cpp
class Car {
private:
    int num;
    double gas;

public:
    void setNumGas(int n, double g);
    void show();
};

void Car::setNumGas(int n, double g)
{
    if (g > 0 && g < 1000) {       // accept only possible values
        num = n;
        gas = g;
        cout << "Set the number to " << num << " and the gas to " << gas << ".\n";
    } else {
        cout << g << " is not a valid amount of gas.\n";
    }
}

void Car::show()
{
    cout << "The number is " << num << ", and the gas is " << gas << ".\n";
}

int main()
{
    Car car1;
    // car1.gas = -10;            // error (it is private, so it cannot be touched from outside)
    car1.setNumGas(1234, 20.5);
    car1.show();
    car1.setNumGas(1234, -10);    // not accepted
    return 0;
}
```

> With `class`, members are `private` if you write nothing; with `struct`, they are `public`. That is the only difference, and you can write member functions in a `struct` too.

## const member functions

Add `const` after member functions that do not change member variables. Then they can also be called on `const` objects, and if you change something by mistake, you get an error.

```cpp
class Car {
    // ...
public:
    double getGas() const { return gas; }    // you can also write the definition inside the class
};
```

## Summary

- A class is a type that bundles data (member variables) and features (member functions). The declaration ends with `};`
- An object is a concrete thing (instance) made from a class. It does not mean the variables inside the class
- Member functions are defined as `ClassName::functionName`
- Data is `private`, and the functions you use are `public` (encapsulation)
