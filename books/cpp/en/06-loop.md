# 6. Loops

## What you will learn

- for statements, while statements and do while statements
- Nesting statements (a times table)
- break and continue

## The for statement

Use it for loops that run a fixed number of times.

```cpp
for (int i = 1; i <= 5; i++) {
    cout << "Loop number " << i << ".\n";
}
cout << "The loop has finished.\n";
```

It works in the order `for (initialization; condition; change)`.

1. Do the initialization (`int i = 1`) once
2. If the condition (`i <= 5`) is true, run the block. If false, finish
3. Do the change (`i++`) and go back to 2

## The while statement

It repeats while the condition is true. Use it when the number of times is not fixed.

```cpp
int num = 0, sum = 0;
cout << "Enter integers (0 to finish)\n";
cin >> num;
while (num != 0) {
    sum += num;
    cin >> num;
}
cout << "The total is " << sum << ".\n";
```

## The do while statement

It runs once first, then checks the condition. It **always runs at least once**.

```cpp
int num = 0;
do {
    cout << "Please enter a number from 1 to 9.\n";
    cin >> num;
} while (num < 1 || num > 9);     // needs a ; at the end
```

## Nesting statements

You can write a loop inside a loop.

```cpp
for (int i = 1; i <= 9; i++) {
    for (int j = 1; j <= 9; j++) {
        cout << i * j << '\t';
    }
    cout << '\n';
}
```

Each time the outer `i` moves forward by one, the inner `j` runs from 1 to 9 (this makes a times table).

## break and continue

| Statement | What it does |
| --- | --- |
| `break` | Ends the loop immediately (only the innermost loop) |
| `continue` | Skips the rest of this round and goes on to the next |

```cpp
for (int i = 1; i <= 10; i++) {
    if (i == 7) break;          // stop when it reaches 7
    if (i % 2 == 0) continue;   // skip even numbers
    cout << i << " ";           // 1 3 5
}
```

## Watch out for infinite loops

If the condition stays true forever, the loop never ends (an **infinite loop**). If it does not stop, press **Ctrl + C** in the terminal to stop it.

```cpp
int i = 0;
while (i < 5) {
    cout << i << "\n";
    // if you forget i++, it keeps printing 0 forever
}
```

## The range-based for statement

You can take out the contents of an array (Chapter 9) or a vector one at a time, in order (from C++11).

```cpp
int test[] = {80, 60, 22, 50, 75};
for (int t : test) {
    cout << t << "\n";
}
```

## Summary

- `for` if the number of times is fixed, `while` if not, `do while` if it must run at least once
- `break` ends the loop, `continue` goes to the next round
- If it will not stop, press Ctrl + C
