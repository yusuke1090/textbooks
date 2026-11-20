# Appendix B. Troubleshooting

## When you cannot flash from VS Code

First check by following this flowchart.

![How to investigate when you cannot flash from VS Code](images/en/trouble-flow.svg)

| Symptom | Cause and fix |
| --- | --- |
| The Project items in Quick Access are grayed out | The project folder (the one with `CMakeLists.txt` and `.vscode`) is not open. File → Open Folder |
| The first project takes forever to be created | It is downloading into `~/.pico-sdk`. Watch the progress in the lower right. Internet is needed |
| `No accessible RP-series devices in BOOTSEL mode were found` | The Pico was not in flashing mode and could not be switched automatically. This happens when MicroPython or a program that does not use USB is running. Hold BOOT while reconnecting, then Run |
| `LIBUSB_ERROR_ACCESS`, no permission | The udev rule is missing. Do Step 3 of Chapter 3, and unplug and replug the Pico |
| Flashing worked, but no port appears | The program lacks Console over USB (`pico_enable_stdio_usb`). Or it does not call `stdio_init_all()` |
| After flashing, Serial Monitor will not connect | The port disappeared once when the Pico restarted. Do Stop → Start Monitoring again |

## Build errors

In C++, there are two kinds of mistakes.

| Kind | When you find out | Examples |
| --- | --- | --- |
| Build errors | When you press Compile Project. They appear in VS Code's "Problems" panel and the terminal below | A missing `;`, a misspelled function name |
| Mistakes while running | After flashing. **No error appears**; it stops or gives strange values | Reading outside an array, not checking a sensor's return value |

### Reading build errors

```text
main.cpp:12:5: error: 'prinf' was not declared in this scope; did you mean 'printf'?
```

- `main.cpp:12:5` … line 12, character 5. In VS Code, click it in the "Problems" panel (Ctrl + Shift + M) to jump to that line
- `error:` … a mistake that stops the build. A `warning:` lets the build pass, but is often a mistake, so fix it too
- The last part … a detailed explanation. `did you mean` suggests what you may have meant

When there are many errors, fix them **starting from the top one**.

### Common build errors

| Error | Meaning and fix |
| --- | --- |
| `expected ';' before ...` | You forgot a `;`. Look at **the line before the one shown** |
| `'xxx' was not declared in this scope` | That name does not exist. Is it misspelled, or did you forget an `#include`? |
| `fatal error: xxx.h: No such file or directory` | That header does not exist. For your own `.h`, is it in the project folder? For an SDK header, did you add the library (`hardware_i2c` and so on) to `target_link_libraries` (Chapter 5)? |
| `undefined reference to 'xxx'` | The function is declared but has no body. Did you add the library (`pico_multicore` and so on) to `target_link_libraries` (Chapter 5)? |
| `expected '}' at end of input` | The numbers of `{` and `}` do not match |
| `invalid conversion from 'const char*' to 'char*'` | The types do not match. Add `const` |
| `narrowing conversion` | The type does not match when initializing with `{}`. Convert with `static_cast<type>(value)` |
| `region 'RAM' overflowed` | Not enough memory. Make large arrays smaller (Chapters 14 and 12) |
| Pico Studio's "C++ development environment" has a ✗ | Install what is missing (Chapter 3). The SDK and compiler are installed when you create your first project in VS Code |

### When it behaves strangely after flashing

| Symptom | Fix |
| --- | --- |
| Nothing appears in the output box | Do you call `stdio_init_all()`? Output right after start-up is lost, so put `sleep_ms(1500)` at the start |
| It stops partway, or the Pico does not respond | Are you writing outside an array, or making a large array inside a function (the stack overflows; Chapter 14)? With a watchdog, it restarts automatically when it hangs (Chapter 16) |
| The next flash cannot be done automatically | The previous program does not call `stdio_init_all()`, or it has stopped. Hold BOOT while reconnecting USB |
| A sensor value stays at 0 | Check the return value (a negative number from `i2c_read_blocking` is an error). The wiring and the I2C scan (Chapter 9) |
| Decimal calculations are slow | Use `float`, not `double`. Put `f` on numbers (`3.3f`). Use `sqrtf`, not `sqrt` |
| The LED does not light | Check the pin number (25 on the official Pico; see the documentation for compatible boards). On the Pico W, `cyw43_arch_gpio_put` (Chapter 7). For an external LED, its direction (long leg is +) and the resistor |
| A sensor value never changes | Did you forget the setting that wakes the sensor (0 to 0x6B for the MPU-6050)? |
| Values jump around a lot | Shorten the wiring, connect GND firmly, read several times and average |
| The button value jumps around | Did you forget `gpio_pull_up` (Chapter 8)? |

> When you cannot find the cause, stopping and investigating with a Debug Probe is quick (Chapter 5).

## When Pico Studio will not connect

| Symptom | Cause and fix |
| --- | --- |
| It says "見つかりません" (not found), or no port appears | The cable may be charge-only. Connect while holding BOOT and see whether it says "BOOTSEL モード". It also does not appear if a program that does not use USB is running |
| "ポートを開く権限がありません" (no permission to open the port) | The udev rule from Step 3 of Chapter 3 ("When it says no permission to open the port" in Chapter 6) |
| It connects, but nothing appears | Is another program, such as VS Code's Serial Monitor, using the same port? Does the program `printf` anything? |
| "MicroPython の応答がありません" (no response from MicroPython) | A C++ program is running on the Pico (check "動いているプログラム"). Or another program is using the port |
| "サーバーに接続できません" (cannot connect to the server) (upper left) | Pico Studio has stopped. Type `./start.sh` again in the terminal |
| "サーバーが古いままです" (the server is out of date) | You updated Pico Studio but the old server is still running. Stop it with Ctrl + C and run `./start.sh` |
| It disconnects right after connecting | Change the cable or USB port. If you use a USB hub, connect directly to the PC |

## Checking with commands whether the PC detects the Pico

Pico Studio's connection check also tells you, but you can check in the terminal too.

```bash
lsusb | grep 2e8a       # find the Raspberry Pi (ID 2e8a) lines in the list of USB devices
ls /dev/ttyACM*         # look for serial ports
lsblk -o NAME,LABEL | grep RP2   # look for the flashing-mode drive
```

| Result | State |
| --- | --- |
| `ID 2e8a:000a Raspberry Pi Pico` appears and `/dev/ttyACM0` exists | **A C++ program** (with Console over USB) is running |
| `ID 2e8a:0005 MicroPython Board in FS mode` appears and `/dev/ttyACM0` exists | **MicroPython** is running |
| `ID 2e8a:0003 Raspberry Pi RP2 Boot` (`2e8a:000f` on the Pico 2) appears and `RPI-RP2` (`RP2350` on the Pico 2) exists | **Flashing mode (BOOTSEL)**. VS Code's Run can flash it as is |
| No `2e8a` line at all | **Not detected**. A program that does not use USB is running, or there is a problem with the cable, the connection or the USB port |

`lsusb` is easiest to understand if you run it twice while unplugging and replugging the Pico, and see whether a line appears or disappears.
You can see the log at the moment of connection with `sudo dmesg -w` (stop with Ctrl+C).

Check whether the permissions are set with `ls -l /dev/ttyACM0`. If the line starts with a `+`, like `crw-rw----+`, it is OK.

## Last resort: returning the Pico to its initial state

For when you want to erase all of flash and start fresh (for example, when settings or records are broken and it stops at every start-up).

1. Download [flash_nuke.uf2](https://datasheets.raspberrypi.com/soft/flash_nuke.uf2)
2. Connect while holding the BOOT button and copy flash_nuke.uf2 to "RPI-RP2" (Pico Studio's ".uf2 ファイルを選ぶ" also works)
3. All of flash is erased (the flash records and settings from Chapters 14 and 16 are erased too)
4. Flash the program again with VS Code's Run Project (USB)

## Tips for looking things up

- Search for the error message (the part after `error:`) as it is
- Search combining "pico sdk" with the function name or error message
- For how to use a function, look up its name in the [Pico SDK API documentation](https://www.raspberrypi.com/documentation/pico-sdk/)
- For examples, look in the folder for the feature you want (i2c, adc, pwm and so on) in [pico-examples](https://github.com/raspberrypi/pico-examples)
- For the meaning of a function or argument, click the word in the code (Chapter 0)
