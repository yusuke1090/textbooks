# 8. Pointers and references

## What you will learn

- Addresses and pointers (`&` and `*`)
- Using pointers as arguments to change the caller's variables
- References and pass by reference

## Addresses

A variable is stored somewhere in memory. The number of that place is called its **address**. Putting `&` (the **address-of operator**) in front of a variable gives you its address.

```cpp
int a = 5;
cout << "The value of a is " << a << ".\n";
cout << "The address of a is " << &a << ".\n";   // a hexadecimal number like 0x7ffd...
```

The address may change each time you run the program.

## Pointers

A variable that holds an address is called a **pointer**.

```cpp
int a = 5;
int* pA;          // declare pA, a pointer to int (also written int *pA;)
pA = &a;          // put in the address of a (pA points to a)

cout << pA << "\n";     // the address of a
cout << *pA << "\n";    // 5 (the value pA points to)

*pA = 50;               // put 50 where it points
cout << a << "\n";      // 50 (a changes)
```

| How to write it | Meaning |
| --- | --- |
| `int* p;` | The `*` in a declaration means "pointer type" |
| `&a` | The address of a (address-of operator) |
| `*p` | The value p points to (the **dereference operator**) |

- To show that it points to nothing, use `nullptr` (`int* p = nullptr;`)
- Using `*` on an uninitialized pointer or on `nullptr` crashes the program

## Using pointers as arguments

The `swap` in Chapter 7 swapped copies, so the caller's variables did not change. If you pass the **addresses**, you can change the caller's variables.

```cpp
void swap(int* pX, int* pY)
{
    int tmp = *pX;    // keep the value it points to
    *pX = *pY;
    *pY = tmp;
}

int main()
{
    int num1 = 5, num2 = 10;
    swap(&num1, &num2);                     // pass the addresses
    cout << num1 << " " << num2 << "\n";    // 10 5 (swapped)
    return 0;
}
```

## References

A **reference** is "another name" for a variable. Add `&` when declaring it, and always initialize it.

```cpp
int a = 5;
int& rA = a;      // rA is another name for a
rA = 50;
cout << a << "\n";    // 50
```

- The `&` in a declaration means "reference type", while `&a` in an expression means "address". Same symbol, different meanings
- Once set, a reference cannot be changed to be another name for a different variable

### Pass by reference

If you make the arguments references, you can change the caller's variables without writing `*` or `&` (**pass by reference**).

```cpp
void swap(int& x, int& y)
{
    int tmp = x;
    x = y;
    y = tmp;
}

int main()
{
    int num1 = 5, num2 = 10;
    swap(num1, num2);                       // pass them as they are
    cout << num1 << " " << num2 << "\n";    // 10 5
    return 0;
}
```

### const references

Passing large data (strings or structs) by value takes time to copy. If you do not change it, passing it as a `const` reference avoids the copy and also prevents it from being changed.

```cpp
void show(const string& name)     // no copy. Changing name inside is an error
{
    cout << name << "\n";
}
```

## When to use pointers and when to use references

| | Pointer | Reference |
| --- | --- | --- |
| Pointing to nothing | Can be `nullptr` | Not possible (always another name for something) |
| Changing what it points to | Possible | Not possible |
| How to write it | Needs `*p`, `&a` | The same as a normal variable |
| Main uses | Arrays (Chapter 9), dynamic memory (Chapter 10) | Function arguments (especially `const` references) |

## Summary

- `&a` gives the address, `int* p = &a;` makes a pointer, and `*p` is the value it points to
- If you pass an address or a reference, a function can change the caller's variables
- Pass large arguments you do not change as `const Type&`

## Exercises

```quiz
Q: How do you get the address of variable a?
A: &a
E: With `int* p = &a;`, p is a pointer to a.

Q: What does this code print?
| int a = 3;
| int* p = &a;
| *p = 8;
| cout << a;
A: 8
E: `*p` is what p points to, which is a itself.

Q: What does this program print?
| void twice(int& x) { x = x * 2; }
| int main() {
|     int a = 5;
|     twice(a);
|     cout << a;
| }
A: 10
E: It is passed by reference (`int&`), so the caller's a changes.

Q: How do you pass a large argument that will not change without copying it (for a `string`)?
A: const string& | const std::string& | const string &
E: `const Type&` avoids the copy and prevents changes.
```
