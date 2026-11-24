# 12. Reading sensors

This assumes you have done the wiring and I2C scan in Chapter 11.

> The programs in this chapter use I2C. Add `hardware_i2c` to `target_link_libraries` in `CMakeLists.txt` before building (Chapter 5).

## What is a register?

Inside a sensor is a row of small memory locations called **registers**, each with a number (an address).
They are like lockers, and which locker holds what is written in the sensor's datasheet (its manual).

- Write to a settings register → changes how the sensor works
- Read a data register → gives the measured value

![Reading and writing registers](images/en/registers.svg)

In C++, you read and write registers by combining `i2c_write_blocking` (send) and `i2c_read_blocking` (read).

```cpp
// write: send the register number and the value in a row
uint8_t buf[2] = {register_number, value};
i2c_write_blocking(i2c0, sensor_address, buf, 2, false);

// read: send the number (true = keep the connection open), then read
uint8_t reg = register_number;
uint8_t data[6];
i2c_write_blocking(i2c0, sensor_address, &reg, 1, true);
i2c_read_blocking(i2c0, sensor_address, data, 6, false);
```

### Turning bytes into numbers

What you read from a sensor is a row of **bytes** (numbers from 0 to 255, `uint8_t`).
Values such as acceleration use 2 bytes to represent one number (−32768 to 32767, `int16_t`).
In C++, you shift the bits (`<<`) and join them.

```cpp
uint8_t hi = 0x40, lo = 0x00;                       // 2 bytes read from the sensor
int16_t v = static_cast<int16_t>((hi << 8) | lo);   // -> 16384
```

| How to write it | Meaning |
| --- | --- |
| `hi << 8` | Shifts `hi` 8 bits (1 byte) to the left. `0x40` → `0x4000` |
| `\|` | Combines bits (OR). `0x4000 \| 0x00` → `0x4000` |
| `static_cast<int16_t>(...)` | Reinterprets a number from 0 to 65535 as signed (−32768 to 32767) |
| High byte first (big-endian) | `(d[0] << 8) \| d[1]`. The MPU-6050 uses this |
| Low byte first (little-endian) | `(d[1] << 8) \| d[0]`. The BMP280's calibration values use this |

## MPU-6050 (accelerometer and gyro)

**Acceleration** is "which way and how strongly it is being pulled", and **angular velocity (gyro)** is "how fast it is turning".
Gravity acts even when it is still, so the accelerometer also tells you "which way is down" (the tilt).

![An MPU-6050 module (GY-521)](images/mpu6050.jpg)

### The sensor's axes

![The directions of the sensor's axes](images/en/mpu-axes.svg)

- The unit is **g** (the strength of gravity = 1 g)
- Placed still on a desk, gravity pulls straight down, so **z ≈ +1.0 g** and x, y ≈ 0
- When tilted, gravity also shows up split into x and y

### Main registers

| Register | Number | Contents |
| --- | --- | --- |
| PWR_MGMT_1 | 0x6B | Writing 0 wakes it from sleep. **It is asleep right after power-on** |
| GYRO_CONFIG | 0x1B | Gyro range (0 = ±250°/s) |
| ACCEL_CONFIG | 0x1C | Accelerometer range (0 = ±2 g) |
| ACCEL_XOUT_H onward | 0x3B–0x48 | Acceleration XYZ, temperature, gyro XYZ (2 bytes each, big-endian) |
| WHO_AM_I | 0x75 | If 0x68 comes back, it is an MPU-6050 |

### Code for reading

The reading part is also used in later chapters, so it is bundled into a **class** (`Mpu6050`) in a separate file called `mpu6050.h`.
It is in the Pico Studio folder; copy it into your project folder to use it.

```bash
cp ~/apps/pico-studio/cpp/include/mpu6050.h ~/apps/project-name/
```

Then just write `#include "mpu6050.h"`. Add `hardware_i2c` to `CMakeLists.txt` (Chapter 5).

```cpp run
#include <cstdio>
#include "pico/stdlib.h"
#include "mpu6050.h"

Mpu6050 mpu(i2c0);                     // an MPU-6050 connected to I2C0

int main() {
    stdio_init_all();
    sleep_ms(1500);
    if (!mpu.begin(4, 5)) {            // SDA=GP4, SCL=GP5. Also wakes it and sets the ranges
        printf("MPU-6050 not found. Check the wiring\n");
    }
    printf("WHO_AM_I: 0x%02x\n", mpu.who_am_i());

    for (int i = 0; i < 20; i++) {
        float acc[3], gyro[3], temp;
        if (mpu.read_all(acc, gyro, temp)) {
            printf("accel[g] x=%+.2f y=%+.2f z=%+.2f  gyro[deg/s] x=%+6.1f y=%+6.1f z=%+6.1f\n",
                   acc[0], acc[1], acc[2], gyro[0], gyro[1], gyro[2]);
        }
        sleep_ms(200);
    }
    while (true) sleep_ms(1000);
}
```

Run it with the sensor lying on the desk and you see something like this (the numbers vary a little).

```text
WHO_AM_I: 0x68
accel[g] x=+0.02 y=-0.01 z=+1.01  gyro[deg/s] x=  -1.2 y=  +0.8 z=  +0.3
accel[g] x=+0.02 y=-0.02 z=+1.00  gyro[deg/s] x=  -1.1 y=  +0.9 z=  +0.2
```

### Inside mpu6050.h

Inside the class, it does the reading and writing from "What is a register?" above. Here are the main parts (the whole file is `~/apps/pico-studio/cpp/include/mpu6050.h`).

```cpp
class Mpu6050 {
public:
    explicit Mpu6050(i2c_inst_t* i2c, uint8_t addr = 0x68) : i2c_(i2c), addr_(addr) {}

    bool begin(uint sda, uint scl, uint baud = 400 * 1000) {
        i2c_init(i2c_, baud);
        gpio_set_function(sda, GPIO_FUNC_I2C);
        gpio_set_function(scl, GPIO_FUNC_I2C);
        gpio_pull_up(sda);
        gpio_pull_up(scl);
        bool ok = write_reg(0x6B, 0x00)      // wake from sleep
               && write_reg(0x1C, 0x00)      // accel ±2g      -> 16384 = 1g
               && write_reg(0x1B, 0x00);     // gyro ±250 deg/s -> 131 = 1 deg/s
        sleep_ms(100);
        return ok;
    }

    bool read_all(float acc[3], float gyro[3], float& temp) {
        uint8_t d[14];
        if (!read_regs(0x3B, d, 14)) {                  // read 14 bytes at once from 0x3B
            for (int i = 0; i < 3; i++) acc[i] = gyro[i] = 0;   // if it cannot read, set 0 and return false
            temp = 0;
            return false;
        }
        for (int i = 0; i < 3; i++) {
            acc[i] = to_i16(d[i * 2], d[i * 2 + 1]) / 16384.0f;
            gyro[i] = to_i16(d[8 + i * 2], d[9 + i * 2]) / 131.0f;
        }
        temp = to_i16(d[6], d[7]) / 340.0f + 36.53f;
        return true;
    }
    // ... (read_accel, who_am_i, write_reg, read_regs, to_i16)
};
```

| Code | Meaning |
| --- | --- |
| `class Mpu6050 { ... };` | Bundles the functions that operate the sensor with the I2C unit and address it uses |
| `Mpu6050 mpu(i2c0);` | Makes a real thing (an object) from the class. Used like `mpu.begin(...)` |
| `bool` | Returns `true` if it read correctly, `false` if not. The C++ SDK does not stop on errors, so check the return value |
| `float& temp` | `&` means "write directly into the caller's variable". Used as a container to return a result |
| `/ 16384.0f` | With the ±2 g setting, 16384 corresponds to 1 g |
| `/ 131.0f` | With the ±250°/s setting, 131 corresponds to 1°/s |

- An angular velocity of a few °/s even when still is the sensor's quirk (offset)
- Tilt and shake the sensor to check that the values change

## BMP280 (pressure and temperature)

The BMP280's raw readings only become correct pressure and temperature after a **compensation calculation**.
The coefficients used for compensation (calibration values) are written into each sensor at the factory.

### Main registers

| Register | Number | Contents |
| --- | --- | --- |
| id | 0xD0 | 0x58 means BMP280 (0x60 means BME280) |
| calib | 0x88–0x9F | Compensation coefficients (24 bytes) |
| ctrl_meas | 0xF4 | Measurement settings |
| config | 0xF5 | Filter and other settings |
| press / temp | 0xF7–0xFC | Raw pressure and temperature (20 bits each) |

### Code for reading

```cpp run
#include <cmath>
#include <cstdio>
#include "pico/stdlib.h"
#include "hardware/i2c.h"

constexpr uint8_t ADDR = 0x76;         // if not found, change to 0x77

// compensation coefficients (T1 and P1 are unsigned, the rest are signed)
uint16_t T1, P1;
int16_t T2, T3, P2, P3, P4, P5, P6, P7, P8, P9;

bool write_reg(uint8_t reg, uint8_t value) {
    uint8_t buf[2] = {reg, value};
    return i2c_write_blocking(i2c0, ADDR, buf, 2, false) == 2;
}

bool read_regs(uint8_t reg, uint8_t* dst, size_t len) {
    if (i2c_write_blocking(i2c0, ADDR, &reg, 1, true) != 1) return false;
    return i2c_read_blocking(i2c0, ADDR, dst, len, false) == static_cast<int>(len);
}

// 2 bytes, low byte first
uint16_t u16le(const uint8_t* p) { return static_cast<uint16_t>(p[0] | (p[1] << 8)); }
int16_t s16le(const uint8_t* p) { return static_cast<int16_t>(u16le(p)); }

void read_calibration() {
    uint8_t c[24];
    read_regs(0x88, c, 24);
    T1 = u16le(c + 0);  T2 = s16le(c + 2);  T3 = s16le(c + 4);
    P1 = u16le(c + 6);  P2 = s16le(c + 8);  P3 = s16le(c + 10);
    P4 = s16le(c + 12); P5 = s16le(c + 14); P6 = s16le(c + 16);
    P7 = s16le(c + 18); P8 = s16le(c + 20); P9 = s16le(c + 22);
}

// read temperature [C] and pressure [Pa] (the formulas from the datasheet)
bool read_bmp(float& temp, float& pa) {
    uint8_t d[6];
    if (!read_regs(0xF7, d, 6)) return false;
    int32_t adc_p = (d[0] << 12) | (d[1] << 4) | (d[2] >> 4);
    int32_t adc_t = (d[3] << 12) | (d[4] << 4) | (d[5] >> 4);

    double v1 = (adc_t / 16384.0 - T1 / 1024.0) * T2;
    double v2 = (adc_t / 131072.0 - T1 / 8192.0) * (adc_t / 131072.0 - T1 / 8192.0) * T3;
    double t_fine = v1 + v2;
    temp = static_cast<float>(t_fine / 5120.0);

    v1 = t_fine / 2.0 - 64000.0;
    v2 = v1 * v1 * P6 / 32768.0 + v1 * P5 * 2.0;
    v2 = v2 / 4.0 + P4 * 65536.0;
    v1 = (P3 * v1 * v1 / 524288.0 + P2 * v1) / 524288.0;
    v1 = (1.0 + v1 / 32768.0) * P1;
    if (v1 == 0) { pa = 0; return true; }
    double p = 1048576.0 - adc_p;
    p = (p - v2 / 4096.0) * 6250.0 / v1;
    v1 = P9 * p * p / 2147483648.0;
    v2 = p * P8 / 32768.0;
    pa = static_cast<float>(p + (v1 + v2 + P7) / 16.0);
    return true;
}

int main() {
    stdio_init_all();
    sleep_ms(1500);
    i2c_init(i2c0, 400 * 1000);
    gpio_set_function(4, GPIO_FUNC_I2C);
    gpio_set_function(5, GPIO_FUNC_I2C);
    gpio_pull_up(4);
    gpio_pull_up(5);

    uint8_t id = 0;
    read_regs(0xD0, &id, 1);
    printf("chip id: 0x%02x\n", id);

    read_calibration();
    write_reg(0xF5, 0x10);             // IIR filter x16 (reduces jitter in the values)
    write_reg(0xF4, 0x57);             // temperature x2, pressure x16 oversampling, continuous measurement
    sleep_ms(100);

    while (true) {
        float temp, pa;
        if (read_bmp(temp, pa)) {
            float alt = 44330.0f * (1.0f - powf(pa / 101325.0f, 1.0f / 5.255f));   // rough altitude calculated from pressure
            printf("temp %.2f C  pressure %.2f hPa  altitude (approx.) %.1f m\n", temp, pa / 100, alt);
        }
        sleep_ms(500);
    }
}
```

When flashed, it shows something like this.

```text
chip id: 0x58
temp 24.31 C  pressure 1008.52 hPa  altitude (approx.) 39.4 m
temp 24.32 C  pressure 1008.51 hPa  altitude (approx.) 39.5 m
```

- The compensation formulas look hard, but they are copied straight from the datasheet. You can use them without understanding them
- These calculations involve large numbers and easily lose precision, so they use `double`. `double` arithmetic is slow on the Pico, but once every 0.5 seconds is no problem. If you need it faster, use the integer-only formulas in the datasheet
- Pressure falls by about **0.12 hPa** for every 1 m higher. Using this, you can tell the sensor has been raised or lowered
- The absolute altitude changes with the weather, so use it to look at **changes** (for example, a cow lowered its head or stood up)

> Hold the sensor in your hand and raise and lower it between the floor and the desk. The altitude should change by about 1 m.

## Taking data at fixed intervals

In machine learning (Chapter 17), it is important to take data at **fixed intervals**, such as "25 times a second".
With `time.sleep(0.02)` alone, the interval drifts by the time the reading takes.

![Two ways to measure at fixed intervals](images/en/sampling.svg)

In C++, decide the next measurement time with `delayed_by_ms` and wait until then with `sleep_until` (B in the figure).

```cpp run
#include <cstdio>
#include "pico/stdlib.h"
#include "mpu6050.h"

constexpr int HZ = 50;                 // 50 times a second
constexpr int INTERVAL_MS = 1000 / HZ; // every 20 ms

Mpu6050 mpu(i2c0);

int main() {
    stdio_init_all();
    sleep_ms(1500);
    mpu.begin(4, 5);

    absolute_time_t next = get_absolute_time();
    for (int n = 0; n < HZ * 3; n++) {             // 3 seconds' worth
        float ax, ay, az;
        bool ok = mpu.read_accel(ax, ay, az);      // true if read successfully
        if (n % 10 == 0) {
            if (ok) printf("%u %.3f %.3f %.3f\n", static_cast<unsigned>(to_ms_since_boot(get_absolute_time())), ax, ay, az);
            else printf("failed to read\n");
        }
        next = delayed_by_ms(next, INTERVAL_MS);   // the next measurement time
        sleep_until(next);                         // wait until that time
    }
    printf("measured %d times in 3 seconds\n", HZ * 3);
    while (true) sleep_ms(1000);
}
```

- `get_absolute_time()` is the time since the Pico started. `to_ms_since_boot` turns it into a number of milliseconds
- `sleep_until` waits after subtracting the time taken by reading and `printf`, so the interval does not drift
- Printing (`printf`) takes time, so it only prints once every 10 times
- In C++, this way of writing keeps up to about 500 Hz. For more accuracy, use a timer interrupt (Chapter 15)

Which sensors to buy is summarized in the next chapter, Chapter 13.

## Summary

- Sensors are operated by reading and writing registers. In C++, send the number with `i2c_write_blocking` and read with `i2c_read_blocking`
- Join 2-byte values with `(hi << 8) | lo` to make an `int16_t`
- MPU-6050: write 0 to 0x6B to wake it, and read 14 bytes from 0x3B. Usable through the class in `mpu6050.h`
- BMP280: read the compensation coefficients and calculate with the datasheet's formulas. It shows changes in height
- For sampling at fixed intervals, use `delayed_by_ms` and `sleep_until`

## Exercises

```quiz
Q: What does this code print?
| uint8_t hi = 0x01, lo = 0x02;
| int16_t v = (hi << 8) | lo;
| printf("%d", v);
A: 258
E: 0x0102 = 256 + 2 = 258. Join two bytes with `(hi << 8) | lo`.

Q: What does this code print?
| uint8_t hi = 0xFF, lo = 0x38;
| int16_t v = (hi << 8) | lo;
| printf("%d", v);
A: -200
E: 0xFF38 is negative as `int16_t` (65336 − 65536 = −200).

Q: Which register do you write 0 to, to wake the MPU-6050 (hex, starting 0x)?
A: 0x6B | 6B
E: Then read 14 bytes from 0x3B.

Q: Which C++ function reads from a sensor over I2C?
A: i2c_read_blocking
E: Send the register number with `i2c_write_blocking`.
```
