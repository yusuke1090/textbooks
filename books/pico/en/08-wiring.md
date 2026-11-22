# 10. Connecting sensors

> For programs that use I2C, add `hardware_i2c` to `target_link_libraries` in `CMakeLists.txt` before building (Chapter 5). If you choose **I2C** under Features when creating the project, it is included from the start.

## What you need

| Part | Description |
| --- | --- |
| MPU-6050 module | An acceleration and gyro (angular velocity) sensor. Often on a board called GY-521 |
| BMP280 module | A pressure and temperature sensor. GY-BMP280 and others |

> Sensors are easier to handle if you buy a **module mounted on a board** rather than "the chip alone".
> Check that it works at 3.3 V and supports I2C.

You also use a breadboard and jumper wires (Chapter 7).

## How I2C works

I2C communicates over two wires: **SDA (data)** and **SCL (clock = the signal that keeps timing in step)**.
Its feature is that **several sensors can be connected side by side** on one pair of wires.

Each sensor has a fixed **address** (number), and the Pico chooses whom to talk to by address.
It is like a class register number: when the Pico calls "number 0x68, tell me your value", only that sensor answers.

| Sensor | I2C address |
| --- | --- |
| MPU-6050 | 0x68 (0x69 if the AD0 pin is connected to 3.3 V) |
| BMP280 | 0x76 or 0x77 (changes with the SDO pin) |
| SHT31 | 0x44 or 0x45 (changes with the ADDR pin) |

As long as addresses do not overlap, you can connect any number to the same wires.

> The `0x` in `0x68` means "hexadecimal". In decimal it is 104.

## Wiring diagram

![Wiring diagram for I2C sensors](images/en/i2c-wiring.svg)

| Pico | MPU-6050 | BMP280 |
| --- | --- | --- |
| 3V3(OUT) (pin 36) | VCC | VCC |
| GND (pin 38) | GND | GND |
| GP4 / I2C0 SDA (pin 6) | SDA | SDA |
| GP5 / I2C0 SCL (pin 7) | SCL | SCL |

### Wiring steps

1. **Unplug USB**
2. Plug the Pico into the breadboard, straddling the groove (USB on the right)
3. With jumper wires, connect a free hole in the column of pin 36 (3V3(OUT)) to the bottom + row, and the column of pin 38 (GND) to the bottom − row. Pin 36 is fifth from the right in the bottom row, and pin 38 is third from the right
4. Push a sensor into a free spot to the left of the Pico. Line its pins up **in the same direction as the groove**, so each pin goes into a different vertical column (if they run across the groove, all the pins are connected inside). Put the second sensor on the other side of the groove, and it fits even on a half-size board
5. With jumper wires, connect the sensor's VCC column to the bottom + row, and its GND column to the bottom − row
6. Connect the sensor's SDA column to the column of the Pico's pin 6 (GP4), and its SCL column to the column of pin 7 (GP5). Pins 6 and 7 are sixth and seventh from the right in the top row. The second sensor goes to free holes in the same columns (a and b are free)
7. Compare with the table and **check every wire once more**
8. Plug in USB

- Always take power from **3V3(OUT)**. Connecting to VBUS (5 V) can damage some sensors
- If the BMP280 has a CSB pin, connect it to 3.3 V; connect the SDO pin to GND (0x76) or 3.3 V (0x77) (on many modules this is already set on the board)

### About pull-up resistors

I2C's SDA and SCL need **pull-up resistors** to 3.3 V (around 4.7 kΩ).
Most sensor modules already have them, so if you use modules, no extra ones are needed.

## I2C scan (checking the connection)

After wiring, first check whether the sensors can be seen.

```cpp run
#include <cstdio>
#include "pico/stdlib.h"
#include "hardware/i2c.h"

// return the name of a common sensor from its address
const char* sensor_name(int addr) {
    switch (addr) {
        case 0x68: return "MPU-6050";
        case 0x69: return "MPU-6050 (AD0=1)";
        case 0x76: case 0x77: return "BMP280 / BME280";
        case 0x44: case 0x45: return "SHT31";
        default: return "?";
    }
}

int main() {
    stdio_init_all();
    sleep_ms(1500);
    i2c_init(i2c0, 400 * 1000);
    gpio_set_function(4, GPIO_FUNC_I2C);
    gpio_set_function(5, GPIO_FUNC_I2C);
    gpio_pull_up(4);
    gpio_pull_up(5);

    int found = 0;
    for (int addr = 0x08; addr < 0x78; addr++) {      // skip 0x00-0x07 and 0x78 and up, which are special numbers
        uint8_t dummy;
        if (i2c_read_blocking(i2c0, addr, &dummy, 1, false) >= 0) {
            printf("found: 0x%02X  %s\n", addr, sensor_name(addr));
            found++;
        }
    }
    if (found == 0) printf("No sensors found. Check the wiring\n");
    while (true) sleep_ms(1000);
}
```

If both are connected, you see the following.

```text
found: 0x68  MPU-6050
found: 0x76  BMP280 / BME280
```

If the addresses found are shown, the wiring is correct.

| Code | Meaning |
| --- | --- |
| `i2c_init(i2c0, 400 * 1000)` | Uses number 0 (`i2c0`) of the Pico's two I2C units at 400 kHz |
| `gpio_set_function(4, GPIO_FUNC_I2C)` | Switches GP4 to I2C. GP4 is I2C0's SDA |
| `gpio_pull_up(4)` | Also uses the pull-up resistor inside the Pico (not needed if the module has resistors) |
| `i2c_read_blocking(i2c0, addr, ...)` | Tries reading 1 byte from that address. If there is no reply, a negative number (an error) is returned |
| `switch (addr) { case ...: }` | A way of branching for each value of `addr` |

### Checks when nothing is found

1. Unplug USB and check the wiring again (swapping SDA and SCL is a common mistake)
2. Is 3.3 V reaching the sensor's VCC (some boards have an LED that lights)?
3. Is GND connected to the Pico?
4. Are any pin header solder joints loose?
5. Try a different jumper wire (they can be broken inside)
6. Try slowing communication down (helps with long wires). Change to `i2c_init(i2c0, 100 * 1000)`

## Summary

- I2C connects several sensors side by side on two wires, SDA and SCL
- Power from 3V3(OUT), shared GND, and start with GP4 (SDA) and GP5 (SCL)
- After wiring, check with an I2C scan that the addresses can be seen

## Exercises

```quiz
Q: I2C uses two wires: SDA and what?
A: SCL
E: Many sensors can share the two wires.

Q: From which Pico pin do sensors get power?
A: 3V3(OUT) | 3V3 | 3V3OUT
E: All GNDs are connected together.

Q: After wiring, what do you run to check the sensor addresses appear?
A: I2C scan | scan
E: If nothing is found, check the wiring and power.
```
