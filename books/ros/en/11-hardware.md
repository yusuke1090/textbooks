# 11. Real hardware: connecting a Jetson or Raspberry Pi

## What you will learn in this chapter

- How to choose a companion computer
- Installing firmware with DDS on the flight controller
- Wiring and parameters for serial (UART) and USB connections
- Running the micro-ROS Agent automatically at startup (systemd)
- The order to test things on the desk

## Choosing a companion computer

![Raspberry Pi 5. Small, cheap and low-power](images/raspberry-pi5.jpg)

| Model | Strengths | OS and ROS 2 |
| --- | --- | --- |
| **Raspberry Pi 5** | Cheap, small, low-power. Lots of information | Ubuntu 24.04 (arm64) + **Jazzy** (`ros-jazzy-ros-base`) |
| **Jetson Orin Nano / NX** | Has a GPU; camera AI (object detection and so on) is fast | JetPack 6 (Ubuntu 22.04) + **Humble**. For Jazzy, use Docker |

![A Jetson Orin NX module. Runs image AI on its GPU](images/jetson-orin.jpg)

- If you run AI on the vehicle, such as telling crops or cows apart with a camera, choose a Jetson; if you only read sensors and send commands, a Raspberry Pi is enough
- When using Humble on a Jetson, read `jazzy` in this textbook's commands as `humble`, and `ros2.jazzy.repos` as `ros2.repos`
- On the vehicle there is no screen, so you log in with `ssh` to work. Develop with SITL on your computer, and bring the finished packages to the vehicle's computer with git (the "GitHub Textbook")

![A Jetson Nano developer kit (older generation). If buying new, get an Orin](images/jetson-nano.jpg)

## Firmware with DDS

- AP_DDS is used on **flight controllers with an H7 CPU** (Pixhawk 6C/6X, Cube Orange and others)
- The firmware normally distributed may not include DDS. With ArduPilot's **Custom Firmware Builder** (custom.ardupilot.org), choose the vehicle type, board and version, tick **DDS** in the feature list, build, and flash it from the ground station
- If you build it yourself, add `--enable-DDS`, as in `./waf configure --board Pixhawk6X --enable-DDS`

## Connecting

### Connecting by serial (UART)

Connect the FC's **TELEM2** (usually SERIAL2) to the companion computer's UART.

| FC (TELEM2) | Raspberry Pi (40-pin header) |
| --- | --- |
| TX | RX (GPIO15, pin 10) |
| RX | TX (GPIO14, pin 8) |
| GND | GND (pin 6 and others) |
| 5V | **Do not connect** (power each separately) |

- **Cross** TX and RX. Both are 3.3 V signals (a 5 V signal will damage the Raspberry Pi)
- The Raspberry Pi 5's UART is `/dev/ttyAMA0`. Enable the UART in `/boot/firmware/config.txt` (`enable_uart=1`) and turn off the serial login (console)
- A Jetson's UART is `/dev/ttyTHS0` or `/dev/ttyTHS1` depending on the model

FC parameters (set in the ground station, then reboot):

| Parameter | Value | Meaning |
| --- | --- | --- |
| `DDS_ENABLE` | 1 | Use DDS |
| `SERIAL2_PROTOCOL` | **45** | Use this port for DDS (XRCE) |
| `SERIAL2_BAUD` | 921 | 921,600 bps (the official example is 115 = 115,200; make both sides the same) |
| `DDS_DOMAIN_ID` | 0 | Make it the same number as `ROS_DOMAIN_ID` |

Run the micro-ROS Agent on the companion computer (build the Chapter 9 workspace on the vehicle's computer too).

```bash
source ~/ardu_ws/install/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial -b 921600 -D /dev/ttyAMA0
```

- Once connected, `/ap/...` appears in `ros2 topic list` in another terminal
- The vehicle's computer does not need to build the ArduPilot firmware itself. `colcon build --packages-up-to micro_ros_agent ardupilot_msgs` builds only what is needed

### Connecting by USB

- Simply plugging the FC's USB into the companion computer also works. An H7 FC has a second port on USB (a second virtual serial port), which can be used for DDS
- In ArduPilot's example (Pixhawk 6X), the second USB port is SERIAL8, so set `SERIAL8_PROTOCOL` to 45 and `SERIAL8_BAUD` to 115, and specify `/dev/serial/by-id/usb-ArduPilot_...-if02`
- Names under `/dev/serial/by-id/` do not change when you replug, so they are safer than numbers like `/dev/ttyACM1`

### Connecting by Ethernet (UDP)

- FCs with Ethernet (Pixhawk 6X and others) can also connect by UDP (the Agent's IP address in `DDS_IP0`–`DDS_IP3`, and 2019 in `DDS_UDP_PORT`)
- The Agent is `ros2 run micro_ros_agent micro_ros_agent udp4 -p 2019`

## Running automatically at startup (systemd)

Make the Agent start automatically when the vehicle is powered on (a Linux systemd service).

`/etc/systemd/system/micro-ros-agent.service`:

```ini
[Unit]
Description=micro-ROS Agent for ArduPilot
After=network-online.target

[Service]
User=ubuntu
Environment=ROS_DOMAIN_ID=0
ExecStart=/bin/bash -c 'source /opt/ros/jazzy/setup.bash && source /home/ubuntu/ardu_ws/install/setup.bash && exec ros2 run micro_ros_agent micro_ros_agent serial -b 921600 -D /dev/ttyAMA0'
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now micro-ros-agent
journalctl -u micro-ros-agent -f        # view the logs
```

- So that `User` can use `/dev/ttyAMA0`, add it to the `dialout` group (`sudo usermod -aG dialout ubuntu`)
- Your own nodes (something like `pilot.py`) can be started by systemd the same way, via a launch file. But **do not design it so the vehicle starts moving just by being powered on**. Design it so arming and takeoff begin only after a person has checked

## The order to test on the desk

![A vehicle with its propellers removed. Always remove the propellers when testing on the desk](images/props-removed.jpg)

1. **Remove the propellers** (this is the most important)
2. Connect the FC and companion computer to power, and check that GPS values arrive with `ros2 topic echo /ap/navsat`
3. Tilt the vehicle by hand and check that the orientation in `/ap/pose/filtered` changes correctly (that it is ENU)
4. Check with `/ap/prearm_check` that it is ready to arm
5. Switch to GUIDED and try only arming and disarming from ROS 2 (without propellers)
6. In the ground station, check the geofence, failsafes and the transmitter's RTL switch
7. In a wide place with no people, first fly manually with the transmitter, then move it briefly from ROS 2
8. Keep the DataFlash logs and a `ros2 bag` every time

- Rovers are the same. At first, test with the wheels off the ground (on a stand)

## Exercises

```quiz
Q: Which STM32 CPU family do flight controllers for AP_DDS use?
A: H7 | STM32H7
E: For example Pixhawk 6C/6X or Cube Orange.

Q: Which ArduPilot web service builds firmware with the features you choose, such as DDS?
A: Custom Firmware Builder
E: Tick DDS in the feature list.

Q: When connecting the FC and companion computer by UART, how are TX and RX wired?
A: crossed | cross | crossover
E: Both use 3.3 V signals. Do not connect 5V.

Q: When testing on the desk, what is the most important thing to remove?
A: propellers | propeller | props
E: Propellers can cut fingers and even break bones.
```
