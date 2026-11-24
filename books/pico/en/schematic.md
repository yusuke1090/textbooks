# 10. Reading schematics

When you buy a sensor or camera board, the shop page or the datasheet often shows a **schematic** (circuit diagram). A schematic is a map drawn with symbols that shows "which leg of which part is connected to where".

In this chapter, you first learn how to read the symbols and lines, and then read the schematic of a camera board (OV7670) one part at a time. Once you can read schematics, you can check for yourself "what to connect to which pin" and "what voltage it can take".

## Pictures and schematics

Here is the external LED from Chapter 8, drawn as a picture and as a schematic.

![The same LED circuit as a picture and as a schematic](images/en/sch-led.svg)

| | Picture (wiring diagram) | Schematic |
| --- | --- | --- |
| Parts | Look like the real thing | Fixed symbols |
| Layout | Same as the real thing | Different from the real thing |
| Used when | Plugging into a breadboard | Studying a circuit |

A position on the schematic has nothing to do with the position on the board. **All you look at is "what is connected to what".**

## Part symbols

![Common part symbols](images/en/sch-symbols.svg)

Next to each symbol is a **reference** (R1, C3, U2 and so on) and a **value**. The first letter of the reference tells you the kind of part.

| First letter | Part |
| --- | --- |
| R | Resistor |
| C | Capacitor |
| U, IC | IC (chip) |
| D, LED | Diode, LED |
| J, P, CN | Connector |
| SW | Switch |
| Q | Transistor |

The same references are printed in white on the board. To find which part is "C7" on the schematic, look for these letters.

![White letters on a board (R1, C7 and so on), the same as the references on the schematic](images/pcb-silkscreen.jpg)

### Reading values

| Written as | Meaning |
| --- | --- |
| `10` (resistor) | 10 Ω. The Ω is often left out |
| `1K`, `4K7` | 1 kΩ (1,000 Ω), 4.7 kΩ. `4K7` puts the K where the decimal point goes |
| `4.7uF` | 4.7 µF (microfarads). u is written instead of µ |
| `0.1uF` | 0.1 µF = 100 nF |
| `10nF` | 0.01 µF |

A capacitor stores a little electricity and smooths out wobbles in the voltage. Large values (such as 10 µF) are physically large, and small values (such as 0.1 µF) can be smaller than a grain of rice.

![Various capacitors](images/capacitors.jpg)

## How lines connect

![Where lines are connected and where they are not](images/en/sch-wires.svg)

- Lines are wires. Everything joined by a line is at the same voltage
- If there is a **black dot** where lines cross, they are connected
- If they just cross without a dot, they are **not connected** (one passes over the other)
- Where a line splits into a T, it is connected (usually drawn with a dot)

## Connecting by name

Drawing every connection of a large schematic as a line would bury it in lines. So **names** are put at the ends of lines, and **lines with the same name are connected**.

![Connecting by name](images/en/sch-names.svg)

- **Net names**: names written at the end of a line (`SIO_C`, `D0` and so on). If the same name appears somewhere else, it is the same as drawing a line to it
- **Power symbols**: a T with a name such as `3V3` or `2V8`. `3V3` is 3.3 V and `2V8` is 2.8 V (the V goes where the decimal point is)
- **GND symbols**: a downward triangle, or horizontal lines that get shorter. They are all connected, and are 0 V
- **AGND**: the GND for the analog part. It is joined to GND somewhere on the board, so you can treat it as GND when connecting to the Pico

## Reading an IC box

An IC is drawn as a box with legs (pins) sticking out.

![Reading an IC box](images/en/sch-ic.svg)

1. **Reference**: U1. The same as the white letters on the board
2. **Part number**: PAM3101DAB28. Searching for "PAM3101 datasheet" finds the datasheet (manual)
3. **Pin number**: the number outside the box. The number of the real leg
4. **Pin name**: the text inside the box. The job of the leg

The order inside the box is different from the order of the real legs. The pins are arranged to be easy to read, for example inputs on the left and outputs on the right.

Common pin names:

| Name | Job |
| --- | --- |
| VIN, VCC, VDD | Power in |
| GND, VSS | 0 V |
| OUT | Output |
| EN | Runs at 1, stops at 0 |
| RESET | Restart |
| NC | Not connected to anything |

If a name has a line over it, or a `#` or `n` (`RESET#`, `nRESET`), it means **it acts when it is 0**.

## Example: reading a camera board (OV7670)

This is the schematic of an OV7670 camera board (with 2 rows of 9 pins) sold on AliExpress, redrawn to be easier to read. The camera you connect to the Pico in Appendix I is the same kind of board.

Read it in this order:

1. Find where the power comes in (3V3 and GND on the connector)
2. Find the ICs and look up their jobs from the part numbers
3. Follow the power (what voltage goes where)
4. Follow the signal lines by name to the connector

### The power part

![The power part of the camera board](images/en/sch-camera-power.svg)

1. **U1 (PAM3101DAB28)**: an IC (regulator) that lowers 3.3 V to **2.8 V**. The `28` at the end of the part number means 2.8 V. 3V3 goes into VIN (pin 1) and 2V8 comes out of OUT (pin 5). EN (pin 3) is tied to VIN, so it always runs when the power is on
2. **C2, C3, C5**: the input and output capacitors. They smooth out wobbles in the voltage. The line from U1's GND (pin 2) crosses the EN line, but there is no dot, so they are not connected
3. **R1 and C1**: make **AVDD** (the power for the analog part that measures light) from 2V8. The 10 Ω resistor and the capacitor stop small wobbles from getting through. R2, C10 and C11 do the same to make **DOVDD** (the power for the signal pins)
4. **U2 (PAM3101DAB180)**: lowers 2.8 V to **1.8 V** (`180` = 1.80 V) to make **DVDD** (the power for the calculations inside the chip)

In short:

```text
3V3 (connector pin 1)
 └ U1 → 2V8 ┬ R1 → AVDD   2.8 V  measures light
            ├ R2 → DOVDD  2.8 V  signal pins (D0–D7 and so on)
            └ U2 → DVDD   1.8 V  calculations inside the chip
```

### The sensor and the connector

![The sensor (U3) and connector of the camera board](images/en/sch-camera-sensor.svg)

1. **camera**: the pins in 2 rows of 9 (the connector). This is the only place you connect to the Pico. Pin 1 is 3V3 and pin 2 is GND. The other 16 pins just have names at the ends of their lines
2. **Same names**: the same names appear on the U3 (OV7670) side. Connector pin 3 `SIO_C` is connected to U3 pin 3 `SIO_C`. D0–D7 work the same way: connector pin 16 `D0` is U3 pin 9 `D0`
3. **C12–C16 (0.1 µF)**: capacitors placed right next to the power pins (bypass capacitors). They hold down wobbles when the IC suddenly draws current. On the board, they are the tiny parts around the chip

![A real OV7670 (center) and the tiny capacitors around it](images/image-sensor.jpg)

`STROBE` (pin 16) has no matching name on the connector. It is a pin that is not brought out (not used).

### What the schematic tells you

- You only need to supply **3.3 V** from the Pico. The board makes 2.8 V and 1.8 V itself. Connect it to the Pico's 3V3(OUT) (pin 36)
- Signals such as D0–D7 come out at **2.8 V** (DOVDD). The Pico reads about 2 V and above as 1, so it can read them as they are
- A camera on just a thin ribbon cable (FPC) has no power parts like U1 and U2, so you cannot connect it straight to the Pico
- Connect it to the Pico as in the table in Appendix I

## Finding schematics

- Look for a board's schematic on the shop page, or search for "part number schematic"
- Look up an IC's pin jobs by searching for "part number datasheet"
- The Pico's own schematic is at the end of the [Pico datasheet](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf). It is good reading practice

## Summary

- A schematic is a map of "what is connected to what". The layout differs from the real thing
- A dot where lines cross means connected. A crossing without a dot is not connected
- Same names (net names, power symbols) are connected. All GND symbols are connected
- On an IC, the number outside the box is the pin number and the text inside is the pin name. Look up the jobs in the datasheet for the part number
- Read in this order: power in → ICs → power flow → signal names

## Exercises

```quiz
Q: Two lines cross with no black dot. Are they connected (yes or no)?
A: no | not connected
E: A crossing without a dot just passes over.

Q: A resistor's value is written as `4K7`. How many kΩ is it?
A: 4.7
E: The K goes where the decimal point is. 4.7 kΩ = 4,700 Ω.

Q: A power symbol says `2V8`. How many volts is it?
A: 2.8
E: The V goes where the decimal point is.

Q: What kind of part is C3 on a schematic?
A: capacitor | condenser
E: The first letter tells you the kind. R is a resistor and U is an IC.

Q: Two separate lines have the same name `SIO_C`. Are they connected (yes or no)?
A: yes | connected
E: Lines with the same name are the same as being joined by a line.
```
