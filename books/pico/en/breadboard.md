# 7. Using the tools (breadboards and soldering)

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

When finished, connect USB and see whether all three items of the connection check turn green.

> **Caution**
> - Keep USB unplugged while soldering
> - Holding the iron on too long can melt the breadboard's plastic
> - Attach headers to sensor modules in the same way. Here too, the short side goes to the board and the long side toward the breadboard

## Summary

- On a breadboard, vertical groups of 5 holes and the horizontal + / − rows are connected. Plug the Pico in straddling the groove
- For pin headers, push the long side into the breadboard as a jig and solder the Pico on from above
- Use a temperature-controlled iron at 330–350 °C. Each joint takes 5 seconds or less. Wipe the tip quickly on a sponge that has been wetted and squeezed
- When you finish, put solder on the tip and switch off. It stays hot for about 10 minutes, so leave it on the stand
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

Q: For one solder joint, within how many seconds in total should the iron be on it?
A: 5 | 5 seconds | five
E: Heat the lead and pad for 2–3 seconds, then feed solder for 1–2 seconds. Heat-sensitive parts such as LEDs get up to 3 seconds.

Q: After wetting the sponge for wiping the tip, what do you do to it?
A: squeeze it | squeeze | squeeze it lightly | wring it out
E: If it is soaking wet, the tip temperature drops sharply. Make it so a little water oozes out when you press it.
```
