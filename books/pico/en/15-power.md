# 15. Saving power and running for a long time

For products that run on batteries for months, like a collar, this chapter is essential. How to calculate battery life is in Chapter 16.

## Ways to reduce power

Power is decided by **time in use × current in use**. There are three broad ways to reduce it.

1. Reduce the current while running (lower the clock, stop unused circuits)
2. Reduce the current while waiting (rest)
3. Shorten the time spent running (batch work together, send less often)

| Method | Rough effect | Effort |
| --- | --- | --- |
| Rest while waiting with `sleep_ms` / `sleep_until` | Medium | Small (already in use) |
| Lower the CPU clock | Medium | Small |
| Put sensors to sleep while not measuring | Medium to large (depends on the sensor) | Small |
| Send less often (send in batches) | Large (when using radio) | Small |
| Do not use USB (in products, move `printf` to UART or remove it) | Small to medium | Small |
| Use DORMANT (deep sleep) | Large | Large (needs pico-extras) |
| Choose the power circuit (an efficient regulator) | Large | Board design |

The numbers vary greatly with the board and connected parts. **Always measure the current in your own circuit** to check ("Measuring current" below).

### Rest while waiting

`sleep_ms` and `sleep_until` rest the CPU while waiting (it stops with an instruction called `__wfe` until an interrupt arrives).
Do not write a loop that does nothing but keep looking at the time (a busy loop), because it keeps using power.

```cpp
// bad: the CPU runs at full power even while waiting
while (absolute_time_diff_us(get_absolute_time(), next) > 0) {}

// good: rest while waiting
sleep_until(next);
```

### Lower the clock

The Pico's CPU runs at 125 MHz (150 MHz on the Pico 2). For just measuring and classifying, much slower is fine.

```cpp run
#include <cstdio>
#include "pico/stdlib.h"
#include "hardware/clocks.h"

int main() {
    set_sys_clock_khz(48000, true);    // set the CPU to 48 MHz (before stdio_init_all)
    stdio_init_all();

    while (true) {
        printf("CPU clock: %u Hz\n", static_cast<unsigned>(clock_get_hz(clk_sys)));
        sleep_ms(1000);
    }
}
```

- The `true` in `set_sys_clock_khz(48000, true)` means "stop if that speed cannot be made". Some speeds cannot be made, so use values such as 48000, 64000 and 96000
- Change the clock **before** setting up `stdio_init_all()`, timers or PWM. PWM and UART speeds are calculated from the clock
- USB runs on a separate clock, so `printf` still works at 48 MHz

### Put sensors to sleep

Sensors use power too. For example, the MPU-6050's gyro can be stopped if you do not use it.

```cpp
// MPU-6050: stop the gyro's three axes (the lower 3 bits of PWR_MGMT_2 = 0x6C)
uint8_t buf[2] = {0x6C, 0x07};
i2c_write_blocking(i2c0, 0x68, buf, 2, false);
```

Which register puts it to sleep is written in the "Power Management" or "Low Power" section of the sensor's datasheet.

### DORMANT (deep sleep)

To reduce current even more, use **DORMANT** or **SLEEP**, which stop almost all clocks. It wakes up on an interrupt from a button or the RTC (clock).
This is not in the main Pico SDK; use `pico_sleep` from [pico-extras](https://github.com/raspberrypi/pico-extras). Download pico-extras and add lines to your project's `CMakeLists.txt` to load it (pico-extras' README explains how).
Examples are in [sleep in pico-playground](https://github.com/raspberrypi/pico-playground/tree/master/sleep).

### Measuring current

Put an ammeter (a multimeter's current range) or a USB current checker between the battery and the Pico's VSYS and measure.

| State | When to measure |
| --- | --- |
| Running | During measurement and classification |
| Resting | While waiting in `sleep_until` |
| Sending | While sending by radio (Pico W and others) |

From each current and the share of time spent in it, work out the average current, and estimate battery life with the calculation in Chapter 16.

![A multimeter (digital multimeter)](images/multimeter.jpg)

## Measuring the battery voltage

On the official Pico, a third of the supply voltage (VSYS) is connected to **GP29 (ADC3)**. Reading it gives a rough idea of how much battery is left.

```cpp run
#include <cstdio>
#include "pico/stdlib.h"
#include "hardware/adc.h"

int main() {
    stdio_init_all();
    adc_init();
    adc_gpio_init(29);                 // GP29 = VSYS / 3
    adc_select_input(3);

    while (true) {
        uint32_t sum = 0;
        for (int i = 0; i < 16; i++) sum += adc_read();
        float vsys = (sum / 16.0f) * 3.3f / 4095 * 3;   // it was divided by 3, so multiply by 3 again
        printf("VSYS: %.2f V\n", vsys);
        sleep_ms(1000);
    }
}
```

- When connected to USB, it shows a value a little below 5 V (around 4.7 V)
- On the **Pico W / Pico 2 W**, GP29 is shared with the wireless chip, so this method does not work as is (you need tricks such as not reading it while the radio is in use)
- Decide in advance what to do as the battery voltage falls: stop recording and save important data, send less often and so on

## Restarting automatically when it hangs (the watchdog)

In products, programs sometimes stop for unexpected reasons (a sensor's reply never comes back, something was written outside an array and so on).
The **watchdog** is a guard that restarts the Pico if the "I'm alive" signal (`watchdog_update()`) does not arrive within a set time.

```cpp run
#include <cstdio>
#include "pico/stdlib.h"
#include "hardware/watchdog.h"

constexpr uint LED_PIN = 25;
constexpr uint BTN_PIN = 24;

int main() {
    stdio_init_all();
    sleep_ms(1500);
    if (watchdog_caused_reboot()) {
        printf("restarted by the watchdog\n");
    } else {
        printf("started normally\n");
    }

    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    gpio_init(BTN_PIN);
    gpio_set_dir(BTN_PIN, GPIO_IN);
    gpio_pull_up(BTN_PIN);

    watchdog_enable(2000, true);       // restart if no signal for 2 s. true = pause while debugging

    while (true) {
        gpio_put(LED_PIN, !gpio_get(LED_PIN));
        if (!gpio_get(BTN_PIN)) {
            printf("button pressed, so hanging on purpose\n");
            while (true) {}            // pretend to hang (no signal is sent)
        }
        watchdog_update();             // the "I'm alive" signal
        sleep_ms(200);
    }
}
```

When flashed, the LED blinks, and pressing the USR button makes it hang. After 2 seconds the Pico restarts and shows "restarted by the watchdog".

| Code | Meaning |
| --- | --- |
| `watchdog_enable(2000, true)` | Restarts if no signal arrives within 2000 ms. The maximum is about 8 seconds |
| `watchdog_update()` | Sends the signal. Call it in the loop at intervals shorter than the set time |
| `watchdog_caused_reboot()` | `true` if the previous restart was caused by the watchdog |

- Make the time comfortably longer than one round of the loop (including long work)
- Call `watchdog_update()` **only when all the work has gone correctly**. Calling it inside an interrupt is pointless, because the signal is sent even if `main` has stopped
- Recording the number of restarts and their reasons lets you find out later what happened in the field (keep a count in flash, the same way as in "Keeping settings" below)

## Keeping settings (flash)

You want sensor calibration values (such as the soil moisture sensor's `DRY` and `WET` in Chapter 10) and the cow's ID number to survive a power cut.
Save them in **the last sector of flash (4096 bytes)**, the same way as in Chapter 13.

To check that the values read back are correct, save **a marker (a magic number)** and **a check value (a CRC or the like)** along with them. This avoids using broken values on first start-up, or after the power is cut in the middle of writing.

```cpp run
#include <cstddef>
#include <cstdio>
#include <cstring>
#include "pico/stdlib.h"
#include "hardware/flash.h"
#include "hardware/sync.h"

struct Settings {
    uint32_t magic;                    // marker. MAGIC if saved correctly
    uint16_t version;                  // increase it when you change the shape of the settings
    uint16_t cow_id;                   // the cow's ID number
    int32_t soil_dry, soil_wet;        // soil moisture sensor calibration
    uint32_t boot_count;               // number of start-ups
    uint32_t check;                    // check value (calculated from everything above)
};

constexpr uint32_t MAGIC = 0x50494331;  // "PIC1"
constexpr uint16_t VERSION = 1;
constexpr uint32_t OFFSET = PICO_FLASH_SIZE_BYTES - FLASH_SECTOR_SIZE;   // the last 4096 bytes

// check value (a simple hash: FNV-1a)
uint32_t checksum(const Settings& s) {
    auto* p = reinterpret_cast<const uint8_t*>(&s);
    uint32_t h = 2166136261u;
    for (size_t i = 0; i < offsetof(Settings, check); i++) h = (h ^ p[i]) * 16777619u;
    return h;
}

bool load(Settings& s) {
    memcpy(&s, reinterpret_cast<const void*>(XIP_BASE + OFFSET), sizeof(s));
    return s.magic == MAGIC && s.version == VERSION && s.check == checksum(s);
}

void save(Settings& s) {
    s.magic = MAGIC;
    s.version = VERSION;
    s.check = checksum(s);
    static uint8_t page[FLASH_PAGE_SIZE];          // only 256 bytes at a time can be written, so put it in a page
    memset(page, 0xFF, sizeof(page));
    memcpy(page, &s, sizeof(s));
    uint32_t irq = save_and_disable_interrupts();
    flash_range_erase(OFFSET, FLASH_SECTOR_SIZE);
    flash_range_program(OFFSET, page, FLASH_PAGE_SIZE);
    restore_interrupts(irq);
}

int main() {
    stdio_init_all();
    sleep_ms(1500);

    Settings s;
    if (!load(s)) {
        printf("no settings, so using the initial values\n");
        s = Settings{};
        s.cow_id = 1;
        s.soil_dry = 3100;
        s.soil_wet = 1250;
    }
    s.boot_count++;
    save(s);                                       // increase the start-up count and save

    printf("cow %u  dry %d  wet %d  start-up number %u\n", static_cast<unsigned>(s.cow_id), static_cast<int>(s.soil_dry),
           static_cast<int>(s.soil_wet), static_cast<unsigned>(s.boot_count));
    while (true) sleep_ms(1000);
}
```

After flashing, "start-up number N" goes up each time you unplug and replug USB.

- Each sector can be erased about 100,000 times. **Do not save at every start-up or every measurement** (this example is just for trying it; in a product, save only when a value changes)
- When using this together with the records in Chapter 13, move the record area one sector earlier so they do not overlap
- When you change the shape of the settings (the `struct`), increase `VERSION`. This prevents reading old-shaped values as if they were the new shape
- When using both cores, also use `multicore_lockout` from Chapter 12

## Summary

- Power is "current × time". Rest while waiting with `sleep_ms` / `sleep_until`, lower the clock, and put sensors to sleep
- For deep sleep, use `pico_sleep` from pico-extras (built with commands)
- Always measure the current to check the effect
- On the official Pico, GP29 (ADC3) gives the battery voltage (a third of VSYS)
- Use the watchdog to restart automatically on a hang. Send the signal only when all the work has gone correctly
- Save settings in the last sector of flash, with a marker and a check value. Save only when needed

## Exercises

```quiz
Q: Energy used is current multiplied by what?
A: time
E: Rest while waiting, lower the clock and put sensors to sleep.

Q: On the official Pico, which GP pin measures battery voltage?
A: 29 | GP29
E: ADC3 reads one third of VSYS.

Q: If GP29 reads 1.4 V, what is VSYS (V)?
A: 4.2
E: It shows one third of VSYS: 1.4 × 3 = 4.2 V.

Q: What is the mechanism that restarts the Pico automatically if it hangs?
A: watchdog | watchdog timer
E: Feed it only when every task has run correctly.

Q: What is the deepest sleep mode called?
A: DORMANT | dormant
E: Use `pico_sleep` from pico-extras.
```
