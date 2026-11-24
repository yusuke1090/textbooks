# 2. Development tools

These are the tools you use for electronics with the Pico, with a photo of each and what it is for.
Parts (LEDs, resistors, sensors) are listed under "What you need" in each chapter.

**Get these first**

| Tool | What it is for |
| --- | --- |
| USB cable | Connects the Pico to the PC (writing programs, power, `printf`) |
| Breadboard | Connects parts by pushing them in, without soldering |
| Jumper wires | Connect breadboard holes to each other, or to pins |
| Pin headers | Let the Pico plug into a breadboard (a Pico H or WH has them already) |
| Soldering iron and solder | Attach pin headers and wires |
| Wire cutters | Cut wires and component legs |

**Handy to have**

| Tool | What it is for |
| --- | --- |
| Desoldering braid | Removes solder put in the wrong place |
| Wire strippers | Strip the plastic off wire ends |
| Needle-nose pliers | Hold small parts, bend legs |
| Heat-shrink tubing | Covers soldered joints |
| Multimeter | Measures voltage and whether a wire is connected |

## Tools for connecting

### USB cable

![USB cable (left: the micro-USB end for the Pico; right: the USB-A end for the PC)](images/usb-cable.jpg)

- Connects the Pico to the PC to write programs, supply power and see the `printf` output (Chapter 4)
- Use one that **can carry data**. With a charge-only cable, the Pico doesn't show up on the PC
- Match the Pico's port. The official Pico uses micro-USB; some compatible boards use USB-C

### Breadboard

![Breadboard](images/breadboard.jpg)

- A board where you build a circuit just by pushing component legs and wires into the holes. No soldering, so you can rebuild it as often as you like
- Use it as a **test bench**: check it works on the breadboard first, then finish it with soldering
- Metal strips inside connect each column of 5 holes, and each + / − row along the top and bottom (Chapter 7)
- In the Christmas lights in Appendix G, it stays at the foot of the tree with the Pico and resistors on it, as the place the LED wires plug into
- They come in 830 holes (full size) and 400 holes (half size). For the Pico plus parts, use 830

### Jumper wires

![Jumper wires (male-male)](images/jumper-wires.jpg)

- Wires that connect breadboard holes to each other or to a sensor's pins. Each end is a metal pin (male) or a socket (female)
- **Male-male** connects breadboard holes (used most), **male-female** connects the breadboard to a sensor's pins, and **female-female** connects pins to pins
- Push them all the way in. If they are shallow, the connection comes and goes

### Pin headers

![Pin headers](images/pin-header-strip.jpg)

- A row of pins soldered into the holes along the Pico's edges (20 each side) so it can plug into a breadboard (how to fit them is in Chapter 7)
- They often come with the Pico. A "Pico H" or "Pico WH" has them already, so you don't need them

## Tools for soldering

### Soldering iron, stand and solder

![Soldering iron, stand and solder](images/soldering-kit.jpg)

- Melts solder (a thin wire of tin and other metals) to join metal parts (Chapter 7)
- An iron with adjustable temperature is easiest (330–350 °C). Use 0.6–0.8 mm solder made for electronics
- Rest it in the stand. The tip is very hot, so switch it off as soon as you finish

### Desoldering braid

![Desoldering braid](images/desolder-braid.jpg)

- A fine braid of copper wire. Lay it on unwanted solder and heat it with the iron, and it soaks the solder up
- Use it when solder joins two neighbouring pins (a bridge) or when you soldered something in the wrong place

## Tools for working with wire

### Wire cutters

![Wire cutters](images/nipper.jpg)

- Cut wires and the long legs of LEDs and resistors
- Small cutters made for electronics are easiest. Don't cut hard wire or screws with them (the blades chip)

### Wire strippers

![Wire strippers](images/wire-stripper.jpg)

- Strip the plastic (insulation) off the end of a wire. Grip it in the hole that matches the wire size (AWG) and pull
- You can strip wire by gripping it lightly with cutters and pulling, but it is easy to cut the thin strands inside too

### Needle-nose pliers

![Needle-nose pliers](images/pliers.jpg)

- Pliers with a thin tip. Hold small parts, bend component legs and twist wires

### Heat-shrink tubing

![Heat-shrink tubing](images/heat-shrink.jpg)

- Tubing that shrinks when heated. Slide it over a soldered joint and shrink it so the joint can't touch other wires
- Thread it onto the wire **before** soldering. Heat it with a hair dryer or a lighter
- If you have none, wrap the joint in insulating tape

## Tools for measuring

### Multimeter

![Multimeter](images/multimeter.jpg)

- Measures voltage (V), resistance (Ω) and current, and whether a wire is connected (continuity) (Chapter 18)
- Use it to check "what voltage is this battery?", "is this jumper wire broken inside?" and "is this solder joint connected?"
- In continuity mode it beeps when there is a connection

## Summary

- Get these first: a USB cable, a breadboard, jumper wires, pin headers, a soldering iron and solder, and wire cutters
- A breadboard is a bench for building and testing circuits without soldering. Check it works, then finish it with soldering
- Choose male-male, male-female or female-female jumper wires to match what you are connecting
- A multimeter lets you check battery voltage and whether a wire is broken

## Exercises

```quiz
Q: What is the board you push parts into to build a circuit without soldering?
A: breadboard | a breadboard
E: Check it works, then finish it with soldering.

Q: Which jumper wire is used most to connect breadboard holes: male-male, male-female or female-female?
A: male-male | male male
E: Use male-female to connect to a sensor's pins.

Q: What is the row of pins you solder into the Pico's edge holes so it can plug into a breadboard?
A: pin header | pin headers | header
E: A Pico H or Pico WH has them already.

Q: What is the tubing you slide over a soldered joint and heat to shrink?
A: heat-shrink tubing | heat shrink tubing | heat shrink | heat-shrink
E: Thread it onto the wire before soldering. If you have none, use insulating tape.

Q: What tool measures whether a wire is connected (continuity) or a battery's voltage?
A: multimeter | a multimeter | tester
E: In continuity mode it beeps when there is a connection.
```
