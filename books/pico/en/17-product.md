# 17. Getting ready to make a product

This uses the content of Chapters 11–16, with the collar (Chapter 16) as the example.

## Differences between a prototype and a product

| Item | Prototype | Product |
| --- | --- | --- |
| Language | C++ (MicroPython is fine for early experiments; Appendix E) | C++ |
| Where it runs | On a desk, connected to a PC | In the field, for months, without a PC |
| When it hangs | Reset by hand | Restarts automatically (the watchdog in Chapter 15) and records the reason |
| Errors | Seen in the output box | Recorded. Reported with LED blinking and the like |
| How to check | Run it and look | Write tests and check every time you change something |
| Which program it is | You remember | The version is in the program, so you can look it up later |
| Flashing | One at a time by hand | With a defined procedure, by script |
| Settings | Written directly in the code | Saved in flash, so each unit can be changed (Chapter 15) |

## Testing the logic on a PC

"Pure calculation" parts such as computing features and classification can be tested on a PC even without a Pico.
To do that, **put the parts that do not depend on the Pico (calculations) and the parts that do (sensors, pins) in separate files**.

```text
~/apps/collar/          (a project made in VS Code; Chapter 3)
├── features.h          calculation only (uses no Pico functions) <- usable on both the PC and the Pico
├── model.h             classification (made by train.py in Chapter 14) <- usable on both the PC and the Pico
├── collar.cpp          for the Pico (reads the sensor and uses features.h and model.h)
└── test_features.cpp   tests for the PC
```

### features.h

Rewrite the feature calculation from Chapter 14 so it uses no Pico functions.

```cpp
#pragma once
#include <cmath>

// make the 8 features. xs, ys, zs are n accelerations [g]
inline void features(const float* xs, const float* ys, const float* zs, int n, float fe[8]) {
    auto mean = [n](const float* a) { float s = 0; for (int i = 0; i < n; i++) s += a[i]; return s / n; };
    auto stdev = [n](const float* a, float m) {
        float s = 0;
        for (int i = 0; i < n; i++) s += (a[i] - m) * (a[i] - m);
        return std::sqrt(s / n);
    };
    float mag[256];                                   // keep n at 256 or less
    for (int i = 0; i < n; i++) mag[i] = std::sqrt(xs[i] * xs[i] + ys[i] * ys[i] + zs[i] * zs[i]);
    float mx = mean(xs), my = mean(ys), mz = mean(zs), mm = mean(mag);
    float diff = 0;
    for (int i = 1; i < n; i++) diff += std::fabs(mag[i] - mag[i - 1]);
    fe[0] = mx; fe[1] = my; fe[2] = mz;
    fe[3] = stdev(xs, mx); fe[4] = stdev(ys, my); fe[5] = stdev(zs, mz);
    fe[6] = stdev(mag, mm);
    fe[7] = diff / (n - 1);
}
```

### test_features.cpp (runs on the PC)

```cpp
// test on the PC: g++ -std=c++17 -Wall test_features.cpp -o test_features && ./test_features
#include <cassert>
#include <cmath>
#include <cstdio>
#include <cstring>
#include "features.h"
#include "model.h"

bool near(float a, float b) { return std::fabs(a - b) < 1e-4f; }

int main() {
    constexpr int N = 50;
    float xs[N], ys[N], zs[N], fe[8];

    // 1. still (only z is 1g) -> spread is 0, classified as rest
    for (int i = 0; i < N; i++) { xs[i] = 0; ys[i] = 0; zs[i] = 1; }
    features(xs, ys, zs, N, fe);
    assert(near(fe[2], 1.0f));
    assert(near(fe[6], 0.0f));
    assert(std::strcmp(predict(fe), "rest") == 0);

    // 2. shaking hard -> large spread
    for (int i = 0; i < N; i++) zs[i] = (i % 2) ? 1.5f : 0.5f;
    features(xs, ys, zs, N, fe);
    assert(fe[6] > 0.4f);
    assert(fe[7] > 0.9f);

    printf("All tests passed\n");
}
```

```bash
cd ~/apps/collar
g++ -std=c++17 -Wall test_features.cpp -o test_features && ./test_features
```

- `assert(condition)` stops there if the condition is not true, and shows the line number
- The classification results (`rest` and so on) depend on the data you trained on. Rewrite the tests to match your own `model.h`
- It is also worth writing a test that **reads the CSV collected on the PC (features.csv from Chapter 14) and checks that the PC's Python and the C++ give the same results**; it catches mistakes in the `features()` calculation

### collar.cpp (for the Pico)

Keep the Pico file to just reading the sensor and calling the tested functions.

```cpp
#include "features.h"
#include "model.h"
#include "mpu6050.h"
// ...
read_window(xs, ys, zs);              // sensor (the part that depends on the Pico)
features(xs, ys, zs, N, fe);          // calculation (tested on the PC)
const char* label = predict(fe);      // classification (tested on the PC)
```

## Putting a name and version into the program

So that you can tell which version of the program is on a Pico that comes back from the field, put the name and version into the program.

```cpp run
#include <cstdio>
#include "pico/stdlib.h"
#include "pico/binary_info.h"

#define APP_VERSION "1.2.0"

// information readable with picotool info
bi_decl(bi_program_name("cow-collar"));
bi_decl(bi_program_version_string(APP_VERSION));
bi_decl(bi_program_description("Cow collar: classifies behavior and sends it every minute"));

int main() {
    stdio_init_all();
    sleep_ms(1500);
    printf("cow-collar %s (built %s %s)\n", APP_VERSION, __DATE__, __TIME__);
    while (true) sleep_ms(1000);
}
```

- If you print the version with `printf` at start-up, you can tell just by looking at the output. `__DATE__` and `__TIME__` are the build date and time
- On a Pico in flashing mode, `picotool info -a` reads the name, version and build date and time (Appendix A)
- Versions are commonly given as three numbers: "major change.feature addition.bug fix"
- Manage the source code with git, and when you set a version, mark it with `git tag v1.2.0`; then you can build exactly the same program again later

## Stopping and investigating line by line (debugging)

For mistakes that `printf` alone cannot reveal, use a **Debug Probe** (an official Raspberry Pi tool) and **gdb** to stop the program partway and investigate while watching variable values.

### How to connect

| Debug Probe | Pico |
| --- | --- |
| The three wires of D (SWD) | The three **DEBUG** pins at the bottom edge of the Pico (SWCLK, GND, SWDIO) |
| USB | PC |

The Pico's DEBUG pins need pin headers soldered on (the Pico H has them from the start).

### How to use it

```bash
sudo apt install openocd gdb-multiarch
cd ~/apps/collar
cmake -S . -B build-debug -DCMAKE_BUILD_TYPE=Debug
make -C build-debug -j4 blink
```

Open two terminals. In the first, run openocd (for the Pico 2, change `rp2040.cfg` to `rp2350.cfg`).

```bash
openocd -f interface/cmsis-dap.cfg -f target/rp2040.cfg -c "adapter speed 5000"
```

In the second, run gdb.

```bash
gdb-multiarch build-debug/blink.elf
```

Inside gdb, type the following.

```text
(gdb) target remote localhost:3333
(gdb) load
(gdb) monitor reset init
(gdb) break main
(gdb) continue
(gdb) next
(gdb) print total
```

| gdb command | Meaning |
| --- | --- |
| `load` | Flashes the program (no need to press BOOT) |
| `break main` | Stops when it reaches `main`. `break blink.cpp:20` stops at line 20 |
| `continue` | Runs until the next place it stops |
| `next` / `step` | Goes one line forward (`step` goes into functions) |
| `print variable` | Shows a variable's value |
| `backtrace` | Which function it is in now (to find where it stopped) |

With the "Raspberry Pi Pico" VS Code extension, you can do the same with on-screen buttons ("Debugging" in Chapter 4). That is normally easier.
For details, see the debugging chapter of [Getting started with Raspberry Pi Pico-series](https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf).

> Without a Debug Probe, you can also use a second Pico as a Debug Probe ([debugprobe](https://github.com/raspberrypi/debugprobe)).

## Flashing many Picos

### Copying the .uf2

The simplest way is to put each one into flashing mode and copy the same `.uf2`. The following script waits for a Pico in flashing mode to be connected, and flashes it when it is.

```bash
#!/bin/sh
# usage: sh flash_many.sh build/collar.uf2
# connect one at a time while holding BOOT. Ctrl+C to finish
n=0
while true; do
    echo "waiting for a Pico in flashing mode..."
    while [ ! -d /run/media/$USER/RPI-RP2 ]; do sleep 0.5; done
    cp "$1" /run/media/$USER/RPI-RP2/ && sync
    n=$((n + 1))
    echo "flashed unit $n. Unplug it and connect the next Pico"
    while [ -d /run/media/$USER/RPI-RP2 ]; do sleep 0.5; done
done
```

### Flashing and verifying with picotool

With picotool, one line flashes, verifies the contents (`-v`) and runs it (`-x`).

```bash
picotool load -v -x build/collar.uf2
picotool info -a        # in flashing mode, check the name and version
```

### A number for each unit

The Pico's flash chip holds a number that is different for every unit (a unique ID). You can use it to tell which Pico data came from.

```cpp run
#include <cstdio>
#include "pico/stdlib.h"
#include "pico/unique_id.h"

int main() {
    stdio_init_all();
    sleep_ms(1500);
    char id[2 * PICO_UNIQUE_BOARD_ID_SIZE_BYTES + 1];
    pico_get_unique_board_id_string(id, sizeof(id));
    printf("this Pico's ID: %s\n", id);
    while (true) sleep_ms(1000);
}
```

Numbers that people decide, like the cow's ID, are saved in flash with the method in Chapter 15. Making a table that maps unique IDs to cow IDs when flashing at the factory makes them easier to manage.

## Ways to avoid trouble in the field

| Measure | How |
| --- | --- |
| Restart automatically on a hang | The watchdog (Chapter 15) |
| Be able to find out later what happened | Keep the number and reasons of restarts, and the number of sensor errors, in flash (Chapter 15) |
| Keep running even if a sensor breaks | Check return values; when it cannot read, use the previous value or send it as an error (Chapter 11) |
| Do not panic when the battery runs low | Measure VSYS; when it gets low, send less often and report it (Chapter 15) |
| Show the state from outside | Show the state with LED blink patterns (for example 1 = normal, 2 = sensor error, 3 = battery low) |
| Be able to replace the program | Make the USB connector usable from outside the case. A button for entering flashing mode too |
| Be able to change settings per unit | Do not write settings in the code; save them in flash (Chapter 15). Make them changeable over USB |

## Things to know

### Reading out the program

On the RP2040 (Pico, Pico W), the contents of flash can be read out. If you do not want your program to be read, consider features such as secure boot on the RP2350 (Pico 2).

### Licenses

The Pico SDK is published under the **BSD-3-Clause** license. You can use it in products, but you need to include the copyright notice and the license text in the product's documentation or the like. Libraries the SDK uses internally, such as the USB library (TinyUSB), also have their own licenses.
Make a list of the libraries you used and their licenses.

### Radio certification

To use a product with radio, such as one built on a Pico W, in Japan, the radio module used must have technical standards conformity certification (*giteki*).
When you put a radio module on a board you made yourself, check with the seller's information that the module has *giteki* certification.

## Pre-shipping checklist

- [ ] All the PC tests pass
- [ ] The program has a name and version, and shows them at start-up
- [ ] The source code has a marker for that version (a git tag)
- [ ] The watchdog is in place, and you have checked that it restarts when you deliberately make it hang
- [ ] You have checked that when a sensor is removed or broken, it reports an error without stopping
- [ ] You have measured the current and calculated that it runs on batteries for the intended period (Chapters 16 and 15)
- [ ] You have run it continuously for days and checked that it does not stop
- [ ] You have checked that settings are saved in flash and survive a power cut
- [ ] You have written down the flashing procedure, and someone else has flashed with it
- [ ] You have made a list of the licenses of the libraries used

## Summary

- Separate the calculations (features, classification) from the parts that depend on the Pico, and test the calculations on the PC
- Put in the name and version with `bi_decl`, and show them at start-up too. Match them to git tags
- Investigate hard mistakes by stopping the program with a Debug Probe and gdb
- For mass-production flashing, script `.uf2` copying or `picotool load -v -x`
- Use the unique ID as each unit's number, and keep numbers people decide in flash
- Avoid trouble in the field with the watchdog, error records and LED indicators

## Exercises

```quiz
Q: Which Pico SDK macro embeds a program's name and version?
A: bi_decl
E: Also print it at start-up and match it to a git tag.

Q: Which command writes to and verifies many Picos?
A: picotool | picotool load
E: Script `picotool load -v -x`.

Q: What built-in number can identify each Pico?
A: unique ID | unique id
E: Numbers chosen by people are stored in flash.

Q: Where do you test the calculations (features and judgement) that do not depend on the Pico?
A: PC | the PC | computer
E: Separate the calculations from Pico-specific parts and test them on the PC.
```
