# 4. Creating and running a project in VS Code

This assumes the development environment from Chapter 3 is ready. If you follow this chapter, the LED on the board will blink and `printf` output will appear in VS Code.

## How it works

![How things work when developing C++ in VS Code](images/en/vscode-system.svg)

- A **project** is one folder and becomes one program (for example `~/apps/collar` → `collar.uf2`)
- The extension builds with the SDK, compiler and CMake in `~/.pico-sdk`, and flashes the Pico over USB with picotool
- With a Debug Probe, you can also flash over a wire called SWD, or stop at a line to investigate (Chapter 5)



## The development flow

![The development flow in VS Code](images/en/vscode-flow.svg)

① (Chapter 3) and ② are only done the first time. Normally you repeat "③ write → ④ build → ⑤ flash → ⑥ view output".

## The development folder

![The development folder and GitHub](images/en/vscode-github.svg)

- **One product (program) is one project**. A project is one folder, and on GitHub it is one repository
- Keep them all at **`~/apps/name`** (for example `~/apps/collar`). If you choose `~/apps` as the Location in New C/C++ Project, a folder with the name is created inside it
- **The order is "create in VS Code → put on GitHub"**. The extension creates the folder and files (including `.gitignore`), so it is easier to create first and then put it on GitHub
- For **practice** with Chapters 8–17 of this guide, it is handy to create one project such as `~/apps/pico-practice` and replace the contents of the `.cpp` for each chapter (it does not need to go on GitHub)
- Create a separate project for the product's program, apart from the practice one, and put it on GitHub

When working in the terminal, stay in this folder. The terminal inside VS Code (View → Terminal) opens in the project folder from the start.

## ② Create a new project

Click the Pico icon on the left and press **New C/C++ Project** in Quick Access to open the project creation screen.

![The New C/C++ Project screen (illustration)](images/en/vscode-new-project.svg)

| No. | Item | What to choose |
| --- | --- | --- |
| ① | Name | The project name (for example `blink`). It becomes the name of the folder and the program. Use only letters, digits and `_` |
| ② | Board type | The type of board. **Pico** for the official Pico, **Pico 2** for the Pico 2, **Pico W** for the Pico W |
| ③ | Location | Where to create it. Choose **`/home/username/apps`** and you get `~/apps/blink` |
| ④ | Pico SDK version | The SDK version. The newest is fine |
| ⑤ | Features | Features to use (SPI, I2C, UART, PIO, DMA, HW watchdog, HW timer, HW clocks and others). Choosing them adds libraries to `CMakeLists.txt` and inserts example code. You can add them later too |
| ⑥ | Stdio support | **Check Console over USB**. `printf` reaches the PC over USB. You can uncheck Console over UART |
| ⑦ | Code generation options | **Check Generate C++ code** (you get a `.cpp`). **Leave Use project name as entry point file name checked** (you get `blink.cpp`; unchecked gives `main.cpp`). Leave Run the program from RAM rather than flash, Enable C++ exceptions and RTTI unchecked (Chapter 13) |
| ⑧ | Debugger | If you use a Debug Probe, **DebugProbe (CMSIS-DAP)** (the default is fine) |

Finally, press **Create**. VS Code reopens the newly created project folder.

- **The first time, it downloads the SDK and compiler into `~/.pico-sdk`, so it takes a few minutes** (progress is shown in the lower right)
- You can leave **CMake Tools** (Enable CMake-Tools extension integration) in the lower right unchecked. Building and flashing are done with the Pico extension's Compile and Run
- **⑥ Console over USB is very important.** If you flash a program without USB output, you will need to press the BOOT button the next time you flash
- Item names and order may differ slightly depending on the extension version (this figure is from 0.23.0)

### The files that are created

In the tree below, **`name`** becomes the name you gave in ① **Name**. If Name is `blink`, you get `~/apps/blink/` and `blink.cpp`; if it is `collar`, you get `~/apps/collar/` and `collar.cpp`.

**Always created**

```text
~/apps/name/                     The project folder
├── name.cpp                     Your program. Write here
├── CMakeLists.txt              Build settings (explained below)
├── pico_sdk_import.cmake       Loads the SDK
├── .gitignore                  What not to put in git (the build folder)
├── .vscode/                    Extension settings (normally do not touch)
│   ├── settings.json           VS Code settings
│   ├── tasks.json              What Compile and Run do
│   ├── launch.json             Debug settings
│   ├── c_cpp_properties.json   Completion settings
│   ├── cmake-kits.json         The compiler used by CMake Tools
│   └── extensions.json         A list of recommended extensions
└── build/                      Intermediate build files and the finished program (④)
```

- `name.cpp` becomes `main.cpp` if you uncheck **Use project name as entry point file name** in ⑦, and becomes `.c` if you uncheck **Generate C++ code**
- The program name in `CMakeLists.txt` and the name of the resulting `.uf2` also come from ① Name
- `build/` is created when the extension opens the project, and the `.uf2` and others appear after you Compile. What is inside is explained in ④

**Created only when chosen**

| File | When it is created |
| --- | --- |
| `blink.pio` | When you choose **PIO interface** in ⑤. An example PIO program. Always this name, regardless of Name |
| `lwipopts.h` | When the Board type is Pico W and you choose **Polled lwIP** or **Background lwIP** under **Pico wireless options**. Network settings |
| `raspberrypi-swd.cfg` | When you choose **SWD (Pi host)** in ⑧. Settings for flashing over SWD from a Raspberry Pi's GPIO |

The heart of `CMakeLists.txt` is the following part (an example with Name set to `blink`; `blink` becomes your own name).

```cmake
# == DO NOT EDIT THE FOLLOWING LINES for the Raspberry Pi Pico VS Code Extension to work ==
# (lines that set the SDK version and location; do not delete or change them)
# ...

add_executable(blink blink.cpp)

pico_enable_stdio_uart(blink 0)
pico_enable_stdio_usb(blink 1)

target_link_libraries(blink
        pico_stdlib)
```

| Line | Meaning |
| --- | --- |
| The `DO NOT EDIT` part | The extension sets the locations of the SDK and compiler here. Do not touch |
| `add_executable(blink blink.cpp)` | Makes a program called `blink` from `blink.cpp` |
| `pico_enable_stdio_usb(blink 1)` | Sends `printf` to the PC over USB |
| `target_link_libraries(blink pico_stdlib)` | The libraries used. Add `hardware_i2c` if you use I2C (the table in Chapter 5) |

## Putting it on GitHub

Put a product project on GitHub right after you create it. Your code survives even if your PC breaks, and you can go back to an earlier state from the history.

### With VS Code's buttons

1. Open **Source Control** on the left (the branching icon)
2. Press **Publish to GitHub**. The first time, you are asked to sign in to GitHub
3. Choose **Publish to GitHub private repository**
4. When asked which files to upload, just press OK

### With commands

If you use the GitHub CLI (`gh`), typing the following in the terminal does the same.

```bash
cd ~/apps/collar
git init
git add .
git commit -m "First version"
gh repo create collar --private --source=. --push
```

- Because of the `.gitignore` the extension made, the `build` folder (build output) is not uploaded
- Upload `.vscode/` and `CMakeLists.txt`. Then the project opens with the same settings on another PC
- For everyday commits and pushes, see "Managing versions with git" in Chapter 5
- For first-time settings (name and email address), making SSH keys, and connecting to a repository made on the GitHub website, see the [GitHub Textbook](https://yusuke1090.github.io/textbooks/?b=github)

### Continuing development on another PC

```bash
cd ~/apps
git clone https://github.com/username/collar.git
code collar
```

Open the folder in VS Code and press Compile and Run to carry on (if that PC does not have the extension yet, install it as in Chapter 3; the extension downloads the SDK and anything else needed).

To clone a private repository, you need to be logged in to GitHub on that PC too (`gh auth login`, or a registered SSH key). Once you register an SSH key, use the URL `git@github.com:username/collar.git`. For a Raspberry Pi or Jetson that only fetches code, you can use a read-only key (a deploy key). For details, see Chapter 9 of the [GitHub Textbook](https://yusuke1090.github.io/textbooks/?b=github).

## ③ Write (blinking LED)

A freshly created `name.cpp` (`blink.cpp` if Name is `blink`) only prints `Hello, world!`; **it has no code to drive the LED**. Delete everything in it and paste in the following program. It turns the board's LED (GP25) on and off every 0.5 seconds and reports each change with `printf` as `LED ON` / `LED OFF`.

```cpp run
#include <cstdio>
#include "pico/stdlib.h"

constexpr uint LED_PIN = 25;      // the official Pico's LED is GP25

int main() {
    stdio_init_all();             // allow printf to be sent over USB
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);

    bool on = false;
    while (true) {
        on = !on;
        gpio_put(LED_PIN, on);
        printf("LED %s\n", on ? "ON" : "OFF");
        sleep_ms(500);
    }
}
```

Chapter 8 explains what it means.

- When you start typing a function name, candidates appear (completion). Type `gpio_` to see a list of the GPIO functions
- If there is a mistake, a red wavy underline appears **before you even build**

> If the Board type in ② is Pico W, the LED is turned on differently (Chapter 8). The ordinary Pico (RP2040) and the Pico 2 work as is.

## ④ Build

Press **Compile Project** in Quick Access (or **Compile** in the bar at the bottom).
Progress appears in the "Terminal" below, and finally `build/name.uf2` (for example `build/blink.uf2`) is made.

- **Success**: the last line is something like `[54/54] Linking CXX executable blink.elf` (if nothing changed, `ninja: no work to do.`)
- **Failure**: `FAILED:` and `ninja: build stopped: subcommand failed.` appear. The `error:` lines above them tell you the cause

- The first time builds the whole SDK, so it takes 1–2 minutes. After that, only what changed is rebuilt, so it takes a few seconds
- Errors are also listed in the "Problems" panel (Ctrl + Shift + M); click one to jump to that line. How to read errors is in Appendix B

### What is in the build folder

The files in `build/` are made at **two different times**. You never edit any of them yourself.

![The build folder after Compile (when Name is check_how_to_use; the boxes mark .elf and .uf2, the ones you normally use)](images/build-folder.png)

**Made on every Compile (the finished program)**

| File | What it is |
| --- | --- |
| `name.uf2` | The file to flash to the Pico. You can also drag it onto the `RPI-RP2` drive that appears when you plug in while holding BOOT |
| `name.elf` | The program itself, with debugging information. Run flashes this (the `picotool load … .elf` in the terminal in ⑤). The debugger uses it too |
| `name.bin` | Just the contents to flash, laid out as is |
| `name.hex` | The same contents as `.bin`, written as text (Intel HEX format) |
| `name.dis` | The machine code turned into a readable form (assembly). Shows what instructions your C++ became |
| `name.elf.map` | Where in memory each function and variable was placed, and how many bytes it takes. Look at it when you run out of space |
| `.ninja_log`, `.ninja_deps` | A record of which files need rebuilding. This is why the second Compile is fast |

Normally you only use `.uf2` and `.elf`. `.bin` and `.hex` are for other flashing tools.

**Made when CMake prepares the build (intermediate files)**

CMake makes these when the extension opens the project, and again when you change `CMakeLists.txt`.

| File | What it is |
| --- | --- |
| `CMakeCache.txt` | Notes on the settings CMake decided (board type, where the SDK and compiler are, and so on) |
| `build.ninja` | The build instructions. When you press Compile, ninja builds by following it |
| `compile_commands.json` | How each file is compiled. VS Code's completion and red wavy underlines (③) use it |
| `CMakeFiles/` | Intermediate files (`.o` files, your `.cpp` turned into machine code, and so on) |
| `pico-sdk/` | Intermediate files for building parts of the SDK |
| `generated/` | Headers the SDK generated (the SDK version and so on) |
| `cmake_install.cmake` | For installing. Not used on the Pico |

You can delete `build/` entirely (it is not put on GitHub either). If the build behaves strangely, press **Clean CMake** in Quick Access: it deletes `build/` and starts again from the preparation step.

## ⑤ Flash

Connect the Pico by USB and press **Run Project (USB)** in Quick Access (or **Run** in the bar at the bottom).
picotool puts the Pico into flashing mode and flashes it, the Pico restarts and the program starts running. If the LED on the board blinks, it worked.

**What is currently running on the Pico** decides whether you need the BOOT button.

| What is running on the Pico | With Run Project (USB) |
| --- | --- |
| A C++ program (with Console over USB) | It can be flashed as is. No BOOT needed |
| Flashing mode (`RPI-RP2` is visible) | It can be flashed as is |
| MicroPython (when new, or after using Appendix E) | It cannot be put into flashing mode automatically. **Hold BOOT while plugging in USB**, then press Run |
| A C++ program that does not use USB | The same: hold BOOT while plugging in, then press Run |

You can tell what is running from the **Port name** in the Serial Monitor in ⑥ (the part after `/dev/ttyACM0 - `). `Raspberry Pi` means a C++ program, and `MicroPython` means MicroPython. Pico Studio's connection check (Chapter 6) tells you too.

### Reading the terminal below

When you press Run, the "Terminal" below shows something like this. **If `The device was rebooted to start the application.` appears, it worked.**

![The terminal after a successful Run (the box marks the sign of success)](images/run-terminal.png)

| Line | Meaning |
| --- | --- |
| `Executing task: … picotool load … -fx` | picotool started flashing |
| `Tracking device serial number …` | It noted the Pico's serial number so it does not lose track of it across the restart |
| `The device was asked to reboot into BOOTSEL mode …` | It switched the Pico into flashing mode (instead of the BOOT button; not shown if you plugged in holding BOOT) |
| `Loading into Flash: … 100%` | Flashing. 100% means it is done |
| `The device was rebooted to start the application.` | **Success.** The Pico restarted and the program is running |
| `Terminal will be reused by tasks …` | The end marker (also shown on failure). Press any key to close it |

On **failure**, `rebooted to start the application` does not appear, and it ends with `The terminal process … terminated with exit code: 1.` The message above that tells you the cause.

| Message | Cause and fix |
| --- | --- |
| `… appears to be an RP-series MicroPython device not in BOOTSEL mode.` | MicroPython is running. See "A real example" below |
| Only `No accessible RP-series devices in BOOTSEL mode were found.` | The Pico is not connected (a charge-only cable, for example), or a program that does not use USB is running. Hold BOOT while replugging, then Run |
| `… picotool was unable to connect. Maybe try 'sudo' or check your permissions.` | No permission. Install the udev rules from Step 3 of Chapter 3 and unplug and replug the Pico |

### A real example: the LED did not blink

| What we found | What we did |
| --- | --- |
| The `.cpp` was still as created, and only printed `Hello, world!` | Replaced it with the program in ③ |
| The Pico had MicroPython on it, and flashing with Run failed (the Serial Monitor Port said `MicroPython`) | Typed `mpremote bootloader` in the terminal to put the Pico into flashing mode (Appendix A), then pressed Run. Replugging while holding BOOT also works |

The board was an ordinary Pico (RP2040, not a W), so Pico was the right Board type in ②.
Once a C++ program is on the Pico, from then on you can flash with just Run, with no BOOT button or command.

## ⑥ View the output

View `printf` output in one of the following ways.

**VS Code's Serial Monitor** (needs the Serial Monitor extension; Chapter 3)

This is where the text your Pico program prints with `printf` shows up (`print()` in MicroPython). Output from the PC's terminal does not appear here.

![Serial Monitor (the numbers match the steps below; in this photo the Port says MicroPython)](images/serial-monitor.png)

1. Open the **Serial Monitor** tab in the bottom panel (if you cannot see it, open View → Terminal first and look for it)
2. Choose `/dev/ttyACM0` as the **Port**. After flashing, press the ↻ to its right and check that the name has become `Raspberry Pi` (if it still says `MicroPython`, the program has not been flashed yet; see ⑤)
3. Leave the **Baud rate** at `115200`
4. Press **Start Monitoring** → lines like the following scroll by in the black area below, and the button changes to **Stop Monitoring**

```text
---- Opened the serial port /dev/ttyACM0 ----
LED ON
LED OFF
LED ON
```

You can leave Monitor Mode, View Mode and Line ending as they are.

**Pico Studio** (Chapter 6)

1. Choose the port and press "接続" (Connect) → `LED ON` / `LED OFF` scroll by in the output box

> **A port can only be used by one program at a time.** Before flashing, press **Stop Monitoring** in Serial Monitor, or "切断" (Disconnect) in Pico Studio. If it stays open, it may not reconnect after flashing. After flashing, do steps 2–4 again.

## Change the program and try again

In the `name.cpp` you pasted in ③ (for example `blink.cpp`), change the last line inside `while`, `sleep_ms(500);`, to `sleep_ms(100);`. `sleep_ms(500)` means "wait 500 milliseconds (0.5 seconds)", so with 100 the LED switches every 0.1 seconds.

```cpp
    while (true) {
        on = !on;
        gpio_put(LED_PIN, on);
        printf("LED %s\n", on ? "ON" : "OFF");
        sleep_ms(100);            // change 500 → 100
    }
```

Save (Ctrl + S) → Compile → Run, and the LED blinks faster, and `LED ON` / `LED OFF` scroll by faster in the Serial Monitor.
This is the everyday development loop.

### When trying code from Chapter 8 onward

- Try it by replacing the contents of the `.cpp` in your practice project (`~/apps/pico-practice` or the like)
- For code that uses I2C and so on, add the library to `target_link_libraries` (the table in Chapter 5)
- When using headers that come with Pico Studio, such as `mpu6050.h` in Chapter 11, copy them into your project folder

```bash
# replace blink with your own project's name
cp ~/apps/pico-studio/cpp/include/*.h ~/apps/blink/
```

## Summary

- One product is one project. Create it at `~/apps/name`, and put product projects on GitHub (create in VS Code → Publish to GitHub)
- Create it with **New C/C++ Project**, with Location `~/apps` and Console over USB and Generate C++ code checked
- Normally you repeat "write → Compile → Run (USB) → Serial Monitor"
- Flashing worked if the terminal shows `The device was rebooted to start the application.`
- For a Pico running MicroPython, or a program that does not use USB, hold BOOT while plugging in, then Run (for MicroPython, `mpremote bootloader` also works)
- A port can only be used by one program. Stop Serial Monitor or Pico Studio before flashing

## Exercises

```quiz
Q: Which VS Code menu item creates a new Pico project?
A: New C/C++ Project | New C++ Project
E: Set the location to `~/apps` and tick Console over USB and Generate C++ code.

Q: The daily loop is "write → Compile → ? → Serial Monitor". What is "?"?
A: Run | Run (USB) | Run Project (USB)
E: Compile builds; Run writes the program to the Pico.

Q: How many programs can use one serial port at the same time?
A: 1 | one
E: Stop Serial Monitor or Pico Studio before writing.

Q: When the Pico is running MicroPython, which button do you hold while plugging in before running C++?
A: BOOT | BOOTSEL
E: The same goes for programs that do not use USB.
```
