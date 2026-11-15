# 11. Writing C++ for microcontrollers

## What you will learn

- What is different from a PC when writing C++ on a microcontroller
- How to choose integer and decimal types
- Where memory lives, and writing without `new`
- Which parts of the standard library you may use, and which to avoid
- How to handle errors (without exceptions)
- Handling sensors with classes, and splitting files
- Running several things at once with a "no waiting" style (a state machine)

This assumes you can create a VS Code project as in Chapter 3. The complete programs in this chapter can be tried by pasting them into your project's `.cpp` and doing Compile → Run.

## Differences from C++ on a PC

| Item | PC | Pico |
| --- | --- | --- |
| Memory | Several GB | 264 KB (520 KB on the Pico 2) |
| Decimal arithmetic | Fast | Slow (the Pico has no floating-point hardware; the Pico 2 is fast only for `float`) |
| Exceptions (`try` / `throw`) | Used | Turned off in the Pico SDK settings |
| Standard library | All usable | Only part. Do not use `std::cout` or `std::thread` |
| End of the program | It ends when `main` ends | `main` does not end. It repeats forever |
| When it stops with an error | The OS tells you | It stops without saying anything. Make sure you can notice (the watchdog in Chapter 15) |

## Integer types

In C++ on the Pico, use **types with a fixed size**, because the size of `int` can differ between environments.

| Type | Size | Range | Use |
| --- | --- | --- | --- |
| `uint8_t` | 1 byte | 0–255 | I2C data, byte sequences |
| `int16_t` | 2 bytes | −32768–32767 | Raw sensor values (MPU-6050 and others) |
| `uint16_t` | 2 bytes | 0–65535 | ADC values |
| `int32_t` / `uint32_t` | 4 bytes | About ±2.1 billion / 0 to about 4.3 billion | Time (milliseconds), intermediate results |
| `uint64_t` | 8 bytes | Very large | Time (microseconds, `time_us_64()`) |
| `uint` | 4 bytes | 0 to about 4.3 billion | Pico SDK pin numbers and so on |
| `size_t` | 4 bytes | 0 to about 4.3 billion | Array sizes |

```cpp
uint8_t hi = 200, lo = 100;
int16_t raw = static_cast<int16_t>((hi << 8) | lo);   // join 2 bytes (Chapter 9)
uint32_t ms = to_ms_since_boot(get_absolute_time());  // milliseconds since startup. Wraps around after about 49 days
```

- If a multiplication goes out of range partway, you get strange values (overflow). Even when computing with `int16_t` values, do the intermediate steps in `int32_t`
- A `uint32_t` of milliseconds goes back to 0 after about 49 days. In products that run for a long time, compute time differences in `int32_t`, or use `uint64_t` microseconds

## Decimal types

| Type | Speed (Pico) | Precision |
| --- | --- | --- |
| `float` | Slowish (computed in software; about 1 microsecond per operation) | About 7 digits |
| `double` | Even slower (2–3 times `float`) | About 15 digits |
| Integers | Fast | No decimals |

- For decimals, use **`float`**, and put an **`f`** on numbers (`3.3f`). Without `f`, they are `double`
- Use the `float` versions of functions too (`sqrtf`, `fabsf`, `powf`)
- Where there is a lot of calculation, **making the unit smaller and computing in integers** is faster

```cpp
// decimal: 0.981 g
float az = raw / 16384.0f;

// integer: 981 mg (milli-g). Expresses the same thing without decimals
int32_t az_mg = raw * 1000 / 16384;
```

> The Pico 2 (RP2350) has floating-point hardware, so it computes `float` fast. `double` stays slow.

## Constants and names

```cpp
constexpr uint LED_PIN = 25;           // a constant decided at build time. Safer than #define
constexpr int HZ = 25;
constexpr int N = HZ * 2;              // calculations between constants are also done at build time

enum class Mode { Idle, Measure, Send };   // give names to states
Mode mode = Mode::Idle;
```

- Do not write numbers directly; give them names with `constexpr`. To change a pin number, you only fix one place
- Give names to states and kinds with `enum class`. They are easier to read and harder to get wrong than numbers like `0`, `1`, `2`

## Where memory lives

A review of Chapter 13. In products, the basic rule is to **decide how memory is used at build time**.

| Where | How to write it | Decided when | Caution |
| --- | --- | --- | --- |
| Flash (read-only) | `static const` / `constexpr` arrays | Build | Uses no RAM. Large tables go here |
| Static (RAM) | Variables outside functions, `static` | Build | Large arrays go here |
| Stack (RAM) | Variables inside functions | Run time | Small (a few KB). Making a large array overflows it |
| Heap (RAM) | `new`, `std::vector`, `std::string` | Run time | Gaps form, and over long runs it runs out |

```cpp
static const float table[256] = { /* ... */ };   // placed in flash (uses no RAM)
float samples[1000];                             // static. 4 KB
Mpu6050 mpu(i2c0);                               // classes can also be placed outside functions

void loop_once() {
    float fe[8];                                 // small things can go on the stack
    // float big[5000];                          // <- overflows the stack
}
```

How much RAM a built program uses can be checked like this when building with commands.

```bash
arm-none-eabi-size build/blink.elf
```

```text
   text    data     bss     dec     hex filename
  31744      0   3592   35336    8a08 build/blink.elf
```

`text` is flash, and `data + bss` is RAM (static) use. You can use up to 264 KB (270336 bytes) minus the stack (a few KB).

## Standard library parts you may use

| OK to use | Why |
| --- | --- |
| `<cstdint>`, `<cstdio>` (`printf`), `<cstring>` (`memcpy`) | Small |
| `<cmath>` (`sqrtf` and others) | Decimal calculations |
| `<array>` (`std::array`) | Fixed-size arrays. Also has `at()`, which checks the range |
| `<algorithm>` (`std::min`, `std::max`, `std::clamp`, `std::sort`) | Uses no memory |
| `<optional>` (`std::optional`) | Can express "no value" ("Handling errors" below) |

| Avoid | Why |
| --- | --- |
| `<iostream>` (`std::cout`) | Makes the program hundreds of KB larger. Use `printf` |
| `std::vector`, `std::string`, `std::map` | Use the heap. If you use them, `reserve` at the start and do not grow them |
| `try` / `throw` | The Pico SDK is set not to use exceptions (`PICO_CXX_ENABLE_EXCEPTIONS=0`) |
| `std::thread`, `std::mutex` | Cannot be used without an OS. The two cores are in Chapter 12 |
| `new` / `delete` | Use the heap. Once at the start is fine |

## Handling errors

Since exceptions are not used, report errors through **return values**.

```cpp
#include <optional>

// method 1: true on success. The result is returned through an argument (reference)
bool read_temp(float& out);

// method 2: express "no value" with std::optional
std::optional<float> read_temp();

if (auto t = read_temp()) {          // only enters when there is a value
    printf("%.1f C\n", *t);
} else {
    printf("could not read\n");
}
```

When you want to distinguish kinds of error, return an `enum class`.

```cpp
enum class SensorError { None, NotFound, BadCrc, Timeout };

SensorError read_sht31(float& temp, float& hum);
```

- Pico SDK functions also return a negative number (`PICO_ERROR_GENERIC` and others) on error. **Always check return values**
- In a product, it is important to decide what to do on error (read again, use the previous value, log it)

## Handling sensors with classes

Making a class for each sensor shortens the code that uses it, and means fewer places to fix when you change sensors. The `Mpu6050` in Chapter 9 has this form.

```cpp
class Sht31 {
public:
    explicit Sht31(i2c_inst_t* i2c, uint8_t addr = 0x44) : i2c_(i2c), addr_(addr) {}

    bool read(float& temp, float& hum);   // the body is the code from Chapter 10

private:
    i2c_inst_t* i2c_;                     // which I2C unit
    uint8_t addr_;                        // address
};
```

- Do not communicate over I2C in the constructor (`Sht31(...)`). Objects placed outside functions are created before `main`, when I2C is not ready yet. Communicate in a function such as `begin()`
- `explicit` is a marker that prevents unexpected type conversions. Put it on constructors with one argument

## Splitting files

When the program gets long, split it into files.

| File | Contents |
| --- | --- |
| `sht31.h` | The shape of the class (declarations) |
| `sht31.cpp` | The bodies of the functions |
| `main.cpp` | `#include "sht31.h"` and use it |

For small classes and functions, it is easy to **write the bodies in the `.h` too** (write the functions inside the class, or mark them `inline`). Then you can use them just by `#include`, without changing `CMakeLists.txt`.
Writing `#pragma once` at the top means reading the same `.h` twice does not cause an error.

```cpp
// filter.h  - put it in the project folder and use it with #include "filter.h"
#pragma once

// moving average. Returns the average of the last N values
template <int N>
class MovingAverage {
public:
    float add(float v) {
        sum_ += v - buf_[i_];
        buf_[i_] = v;
        i_ = (i_ + 1) % N;
        if (count_ < N) count_++;
        return sum_ / count_;
    }

private:
    float buf_[N] = {};
    float sum_ = 0;
    int i_ = 0, count_ = 0;
};
```

When you split into a `.cpp`, add it to `add_executable` in `CMakeLists.txt` ("Splitting files" in Chapter 4).

```cmake
add_executable(collar collar.cpp sht31.cpp)
```

## The no-waiting style (a state machine)

While waiting in `sleep_ms`, the Pico cannot do anything else.
When you want several things to happen at once — "blink the LED every 0.5 seconds, watch the button, and measure the temperature every second" — write it so that it **looks at the time and does only the things whose time has come**.

```cpp run
#include <cstdio>
#include "pico/stdlib.h"
#include "hardware/adc.h"

constexpr uint LED_PIN = 25;
constexpr uint BTN_PIN = 24;

enum class Mode { Slow, Fast, Off };   // how the LED blinks

// a timer that "becomes true every period_ms"
class Every {
public:
    explicit Every(uint32_t period_ms) : period_(period_ms), next_(make_timeout_time_ms(period_ms)) {}
    bool ready() {
        if (absolute_time_diff_us(get_absolute_time(), next_) > 0) return false;   // not time yet
        next_ = delayed_by_ms(next_, period_);
        return true;
    }
    void set_period(uint32_t ms) { period_ = ms; }

private:
    uint32_t period_;
    absolute_time_t next_;
};

int main() {
    stdio_init_all();
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    gpio_init(BTN_PIN);
    gpio_set_dir(BTN_PIN, GPIO_IN);
    gpio_pull_up(BTN_PIN);
    adc_init();
    adc_set_temp_sensor_enabled(true);
    adc_select_input(4);

    Mode mode = Mode::Slow;
    Every blink(500), measure(1000), button(20);
    bool led = false, last_pressed = false;

    while (true) {
        if (button.ready()) {                       // check the button every 20 ms
            bool pressed = !gpio_get(BTN_PIN);
            if (pressed && !last_pressed) {         // only at the moment it is pressed
                mode = (mode == Mode::Slow) ? Mode::Fast : (mode == Mode::Fast) ? Mode::Off : Mode::Slow;
                blink.set_period(mode == Mode::Fast ? 100 : 500);
                printf("mode: %s\n", mode == Mode::Slow ? "slow" : mode == Mode::Fast ? "fast" : "off");
            }
            last_pressed = pressed;
        }
        if (blink.ready()) {                        // blinking
            led = (mode == Mode::Off) ? false : !led;
            gpio_put(LED_PIN, led);
        }
        if (measure.ready()) {                      // temperature every second
            float v = adc_read() * 3.3f / 4096;
            printf("temp %.1f C\n", 27.0f - (v - 0.706f) / 0.001721f);
        }
        sleep_ms(1);                                // rest a little (lowers power use)
    }
}
```

Each press of the USR button changes the LED from "slow → fast → off". Meanwhile, the temperature keeps coming out every second.

| Idea | What it means |
| --- | --- |
| Do not wait inside the loop | Do not put long waits like `sleep_ms(500)` in it. Look at the time and do only the things whose time has come |
| Keep the state in a variable | Remember "which mode it is in now" in `Mode mode` |
| Detect the moment of pressing | Compare with the previous value (`last_pressed`) and act only when it changes from released to pressed |
| Check every 20 ms | Prevents the button contacts from bouncing so that one press looks like several (contact bounce) |

This form is the same idea as MicroPython's `asyncio` or an event loop on a PC. To run at more precise times, use the interrupts in Chapter 12.

## Summary

- Use types with a fixed size, such as `uint8_t`, `int16_t` and `uint32_t`
- For decimals, use `float` and numbers with `f`. For heavy calculation, use integers (mg and so on)
- Constants are `constexpr`, states are `enum class`
- Large data goes outside functions (static) or in `static const` (flash). Avoid `new` and `std::vector`
- Do not use `std::cout`, exceptions or `std::thread`. Report errors through return values (`bool`, `std::optional`, `enum class`)
- Bundle sensors into classes. Communicate in `begin()`, not in the constructor
- Run several things by looking at the time (a state machine). Do not `sleep_ms` for long
