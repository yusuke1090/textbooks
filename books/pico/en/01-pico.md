# 1. What is the Raspberry Pi Pico?

## What you will learn

- What a microcontroller is, and how it differs from a PC
- The features and types of the Raspberry Pi Pico
- The names of the parts of the board (BOOT, USR and RST buttons and more)
- How to enter flashing mode (BOOTSEL)
- Ways to write programs for the Pico (C/C++ and MicroPython) and when to use each
- Words that come up often in this guide

## What is a microcontroller?

A **microcontroller** (MCU) is a small computer with a CPU, memory and input/output circuits on a single chip.
It runs inside many machines around you: microwaves, air conditioners, rice cookers, cars, toys and more.

For example, a rice cooker's microcontroller measures the temperature of the pot with a temperature sensor and turns the heater on and off to cook the rice.
Repeating "**measure with a sensor → think → move something**" like this is a microcontroller's job.

The big differences from a PC are as follows.

| | PC | Microcontroller |
| --- | --- | --- |
| OS | Windows, Linux and so on | None (only your one program runs) |
| Memory | Several GB and up | A few hundred KB (tens of thousands of times less than a PC) |
| Time from power-on to running | Tens of seconds | An instant |
| Power consumption | Tens of watts | Around 0.1 W (runs for days on batteries) |
| Size and price | Large; tens of thousands of yen and up | About the size of a finger; a few hundred yen and up |
| What it is good at | Screens, the internet, heavy computation | Reading sensors, controlling motors and LEDs |

With no OS, your program runs as soon as the power is turned on, and it can run on batteries for a long time.
On the other hand, you cannot log in with SSH or run several apps at the same time.

## What is the Raspberry Pi Pico?

The **Raspberry Pi Pico** is a microcontroller board made by the Raspberry Pi Foundation. It costs around 1,000 yen.
It has "Raspberry Pi" in its name, but it is different from the Raspberry Pi that runs Linux (the Pi 4 or 5); it is a microcontroller.

The chip at its center is the **RP2040**.

| Item | Details | In short |
| --- | --- | --- |
| CPU | Dual-core ARM Cortex-M0+ at 133 MHz | Two brains. About 100 million calculations a second |
| Memory (SRAM) | 264 KB | A workspace used only while running |
| Flash (storage) | 2 MB on the official Pico (some compatible boards have 16 MB) | A file store that keeps its contents with the power off |
| Input/output pins (GPIO) | 26 | Legs for connecting sensors and LEDs |
| Analog inputs (ADC) | 3 (12-bit) | Legs that can read voltage as a number |
| Communication | I2C ×2, SPI ×2, UART ×2, USB | Ways to talk with sensors and the PC |
| Other | PIO, a built-in temperature sensor | Input/output circuits you can design freely, and more |

![Raspberry Pi Pico (RP2040)](images/pico-board.jpg)

### Types of Pico

| Name | Features |
| --- | --- |
| Pico | The basic model |
| Pico H | A Pico with pin headers (legs for plugging into a breadboard) already attached |
| Pico W / Pico WH | With WiFi and Bluetooth |
| Pico 2 / Pico 2 W | Faster models with more memory, using the new RP2350 chip |
| Compatible boards | Made by other companies. Many have USB Type-C, buttons and an RGB LED |

The way you write programs is almost the same, so everything in this guide works on any of them.

![Pico 2](images/pico2.jpg)

![Pico WH (left: front, right: back; with pin headers)](images/pico-wh.jpg)

## The parts of the board

This is an example of a compatible board with USB Type-C. On the official Pico, the only button is BOOT, and the USB connector is micro-B.

![The parts of a compatible board](images/en/board-buttons.svg)

| Part | Description |
| --- | --- |
| **USB connector** | Connects to the PC; used for both power and data |
| **BOOT button** | Starting up while holding it puts the board in flashing mode (BOOTSEL) |
| **RST button** | Press it to restart the Pico |
| **USR button** | A button you can use freely in your own program |
| **LED** | A small lamp you can turn on and off from your program |
| **RGB LED** | An LED that mixes red, green and blue to light in many colors |
| **RP2040** | The brain of the board (the microcontroller chip) |
| **Pins** | 20 on each side, 40 in total. Connect sensors and other parts (explained in Chapter 7) |

## The three buttons (BOOT, USR, RST)

| Button | Name | Role |
| --- | --- | --- |
| **BOOT** | Boot button (BOOTSEL) | Starting up while holding it enters flashing mode, and the PC sees the board as a USB drive called "RPI-RP2". Copying a .uf2 file to it flashes the program |
| **USR** | User button | A button you can use freely in your own program. On many boards it is connected to **GP24** (0 when pressed, 1 when released). Chapter 6 explains how to read it |
| **RST** | Reset button | Press it to restart the Pico. The same as unplugging and replugging USB. The flashed program starts again from the beginning |

### Entering flashing mode (BOOTSEL)

You use this when flashing a program. VS Code's Run Project (USB) normally puts the board into flashing mode automatically, but when it cannot (when the board is brand new, when MicroPython is on it and so on), enter it by hand (Chapter 3). There are two ways.

![Two ways to enter flashing mode](images/en/bootsel-steps.svg)

- **Method A (works on any board)**: hold BOOT while plugging in USB, and let go once it is connected
- **Method B (boards with RST)**: with USB connected, hold BOOT, press and release RST, then release BOOT

If it worked, Pico Studio's connection check shows **BOOTSEL mode** (the figure in Chapter 5).

### Common operations

| What you want to do | How |
| --- | --- |
| Restart the program from the beginning | Press RST once |
| Enter flashing mode | Method A or Method B above |
| It has stopped and does not respond | Press RST. If that does not help, enter flashing mode and flash the program again (Appendix B) |

> Pressing BOOT or RST does not erase the flashed program.
> It is erased only when you flash another program, or flash flash_nuke.uf2 (Appendix B).

## Ways to write programs

There are two main ways to write programs for the Pico. **This guide uses C/C++.**

### C/C++ (Pico SDK) (the method used in this guide)

Write in C/C++ using the official Raspberry Pi **Pico SDK**.

- 10–100 times faster than MicroPython
- You decide how memory is used, so it is easier to make it run stably for a long time
- After writing, you build it (convert it to machine code) and flash the `.uf2` file to the Pico. With the VS Code extension, this is done with buttons (Chapter 3)
- The flashed program runs automatically when the power is turned on

### MicroPython

A small version of Python for microcontrollers.

- No build needed; code you write runs right away
- You can try one line at a time in the REPL (interactive mode)
- It is slow and uses a lot of memory, so it is not suited to products

In this guide, Appendix E explains how to use it as a tool for quickly checking wiring and sensors.

### When to use which

| | C/C++ | MicroPython |
| --- | --- | --- |
| Making a product | **Suited** | Not suited |
| Speed | Fast | Slow |
| Battery life | Can be long (fine control of power-saving features; Chapter 15) | Shorter |
| Reliability | You can plan memory use, so it is easier to run stably for a long time | Can stop because of things like running out of memory |
| Flashing | Just flash one `.uf2` (easy for mass production) | Install MicroPython, then put `.py` files on it |
| Trying things | Building and flashing take about 10 seconds | Runs immediately. One line at a time in the REPL |

> If you know C++, there is also **arduino-pico**, which lets you write in the Arduino style (links in Appendix D). This guide uses the official Pico SDK.

## Words that come up often

| Word | Meaning |
| --- | --- |
| Pico SDK | The official Raspberry Pi collection of C/C++ parts. Contains functions to operate GPIO, I2C and more |
| Build | Turning a C++ program into machine code the Pico can run (`.uf2`) |
| Firmware | A program flashed to the Pico. Your own C++ program and MicroPython are both firmware |
| .uf2 file | The firmware file flashed to the Pico. Made by building. You can also flash it by copying it to a Pico in flashing mode |
| BOOTSEL (flashing mode) | A mode for flashing firmware. The Pico looks like a USB drive |
| GPIO | Pins that your program can set to 0 / 1 or read |
| Flash | Storage that keeps its contents when the power is off. The program goes here (2 MB) |
| RAM (memory) | A workspace used only while the program runs. Erased when the power is turned off |
| Port | The window the PC uses to communicate with the Pico. On Linux, `/dev/ttyACM0` and the like. `printf` output also arrives here |

## Summary

- A microcontroller is a small computer without an OS, good at controlling sensors and LEDs
- The Raspberry Pi Pico is a microcontroller board with an RP2040. Different types are written in almost the same way
- BOOT is for flashing mode, RST restarts, and USR is a button for your own use
- This guide uses C/C++ (Pico SDK). MicroPython is for quick tests (Appendix E)

## Exercises

```quiz
Q: What is the name of the microcontroller chip on the Raspberry Pi Pico?
A: RP2040
E: Different Pico boards are programmed in almost the same way.

Q: Which button do you hold while plugging in to put the Pico in programming mode?
A: BOOT | BOOTSEL
E: RST restarts; USR is a button for your own use.

Q: Which language does this guide use for product programs?
A: C++ | C/C++ | cpp
E: It uses the Pico SDK. MicroPython is for quick tests.

Q: A PC has something a microcontroller lacks, such as Windows or Linux. What is it?
A: OS | operating system
E: A microcontroller is a small computer without an OS, good at controlling sensors and LEDs.
```
