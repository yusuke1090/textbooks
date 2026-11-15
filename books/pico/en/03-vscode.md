# 3. Creating and running a project in VS Code

## What you will learn

- How things work when you develop with the VS Code extension
- Where to keep your development folders, and how to put them on GitHub
- How to create a new project, and what the generated files mean
- The flow of write → build → flash → view output
- Getting your first program (a blinking LED) running

This assumes the development environment from Chapter 2 is ready. If you follow this chapter, the LED on the board will blink and `printf` output will appear in VS Code.

## How it works

![How things work when developing C++ in VS Code](images/en/vscode-system.svg)

- A **project** is one folder and becomes one program (for example `~/apps/collar` → `collar.uf2`)
- The extension builds with the SDK, compiler and CMake in `~/.pico-sdk`, and flashes the Pico over USB with picotool
- With a Debug Probe, you can also flash over a wire called SWD, or stop at a line to investigate (Chapter 4)



## The development flow

![The development flow in VS Code](images/en/vscode-flow.svg)

① (Chapter 2) and ② are only done the first time. Normally you repeat "③ write → ④ build → ⑤ flash → ⑥ view output".

## The development folder

![The development folder and GitHub](images/en/vscode-github.svg)

- **One product (program) is one project**. A project is one folder, and on GitHub it is one repository
- Keep them all at **`~/apps/name`** (for example `~/apps/collar`). If you choose `~/apps` as the Location in New C/C++ Project, a folder with the name is created inside it
- **The order is "create in VS Code → put on GitHub"**. The extension creates the folder and files (including `.gitignore`), so it is easier to create first and then put it on GitHub
- For **practice** with Chapters 6–15 of this guide, it is handy to create one project such as `~/apps/pico-practice` and replace the contents of the `.cpp` for each chapter (it does not need to go on GitHub)
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
| ⑦ | Code generation options | **Check Generate C++ code** (you get a `.cpp`). **Leave Use project name as entry point file name checked** (you get `blink.cpp`; unchecked gives `main.cpp`). Leave Run the program from RAM rather than flash, Enable C++ exceptions and RTTI unchecked (Chapter 11) |
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
└── build/                      Build output (name.uf2 and others, after Compile)
```

- `name.cpp` becomes `main.cpp` if you uncheck **Use project name as entry point file name** in ⑦, and becomes `.c` if you uncheck **Generate C++ code**
- The program name in `CMakeLists.txt` and the name of the resulting `.uf2` also come from ① Name
- `build/` is created along with the project, and the `.uf2` appears after you Compile

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
| `target_link_libraries(blink pico_stdlib)` | The libraries used. Add `hardware_i2c` if you use I2C (the table in Chapter 4) |

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
- For everyday commits and pushes, see "Managing versions with git" in Chapter 4
- For first-time settings (name and email address), making SSH keys, and connecting to a repository made on the GitHub website, see the [GitHub Textbook](https://yusuke1090.github.io/textbooks/?b=github)

### Continuing development on another PC

```bash
cd ~/apps
git clone https://github.com/username/collar.git
code collar
```

Open the folder in VS Code and press Compile and Run to carry on (if that PC does not have the extension yet, install it as in Chapter 2; the extension downloads the SDK and anything else needed).

To clone a private repository, you need to be logged in to GitHub on that PC too (`gh auth login`, or a registered SSH key). Once you register an SSH key, use the URL `git@github.com:username/collar.git`. For a Raspberry Pi or Jetson that only fetches code, you can use a read-only key (a deploy key). For details, see Chapter 8 of the [GitHub Textbook](https://yusuke1090.github.io/textbooks/?b=github).

## ③ Write (blinking LED)

Open `name.cpp` (`blink.cpp` if Name is `blink`), delete everything in it, and paste in the following program. It blinks the board's LED (GP25) and reports each change with `printf`.

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

Chapter 6 explains what it means.

- When you start typing a function name, candidates appear (completion). Type `gpio_` to see a list of the GPIO functions
- If there is a mistake, a red wavy underline appears **before you even build**

> On a Pico W, the LED is turned on differently (Chapter 6).

## ④ Build

Press **Compile Project** in Quick Access (or **Compile** in the bar at the bottom).
Progress appears in the "Terminal" below, and finally `build/name.uf2` (for example `build/blink.uf2`) is made.

- The first time builds the whole SDK, so it takes 1–2 minutes. After that, only what changed is rebuilt, so it takes a few seconds
- Errors are also listed in the "Problems" panel (Ctrl + Shift + M); click one to jump to that line. How to read errors is in Appendix B

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

You can see what is running with Pico Studio's connection check (Chapter 5).

> If you see "device not found" or "no permission (LIBUSB_ERROR_ACCESS)", install the udev rules from Step 3 of Chapter 2 and unplug and replug the Pico.

## ⑥ View the output

View `printf` output in one of the following ways.

**VS Code's Serial Monitor** (needs the Serial Monitor extension; Chapter 2)

1. Open the **SERIAL MONITOR** tab in the bottom panel (if you cannot see it, open View → Terminal first and look for it)
2. Choose `/dev/ttyACM0` as the Port and `115200` as the Baud rate
3. Press **Start Monitoring** → `LED ON` / `LED OFF` scroll by

**Pico Studio** (Chapter 5)

1. Choose the port and press "接続" (Connect) → `LED ON` / `LED OFF` scroll by in the output box

> **A port can only be used by one program at a time.** Before flashing, press **Stop Monitoring** in Serial Monitor, or "切断" (Disconnect) in Pico Studio. If it stays open, it may not reconnect after flashing.

## Change the program and try again

Change `sleep_ms(500)` to `sleep_ms(100)`, save (Ctrl + S) → Compile → Run, and the LED blinks faster.
This is the everyday development loop.

### When trying code from Chapter 6 onward

- Try it by replacing the contents of the `.cpp` in your practice project (`~/apps/pico-practice` or the like)
- For code that uses I2C and so on, add the library to `target_link_libraries` (the table in Chapter 4)
- When using headers that come with Pico Studio, such as `mpu6050.h` in Chapter 9, copy them into your project folder

```bash
# replace blink with your own project's name
cp ~/apps/pico-studio/cpp/include/*.h ~/apps/blink/
```

## Summary

- One product is one project. Create it at `~/apps/name`, and put product projects on GitHub (create in VS Code → Publish to GitHub)
- Create it with **New C/C++ Project**, with Location `~/apps` and Console over USB and Generate C++ code checked
- Normally you repeat "write → Compile → Run (USB) → Serial Monitor"
- For a Pico running MicroPython, or a program that does not use USB, hold BOOT while plugging in, then Run
- A port can only be used by one program. Stop Serial Monitor or Pico Studio before flashing
