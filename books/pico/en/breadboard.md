# 7. Breadboards and pin headers

How to use the tools that connect parts to the Pico. You use them from the external LED in Chapter 8 on.

## What you need

| Part | Description |
| --- | --- |
| Breadboard | A board you wire just by pushing parts into holes. No soldering needed |
| Jumper wires | Wires that connect breadboard holes to each other, or to a module's pins |
| Pin headers | Attached to the Pico or a sensor board so it can be plugged into a breadboard (soldering is often needed) |

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

When finished, connect USB and see whether all three items of the connection check turn green.

> **Caution**
> - Keep USB unplugged while soldering
> - Holding the iron on too long can melt the breadboard's plastic
> - Ventilate so you do not breathe in the fumes. The iron tip is over 300 °C, so rest it on the stand
> - Attach headers to sensor modules in the same way. Here too, the short side goes to the board and the long side toward the breadboard

## Summary

- On a breadboard, vertical groups of 5 holes and the horizontal + / − rows are connected. Plug the Pico in straddling the groove
- For pin headers, push the long side into the breadboard as a jig and solder the Pico on from above
- Just pushing pin headers into the holes does not connect them. Solder all 40

## Exercises

```quiz
Q: How many holes in a breadboard column are connected?
A: 5 | five
E: The long + / − rails are connected too.

Q: Which side of a pin header goes into the breadboard, the long side or the short side?
A: long | the long side | long side | the long one
E: The short side goes through the Pico's holes and is soldered from above.

Q: How many pin header pins do you solder onto the Pico in total?
A: 40 | forty
E: Just pushing them into the holes does not connect them. Soldering the unused pins too keeps the Pico steady.
```
