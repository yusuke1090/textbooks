# 0. How to use this guide

## What you will learn

- What you will be able to do with this guide
- The roles of the three tools used for development (VS Code, Pico Studio, the terminal)
- The order in which to read it
- How to read the guide (code labels, word explanations, sticky notes, highlights and notes)

## About this guide

This guide covers the steps for using a Raspberry Pi Pico to build a device that reads sensors, makes judgments and sends data (for example, a cow collar), **all the way to a product**.
The product's program is written in **C++** and developed in **VS Code**.

![A map of this guide](images/en/guide-map.svg)

| Part | Contents |
| --- | --- |
| Part 1: Getting ready | About the Pico, the development environment, how to develop in VS Code, checking with Pico Studio |
| Part 2: Basics | Wiring and reading LEDs, buttons, pins and sensors |
| Part 3: Going deeper with C++ | C++ for microcontrollers, interrupts, recording data, machine learning, power saving |
| Part 4: Making a product | The real development flow, testing, debugging, preparing for mass production |
| Appendix | Working with commands, troubleshooting, comparing with the Raspberry Pi, links, MicroPython |

## The roles of the three tools

| Tool | Role | Chapters |
| --- | --- | --- |
| **VS Code** (the "Raspberry Pi Pico" extension) | **The center of development.** Write, build, flash to the Pico and debug C++ | Chapters 3–4, and everything from Chapter 6 on |
| **Pico Studio** | **A tool for checking.** See whether the Pico is connected, what is running on it and whether the development environment is complete. See `printf` output. Open this guide with "📚 ガイド" in the upper right | Chapter 5 |
| Terminal | When doing the same things with commands, or putting them into scripts | Appendix A |

Normally you **write and flash in VS Code, and check the connection in Pico Studio when something does not work**.
Pico Studio also lets you quickly try MicroPython code (Appendix E). It is handy when you want to check that your wiring and sensors are right before writing C++.

## The order to read in

| Who | Order |
| --- | --- |
| Beginners | Chapters 0 → 1 → 2 → 3 → 5 → 6 in order. Then 7 → 8 → 9 to be able to read sensors |
| People with C++ or embedded experience | Set up the environment with Chapters 2–3, then only the chapters you need |
| People at the product stage | Chapters 11, 12, 15, 16, 17 |
| When something does not work | Appendix B "Troubleshooting" |

## How to read the guide

### Code labels

The label above each piece of code tells you where it is used.

| Label | Meaning | How to use it |
| --- | --- | --- |
| C++ program (paste into the .cpp of your VS Code project) | One complete program that runs on the Pico | "Copy" it, paste it into the `.cpp` of your VS Code project, then Compile → Run (Chapter 3) |
| C++ code (excerpt) | Part of a program, for explanation | It cannot be built as is. Read it to learn how to use things |
| CMakeLists.txt | Build settings | Write it in your project's `CMakeLists.txt` |
| Python on the PC | Python run in the PC's terminal (Chapters 13–14) | Save it to a file and run `python3 filename` |
| MicroPython (try it in Pico Studio) | MicroPython you can try right away in Pico Studio (Appendix E) | "Copy" it, paste it into Pico Studio's code box → "▶ 実行" (Run) |
| No label | Commands or example output | Read it. Type commands in the terminal |

### Looking up the meaning of words

**Click** a function or argument name in the code (`gpio_put`, `i2c_write_blocking` and so on) or a word in a command (`cmake`, `picotool` and so on) **to see its meaning in a speech bubble**. Clicking a header name such as `cstdio` in `#include <cstdio>` shows what kind of header it is (the C++ standard library, the Pico SDK, or one you make yourself) and the functions in it.

![Clicking an argument](images/studio-tip.png)

- The bubble disappears when you click somewhere else or press Esc
- Nothing appears for words without an explanation. Explanations can be added to `books/pico/glossary.json` (and `glossary-en.json` for English) in the textbook repository

### The guide's screen

Read this guide on [the textbook site](https://yusuke1090.github.io/textbooks/?b=pico) (it also works on a phone; you can open it from "📚 ガイド" in the upper right of Pico Studio too).

| Action | What happens |
| --- | --- |
| Tap the chapter name at the top | The table of contents opens, grouped by part. ▶ to the left of a chapter opens its headings |
| ◀ ▶ | Go to the previous or next chapter |
| Tap a figure | Shows it large (on a phone you can scroll sideways or pinch to zoom) |
| `#ch=9` in the address | Opens that chapter directly (the number is its order in the table of contents) |
| 🔖 | Opens the list of sticky notes, highlights and notes (explained below) |

When you open it again, it shows the chapter you were reading, at the place you were reading.

### Adding sticky notes, highlights and notes

Like a paper book or a PDF, you can mark how far you have read and what is important.

| What you want to do | How |
| --- | --- |
| Highlight something important | Select text → press a color (yellow, pink, green, blue) on the buttons that appear |
| Write a note | Select text → **📝 メモ** (note) → write (saved automatically). A 📝 appears after the highlight, and hovering over the highlight shows the note |
| Put a marker where you stopped reading | Select text → **📌 付箋** (sticky note). Or 🔖 → **今見ている所に付箋を貼る** (put a sticky note where I am now). You can write on it, like "read up to here" or "try from here" |
| Change the color or delete | Tap the highlight or sticky note → press a color, or 🗑 |
| Find in the list and jump | Press 🔖. Items are listed by chapter; tap one to jump there. ✕ deletes it |

- Chapters with sticky notes also show 📌 in the table of contents (next to the chapter name)
- You can highlight inside code too. Clicking a word inside a highlight still shows its explanation
- Sticky notes, highlights and notes are saved in the browser you are using (iPhone and PC are separate)
- Even if the guide's text is changed later, they stay in the same place as long as the selected text remains. Ones whose text has changed and cannot be found are shown in the list as "場所が見つかりません" (location not found)


## Summary

- The product's program is written in C++ and developed in VS Code
- Pico Studio is a tool for checking the connection and the development environment. You can also try MicroPython quickly
- Beginners should read Chapters 0–6 in order. If you get stuck, see Appendix B
- Code labels tell you how to use the code. Click a word to see its meaning
- Select text to add highlights, notes and sticky notes. Open the list with 🔖
