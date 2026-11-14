# 2. Basic grammar

## What you will learn

- The shape of a C++ program (the main function, statements, blocks, comments)
- How to show text and numbers on screen
- How to write characters, strings and numbers (literals), and escape sequences

## The shape of a program

```cpp
#include <iostream>      // makes the screen output feature (cout) available
using namespace std;     // lets you write std::cout as cout

int main()               // the program starts here
{
    cout << "Hello\n";
    cout << "Let's start C++\n";
    return 0;            // finish by returning 0 (meaning it ended normally)
}
```

| Rule | Explanation |
| --- | --- |
| The `main` function | A program always starts from `main`. Only one per program |
| Statement | One unit of processing. **End it with `;`** |
| Block | From `{` to `}`. Groups statements |
| Upper and lower case | They are different. `Main` and `main` are different things |
| Spaces and newlines | Free, except where they separate words. Indent to make code easy to read |

### Comments

Notes for people that the compiler does not read.

```cpp
// a one-line comment (to the end of the line)
/* a comment that
   spans many lines */
```

### using namespace std

`cout` is really `std::cout` (the `cout` inside the namespace called `std`). Writing `using namespace std;` lets you leave out `std::`. It is handy in short programs, but in large programs names can clash, so people often write `std::cout`.

## Showing things on screen (cout)

```cpp
cout << "The total is " << 10 + 5 << ".\n";  // The total is 15.
cout << 3.14 << endl;                       // endl also gives a newline
```

- Use `<<` to chain the things you want to show, in order
- A newline is `"\n"` or `endl`. `endl` also sends the output to the screen immediately (a little slower)

## Literals

Values written directly in a program are called **literals**.

| Kind | How to write it | Examples |
| --- | --- | --- |
| Character literal | One character in `'` | `'A'`, `'1'` |
| String literal | A sequence of characters in `"` | `"Hello"`, `"123"` |
| Integer literal | Decimal, octal (starts with `0`), hexadecimal (starts with `0x`), binary (`0b`) | `10`, `012`, `0xA`, `0b1010` (all are 10) |
| Floating-point literal | Uses a decimal point or exponent | `3.14`, `1.5e3` (1500) |

> `'1'` is a character, `1` is a number and `"1"` is a string; they are all different. Characters that are not 1 byte, such as Japanese, are written as a string like `"あ"`, not `'あ'`.

### Escape sequences

Characters you cannot type directly are written with a `\` in front.

| How to write it | Meaning |
| --- | --- |
| `\n` | Newline |
| `\t` | Tab |
| `\\` | `\` itself |
| `\'` | `'` |
| `\"` | `"` |
| `\0` | The mark for the end of a string (Chapter 9) |

```cpp
cout << "Name\tScore\n";
cout << "Learning \"C++\"\n";   // Learning "C++"
```

## Summary

- A program starts from the `main` function. Statements end with `;`, and blocks are `{ }`
- Show things on screen with `cout << value`. A newline is `"\n"`
- A character is `'A'` and a string is `"ABC"`. Write special characters with escape sequences such as `\n`
