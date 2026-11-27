# 7. Using the tools

How to use the tools that connect parts to the Pico. You use them from the external LED in Chapter 8 on.

## What you need

| Part | Description |
| --- | --- |
| Breadboard | A board you wire just by pushing parts into holes. No soldering needed |
| Jumper wires | Wires that connect breadboard holes to each other, or to a module's pins |
| Pin headers | Attached to the Pico or a sensor board so it can be plugged into a breadboard (soldering is often needed) |
| Resistor | A part that holds back the flow of electricity. Connected together with an LED |
| Multimeter | Measures voltage, and whether a wire is connected (you can start without one) |

![A breadboard (half size)](images/breadboard.jpg)

## How a breadboard works

Under the holes of a breadboard are metal strips that connect certain holes to each other.

![The connections inside a breadboard](images/en/breadboard.svg)

| Place | How it connects |
| --- | --- |
| a–e in the middle | **Each vertical group of 5 holes** is connected as one. The same goes for f–j |
| The groove in the middle | Above the groove (a–e) and below it (f–j) are **not connected** |
| The + / − rows at the top and bottom | **A whole horizontal row** is connected. Used to distribute power (3.3 V) and GND |

- Plug the Pico in **straddling the groove**. That way its left and right pins do not short together. With USB on the right, the top row goes from pin 20 at the left end to 19, 18 … 1 on the right, and the bottom row from pin 21 at the left end to 22, 23 … 40
- Legs of parts plugged into the same vertical column (for example a–e of column 5) are connected without any wire
- If you connect the Pico's 3V3(OUT) to the + row and GND to the − row, it is easy to power sensors

![Video: How to use a breadboard (LeftyMaker)](https://www.youtube.com/watch?v=W6mixXsn-Vc)

## Using jumper wires

A jumper wire is a wire with a connector on each end. There are two shapes of end.

![Types of jumper wire](images/en/jumper-types.svg)

| End | Shape | What it goes into |
| --- | --- | --- |
| **Male** | A metal pin sticks out of the tip | A breadboard hole, or a female end |
| **Female** | The tip is a square sleeve with a hole inside | A pin, such as on a pin header |

There are three types, one for each combination of ends.

| Type | What it connects |
| --- | --- |
| Male–male | Breadboard holes to each other. The most common (the LED in Chapter 8) |
| Male–female | The breadboard to a module with pins sticking out (the camera in Appendix I) |
| Female–female | Pins directly to each other. Connects the Pico and a sensor without a breadboard |

![Male–male](images/jumper-wires.jpg)

![Male–female](images/jumper-mf.jpg)

![Female–female](images/jumper-ff.jpg)

### Length

| Length | Where it is used |
| --- | --- |
| 10 cm | On the breadboard. Fast signals such as a camera (long wires easily disturb them) |
| 20 cm | Parts a little away from the breadboard (the LEDs in Appendix G) |
| 30 cm or more | Sensors far away. Signals are easily disturbed, so use wires as short as you can |

### When they arrive

They often come as a strip of 40 joined side by side. Peel off as many as you need, one at a time from the edge.

![A strip of 40 joined wires (female–female)](images/jumper-ribbon.jpg)

### Pushing in and pulling out

- Push them **all the way** in. If they are shallow, they connect and disconnect (in Chapter 8, an LED lit after the parts were pushed in again)
- To pull one out, hold **the black part at the end** (the housing), not the wire. Pulling the wire breaks it inside
- When a female end gets loose and slips off easily, replace the wire
- Check whether a wire is broken inside with the multimeter's continuity mode (see "Using a multimeter" below)

Deciding on wire colors reduces mistakes (for example red = 3.3 V, black = GND, blue = SDA, yellow = SCL).

## Reading a resistor's value

A resistor is a part that holds back the flow of electricity. Always connect an LED together with a resistor (without one, the LED or the Pico's pin can be damaged).
For the external LED in Chapter 8, anything from **220 Ω to 1 kΩ** works. If in doubt, use **330 Ω**. The bigger the number, the dimmer the LED. The legs have no direction.

![Resistors (the color bands show the value)](images/resistors.jpg)

The value is not printed as a number. It is shown by **color bands**. A number printed on the bag or kit (a part number) is often not the value.

![Reading a resistor's bands](images/en/resistor-bands.svg)

1. Hold it with the band that sits a little apart (gold on a 4-band resistor, brown on a 5-band one) on the right
2. From the left, read the digit bands (2 on a 4-band resistor, 3 on a 5-band one)
3. The next band is how many zeros to add (brown adds one 0, black adds none)
4. The band at the right end is the tolerance (gold ±5%, brown ±1%). It is not part of the value

| Value | 4 bands | 5 bands |
| --- | --- | --- |
| 100 Ω | brown, black, brown, gold | brown, black, black, black, brown |
| 220 Ω | red, red, brown, gold | red, red, black, black, brown |
| 330 Ω | orange, orange, brown, gold | orange, orange, black, black, brown |
| 1 kΩ | brown, black, red, gold | brown, black, black, brown, brown |
| 4.7 kΩ | yellow, violet, red, gold | yellow, violet, black, brown, brown |
| 10 kΩ | brown, black, orange, gold | brown, black, black, red, brown |

> Brown and red, or orange and red, can be hard to tell apart. If in doubt, measure it with a **multimeter** (see "Using a multimeter" below).

## Soldering basics

Soldering means melting solder (a thin wire of tin and other metals) with the heat of an iron to join metal parts together. Before attaching pin headers, learn how to choose the tools and use them safely.

### Choosing an iron (watts and temperature)

Watts (W) are the iron's **heating power**, not its temperature. The more watts, the faster it heats up, and the less its temperature drops when a thick wire or a large area of metal takes heat away.

| Iron | Suits |
| --- | --- |
| **Temperature-controlled** (about 50–80 W) | The best choice. Set the dial to 330–350 °C (350–370 °C for lead-free solder) |
| Not temperature-controlled (20–30 W) | Cheap. Fine for pin headers. You cannot change the temperature, and some 30 W irons reach about 480 °C. Too hot damages parts and the metal on the board (the pads) |

- Irons of 40 W or more without temperature control are for thick wires and sheet metal. They are too hot for electronics

### Choosing solder (thickness and type)

Use **rosin-core** solder for electronics. The rosin (flux) helps the melted solder wet the metal.

| Thickness | Suits |
| --- | --- |
| **0.6 mm** | Pin headers and small parts. You can feed a little at a time, so it is hard to use too much. **The one to start with** |
| 0.8 mm | Pin headers, LED leads and jumper-wire ends. Faster than 0.6 mm |
| 1.0–1.2 mm | Thick wires and battery-box leads. Too much for Pico pins, and it easily bridges to the next pin |

| Type | Melts at | Iron temperature |
| --- | --- | --- |
| Leaded (Sn60, Sn63 and so on) | About 183–190 °C | 330–350 °C. Melts at a low temperature and is easy for beginners. Wash your hands afterwards |
| Lead-free (tin, silver, copper) | About 217 °C | 350–370 °C. Needs a little more heat and is less shiny |

### How long it takes to heat up

| Iron | From switching on until ready (rough guide) |
| --- | --- |
| Temperature-controlled | 30 seconds to 1 minute |
| Not temperature-controlled | 2–3 minutes |

A surer test than the clock is to touch solder to the tip. **If it melts at once (within a second), it is ready.** If it melts slowly or not at all, wait a little longer.

### How long to heat one joint

| What you do | Time |
| --- | --- |
| Heat both the component lead and the pad with the tip | 2–3 seconds |
| Feed in the solder and let it flow | 1–2 seconds |
| In total | **5 seconds or less** (up to 3 seconds for heat-sensitive parts such as LEDs) |
| From taking the iron away until the solder sets | **2–3 seconds**. Do not move the part or the board meanwhile |
| Until it is cool enough to touch | About 30 seconds |

- If it does not take, do not keep the iron on it. Take it away, let it cool for about 10 seconds and try again
- Moving it before it sets gives a dull joint that cracks easily. If that happens, heat it again and redo it

### Cleaning the tip (sponge and metal wool)

Wipe the dirt that builds up on the tip (black residue and old solder) off with a sponge or metal wool. A dirty tip does not pass heat well, and solder does not take.

**Sponge** (uses water)


1. Before use, wet it and **squeeze it lightly**, so that a little water oozes out when you press it. If it is soaking wet, the tip temperature drops sharply
2. **Wipe the tip across the sponge once, quickly (about 1 second).** Do not press it in or scrub for long
3. If the tip **shines silver**, it is clean. If it is still black, wipe it again
4. Wipe it the same way after every few joints

- Do not use a dry sponge. The heat of the tip burns it
- Do not use a kitchen sponge. It melts and damages the tip. Use the heat-resistant sponge that comes with the iron stand

**Metal wool** (a ball of fine brass or copper wire; no water)

1. **Push the tip gently into the wool and pull it out.** Do this 2–3 times
2. If the tip shines silver, it is clean

- It uses no water, so the tip temperature does not drop. The tip lasts longer than with a sponge
- Every so often, empty the bits of solder that collect in the wool by turning the holder upside down

### Removing extra solder (desoldering braid)

![Desoldering braid (a braid of fine copper wire)](images/desolder-braid.jpg)

Desoldering braid is a tape woven from fine copper wire. Use it when solder joins a pin to the next one (a bridge) or when you have used too much solder.

1. Lay the end of the braid on the solder you want to remove
2. Press the iron tip on top of it (2–3 seconds)
3. The solder melts and soaks into the copper. The part that soaked it up turns silver
4. **Lift the braid and the iron away together.** If you lift only the iron first, the braid gets stuck in the solder
5. The silver end will not soak up any more, so cut it off with nippers and throw it away

- Copper carries heat well, so **do not hold the end of the braid with your fingers**. Hold the case or the reel
- If it does not soak up well, add a little solder first and then soak it up (the rosin in the fresh solder helps)

![Video: cleaning the tip in metal wool and removing solder with braid](videos/en/solder-cleanup.mp4)

### Using it safely

- **Always rest the iron on its stand.** Never put it straight on the desk or the breadboard
- **Hold only the grip.** The metal parts are over 300 °C. If you drop it, step back instead of trying to catch it
- When you have finished, **put a little solder on the tip before switching off** (it keeps the tip from corroding). The iron stays **hot for about 10 minutes** after switching off, so do not touch it or put it away until it cools
- Do not breathe in the smoke (the rosin in the solder melting). Open a window or use a fan to blow it to the side
- **Wash your hands** after using solder that contains lead. Do not eat or drink while you work
- Cut leads can fly off, so wear glasses or safety glasses
- Keep things that burn easily, such as paper and plastic bags, away

![Video: getting the iron ready and putting it away, and how long one joint takes](videos/en/soldering-basics.mp4)

## Attaching pin headers

A pin header is a part with metal pins lined up in a strip of black or yellow plastic.
Soldering them into the holes along the edges of the Pico (20 on each side) lets you plug it into a breadboard.

- **If you only connect USB and run programs, you do not need them.** They are needed when you connect LEDs or sensors on a breadboard (from the external LED in Chapter 8)
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
5. Solder **all** the remaining pins too (40 in total), one at a time. Soldering the pins you do not use as well keeps the Pico steady and lets you use any pin later
   - Touch the iron tip to **both the pin and the metal around the hole (the pad)** and heat for 2–3 seconds
   - Then touch the solder there and let it melt in. Use enough to fill around the hole
   - **Remove the solder first, then remove the iron**
6. When all are done, pull the Pico straight out of the breadboard

![Video: Soldering header pins to a Raspberry Pi Pico (Learn Embedded Systems)](https://www.youtube.com/watch?v=R11QanPDccs)

### Checking the result

- ○ Shaped like Mount Fuji, and shiny
- × Rounded like a ball, or a gap between the pin and the pad → touch the iron to it and reheat
- × Joined to the next pin by solder (a bridge) → heat it and draw off the extra solder with the iron tip
- If you have a multimeter, you can check with its continuity mode (see "Using a multimeter" below)

When finished, connect USB and see whether all three items of the connection check turn green.

> **Caution**
> - Keep USB unplugged while soldering
> - Holding the iron on too long can melt the breadboard's plastic
> - Attach headers to sensor modules in the same way. Here too, the short side goes to the board and the long side toward the breadboard

## Using a multimeter

A multimeter measures voltage, resistance, current and whether a wire is connected (continuity), all in one. Its full name is digital multimeter (DMM); in Japan it is often called a "tester". Values appear as numbers on the display.

![A multimeter (you pick the range)](images/multimeter.jpg)

![A multimeter that picks the range itself](images/multimeter-auto.jpg)

### Names of the parts

![Parts of a multimeter (digital multimeter)](images/en/tester-parts.svg)

- Plug the black probe into **COM** and the red probe into **VΩmA** (some say VΩ). In this book, you never move them from there
- **10A** is for large currents. This book does not use it

### Dial symbols

| Symbol | What it measures | Where this book uses it |
| --- | --- | --- |
| V (with a solid and a dashed line beside it) | DC voltage | Batteries, the Pico's 3.3 V, pin outputs |
| V~ | AC voltage | Not used (household outlets) |
| Ω | Resistance | A resistor's value |
| ·))) | Continuity (beeps when connected) | Broken wires, solder bridges |
| ▷\| | Diode | An LED's direction and color |
| A (with a solid and a dashed line beside it) | DC current | Chapter 18 (how many days on batteries) |

### Choosing the range

On a meter where you pick the range yourself, choose **the smallest range that is bigger than the value you measure**.

| What you measure | Range | Example reading |
| --- | --- | --- |
| The Pico's 3.3 V, a 4.5 V battery | V, 20 | `3.30` |
| A 330 Ω resistor | Ω, 2000 | `328` |
| A 10 kΩ resistor | Ω, 20k | `9.96` |

- If the range is too small, only `1` (or `OL`) appears. Go up one range
- If it is too big, you lose digits and get a rough reading such as `3.3`
- On a meter that picks the range itself (auto-ranging), you only choose the symbol

### Measuring voltage (the Pico's 3.3 V)

1. Plug the black probe into COM and the red probe into VΩmA
2. Turn the dial to DC voltage (V), 20
3. Connect the Pico plugged into the breadboard over USB (the same as in Chapter 8)
4. Push a male–male wire into a free hole in each of the columns of pin 36 (3V3) and pin 38 (GND). The probes are too thick to go into breadboard holes
5. Touch the black probe to the tip of the GND wire, and the red probe to the tip of the 3V3 wire

![Video: Measuring the Pico's 3.3 V, a wire's continuity and a resistor with a multimeter](videos/en/tester-basics.mp4)

![Measuring by touching the probes to part legs and wires from above](images/tester-breadboard.jpg)

| Reading | Meaning |
| --- | --- |
| `3.28`–`3.32` | It worked. The Pico's 3.3 V is there |
| `-3.30` | Red and black are swapped. Nothing breaks, so just swap them |
| `0.00` | A probe is not touching, a wire is in the wrong column, or USB is unplugged |
| `1` (or `OL`) | The range is too small (it is on 2000m or similar) |

- The same way, pin 40 (VBUS) gives USB's 5 V (`4.8`–`5.1`), and the red and black wires of the battery box give the battery voltage (3 × AA: `4.6`–`4.8` when new; replace them below `3.6`)
- If you measure the column of pin 20 (GP15) while Chapter 8's blinking program runs, it shows about `3.2` and `0.00` in turn. You can check that a signal is coming out of the pin

### Checking continuity (beep)

This checks by sound whether two points are electrically connected. Measure **with USB unplugged**.

1. Turn the dial to ·))) (often the same position as ▷|)
2. Touch the tips of the red and black probes together. If it beeps, you are ready
3. Touch one probe to each of the two points you want to check

| What to check | Where to touch | When it is right |
| --- | --- | --- |
| Is a wire broken inside? | The pins at both ends of the wire | Beeps |
| Pin header soldering | The tips of wires pushed into the columns of pins 18 and 38 | Beeps |
| A bridge to the next pin | Two neighboring pins | Does not beep |

- When they are not connected, it does not beep and shows `1` (or `OL`)
- Pins 18 and 38 are both connected to GND inside the Pico. If both are soldered, it beeps. You can check the other GND pins (3, 8, 13, 23, 28, 33) against pin 38 the same way

### Measuring resistance

1. Unplug USB. Take the resistor out of the breadboard so it is on its own (if other parts are connected, they mix into the reading)
2. Turn the dial to Ω, 2000 (for 330 Ω)
3. Touch one probe to each leg of the resistor. Direction does not matter

| Reading | Meaning |
| --- | --- |
| `314`–`346` | 330 Ω (a gold band means ±5%) |
| `1` (or `OL`) | The range is too small, or a probe is not touching a leg |
| A large resistor (10 kΩ or more) reads low | You are pinching both legs with your fingers. Your body's resistance mixes in, so hold only one |

### Checking an LED's direction and color (diode)

1. Unplug USB and take the LED out of the breadboard
2. Turn the dial to ▷|
3. Touch the red probe to the long leg and the black probe to the short leg

| Reading | Meaning |
| --- | --- |
| About `1.6`–`2.2`, and the LED glows faintly | The direction is right (red, yellow, green and so on) |
| About `2.5`–`3.0`, or `1` (OL) | Blue, white and so on. On some meters it does not glow |
| `1` (or `OL`), and no glow | It is the wrong way round. Swap the probes |

Some meters show it in mV, such as `1820`. It also tells you the color of a clear LED, because it glows faintly.

### Measuring current (Chapter 18)

To measure current, break the circuit at one point and put the meter in the gap. You use it to find out how many days something runs on batteries.

1. Turn the dial to DC current (A), 200m. The red probe stays in VΩmA (on a meter with a separate mA socket, move it there)
2. Put it between the battery's + and the Pico's VSYS (red probe on the battery's +, black probe on the VSYS side)

> If you try to measure voltage while in current mode, the meter shorts inside and its fuse blows. After measuring current, put the dial (and the red probe) back right away.

### Using it safely and putting it away

- Do not measure household outlets (AC 100 V). In this book you only measure up to batteries and USB's 5 V
- Move the probes away before turning the dial
- Measure resistance, continuity and diodes with the power off (with current flowing, the reading is wrong)
- Switch it OFF when you finish (left on, it drains its battery)
- When a battery mark appears on the display, replace the meter's battery (readings drift)

### Choosing one

- A digital one for 2,000–3,000 yen is enough
- One with a **continuity buzzer** (almost all have one)
- One that picks the range itself (auto-ranging) is easy: just set the symbol. One where you pick the range is cheaper and teaches you how ranges work

## Summary

- On a breadboard, vertical groups of 5 holes and the horizontal + / − rows are connected. Plug the Pico in straddling the groove
- Jumper wires combine male ends (pins) and female ends (holes). Push them all the way in, and hold the end to pull them out
- Read a resistor's value from its color bands. For an LED, use 220 Ω–1 kΩ (330 Ω if in doubt)
- For pin headers, push the long side into the breadboard as a jig and solder the Pico on from above
- Use a temperature-controlled iron at 330–350 °C. Each joint takes 5 seconds or less. Wipe the tip quickly on a sponge that has been wetted and squeezed
- When you finish, put solder on the tip and switch off. It stays hot for about 10 minutes, so leave it on the stand
- Just pushing pin headers into the holes does not connect them. Solder all 40
- Plug the multimeter's black probe into COM and the red into VΩmA. Use the smallest range bigger than the value. Measure resistance and continuity with the power off

## Exercises

```quiz
Q: How many holes in a breadboard column are connected?
A: 5 | five
E: The long + / − rails are connected too.

Q: Which jumper wire connects the breadboard to a camera module with pins sticking out: male–male, male–female or female–female?
A: male–female | male-female | male female | female-male
E: The male end goes into a breadboard hole, and the female end onto the module's pin.

Q: A 4-band resistor's colors, from the left, are orange, orange, brown, gold. How many Ω is it?
A: 330 | 330Ω | 330 Ω
E: Orange is 3, orange is 3, and brown adds one 0, so 330 Ω. Gold is the tolerance.

Q: Which side of a pin header goes into the breadboard, the long side or the short side?
A: long | the long side | long side | the long one
E: The short side goes through the Pico's holes and is soldered from above.

Q: How many pin header pins do you solder onto the Pico in total?
A: 40 | forty
E: Just pushing them into the holes does not connect them. Soldering the unused pins too keeps the Pico steady.

Q: For one solder joint, within how many seconds in total should the iron be on it?
A: 5 | 5 seconds | five
E: Heat the lead and pad for 2–3 seconds, then feed solder for 1–2 seconds. Heat-sensitive parts such as LEDs get up to 3 seconds.

Q: After wetting the sponge for wiping the tip, what do you do to it?
A: squeeze it | squeeze | squeeze it lightly | wring it out
E: If it is soaking wet, the tip temperature drops sharply. Make it so a little water oozes out when you press it.

Q: You measure the Pico's 3.3 V with a meter where you pick the range. Which V range do you use (200m, 2000m, 20, 200, 600)?
A: 20
E: Use the smallest range bigger than the value. 2000m (2 V) is too small and shows `1`.

Q: What is the multimeter mode called that checks by a beep whether a wire is broken inside?
A: continuity | continuity test | continuity check
E: Touch the probes to the pins at both ends; if it beeps, it is connected. Measure with USB unplugged.
```
