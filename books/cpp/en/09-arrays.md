# 9. Arrays and strings

## Arrays

A row of boxes that hold values of the same type together is called an **array**.

```cpp
int test[5] = {80, 60, 22, 50, 75};    // an array holding 5 ints

for (int i = 0; i < 5; i++) {
    cout << "Person " << i + 1 << "'s score is " << test[i] << ".\n";
}
```

- Each box is called an **element**, and the number inside `[ ]` is called the **index**
- Indexes start **from 0**. For the array `test[5]`, you can use `test[0]` to `test[4]`
- Using something out of range (`test[5]`) still compiles, but it damages other memory and causes strange behavior or crashes
- You can get the number of elements with `sizeof(test) / sizeof(test[0])` (size of the whole array ÷ size of one element)

### Sorting (bubble sort)

It repeatedly compares neighbors and moves the larger one back.

```cpp
const int NUM = 5;
int test[NUM] = {80, 60, 22, 50, 75};

for (int s = 0; s < NUM - 1; s++) {
    for (int t = s + 1; t < NUM; t++) {
        if (test[t] > test[s]) {        // largest first
            int tmp = test[t];
            test[t] = test[s];
            test[s] = tmp;
        }
    }
}
// test is {80, 75, 60, 50, 22}
```

Normally, use `std::sort` from the standard library (`#include <algorithm>`).

```cpp
sort(test, test + NUM);                       // smallest first
sort(test, test + NUM, greater<int>());       // largest first
```

## Multidimensional arrays

```cpp
int score[2][3] = {
    {80, 60, 22},     // 3 subjects for person 1
    {50, 75, 90},     // 3 subjects for person 2
};
cout << score[1][2] << "\n";    // 90
```

## Arrays and pointers

The name of an array can be used as **the address of its first element**.

```cpp
int test[5] = {80, 60, 22, 50, 75};
int* p = test;            // the same as &test[0]

cout << *p << "\n";       // 80
cout << *(p + 1) << "\n"; // 60 (p + 1 is the address of the next element)
cout << p[2] << "\n";     // 22 (you can use [ ] with pointers too)
```

`p + 1` moves the address forward not by 1 byte but by **one element** (4 bytes for an int).

### Passing an array to a function

When you pass an array as an argument, the address of its first element is passed. The function cannot know the number of elements, so pass it too.

```cpp
double avg(const int t[], int n)     // the same as const int* t
{
    int sum = 0;
    for (int i = 0; i < n; i++) sum += t[i];
    return static_cast<double>(sum) / n;
}

avg(test, 5);    // 57.4
```

Because an address is passed, without `const` the function could change the caller's array.

## Strings

### char arrays (C strings)

In the style that comes from C, a string is an array of `char` with an end mark `'\0'` at the end.

```cpp
char str[] = "Hello";    // room for 6 characters: 'H' 'e' 'l' 'l' 'o' '\0'
cout << str << "\n";
cout << strlen(str) << "\n";     // 5 ('\0' is not counted; #include <cstring>)
```

- Length is `strlen`, copying is `strcpy`, joining is `strcat` and comparing is `strcmp`
- Writing beyond the size of the array damages memory. You cannot assign with `=` or compare with `==`

### std::string (use this in today's C++)

With `std::string` from `#include <string>`, you do not have to worry about length, and you can treat it like a normal value.

```cpp
#include <string>

string name = "Taro";
string msg = "Hello, " + name;       // join with +
cout << msg << " (" << msg.size() << " characters)\n";   // Hello, Taro (11 characters)
if (name == "Taro") cout << "They are the same\n";   // you can compare with ==

string line;
getline(cin, line);                  // read one line, including spaces
```

## std::vector (an array whose size can change)

`std::vector` from `#include <vector>` is an array you can add elements to later.

```cpp
#include <vector>

vector<int> test = {80, 60, 22};
test.push_back(50);                  // add to the end
cout << test.size() << "\n";         // 4
for (int t : test) cout << t << " "; // 80 60 22 50
```

If you take out an element with `at`, as in `test.at(10)`, going out of range is reported as an error (an exception, Chapter 15).

## Summary

- Array indexes start from 0. Do not go out of range
- An array name is the address of the first element. Pass it to functions together with the number of elements
- Using `std::string` for strings and `std::vector` for arrays whose size changes is safe and easy

## Exercises

```quiz
Q: What is the index of the last element of `int a[5];`?
A: 4
E: Indexes start at 0, so they are 0–4.

Q: What does this code print?
| int a[] = {4, 7, 1, 9};
| int m = a[0];
| for (int x : a) if (x > m) m = x;
| cout << m;
A: 9
E: A range-based for loop finds the largest value.

Q: What does this code print?
| vector<int> v = {1, 2, 3};
| v.push_back(4);
| cout << v.size();
A: 4
E: `push_back` adds one at the end.

Q: Which standard library type should you use for strings in modern C++?
A: std::string | string
E: It is safer and easier than a char array (C string).
```
