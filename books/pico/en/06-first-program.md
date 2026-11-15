# 6. Your first programs

## What you will learn

- Running your first C++ programs and learning to read them
- Sending results to the PC with `printf`
- Blinking LEDs ("blinky"): the board's LED, an external LED and an RGB LED
- Reading a button
- How to stop a flashed program, and what happens at power-on

This assumes you have created a VS Code project and flashed the blinking LED in Chapter 3.
For every program in this chapter, "Copy" it, replace the contents of the `.cpp` in your VS Code project, and try it with **Compile Project → Run Project (USB)**. View the output in Serial Monitor or Pico Studio (Chapter 3).

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

Connect an LED and a resistor on a breadboard and blink it in the same way. Do the wiring **with USB unplugged**.

![How to connect an external LED](images/en/led-circuit.svg)

1. Unplug USB
2. Connect the Pico's **GP15 (pin 20)** to a resistor (220 Ω–1 kΩ)
3. Connect the other end of the resistor to the LED's **long leg (+)**
4. Connect the LED's **short leg (−)** to the Pico's **GND (pin 18)**
5. Plug in USB and flash the program below

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

If it does not light, check the LED's direction (the long leg on the GP15 side) and the pin number (physical pin 20 = GP15).
How to read pin numbers is explained in Chapter 7, and how to use a breadboard in Chapter 8.

### RGB LED (only on boards that have one)

On a compatible board with an RGB LED, you can make it light in different colors.

Use `ws2812.h`, which comes with Pico Studio. Inside, it uses PIO (the Pico's freely programmable input/output circuits) to make the signal for the RGB LED.

1. Copy `ws2812.h` into your project folder (`cp ~/apps/pico-studio/cpp/include/ws2812.h ~/apps/blink/`)
2. Add `hardware_pio` and `hardware_clocks` to `target_link_libraries` in `CMakeLists.txt` (Chapter 4)
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
For an external button, connect one side of the button to a GPIO (for example GP14) and the other side to GND, and change `24` in the code to `14`.

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

`gpio_pull_up` is a setting that uses a resistor inside the Pico to fix the value at 1 when nothing is connected (explained with a figure in Chapter 7).
`condition ? A : B` is a way of writing "A if the condition is true, otherwise B".

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
