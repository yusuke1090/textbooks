# Appendix I. Showing a cheap camera's pictures on a PC

Connect an OV2640 camera from AliExpress (about 1,000 yen) to the Pico, send the pictures it takes to your PC over USB, and show them in a window.
You can also save the pictures, so they become material for teaching a machine learning model to spot crows later (idea #6 in Appendix H).

## The overall shape

```text
Camera (OV2640)  takes a JPEG picture
   │ 18 wires
   ▼
Pico             sends one when the PC asks
   │ USB
   ▼
PC               shows it and saves it
```

The Pico has only 264 KB of memory, so it just receives pictures and passes them on. Recognising things (machine learning) is the PC's job.

## Choosing a camera

| Camera | Rough price | Differences |
| --- | --- | --- |
| **OV2640 (18-pin)** | 500–1,500 yen | Used in this appendix. 2 megapixels. It makes the JPEG inside the camera, so pictures travel quickly even over USB |
| OV7670 | 200–400 yen | The cheapest. 0.3 megapixels, and it cannot make JPEGs. The programs in this appendix do not work with it |
| ESP32-CAM | 1,000–2,000 yen | A camera and a Wi-Fi microcontroller on one board. Shows pictures in a browser without a Pico, but many have no Japanese radio certification (giteki) |

Prices are rough AliExpress figures from November 2026. Picture quality matters for spotting crows, so we use the OV2640.

![ESP32-CAM (the OV2640 is joined by a thin ribbon cable)](images/esp32-cam.jpg)

### What to check when buying

Search AliExpress for **OV2640 camera module 18pin**.

- The photo should show **18 pins standing in 2 rows of 9**. An OV2640 on just a thin ribbon cable (FPC) has no power circuit for the camera, so you cannot connect it straight to the Pico
- It should run on **3.3 V**
- Choose a lens with a **normal angle of view (60–70°)**. Wide 120° and 160° lenses bend the edges. Ones labelled "Night Vision" or "850nm" let infrared through, so daytime colours look reddish

## What you need

| Item | How many | Notes |
| --- | --- | --- |
| OV2640 camera (18-pin) | 1 | AliExpress |
| Pico | 1 | Your current RP2040 one. No wireless needed |
| Breadboard | 1 | The one from Appendix G |
| Jumper wires (male–female) | 18 | Female end on the camera pins, male end in the breadboard. 10 cm is best (long wires tend to spoil the picture) |
| USB cable | 1 | The one from Appendix G |

Male–female wires are also on AliExpress (**dupont wire male female 10cm**, about 200 yen for 40).

## Wiring

### What each wire does

![The image sensor inside a camera (OV7670). It takes in light and turns the brightness of each dot into a number](images/image-sensor.jpg)

| Wire | Job |
| --- | --- |
| 3.3V, GND | Power |
| SIOC, SIOD | Write the camera's settings. Works the same way as I2C (Chapter 8) |
| XCLK | The clock the Pico sends to the camera (10 million ticks a second). The camera does not work without it |
| VSYNC, HREF, PCLK | Signals for "a picture starts", "a line starts" and "next byte" |
| D0–D7 | The picture data. Eight wires send one byte at a time |
| RESET, PWDN | Restart and power-off. We don't use them, so RESET goes to 3.3 V and PWDN to GND |

The Pico reads D0–D7 at every PCLK signal using PIO (a small circuit for reading pins quickly). The library you add later drives the PIO.

### Connecting

![Wiring the camera to the Pico](images/en/camera-wiring.svg)

| Camera | Pico | Pin number |
| --- | --- | --- |
| 3.3V | 3V3(OUT) | 36 |
| GND | GND | 38 |
| SIOC | GP13 | 17 |
| SIOD | GP12 | 16 |
| VSYNC | GP2 | 4 |
| HREF | GP3 | 5 |
| PCLK | GP4 | 6 |
| XCLK | GP5 | 7 |
| D0–D3 | GP14–GP17 | 19, 20, 21, 22 |
| D4–D7 | GP18–GP21 | 24, 25, 26, 27 |
| RESET | 3V3(OUT) | 36 |
| PWDN | GND | 38 |

1. Unplug the USB cable
2. Push the Pico into the breadboard (as in Appendix G, across the middle groove)
3. Look at the names printed on the camera board and push the female ends of the wires onto those pins. Push the male ends into the row of holes beside the Pico pin with the matching number
4. Put RESET in the row for pin 36 and PWDN in the row for pin 38. Two wires in the same row is fine

- D0–D7 must be **eight pins in a row** (GP14–GP21). The library needs it that way
- Some boards name the data wires **D2–D9**. Then connect D2 to GP14, D3 to GP15 … D9 to GP21
- If there is a protective film on the lens, peel it off

## Making the project

1. Open **New C/C++ Project** in the "Raspberry Pi Pico" VS Code extension (Chapter 3). Name it `camera`, put it in `~/apps`, tick **Console over USB** and **Generate C++ code**, and create it
2. In the VS Code terminal, download the camera library [PicoCamera](https://github.com/umeiko/PicoCamera) into the project

```bash
cd ~/apps/camera
git clone --depth 1 --branch 0.4.2 https://github.com/umeiko/PicoCamera.git
```

After `Cloning into 'PicoCamera'...` you will see `You are in 'detached HEAD' state.` That only means you downloaded the fixed version 0.4.2; it is not a problem. If `ls PicoCamera` shows `CMakeLists.txt` and `src`, it worked.

3. Add two things to `CMakeLists.txt` (one line above `target_link_libraries`, and `pico_camera` inside it)

```cmake
add_subdirectory(PicoCamera)

target_link_libraries(camera
        pico_stdlib
        pico_camera)
```

| Added line | Meaning |
| --- | --- |
| `add_subdirectory(PicoCamera)` | Also read the `CMakeLists.txt` in the `PicoCamera` folder and build the library |
| `pico_camera` | Use that library in the `camera` program |

## Checking the wiring

Connect the USB cable to your PC. Replace the contents of `camera.cpp` with this program, then write it with **Compile → Run (USB)**. The first Compile takes a little longer because it builds the library too.

```cpp
#include <cstdio>
#include "pico/stdlib.h"
#include "PicoCamera.h"

// How the camera is connected (same GP numbers as the wiring table)
camera_config_t camera_config() {
    camera_config_t c = {};
    c.pin_sccb_sda = 12;               // SIOD
    c.pin_sccb_scl = 13;               // SIOC
    c.pin_vsync = 2;
    c.pin_href = 3;
    c.pin_pclk = 4;
    c.pin_xclk = 5;
    c.pin_d0 = 14; c.pin_d1 = 15; c.pin_d2 = 16; c.pin_d3 = 17;   // D0–D7 are GP14–GP21 (eight in a row)
    c.pin_d4 = 18; c.pin_d5 = 19; c.pin_d6 = 20; c.pin_d7 = 21;
    c.pin_reset = -1;                  // RESET is tied to 3.3 V and PWDN to GND,
    c.pin_pwdn = -1;                   // so the Pico does not drive them
    c.xclk_freq_hz = 10000000;         // clock sent to the camera (10 MHz)
    c.sccb_i2c_port = 0;               // GP12 and GP13 are I2C0
    c.pixel_format = PIXFORMAT_JPEG;
    c.frame_size = FRAMESIZE_VGA;      // 640×480
    c.jpeg_quality = 12;               // 0–63. Smaller is sharper and gives more data
    c.fb_count = 1;
    return c;
}

int main() {
    stdio_init_all();
    sleep_ms(3000);                    // wait for Serial Monitor to connect
    camera_config_t config = camera_config();
    pico_camera_err_t err = pico_camera_init(&config);
    while (err != PICO_CAMERA_OK) {
        printf("Camera setup failed: %s\n", pico_camera_err_str(err));
        sleep_ms(1000);
    }
    printf("Camera: %s\n", pico_camera_sensor_info_get()->name);
    while (true) {
        camera_fb_t *fb = pico_camera_fb_get();
        if (fb == nullptr) {
            printf("Could not take a picture\n");
        } else {
            bool jpeg = fb->len > 2 && fb->buf[0] == 0xFF && fb->buf[1] == 0xD8;   // a JPEG starts with FF D8
            printf("%u×%u picture, %u bytes (JPEG %s)\n",
                   (unsigned)fb->width, (unsigned)fb->height, (unsigned)fb->len, jpeg ? "OK" : "NG");
            pico_camera_fb_return(fb);
        }
        sleep_ms(1000);
    }
}
```

- `pico_camera_init()` finds the camera, sets it up and reserves space in memory for a picture (about 85 KB)
- `pico_camera_fb_get()` takes one picture; when you have finished with it, give the space back with `pico_camera_fb_return()`. If you don't, the next picture cannot be taken

### Reading Serial Monitor

If it works, the size of a picture appears every second (the number of bytes changes with what the camera sees).

```text
Camera: OV2640
640×480 picture, 18234 bytes (JPEG OK)
640×480 picture, 18190 bytes (JPEG OK)
```

| What appears | Cause and fix |
| --- | --- |
| `Camera setup failed: no sensor detected on the SCCB bus (check wiring/power)` | The Pico cannot talk to the camera. Check 3.3V, GND, SIOC (GP13), SIOD (GP12) and XCLK (GP5). SIOC and SIOD swapped round is common |
| `Camera setup failed: not supported (e.g. JPEG on a sensor without a JPEG encoder)` | The camera is not an OV2640 (an OV7670, for example) |
| `Camera setup failed: invalid argument (check pins, pixel_format, frame_size)` | The pin numbers in the program are wrong. D0–D7 must be eight in a row, and SIOD must be an even GP |
| `Could not take a picture` again and again | One of VSYNC, HREF or PCLK is not connected |
| `(JPEG NG)` | D0–D7 are in the wrong order. On a D2–D9 board, D2 goes to GP14 |

## Showing it on the PC

### The Pico program

Replace the contents of `camera.cpp` with this program, then write it with **Compile → Run (USB)**. `camera_config()` is the same as above.

```cpp
#include <cstdio>
#include "pico/stdlib.h"
#include "PicoCamera.h"

// How the camera is connected (same GP numbers as the wiring table)
camera_config_t camera_config() {
    camera_config_t c = {};
    c.pin_sccb_sda = 12;               // SIOD
    c.pin_sccb_scl = 13;               // SIOC
    c.pin_vsync = 2;
    c.pin_href = 3;
    c.pin_pclk = 4;
    c.pin_xclk = 5;
    c.pin_d0 = 14; c.pin_d1 = 15; c.pin_d2 = 16; c.pin_d3 = 17;   // D0–D7 are GP14–GP21 (eight in a row)
    c.pin_d4 = 18; c.pin_d5 = 19; c.pin_d6 = 20; c.pin_d7 = 21;
    c.pin_reset = -1;                  // RESET is tied to 3.3 V and PWDN to GND,
    c.pin_pwdn = -1;                   // so the Pico does not drive them
    c.xclk_freq_hz = 10000000;         // clock sent to the camera (10 MHz)
    c.sccb_i2c_port = 0;               // GP12 and GP13 are I2C0
    c.pixel_format = PIXFORMAT_JPEG;
    c.frame_size = FRAMESIZE_VGA;      // 640×480
    c.jpeg_quality = 12;               // 0–63. Smaller is sharper and gives more data
    c.fb_count = 1;
    return c;
}

int main() {
    stdio_init_all();
    camera_config_t config = camera_config();
    pico_camera_err_t err = pico_camera_init(&config);
    while (true) {
        int ch = getchar_timeout_us(100000);           // wait for one character from the PC (every 0.1 s)
        if (ch != 'c') continue;                       // take a picture when "c" arrives
        if (err != PICO_CAMERA_OK) {
            printf("ERR %s\n", pico_camera_err_str(err));
            continue;
        }
        camera_fb_t *fb = pico_camera_fb_get();
        if (fb == nullptr) {
            printf("ERR could not take a picture\n");
            continue;
        }
        printf("JPG %u\n", (unsigned)fb->len);          // first line: size of the picture in bytes
        stdio_put_string((const char *)fb->buf, (int)fb->len, false, false);   // send the picture unchanged
        stdio_flush();
        pico_camera_fb_return(fb);
    }
}
```

When the PC sends the single character `c`, the Pico sends back one picture in this form.

```text
JPG 18234          ← first line: how many bytes follow
(18234 bytes of JPEG data)
```

- Because the size comes first, the PC knows the picture is complete once it has read that many bytes
- `printf()` changes `\n` into `\r\n` as it sends. The picture data also contains the same value as `\n`, so the picture goes out with `stdio_put_string()`, which sends it unchanged (the last `false` means "don't change")
- The Pico only takes a picture when the PC asks, so even if the PC is slow (with machine learning later), pictures do not pile up

### The PC program

Install OpenCV (a Python library for working with pictures). You installed pyserial in Chapter 2.

```bash
sudo apt install python3-opencv
```

Save the following program as `~/apps/camera/camera_view.py`.

```python
# camera_view.py  - usage: python3 camera_view.py
import os, time
import cv2
import numpy as np
import serial

PORT = "/dev/ttyACM0"
SAVE_DIR = "photos"     # folder for pictures saved with s
AUTO_SAVE = 0           # save automatically every this many seconds (0 = never)


def get_photo(ser):
    """Send c to the Pico and receive one picture (JPEG). None if it fails"""
    ser.write(b"c")
    while True:
        line = ser.readline().decode(errors="replace").strip()
        if line == "":
            print("No reply from the Pico. Check that camera.cpp has been written to it")
            return None
        if line.startswith("JPG "):
            size = int(line[4:])
            data = ser.read(size)
            if len(data) < size:
                print("The picture was cut short")
                return None
            return data
        print("Pico:", line)            # messages such as ERR ...
        if line.startswith("ERR"):
            return None


def save(data):
    name = time.strftime(f"{SAVE_DIR}/%Y%m%d_%H%M%S.jpg")
    with open(name, "wb") as f:
        f.write(data)
    print("Saved:", name)


ser = serial.Serial(PORT, 115200, timeout=2)
ser.reset_input_buffer()
os.makedirs(SAVE_DIR, exist_ok=True)
print("s to save, q to quit")
count, start, last_save = 0, time.time(), time.time()
while True:
    data = get_photo(ser)
    if data is None:
        time.sleep(1)
        continue
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        print("Could not read the JPEG (moving on to the next one)")
        continue
    cv2.imshow("camera", img)
    count += 1
    if time.time() - start >= 5:                # show the speed every 5 seconds
        print(f"{img.shape[1]}×{img.shape[0]}  {count / (time.time() - start):.1f} pictures a second")
        count, start = 0, time.time()
    key = cv2.waitKey(1) & 0xFF
    if key == ord("s") or (AUTO_SAVE and time.time() - last_save >= AUTO_SAVE):
        save(data)
        last_save = time.time()
    elif key == ord("q"):
        break
ser.close()
cv2.destroyAllWindows()
```

| Part | What it does |
| --- | --- |
| `get_photo()` | Sends `c`, waits for the `JPG 18234` line, then reads that many bytes. If an `ERR` line comes, it prints it |
| `cv2.imdecode()` | Turns the JPEG data back into an OpenCV image (a table of colours, one per dot) |
| `cv2.imshow()` | Shows it in a window called `camera` |
| `cv2.waitKey(1)` | Redraws the window and picks up any key pressed. Without it the window freezes |

### Running it

1. Stop VS Code's Serial Monitor (and if you were using Pico Studio, press "Disconnect"). Only one program can use a port at a time
2. Run it in a terminal

```bash
cd ~/apps/camera
python3 camera_view.py
```

3. A window called `camera` opens and pictures appear one after another. With the window selected, press **s** to save and **q** to finish

If it works, the terminal shows something like this (the pictures per second is just an example).

```text
s to save, q to quit
640×480  4.8 pictures a second
Saved: photos/20261121_093015.jpg
```

| What appears | Cause and fix |
| --- | --- |
| `could not open port /dev/ttyACM0: [Errno 16] Device or resource busy` | Serial Monitor or Pico Studio is using the port. Stop it |
| `could not open port /dev/ttyACM0: [Errno 2] No such file or directory` | The Pico is not connected. Check the USB cable |
| `ModuleNotFoundError: No module named 'cv2'` | OpenCV is missing. `sudo apt install python3-opencv` |
| `No reply from the Pico` | The Pico does not have `camera.cpp` (the one that shows pictures on the PC). Write it again |
| `Pico: 640×480 picture, 18234 bytes (JPEG OK)` keeps scrolling | The Pico still has the wiring-check program. Write the PC one |
| `Pico: ERR no sensor detected …` | The Pico cannot talk to the camera. Check the wiring as in the Serial Monitor table |
| The picture is whitish or blurry | Peel the protective film off the lens. Turning the lens a little brings it into focus (some are glued and do not turn) |

### Files that appear

| File | When it appears and what it is |
| --- | --- |
| `PicoCamera/` | When you `git clone`. The library that drives the camera (C++ source) |
| `build/camera.uf2` | When you Compile. The program written to the Pico (Chapter 3) |
| `camera_view.py` | When you save it yourself. The program that runs on the PC |
| `photos/20261121_093015.jpg` | When you press **s** (or every so many seconds if you set `AUTO_SAVE`). A picture you took, named by date and time |

### Changing things

| What to change | Where |
| --- | --- |
| Picture size | `c.frame_size` in `camera.cpp`. `FRAMESIZE_QVGA` (320×240, fast), `FRAMESIZE_VGA` (640×480) or `FRAMESIZE_SVGA` (800×600; anything bigger runs out of memory) |
| Picture quality | `c.jpeg_quality` in `camera.cpp` (10–20; smaller is sharper but slower) |
| Saving automatically | `AUTO_SAVE = 10` in `camera_view.py` (every 10 seconds) |
| Upside down | Add the code below on the line after `pico_camera_init()` in `camera.cpp` |

```cpp
    if (err == PICO_CAMERA_OK) {
        sensor_t *s = pico_camera_sensor_get();
        s->set_vflip(s, 1);                        // flip upside down (set_hmirror flips left to right)
    }
```

## Using it to collect crow pictures

![A crow](images/h-crow.jpg)

- Point the camera where crows come, by a window for example, and run it with `AUTO_SAVE = 10` to collect pictures. Sorting them into folders of pictures with and without crows gives you the labels for training (Chapter 14)
- A program that spots crows will pass the `img` received by `get_photo()` to a trained model. The Pico side stays exactly as it is
- To use it in the barn, plug it into the Raspberry Pi from Appendix H over USB instead of the PC. `camera_view.py` runs unchanged on the Raspberry Pi

## Summary

- The camera is an 18-pin OV2640 board. It makes the JPEG inside the camera, so 640×480 pictures fit through the Pico's small memory and USB
- There are 18 wires. D0–D7 go to eight pins in a row (GP14–GP21), SIOC and SIOD to I2C0 (GP13 and GP12), and XCLK is a 10 MHz clock from GP5
- `git clone` the PicoCamera library and add `add_subdirectory(PicoCamera)` and `pico_camera` to `CMakeLists.txt`
- When the PC sends `c`, the Pico replies with a `JPG <bytes>` line and the JPEG. The picture goes out unchanged with `stdio_put_string()`
- `camera_view.py` on the PC shows it in a window and saves it to `photos/` with **s**. The pictures you collect are the material for teaching crow spotting

## Exercises

```quiz
Q: With the wiring in this appendix, which GP number on the Pico does the camera's D0 connect to?
A: 14 | GP14
E: D0–D7 connect to GP14–GP21, eight pins in a row. If they are not in a row, the library cannot read them.

Q: The clock wire from the Pico goes to which pin on the camera?
A: XCLK
E: GP5 sends 10 MHz. Without it the camera does not work and you get `no sensor detected`.

Q: What format does the OV2640 use to shrink a picture inside the camera?
A: JPEG | JPG
E: A 640×480 picture becomes a few tens of KB. The OV7670 cannot do this.

Q: In `camera_view.py`, which key saves a picture?
A: s
E: It saves into the `photos/` folder with the date and time as the name. q quits.

Q: `camera_view.py` says `Device or resource busy`. Which part of VS Code should you stop first?
A: Serial Monitor | the Serial Monitor
E: Only one program can use a port at a time. Disconnect Pico Studio too.
```
