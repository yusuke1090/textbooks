# Appendix C. Comparing the Raspberry Pi and the Pico

Here, "Raspberry Pi" means a board that runs Linux, such as the Raspberry Pi 4 or 5. A Jetson can be thought of in the same way.

## The biggest difference

**The Pico has no Linux.** There is nothing to log in to, and no system for managing services.
When the power comes on, only the one program you flashed runs. Within that one program, you can move several tasks forward (Chapters 14 and 15).

| Item | Raspberry Pi | Pico |
| --- | --- | --- |
| OS | Linux | None (your program runs directly) |
| Programs running | Many at once | One |
| Memory | Several GB | 264 KB (520 KB on the Pico 2) |
| Storage | Tens of GB on an SD card or the like | 2 MB (both the program and records go here) |
| Power consumption | Several watts | Around 0.1 W (even less when asleep) |
| Start-up time | Tens of seconds | An instant |
| Sudden power loss | Files can be corrupted | Basically no problem. Data being written may be lost |
| Analog input (ADC) | None (needs an external part) | Yes |
| Network | Wired and wireless | None (the Pico W has wireless) |

The numbers are rough guides.

![The Raspberry Pi family (Pi 400, Pi 1, Pi 5, Zero 2, Pico)](images/pi-family.jpg)

## A table of corresponding tasks

| Task | Raspberry Pi | Pico (C++) |
| --- | --- | --- |
| Connect | `ssh pi@raspberrypi.local` | Connect by USB |
| Build | `g++` or CMake on the Raspberry Pi | Build **on the PC** (VS Code's Compile; cross-compiling) |
| Send the program | Send the executable with `scp` | Flash the `.uf2` (VS Code's Run) |
| Run automatically at start-up | A systemd service | The flashed program always runs |
| Stop | Ctrl + C, `systemctl stop` | There is no stop operation. Flash a different program |
| Restart | `sudo systemctl restart` | The RST button, unplugging and replugging USB |
| View logs | `journalctl -u logger` | View `printf` in Serial Monitor. To keep them, write to flash (Chapter 16) |
| Restart automatically after a crash | `Restart=always` in the service | The watchdog (`watchdog_enable`, Chapter 18) |
| Install libraries | `apt install`, `pip install` | Add Pico SDK components to `CMakeLists.txt` (Chapter 5). Put other libraries' source into the project |
| Debug | `gdb` | A Debug Probe (SWD) and gdb (Chapters 5 and 20) |
| Update the OS | `sudo apt upgrade` | None (raise the SDK version and rebuild) |
| Shell scripts | Kept on the Raspberry Pi | Kept on the PC (Appendix A) |

## Differences from C++ on the Raspberry Pi

If you have written C++ on a Raspberry Pi, watch out for the following differences.

| Item | Raspberry Pi (C++ on Linux) | Pico (Pico SDK) |
| --- | --- | --- |
| What you can use | The whole standard library, exceptions, `std::thread`, files | Part of the standard library. No exceptions, `std::thread` or files (Chapter 14) |
| Memory | Use `new` and `std::vector` without worrying | Fix sizes and place things outside functions (Chapters 14 and 16) |
| Several tasks | Threads, processes | Move forward in turn by looking at the time (Chapter 14), interrupts, the two cores (Chapter 15) |
| Driving pins | Operated like files, with `libgpiod` and the like | Drive the hardware directly with `gpio_put` and the like (Chapter 8) |
| I2C | Open `/dev/i2c-1` and use `ioctl` | `i2c_write_blocking` / `i2c_read_blocking` (Chapter 12) |
| Time | `std::chrono`, `sleep` | `sleep_ms`, `get_absolute_time` (Chapter 12) |
| When it stops with an error | The OS reports it, and the service restarts | It stops without saying anything. Restart with the watchdog (Chapter 18) |

Comparing a blinking LED gives the following.

Raspberry Pi (an example using libgpiod, with an LED on GPIO17):

```text
gpiod::chip chip("gpiochip0");
auto line = chip.get_line(17);
line.request({"blink", gpiod::line_request::DIRECTION_OUTPUT, 0});
while (true) {
    line.set_value(1); std::this_thread::sleep_for(500ms);
    line.set_value(0); std::this_thread::sleep_for(500ms);
}
```

Pico (the same as Chapter 8):

```cpp
gpio_init(25);
gpio_set_dir(25, GPIO_OUT);
while (true) {
    gpio_put(25, 1); sleep_ms(500);
    gpio_put(25, 0); sleep_ms(500);
}
```

## Where Linux habits trip you up

- **When `main` ends, it does nothing.** Repeat with `while (true)` (Chapter 8)
- **`printf` output is not kept.** You only see it while connected by USB and watching. To keep it, write to flash (Chapter 16)
- **When it stops with an error, nothing appears.** Add a watchdog and error records (Chapters 18 and 20)
- **Write to flash sparingly.** The number of write cycles is limited (Chapter 16)
- **A port can only be used by one program at a time.** Unlike ssh, you cannot have several connections at once
- **Making a large array inside a function breaks things.** The stack is only a few KB (Chapter 14)

## Which to use

| Purpose | Better suited |
| --- | --- |
| Running for a long time on batteries | Pico |
| Reading sensors precisely at fixed intervals | Pico |
| Using it where the power may be cut suddenly | Pico |
| Handling camera images | Raspberry Pi |
| Running large machine learning models | Raspberry Pi, Jetson |
| Running a web server or database | Raspberry Pi |

You can also combine the two: the Pico reads sensors in the field, and the Raspberry Pi receives the data and stores and analyzes it (Chapter 19). Passing data over USB is in Chapter 16.

## Summary

- The Pico has no Linux. Build on the PC and flash the `.uf2`
- What corresponds to a systemd service is the flashed program itself. Restarting after a crash is done by the watchdog
- Even in C++, do not use exceptions, threads, files or a large heap
- The Pico suits power saving and reading sensors; the Raspberry Pi suits heavy processing
