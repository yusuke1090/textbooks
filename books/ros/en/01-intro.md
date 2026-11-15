# 1. What are ROS 2 and ArduPilot?

## What you will learn in this chapter

- What ROS 2 does
- What ArduPilot does
- What you can do by combining the two
- The environment used in this textbook (Ubuntu 24.04 and ROS 2 Jazzy)

## ROS 2

- **ROS** (Robot Operating System) is a **set of tools and parts** for building robot programs. Despite "OS" in the name, it is not an operating system like Windows or Linux, but a collection of libraries and tools that run on Linux (Ubuntu)
- A robot program is split into small programs (**nodes**), and the nodes work by exchanging messages
  - A camera node, a node that finds obstacles, a node that decides the route, a node that drives the motors...
  - Even if different people make each one, they connect as long as the message formats match
- Its biggest strength is that you can use, as they are, nodes made by researchers and companies around the world (LiDAR drivers, mapping, the Nav2 autonomous navigation, MoveIt for robot arms and so on)
- **ROS 2** is a rebuilt version of ROS 1. It uses **DDS** (a real-time communication standard long used in factories and the military) for communication, and aims for reliability good enough for products, plus support for multiple robots and Windows/macOS. ROS 1 support ended in May 2025, so if you are learning now, learn ROS 2

![TurtleBot3, a small mobile robot for learning ROS](images/turtlebot3.jpg)

### Distributions

A new version of ROS 2 (a **distribution**) comes out every May. They are named after turtles, in alphabetical order. Those released in even-numbered years are **LTS** releases, supported for 5 years.

| Name | Released | Ubuntu | Support |
| --- | --- | --- | --- |
| Humble Hawksbill | May 2022 | 22.04 | Until May 2027 (LTS) |
| **Jazzy Jalisco** | May 2024 | **24.04** | Until May 2029 (LTS) |
| Kilted Kaiju | May 2025 | 24.04 | Until November 2026 |
| Lyrical Luth | May 2026 | 26.04 | Until May 2031 (LTS) |

- This textbook uses **Ubuntu 24.04 + ROS 2 Jazzy**, because ArduPilot's ROS 2 parts support Humble and Jazzy (the newest, Lyrical, is not officially supported yet)
- On a Jetson (JetPack 6 is Ubuntu 22.04) you will use Humble. Read `jazzy` in the commands as `humble` and it is almost the same (Chapter 11)

## ArduPilot

![ArduPilot logos: Plane (airplanes), Copter (multicopters), Rover (cars, boats), Sub (underwater)](images/ardu-logos.jpg)

- **ArduPilot** is **open-source software** (an autopilot) for driving drones, airplanes, cars, boats and underwater robots automatically
- It runs on a **flight controller** (a small single-board computer), reads the sensors (acceleration, angular rate, compass, barometer, GPS), and adjusts the motors hundreds of times a second to keep the vehicle stable
- It started around 2009 as a hobby project using Arduino (ArduPilot Mega, APM), and is now used around the world in agriculture, surveying, logistics and research. Commercial drones often have ArduPilot inside
- Firmware for each kind of vehicle is built from the same single source code

| Firmware | Vehicle |
| --- | --- |
| **ArduCopter** | Multicopters (4–8 propellers), helicopters |
| ArduPlane | Airplanes, airplanes that take off and land vertically (QuadPlane) |
| **ArduRover** | Cars, boats, lawn mowers, tractors |
| ArduSub | Underwater robots |

![An early flight controller (ArduPilot Mega 2.5)](images/apm25.jpg)

- From a **ground control station** (GCS: Mission Planner, QGroundControl) on a computer or tablet on the ground, you can change settings, plan flights (waypoints) and check on the vehicle. The vehicle and the ground station talk using a communication protocol called **MAVLink** (Chapter 8)
- It is often compared with **PX4** (another open-source autopilot). It runs on the same flight controllers and can also be combined with ROS 2. ArduPilot supports more kinds of vehicles and has a strong track record in agriculture and rovers

## Combining the two

![How ArduPilot and ROS 2 connect](images/en/ardupilot-ros2.svg)

- The roles are divided
  - **Flight controller (ArduPilot)**: "**the calculations for flying**", such as keeping the vehicle stable, flying to set places and coming back when the battery runs low. If it stops, the vehicle falls, so it is kept small and reliable
  - **Companion computer** (Jetson, Raspberry Pi, ROS 2): "**the thinking work**", such as finding crops with a camera, avoiding obstacles, making maps and deciding where to go next. It can do heavy calculations
- There are two ways to connect them
  - **AP_DDS** (from ArduPilot 4.5): ArduPilot speaks the ROS 2 language (DDS) directly. The main method in this textbook (Chapter 9)
  - **MAVROS**: a bridge node between MAVLink and ROS. The long-established method
- Examples of what you can do
  - An agricultural rover finds crop rows with a camera and drives straight along them
  - A drone finds poorly growing spots with a camera and spreads fertilizer only there
  - Automatically patrol barns and fields and collect data

![An agricultural drone (DJI Agras T50). Commercial drones work on the same idea inside](images/agras-flight.jpg)

## How this textbook is organized

| Part | Chapters | Contents |
| --- | --- | --- |
| Part 1: ROS 2 | 2–5 | Installing; nodes, topics, services, launch; messages and coordinates |
| Part 2: ArduPilot | 6–8 | How it works, flying inside a computer (SITL), MAVLink |
| Part 3: Connecting | 9–12 | Driving ArduPilot from ROS 2, Gazebo, real hardware (Jetson, Raspberry Pi), safety and law |

- What you need: a computer with **Ubuntu 24.04** (with another OS, a virtual machine or Docker). 16 GB of memory or more; if you use Gazebo, faster graphics help
- Real hardware comes last (Chapter 11). Until then you can try **everything in simulation inside the computer**. You will not break a vehicle and you need no legal paperwork, so get used to things in simulation first
- It is easier if you know Linux commands, ssh and systemd, Python basics (the "Python Textbook"), Docker (the "Docker Textbook") and git (the "GitHub Textbook")

## Exercises

```quiz
Q: In ROS 2, what is a small program that does one job called?
A: node | nodes
E: Nodes work by exchanging messages.

Q: Which three-letter real-time communication standard does ROS 2 use?
A: DDS
E: ROS 1 support ended in May 2025.

Q: What is the name of the ROS 2 LTS release from May 2024 used in this book?
A: Jazzy | Jazzy Jalisco
E: It is paired with Ubuntu 24.04.

Q: What is the ArduPilot firmware for multicopters and helicopters called?
A: ArduCopter | Copter
E: Cars, boats and tractors use ArduRover.

Q: What is the communication protocol between a vehicle and a ground station called?
A: MAVLink
E: Chapter 8 covers it in detail.
```
