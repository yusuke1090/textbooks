# Appendix G. Making Christmas lights

Connect ten ordinary LEDs to the Pico and make them blink, light up one by one, fade in and out, and twinkle.
The program is written in C++, written to the Pico from VS Code (Chapter 4), and runs on batteries.

![An LED Christmas tree](images/xmas-tree.jpg)

## What you need

| Item | How many | Notes |
| --- | --- | --- |
| LEDs (5 mm) | 10 | Two each of red, green, yellow, blue and white |
| 330 Ω resistors | 4 | For the red and yellow LEDs |
| 100 Ω resistors | 6 | For the green, blue and white LEDs |
| Breadboard | 1 | 830 holes |
| Jumper wires (male-male) | 11 | Flexible ones, long enough to reach the far LEDs |
| Pin headers | 2 × 20 pins | Often come with the Pico. Soldering is in Chapter 7 |
| USB cable | 1 | One that can carry data. Match the Pico's port (USB-C or micro-USB) |
| Battery box | 1 | 3 × AA, with a switch |
| AA batteries | 3 | Alkaline |

Bought on Amazon Japan, it all comes to about ¥3,000 (November 2026).

![5 mm LEDs](images/leds.jpg)

### Choosing the resistors

| LED colour | Resistor | Bands |
| --- | --- | --- |
| Red, yellow | 330 Ω | orange, orange, brown, gold |
| Green, blue, white | 100 Ω | brown, black, brown, gold |

Red and yellow LEDs light up at a lower voltage, so they get a bigger resistor. That way every colour draws about 4 mA.
All the Pico's GPIO pins together can supply up to 50 mA, so ten LEDs (about 40 mA) can be connected directly.
If in doubt, 330 Ω for all of them is fine too (green, blue and white just get a little dimmer).

![Resistors (the colour bands show the value)](images/resistors.jpg)

## Wiring

![The lights circuit (10 LEDs and a battery)](images/en/xmas-circuit.svg)

- Each of GP0–GP9 gets one resistor and one LED. The short legs of all the LEDs go to GND
- The battery box's red wire (+) goes to **VSYS (pin 39)** and the black wire (−) to GND. VSYS accepts 1.8–5.5 V, so do not use four AA batteries (6 V)

### Laying it out on the breadboard

![Laying it out on the breadboard](images/en/xmas-breadboard.svg)

![Schematic of the lights](images/en/xmas-sch.svg)

1. Make sure the USB cable and the battery are disconnected
2. Put the Pico at the right end with the USB port facing right, straddling the centre groove
3. Put in the ten resistors so they straddle the centre groove. From the left, GP0, GP1 … with two empty columns between them
4. Put each LED's long leg (+) in the column below its resistor, and the short leg (−) in the row with the blue line (−)
5. With jumper wires, connect the Pico's GP0–GP9 columns to the columns above the resistors. GP0 is the leftmost LED
6. Connect the Pico's GND (pin 38) column to the blue-line (−) row with a wire
7. With the battery box switched off, put the red wire in the VSYS (pin 39) column and the black wire in the blue-line (−) row

If the battery box wires end in thin stranded wire, tin them with solder first so they stay in.

## Making the project in VS Code

1. In VS Code, open **New C/C++ Project** from the Raspberry Pi Pico extension (Chapter 4). Name it `xmas`, put it in `~/apps`, and tick **Console over USB** and **Generate C++ code**
2. The brightness uses PWM, so add `hardware_pwm` to `target_link_libraries` in `CMakeLists.txt` (Chapter 5)

```cmake
target_link_libraries(xmas
        pico_stdlib
        hardware_pwm)
```

## Checking the wiring

Connect the USB cable to your PC (leave the battery switched off) and check that each LED lights up in turn. Replace the contents of `xmas.cpp` with this program, then write it with **Compile → Run (USB)**.

```cpp run
#include <cstdio>
#include "pico/stdlib.h"

int main() {
    stdio_init_all();
    sleep_ms(1500);                     // wait for Serial Monitor to connect
    for (uint n = 0; n < 10; n++) {     // make GP0-GP9 outputs
        gpio_init(n);
        gpio_set_dir(n, GPIO_OUT);
    }
    while (true) {
        for (uint n = 0; n < 10; n++) {
            printf("GP%u should be lit\n", n);
            gpio_put(n, 1);
            sleep_ms(1000);
            gpio_put(n, 0);
        }
        printf("round done\n");
    }
}
```

Serial Monitor shows the GP number that should be lit. If an LED does not light up, check which way round it is (long leg on the resistor side) and which column the wire is in.

## The lights program

Replace the contents of `xmas.cpp` with this program, then write it with **Compile → Run (USB)**.

```cpp run
#include <cstdlib>
#include "pico/stdlib.h"
#include "hardware/pwm.h"

constexpr uint PINS[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};   // the GP numbers the LEDs are on (in lighting order)
constexpr int N = sizeof(PINS) / sizeof(PINS[0]);

// set LED number i to a brightness of 0-100
void light(int i, int level) {
    pwm_set_gpio_level(PINS[i], level * level / 10);   // 0-1000. Squaring looks more natural to the eye
}

void all_light(int level) {
    for (int i = 0; i < N; i++) light(i, level);
}

// all blink together
void blink(int times = 10) {
    for (int k = 0; k < times; k++) {
        all_light(100);
        sleep_ms(400);
        all_light(0);
        sleep_ms(400);
    }
}

// light one at a time in turn
void chase(int rounds = 5) {
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < N; i++) {
            all_light(0);
            light(i, 100);
            sleep_ms(100);
        }
    }
    all_light(0);
}

// fade in, then fade out
void fade(int times = 3) {
    for (int k = 0; k < times; k++) {
        for (int level = 0; level <= 100; level += 2) { all_light(level); sleep_ms(20); }
        for (int level = 100; level >= 0; level -= 2) { all_light(level); sleep_ms(20); }
    }
}

// twinkle at random
void twinkle(int seconds = 15) {
    int levels[N] = {};
    absolute_time_t end = make_timeout_time_ms(seconds * 1000);
    while (!time_reached(end)) {
        if (rand() % 100 < 20) levels[rand() % N] = 100;   // about one time in five
        for (int i = 0; i < N; i++) {
            levels[i] = levels[i] * 9 / 10;                // dim a little each time
            light(i, levels[i]);
        }
        sleep_ms(30);
    }
    all_light(0);
}

int main() {
    stdio_init_all();
    for (uint pin : PINS) {
        gpio_set_function(pin, GPIO_FUNC_PWM);         // use the pin for PWM (Chapter 9)
        uint slice = pwm_gpio_to_slice_num(pin);
        pwm_set_clkdiv(slice, 125.0f);                 // 125 MHz / 125 / 1000 = 1 kHz
        pwm_set_wrap(slice, 999);
        pwm_set_enabled(slice, true);
    }
    srand(time_us_32());                               // seed for the random numbers
    while (true) {
        blink();
        chase();
        fade();
        twinkle();
    }
}
```

| Function | How it lights |
| --- | --- |
| `blink()` | All blink together |
| `chase()` | One by one in turn |
| `fade()` | Fade in, then fade out |
| `twinkle()` | Twinkle at random |

- The brightness is set with **PWM** (Chapter 9). The pin switches on and off 1000 times a second, and `pwm_set_gpio_level()` sets how much of the time it is on. With `wrap` at 999, 0 is off and 1000 is brightest
- `light()` squares the 0–100 brightness before turning it into 0–1000. With a straight proportion, the LEDs seem to jump up suddenly at the dim end
- Two GP pins share one PWM circuit (slice), so GP0–GP9 use five slices. Setting the same slice twice does no harm
- The `while (true)` at the end repeats the four patterns in turn (about 35 seconds per round)

### Changing how it lights

| What to change | Where |
| --- | --- |
| The order of the LEDs | The `PINS` list (`{9, 8, 7, 6, 5, 4, 3, 2, 1, 0}` runs backwards) |
| The speed | The milliseconds in `sleep_ms()` |
| How many times | The number in the brackets, as in `blink(20)` |
| The order of the patterns | The lines inside the final `while (true)` |

After a change, write it again with Compile → Run (USB).

## Running on batteries

1. A program written with Run (USB) stays on the Pico and runs by itself when the power comes on
2. Unplug the USB cable and switch on the battery box

> Switch the battery off whenever the USB cable is connected. With both connected, current from USB can flow into the batteries.

Alkaline AA batteries last about 40–50 hours (around 10 days at 4 hours a night).

## Hanging it on the tree

Once every LED lights on the breadboard, take the LEDs off the board, extend them with red-and-black two-core wire and hang them on the branches.
The Pico, resistors and battery stay on the board at the foot of the tree.

![Extending the LEDs with wire and hanging them on the tree](images/en/xmas-hang.svg)

| Item | How many | Notes |
| --- | --- | --- |
| Red-and-black two-core wire (UL2468, 24 AWG) | 20 m | Red for the long leg (+), black for the short leg (−). Available on AliExpress |
| Jumper wires (male-male, 20 cm) | 10 | Cut in half to make 20 wires with a male end. These go into the board |
| Insulating tape | A little | To wrap the soldered joints. Heat-shrink tubing is neater if you have it |
| Wire cutters | 1 | To cut the wire and strip the ends. Scissors will do |

1. Unplug the USB cable and switch off the battery
2. Cut ten jumper wires in the middle. That gives 20 wires with a male end; strip about 5 mm from each cut end
3. Decide which branch each LED goes on, and cut the two-core wire to the distance from the foot of the tree to that branch plus 20 cm. You are splitting 20 m into ten, so keep the average to 2 m or less
4. At both ends, split the red and black apart for about 3 cm, strip about 5 mm and twist the thin strands together
5. At one end, solder a male-ended wire to the red and another to the black
6. Take one LED off the board. Cut the long leg to about 1 cm and solder the red to it, then cut the short leg and solder the black
7. Wrap each joint separately in tape. At the LED end, wrap the two together as well. If the metal parts touch, that LED won't light
8. Put the red wire's male end in the column below the resistor (where that LED's long leg was) and the black wire's in the − row. Doing one LED at a time and putting it back where it came from keeps each colour with the right resistor
9. When all ten are done, switch on the battery and check they all light. If one doesn't, check for a loose joint and that red and black aren't swapped
10. Hang the LEDs on the branches and wind the wire around them. Running the wires near the trunk down to the foot of the tree makes them less visible

## Summary

- Connect each LED through its own resistor to GP0–GP9, and bring all the short legs to GND
- Resistors: 330 Ω for red and yellow, 100 Ω for green, blue and white
- The program is C++. It uses PWM, so add `hardware_pwm` to `CMakeLists.txt`, then write it with Compile → Run (USB)
- Set the brightness with `pwm_set_gpio_level()` (0–1000 in this appendix)
- Once written, the lights come on just by switching on the battery. The battery goes to VSYS (1.8–5.5 V); switch it off when the USB cable is connected
- To hang them on a tree, solder red-and-black two-core wire to the LED legs, with half a jumper wire's male end on the board side. Keep the Pico, resistors and battery at the foot of the tree

## Exercises

```quiz
Q: What resistor value, in Ω, goes with a red LED?
A: 330
E: 330 Ω for red and yellow, 100 Ω for green, blue and white.

Q: What is the name of the Pico pin that the battery box's red wire (+) goes to?
A: VSYS
E: It is pin 39. It accepts 1.8–5.5 V.

Q: Is an LED's long leg plus or minus?
A: plus | + | anode | positive
E: The long leg (+) goes on the resistor side and the short leg (−) on the GND side.

Q: Which library do you add to `target_link_libraries` in `CMakeLists.txt` to use PWM?
A: hardware_pwm
E: Add the library for each feature you use, such as `hardware_adc` for the ADC or `hardware_i2c` for I2C (Chapter 5).

Q: In this appendix's program (`wrap` at 999), what value given to `pwm_set_gpio_level()` makes an LED brightest?
A: 1000 | 999
E: 0 is off, and 1000 (`wrap` + 1) keeps it on all the time.
```
