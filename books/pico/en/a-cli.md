# Appendix A. Working with commands

Everyday development is done in VS Code (Chapter 4). Use this appendix in situations like these.

- You want to put the steps into a script (such as flashing for mass production; Chapter 19)
- You want to know what is happening inside VS Code
- You want to try many small programs together in one folder

Click a word in a command (`cmake`, `make` and others) to see its meaning in a speech bubble.

## Installing the command-line tools

The tools the VS Code extension installs (`~/.pico-sdk`) are meant to be used from inside VS Code. If you want to build directly in the terminal, install the command-line tools all at once with the following script. It asks for your password partway through.

```bash
sh ~/apps/pico-studio/cpp/setup-sdk.sh
```

When `OK: C++ を開発できます` (OK: ready for C++ development) appears at the end, you are done. Open a new terminal before using it. Running it again is fine (it uses what is already there and adds only what is missing).

### What this script does

The script does the following five things, from top to bottom. You can read it at `~/apps/pico-studio/cpp/setup-sdk.sh`.

| Step | What it does | Where things go | Contents |
| --- | --- | --- | --- |
| 1/5 | Install the compiler and so on (`sudo apt install`) | `/usr/bin` and so on (system-wide) | The packages in the table under "1. Install the compiler and so on" below |
| 2/5 | Download Pico SDK 2.1.1 (`git clone` and `git submodule update --init`) | `~/pico/pico-sdk` | The SDK itself and the libraries it uses (table below) |
| 3/5 | Register the SDK's location | One line at the end of `~/.bashrc` | `export PICO_SDK_PATH=/home/username/pico/pico-sdk` |
| 4/5 | Prepare the project folder and check that everything is in place | `~/apps/pico-cpp` | `CMakeLists.txt`, `pico_sdk_import.cmake`, `.gitignore`, `blink.cpp`, `mpu6050.h`, `ws2812.h` |
| 5/5 | Build and install picotool (`git clone` and build). Also installs a udev rule so it works without sudo | `~/pico/picotool` (source), `~/.local/bin/picotool`, `/etc/udev/rules.d/60-picotool.rules` | A tool to put the Pico into flashing mode over USB, flash it and inspect it (this appendix, Chapter 19). Building works even without it |

The libraries downloaded with the SDK (submodules) are as follows.

| Library | Use |
| --- | --- |
| TinyUSB | The USB system. Used to send `printf` to the PC over USB (**required**) |
| cyw43-driver | Drives the Pico W's wireless chip |
| lwIP | WiFi communication (TCP/IP) on the Pico W |
| BTstack | Bluetooth on the Pico W |
| mbedtls | Cryptography (HTTPS and so on) |

- Downloading and installing use **around 1 GB** of disk in total (a rough figure). An internet connection is needed
- The line written to `~/.bashrc` takes effect in **newly opened terminals**. In a terminal that is already open, type `source ~/.bashrc` or open a new one
- Step 3/5 does nothing if `PICO_SDK_PATH` is already in `~/.bashrc`. To put the SDK somewhere else, type something like `PICO_SDK_PATH=/where/you/want sh ~/apps/pico-studio/cpp/setup-sdk.sh`
- Step 4/5 does not overwrite existing files
- Step 5/5 does nothing if a picotool with USB support is already there

### Things created later

After the script, the following are created automatically the first time you build.

| Item | Where | Contents |
| --- | --- | --- |
| What you built with commands | `~/apps/pico-cpp/build` | `.uf2` files and so on. You can delete it and start again from `cmake` |
| picotool (for making `.uf2` files) | Inside each `build/_deps` | The SDK downloads and builds it automatically when building (internet needed). It has no USB features, so use the picotool installed in step 5/5 to operate the Pico |

### Undoing it

To remove the C++ development environment, do the following.

```bash
rm -rf ~/pico/pico-sdk ~/pico/picotool ~/.local/bin/picotool ~/.cache/pico-studio
sudo rm /etc/udev/rules.d/60-picotool.rules
sudo apt remove gcc-arm-none-eabi libnewlib-arm-none-eabi libstdc++-arm-none-eabi-newlib
```

Open `~/.bashrc` in a text editor and delete the `export PICO_SDK_PATH=...` line (`nano ~/.bashrc`).
`~/apps/pico-cpp` contains programs you wrote, so check what is in it before deleting it.

### Installing one by one

These are the steps for installing things yourself, one at a time, without the script. They do the same as steps 1/5–3/5 of the script (for building picotool, see [picotool's README](https://github.com/raspberrypi/picotool)).

#### 1. Install the compiler and so on

```bash
sudo apt install cmake gcc-arm-none-eabi libnewlib-arm-none-eabi libstdc++-arm-none-eabi-newlib build-essential git python3 libusb-1.0-0-dev pkg-config
```

| Package | Role |
| --- | --- |
| `cmake` | Software that creates the build steps |
| `gcc-arm-none-eabi` | The compiler for the Pico (ARM). The PC's `g++` cannot make Pico programs |
| `libnewlib-arm-none-eabi`, `libstdc++-arm-none-eabi-newlib` | The C / C++ standard libraries for the Pico |
| `build-essential` | Basic build tools such as `make` |
| `git` | Used to download the SDK |
| `python3` | Used during the SDK build |
| `libusb-1.0-0-dev`, `pkg-config` | Used to build picotool (the tool that operates the Pico) automatically during the build |

#### 2. Download the Pico SDK

```bash
mkdir -p ~/pico
cd ~/pico
git clone --branch 2.1.1 https://github.com/raspberrypi/pico-sdk.git
cd pico-sdk
git submodule update --init
```

- `--branch 2.1.1` specifies the version. You can check for newer versions on the [releases page](https://github.com/raspberrypi/pico-sdk/releases)
- `git submodule update --init` downloads the USB library (TinyUSB) and others that the SDK uses. **If you forget this, `printf` will not come out over USB**

#### 3. Register the SDK's location

Write it in `~/.bashrc` so the build can find the SDK.

```bash
echo 'export PICO_SDK_PATH=~/pico/pico-sdk' >> ~/.bashrc
source ~/.bashrc
```

> If you use VS Code, the **Raspberry Pi Pico** extension lets you set up, build, flash and debug with buttons (Chapter 4).
> This appendix uses commands so you can see what is happening.

## The project folder

### Creating the folder

```bash
python3 ~/apps/pico-studio/devenv.py init
```

The files needed for building are created in `~/apps/pico-cpp` (if you used the all-in-one script, they are already there).
It does not overwrite existing files, so running it again is fine. To create it in a different folder, give the folder, as in `init ~/apps/collar`.

```text
~/apps/pico-cpp/
├── CMakeLists.txt          build settings (explained below)
├── pico_sdk_import.cmake   loads the SDK (copied from the SDK)
├── .gitignore              settings so git does not track the build folder
├── blink.cpp               blinking LED (the first program)
├── mpu6050.h               a class for reading the MPU-6050 (Chapter 11)
├── ws2812.h                a class for lighting the RGB LED (Chapter 8)
└── build/                  files made by building (.uf2 and so on). Created when you run cmake
```

If you used `setup-sdk.sh`, it is already there.

### CMakeLists.txt

The build settings. **Each `.cpp` in this folder becomes one program** (`blink.cpp` → `build/blink.uf2`).
Any of the C++ code from Chapters 8–17 can be built as is by saving it as a `.cpp`. The heart of it is as follows.

```cmake
cmake_minimum_required(VERSION 3.13)
include(pico_sdk_import.cmake)        # read before pico_sdk_init
project(pico_cpp C CXX ASM)
set(CMAKE_CXX_STANDARD 17)
pico_sdk_init()

set(PICO_LIBS pico_stdlib hardware_adc hardware_i2c ...)   # libraries used (those in the table in Chapter 5)

file(GLOB APP_SOURCES CONFIGURE_DEPENDS "${CMAKE_CURRENT_LIST_DIR}/*.cpp")
foreach(src IN LISTS APP_SOURCES)
    get_filename_component(name "${src}" NAME_WE)   # blink.cpp -> blink
    add_executable(${name} "${src}")
    target_link_libraries(${name} ${PICO_LIBS})
    pico_enable_stdio_usb(${name} 1)                # send printf over USB
    pico_add_extra_outputs(${name})                 # also make a .uf2
endforeach()
```

| Line | Meaning |
| --- | --- |
| `project(pico_cpp C CXX ASM)` | The project name and the languages used (C, C++, assembly) |
| `pico_sdk_init()` | Prepares the SDK |
| `set(PICO_LIBS ...)` | The libraries used. `pico_stdlib` is the basics such as GPIO, time and `printf`; `hardware_i2c` is I2C, and so on |
| `file(GLOB ... *.cpp)` | Finds all the `.cpp` files in the folder |
| `add_executable(blink blink.cpp)` | Makes a program called `blink` from `blink.cpp` |
| `pico_enable_stdio_usb(... 1)` | Sends `printf` output to USB serial. **Without this, you cannot see the output** |
| `pico_add_extra_outputs` | Also makes the `.uf2` file for flashing |

- `.cpp` files starting with `test_` are tests for the PC (Chapter 19), so they are not built for the Pico
- To split one program into several `.cpp` files (Chapter 13), add a line yourself, such as `add_executable(collar collar.cpp sensor.cpp)`

## The overall flow

| Step | What to do | Command | In VS Code |
| --- | --- | --- | --- |
| 0 | Prepare the tools and project (first time only) | `sh ~/apps/pico-studio/cpp/setup-sdk.sh` | The extension installs them automatically |
| 1 | Check that it is detected over USB | `lsusb -d 2e8a:` | (Pico Studio's "USB で認識") |
| 2 | Prepare the build (first time, and when you change CMakeLists.txt) | `cmake -S . -B build` | (automatic) |
| 3 | Build | `make -C build -j4 blink` | Compile Project |
| 4 | Enter flashing mode | For MicroPython `mpremote bootloader`, for C++ `picotool reboot -f -u` | (automatic) |
| 5 | Flash | `cp build/blink.uf2 /run/media/$USER/RPI-RP2/` | Run Project (USB) |
| 6 | View the output | `python3 -m serial.tools.miniterm /dev/ttyACM0 115200` | Serial Monitor |
| 7 | Inspect the program on the Pico (when needed) | `picotool info -a` | (none) |

> **A port can only be used by one program at a time.** Before using the commands, press "切断" (Disconnect) in Pico Studio or Stop Monitoring in VS Code's Serial Monitor.

## Step 1: Check that it is detected over USB

```bash
lsusb -d 2e8a:
```

| Result | State |
| --- | --- |
| `2e8a:000a Raspberry Pi Pico` | A C++ (Pico SDK) program with USB output is running |
| `2e8a:0005 MicroPython Board in FS mode` | Running MicroPython |
| `2e8a:0003 Raspberry Pi RP2 Boot` (`2e8a:000f` on the Pico 2) | Flashing mode (BOOTSEL) |
| Nothing | Not detected. Or a program that does not use USB is running |

## Steps 2–3: Build

Do this in the project folder (`~/apps/pico-cpp`). Each `.cpp` in this folder becomes one program (`blink.cpp` → `build/blink.uf2`).
If `cd` says "No such file or directory", the folder does not exist yet. Create it with `python3 ~/apps/pico-studio/devenv.py init`.

```bash
cd ~/apps/pico-cpp
cmake -S . -B build
make -C build -j4 blink
```

- `cmake -S . -B build` reads the `CMakeLists.txt` in the current folder and creates the build steps in the `build` folder. Run it the first time, and whenever you add or remove `.cpp` files
- `make -C build -j4 blink` builds `blink` in the `build` folder. `build/blink.uf2` is created
- Errors appear like `blink.cpp:12:5: error: ...`, meaning line 12, character 5

## Step 4: Enter flashing mode

**The method depends on what is currently running on the Pico.** Check with `lsusb -d 2e8a:` from step 1.

| What `lsusb` shows | What is running | Command to enter flashing mode |
| --- | --- | --- |
| `2e8a:0005 MicroPython Board` | MicroPython | `mpremote bootloader` |
| `2e8a:000a Raspberry Pi Pico` | A C++ program (with `stdio_init_all()`) | `picotool reboot -f -u`, or the 1200 bps method below |
| `2e8a:0003` (`000f` on the Pico 2) | Already in flashing mode | Nothing to do |
| Nothing | A program that does not use USB, or it has stopped | Hold BOOT while reconnecting USB |

**The first time you flash C++**, MicroPython is still running, so use `mpremote bootloader`.

```bash
mpremote bootloader
```

When a C++ program is running, use picotool.

```bash
picotool reboot -f -u
```

Without picotool, open and close the port at 1200 bps. Pico SDK programs take this as the signal "go into flashing mode".

```bash
python3 -c "import serial; serial.Serial('/dev/ttyACM0', 1200).close()"
```

If the `RPI-RP2` drive appears, it worked. If not, hold BOOT while reconnecting USB.

> If `picotool` is "not found", run `sh ~/apps/pico-studio/cpp/setup-sdk.sh` again to install it (the start of this appendix). The `~/.pico-sdk/picotool/…/picotool` installed by the VS Code extension also works. The picotool made in `build/_deps` during a build is built without USB features, so it cannot be used to operate the Pico.

## Step 5: Flash

```bash
cp build/blink.uf2 /run/media/$USER/RPI-RP2/
```

When the copy finishes, the Pico restarts automatically and the program starts running.

> Where the drive appears differs between PCs. If it is not under `/run/media/$USER/`, look in `/media/$USER/`.
> On the Pico 2, the drive name is `RP2350`.

With picotool, switching to flashing mode and flashing can be done in one line.

```bash
picotool load -x -f build/blink.uf2
```

## Step 6: View the output

```bash
python3 -m serial.tools.miniterm /dev/ttyACM0 115200
```

- To stop, press **Ctrl + ]**
- Flashing again makes the port disappear once, so stop miniterm and reconnect
- Characters you send can be received by the Pico with `getchar()` and the like

## Step 7: Inspect the program on the Pico

With picotool, you can see the name of the flashed program, its build date and time, the pins it uses and more (in flashing mode).

```bash
picotool info -a
```

How to put a name and version into a program is in Chapter 19.

## Putting the steps into a script

It is convenient to put everything from building to viewing output into one script. Save the following as `~/apps/pico-cpp/run.sh`.

```bash
#!/bin/sh
# usage: sh run.sh blink
set -e
cd "$(dirname "$0")"
make -C build -j4 "$1"
python3 -c "import serial; serial.Serial('/dev/ttyACM0', 1200).close()" 2>/dev/null || true
echo "waiting for flashing mode..."
while [ ! -d /run/media/$USER/RPI-RP2 ]; do sleep 0.5; done
cp "build/$1.uf2" /run/media/$USER/RPI-RP2/
echo "flashed. Showing the output (Ctrl+] to quit)"
sleep 3
python3 -m serial.tools.miniterm /dev/ttyACM0 115200
```

```bash
sh run.sh blink
```

## Building a VS Code project with commands

Projects made in VS Code (Chapter 4) can be built with the same commands, because the `DO NOT EDIT` part of `CMakeLists.txt` selects the SDK and compiler in `~/.pico-sdk`.

```bash
cd ~/apps/blink
cmake -S . -B build
make -C build -j4
```

If it does not work, use Compile Project in VS Code.

## Troubleshooting (commands)



## Summary

- Install the command-line tools all at once with `setup-sdk.sh`. What it does is in the tables in this appendix
- In `~/apps/pico-cpp`, each `.cpp` in the folder becomes one program. When you add a `.cpp`, run `cmake -S . -B build` again
- Build with `make -C build -j4 name`; flash by copying the `.uf2` to `RPI-RP2` or with `picotool load -x -f`
- To enter flashing mode, use `mpremote bootloader` for MicroPython and `picotool reboot -f -u` for C++
- View output with miniterm. Stop with Ctrl + ]
