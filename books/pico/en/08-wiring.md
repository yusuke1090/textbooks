# 8. Connecting sensors

> For programs that use I2C, add `hardware_i2c` to `target_link_libraries` in `CMakeLists.txt` before building (Chapter 4). If you choose **I2C** under Features when creating the project, it is included from the start.

## What you need

| Part | Description |
| --- | --- |
| Breadboard | A board you wire just by pushing parts into holes. No soldering needed |
| Jumper wires | Wires that connect breadboard holes to each other, or to a module's pins |
| Pin headers | Attached to the Pico or a sensor board so it can be plugged into a breadboard (soldering is often needed) |
| MPU-6050 module | An acceleration and gyro (angular velocity) sensor. Often on a board called GY-521 |
| BMP280 module | A pressure and temperature sensor. GY-BMP280 and others |

> Sensors are easier to handle if you buy a **module mounted on a board** rather than "the chip alone".
> Check that it works at 3.3 V and supports I2C.

![A breadboard (half size)](images/breadboard.jpg)

## How a breadboard works

Under the holes of a breadboard are metal strips that connect certain holes to each other.

![The connections inside a breadboard](images/en/breadboard.svg)

| Place | How it connects |
| --- | --- |
| a–e in the middle | **Each vertical group of 5 holes** is connected as one. The same goes for f–j |
| The groove in the middle | Above the groove (a–e) and below it (f–j) are **not connected** |
| The + / − rows at the top and bottom | **A whole horizontal row** is connected. Used to distribute power (3.3 V) and GND |

- Plug the Pico in **straddling the groove**. That way its left and right pins do not short together
- Legs of parts plugged into the same vertical column (for example a–e of column 5) are connected without any wire
- If you connect the Pico's 3V3(OUT) to the + row and GND to the − row, it is easy to power sensors

## Types of jumper wire

| Type | Where it is used |
| --- | --- |
| Male–male | Connecting breadboard holes to each other (the most common) |
| Male–female | Connecting the breadboard to a module with pin headers |
| Female–female | Connecting pin headers directly to each other |

Deciding on wire colors reduces mistakes (for example red = 3.3 V, black = GND, blue = SDA, yellow = SCL).

![Male–male jumper wires](images/jumper-wires.jpg)

## Attaching pin headers

A pin header is a part with metal pins lined up in a strip of black or yellow plastic.
Soldering them into the holes along the edges of the Pico (20 on each side) lets you plug it into a breadboard.

- **If you only connect USB and run programs, you do not need them.** They are needed when connecting sensors
- There are also models with pin headers already attached, the "Pico H" and "Pico WH". In that case, skip this section
- The three small holes at the end of the Pico (DEBUG) are not used in this guide. You do not need to attach anything there

![Attaching pin headers](images/en/pin-header.svg)

### What you need

| Tool | Description |
| --- | --- |
| Soldering iron | One with temperature control is easier to use. Around 330–350 °C |
| Iron stand | A stand to rest the hot iron on. One with a sponge for wiping the tip is handy |
| Solder | For electronics, about 0.6–0.8 mm thick |
| Breadboard | Used as a jig to hold the pins straight |
| Wire cutters | Used to cut pin headers to length |

![A soldering iron, iron stand and solder](images/soldering-kit.jpg)

### Steps

1. Make **two strips of 20 pins** each. If you have a 40-pin strip, snap it in the middle or cut it with wire cutters
2. Push the pin headers into the breadboard **with the long side down**. Space the two strips to match the Pico's width, straddling the middle groove
3. Place the Pico on top **with the chip side up**. The short side of the pins sticks out a little through the Pico's holes
4. First solder only **two pins at opposite corners**. Check that the Pico is not tilted; if it is, reheat that pin and straighten it
5. Solder the remaining pins one at a time
   - Touch the iron tip to **both the pin and the metal around the hole (the pad)** and heat for 2–3 seconds
   - Then touch the solder there and let it melt in. Use enough to fill around the hole
   - **Remove the solder first, then remove the iron**
6. When all are done, pull the Pico straight out of the breadboard

### Checking the result

- ○ Shaped like Mount Fuji, and shiny
- × Rounded like a ball, or a gap between the pin and the pad → touch the iron to it and reheat
- × Joined to the next pin by solder (a bridge) → heat it and draw off the extra solder with the iron tip

When finished, connect USB and see whether all three items of the connection check turn green.

> **Caution**
> - Keep USB unplugged while soldering
> - Holding the iron on too long can melt the breadboard's plastic
> - Ventilate so you do not breathe in the fumes. The iron tip is over 300 °C, so rest it on the stand
> - Attach headers to sensor modules in the same way. Here too, the short side goes to the board and the long side toward the breadboard

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
2. Plug the Pico into the breadboard, straddling the groove
3. Run a wire from the Pico's 3V3(OUT) (pin 36) to the + row, and from GND (pin 38) to the − row
4. Plug the sensors into the breadboard one at a time
5. Connect each sensor's VCC to the + row and GND to the − row
6. Connect each sensor's SDA to the Pico's GP4 (pin 6) and SCL to GP5 (pin 7). The second sensor goes to the same GP4 and GP5
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

- On a breadboard, vertical groups of 5 holes and the horizontal + / − rows are connected. Plug the Pico in straddling the groove
- For pin headers, push the long side into the breadboard as a jig and solder the Pico on from above
- I2C connects several sensors side by side on two wires, SDA and SCL
- Power from 3V3(OUT), shared GND, and start with GP4 (SDA) and GP5 (SCL)
- After wiring, check with an I2C scan that the addresses can be seen

## Exercises

```quiz
Q: How many holes in a breadboard column are connected?
A: 5 | five
E: The long + / − rails are connected too.

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
