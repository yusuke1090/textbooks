# 2. Setting up the development environment

These steps are for Ubuntu. You only do them once.

## What you need

| Item | Role | How to install |
| --- | --- | --- |
| **VS Code** | Software for writing programs | Step 1 in this chapter |
| **The "Raspberry Pi Pico" extension** | Lets you build, flash and debug with buttons. It also installs the compiler and Pico SDK automatically | Step 2 in this chapter |
| **The "Serial Monitor" extension** | Shows `printf` output inside VS Code | Step 2 in this chapter |
| udev rules | Use the Pico without sudo (flashing, viewing output) | Step 3 in this chapter |
| Pico Studio | Check whether the Pico is connected (Chapter 5) | Step 3 in this chapter |
| (If needed) tools for the command line | Build and flash in the terminal without VS Code | Appendix A |

To make Pico programs, you also need an **ARM compiler** (software that makes machine code for the Pico) and the **Pico SDK** (the official Raspberry Pi collection of C/C++ parts). The extension installs both automatically, so you do not need to install them yourself.

## Step 1: Install VS Code

Skip this if it is already installed.

1. Download the **.deb** (for Ubuntu) from the [VS Code download page](https://code.visualstudio.com/)
2. In the terminal, install the downloaded file

```bash
sudo apt install ~/Downloads/code_*.deb
```

## Step 2: Install the "Raspberry Pi Pico" extension

1. Open **Extensions** on the left of VS Code (the icon of four squares)
2. Type `Raspberry Pi Pico` in the search box
3. Choose the one whose author is **Raspberry Pi** and press "Install"
4. A **Pico-shaped icon** appears on the left. Click it to open the "Quick Access" menu

![The extension's menu (Quick Access)](images/vscode-quick-access.png)

The extension uses git, tar, python3 and others. They are usually on Ubuntu already, but if you are told they are missing, type the following.

```bash
sudo apt install git tar python3 build-essential
```

### Install Serial Monitor too

To see `printf` output inside VS Code, also install the **Serial Monitor** extension (author: Microsoft) (used in Chapter 3).
Type `Serial Monitor` in the Extensions search box and install the one by Microsoft. From the terminal, this command also installs it.

```bash
code --install-extension ms-vscode.vscode-serial-monitor
```

Other recommended extensions are in "Recommended extensions" in Chapter 4.

## What the extension installs

**The first time you create a project** (Chapter 3), the extension downloads the following into **`~/.pico-sdk`**. It takes a few minutes and needs the internet.

| What | Where | Role |
| --- | --- | --- |
| Pico SDK | `~/.pico-sdk/sdk/2.x.x` | A collection of functions that operate the Pico's parts (GPIO, I2C and more) |
| ARM compiler | `~/.pico-sdk/toolchain/…` | Turns C++ into the Pico's machine code |
| CMake, Ninja | `~/.pico-sdk/cmake`, `~/.pico-sdk/ninja` | Create and run the build steps |
| picotool | `~/.pico-sdk/picotool/…` | Puts the Pico into flashing mode over USB and flashes it |
| OpenOCD | `~/.pico-sdk/openocd/…` | Debugging with a Debug Probe (Chapter 4) |

- Each version gets its own folder, so different projects can use different versions without conflict
- You can see, add or remove installed versions with **Manage Components** in Quick Access
- Nothing is installed system-wide (in `/usr/bin` and so on), so other software is not affected

## Step 3: Make the Pico usable without sudo

Make it possible to flash the Pico from VS Code, and to talk to the Pico from Pico Studio (Chapter 5), without sudo.

```bash
sudo apt install python3-serial
cd ~/apps/pico-studio
sudo cp 70-pico-studio.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
```

| Command | What it does |
| --- | --- |
| `sudo apt install python3-serial` | Installs pyserial, which Pico Studio uses to talk to the Pico |
| `sudo cp 70-pico-studio.rules …` | Installs the setting (a udev rule) that lets you use the Pico without sudo. It covers both the serial port (viewing output) and flashing over USB (VS Code's Run Project (USB)) |
| `sudo udevadm control --reload-rules` | Reloads the settings |

After installing, **unplug the Pico once and plug it back in**. How to start Pico Studio is in Chapter 5.

> Even if you installed `70-pico-studio.rules` before, copy it again. Settings for flashing over USB have been added.

## Checking that everything is in place

When you start Pico Studio (Chapter 5), the fourth item of its connection check is **the C++ development environment**.

| Display | Meaning |
| --- | --- |
| ✓ VS Code の拡張機能 (VS Code extension) | The "Raspberry Pi Pico" extension is installed |
| ✓ Pico SDK | The SDK is there. It becomes ✓ once you create your first project in VS Code |
| ✓ コンパイラ (compiler) | The ARM compiler is there. Likewise, it becomes ✓ with your first project |
| ✓ picotool | The tool for operating the Pico over USB is there |

A green dot means you are ready. You can also check in the terminal.

```bash
python3 ~/apps/pico-studio/devenv.py check
```

> Just installing the extension still leaves the SDK and compiler as ✗. They are installed automatically and become ✓ when you create your first project in Chapter 3.

## Summary

- You need VS Code and the "Raspberry Pi Pico" and "Serial Monitor" extensions. The extension installs the compiler and SDK into `~/.pico-sdk`
- Install the udev rules so you can use the Pico without sudo (reinstall them even if you installed them before)
- The first time you create a project, it takes a few minutes to download
- Pico Studio needs pyserial and the udev rules
- Check that everything is in place with Pico Studio's "C++ development environment" or `devenv.py check`

## Exercises

```quiz
Q: What is the name of the VS Code extension for Pico development?
A: Raspberry Pi Pico
E: Also install Serial Monitor.

Q: In which folder does the extension install the compiler and SDK?
A: ~/.pico-sdk | .pico-sdk
E: The first new project downloads them, which takes a few minutes.

Q: What kind of rules let you use the Pico without sudo?
A: udev | udev rules
E: Reinstall them even if you installed them before.

Q: Which Python serial library does Pico Studio need?
A: pyserial
E: Prepare it together with the udev rules.
```
