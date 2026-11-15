# 4. Getting more out of VS Code

## What you will learn

- What each item in the Quick Access menu means
- Features that help you write (completion, go to definition, the problems list)
- How to add libraries, and how to split files
- How to stop at a line and investigate with a Debug Probe
- Version control with git
- Recommended extensions
- When to use VS Code and when to use Pico Studio

This assumes you have created a project and got the blinking LED running in Chapter 3.

## The Quick Access menu

![Quick Access in Raspberry Pi Pico](images/vscode-quick-access.png)

### General (creating projects)

| Menu item | What it does |
| --- | --- |
| New C/C++ Project | Creates a new C / C++ project (Chapter 3) |
| New MicroPython Project | Creates a MicroPython project. This guide tries MicroPython in Pico Studio (Appendix E), so you do not need it |
| New Rust Project | Creates a project in Rust (another language) |
| New Zephyr Project | Creates a project for Zephyr (an OS for microcontrollers) |
| Import Project | Makes an existing CMake project usable with the extension |
| New Project From Example | Creates a project chosen from the official examples (pico-examples), such as `blink`, `hello_usb` and `i2c/bus_scan` |
| Manage Components | Adds or removes versions of the SDK, compiler and so on in `~/.pico-sdk` |

### Project (operations on the open project)

These are grayed out when no project folder is open.

| Menu item | What it does | Used normally? |
| --- | --- | --- |
| Debug Project | Flashes with a Debug Probe and starts debugging ("Debugging" below) | If you have a Debug Probe |
| Compile Project | Builds (Chapter 3) | **Often** |
| Run Project (USB) | Flashes over USB and runs (Chapter 3) | **Often** |
| Flash Project (SWD) | Flashes with a Debug Probe (without debugging) | If you have a Debug Probe |
| Configure CMake | Reloads `CMakeLists.txt`, for example after adding files | Sometimes |
| Clean CMake | Deletes `build` and builds again. When strange errors persist | Sometimes |
| Switch Build Type | Switches between Debug (easy to investigate) and Release (fast and small) | Release for products |
| Switch SDK | Changes the SDK version | Rarely |
| Switch Board | Changes the board type (Pico → Pico 2 and so on) | When you change boards |
| Debug Layout | Arranges the screen for debugging | When debugging |

### Documentation (viewing explanations)

| Menu item | Contents |
| --- | --- |
| Hardware APIs | Explanations of functions such as `hardware_gpio` and `hardware_i2c` that operate the Pico's parts directly |
| High Level APIs | Explanations of easier, bundled functions such as `pico_stdlib` and `pico_multicore` |
| Networking Libraries | Explanations of the Pico W's WiFi and Bluetooth |
| Runtime Infrastructure | Explanations of how startup works, where `printf` output goes and more |

When you are unsure how to use a function, look here (the same as the "Pico SDK API documentation" in Appendix D).

## Features that help you write

| Action | What it does |
| --- | --- |
| Start typing a function name | Candidates appear (completion). Insert with Tab or Enter. `gpio_`, `i2c_`, `adc_` and so on show lists |
| Hover over a function name | Shows its arguments and description |
| **F12** (or Ctrl + click) | Jumps to the function's code (the SDK source). Alt + ← goes back |
| Shift + F12 | Lists where the function or variable is used |
| F2 | Renames all at once (everywhere it is used) |
| Ctrl + Shift + M | The "Problems" list (errors and warnings). Click to go to the line |
| Ctrl + P | Find and open a file by name |
| Ctrl + Shift + F | Search for text across the whole folder |

> Red wavy underlines sometimes appear even on correct code. Compiling once creates the completion settings (`build/compile_commands.json`) and fixes it. If they still appear, Clean CMake → Compile.

## Adding libraries

When you use I2C, ADC and so on, add libraries to `target_link_libraries` in `CMakeLists.txt`.

```cmake
target_link_libraries(collar
        pico_stdlib
        hardware_i2c
        hardware_adc)
```

| What you use | Library to add | Chapter |
| --- | --- | --- |
| GPIO, time, `printf` | `pico_stdlib` (included from the start) | Chapter 6 |
| ADC (analog input, built-in temperature sensor) | `hardware_adc` | Chapter 7 |
| PWM | `hardware_pwm` | Chapter 7 |
| I2C / SPI / UART | `hardware_i2c` / `hardware_spi` / `hardware_uart` | Chapters 8–9 |
| PIO (the RGB LED in `ws2812.h`) | `hardware_pio` (and `hardware_clocks`) | Chapter 6 |
| Writing to flash | `hardware_flash` | Chapters 13, 15 |
| The second core | `pico_multicore` | Chapter 12 |
| Watchdog | `hardware_watchdog` | Chapter 15 |
| Changing the CPU clock | `hardware_clocks` | Chapter 15 |
| A number for each unit (unique ID) | `pico_unique_id` | Chapter 17 |
| The Pico W's LED | `pico_cyw43_arch_none` | Chapter 6 |

If you forget to add one, building gives `fatal error: hardware/i2c.h: No such file or directory` or `undefined reference to ...`.
Saving reloads the CMake settings automatically. If it does not work, press **Configure CMake** in Quick Access.

## Splitting files

When the program gets long, split it into files (how to think about splitting is in Chapter 11).

```text
~/apps/collar/
├── collar.cpp       main. Only the overall flow
├── mpu6050.h        The sensor class (Chapter 9)
├── features.h       Feature calculation (Chapters 14, 17)
├── model.h          Classification (made by train.py in Chapter 14)
├── radio.h          Sending
└── radio.cpp        The sending code
```

- A `.h`-only file can be used just by writing `#include "features.h"`. There is no need to change `CMakeLists.txt`
- When you add a `.cpp`, add it to `add_executable`

```cmake
add_executable(collar collar.cpp radio.cpp)
```

## Debugging (when you have a Debug Probe)

With a Debug Probe (an official Raspberry Pi tool), you can stop the program at any line and investigate while watching variable values. Use it to find mistakes that `printf` alone cannot reveal.

### How to connect

| Debug Probe | Pico |
| --- | --- |
| The three wires of D (SWD) | The three **DEBUG** pins at the bottom edge of the Pico (SWCLK, GND, SWDIO) |
| USB | PC |

The Pico's DEBUG pins need pin headers soldered on (the Pico H has them from the start).
Without a Debug Probe, you can also use a second Pico as a Debug Probe ([debugprobe](https://github.com/raspberrypi/debugprobe)).

### How to use it

1. When creating the project, choose **DebugProbe** as the Debugger (the default setting)
2. Connect the Debug Probe to the PC and the Pico. Keep the Pico's USB connected too, for power and `printf`
3. Click in the margin to the left of the line where you want to stop, to add a red dot (a breakpoint)
4. Press **Debug Project** in Quick Access (or **F5**)
5. The program is flashed and stops at the line with the red dot

| Key | What it does |
| --- | --- |
| F5 | Continue to the next breakpoint |
| F10 | Go one line forward (without going into functions) |
| F11 | Go one line forward (going into functions) |
| Shift + F5 | Stop debugging |

- While stopped, you can see variable values in the "Variables" panel on the left. You can also hover over a variable
- Building as Debug makes the match between lines and instructions clearer (Switch Build Type). With Release, lines can seem to jump

## Debug and Release

Switch the build type with **Switch Build Type** in Quick Access.

| Type | Features | When to use it |
| --- | --- | --- |
| Debug | Clear match between lines and instructions. A little slower and larger | When debugging |
| Release | Fast and small. In debugging, lines can seem to jump | Normally, and for products |

## Managing versions with git

How to put a project on GitHub is in "Putting it on GitHub" in Chapter 3. After that, do your everyday recording with **Source Control** on the left of VS Code (the branching icon).

| Task | In Source Control | Command |
| --- | --- | --- |
| See what changed | Click a file in the list (before and after side by side) | `git diff` |
| Record (commit) | Write "what you changed" in the top box and press **Commit** | `git add . && git commit -m "…"` |
| Upload to GitHub (push) | **Sync Changes** (or … → Push) | `git push` |
| Bring in changes from GitHub | **Sync Changes** (or … → Pull) | `git pull` |
| Go back to an earlier state | Right-click a file → Discard Changes (throw away uncommitted changes) | `git restore filename` |

- **Commit often whenever something works**. When it stops working, you can tell where you broke it
- Write commit descriptions briefly, saying what you did, like "Add I2C reading" or "Add the watchdog"
- Mark versions you ship with `git tag v1.0.0` → `git push --tags` (Chapter 17)
- `build/` is excluded by `.gitignore`, so it is not uploaded
- Detailed use in VS Code (branches, conflicts, handy extensions), use with commands, and common errors are in the [GitHub Textbook](https://yusuke1090.github.io/textbooks/?b=github)

## Recommended extensions

### Installed together with the "Raspberry Pi Pico" extension

These are already there without installing them yourself.

| Extension (author) | Role |
| --- | --- |
| Cortex-Debug (marus25) | Debugging with a Debug Probe. Stop at lines, view variables. Four mcu-debug tools (for viewing memory and registers) are installed with it |
| MicroPico (paulober) | For developing MicroPython in VS Code. Not used in this guide (it only runs when you open a MicroPython project, and connects automatically to a Pico running MicroPython; at that point it competes with Pico Studio for the port, so use only one of them) |
| Python (Microsoft) | For writing Python programs. Also usable for `train.py` in Chapter 14 and the like |

### Recommended when you open a project (install them)

When you open a project made by the extension, "This workspace has extension recommendations" appears in the lower right. Pressing **"Install All"** installs the following.

| Extension (author) | Role |
| --- | --- |
| **C/C++** (Microsoft) | Completion, red underlines for errors as you type, jumping with F12 |
| **C/C++ Extension Pack** (Microsoft) | A bundle of C/C++, CMake Tools and others |
| **Serial Monitor** (Microsoft) | View `printf` output inside VS Code (step ⑥ in Chapter 3) |

You can also install them from the terminal.

```bash
code --install-extension ms-vscode.cpptools-extension-pack
code --install-extension ms-vscode.vscode-serial-monitor
```

### Nice to have

| Extension (author) | Role | How to install |
| --- | --- | --- |
| Error Lens (Alexander) | Shows errors and warnings as text to the right of the line. You notice them without opening the Problems panel | `code --install-extension usernamehw.errorlens` |
| Git Graph (mhutchie) | Shows the commit history as a branching diagram | `code --install-extension mhutchie.git-graph` |
| Rainbow CSV (mechatroner) | Colors CSV files by column. Handy for the logs in Chapters 13–14 and `features.csv` | `code --install-extension mechatroner.rainbow-csv` |
| GitHub Actions (GitHub) | Shows the results of automatic builds on GitHub in VS Code (when you set up automatic builds for a product repository) | `code --install-extension github.vscode-github-actions` |
| Japanese Language Pack (Microsoft) | Puts VS Code's menus in Japanese (if you like) | `code --install-extension ms-ceintl.vscode-language-pack-ja` |

You can see installed extensions under **Extensions** on the left (the icon of four squares). Extensions you do not use can be stopped with "Disable".

## When to use VS Code and when to use Pico Studio

| Task | Tool |
| --- | --- |
| Write, build and flash C++ | **VS Code** |
| Stop at a line and investigate | **VS Code** (Debug Probe) |
| View `printf` output | VS Code's Serial Monitor or Pico Studio |
| Check whether the Pico is connected and what is running | **Pico Studio** (Chapter 5) |
| Check whether the development environment is complete | **Pico Studio** (Chapter 5) |
| Quickly try wiring and sensors before writing C++ | MicroPython in Pico Studio (Appendix E) |

The same Pico cannot be used from both at once. Before flashing from one, press "切断" (Disconnect) or Stop Monitoring in the other.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| The Project items in Quick Access are grayed out | Is the project folder (the one with `CMakeLists.txt` and `.vscode`) open? File → Open Folder |
| The first project takes forever to be created | It is downloading into `~/.pico-sdk`. Watch the progress in the lower right. Internet is needed |
| Run says "device not found" | Is MicroPython running (hold BOOT while plugging in)? Are Pico Studio or Serial Monitor using the port? |
| Run says "no permission" | Install the udev rules from Step 3 of Chapter 2, and unplug and replug the Pico |
| Red wavy underlines will not go away | Compile once. If they still appear, Clean CMake → Compile |
| `printf` output does not appear | Did you check Console over USB when creating the project? Does `CMakeLists.txt` have `pico_enable_stdio_usb(name 1)`? |
| A `No such file` error after adding a feature | Did you add the library (`hardware_i2c` and so on) to `target_link_libraries`? |

Detailed explanations of the extension are on [the extension's page](https://marketplace.visualstudio.com/items?itemName=raspberry-pi.raspberry-pi-pico) and in [Getting started with Raspberry Pi Pico-series (PDF)](https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf).
How to read build errors is in Appendix B.

## Summary

- The most used items are Compile Project and Run Project (USB). When things are strange, Clean CMake
- F12 jumps to the SDK source. Ctrl + Shift + M shows the Problems list
- When using a feature, add its library to `target_link_libraries`. When you add a `.cpp`, add it to `add_executable`
- With a Debug Probe, you can investigate line by line with F5, F10 and F11
- Put projects on GitHub, and commit and push often whenever something works (Source Control)
- For extensions, "Install All" of the recommendations when you open a project (C/C++, Serial Monitor and others). Error Lens is also handy
- Write in VS Code; check the connection in Pico Studio
