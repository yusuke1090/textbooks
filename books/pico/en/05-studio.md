# 6. Checking the connection with Pico Studio

Pico Studio's screen is in Japanese, so this chapter gives each button's Japanese label followed by its meaning in English.

## What is Pico Studio?

A tool that runs on your own PC to check that the Pico is properly connected. **Program development is done in VS Code (Chapter 4); Pico Studio is used for checking.**

| What it can do | When to use it |
| --- | --- |
| See whether the Pico is visible over USB and what is running on it (C++ / MicroPython / flashing mode) | When you cannot flash from VS Code, or when you first connect |
| See whether the C++ development environment (VS Code extension, SDK, compiler, picotool) is complete | Before starting development, or when builds fail |
| See `printf` output | Instead of VS Code's Serial Monitor |
| Flash a `.uf2` (MicroPython, or one built in VS Code) | When Run Project cannot be used |
| Try MicroPython code right away | When you want to check wiring and sensors before writing C++ (Appendix E) |

![How Pico Studio works](images/en/studio-system.svg)

Pico Studio is made of a small server running on your PC (`server.py`) and a browser that shows its screen. It does not connect to the internet and runs only inside your PC (it uses the internet only when downloading MicroPython).

Before using it, finish Step 3 of Chapter 3 (pyserial and the udev rules).

## Starting it

In the terminal (the black window opened with Ctrl + Alt + T), type these two lines.

```bash
cd ~/apps/pico-studio
./start.sh
```

After a moment a browser opens and shows the Pico Studio screen.
If it does not open, open **http://localhost:8765** in a browser.

- If it is already running, typing `./start.sh` just opens it in the browser (it will not start twice)
- Pico Studio keeps running even if you close the browser tab. Open http://localhost:8765 again to go back
- **When you update Pico Studio** (for example after `git pull`), restart it. Press Ctrl + C in the terminal where it is running to stop it, then type `./start.sh`. If the old version is still running, the screen shows "サーバーが古いままです" (the server is out of date)

### When you finish

1. Press "切断" (Disconnect) on the screen
2. Press **Ctrl + C** in the terminal where you typed `./start.sh`

Closing the terminal also ends it.

## Reading the screen

![The Pico Studio screen](images/studio-screen.svg)

| No. | Area | What you can do |
| --- | --- | --- |
| ① | Port box | Choose where the Pico is connected (the port). For a Pico, what is running is shown too, like "(ピコ・C++ のプログラム)" (Pico, C++ program) |
| ② | 更新・接続・切断 (Refresh, Connect, Disconnect) | Search for ports again, connect, disconnect |
| ③ | 📚 ガイド (Guide) | Opens this guide (the textbook site) |
| ④ | 接続の確認 (Connection check) | Shows the connection and the development environment in four items (explained below) |
| ⑤ | ピコのファイル (Files on the Pico) | MicroPython only. A list of files saved on the Pico |
| ⑥ | コード (Code) | Write MicroPython code and try it with "▶ 実行" (Run) (Appendix E) |
| ⑦ | 出力 (Output) | Output from the Pico (`printf` or `print`) appears here |
| ⑧ | 送信欄 (Send box) | Send one line to the Pico (it can be received with `getchar()` or `input()`) |

Drag the divider between the code box and the output box up or down to change their relative heights.

## Connecting and checking

### Steps

1. Connect the Pico to the PC with a USB cable
2. Press **"更新" (Refresh)** (while disconnected, it also searches automatically every 3 seconds)
3. In the port box, choose the one marked **"(ピコ…)" (Pico…)**
4. Press **"接続" (Connect)**

### The four items of the connection check

| Item | When green | When not green |
| --- | --- | --- |
| USB で認識 (Detected over USB) | The PC has found the Pico. What is running is shown too | Check the cable and USB port ("Not found" below) |
| シリアル接続 (Serial connection) | Ready to communicate with the Pico | Press "接続" (Connect). For a permission error, see below |
| 動いているプログラム (Running program) | For a C++ program, "C++ のプログラムが動いています" (a C++ program is running). For MicroPython, its version and free space | Is another program (such as VS Code's Serial Monitor) using the port? |
| C++ の開発環境 (C++ development environment) | The VS Code extension, Pico SDK, compiler and picotool each show ✓ or ✗ | Install the ✗ items as in Chapter 3. The SDK and compiler are installed when you create your first project in VS Code |

The colors of the dots mean the following.

| Color | Meaning |
| --- | --- |
| Green | OK |
| Yellow | Caution (flashing mode, only partly complete, running and so on) |
| Red | There is a problem (not found, no response and so on) |
| Gray | Not checked yet (not connected and so on) |

### The "Detected over USB" display tells you what is running

| Display | What is running on the Pico | When flashing with VS Code's Run Project (USB) |
| --- | --- | --- |
| （C++ のプログラム） (C++ program) | A C++ program with Console over USB | It can be flashed as is |
| （MicroPython） | MicroPython | Hold BOOT while reconnecting, then flash |
| BOOTSEL モード（書き込み待ち） (BOOTSEL mode, waiting to be flashed) | Flashing mode | It can be flashed as is |
| 見つかりません (Not found) | A program that does not use USB, the Pico has stopped, or a cable problem | Hold BOOT while reconnecting |

## Viewing a C++ program's output

The `printf` output of a C++ program flashed from VS Code can also be seen in Pico Studio's output box.

1. Flash with Run Project (USB) in VS Code
2. In Pico Studio, "更新" (Refresh) → choose the port (`(ピコ・C++ のプログラム)`) and "接続" (Connect)
3. `printf` output scrolls by in the output box

- Text typed in the send box can be received by the Pico with `getchar()` and the like
- With a C++ program, "▶ 実行" (Run) and file operations cannot be used (they are for MicroPython)
- **Press "切断" (Disconnect) before flashing again from VS Code.** If it stays connected, it may not reconnect after flashing

## Flashing a .uf2

When the Pico is in flashing mode, buttons appear below the connection check.

1. Hold the Pico's **BOOT** button while connecting USB, and let go once it is connected
2. "USB で認識" shows **BOOTSEL モード（書き込み待ち）** (BOOTSEL mode, waiting to be flashed)

![In flashing mode](images/studio-bootsel.png)

| Button | What it does |
| --- | --- |
| 最新の MicroPython を書き込む (Flash the latest MicroPython) | Downloads MicroPython and flashes it (Appendix E) |
| .uf2 ファイルを選ぶ (Choose a .uf2 file) | Flashes a `.uf2` on your PC. You can also choose `~/apps/project/build/name.uf2` built in VS Code |

> If you see "ドライブがまだ開かれていません" (the drive has not been opened yet), open "RPI-RP2" in the file manager, then press "更新" (Refresh).

## When it will not connect

### When it says "Not found"

![When the Pico cannot be found](images/studio-notfound.png)

The PC cannot find the Pico. Try the following in order.

1. Change to a USB cable that supports data
2. Plug into a different USB port on the PC. If you are using a USB hub, plug directly into the PC
3. Connect while holding the Pico's **BOOT** button. If it shows "BOOTSEL mode", the cable is fine and MicroPython simply is not installed (go to "Flashing a .uf2" above)

How to check with commands is in Appendix B.

### When it says "no permission to open the port"

![A permission error](images/studio-perm.png)

On Linux, a one-time setting is needed to make the Pico's port usable.
Type the following in the terminal (you will be asked for your password; nothing appears on screen as you type, but keep typing and press Enter).

```bash
cd ~/apps/pico-studio
sudo cp 70-pico-studio.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
```

When done, **unplug the Pico once and plug it back in**. Then press "更新" (Refresh) → "接続" (Connect).

> If you installed `99-pico-studio.rules` before, its number is too high and it does not take effect.
> First delete it with `sudo rm /etc/udev/rules.d/99-pico-studio.rules`, then install as above.

You can tell whether the setting worked by typing this command in the terminal.

```bash
ls -l /dev/ttyACM0
```

If the line starts **with a `+`**, like `crw-rw----+`, it worked.

## Summary

- Pico Studio is a tool for checking. Development is done in VS Code
- The connection check shows four things: USB, serial, the running program and the C++ development environment
- The `printf` output of C++ programs can also be seen in the output box. Press "切断" (Disconnect) before flashing from VS Code
- In flashing mode, you can flash MicroPython or a `.uf2`
- If it will not connect, try in this order: cable → USB port → connect while holding BOOT

## Exercises

```quiz
Q: Is Pico Studio a tool for developing or for checking?
A: checking | check | for checking
E: Develop in VS Code.

Q: Which button do you press in Pico Studio before writing from VS Code?
A: Disconnect | 切断
E: Only one program can use the port at a time.

Q: What file extension can you drag onto a Pico in programming mode?
A: .uf2 | uf2
E: MicroPython firmware is also a `.uf2` file.

Q: When it will not connect, what do you suspect first?
A: cable | USB cable | the cable
E: Try cable → USB port → hold BOOT and plug in.
```
