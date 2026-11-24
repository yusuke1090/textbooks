# Appendix I. Showing a cheap camera's pictures on a PC

Connect an OV7670 camera from AliExpress (about 300 yen) to the Pico, send the pictures it takes to your PC over USB, and show them in a window.
You can also save the pictures, so they become material for teaching a machine learning model to spot crows later (idea #6 in Appendix H).

## The overall shape

```text
Camera (OV7670)  takes a picture as a number for each dot's colour
   │ 18 wires
   ▼
Pico             sends one when the PC asks
   │ USB
   ▼
PC               shows it and saves it
```

The Pico has only 264 KB of memory, so it just receives pictures and passes them on. One 320×240 picture uses 150 KB of it. Recognising things (machine learning) is the PC's job.

## Choosing a camera

| Camera | Rough price | Differences |
| --- | --- | --- |
| **OV7670 (18-pin)** | 200–500 yen | Used in this appendix. The cheapest. 0.3 megapixels. It cannot make JPEGs, so it sends the colour numbers as they are |
| OV2640 (18-pin) | 500–1,500 yen | 2 megapixels. It makes the JPEG inside the camera, so even big pictures travel quickly |
| ESP32-CAM | 1,000–2,000 yen | A camera and a Wi-Fi microcontroller on one board. Shows pictures in a browser without a Pico, but many have no Japanese radio certification (giteki) |

Prices are rough AliExpress figures from November 2026. To tell whether a crow is there, 0.3 megapixels is enough (machine learning shrinks pictures to about 96×96 anyway). So we use the cheapest, the OV7670.

![ESP32-CAM (the OV2640 is joined by a thin ribbon cable)](images/esp32-cam.jpg)

### What to check when buying

Search AliExpress for **OV7670 camera module**.

- The photo should show **18 pins standing in 2 rows of 9**. The **FIFO** version (with a big "AL422B" chip on the back and 22 pins) is a different thing, and the programs in this appendix do not work with it
- It should run on **3.3 V**

## What you need

| Item | How many | Notes |
| --- | --- | --- |
| OV7670 camera (18-pin, no FIFO) | 1 | AliExpress |
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
| SIOC, SIOD | Write the camera's settings. Works the same way as I2C (Chapter 11) |
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
3. Look at the names printed on the camera board and push the female ends of the wires onto those pins
4. Push each male end into a free hole in **the same vertical column** as the Pico pin number in the table. For the top row (pins 1–20) holes a and b are free; for the bottom row (pins 21–40), holes i and j
5. Put RESET in the column for pin 36 and PWDN in the column for pin 38. Two wires in the same vertical column is fine (they are joined inside)

![Video: wiring the camera to the Pico, then writing a program to check it](videos/en/camera-wiring.mp4)

- D0–D7 must be **eight pins in a row** (GP14–GP21). The library needs it that way
- If there is a protective film on the lens, peel it off

## Making the project

1. Open **New C/C++ Project** in the "Raspberry Pi Pico" VS Code extension (Chapter 4). Name it `camera`, put it in `~/apps`, tick **Console over USB** and **Generate C++ code**, and create it
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
    c.pixel_format = PIXFORMAT_RGB565; // send each dot's colour in 2 bytes
    c.frame_size = FRAMESIZE_QVGA;     // 320×240
    c.fb_count = 1;
    return c;
}

// Brightness of the picture (0–255): the average green of all the dots
int brightness(const camera_fb_t *fb) {
    size_t n = fb->len / 2;                                         // number of dots (2 bytes each)
    uint32_t sum = 0;
    for (size_t i = 0; i < n; i++) {
        uint16_t px = (fb->buf[2 * i] << 8) | fb->buf[2 * i + 1];   // the high byte comes first
        sum += (px >> 5) & 0x3F;                                    // green (0–63)
    }
    return (int)(sum * 255 / (63 * n));
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
            printf("%u×%u picture, %u bytes  brightness %d\n",
                   (unsigned)fb->width, (unsigned)fb->height, (unsigned)fb->len, brightness(fb));
            pico_camera_fb_return(fb);
        }
        sleep_ms(1000);
    }
}
```

- `pico_camera_init()` finds the camera, sets it up and reserves space in memory for a picture (153,600 bytes)
- `pico_camera_fb_get()` takes one picture; when you have finished with it, give the space back with `pico_camera_fb_return()`. If you don't, the next picture cannot be taken
- `PIXFORMAT_RGB565` stores the colour of one dot in 2 bytes (16 bits): 5 bits of red, 6 of green and 5 of blue, with the high byte first. At 320×240 that is 320×240×2 = 153,600 bytes
- `brightness()` turns the average green (0–63) of all the dots into 0–255. Green is the colour the human eye feels most strongly as brightness

### Reading Serial Monitor

If it works, the picture size and brightness appear every second (the brightness numbers are just examples).

```text
Camera: OV7670
320×240 picture, 153600 bytes  brightness 118
320×240 picture, 153600 bytes  brightness 121
320×240 picture, 153600 bytes  brightness 6      ← lens covered with a hand
```

The number of bytes is always 153600, whatever the camera sees (nothing is shrunk as in a JPEG). Use the **brightness** to check the wiring: if the number drops when you cover the lens with your hand and comes back when you take it away, it worked.

| What appears | Cause and fix |
| --- | --- |
| `Camera setup failed: no sensor detected on the SCCB bus (check wiring/power)` | The Pico cannot talk to the camera. Check 3.3V, GND, SIOC (GP13), SIOD (GP12) and XCLK (GP5). SIOC and SIOD swapped round is common. If the wiring is right and this still appears, connect SIOC and SIOD each to the 3.3 V column through a 4.7 kΩ–10 kΩ resistor |
| `Camera setup failed: not supported (e.g. JPEG on a sensor without a JPEG encoder)` | `c.pixel_format` is `PIXFORMAT_JPEG`. The OV7670 cannot make JPEGs, so use `PIXFORMAT_RGB565` |
| `Camera setup failed: invalid argument (check pins, pixel_format, frame_size)` | The pin numbers in the program are wrong. D0–D7 must be eight in a row, and SIOD must be an even GP |
| `Could not take a picture` again and again | One of VSYNC, HREF or PCLK is not connected |
| The brightness does not change when you cover the lens | One of D0–D7 is not connected, or they are in the wrong order |
| Nothing appears after `Camera: OV7670` | The picture is too big: the Pico ran out of memory and stopped. Set `c.frame_size` to `FRAMESIZE_QVGA` |

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
    c.pixel_format = PIXFORMAT_RGB565; // send each dot's colour in 2 bytes
    c.frame_size = FRAMESIZE_QVGA;     // 320×240
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
        printf("RGB %u %u\n", (unsigned)fb->width, (unsigned)fb->height);   // first line: width and height of the picture
        stdio_put_string((const char *)fb->buf, (int)fb->len, false, false);   // send the picture unchanged
        stdio_flush();
        pico_camera_fb_return(fb);
    }
}
```

When the PC sends the single character `c`, the Pico sends back one picture in this form.

```text
RGB 320 240        ← first line: width and height of the picture
(colour data, 320×240×2 = 153600 bytes)
```

- Because the width and height come first, the PC knows the picture is complete once it has read width × height × 2 bytes
- `printf()` changes `\n` into `\r\n` as it sends. The picture data also contains the same value as `\n`, so the picture goes out with `stdio_put_string()`, which sends it unchanged (the last `false` means "don't change")
- The Pico only takes a picture when the PC asks, so even if the PC is slow (with machine learning later), pictures do not pile up

### The PC program

Install OpenCV (a Python library for working with pictures). You installed pyserial in Chapter 3.

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
SCALE = 2               # how much to enlarge the window (320×240 is small, so ×2)


def to_image(data, w, h):
    """Turn RGB565 (2 bytes per dot) into an OpenCV image (blue, green, red 0-255 for each dot)"""
    px = np.frombuffer(data, ">u2").reshape(h, w)     # 2 bytes at a time, high byte first
    r = ((px >> 11) & 0x1F) << 3                       # red, 5 bits
    g = ((px >> 5) & 0x3F) << 2                        # green, 6 bits
    b = (px & 0x1F) << 3                               # blue, 5 bits
    return np.dstack([b, g, r]).astype(np.uint8)


def get_photo(ser):
    """Send c to the Pico and receive one picture. None if it fails"""
    ser.write(b"c")
    while True:
        line = ser.readline().decode(errors="replace").strip()
        if line == "":
            print("No reply from the Pico. Check that camera.cpp has been written to it")
            return None
        if line.startswith("RGB "):
            w, h = map(int, line.split()[1:])
            data = ser.read(w * h * 2)
            if len(data) < w * h * 2:
                print("The picture was cut short")
                return None
            return to_image(data, w, h)
        print("Pico:", line)            # messages such as ERR ...
        if line.startswith("ERR"):
            return None


def save(img):
    name = time.strftime(f"{SAVE_DIR}/%Y%m%d_%H%M%S.jpg")
    cv2.imwrite(name, img)
    print("Saved:", name)


ser = serial.Serial(PORT, 115200, timeout=3)
ser.reset_input_buffer()
os.makedirs(SAVE_DIR, exist_ok=True)
print("s to save, q to quit")
count, start, last_save = 0, time.time(), time.time()
while True:
    img = get_photo(ser)
    if img is None:
        time.sleep(1)
        continue
    cv2.imshow("camera", cv2.resize(img, None, fx=SCALE, fy=SCALE, interpolation=cv2.INTER_NEAREST))
    count += 1
    if time.time() - start >= 5:                # show the speed every 5 seconds
        print(f"{img.shape[1]}×{img.shape[0]}  {count / (time.time() - start):.1f} pictures a second")
        count, start = 0, time.time()
    key = cv2.waitKey(1) & 0xFF
    if key == ord("s") or (AUTO_SAVE and time.time() - last_save >= AUTO_SAVE):
        save(img)
        last_save = time.time()
    elif key == ord("q"):
        break
ser.close()
cv2.destroyAllWindows()
```

| Part | What it does |
| --- | --- |
| `get_photo()` | Sends `c`, waits for the `RGB 320 240` line, then reads width × height × 2 bytes. If an `ERR` line comes, it prints it |
| `to_image()` | Takes red, green and blue out of each 2-byte colour (RGB565), stretches each to 0–255 and makes an OpenCV image (a table of colours, one per dot) |
| `cv2.resize()` | 320×240 is small on a PC screen, so it enlarges the picture `SCALE` times |
| `cv2.imshow()` | Shows it in a window called `camera` |
| `cv2.waitKey(1)` | Redraws the window and picks up any key pressed. Without it the window freezes |
| `cv2.imwrite()` | Saves the picture as a JPEG file (the name ends in `.jpg`, so it becomes a JPEG) |

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
320×240  2.0 pictures a second
Saved: photos/20261124_093015.jpg
```

Each picture is 150 KB going over USB, so you get about 2 a second. To go faster, make the picture smaller (see "Changing things" below).

| What appears | Cause and fix |
| --- | --- |
| `could not open port /dev/ttyACM0: [Errno 16] Device or resource busy` | Serial Monitor or Pico Studio is using the port. Stop it |
| `could not open port /dev/ttyACM0: [Errno 2] No such file or directory` | The Pico is not connected. Check the USB cable |
| `ModuleNotFoundError: No module named 'cv2'` | OpenCV is missing. `sudo apt install python3-opencv` |
| `No reply from the Pico` | The Pico does not have `camera.cpp` (the one that shows pictures on the PC). Write it again |
| `Pico: 320×240 picture, 153600 bytes  brightness 118` keeps scrolling | The Pico still has the wiring-check program. Write the PC one |
| `Pico: ERR no sensor detected …` | The Pico cannot talk to the camera. Check the wiring as in the Serial Monitor table |
| The colours are wrong or there are stripes | D0–D7 are in the wrong order. Check them against the wiring table |
| The picture is whitish or blurry | Peel the protective film off the lens. Turning the lens a little brings it into focus |

### Files that appear

| File | When it appears and what it is |
| --- | --- |
| `PicoCamera/` | When you `git clone`. The library that drives the camera (C++ source) |
| `build/camera.uf2` | When you Compile. The program written to the Pico (Chapter 4) |
| `camera_view.py` | When you save it yourself. The program that runs on the PC |
| `photos/20261124_093015.jpg` | When you press **s** (or every so many seconds if you set `AUTO_SAVE`). A picture you took, named by date and time |

### Changing things

| What to change | Where |
| --- | --- |
| Picture size | `c.frame_size` in `camera.cpp`. `FRAMESIZE_QQVGA` (160×120; a quarter of the data, so more pictures a second) or `FRAMESIZE_QVGA` (320×240). `FRAMESIZE_VGA` (640×480) runs out of memory and the Pico stops |
| Saving automatically | `AUTO_SAVE = 10` in `camera_view.py` (every 10 seconds) |
| Window size | `SCALE` in `camera_view.py` (3 makes it three times bigger) |
| Upside down | Add the code below on the line after `pico_camera_init()` in `camera.cpp` |

```cpp
    if (err == PICO_CAMERA_OK) {
        sensor_t *s = pico_camera_sensor_get();
        s->set_vflip(s, 1);                        // flip upside down (set_hmirror flips left to right)
    }
```

## Using it to collect crow pictures

![A crow](images/h-crow.jpg)

- Point the camera where crows come, by a window for example, and run it with `AUTO_SAVE = 10` to collect pictures. Sorting them into folders of pictures with and without crows gives you the labels for training (Chapter 17)
- A program that spots crows will pass the `img` returned by `get_photo()` to a trained model. The Pico side stays exactly as it is
- To use it in the barn, plug it into the Raspberry Pi from Appendix H over USB instead of the PC. `camera_view.py` runs unchanged on the Raspberry Pi

## Summary

- The camera is an 18-pin OV7670 board (no FIFO). It is the cheapest, with 0.3 megapixels. It cannot make JPEGs, so the colour numbers of a 320×240 picture (153,600 bytes) are sent as they are
- There are 18 wires. D0–D7 go to eight pins in a row (GP14–GP21), SIOC and SIOD to I2C0 (GP13 and GP12), and XCLK is a 10 MHz clock from GP5
- `git clone` the PicoCamera library and add `add_subdirectory(PicoCamera)` and `pico_camera` to `CMakeLists.txt`
- With the wiring-check program, if the brightness number drops when you cover the lens with your hand, the wiring is right
- When the PC sends `c`, the Pico replies with an `RGB <width> <height>` line and the colour data. The data goes out unchanged with `stdio_put_string()`
- `camera_view.py` on the PC turns the colour numbers back into a picture, shows it in a window and saves it to `photos/` with **s**. The pictures you collect are the material for teaching crow spotting

## Exercises

```quiz
Q: With the wiring in this appendix, which GP number on the Pico does the camera's D0 connect to?
A: 14 | GP14
E: D0–D7 connect to GP14–GP21, eight pins in a row. If they are not in a row, the library cannot read them.

Q: The clock wire from the Pico goes to which pin on the camera?
A: XCLK
E: GP5 sends 10 MHz. Without it the camera does not work and you get `no sensor detected`.

Q: How many bytes is a 320×240 picture sent as RGB565 (2 bytes per dot)?
A: 153600 | 153,600 | 153600 bytes | 153,600 bytes
E: 320×240×2 = 153,600 bytes. The OV7670 cannot make JPEGs, so the size stays the same whatever the camera sees.

Q: In `camera_view.py`, which key saves a picture?
A: s
E: It saves into the `photos/` folder with the date and time as the name. q quits.

Q: `camera_view.py` says `Device or resource busy`. Which part of VS Code should you stop first?
A: Serial Monitor | the Serial Monitor
E: Only one program can use a port at a time. Disconnect Pico Studio too.
```
