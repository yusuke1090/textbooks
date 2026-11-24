# Appendix D. What microcontrollers can do, and recommended links

## Main uses of microcontrollers

| Field | Examples |
| --- | --- |
| Measuring with sensors | Measuring and recording temperature, humidity, air pressure, acceleration, light and soil moisture |
| Moving things | Controlling motors, servos, LEDs, buzzers and relays (switching appliances on and off) |
| Connecting | Sending sensor values over WiFi, Bluetooth or LoRa (IoT) |
| Input devices | Homemade keyboards, game controllers, MIDI devices |
| Monitoring | Watching the movement of animals or people, or the vibration of equipment, and reporting anything unusual |
| Edge AI | Classifying sounds or movements on the spot with a small machine learning model |

### Example: IoT for monitoring cow behavior

Suppose you put a Pico and an accelerometer on a collar to measure a cow's movement. Chapters 8–17 of this guide follow this flow.

![The flow of IoT for monitoring cow behavior](images/en/iot-system.svg)

1. **Measure**: measure neck movement with an accelerometer, and changes in head height with a pressure sensor (Chapters 11 and 12)
2. **Record and classify**: summarize and save the data at regular intervals (Chapter 16), and classify "walking", "eating", "ruminating", "resting" and so on with machine learning (Chapter 17)
3. **Send**: send the results with a WiFi board (Pico W and others) or LoRa
4. **Collect and view**: collect them in the cloud or on a PC, make graphs, and report anything unusual

The order for actually building it is summarized in Chapter 19.

If classification is done on the microcontroller, the data sent changes from "raw acceleration" to "the kind of behavior", saving a lot of data and battery.

## When a microcontroller suits, and when it does not

**Suits**

- You want it to run for a long time on batteries
- You want it to start running as soon as the power comes on
- You want to read sensors precisely at fixed intervals
- You want to make it small and cheap
- You want to make many of the same thing

**Does not suit (a Raspberry Pi 4/5 or a PC suits better)**

- Processing camera video, or large AI models
- Complex displays on a screen
- Storing and totaling large amounts of data

A common setup is "**in the field, a microcontroller measures and sends → the cloud or a PC collects and analyzes**".

## Things worth getting first

These are the parts used to work through the whole guide. Search online shops for "part name + module" to find them.

| Part | Chapters | Note |
| --- | --- | --- |
| Raspberry Pi Pico (or a compatible board) | All | With pin headers (Pico H and others), no soldering is needed |
| Debug Probe | 5, 19 | Lets you stop at a line and investigate. You can develop without it |
| A USB cable that supports data | All | Match the board's connector (micro-B or Type-C) |
| Breadboard | 7–11 | About 400 or 830 holes |
| Jumper wires (male–male) | 7–11 | A set with various colors |
| LEDs and resistors (220 Ω–1 kΩ) | 8, 9 | Often included in beginner electronics kits |
| Tactile switches (push buttons) | 8, 9 | Not needed if the board has a USR button |
| Potentiometer (variable resistor, 10 kΩ) | 9 | For practicing analog input |
| MPU-6050 module (GY-521) | 10, 11, 15, 16 | Accelerometer and gyro sensor |
| BMP280 module | 10, 11 | Pressure and temperature sensor |
| Soldering iron set | 7 | Only if pin headers are not attached |

> Even without parts, you can try a Pico and sensors in the browser on a site called [Wokwi](https://wokwi.com/).

## Recommended links

### Where to start reading?

1. First, work through this guide in order
2. When you are unsure how to use a function, look up its name in the **Pico SDK API documentation** (you can also open it from Documentation in VS Code's Quick Access)
3. Look for examples in **pico-examples**. Official samples are organized by feature: GPIO, I2C, ADC, PWM, interrupts, power saving and more (you can try them as is with New Project From Example in VS Code)
4. For how to use a sensor, look up its model number in the datasheet and on **Random Nerd Tutorials** (many Python and Arduino examples), and rewrite it in C++
5. When you want to know more, read the official PDFs (the C/C++ SDK and the RP2040 datasheet)

### C/C++ and VS Code (look here first)

- [Pico SDK API documentation](https://www.raspberrypi.com/documentation/pico-sdk/)
  — A list and explanation of functions. Search by function name, such as `gpio_put`. The most used
- [pico-examples](https://github.com/raspberrypi/pico-examples) — The official collection of Pico SDK samples
- [Getting started with Raspberry Pi Pico-series (PDF)](https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf)
  — The official introduction. The VS Code extension, how to debug
- [The Raspberry Pi Pico VS Code extension](https://marketplace.visualstudio.com/items?itemName=raspberry-pi.raspberry-pi-pico)
  — The extension's page (Chapters 4 and 5)
- [Raspberry Pi Pico-series C/C++ SDK (PDF)](https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-c-sdk.pdf)
  — The ideas behind the SDK and an overall explanation
- [Pico SDK](https://github.com/raspberrypi/pico-sdk) — The SDK's source
- [arduino-pico](https://github.com/earlephilhower/arduino-pico) — Lets you use the Pico in the Arduino style (not used in this guide)

### Hardware documents

- [Raspberry Pi Pico datasheet (PDF)](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf)
  — The pinout and power specifications (Chapter 9)
- [RP2040 datasheet (PDF)](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf)
  — Detailed specifications of the chip. For looking up details such as the ADC, PWM, PIO and low power
- [Debug Probe](https://www.raspberrypi.com/documentation/microcontrollers/debug-probe.html) — The official debugging tool (Chapter 5)

### Tutorials and projects

- [Random Nerd Tutorials (Raspberry Pi Pico)](https://randomnerdtutorials.com/projects-raspberry-pi-pico/)
  — Wiring and usage for each sensor. Search by model number
- [Wokwi](https://wokwi.com/) — A simulator for trying a Pico and sensors in the browser

### Machine learning (used in Chapter 17)

- [emlearn](https://github.com/emlearn/emlearn)
  — Converts scikit-learn models into C code
- [LiteRT for Microcontrollers (formerly TensorFlow Lite Micro)](https://ai.google.dev/edge/litert/microcontrollers/overview)
  — Runs neural networks on microcontrollers
- [pico-tflmicro](https://github.com/raspberrypi/pico-tflmicro) — The above ported to the Pico (C++)
- [Edge Impulse](https://edgeimpulse.com/) / [documentation](https://docs.edgeimpulse.com/)
  — A service that does everything from data collection to training and exporting to a microcontroller in the browser
- [scikit-learn decision trees](https://scikit-learn.org/stable/modules/tree.html)

### Sensors

- [MPU-6050 (accelerometer and gyro sensor)](https://invensense.tdk.com/products/motion-tracking/6-axis/mpu-6050/)
  — The product page. The register documents are here too

### MicroPython (Appendix E)

- [MicroPython RP2 quick reference](https://docs.micropython.org/en/latest/rp2/quickref.html)
  — How to write pins, I2C, timers and more, on one page
- [Download MicroPython](https://micropython.org/download/RPI_PICO/)
  — The firmware (.uf2). It can also be flashed with a button in Pico Studio

## Summary

- Microcontrollers are good at "measuring, moving and connecting". Leave heavy processing to a PC or the cloud
- Monitoring cow behavior follows the flow "measure → classify → send → collect"
- When in doubt, look at the Pico SDK API documentation and pico-examples
