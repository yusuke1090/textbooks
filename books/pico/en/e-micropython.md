# Appendix E. Quick tests with MicroPython

## When MicroPython is worth using

**MicroPython** is a small version of Python for microcontrollers. Code runs as soon as you send it, so you can try things without waiting for a build and flash.

| Situation | What to use |
| --- | --- |
| You want to check right away whether the wiring is right and the sensor replies | **MicroPython** (this appendix) |
| You want to read register values one at a time (line by line in the REPL) | **MicroPython** |
| A product's program, where speed, power saving and long running matter | **C++** (from Chapter 4) |

Product programs are written in C++. MicroPython is handy for **early experiments before writing C++**.

> Flashing MicroPython erases the C++ program on the Pico (it comes back if you flash it again from VS Code later).

## When MicroPython is not installed yet

A brand-new Pico may not have MicroPython on it.

1. Hold the Pico's **BOOT** button while connecting it to the PC with a USB cable (details in the figure in Chapter 1)
2. Let go of the button once it is connected
3. The connection check shows **BOOTSEL モード（書き込み待ち）** (BOOTSEL mode, waiting to be flashed)

![In flashing mode](images/studio-bootsel.png)

4. Press **"最新の MicroPython を書き込む"** (Flash the latest MicroPython). It downloads the latest version from the internet and flashes it automatically
5. After a few seconds the Pico restarts, so press "更新" (Refresh) → "接続" (Connect)

To use a .uf2 file you already have (a file of software to flash to the Pico), press ".uf2 ファイルを選ぶ" (Choose a .uf2 file).

> If you see "ドライブがまだ開かれていません" (the drive has not been opened yet), open "RPI-RP2" in the file manager, then press "更新" (Refresh).

## Writing and running code

### How to run

1. Write code in the "コード" (Code) box in the middle
2. Press **"▶ 実行" (Run)** (or **Ctrl + Enter**)
3. The result appears in the "出力" (Output) box below

![Running code](images/studio-run.png)

Blue text in the output box is a notice from Pico Studio.

| Display | Meaning |
| --- | --- |
| `[実行開始]` (run started) | The Pico received the code and started running it |
| `[実行終了]` (run finished) | It ran to the end (or was stopped) |
| `>>>` | The Pico is waiting for the next command |

### Handy features of the code box

| Action | What it does |
| --- | --- |
| Tab | Inserts an indent (4 spaces). Select several lines and press it to indent them all |
| Shift + Tab | Removes one level of indent |
| Enter | A new line with the same indent as the previous one. After a line ending in `:` (`{` in C++), it indents one level deeper |
| Ctrl + Enter | Run |
| Ctrl + S | Save to the Pico |

The code you write is kept in the browser automatically, so it is still there the next time you open the screen.

### Using samples

From "サンプルを選ぶ" (Choose a sample), you can load code to try right away.

| Sample | Contents |
| --- | --- |
| hello: 文字と計算 (text and arithmetic) | Shows text and does simple arithmetic |
| LED を点滅させる (blink the LED) | Blinks the board's LED |
| RGB LED を光らせる (light the RGB LED) | Lights red, green and blue on a board with an RGB LED |
| 内蔵の温度センサー (built-in temperature sensor) | Reads the temperature of the Pico's chip |
| PC と送受信する (send and receive with the PC) | Doubles a number typed in the send box and sends it back |

> The current code is replaced by the sample without asking. If you made a mistake, press **Ctrl + Z** in the code box to get the previous code back.

### Stopping a run

A program that repeats forever does not end by itself. To stop it, press **"■ 停止" (Stop)**.

![The screen while running](images/studio-running.png)

- While running, the top bar shows **"実行中" (running)** (①), and "▶ 実行" (Run) cannot be pressed
- Pressing "■ 停止" (Stop) (②) sends Ctrl-C to the Pico to stop it
- After stopping, `KeyboardInterrupt` may appear in the output box, but it is not an error

### When an error appears

If there is a mistake in the code, an error appears in **red text** in the output box.

![How errors are shown](images/studio-error.png)

**The last line** of an error is the most important. `ZeroDivisionError: division by zero` in the example above means "you divided by 0".
Common errors and how to fix them are collected in "Common errors" at the end of this appendix.

## The output box and the REPL

Type one line of Python in the send box below the output box and press **"送信" (Send)** (or Enter), and the Pico runs it on the spot and returns the result. This is called the **REPL** (interactive mode).

![Trying things one line at a time in the REPL](images/studio-repl.png)

| No. | Place | Role |
| --- | --- | --- |
| ① | Send box | Type a one-line command. Also used for input to a program's `input()` |
| ② | 送信 (Send) | Sends it to the Pico (Enter does the same) |

- Variables and `import`s you typed before are remembered, so you can keep using them
- It is handy to use the REPL for quick checks and the code box for whole programs
- **"クリア" (Clear)** in the upper right of the output box clears the display
- **"リセット" (Reset)** restarts the Pico (a soft reset). If there is a main.py, it starts running

## Saving to the Pico

You can save the code in the code box as a file on the Pico.

![Saving to the Pico](images/studio-save.png)

1. Type a name in the file name box (①). Make it end in `.py` (for example `blink.py`)
2. Press **"ピコに保存" (Save to Pico)** (②) (or **Ctrl + S**)
3. It appears in the "ピコのファイル" (Files on the Pico) list

### Running automatically at power-on (main.py)

If you save it with the name **main.py**, it runs automatically when the Pico is powered on.
It then runs just by plugging it into a USB charger or power bank, without a PC.

- Even while main.py is running, "接続" (Connect) in Pico Studio stops it automatically
- To run it again, press "リセット" (Reset) in the output box
- If you no longer want it to run automatically, "削除" (Delete) main.py in the file list

### A recommended flow

Programs are easier to make in this order.

1. Write the code in the code box
2. Try it with **"▶ 実行" (Run)** (it is not saved on the Pico)
3. Fix it and try again
4. When it is finished, name it **main.py** and press **"ピコに保存" (Save to Pico)**
5. Press "リセット" (Reset) in the output box and check that it runs automatically

How to do the same with commands is in "Working with commands" in this appendix.

## Checking the files saved on the Pico

### Viewing them in "Files on the Pico" (recommended)

When connected, **"ピコのファイル" (Files on the Pico)** on the left lists the files saved on the Pico.

![Files on the Pico](images/studio-files.png)

| No. | Place | Role |
| --- | --- | --- |
| ① | 更新 (Refresh) | Reloads the list. Press it after saving, or after a program creates a file |
| ② | File name | Click to open its contents in the code box |
| ③ | 削除 (Delete) | Deletes the file from the Pico (it cannot be undone, so be careful) |

- The number next to a name is the file's size (B is bytes)
- Items marked 📁 are folders. This list cannot open folders, so check inside them with the REPL method below
- Free storage is shown under "MicroPython の応答" (MicroPython response) in the connection check

Click a file name, and its contents open in the code box and its name is put in the file name box.

![log.csv opened](images/studio-opencsv.png)

If you edit an opened file and press "ピコに保存" (Save to Pico), it is overwritten under the same name.
To bring a file's contents to the PC, open it in the code box, copy it with Ctrl + A → Ctrl + C, and paste it into a text editor on the PC.

### Looking with the REPL

Type the following in the send box to look up the list of files and their sizes.

```text
>>> import os; os.listdir()
['model.py', 'log.csv', 'main.py']
>>> os.stat("log.csv")[6]
960
```

| What to type | What it tells you |
| --- | --- |
| `import os; os.listdir()` | The list of files |
| `os.listdir("folder_name")` | The contents of a folder |
| `os.stat("log.csv")[6]` | The size of a file (bytes) |
| `print(open("log.csv").read())` | Shows the contents of a file |

## Commonly used code

"Copy" it, paste it into Pico Studio's code box and try it with "▶ 実行" (Run). Detailed explanations are in the chapters that write the same thing in C++.

### Blinking an LED (Chapter 7)

```python run
from machine import Pin
import time

led = Pin(25, Pin.OUT)   # make GP25 an output

for i in range(10):
    led.on()
    time.sleep(0.3)
    led.off()
    time.sleep(0.3)

print("done")
```

### Reading a button (Chapter 7)

```python run
from machine import Pin
import time

button = Pin(24, Pin.IN, Pin.PULL_UP)   # 1 when not pressed, 0 when pressed

for i in range(50):
    print("pressed" if button.value() == 0 else "-")
    time.sleep(0.2)
```

### Analog input (Chapter 8)

```python run
from machine import ADC
import time

adc = ADC(26)            # GP26
for i in range(20):
    raw = adc.read_u16()  # 0-65535
    volt = raw * 3.3 / 65535
    print("value:", raw, " voltage: {:.2f} V".format(volt))
    time.sleep(0.5)
```

### I2C scan (Chapter 9)

```python run
from machine import Pin, I2C

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
found = i2c.scan()

if not found:
    print("No sensors found. Check the wiring")
for addr in found:
    name = {0x68: "MPU-6050", 0x69: "MPU-6050 (AD0=1)",
            0x76: "BMP280 / BME280", 0x77: "BMP280 / BME280",
            0x44: "SHT31", 0x45: "SHT31"}.get(addr, "?")
    print("found: 0x{:02X}  {}".format(addr, name))
```

### Reading the MPU-6050 (Chapter 10)

```python run
from machine import Pin, I2C
import struct, time

ADDR = 0x68
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)

print("WHO_AM_I:", hex(i2c.readfrom_mem(ADDR, 0x75, 1)[0]))

i2c.writeto_mem(ADDR, 0x6B, b"\x00")   # wake from sleep
i2c.writeto_mem(ADDR, 0x1C, b"\x00")   # accel ±2g -> 16384 = 1g
i2c.writeto_mem(ADDR, 0x1B, b"\x00")   # gyro ±250 deg/s -> 131 = 1 deg/s
time.sleep_ms(100)

def read_mpu():
    data = i2c.readfrom_mem(ADDR, 0x3B, 14)
    ax, ay, az, t, gx, gy, gz = struct.unpack(">hhhhhhh", data)
    return (ax / 16384, ay / 16384, az / 16384,
            gx / 131, gy / 131, gz / 131,
            t / 340 + 36.53)

for i in range(20):
    ax, ay, az, gx, gy, gz, temp = read_mpu()
    print("accel[g] x={:+.2f} y={:+.2f} z={:+.2f}  gyro[deg/s] x={:+6.1f} y={:+6.1f} z={:+6.1f}"
          .format(ax, ay, az, gx, gy, gz))
    time.sleep(0.2)
```

## How MicroPython and C++ code correspond

This is the correspondence for rewriting code tried in MicroPython in C++.
The `CMakeLists.txt` column shows the library to add to `target_link_libraries` (Chapter 5).

| Task | MicroPython | C++ (Pico SDK) | CMakeLists.txt |
| --- | --- | --- | --- |
| Make an output | `Pin(25, Pin.OUT)` | `gpio_init(25); gpio_set_dir(25, GPIO_OUT);` | |
| Output a value | `led.value(1)` | `gpio_put(25, true);` | |
| Input with pull-up | `Pin(24, Pin.IN, Pin.PULL_UP)` | `gpio_init(24); gpio_set_dir(24, GPIO_IN); gpio_pull_up(24);` | |
| Read | `btn.value()` | `gpio_get(24)` | |
| Wait | `time.sleep_ms(20)` | `sleep_ms(20);` | |
| Time since start-up | `time.ticks_ms()` / `ticks_us()` | `to_ms_since_boot(get_absolute_time())` / `time_us_64()` | |
| Analog input | `ADC(26).read_u16()` (0–65535) | `adc_gpio_init(26); adc_select_input(0); adc_read()` (0–4095) | `hardware_adc` |
| Prepare I2C | `I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)` | `i2c_init(i2c0, 400000);` and `gpio_set_function(4, GPIO_FUNC_I2C);` and so on | `hardware_i2c` |
| Read a register | `i2c.readfrom_mem(addr, reg, n)` | Send the number with `i2c_write_blocking(...)`, then `i2c_read_blocking(...)` | `hardware_i2c` |
| Write a register | `i2c.writeto_mem(addr, reg, b"\x00")` | Send the number and value in a row with `i2c_write_blocking(...)` | `hardware_i2c` |
| PWM | `PWM(Pin(15))` | `gpio_set_function(15, GPIO_FUNC_PWM);` and `pwm_set_wrap` and so on | `hardware_pwm` |
| Turn 2 bytes into a number | `struct.unpack(">h", d)` | `int16_t v = (d[0] << 8) + d[1];` | |
| Timer interrupt | `machine.Timer` | `add_repeating_timer_ms(...)` | |
| The second core | `_thread` | `multicore_launch_core1(...)` | `pico_multicore` |
| Watchdog | `machine.WDT(timeout=2000)` | `watchdog_enable(2000, true);` and `watchdog_update();` | `hardware_watchdog` |
| Save to a file | `open("log.csv", "a")` | None. Send to the PC over USB | |

- The ADC value ranges differ. MicroPython's `read_u16()` is scaled to 0–65535, while C++'s `adc_read()` is the raw 12 bits (0–4095)
- The ADC numbers are 0 for GP26, 1 for GP27, 2 for GP28 and 4 for the built-in temperature sensor

## Working with commands (mpremote)

You can do the same things with terminal commands instead of Pico Studio, using **mpremote**, MicroPython's official tool.

```bash
sudo apt install pipx
pipx install mpremote
pipx ensurepath
```

### List of commands

Go from the top. From the second time on, start at step 2, and skip step 3 if MicroPython is already on it.

| Step | What to do | Command |
| --- | --- | --- |
| 1 | Install mpremote (first time only) | `pipx install mpremote` |
| 2 | Check that it is detected over USB | `lsusb -d 2e8a:` |
| 3 | Flash MicroPython (only in BOOTSEL mode) | `cp RPI_PICO-*.uf2 /run/media/$USER/RPI-RP2/` |
| 4 | Check the serial port | `ls -l /dev/ttyACM0` |
| 5 | Check that MicroPython responds | `mpremote exec "import os; print(os.uname())"` |
| 6 | Run code | `mpremote run hello.py` |
| 7 | Stop a run | Ctrl + C, then `mpremote soft-reset` |
| 8 | Save to the Pico | `mpremote cp hello.py :hello.py` |
| 9 | Check the saved files | `mpremote ls` |
| 10 | Try things line by line in the REPL (when needed) | `mpremote repl` |
| 11 | Restart the Pico (when needed) | `mpremote reset` |

> **It cannot be used at the same time as Pico Studio.** If two programs use one port, their communication gets mixed up and stops working.
> Before using the commands, press "切断" (Disconnect) in Pico Studio.

## Common errors

| Error | Meaning and fix |
| --- | --- |
| `SyntaxError: invalid syntax` | A grammar mistake. Look for a missing `:`, an unclosed bracket, or full-width (Japanese) symbols such as `（` or `：` |
| `IndentationError` | The indentation is off. Line it up with 4 spaces |
| `NameError: name 'xxx' isn't defined` | No variable or function with that name. Is it misspelled, or did you forget an `import`? |
| `ImportError: no module named 'xxx'` | That library is not in MicroPython. Libraries for the PC (numpy and so on) cannot be used as is. If it is a file you made, is it saved on the Pico? |
| `TypeError` | A wrong combination of types (numbers, text and so on). For example, joining text and a number with `+` → use `str(number)` |
| `OSError: [Errno 5] EIO` | I2C communication failed. Check the wiring, address and power, and run the I2C scan from Chapter 9 |
| `OSError: [Errno 110] ETIMEDOUT` | The sensor does not respond. Check the wiring and lower it to `freq=100000` |
| `OSError: [Errno 2] ENOENT` | That file does not exist. Check the spelling of the file name and the "Files on the Pico" list |
| `MemoryError` | Out of memory. Make lists smaller, use `array`, save often |
| `KeyboardInterrupt` | Appears when you stop with "■ 停止" (Stop). Not an error |

## Going back to a C++ program

1. Hold the Pico's **BOOT** while connecting USB (while MicroPython is running, VS Code cannot put it into flashing mode automatically)
2. Press **Run Project (USB)** in VS Code (Chapter 4)

From then on, a C++ program is running, so you can flash without pressing BOOT.

## Summary

- Use MicroPython for early experiments before writing C++. Products are in C++
- Connect while holding BOOT and install it with "最新の MicroPython を書き込む" (Flash the latest MicroPython) in Pico Studio
- Try with "▶ 実行" (Run), stop with "■ 停止" (Stop), test line by line in the REPL, and save as main.py to run at power-on
- To go back to C++, connect while holding BOOT, then Run in VS Code
