# 8. Your first programs

This assumes you have created a VS Code project and flashed the blinking LED in Chapter 4.
For every program in this chapter, "Copy" it, replace the contents of the `.cpp` in your VS Code project, and try it with **Compile Project → Run Project (USB)**. View the output in Serial Monitor or Pico Studio (Chapter 4).

## How to work in C++

In C++, the flow is always as follows. There is no way to try one line at a time (a REPL) as in MicroPython.

1. Write the whole program
2. Build it (Compile Project)
3. Flash it (Run Project (USB)). The Pico restarts and the program starts running
4. See the result of `printf` (Serial Monitor or Pico Studio)

From the second time on, one build and flash takes about 10 seconds.

## Your first program

```cpp run
#include <cstdio>
#include "pico/stdlib.h"

int main() {
    stdio_init_all();
    sleep_ms(1500);            // wait until the PC can receive output

    printf("hello, pico!\n");

    int total = 0;
    for (int i = 1; i <= 10; i++) {
        total += i;
    }
    printf("Sum of 1 to 10: %d\n", total);

    while (true) {             // keep main() from ending
        sleep_ms(1000);
    }
}
```

Right after flashing, look at the output in Serial Monitor (or "接続" (Connect) in Pico Studio). If you see the following, it worked.

```text
hello, pico!
Sum of 1 to 10: 55
```

> If you do not start watching within 1.5 seconds, you miss the first output. If you missed it, press the Pico's RST button or unplug and replug USB to start again from the beginning.

### Reading the code

| Line | Meaning |
| --- | --- |
| `#include <cstdio>` | Loads the parts for using `printf` |
| `#include "pico/stdlib.h"` | Loads the Pico's basic parts (pins, time, USB output and so on) |
| `int main() { ... }` | The program starts from `main` |
| `stdio_init_all();` | Lets `printf` output be sent to the PC over USB |
| `sleep_ms(1500);` | Waits 1.5 seconds. Output right after the Pico restarts would be lost before the PC can receive it |
| `int total = 0;` | Makes a container `total` for an integer (`int`) and puts 0 in it |
| `for (int i = 1; i <= 10; i++) { ... }` | Repeats what is inside `{ }` while changing `i` to 1, 2, …, 10 |
| `printf("...%d\n", total);` | Outputs text. The value of `total` goes where `%d` is. `\n` is a newline |
| `while (true) { ... }` | Repeats forever. If `main` ends, the Pico does nothing |

> In C++, statements need a **`;`** at the end. If you forget it, you get an error when building.
> When there is an error, click it in VS Code's "Problems" panel (Ctrl + Shift + M) to jump to that line. How to read errors is in Appendix B.

| `printf` format | Meaning | Example |
| --- | --- | --- |
| `%d` | Integer | `printf("%d", 55)` → `55` |
| `%.2f` | Decimal (2 decimal places) | `printf("%.2f", 3.14159)` → `3.14` |
| `%s` | String | `printf("%s", "pico")` → `pico` |
| `%02x` | Hexadecimal (2 digits, padded with 0) | `printf("%02x", 104)` → `68` |
| `\n` | Newline | |

### Where `#include` reads files from

The `pico` in `#include "pico/stdlib.h"` is not the board. It is **the name of a folder**. And it is not the Pico that reads it, but the PC when it builds.

The compiler has a list of "folders to search for includes". It adds `pico/stdlib.h` to each one in turn and checks whether the file is there. In a project made with VS Code, it finds this file.

| Part | Contents |
| --- | --- |
| Folder to search (added by the SDK) | `~/.pico-sdk/sdk/2.3.1/src/common/pico_stdlib_headers/include` |
| What you wrote in `#include` | `pico/stdlib.h` |

`2.3.1` is the SDK version. It is set by `sdkVersion` in the `DO NOT EDIT` part of `CMakeLists.txt`.

The line in `CMakeLists.txt` that puts this folder on the list is this one (Chapter 4).

```cmake
target_link_libraries(blink
        pico_stdlib)
```

If you remove `pico_stdlib` and build, it stops with this error. It means the file in line 2, `#include "pico/stdlib.h"`, was not found.

```text
blink.cpp:2:10: fatal error: pico/stdlib.h: No such file or directory
```

`< >` and `" "` search in a different order.

| Form | Search order | Used for |
| --- | --- | --- |
| `#include <cstdio>` | Only the listed folders | What comes with C++ |
| `#include "pico/stdlib.h"` | ① The folder of that `.cpp` → ② the listed folders | The SDK and your own files |

The `#include "ws2812.h"` in the RGB LED example below is found in ①, the project folder.

You can check the listed folders in `build/compile_commands.json` (Chapter 4). Open it in VS Code and search for `pico_stdlib_headers`, and you find `-isystem /home/username/.pico-sdk/sdk/2.3.1/src/common/pico_stdlib_headers/include`. What follows `-I` or `-isystem` is a listed folder.

## Blinking an LED (blinky)

A microcontroller's first step is blinking an LED (blinky).

### The board's LED

On the official Pico, the LED on the board is connected to **GP25**.

```cpp run
#include <cstdio>
#include "pico/stdlib.h"

constexpr uint LED_PIN = 25;      // GP25

int main() {
    stdio_init_all();
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);   // make it an output

    for (int i = 0; i < 10; i++) {
        gpio_put(LED_PIN, true);       // on
        sleep_ms(300);
        gpio_put(LED_PIN, false);      // off
        sleep_ms(300);
    }
    printf("done\n");

    while (true) sleep_ms(1000);
}
```

If the small LED on the board blinks 10 times, it worked.

| Code | Meaning |
| --- | --- |
| `constexpr uint LED_PIN = 25;` | Gives the pin number a name. `constexpr` means "a value that does not change", and `uint` is an unsigned integer |
| `gpio_init(LED_PIN);` | Makes pin 25 usable |
| `gpio_set_dir(LED_PIN, GPIO_OUT);` | Makes pin 25 an "output" |
| `gpio_put(LED_PIN, true);` | Outputs 3.3 V (on). `false` gives 0 V (off) |
| `sleep_ms(300);` | Waits 300 milliseconds (0.3 seconds) |

> On the **Pico W / Pico 2 W**, the LED is connected to the wireless chip, so it is written differently. Choose Pico W as the Board type when creating the project, and write it like this.
>
> - Add `#include "pico/cyw43_arch.h"`
> - Call `cyw43_arch_init();` first
> - Turn it on with `cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, true);`
> - Add `pico_cyw43_arch_none` to `target_link_libraries` in `CMakeLists.txt`
>
> On compatible boards, the LED's pin number may be different. If it does not light, check the board's documentation.

### An external LED

Push an LED and a resistor into a breadboard and blink it in the same way. For the LED and the resistor, you just push the legs into the holes (no soldering). Do the wiring **with USB unplugged**.

You need: a breadboard, 1 LED, 1 resistor (220 Ω–1 kΩ), and 1 jumper wire (male-male)

> The Pico goes into the breadboard by its **pin headers** (the legs sticking out underneath). Just pushing pin headers into the Pico's holes does not connect them. If your Pico has none, solder them on first (Chapter 7, "Attaching pin headers"). The Pico H and Pico WH come with them.

![How to connect an external LED](images/en/led-circuit.svg)

Inside a breadboard, **the 5 holes in the same vertical column** (a–e, f–j) and **each − row (the whole horizontal row)** are connected. Legs pushed into the same column are connected without any wire.

![How to push the parts into the breadboard](images/en/led-breadboard.svg)

1. Unplug USB
2. Push the Pico's **pin headers** in so they straddle the groove in the middle. With USB on the right, the top row starts with **pin 20 (GP15)** at the left end and goes 19, **18 (GND)** … to the right (the bottom row starts with pin 21 at the left end and goes 22, 23 … to the right)
3. Push one leg of the resistor into a free hole in the same column as pin 20. Push the other leg into a free column to the left of the Pico
4. Push the LED's **long leg (+)** into the same column as the resistor. Push the **short leg (−)** into the − row
5. With a jumper wire, connect a free hole in the same column as pin 18 to the − row
6. Plug in USB and flash the program below

![Video: Connecting an external LED to a Raspberry Pi Pico with C/C++ (Dr Jon EA)](https://www.youtube.com/watch?v=gjSK2oaflSM)

**If you have no jumper wire**, move the resistor to the LED's short-leg side. The resistor works the same on either side of the LED. The − row is not used.

![Without a jumper wire](images/en/led-nowire.svg)

- Push the LED's long leg into hole a of the pin 20 (GP15) column, and its short leg into hole a of the column two to the left
- Push one leg of the resistor into hole b of the short leg's column, and the other leg into hole b of the pin 18 (GND) column

```cpp run
#include "pico/stdlib.h"

constexpr uint LED_PIN = 15;      // GP15

int main() {
    stdio_init_all();
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);

    for (int i = 0; i < 20; i++) {
        gpio_put(LED_PIN, !gpio_get(LED_PIN));   // set the opposite of the current state (turn it off if on)
        sleep_ms(200);
    }
    gpio_put(LED_PIN, false);

    while (true) sleep_ms(1000);
}
```

`!` means "the opposite". It reads the current state with `gpio_get` and outputs the opposite value.

If it does not light, check the LED's direction (the long leg on the resistor side), the pin number (physical pin 20 = GP15), and that the legs are pushed all the way into the holes.
How to read pin numbers is explained in Chapter 9.

### RGB LED (only on boards that have one)

On a compatible board with an RGB LED, you can make it light in different colors.

Use `ws2812.h`, which comes with Pico Studio. Inside, it uses PIO (the Pico's freely programmable input/output circuits) to make the signal for the RGB LED.

1. Copy `ws2812.h` into your project folder (`cp ~/apps/pico-studio/cpp/include/ws2812.h ~/apps/blink/`)
2. Add `hardware_pio` and `hardware_clocks` to `target_link_libraries` in `CMakeLists.txt` (Chapter 5)
3. Paste the following program and Compile → Run

```cpp run
#include "pico/stdlib.h"
#include "ws2812.h"

Ws2812 rgb(23);                   // the pin number differs by board (for example 23, 16)

int main() {
    stdio_init_all();
    rgb.begin();
    const uint8_t colors[][3] = {{30, 0, 0}, {0, 30, 0}, {0, 0, 30}, {30, 30, 30}, {0, 0, 0}};
    for (auto& c : colors) {      // repeat, putting each item of colors into c in turn
        rgb.put(c[0], c[1], c[2]);   // red, green, blue, each from 0 to 255
        sleep_ms(500);
    }
    while (true) sleep_ms(1000);
}
```

Bigger numbers make it brighter. It is very bright, so start from around 30.

## Stopping

C++ programs have no "stop" operation. A flashed program keeps running **until you flash a different program**.

- To stop it doing things, flash a program that does nothing (the example below)
- Unplugging USB stops it, but when you plug it in, it starts again from the beginning

```cpp run
#include "pico/stdlib.h"

int main() {
    stdio_init_all();             // keep USB output usable (so the next flash can be done automatically)
    while (true) sleep_ms(1000);  // do nothing
}
```

> **In C++ programs, always call `stdio_init_all()` first.** Even in programs that do not use `printf`.
> If you flash a program that does not call it, the next flash cannot put the Pico into flashing mode automatically. In that case, hold BOOT while reconnecting.

## Running automatically at power-on

**The program you flashed becomes the program that runs when the power is turned on.**

1. Change the "board's LED" code above to repeat with `while (true)` instead of `for`, and flash it
2. Unplug USB and plug it into a USB charger or power bank → the LED starts blinking

The code you wrote stays in your VS Code project folder (`~/apps/blink` and so on). Only the built program (machine code) goes into the Pico.

## Reading a button

Some compatible boards have a user button (**USR**, often **GP24**). Flash the program below and press USR, and it shows "pressed".
You can also try it with an external button (see "An external button" below).

```cpp run
#include <cstdio>
#include "pico/stdlib.h"

constexpr uint BTN_PIN = 24;

int main() {
    stdio_init_all();
    gpio_init(BTN_PIN);
    gpio_set_dir(BTN_PIN, GPIO_IN);
    gpio_pull_up(BTN_PIN);        // 1 when not pressed, 0 when pressed

    while (true) {
        printf("%s\n", gpio_get(BTN_PIN) == 0 ? "pressed" : "-");
        sleep_ms(200);
    }
}
```

`gpio_pull_up` is a setting that uses a resistor inside the Pico to fix the value at 1 when nothing is connected (explained with a figure in Chapter 9).
`condition ? A : B` is a way of writing "A if the condition is true, otherwise B".

### An external button

A button (tactile switch) has four legs, connected in pairs inside. If you use **two diagonal legs**, you cannot get the direction wrong. As with the LED, you just push it into the breadboard.

![How to push the button into the breadboard](images/en/button-breadboard.svg)

1. Unplug USB
2. Push the button into a free spot to the left of the Pico, straddling the groove in the middle
3. With a jumper wire, connect the column of the button's top-left leg to the column of **pin 19 (GP14)**. Pin 19 is second from the left in the top row
4. With a jumper wire, connect the column of the button's bottom-right leg to the column of **pin 23 (GND)**. Pin 23 is third from the left in the bottom row
5. Change `24` to `14` in the program above and flash it. Press the button and "pressed" appears

### Lighting the LED with the button

Combining the two gives "the LED is on only while the button is pressed".

```cpp run
#include "pico/stdlib.h"

constexpr uint LED_PIN = 25;
constexpr uint BTN_PIN = 24;

int main() {
    stdio_init_all();
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    gpio_init(BTN_PIN);
    gpio_set_dir(BTN_PIN, GPIO_IN);
    gpio_pull_up(BTN_PIN);

    while (true) {
        gpio_put(LED_PIN, gpio_get(BTN_PIN) == 0);   // on if pressed (0)
        sleep_ms(10);
    }
}
```

## Try it yourself

Change things little by little and see how the behavior changes.

- Change `sleep_ms(300)` in blinky to `50` or `1000`
- Change `i < 10` to `i < 3`
- Count and show how many times the button was pressed (hint: remember the previous value, and increase the count when it changes from 1 to 0)

## Summary

- Write the whole program and flash it with Compile → Run. See `printf` results in Serial Monitor or Pico Studio
- Call `stdio_init_all()` first. Output right after startup is easy to miss, so wait with `sleep_ms(1500)`
- Handle LEDs and buttons with `gpio_init` → `gpio_set_dir` → `gpio_put` / `gpio_get`
- The flashed program runs as is at power-on. To stop it, flash a different program

## Exercises

```quiz
Q: Which function do you call first so `printf` goes out over USB?
A: stdio_init_all | stdio_init_all()
E: Output right after start-up is easy to miss, so wait with `sleep_ms(1500)`.

Q: `gpio_set_dir` makes a pin an output. Which function sets the pin to 1 or 0?
A: gpio_put
E: Reading uses `gpio_get`.

Q: What code waits 500 milliseconds?
A: sleep_ms(500) | sleep_ms(500);
E: `sleep_ms` waits in milliseconds.

Q: How do you stop a program you wrote to the Pico? Write a different what?
A: program | another program | a different program
E: The program runs every time the Pico powers on.
```
