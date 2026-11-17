# Appendix G. Making Christmas lights

Connect ten ordinary LEDs to the Pico and make them blink, light up one by one, fade in and out, and twinkle.
The program is written in MicroPython, copied to the Pico with a command (mpremote), and runs on batteries.

![An LED Christmas tree](images/xmas-tree.jpg)

## What you need

| Item | How many | Notes |
| --- | --- | --- |
| LEDs (5 mm) | 10 | Two each of red, green, yellow, blue and white |
| 330 Ω resistors | 4 | For the red and yellow LEDs |
| 100 Ω resistors | 6 | For the green, blue and white LEDs |
| Breadboard | 1 | 830 holes |
| Jumper wires (male-male) | 11 | Flexible ones, long enough to reach the far LEDs |
| Pin headers | 2 × 20 pins | Often come with the Pico. Soldering is in Chapter 8 |
| USB cable | 1 | One that can carry data. Match the Pico's port (USB-C or micro-USB) |
| Battery box | 1 | 3 × AA, with a switch |
| AA batteries | 3 | Alkaline |

Bought on Amazon Japan, it all comes to about ¥3,000 (November 2026).

![5 mm LEDs](images/leds.jpg)

### Choosing the resistors

| LED colour | Resistor | Bands |
| --- | --- | --- |
| Red, yellow | 330 Ω | orange, orange, brown, gold |
| Green, blue, white | 100 Ω | brown, black, brown, gold |

Red and yellow LEDs light up at a lower voltage, so they get a bigger resistor. That way every colour draws about 4 mA.
All the Pico's GPIO pins together can supply up to 50 mA, so ten LEDs (about 40 mA) can be connected directly.
If in doubt, 330 Ω for all of them is fine too (green, blue and white just get a little dimmer).

![Resistors (the colour bands show the value)](images/resistors.jpg)

## Wiring

![The lights circuit (10 LEDs and a battery)](images/en/xmas-circuit.svg)

- Each of GP0–GP9 gets one resistor and one LED. The short legs of all the LEDs go to GND
- The battery box's red wire (+) goes to **VSYS (pin 39)** and the black wire (−) to GND. VSYS accepts 1.8–5.5 V, so do not use four AA batteries (6 V)

### Laying it out on the breadboard

![Laying it out on the breadboard](images/en/xmas-breadboard.svg)

1. Make sure the USB cable and the battery are disconnected
2. Put the Pico at the right end with the USB port facing right, straddling the centre groove
3. Put in the ten resistors so they straddle the centre groove. From the left, GP0, GP1 … with two empty columns between them
4. Put each LED's long leg (+) in the column below its resistor, and the short leg (−) in the row with the blue line (−)
5. With jumper wires, connect the Pico's GP0–GP9 columns to the columns above the resistors. GP0 is the leftmost LED
6. Connect the Pico's GND (pin 38) column to the blue-line (−) row with a wire
7. With the battery box switched off, put the red wire in the VSYS (pin 39) column and the black wire in the blue-line (−) row

If the battery box wires end in thin stranded wire, tin them with solder first so they stay in.

## Checking the wiring

Connect the USB cable to your PC (leave the battery switched off) and check that each LED lights up in turn. Save this program as test.py.

```python run
from machine import Pin
import time

for n in range(10):
    print("GP{} should be lit".format(n))
    led = Pin(n, Pin.OUT)
    led.on()
    time.sleep(1)
    led.off()

print("done")
```

```bash
mpremote run test.py
```

If an LED does not light up, check which way round it is (long leg on the resistor side) and which column the wire is in.

## The lights program

Save this program as main.py.

```python run
from machine import Pin, PWM
import time
import random

PINS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]   # the GP numbers of the LEDs (in lighting order)

leds = []
for n in PINS:
    p = PWM(Pin(n))
    p.freq(1000)
    leds.append(p)

def light(i, level):
    # set LED number i to a brightness from 0 to 100
    leds[i].duty_u16(level * level * 65535 // 10000)   # squaring makes the change in brightness look natural

def all_light(level):
    for i in range(len(leds)):
        light(i, level)

def blink(times=10):
    # all blink together
    for _ in range(times):
        all_light(100)
        time.sleep(0.4)
        all_light(0)
        time.sleep(0.4)

def chase(rounds=5):
    # light them one by one
    for _ in range(rounds):
        for i in range(len(leds)):
            all_light(0)
            light(i, 100)
            time.sleep(0.1)
    all_light(0)

def fade(times=3):
    # fade in, then fade out
    for _ in range(times):
        for level in range(0, 101, 2):
            all_light(level)
            time.sleep(0.02)
        for level in range(100, -1, -2):
            all_light(level)
            time.sleep(0.02)

def twinkle(seconds=15):
    # twinkle at random
    levels = [0] * len(leds)
    end = time.ticks_add(time.ticks_ms(), seconds * 1000)
    while time.ticks_diff(end, time.ticks_ms()) > 0:
        if random.randint(1, 100) <= 20:                  # about one time in five
            levels[random.randint(0, len(leds) - 1)] = 100
        for i in range(len(leds)):
            levels[i] = levels[i] * 9 // 10              # dim a little each time
            light(i, levels[i])
        time.sleep(0.03)
    all_light(0)

while True:
    blink()
    chase()
    fade()
    twinkle()
```

| Function | How it lights |
| --- | --- |
| `blink()` | All blink together |
| `chase()` | One by one in turn |
| `fade()` | Fade in, then fade out |
| `twinkle()` | Twinkle at random |

- The brightness is set with **PWM** (Chapter 7). Give `duty_u16()` a value from 0 to 65535: 0 is off and 65535 is brightest
- `light()` squares the 0–100 brightness before turning it into the `duty_u16()` value. With a straight proportion, the LEDs seem to jump up suddenly at the dim end
- The `while True:` at the end repeats the four patterns in turn (about 35 seconds per round)

### Changing how it lights

| What to change | Where |
| --- | --- |
| The order of the LEDs | The `PINS` list (`[9, 8, 7, 6, 5, 4, 3, 2, 1, 0]` runs backwards) |
| The speed | The seconds in `time.sleep()` |
| How many times | The number in the brackets, as in `blink(20)` |
| The order of the patterns | The lines inside the final `while True:` |

## Copying it over and running on batteries

```bash
mpremote run main.py           # try it (Ctrl + C to stop)
mpremote cp main.py :main.py   # save it on the Pico
```

1. Check the patterns with `mpremote run main.py`
2. Save it on the Pico with `mpremote cp main.py :main.py`. main.py runs by itself when the power comes on
3. Unplug the USB cable and switch on the battery box

You can do the same with Pico Studio's "▶ 実行" (Run) and "ピコに保存" (Save to Pico) buttons (Appendix E).

> Switch the battery off whenever the USB cable is connected. With both connected, current from USB can flow into the batteries.

Alkaline AA batteries last about 40–50 hours (around 10 days at 4 hours a night).

## Summary

- Connect each LED through its own resistor to GP0–GP9, and bring all the short legs to GND
- Resistors: 330 Ω for red and yellow, 100 Ω for green, blue and white
- Set the brightness with PWM's `duty_u16()` (0–65535)
- Saved as main.py, the lights come on just by switching on the battery
- The battery goes to VSYS (1.8–5.5 V). Switch it off when the USB cable is connected

## Exercises

```quiz
Q: What resistor value, in Ω, goes with a red LED?
A: 330
E: 330 Ω for red and yellow, 100 Ω for green, blue and white.

Q: What is the name of the Pico pin that the battery box's red wire (+) goes to?
A: VSYS
E: It is pin 39. It accepts 1.8–5.5 V.

Q: Is an LED's long leg plus or minus?
A: plus | + | anode | positive
E: The long leg (+) goes on the resistor side and the short leg (−) on the GND side.

Q: What value given to `duty_u16()` makes an LED brightest?
A: 65535
E: 0 is off and 65535 is brightest.

Q: How many volts do three alkaline AA batteries make when connected together?
A: 4.5
E: 1.5 V × 3 = 4.5 V, which is within VSYS's 5.5 V limit.
```
