# 1. Running a program

## What you will learn

- The steps until a program runs (source code → compile → run)
- Getting ready to write and run C++ on Ubuntu with VS Code
- Running your first program

This textbook is based on my [study notes](https://note.com/k_1090/n/n9ca36fcc9a8a) on *やさしいC++ 第5版* (*Easy C++, 5th edition*, by Mana Takahashi, SB Creative). Mistakes in the notes have been fixed, and a few ways of writing that are common in today's C++ (`std::string`, `std::vector` and others) have been added.

## Until a program runs

All a computer understands directly is sequences of 0s and 1s (**machine code**). You write C++ text that people can read (**source code**), turn it into machine code, and then run it.

| Step | What you do | What you get |
| --- | --- | --- |
| 1 | Write the source code in an editor | A source file (`hello.cpp`) |
| 2 | Turn it into machine code with a **compiler** (compiling) | An object file (`hello.o`) |
| 3 | Connect it with the parts (libraries) it uses, with a **linker** (linking) | An executable file (`hello`; `hello.exe` on Windows) |
| 4 | Run it | The result appears on screen |

Steps 2 and 3 are usually done together with one command (`g++`). This whole process is called **building**.

> Python reads and runs what you write each time (an interpreter). C++ turns it into machine code in advance, so it runs fast. On the other hand, every time you change it, you have to compile again.

## Getting ready (Ubuntu and VS Code)

### Installing the compiler

```bash
sudo apt update
sudo apt install g++
g++ --version          # OK if it shows a version
```

### Opening VS Code

1. Make a folder for studying and open it in VS Code

   ```bash
   mkdir -p ~/apps/cpp-study
   cd ~/apps/cpp-study
   code .
   ```

2. In Extensions on the left (the icon of four squares), install "C/C++" (Microsoft). You get syntax colors, completion and red underlines for errors
3. Press **Ctrl + `** (backquote) to open the terminal at the bottom. Compile and run here

## Your first program

In VS Code, create `hello.cpp`, write the following and save it (Ctrl + S).

```cpp
#include <iostream>
using namespace std;

int main()
{
    cout << "Welcome to C++!\n";
    return 0;
}
```

Compile it in the terminal, then run it.

```bash
g++ -std=c++17 -Wall -o hello hello.cpp
./hello
```

```text
Welcome to C++!
```

| Part | Meaning |
| --- | --- |
| `g++` | The C++ compiler |
| `-std=c++17` | Compile with the rules of C++17 |
| `-Wall` | Warn about code that is easy to get wrong (always add it) |
| `-o hello` | The name of the executable to make (without it, `a.out`) |
| `./hello` | Run `hello` in the current folder (`./`) |

## When you get an error

If compiling fails, you get the file name, line number and reason.

```text
hello.cpp:6:28: error: expected ';' before 'return'
```

- It means a `;` is missing around **line 6, character 28** of `hello.cpp`
- The real mistake is often on that line or on **the line before it**
- If you get many errors, fix them **from the top**. Fixing one often makes the others go away
- A `warning` still compiles, but it is a source of bugs. Fix those too

## With Visual Studio (Windows)

The original book uses Visual Studio on Windows.

1. Choose "Create a new project" → "Empty Project"
2. In Solution Explorer, right-click "Source Files" → "Add" → "New Item" → "C++ File"
3. Write the code, and press **Ctrl + F5** (Start Without Debugging) to compile and run in one go

## Summary

- Compile and link the source code to make an executable, then run it
- On Ubuntu, compile with `g++ -std=c++17 -Wall -o name file.cpp` and run with `./name`
- For errors, look at the line number and fix from the top
