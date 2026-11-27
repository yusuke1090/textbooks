# 9. Pin and power basics

> For the programs in this chapter, add `hardware_adc` (for ADC) and `hardware_pwm` (for PWM) to `target_link_libraries` in `CMakeLists.txt` before building ("Adding libraries" in Chapter 5).

## Two kinds of numbers

The Pico's pins have two numbers. **They are easy to mix up, so be careful.**

- **Physical pin numbers (1–40)**: numbers for the position, counted counterclockwise from the top left of the board. Used when wiring

- **GP numbers (GP0–GP28)**: numbers used in programs. The 4 in `gpio_init(4)` is this kind

For example, GP4 is physical pin 6. So you "plug the wire into hole 6, and write `gpio_init(4)` in the program".

## Pinout (official Pico)

Viewed from the front, with USB at the top.

![Pinout](images/en/pinout.svg)

- The white numbers are physical pin numbers, and the colored names are GP numbers
- Many compatible boards have the same layout, but check the board's printing or documentation to be sure
- Pin names are often printed on the back of the board too

The exact diagram is in the [Pico datasheet](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf).

## Power pins

| Pin | Description | Use |
| --- | --- | --- |
| **3V3(OUT)** (pin 36) | 3.3 V made by the Pico | **Take sensor power from here** (up to about 300 mA in total) |
| **GND** (pins 3, 8, 13, 18, 23, 28, 33, 38) | 0 V | Connect the GND of every part here. Any GND is the same |
| **VBUS** (pin 40) | 5 V coming from USB | 5 V available only while USB is connected |
| **VSYS** (pin 39) | The Pico's power input | Where to connect a battery (1.8–5.5 V) |

> **The Pico's pins are 3.3 V.** Putting a 5 V signal into a GPIO can damage it.
> When choosing sensors, check that they are "3.3 V compatible".

## Digital input/output (GPIO)

Any of GP0–GP28 can be used for digital input and output. Digital means dealing with only two values: "0 or 1".

| Use | How to write it | Behavior | Examples |
| --- | --- | --- | --- |
| **Output** | `gpio_set_dir(n, GPIO_OUT)` | Outputs 0 V (0) or 3.3 V (1) | LED, buzzer |
| **Input** | `gpio_set_dir(n, GPIO_IN)` | Reads whether the voltage is high or low as 1 / 0 | Button, switch |

In both cases, first make the pin usable with `gpio_init(n)`, then set it up.

```cpp run
#include <cstdio>
#include "pico/stdlib.h"

int main() {
    stdio_init_all();
    sleep_ms(1500);

    gpio_init(15);
    gpio_set_dir(15, GPIO_OUT);
    gpio_put(15, 1);               // set to 3.3 V
    gpio_put(15, 0);               // set to 0 V

    gpio_init(14);
    gpio_set_dir(14, GPIO_IN);
    gpio_pull_up(14);
    printf("GP14 value: %d\n", gpio_get(14));   // 1 if nothing is connected

    while (true) sleep_ms(1000);
}
```

There are also functions that handle several pins at once.

| Function | Meaning |
| --- | --- |
| `gpio_init_mask(mask)` | Makes all pins whose bit in `mask` is 1 usable at once. For example `(1u << 14) \| (1u << 15)` is GP14 and GP15 |
| `gpio_set_dir_out_masked(mask)` | Makes them all outputs at once |
| `gpio_put_masked(mask, value)` | Outputs to them all at once |
| `gpio_get_all()` | Reads the state of all pins as one number (bit n is GPn) |

### Pull-up and pull-down

When the button is not pressed, the input pin is connected to nothing (it is "floating"), and its value wanders between 0 and 1.
Pull-ups and pull-downs prevent this.

![How a pull-up works](images/en/pullup.svg)

- `gpio_pull_up(n)`: **1** when nothing is connected. Connect the button between the GPIO and **GND** (0 when pressed)
- `gpio_pull_down(n)`: **0** when nothing is connected. Connect the button between the GPIO and **3V3** (1 when pressed)
- `gpio_disable_pulls(n)`: use neither

The pull-up is the common one. Because "pressed is 0", the program checks for a press with `gpio_get(n) == 0`.

## Analog input (ADC)

Only three pins, **GP26, GP27 and GP28**, can read a voltage of 0–3.3 V as a number.
They are used for potentiometers (variable resistors), light sensors, sensors with analog output and so on.

![Reading a potentiometer with analog input](images/en/adc-pot.svg)

![A potentiometer (variable resistor)](images/potentiometer.jpg)

### Connecting and reading a potentiometer

Push it into the breadboard and connect it to the Pico with three jumper wires. How to push in the Pico, and the order of its pins, are the same as in "An external LED" in Chapter 8.

![How to push the potentiometer into the breadboard](images/en/pot-breadboard.svg)

![Schematic of the potentiometer](images/en/pot-sch.svg)

1. Unplug USB
2. Push the potentiometer's three legs into a free spot below the groove, to the left of the Pico. Each leg should go into a different vertical column
3. With jumper wires, connect the column of the left leg to **pin 36 (3V3(OUT))**, the middle leg to **pin 31 (GP26)**, and the right leg to **pin 28 (GND)**. All of them are in the bottom row (pin 21 at the left end, then 22, 23 … to the right)
4. Plug in USB
5. In VS Code, open `CMakeLists.txt`, add `hardware_adc` to `target_link_libraries`, and save (chapter 5). Without it, the build stops with `fatal error: hardware/adc.h: No such file or directory`

```cmake
target_link_libraries(blink
        pico_stdlib
        hardware_adc)
```

6. Delete everything in the `.cpp`, paste the program below, save, then Compile → Run (the same as "External LED" in chapter 8)
7. Watch the output in Serial Monitor or Pico Studio. Turn the knob and the value changes between 0 and 4095

```cpp run
#include <cstdio>
#include "pico/stdlib.h"
#include "hardware/adc.h"

int main() {
    stdio_init_all();
    adc_init();
    adc_gpio_init(26);             // make GP26 an analog input
    adc_select_input(0);           // read ADC0 (= GP26)

    while (true) {
        uint16_t raw = adc_read(); // 0-4095 (12 bits)
        float volt = raw * 3.3f / 4095;
        printf("value: %4u  voltage: %.2f V\n", raw, volt);
        sleep_ms(500);
    }
}
```

| Code | Meaning |
| --- | --- |
| `adc_init()` | Makes the ADC usable (once, at the start) |
| `adc_gpio_init(26)` | Switches GP26 to analog input |
| `adc_select_input(0)` | Which ADC to read. GP26 = 0, GP27 = 1, GP28 = 2, temperature sensor = 4 |
| `adc_read()` | Reads it. A 12-bit value from 0 to 4095 (MicroPython's `read_u16()` scales it to 0–65535, so the numbers differ) |

If nothing is connected, the value changes randomly (because it is floating).
The `f` in `3.3f` means "a float number". The Pico's CPU is not good at decimal arithmetic, so use `float` rather than `double` (without `f`).

> Swapping the potentiometer's two ends (3V3 and GND) only reverses which way the value increases as you turn it; nothing breaks.
> But do not connect the middle leg directly to 3V3 or GND.

### Reading the chip's temperature

ADC number 4 is the chip's built-in temperature sensor. You can try it without connecting anything.

```cpp run
#include <cstdio>
#include "pico/stdlib.h"
#include "hardware/adc.h"

int main() {
    stdio_init_all();
    sleep_ms(1500);
    adc_init();
    adc_set_temp_sensor_enabled(true);   // power on the temperature sensor
    adc_select_input(4);

    float v = adc_read() * 3.3f / 4096;
    printf("chip temperature: %.1f C\n", 27.0f - (v - 0.706f) / 0.001721f);
    while (true) sleep_ms(1000);
}
```

It is the temperature of the chip itself, so it reads a little higher than the room temperature.

## Changing an LED's brightness with PWM

A GPIO can only output 0 V or 3.3 V, but if you **turn it on and off very quickly**, the LED looks partly bright. This is called **PWM**.
Changing "the share of time it is on" (the duty cycle) changes the brightness.

Try it with the external LED (GP15) from Chapter 8.

```cpp run
#include "pico/stdlib.h"
#include "hardware/pwm.h"

constexpr uint PIN = 15;

int main() {
    stdio_init_all();
    gpio_set_function(PIN, GPIO_FUNC_PWM);     // use GP15 for PWM
    uint slice = pwm_gpio_to_slice_num(PIN);   // the number of the PWM circuit (slice) GP15 uses

    // set the period: 125 MHz / divider 125 / (wrap+1) 1000 = 1 kHz (1000 times a second)
    pwm_set_clkdiv(slice, 125.0f);
    pwm_set_wrap(slice, 999);
    pwm_set_enabled(slice, true);

    for (int n = 0; n < 3; n++) {
        for (int d = 0; d <= 1000; d += 25) {  // gradually brighter
            pwm_set_gpio_level(PIN, d);
            sleep_ms(20);
        }
        for (int d = 1000; d >= 0; d -= 25) {  // gradually dimmer
            pwm_set_gpio_level(PIN, d);
            sleep_ms(20);
        }
    }
    pwm_set_gpio_level(PIN, 0);
    while (true) sleep_ms(1000);
}
```

| Code | Meaning |
| --- | --- |
| `gpio_set_function(PIN, GPIO_FUNC_PWM)` | Switches the pin to PWM |
| `pwm_gpio_to_slice_num(PIN)` | The number of the PWM circuit the pin uses. Two pins share one circuit |
| `pwm_set_clkdiv` and `pwm_set_wrap` | Set the speed. Divide the CPU's 125 MHz by 125 and count 0–999, and you get 1 kHz |
| `pwm_set_gpio_level(PIN, d)` | The share of time it is on. With `wrap` 999, 0 is off, 500 is half and 1000 is brightest |

- The Pico 2's CPU runs at 150 MHz, so the same calculation gives 1.2 kHz. You cannot tell the difference with an LED

- The angle of a servo motor and the pitch of a buzzer are also set with PWM

## Pins for communication

When exchanging data with sensors, you use fixed communication methods.

| Method | Wires | Features | Commonly used pins |
| --- | --- | --- | --- |
| **I2C** | 2 (SDA, SCL) | Several sensors can share one pair of wires. **The most commonly used** | I2C0: GP4 (SDA), GP5 (SCL) |
| **SPI** | 4 | Faster than I2C. SD cards and displays | SPI0: GP16–19 |
| **UART** | 2 (TX, RX) | Talking with GPS or other microcontrollers | UART0: GP0 (TX), GP1 (RX) |

I2C, SPI and UART can also be assigned to pins other than those in the table.

For which pins can be used, see the pinout diagram in the [Pico datasheet](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf).

In C++, you switch the pins to the communication function before using them. Here is an example for I2C (details in Chapter 12).

```cpp
#include "hardware/i2c.h"

i2c_init(i2c0, 400 * 1000);              // use I2C0 at 400 kHz
gpio_set_function(4, GPIO_FUNC_I2C);     // GP4 as SDA
gpio_set_function(5, GPIO_FUNC_I2C);     // GP5 as SCL
gpio_pull_up(4);
gpio_pull_up(5);
```

| Method | Setup function | Pin function |
| --- | --- | --- |
| I2C | `i2c_init(i2c0, speed)` | `GPIO_FUNC_I2C` |
| SPI | `spi_init(spi0, speed)` | `GPIO_FUNC_SPI` |
| UART | `uart_init(uart0, 115200)` | `GPIO_FUNC_UART` |

In this guide, the I2C sensors from Chapter 11 onward use GP4 and GP5.

## Precautions to avoid damage

- **Do not put 5 V into a GPIO** (3.3 V maximum)
- Do not connect 3V3 directly to GND (a short circuit)
- When changing wiring, **unplug USB first**
- Always connect LEDs together with a resistor (220 Ω–1 kΩ)
- Do not drive things that draw a lot of current, such as motors, directly from a GPIO (use a driver circuit)
- When the wiring is done, check it once more before plugging in USB

## Summary

- Programs use GP numbers. Do not confuse them with physical pin numbers
- Take sensor power from 3V3(OUT), and connect all GNDs together

- Buttons use a pull-up so that "pressed is 0" (in C++, `gpio_pull_up`)
- Analog is GP26–28. C++'s `adc_read()` gives 0–4095. Change brightness with PWM
- In C++, `gpio_set_function` switches a pin to a role such as PWM or I2C

- For I2C, start with GP4 (SDA) and GP5 (SCL)
- The Pico is 3.3 V. Do not put in 5 V

## Exercises

```quiz
Q: Do programs use physical pin numbers or GP numbers?
A: GP | GP numbers | GP number
E: Do not confuse them with physical pin numbers.

Q: What is the highest voltage you may put on a Pico GPIO pin (V)?
A: 3.3
E: 5V will damage it.

Q: What is the largest value C++ `adc_read()` returns?
A: 4095
E: It is 12-bit, so 0–4095.

Q: With a pull-up button, what does `gpio_get` return while pressed: 0 or 1?
A: 0
E: With a pull-up, pressed means 0.

Q: For I2C, GP4 is SDA. What is GP5?
A: SCL
E: SDA is the data line; SCL is the clock line.
```
