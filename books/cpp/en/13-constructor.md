# 13. Constructors and static members

## What you will learn

- Constructors (initialization when an object is made) and destructors (cleanup when it disappears)
- Overloading constructors, and initializer lists
- Arrays of objects
- Static members (shared by all objects)

## Constructors

A function that is called automatically when an object is made. It is used to initialize members.

- Its name is the same as the class name
- You do not write a return type (not even `void`)

```cpp
class Car {
private:
    int num;
    double gas;

public:
    Car();                     // constructor with no arguments
    Car(int n, double g);      // constructor with arguments (overloading)
    void show() const;
};

Car::Car() : num(0), gas(0.0)  // after : comes the initializer list
{
    cout << "Made a car.\n";
}

Car::Car(int n, double g) : num(n), gas(g)
{
    cout << "Made a car with number " << num << " and gas " << gas << ".\n";
}

void Car::show() const
{
    cout << "The number is " << num << ", and the gas is " << gas << ".\n";
}

int main()
{
    Car car1;                 // the constructor with no arguments is called
    Car car2(1234, 20.5);     // the constructor with arguments is called
    car1.show();
    car2.show();
    return 0;
}
```

- The types and number of arguments decide which constructor is called (the same as overloading in Chapter 7)
- An **initializer list** (`: num(n), gas(g)`) puts values into members as they are created. This is more common than assigning inside the block. `const` members and reference members can only be given values in the initializer list
- If you write no constructor at all, a do-nothing constructor with no arguments is made automatically. If you write even one with arguments, the one without arguments is not made (`Car car1;` becomes an error)
- You can also combine them into one with default arguments, as in `Car(int n = 0, double g = 0.0);`

## Destructors

A function that is called automatically when an object disappears. It is used for cleanup, such as giving back borrowed memory.

- Its name is `~ClassName`. It has no arguments and no return value

```cpp
class Car {
public:
    Car()  { cout << "Made\n"; }
    ~Car() { cout << "Cleaned up\n"; }
};

int main()
{
    Car car1;           // Made
    {
        Car car2;       // Made
    }                   // leaving the block, car2 disappears: Cleaned up
    return 0;
}                       // car1 disappears: Cleaned up
```

## Arrays of objects

```cpp
Car cars[3];                          // the constructor with no arguments is called 3 times
Car cars2[2] = {Car(1234, 20.5), Car(4567, 30.0)};
cars2[1].show();
```

## Static members

Normal member variables are separate for each object. A member with `static` is **one single thing shared by all objects**. It is data attached to the class itself.

```cpp
class Car {
private:
    int num;
    double gas;

public:
    static int sum;                  // static member variable: the number of cars made
    Car(int n, double g);
    static void showSum();           // static member function
};

int Car::sum = 0;                    // static member variables are defined outside the class

Car::Car(int n, double g) : num(n), gas(g)
{
    sum++;                           // add 1 every time a car is made
}

void Car::showSum()
{
    cout << "There are " << sum << " cars in total.\n";
}

int main()
{
    Car::showSum();                  // There are 0 cars in total.
    Car car1(1234, 20.5);
    Car::showSum();                  // There are 1 cars in total.
    Car car2(4567, 30.0);
    Car::showSum();                  // There are 2 cars in total.
    return 0;
}
```

- Static members can be used with `ClassName::name` without making an object
- Inside a static member function, you cannot use normal members (`num`, `gas`) (because it is not known which object they would belong to)
- From C++17, if you write `inline static int sum = 0;` inside the class, the definition outside is not needed

## The this pointer

Inside a member function, `this` is a pointer to **the object the function was called on**. It is used, for example, when an argument and a member have the same name.

```cpp
void Car::setNum(int num)
{
    this->num = num;      // the left is the member, the right is the argument
}
```

## Summary

- A constructor has the same name as the class and no return value. Initialize members with an initializer list
- A destructor is `~ClassName`. It cleans up when the object disappears
- `static` members are shared by all objects and used with `ClassName::name`
- `this` is a pointer to the object itself

## Exercises

```quiz
Q: What is the function that cleans up when an object is destroyed called?
A: destructor
E: Its name is `~ClassName`.

Q: What does this program print?
| class A {
| public:
|     A() { cout << "1"; }
|     ~A() { cout << "2"; }
| };
| int main() {
|     A a;
|     cout << "3";
| }
A: 132 | 1 3 2
E: The constructor runs on creation (1), and the destructor at the end of main (2).

Q: Which keyword makes a member shared by all objects?
A: static
E: Use it as `ClassName::name`.

Q: Inside a member function, what pointer points to the object itself?
A: this
E: For example `this->x`.
```
