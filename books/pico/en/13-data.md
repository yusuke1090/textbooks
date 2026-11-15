# 13. Recording and sending data

## What you will learn

- Ways to keep measured data (comparing three methods)
- Saving data in the Pico's flash and bringing it to the PC (in C++, saved in flash as raw numbers, then printed as CSV)
- Sending data to the PC over USB serial and saving it on the PC side
- Points to watch about memory and storage capacity

## Comparing the methods

![Three ways to keep measured data](images/en/data-paths.svg)

| Method | Good points | Cautions |
| --- | --- | --- |
| Save in the Pico's flash | Records even without a PC | Small capacity (about 1.4 MB on the official Pico). A limited number of write cycles |
| Send to the PC over USB | No need to worry about capacity | Only while connected to the PC |
| Send over WiFi (Pico W) | Can send from far away | Uses a lot of battery |

**CSV** is a text file with values separated by commas (`,`), one line at a time. It can be read as is by spreadsheet software (LibreOffice Calc, Excel and others) and by Python.

```text
ms,ax,ay,az
0,0.012,-0.020,0.998
100,0.010,-0.018,1.001
```

## Saving in the Pico's flash

C++ on the Pico has no "file" system like a PC. Instead, **numbers are written as they are into a fixed place in flash**.
This is smaller than turning them into text like CSV, and faster to write because there is no file system.

Flash has the following rules.

| Rule | Details |
| --- | --- |
| Erase unit | 4096 bytes (a sector) at a time. Erasing turns everything into `0xFF` |
| Write unit | 256 bytes (a page) at a time. You can only write to places that have been erased |
| Lifetime | Each sector can be erased about 100,000 times |
| While writing | The program stops (interrupts must also be stopped) |

Here, **the last 256 KB** of flash is used for records. The program is placed from the beginning, so they do not overlap even as the program grows (up to 1.75 MB of the 2 MB can be used for the program).

### Recording

Using the MPU-6050 (the wiring from Chapters 8–9), record the acceleration every 0.1 seconds. One entry (one record) is 16 bytes, and 16 fit in one page.

```cpp run
#include <cstdio>
#include <cstring>
#include "pico/stdlib.h"
#include "hardware/flash.h"
#include "hardware/sync.h"
#include "mpu6050.h"

// one entry (16 bytes)
struct Record {
    uint32_t ms;
    float ax, ay, az;
};

constexpr uint32_t LOG_SIZE = 256 * 1024;                          // size used for records
constexpr uint32_t LOG_OFFSET = PICO_FLASH_SIZE_BYTES - LOG_SIZE;  // the last 256 KB of flash
constexpr int PER_PAGE = FLASH_PAGE_SIZE / sizeof(Record);        // number that fit in one page (16)

Mpu6050 mpu(i2c0);

// write one page (256 bytes). Stop interrupts while writing
void write_page(uint32_t offset, const Record* page) {
    uint32_t irq = save_and_disable_interrupts();
    flash_range_program(offset, reinterpret_cast<const uint8_t*>(page), FLASH_PAGE_SIZE);
    restore_interrupts(irq);
}

int main() {
    stdio_init_all();
    sleep_ms(1500);
    mpu.begin(4, 5);

    // erase the record area. Erase 4096 bytes at a time, restoring interrupts each time (so USB does not drop)
    for (uint32_t off = LOG_OFFSET; off < LOG_OFFSET + LOG_SIZE; off += FLASH_SECTOR_SIZE) {
        uint32_t irq = save_and_disable_interrupts();
        flash_range_erase(off, FLASH_SECTOR_SIZE);
        restore_interrupts(irq);
    }
    printf("starting to record (10 seconds)\n");

    Record page[PER_PAGE];
    int n = 0;
    uint32_t offset = LOG_OFFSET;
    uint32_t start = to_ms_since_boot(get_absolute_time());
    for (int i = 0; i < 100; i++) {                                // every 0.1 s for 10 s
        Record& r = page[n++];
        r.ms = to_ms_since_boot(get_absolute_time()) - start;
        mpu.read_accel(r.ax, r.ay, r.az);
        if (n == PER_PAGE) {                                       // write when one page has built up
            write_page(offset, page);
            offset += FLASH_PAGE_SIZE;
            n = 0;
        }
        sleep_ms(100);
    }
    if (n > 0) {                                                   // write the rest (empty slots stay 0xFF)
        memset(&page[n], 0xFF, sizeof(Record) * (PER_PAGE - n));
        write_page(offset, page);
    }
    printf("recorded: %d entries\n", 100);
    while (true) sleep_ms(1000);
}
```

| Code | Meaning |
| --- | --- |
| `struct Record { ... };` | The shape of one entry. The time and three acceleration values |
| `PICO_FLASH_SIZE_BYTES` | The size of the flash (2 MB on the official Pico). Set by the board settings |
| `flash_range_erase(place, size)` | Erases. Place and size are multiples of 4096 |
| `flash_range_program(place, data, size)` | Writes. Size is a multiple of 256 |
| `save_and_disable_interrupts()` | Stops interrupts. If other code reads flash while it is being written, it stops. Stopping for long drops USB, so do it a little at a time |

> When using both cores, the other core must also be stopped (`multicore_lockout`, Chapter 12).

### Bringing it to the PC

The contents of flash can be read like normal memory from the Pico's address `XIP_BASE + place`. Read them and `printf` in CSV form, and CSV appears in the output box.

```cpp run
#include <cstdio>
#include "pico/stdlib.h"
#include "hardware/flash.h"

struct Record {
    uint32_t ms;
    float ax, ay, az;
};

constexpr uint32_t LOG_SIZE = 256 * 1024;
constexpr uint32_t LOG_OFFSET = PICO_FLASH_SIZE_BYTES - LOG_SIZE;

int main() {
    stdio_init_all();
    sleep_ms(2000);
    auto* records = reinterpret_cast<const Record*>(XIP_BASE + LOG_OFFSET);   // read the flash directly
    int count = LOG_SIZE / sizeof(Record);

    printf("ms,ax,ay,az\n");
    for (int i = 0; i < count; i++) {
        if (records[i].ms == 0xFFFFFFFF) break;                   // still-erased area = end of the records
        printf("%u,%.3f,%.3f,%.3f\n", static_cast<unsigned>(records[i].ms),
               records[i].ax, records[i].ay, records[i].az);
    }
    printf("done\n");
    while (true) sleep_ms(1000);
}
```

1. Flash the program above and look at the output in Serial Monitor (or Pico Studio) right away. CSV appears
2. Select from `ms,ax,ay,az` to just before `done`, copy it, paste it into a text editor and save it as `log.csv`
3. Open it in LibreOffice Calc or the like to make tables and graphs

> Flashing the recording program again erases the record area first, so the previous records are lost.

### Tips for recording for a long time

- Write once one page (256 bytes) has built up. You cannot write one entry at a time
- Rather than erasing everything each time the power comes on, first look for "how far it has written" (the place with `0xFF`) and continue from there
- Saving **summarized values** such as averages or classification results instead of raw data lets you record tens of times longer
- If the power is cut suddenly, the page being written is lost. So is anything not yet built up into a page
- If you need many records of a fixed form, you can also use an SD card (SPI)

## Sending to the PC over USB

What you `printf()` reaches the PC over USB serial (that is also what appears in Serial Monitor and Pico Studio's output box).
If you run a Python program on the PC side, it can receive this and save it to a file.

### The Pico side

The flashed program runs when the power comes on, so it starts sending as soon as it is connected.

```cpp run
#include <cstdio>
#include "pico/stdlib.h"
#include "mpu6050.h"

Mpu6050 mpu(i2c0);

int main() {
    stdio_init_all();
    mpu.begin(4, 5);

    uint32_t start = to_ms_since_boot(get_absolute_time());
    absolute_time_t next = get_absolute_time();
    while (true) {
        float ax, ay, az;
        if (mpu.read_accel(ax, ay, az)) {
            unsigned t = to_ms_since_boot(get_absolute_time()) - start;
            printf("%u,%.3f,%.3f,%.3f\n", t, ax, ay, az);
        }
        next = delayed_by_ms(next, 50);
        sleep_until(next);
    }
}
```

### The PC side (run in the PC's terminal)

> The PC-side program runs **on the PC**, not on the Pico.
> Only one program can use a port at a time, so first stop Serial Monitor and press **"切断" (Disconnect)** in Pico Studio.

```python
# pc_logger.py  - usage: python3 pc_logger.py
import serial, time

PORT = "/dev/ttyACM0"
ser = serial.Serial(PORT, 115200, timeout=1)
ser.reset_input_buffer()

name = time.strftime("log_%Y%m%d_%H%M%S.csv")
with open(name, "w") as f:
    f.write("ms,ax,ay,az\n")
    print("saving to", name, "... Ctrl+C to stop")
    try:
        while True:
            line = ser.readline().decode(errors="replace").strip()
            if line.count(",") == 3:
                f.write(line + "\n")
                print(line)
    except KeyboardInterrupt:
        pass
print("saved:", name)
```

### Steps

1. Flash the Pico-side program above from VS Code
2. Stop Serial Monitor, and press "切断" (Disconnect) in Pico Studio
3. Copy the PC-side code with the "Copy" button, paste it into a text editor and save it as `pc_logger.py` (for example in your home folder)
4. In the terminal, move to where you saved it and run it

```bash
cd ~
python3 pc_logger.py
```

5. Numbers scroll by on screen and are saved to a file with a name like `log_20261105_210000.csv`
6. To finish, press **Ctrl + C**

- `pyserial` is needed (`sudo apt install python3-serial`; installed in Chapter 2)
- If you get an error that "the port is in use", check whether Serial Monitor or Pico Studio is using the port

## Memory cautions

The Pico's RAM is 264 KB (520 KB on the Pico 2). Your program can use almost all of it.
At the end of a build, you can check how much memory the program uses.

| Where | What goes there | Caution |
| --- | --- | --- |
| Static (variables outside functions, `static`) | Large arrays, sensor classes | The size is decided at build time. **Put large data here** |
| Stack (variables inside functions) | Temporary variables | Small, 2–4 KB. Making a large array inside a function breaks things (overflows) |
| Heap (`new`, `std::vector`) | Things whose size is decided later | Repeatedly using and returning memory leaves gaps until it runs out. Avoid it for long runs |

```cpp
float samples[2000];          // outside a function: static. Even 8 KB is fine

void measure() {
    float tmp[2000];          // inside a function: overflows the stack. Do not do this
    static float buf[2000];   // adding static makes it static
}
```

- Keep data in arrays whose size is fixed at the start (`float samples[N]`)
- When a certain amount has built up, save or send it and start using the array again from the beginning (a ring buffer, Chapter 12)

> **The difference between RAM and flash**: RAM is the workspace while running (264 KB, erased when the power is off).
> Flash is where the program and records are kept (2 MB, kept when the power is off).

## Summary

- In C++, write raw numbers into the last area of flash. Erase 4096 bytes at a time and write 256 bytes at a time
- Print records as CSV with `printf` and copy them from Serial Monitor or the like to bring them to the PC
- When connected to a PC, `printf` → receive and save with pyserial on the PC side. Free the port from other programs first
- Put large arrays outside functions (static). Avoid `new` where possible

## Exercises

```quiz
Q: In how many bytes at a time is the Pico's flash erased?
A: 4096
E: It is written 256 bytes at a time.

Q: In how many bytes at a time is the Pico's flash written?
A: 256
E: It is erased 4096 bytes (one sector) at a time.

Q: Which Python library on the PC receives data sent from the Pico over USB?
A: pyserial
E: Free the port from other programs first.

Q: In what format do you `printf` records so they are easy to bring to the PC?
A: CSV
E: Copy from Serial Monitor and open it in a spreadsheet.
```
