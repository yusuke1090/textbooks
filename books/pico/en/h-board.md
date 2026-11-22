# Appendix H. Building the message-board ideas with the Pico

This appendix shows how to build, with the Pico, the six ideas posted on the Smart Agri News [message board](https://yusuke1090.github.io/smart-agri-news/board.html), and what to buy for each one.
Prices are rough Amazon Japan prices (November 2026). They change by shop and over time.

## The overall shape

### Splitting the work between the Pico and a Raspberry Pi

The Pico is good at measuring and moving things. It is poor at looking at camera video with AI (it has only about 0.5 MB of memory).
So the camera goes to a Raspberry Pi in the barn, and the Pico measures, moves and sends.

```text
Pico (cow, barn)      measure, move, send
   │ Wi-Fi
   ▼
Raspberry Pi (barn)   collect, camera, page
   │ Wi-Fi
   ▼
Phone                 view
```

Everything runs inside the barn Wi-Fi, even without the internet (the same idea as Chapter 18).

![Raspberry Pi 5 (used as the barn receiver)](images/h-rpi5.jpg)

### The six ideas and what to build

| Board post | What the Pico builds | Difficulty |
| --- | --- | --- |
| #1 Cattle management system | Activity collar (continues Chapters 15–19) | ★★★ |
| #2 Single-purpose sensors | Leg and tail tags, drinking-water flow meter | ★★ |
| #3 Barn environment | Temperature, humidity, THI and CO2 meter | ★ |
| #4 Night mounting and cows that cannot stand | Tailhead mount sensor, leg tag | ★★ |
| #5 App for surplus raw milk | Almost nothing (it is mostly an app) | − |
| #6 Scaring off crows | Pan-and-tilt water gun (the Raspberry Pi finds the crows) | ★★★ |

**Start with #3 (barn environment).** Nothing is attached to a cow, and it runs from a wall socket, so it is the easiest.
Next build the flow meter from #2, then move on to the things that go on cows (tags, collar, mount sensor).

### Things every build uses

Search Amazon for the words in bold. Keep using what you bought for Appendix G (breadboard, male-male wires, resistors, battery box, soldering iron).

| Item | How many | Rough price |
| --- | --- | --- |
| **Raspberry Pi Pico 2 WH** (wireless, pin headers fitted) | One per build | About ¥2,000 each |
| **Raspberry Pi 5** (2 GB or 4 GB) | 1 | ¥15,000–25,000 |
| **Raspberry Pi 5 27W power supply** (official) | 1 | About ¥2,000 |
| **microSD 32GB** | 1 | About ¥1,000 |
| **Raspberry Pi 5 case with fan** | 1 | About ¥1,500 |
| **micro USB cable, data** | 2 | About ¥500 |
| **USB charger 5V** (for Picos running from a socket) | 2 | About ¥1,000 |
| **Jumper wires male-female** and **female-female** | 1 bag each | About ¥500 |
| **Resistor kit** (one that includes 10 kΩ) | 1 box | About ¥1,000 |
| **Waterproof case IP67** (about 10 cm) | One per build | About ¥1,000 each |
| **Digital multimeter** | 1 | About ¥2,000 |

- Because the builds are wireless, the Pico must be **one with a W**. The Pico 2 W has a micro-USB port
- For anything that transmits radio, choose a board with the Japanese **technical conformity mark (技適)** (Chapter 19). Some compatible boards shipped directly from abroad do not have it
- The Raspberry Pi 5 went up in price several times in 2026. Check the price before buying. While you are trying things out, your usual PC can be the receiver

### Sending to the Raspberry Pi (used by every build)

In every build, the Pico makes one line a minute and sends it to the Raspberry Pi. All lines have this shape:

```text
type,number,name=value,name=value …
env,1,t=28.5,rh=70,thi=78,co2=850,alert=heat
```

A line with `alert=` in it is an alert.

#### On the Pico

1. In VS Code, use **New C/C++ Project** with Board type **Pico 2 W** and **Pico wireless options** set to **Background lwIP** (Chapter 4). `lwipopts.h` is created for you
2. Create `wifi_udp.h` in the same folder with the contents below. Change the Wi-Fi name, password and the Raspberry Pi's IP address
3. Call `wifi_begin()` at the start of the program, and change `printf(` to `send_line(`

```cpp
#pragma once
// Send one line at a time from a Pico W or Pico 2 W to the Raspberry Pi in the barn (the receiver)
#include <cstdarg>
#include <cstdio>
#include <cstring>
#include "pico/cyw43_arch.h"
#include "lwip/pbuf.h"
#include "lwip/udp.h"

#define WIFI_SSID     "barn Wi-Fi name"
#define WIFI_PASSWORD "Wi-Fi password"
#define RECEIVER_IP   "192.168.1.10"      // the Raspberry Pi's IP address (run hostname -I on it)
constexpr uint16_t RECEIVER_PORT = 5005;

inline udp_pcb* udp_out = nullptr;
inline ip_addr_t receiver;

// Connect to Wi-Fi (waits up to 30 s). Returns true when connected
inline bool wifi_connect() {
    return cyw43_arch_wifi_connect_timeout_ms(WIFI_SSID, WIFI_PASSWORD, CYW43_AUTH_WPA2_AES_PSK, 30000) == 0;
}

// Call once at the start of main()
inline bool wifi_begin() {
    if (cyw43_arch_init()) return false;
    cyw43_arch_enable_sta_mode();
    ipaddr_aton(RECEIVER_IP, &receiver);
    udp_out = udp_new();
    return wifi_connect();
}

// Send one line, written the same way as printf. It also goes to the USB Serial Monitor
inline void send_line(const char* fmt, ...) {
    char buf[200];
    va_list ap;
    va_start(ap, fmt);
    int n = vsnprintf(buf, sizeof buf, fmt, ap);
    va_end(ap);
    if (n <= 0) return;
    if (n >= (int)sizeof buf) n = sizeof buf - 1;
    printf("%s", buf);
    if (cyw43_wifi_link_status(&cyw43_state, CYW43_ITF_STA) != CYW43_LINK_JOIN) {
        wifi_connect();                       // reconnect if the link dropped
    }
    cyw43_arch_lwip_begin();
    pbuf* p = pbuf_alloc(PBUF_TRANSPORT, n, PBUF_RAM);
    if (p) {
        memcpy(p->payload, buf, n);
        udp_sendto(udp_out, p, &receiver, RECEIVER_PORT);
        pbuf_free(p);
    }
    cyw43_arch_lwip_end();
}
```

- **UDP** is a simple way to send that does not check whether the data arrived. A new line comes every minute, so losing the odd line does not matter
- Do not put a file containing your password on GitHub

#### On the Raspberry Pi

Run the following `receiver.py`. It saves the lines in one CSV per day and lets you see the latest values in your phone's browser.

```python
# receiver.py  - usage: python3 receiver.py (run it on the Raspberry Pi, then open http://<Pi's IP>:8000 on your phone)
# Lines from the Pico look like: type,number,name=value,name=value … (e.g. env,1,t=28.5,rh=70,thi=78)
import datetime
import html
import socket
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

DATA = Path.home() / "barn-data"      # folder for the CSV files (type-number-date.csv)
latest = {}                            # "env,1" → (time received, ["t=28.5", ...])


def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", 5005))
    while True:
        msg, _ = sock.recvfrom(1024)
        parts = msg.decode(errors="replace").strip().split(",")
        if len(parts) < 3:
            continue
        now = datetime.datetime.now()
        latest[",".join(parts[:2])] = (now, parts[2:])
        DATA.mkdir(exist_ok=True)
        with open(DATA / f"{parts[0]}-{parts[1]}-{now:%Y-%m-%d}.csv", "a") as f:
            f.write(f"{now:%H:%M:%S}," + ",".join(parts[2:]) + "\n")
        if any(p.startswith("alert=") for p in parts):
            print(now, "alert:", ",".join(parts), flush=True)   # you could notify your phone here


class Page(BaseHTTPRequestHandler):
    def do_GET(self):
        rows = ""
        for key, (t, values) in sorted(latest.items()):
            color = " style='color:red'" if any(v.startswith("alert=") for v in values) else ""
            rows += f"<tr{color}><td>{html.escape(key)}</td><td>{t:%H:%M}</td><td>{html.escape(' '.join(values))}</td></tr>"
        body = ("<meta charset='utf-8'><meta name='viewport' content='width=device-width'>"
                "<meta http-equiv='refresh' content='60'><h3>Barn</h3>"
                f"<table border='1' cellpadding='4'>{rows}</table>").encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):      # do not log every page view
        pass


threading.Thread(target=listen, daemon=True).start()
ThreadingHTTPServer(("", 8000), Page).serve_forever()
```

- Alert lines turn red on the page. To keep it running all the time, make it a systemd service (Appendix C)
- To get a notification on your phone, send it to a notification service where the `print(now, "alert:" …)` line is. In a barn without the internet, use a lamp or a buzzer instead (Chapter 18)

## #1 Cattle management system (collar)

> Board post: a buy-once, local-only system for small dairy farms, like U-motion

This is exactly what Chapters 15–19 of this guide have been building. The Pico on the collar works out the behaviour (resting, eating, ruminating and so on) from the acceleration and sends a summary to the Raspberry Pi every minute.

![A cow wearing a collar (New Zealand)](images/h-collar.jpg)

### What to buy (besides the shared items)

| Item | How many | Rough price |
| --- | --- | --- |
| **GY-521** (MPU-6050) | One per collar plus spares | About ¥1,000 for 3 |
| **Battery box 3×AA with switch** | One per collar | About ¥300 |
| **Nylon webbing 50mm with buckle** | One per collar | About ¥1,000 |

Cattle collars are also sold at livestock supply shops.

### How to build it

1. On the desk, connect the GY-521 (Chapters 10 and 11) and record the acceleration to flash (Chapter 15)
2. Put the Pico, GY-521 and batteries in the waterproof case, and fix it to the strap so the case sits on top of the neck
3. Put it on a cow and collect data together with video (Chapter 18, "4. Fit it to cows and collect data and video")
4. Build the behaviour classifier in Chapter 16 and shape it like `collar.cpp` from Chapter 19
5. Send the summary every minute with `send_line()` (for example `collar,12,rest=40,eat=20,rum=0`)
6. On the Raspberry Pi, compare each cow with its usual behaviour to flag possible heat or illness (Chapter 18, "9.")

### Things to watch out for

- With Wi-Fi connected all the time, 3 AA batteries last only a few days. First build the classifier in a trial of a few days. Think about making the batteries last (Chapter 17) or moving to a low-power microcontroller with BLE (Chapter 18) after that
- Decide how to fit it together with the person who looks after the cows

## #2 Single-purpose sensors

> Board post: cheap, small sensors that detect just one thing, such as calving, heat, signs of illness or how much water is drunk

The same set of Pico, GY-521 and batteries (a **tag**) becomes a different single-purpose sensor **depending on where you fit it**. Only drinking water needs a different build: a flow meter on the water pipe.

| Where it goes | What it tells you |
| --- | --- |
| Hind leg | Steps (more during heat), time lying down |
| Tail | Time the tail is raised (calving is near) |
| Neck | Rumination and eating (the #1 collar) |
| Water pipe | How much water was drunk (per trough) |

They all use the same `receiver.py` and the same page.

### Leg and tail tags

| Item | How many | Rough price |
| --- | --- | --- |
| **GY-521** (MPU-6050) | One per tag | About ¥1,000 for 3 |
| **Battery box 3×AA with switch** | One per tag | About ¥300 |
| **Hook and loop strap 50mm** (around the leg) | One per tag | About ¥800 |
| **Self-adhesive bandage** (around the tail; the kind vets use) | 1 roll | About ¥500 |

The wiring is the same as Chapter 11 (GY-521 VCC→3V3(OUT), GND→GND, SDA→GP4, SCL→GP5).
Fix the GY-521 so the **Y arrow** printed on the board points down along the leg (or tail).

```cpp run
#include <cmath>
#include <cstdio>
#include "pico/stdlib.h"
#include "mpu6050.h"

// A tag for the leg (or tail). Every minute: steps, seconds tilted, and minutes tilted in a row
constexpr int ID = 1;              // tag number (different for each cow)
constexpr int AXIS = 1;            // axis along the leg (tail): 0=X, 1=Y, 2=Z
constexpr float TILT_DEG = 60;     // tilted more than this = "sideways" (leg: lying, tail: raised)
constexpr float STEP_G = 1.4f;     // a jolt this big counts as one step [g]
constexpr int LONG_MIN = 180;      // alert when sideways for longer than this many minutes in a row
constexpr int HZ = 10;             // measurements per second

Mpu6050 imu(i2c0);

int main() {
    stdio_init_all();
    if (!imu.begin(4, 5)) printf("MPU-6050 not found (check the wiring)\n");

    int n = 0, steps = 0, tilt_n = 0, tilt_min = 0;
    bool swing = false;
    absolute_time_t next = get_absolute_time();
    while (true) {
        float a[3];
        imu.read_accel(a[0], a[1], a[2]);
        float g = std::sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2]);   // about 1 when still
        if (g > 0.5f) {
            float deg = std::acos(std::fmin(1.0f, std::fabs(a[AXIS]) / g)) * 57.3f;   // angle between axis and gravity
            if (deg > TILT_DEG) tilt_n++;
        }
        if (!swing && g > STEP_G) {        // count the moment the jolt gets big as one step
            steps++;
            swing = true;
        } else if (g < 1.1f) {
            swing = false;
        }

        if (++n == 60 * HZ) {              // one minute has passed
            int tilt_s = tilt_n / HZ;
            tilt_min = (tilt_s >= 50) ? tilt_min + 1 : 0;   // sideways for almost the whole minute: add a minute
            printf("tag,%d,steps=%d,tilt_s=%d,tilt_min=%d%s\n", ID, steps, tilt_s, tilt_min,
                   tilt_min >= LONG_MIN ? ",alert=long" : "");
            n = steps = tilt_n = 0;
        }
        next = delayed_by_ms(next, 1000 / HZ);
        sleep_until(next);
    }
}
```

| Value | On a leg | On the tail |
| --- | --- | --- |
| `steps` | Steps in the minute. Several times the usual number during heat | (not used) |
| `tilt_s` | Seconds lying down in the minute | Seconds the tail was raised in the minute |
| `tilt_min` | Minutes lying down in a row. Too long gives `alert=long` | (not used) |

- On the desk, stand the board up, lay it down and shake it to check the values change before fitting it to a cow
- Fit the tail tag a few days before the due date. When the tail is raised for much longer than usual, calving may be near
- Judge heat and calving by comparing with that cow's last few days (Chapter 18, "9."). Adjust the numbers (1.4 g, 60 degrees, 180 minutes) as you test

### Drinking-water flow meter

![Cows drinking](images/h-drink.jpg)

Fit a flow sensor in the pipe from the tap to the water trough, and count the pulses it gives each time its impeller turns.

| Item | How many | Rough price |
| --- | --- | --- |
| **YF-S201 water flow sensor** (1/2 inch) | 1 | About ¥1,000 |
| **Diode 1N4148** | 1 | About ¥300 for several |
| **Hose joint 1/2 thread** and **sealing tape** | 1 set | About ¥1,000 |

The YF-S201 runs on 5 V, and its signal may also come out at 5 V. To keep 5 V off the Pico's pin, put one diode in the signal line.

| YF-S201 wire | Connect to |
| --- | --- |
| Red (+) | VBUS (pin 40, the 5 V from USB) |
| Black (−) | GND (pin 38) |
| Yellow (signal) | The banded end of the diode. The other end goes to GP15 (pin 20) |

When the signal goes to 0 V, the pin is pulled low through the diode. When the signal is at 5 V, the diode blocks it, and the Pico's internal pull-up holds the pin at 3.3 V.

Push the parts into the breadboard as follows. How to push in the Pico, and the order of its pins, are the same as in "An external LED" in Chapter 8.

1. Push the diode's unbanded leg into a free hole in the column of pin 20 (GP15), and its banded leg into a free column to the left of the Pico
2. If the sensor's wires end in a connector (female), push three male-male jumper wires into it to extend them
3. Push yellow into the column of the diode's banded leg, red into the column of pin 40 (VBUS), and black into the column of pin 38 (GND). Pin 40 is at the right end of the bottom row, and pin 38 is third from the right

```cpp run
#include <cstdio>
#include "pico/stdlib.h"

// Flow sensor (YF-S201) on the water pipe. Every minute: how much water flowed
constexpr int ID = 1;
constexpr uint PIN = 15;                 // yellow wire (to GP15 through the diode)
constexpr float PULSES_PER_L = 450;      // pulses per litre (measure with a bucket and correct it)

volatile uint32_t pulses = 0;            // counted in an interrupt (Chapter 14)

void on_pulse(uint, uint32_t) {
    pulses++;
}

int main() {
    stdio_init_all();
    gpio_init(PIN);
    gpio_set_dir(PIN, GPIO_IN);
    gpio_pull_up(PIN);
    gpio_set_irq_enabled_with_callback(PIN, GPIO_IRQ_EDGE_FALL, true, &on_pulse);

    uint32_t last = 0;
    absolute_time_t next = get_absolute_time();
    while (true) {
        next = delayed_by_ms(next, 60 * 1000);
        sleep_until(next);
        uint32_t now = pulses;
        float liters = (now - last) / PULSES_PER_L;
        last = now;
        printf("water,%d,l=%.1f,total_l=%.0f,pulses=%lu\n", ID, liters, now / PULSES_PER_L, (unsigned long)now);
    }
}
```

- **Calibrating:** fill a bucket with 10 L, and set `PULSES_PER_L` to the increase in `pulses` divided by 10
- Point the arrow on the body in the direction the water flows. It is only accurate to about ±10%, so use it to spot "less than usual"
- Fit it in the hose just before the trough, so it does not count as plumbing work
- This tells you the amount per trough. To know how much each cow drinks, you need a way to tell which cow is drinking (such as RFID ear tags)

## #3 Barn environment

> Board post: temperature, humidity and THI, ventilation and smells, and how the cows look on camera. Keep only numbers, without sending video to the cloud

The Pico measures temperature, humidity, THI and CO2. Counting cows with a camera is the Raspberry Pi's job.

![A free-stall barn with fans](images/h-barn.jpg)

### What to buy

| Item | How many | Rough price |
| --- | --- | --- |
| **SHT31 module** (temperature, humidity) | 1 | About ¥1,000 |
| **SCD41 module** (CO2; optional) | 1 | ¥6,000–10,000 |
| **USB extension cable 3m** | 1 | About ¥800 |

### Wiring

The SHT31 and SCD41 are both I2C. Connect them side by side on the same four wires (Chapter 12). Push them into the breadboard the same way as in "Wiring steps" in Chapter 10.

| Pico | SHT31 and SCD41 |
| --- | --- |
| 3V3(OUT) (pin 36) | VIN (VCC) |
| GND (pin 38) | GND |
| GP4 (pin 6) | SDA |
| GP5 (pin 7) | SCL |

### The program

```cpp run
#include <cstdio>
#include "pico/stdlib.h"
#include "hardware/i2c.h"

// Barn environment. Every minute: temperature, humidity, THI, and CO2 (when an SCD41 is connected)
constexpr int ID = 1;
constexpr uint8_t SHT31 = 0x44;
constexpr uint8_t SCD41 = 0x62;
constexpr float THI_ALERT = 72;          // alert at this THI or above

// Check byte (CRC). The SHT31 and SCD41 use the same rule (Chapter 12)
uint8_t crc8(const uint8_t* data, int len) {
    uint8_t crc = 0xFF;
    for (int i = 0; i < len; i++) {
        crc ^= data[i];
        for (int b = 0; b < 8; b++) crc = (crc & 0x80) ? (crc << 1) ^ 0x31 : (crc << 1);
    }
    return crc;
}

// Send a 2-byte command
bool command(uint8_t addr, uint16_t cmd) {
    uint8_t b[2] = {uint8_t(cmd >> 8), uint8_t(cmd & 0xFF)};
    return i2c_write_blocking(i2c0, addr, b, 2, false) == 2;
}

// Read n sets (up to 3) of "2-byte value + 1 check byte"
bool read_words(uint8_t addr, uint16_t* w, int n) {
    uint8_t d[9];
    if (n > 3 || i2c_read_blocking(i2c0, addr, d, n * 3, false) != n * 3) return false;
    for (int i = 0; i < n; i++) {
        if (crc8(d + i * 3, 2) != d[i * 3 + 2]) return false;
        w[i] = (d[i * 3] << 8) | d[i * 3 + 1];
    }
    return true;
}

bool read_sht31(float& temp, float& hum) {
    uint16_t w[2];
    if (!command(SHT31, 0x2400)) return false;   // measure once
    sleep_ms(20);
    if (!read_words(SHT31, w, 2)) return false;
    temp = -45 + 175 * w[0] / 65535.0f;
    hum = 100 * w[1] / 65535.0f;
    return true;
}

bool read_co2(int& ppm) {
    uint16_t w[3];                                // CO2, temperature, humidity, in that order
    if (!command(SCD41, 0xEC05)) return false;    // read the measurement
    sleep_ms(1);
    if (!read_words(SCD41, w, 3)) return false;
    ppm = w[0];
    return true;
}

int main() {
    stdio_init_all();
    i2c_init(i2c0, 100 * 1000);
    gpio_set_function(4, GPIO_FUNC_I2C);
    gpio_set_function(5, GPIO_FUNC_I2C);
    gpio_pull_up(4);
    gpio_pull_up(5);
    sleep_ms(1000);
    command(SCD41, 0x3F86);                  // stop any earlier measuring (for when only the Pico restarted)
    sleep_ms(500);
    bool has_co2 = command(SCD41, 0x21B1);   // start measuring every 5 s; false if not connected

    absolute_time_t next = get_absolute_time();
    while (true) {
        next = delayed_by_ms(next, 60 * 1000);
        sleep_until(next);
        float t = 0, rh = 0;
        if (!read_sht31(t, rh)) {
            printf("env,%d,error=sht31\n", ID);
            continue;
        }
        float thi = 0.8f * t + rh / 100 * (t - 14.4f) + 46.4f;
        char co2[16] = "";
        int ppm = 0;
        if (has_co2 && read_co2(ppm)) snprintf(co2, sizeof co2, ",co2=%d", ppm);
        printf("env,%d,t=%.1f,rh=%.0f,thi=%.0f%s%s\n", ID, t, rh, thi, co2,
               thi >= THI_ALERT ? ",alert=heat" : "");
    }
}
```

- **THI** uses the same formula as the cattle textbook (0.8 × temperature + humidity/100 × (temperature − 14.4) + 46.4). Heat stress starts above 68–72, so it alerts at 72
- **CO2** is a guide to ventilation. Outside air is about 420 ppm; the higher it is inside the barn, the poorer the ventilation. For livestock buildings, staying below 3,000 ppm is a common guide
- Mount the sensors where cows cannot lick or bump them, out of direct sunlight and away from mist sprays
- To add **a guide to smell**, there is the ammonia sensor **MQ-137** (about ¥2,000). It does not give accurate ppm; it only shows whether it is going up or down. It runs on 5 V and its output goes up to 5 V, so divide it with 10 kΩ and 20 kΩ before feeding it to GP26 (Chapter 9)

### Counting cows with a camera (Raspberry Pi)

![Raspberry Pi AI Camera](images/h-ai-camera.jpg)

The **Raspberry Pi AI Camera** (about ¥15,000) runs the AI inside the camera and outputs the positions of cows, people, birds and so on. The Raspberry Pi only receives the positions, so it runs lightly. You can keep just the counts, without keeping any video.

1. Connect the AI Camera to the Raspberry Pi 5, run `sudo apt install imx500-all` and reboot
2. Download the examples with `git clone https://github.com/raspberrypi/picamera2`, then run `imx500_object_detection_demo.py` in `picamera2/examples/imx500/`. The model is `--model /usr/share/imx500-models/imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk`
3. Once you see boxes on the cows, add the function below to the example, and call `count_cows(last_results, get_labels())` after the list of detections (`last_results`) is made

```python
# Add to the official example (Raspberry Pi). Count cows inside set boxes and send to receiver.py every minute
import socket
import time

AREAS = {"feed": (0, 0, 640, 200), "water": (480, 200, 640, 480)}   # boxes in the image (left, top, right, bottom)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
last_sent = 0


def count_cows(detections, labels):
    global last_sent
    if time.time() - last_sent < 60:
        return
    last_sent = time.time()
    counts = {name: 0 for name in AREAS}
    for d in detections:
        if labels[int(d.category)] != "cow":
            continue
        x, y, w, h = d.box
        cx, cy = x + w / 2, y + h / 2                 # centre of the box
        for name, (x1, y1, x2, y2) in AREAS.items():
            if x1 <= cx < x2 and y1 <= cy < y2:
                counts[name] += 1
    line = "cam,1," + ",".join(f"{k}={v}" for k, v in counts.items())
    sock.sendto(line.encode(), ("127.0.0.1", 5005))  # to receiver.py on the same Raspberry Pi
```

- To run it without a screen, change `show_preview=True` in the example to `False`
- At night it cannot see without some light
- To tell lying cows apart, you need to label photos taken in the barn and train your own model (the same idea as Chapter 16)

## #4 Night mounting and cows that cannot stand

> Board post: use AI to find mounting at night and cows that cannot get up, send an alert, and have a person check and record it

The board idea uses a camera and AI, but with the Pico it is easier to learn the same things with sensors.

| What you want to know | How the Pico does it |
| --- | --- |
| Mounting | A pressure sensor on the tailhead counts one mount when pressed for 2 s or more |
| Cannot stand | The leg tag (#2) shows the cow has been lying down for too long |

If the sensors record when things happened, you can later use that as the correct answers (the labels in Chapter 16) when you build a camera AI.

### Mount sensor

A cow in heat stands still when other cows mount her (standing heat). A pressure sensor on the tailhead (the top of the base of the tail) tells you how many times and how long she was mounted.

| Item | How many | Rough price |
| --- | --- | --- |
| **FSR402 force sensor** | One per cow | About ¥1,500 each |
| 10 kΩ resistor (from the resistor kit) | One per cow | − |
| **Battery box 3×AA with switch** | One per cow | About ¥300 |
| A cloth patch and glue that works on cattle hair | 1 set | Ask a livestock supply shop or a vet |

| Part | Pico |
| --- | --- |
| One leg of the FSR402 | 3V3(OUT) (pin 36) |
| The other leg of the FSR402 | GP26 (pin 31) |
| 10 kΩ resistor | Between GP26 and GND (pin 33) |

The harder it is pressed, the lower the FSR402's resistance and the higher the voltage at GP26.

To try it on a desk, push the parts into the breadboard as follows.

1. Push the FSR402's two legs into two free vertical columns to the left of the Pico. If they slip out easily, cover them with the female ends of male-female jumper wires to extend them
2. With jumper wires, connect the column of one leg to the column of pin 36 (3V3(OUT)), and the column of the other leg to the column of pin 31 (GP26)
3. Push one leg of the 10 kΩ resistor into the column of the leg connected to pin 31, and the other leg into a free column. Connect that column to the column of pin 33 (GND) with a wire

```cpp run
#include <cstdio>
#include "pico/stdlib.h"
#include "hardware/adc.h"

// Mount sensor on the tailhead. Pressed for 2 s or more counts as "mounted"
constexpr int ID = 1;
constexpr uint PRESSED = 1500;                  // value that counts as pressed (0–4095; decide by pressing by hand)
constexpr uint32_t MIN_MS = 2000;               // shorter than this is not counted (just a bump)
constexpr uint32_t MAX_MS = 30000;              // longer than this is not counted (pushed against a rail)
constexpr uint32_t WINDOW_MS = 4 * 3600 * 1000; // 4 hours
constexpr int HEAT_COUNT = 3;                   // alert at this many mounts within 4 hours
constexpr int KEEP = 16;                        // how many mounts to remember

int main() {
    stdio_init_all();
    adc_init();
    adc_gpio_init(26);                          // GP26 = ADC0 (Chapter 9)
    adc_select_input(0);

    uint32_t times[KEEP] = {};                  // times of recent mounts
    int count = 0;
    uint32_t start = 0;
    bool pressed = false;
    while (true) {
        uint32_t now = to_ms_since_boot(get_absolute_time());
        bool p = adc_read() > PRESSED;
        if (p && !pressed) start = now;         // pressing started
        if (!p && pressed) {                    // released
            uint32_t len = now - start;
            if (len >= MIN_MS && len <= MAX_MS) {
                times[count % KEEP] = now;
                count++;
                int recent = 0;                 // mounts within 4 hours
                for (int i = 0; i < KEEP && i < count; i++) {
                    if (now - times[i] <= WINDOW_MS) recent++;
                }
                printf("mount,%d,sec=%.1f,in4h=%d%s\n", ID, len / 1000.0f, recent,
                       recent >= HEAT_COUNT ? ",alert=heat" : "");
            }
        }
        pressed = p;
        sleep_ms(100);
    }
}
```

- Decide `PRESSED` by pressing the sensor by hand while watching the value of `adc_read()` (Chapter 9)
- "3 mounts in 4 hours" is one of the guides used by tailhead heat-detection devices. Adjust it for your barn
- Clip the hair short where the patch goes. Decide how to stick it on, and what to do when it comes off, with the person who looks after the cows or a vet

### Cows that cannot stand

Use the leg tag from #2 as it is. A cow lies down for about an hour at a time, and normally does not stay down for hours on end.
When `tilt_min` (minutes lying down in a row) goes over `LONG_MIN` (180 minutes), it sends `alert=long`. At night, receive this alert with a lamp or on your phone.

## #5 App for surplus raw milk

> Board post: an app that connects surplus raw milk with demand for gelato, cheese, skim milk powder and so on

![A bulk tank (a tank that cools and stores raw milk)](images/h-bulk-tank.jpg)

The heart of this idea is an app that runs on phones and computers. There is almost nothing for the Pico to build.
How much milk will be surplus, and when, can be read from the collection slips and the bulk tank gauge, so entering it by hand is more reliable to start with.

If the Pico helps at all, it is by watching the bulk tank temperature and alerting you when it is not cooling (a breakdown). Stick a waterproof temperature sensor (**DS18B20 waterproof**, about ¥800) on the outside of the tank so it never touches the milk, and send a line every minute as in #3. How to read a DS18B20 is shown in the Pico SDK examples (`pio/onewire` in pico-examples).

## #6 Scaring off crows

> Board post: find crows with a camera and scare off just those crows

![A large-billed crow (Osaka)](images/h-crow.jpg)

The Raspberry Pi's AI Camera finds them; the Pico aims and sprays water.

```text
AI Camera         finds birds
   ▼
Raspberry Pi      works out the aim
   ▼ USB
Pico              moves servos, sprays
   ▼
pan-tilt mount and valve
```

Build it in two stages.

1. Use **the pan-tilt mount and an LED** to check it points where you aim
2. Fit a nozzle and spray water with a **solenoid valve**

### What to buy

| Item | How many | Rough price |
| --- | --- | --- |
| **Raspberry Pi AI Camera** | 1 | About ¥15,000 |
| **SG90 pan tilt** (mount with two servos) | 1 set | About ¥1,500 |
| Two **MG996R** and a **metal pan tilt bracket** | 1 set | About ¥3,500 |
| **Solenoid valve 12V normally closed 1/2** | 1 | About ¥1,500 |
| **MOSFET module 3.3V** (such as D4184) | 1 | About ¥800 |
| **Diode 1N4007** | 1 | About ¥300 for several |
| **AC adapter 12V 2A** (for the valve) | 1 | About ¥1,200 |
| **AC adapter 5V 3A** and **DC jack adapter** (for the servos) | 1 set | About ¥1,500 |
| Hose joint, thin tube and nozzle | 1 set | About ¥1,500 |

- The SG90 is light, so it is for the first stage with the LED. For the second stage, which carries a nozzle and tube, use the stronger MG996R
- "Normally closed" means the valve stays shut when no power flows. Water does not keep running during a power cut

![A servo motor (SG90)](images/h-servo.jpg)

### Wiring

| Pico | Connect to |
| --- | --- |
| GP16 (pin 21) | Signal of the servo that turns sideways (orange) |
| GP17 (pin 22) | Signal of the servo that turns up and down (orange) |
| GP18 (pin 24) | Signal of the MOSFET module (SIG or IN) |
| GND (pin 23) | − of the 5 V servo supply, GND of the MOSFET module |

- Connect the servos' red (+) and brown (−) to the 5 V 3 A adapter. Taking power from the Pico's 3V3 or VBUS stops the Pico. **Join the GND to the Pico's GND** so they share it
- Wire the valve as 12 V + → valve → MOSFET module output. Across the valve's two wires, connect a 1N4007 diode with its banded end towards + (it protects the Pico from the voltage spike when the valve switches off)
- For the first stage, connect an LED and a 330 Ω resistor to GP18 instead of the valve (Appendix G)

Push the parts into the breadboard as follows. The pins you use (21 to 24) are the four at the left end of the bottom row.

1. Use the bottom + / − rows only for the servos' 5 V (do not connect the Pico's 3V3). Fix male-male jumper wires in the screw terminals of the 5 V adapter's DC jack adapter, and push + into the bottom + row and − into the bottom − row
2. Connect the column of the Pico's pin 23 (GND) to the bottom − row with a wire (so they share GND)
3. Push three male-male jumper wires into each servo's connector (female) to extend it. Push orange into the columns of pin 21 (GP16) and pin 22 (GP17), red into the bottom + row, and brown into the bottom − row
4. Push the female ends of male-female jumper wires onto the MOSFET module's signal (SIG or IN) and GND (if they are screw terminals, fix the male ends instead). Push the signal into the column of pin 24 (GP18), and GND into the bottom − row. Fix the valve and the 12 V wires in the module's output screw terminals

### The Pico program

```cpp run
#include <cstdio>
#include "pico/stdlib.h"
#include "hardware/clocks.h"
#include "hardware/pwm.h"

// Aim the pan-tilt mount and spray water, following commands sent over USB from the Raspberry Pi
//   aim pan tilt  … servo angles (0–180; 90 is straight ahead)
//   spray ms      … open the valve (1 second at most)
constexpr uint PAN = 16, TILT = 17, VALVE = 18;

void servo_init(uint pin) {
    gpio_set_function(pin, GPIO_FUNC_PWM);
    uint slice = pwm_gpio_to_slice_num(pin);
    pwm_set_clkdiv(slice, clock_get_hz(clk_sys) / 1000000.0f);   // 1 count = 1 microsecond
    pwm_set_wrap(slice, 19999);                                   // every 20 ms (50 Hz)
    pwm_set_enabled(slice, true);
}

void servo_deg(uint pin, int deg) {
    if (deg < 0) deg = 0;
    if (deg > 180) deg = 180;
    pwm_set_gpio_level(pin, 500 + deg * 2000 / 180);              // 0.5–2.5 ms pulse
}

int main() {
    stdio_init_all();
    servo_init(PAN);
    servo_init(TILT);
    servo_deg(PAN, 90);
    servo_deg(TILT, 90);
    gpio_init(VALVE);
    gpio_set_dir(VALVE, GPIO_OUT);
    gpio_put(VALVE, 0);

    char line[32];
    int len = 0;
    while (true) {
        int c = getchar_timeout_us(100 * 1000);      // read one character (wait up to 0.1 s)
        if (c == PICO_ERROR_TIMEOUT) continue;
        if (c != '\n' && c != '\r') {
            if (len < (int)sizeof line - 1) line[len++] = (char)c;
            continue;
        }
        line[len] = '\0';                            // a whole line has arrived
        len = 0;
        int a = 0, b = 0;
        if (sscanf(line, "aim %d %d", &a, &b) == 2) {
            servo_deg(PAN, a);
            servo_deg(TILT, b);
            printf("ok aim %d %d\n", a, b);
        } else if (sscanf(line, "spray %d", &a) == 1) {
            if (a < 0) a = 0;
            if (a > 1000) a = 1000;
            gpio_put(VALVE, 1);
            sleep_ms(a);
            gpio_put(VALVE, 0);
            printf("ok spray %d\n", a);
        }
    }
}
```

After writing it to the Pico, type `aim 60 90` or `spray 300` in the Serial Monitor to check the movement.
If a servo buzzes at the ends of its travel, use a narrower range than 0–180.

### The Raspberry Pi program

Add the function below to the same official example as #3, `imx500_object_detection_demo.py`. Call `chase(last_results, get_labels())` after the list of detections is made.
Connect the Pico to the Raspberry Pi by USB (it appears as `/dev/ttyACM0`).

```python
# Add to the official example (Raspberry Pi). When a bird is found, send aim and spray commands to the Pico
import random
import time
from pathlib import Path

import serial                        # sudo apt install python3-serial

pico = serial.Serial("/dev/ttyACM0", 115200, timeout=1)
W, H = 640, 480                      # image size (as set in the example)
FOV_H, FOV_V = 66, 52                # AI Camera field of view (horizontal, vertical, degrees)
LOG = Path.home() / "barn-data"
last_shot = 0


def near(cow, cx, cy):
    x, y, w, h = cow.box
    return x - w / 2 < cx < x + w * 1.5 and y - h / 2 < cy < y + h * 1.5


def chase(detections, labels):
    global last_shot
    names = [labels[int(d.category)] for d in detections]
    birds = [d for d, n in zip(detections, names) if n == "bird"]
    cows = [d for d, n in zip(detections, names) if n == "cow"]
    if not birds or time.time() - last_shot < 5:     # at most once every 5 seconds
        return
    x, y, w, h = birds[0].box
    cx, cy = x + w / 2, y + h / 2
    if any(near(c, cx, cy) for c in cows):            # do not aim at birds next to cows
        return
    pan = 90 - (cx / W - 0.5) * FOV_H                 # if it moves the wrong way, swap - and +
    tilt = 90 + (cy / H - 0.5) * FOV_V
    pico.write(f"aim {pan:.0f} {tilt:.0f}\n".encode())
    time.sleep(0.5)                                   # wait for it to turn
    pico.write(f"spray {random.choice([200, 400, 700])}\n".encode())   # vary the length so they get used to it less
    last_shot = time.time()
    LOG.mkdir(exist_ok=True)
    with open(LOG / f"crow-{time.strftime('%Y-%m-%d')}.csv", "a") as f:
        f.write(f"{time.strftime('%H:%M:%S')},{cx:.0f},{cy:.0f}\n")
```

- The times birds were found go into `crow-<date>.csv`, so you can see when crows come most
- The AI Camera's model only recognises "bird". To target only crows, train it with photos of crows taken in the barn
- Mount the camera and nozzle as close together as you can. If they are far apart, the aim drifts

### Things to watch out for

- **Do not spray the cows.** Do not aim at birds next to cows, and keep the water away from the height of the cows' bodies
- **Stop them getting used to it.** Crows get used to anything that keeps repeating. Besides varying the spray length, think about mixing in light or sound at different times of day
- **Do not use lasers.** They can damage the eyes of cows and people
- **Only scare them off.** Catching or harming crows needs a permit under Japan's Wildlife Protection and Hunting Management Act. Just scaring them off needs no permit
- You are using electricity near water, so put the Pico and power supplies in a waterproof case, and keep the socket end where water cannot reach it

## Rough totals

| Build | Rough price |
| --- | --- |
| Shared items (Raspberry Pi set, two Picos, etc.) | ¥30,000–40,000 |
| #3 Barn environment (with CO2) | About ¥10,000 (camera another ¥15,000) |
| #2 Flow meter | About ¥3,000 |
| #1, #2, #4 Tag or collar (each) | About ¥3,000 |
| #4 Mount sensor (each) | About ¥4,000 |
| #6 Scaring off crows | About ¥30,000 (including the AI Camera) |

## Summary

- The Pico measures, moves and sends; the Raspberry Pi does the camera AI and the records. Everything runs inside the barn Wi-Fi
- The Pico sends one "type,number,name=value" line with `send_line()`, and `receiver.py` on the Raspberry Pi saves it to CSV and shows it on a page
- Start with #3 (barn environment), then the flow meter, then the things that go on cows
- Leg, tail and neck tags are the same set of parts; only where they go and the numbers change
- The alerts are not diagnoses but prompts for a person to check. Adjust the numbers as you test in the barn

## Exercises

```quiz
Q: Which do you give the job of looking at camera video with AI: the Pico or the Raspberry Pi?
A: Raspberry Pi | the Raspberry Pi | Pi
E: The Pico has little memory, so it measures, moves and sends.

Q: In this appendix's barn environment program, at what THI or above does it send `alert=heat`?
A: 72
E: Heat stress starts when THI goes above 68–72.

Q: About how many pulses does the YF-S201 give for 1 L of water?
A: 450
E: Get the exact number by filling a bucket with 10 L and counting.

Q: For how many seconds or more must the mount sensor be pressed to count one mount?
A: 2 | 2 seconds | two
E: Shorter presses are just bumps, and very long ones are pushing against a rail, so they are not counted.

Q: Which kind of light do you not use to scare off crows, because it can damage the eyes of cows and people?
A: laser | lasers | a laser
E: Combine water, light and sound, and keep changing them so the crows do not get used to them.
```
