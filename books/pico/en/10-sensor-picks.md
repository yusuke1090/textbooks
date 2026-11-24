# 13. Recommended sensors

> For the SHT31 program, add `hardware_i2c`, and for the soil moisture sensor program, add `hardware_adc`, to `target_link_libraries` in `CMakeLists.txt` before building (Chapter 5).

## To start with

These two are recommended. Both connect over I2C. The wiring is in Chapter 11, and the code is in Chapter 12 as is.

| Sensor | What it measures | Good for |
| --- | --- | --- |
| **MPU-6050 (GY-521)** | Acceleration, tilt, rotation | Measuring movement. Classifying cow behavior (it carries through to machine learning in Chapter 17) |
| **BMP280** | Air pressure, temperature | Changes in height, air temperature |

## For agriculture

These two are also candidates. How to connect them and the code are in the sections after this one.

| Sensor | What it measures | Connection | Good for |
| --- | --- | --- | --- |
| **SHT31** | Temperature, humidity | I2C | Measuring conditions inside a greenhouse |
| **Capacitive soil moisture sensor** | Soil moisture | ADC (Chapter 9) | A guide for watering. The electrodes do not rust easily |

## Things to watch out for when choosing

- **Choose ones that work at 3.3 V.** Take power from the Pico's 3V3(OUT) (Chapter 11)
- **Check whether soldering is needed.** Many modules come with separate pins that need soldering (Chapter 7)
- **When connecting several to the same I2C wires, choose ones whose addresses do not overlap.** You can check addresses with the I2C scan in Chapter 11

> The code for these two has not yet been tested with real sensors. If it does not work, compare it with the documentation of the module you bought.

## Connecting and reading the SHT31

It can share the same I2C wires as the MPU-6050. Wire it with USB unplugged. Push it into the breadboard the same way as in "Wiring steps" in Chapter 11. Pin names differ between modules, so follow the markings on the product you bought.

| Pico | SHT31 |
| --- | --- |
| 3V3(OUT) (pin 36) | VIN (or VCC) |
| GND (pin 38) | GND |
| GP4 / I2C0 SDA (pin 6) | SDA |
| GP5 / I2C0 SCL (pin 7) | SCL |

The I2C address is `0x44` (`0x45` if the ADDR pin is connected to 3.3 V). You can check it with the I2C scan in Chapter 11.

```cpp run
#include <cstdio>
#include "pico/stdlib.h"
#include "hardware/i2c.h"

constexpr uint8_t ADDR = 0x44;

// calculate the check byte (CRC). Datasheet rule: polynomial 0x31, initial value 0xFF
uint8_t crc8(const uint8_t* data, int len) {
    uint8_t crc = 0xFF;
    for (int i = 0; i < len; i++) {
        crc ^= data[i];
        for (int b = 0; b < 8; b++) crc = (crc & 0x80) ? (crc << 1) ^ 0x31 : (crc << 1);
    }
    return crc;
}

int main() {
    stdio_init_all();
    i2c_init(i2c0, 100 * 1000);
    gpio_set_function(4, GPIO_FUNC_I2C);
    gpio_set_function(5, GPIO_FUNC_I2C);
    gpio_pull_up(4);
    gpio_pull_up(5);

    while (true) {
        const uint8_t cmd[2] = {0x24, 0x00};             // tell it to measure once
        i2c_write_blocking(i2c0, ADDR, cmd, 2, false);
        sleep_ms(20);                                     // wait for the measurement to finish
        uint8_t d[6];                                     // temp 2, check 1, humidity 2, check 1
        if (i2c_read_blocking(i2c0, ADDR, d, 6, false) != 6) {
            printf("failed to read\n");
        } else if (crc8(d, 2) != d[2] || crc8(d + 3, 2) != d[5]) {
            printf("check bytes do not match (noise)\n");
        } else {
            float temp = -45 + 175 * ((d[0] << 8) | d[1]) / 65535.0f;
            float hum = 100 * ((d[3] << 8) | d[4]) / 65535.0f;
            printf("temperature: %.1f C  humidity: %.1f %%\n", temp, hum);
        }
        sleep_ms(1000);
    }
}
```

- In a product, always check the check bytes (CRC). With long wires, noise can corrupt the values
- To print `%` with `printf`, write `%%`

## Connecting and reading a soil moisture sensor

Read it with analog input (ADC). The Pico's ADC goes only up to 3.3 V, so always take power from 3V3(OUT). Running it at 5 V raises the output voltage and can damage the Pico.

| Pico | Soil moisture sensor |
| --- | --- |
| 3V3(OUT) (pin 36) | VCC |
| GND (pin 38) | GND |
| GP26 / ADC0 (pin 31) | AOUT |

If the sensor's three wires end in female sockets, push male-male jumper wires into them to extend them, and push the other ends into the breadboard columns of the Pico's pins 36, 38 and 31. How to push in the Pico, and the order of its pins, are the same as in "An external LED" in Chapter 8.

```cpp run
#include <algorithm>
#include <cstdio>
#include "pico/stdlib.h"
#include "hardware/adc.h"

constexpr int DRY = 3100;    // value in air (replace with your own sensor's value)
constexpr int WET = 1250;    // value in water (replace with your own sensor's value)

int main() {
    stdio_init_all();
    adc_init();
    adc_gpio_init(26);
    adc_select_input(0);

    while (true) {
        // read 16 times and average (reduces jitter in the value)
        int sum = 0;
        for (int i = 0; i < 16; i++) sum += adc_read();
        int value = sum / 16;
        float percent = (DRY - value) * 100.0f / (DRY - WET);
        percent = std::clamp(percent, 0.0f, 100.0f);     // keep it between 0 and 100
        printf("value: %d  moisture: %.0f %%\n", value, percent);
        sleep_ms(1000);
    }
}
```

C++'s `adc_read()` gives 0–4095, so `DRY` and `WET` are also values in the 0–4095 range (about a sixteenth of MicroPython's `read_u16()` values).

The values differ for each sensor, so measure them first.

1. Place the sensor in air, flash the program and write the value shown into `DRY`
2. Put the sensor in water, flash and write the value shown into `WET`. Only the part below the line marked on it may go in water
3. Push it into soil and look at the value

This sensor gives smaller values the more moisture there is. The % shown is a rough guide to where it is between dry and wet.

## Reading product descriptions

### When it says "requires an ADC converter"

ADC is short for Analog-to-Digital Converter. It is the part that turns a voltage from a sensor into a number a computer can read.

| Board | ADC | What an analog sensor needs |
| --- | --- | --- |
| Pico | Built in (GP26, GP27, GP28) | Just the sensor |
| Raspberry Pi | None | An external ADC (MCP3008 and others) |

Even if a product description says "the Raspberry Pi requires an ADC converter", that is about the Linux Raspberry Pi. The Pico does not need one.

### When it says "works at 3.3–5.5 V"

Even if it says it also works at 5 V, use it at **3.3 V** with the Pico. If the output voltage goes above 3.3 V, it can damage the Pico's ADC.

### Wire colors

Wire colors can differ between products. Connect according to **the letters printed on the board** (VCC, GND, AOUT), not the colors.

### The same look can hide different insides

Cheap soil moisture sensors are said to come in units that look the same but have different parts on the board. Units whose timer IC is an NE555 may not work at 3.3 V.
When yours arrives, check that the value changes a lot between air and water.
## Summary

- MPU-6050 and BMP280 are recommended as first sensors
- SHT31 for temperature and humidity, a capacitive soil moisture sensor for soil moisture
- Check that every sensor works at 3.3 V, and take power from 3V3(OUT)
- The Pico has a built-in ADC, so an "ADC converter" is not needed

## Exercises

```quiz
Q: Which sensor does the guide recommend for temperature and humidity?
A: SHT31
E: It connects over I2C.

Q: What type of soil moisture sensor does the guide recommend?
A: capacitive
E: Its electrodes do not corrode easily, so it lasts.

Q: What does the Pico have built in, so you do not need to buy one (three letters)?
A: ADC
E: Even if a listing says "needs an ADC converter", you do not need it.

Q: Which first sensor measures air pressure and temperature?
A: BMP280
E: For acceleration and gyro, use the MPU-6050.
```
