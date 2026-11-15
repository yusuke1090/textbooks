# 6. How ArduPilot works

## What you will learn in this chapter

- The flight controller and the parts connected to it
- Sensors and the EKF (estimating position and orientation)
- Parameters
- Flight modes (Copter and Rover)
- Arming, pre-arm checks, failsafes and geofences

## The flight controller

![Pixhawk (the original). A typical flight controller used with both ArduPilot and PX4](images/pixhawk.jpg)

- A **flight controller** (FC, the autopilot board) is a small board carrying a microcontroller (an STM32 ARM), sensors and many connectors
- Typical ones

| Product | In a word |
| --- | --- |
| Pixhawk (6C, 6X and others) | Made by Holybro and others following an open design (the Pixhawk standard). The most information available |
| CubePilot (Cube Orange and others) | In a vibration-damped case. Common in industrial and agricultural drones |
| Matek, SpeedyBee and others | Small and cheap. Hobby and small vehicles |

![Cube Orange. Inside the orange case are sensors protected from vibration](images/cubepilot.jpg)

- **AP_DDS**, which connects directly to ROS 2, is used on boards with an **H7** (STM32H7) CPU with plenty of memory (not recommended on F4 and F7)
- Firmware is flashed from a ground station (Mission Planner, QGroundControl). Firmware with chosen features added can be made with ArduPilot's **Custom Firmware Builder** (choose on the web and it builds it for you)

### Connected parts (multicopter example)

![A development quadcopter (Holybro X500). An assembly kit with frame, motors, FC and GPS](images/holybro-x500.jpg)

| Part | Role |
| --- | --- |
| Frame, motors, propellers | The vehicle. The motors are **brushless motors** |
| **ESC** | Controls the motors' rotation as the FC commands |
| **GPS (GNSS) and compass** | Position and direction. Mounted on a mast to reduce magnetic interference. RTK GPS gives cm accuracy |
| Power module | Measures battery voltage and current, and supplies stable power to the FC |
| **LiPo battery** | Lithium polymer battery. Light and gives high current, but can catch fire if mishandled (Chapter 12) |
| **RC transmitter and receiver** | A person flies by hand. Always fit one, even on autonomous vehicles, so you **can take back control at any time** |
| **Telemetry radio** | Talks to the ground station with MAVLink (Chapter 8). Watch which frequencies are allowed (Chapter 12) |
| Companion computer | Jetson, Raspberry Pi. Runs ROS 2 (Chapter 11) |

## Sensors and the EKF

- Sensors inside and outside the FC
  - **IMU** (accelerometer and gyro): measures tilt and rotation thousands of times a second
  - **Barometer**: height
  - **Compass** (magnetometer): the direction of north
  - **GPS**: position on the earth and velocity
  - Also rangefinders (height above the ground), optical flow (sideways movement from a downward camera), and external position (motion capture, visual odometry)
- Every sensor has errors and noise. The **EKF** (extended Kalman filter; ArduPilot uses **EKF3**) combines all the sensors and estimates the most likely "position, velocity and orientation" every cycle
- Before flying you need to wait until the EKF's estimate settles (until GPS has a fix and the spread is small). The ground station shows something like "EKF3 IMU0 is using GPS"

## Parameters

- ArduPilot has **more than 1,000 parameters** (settings): vehicle shape, sensors, flight mode assignments, failsafes, PID (control strength) and more
- You can view, change and save them to a file in the ground station. They can also be read and written from ROS 2 (Chapter 9)
- Names have the form `GROUP_ITEM`

| Parameter | Meaning |
| --- | --- |
| `FRAME_CLASS`, `FRAME_TYPE` | Vehicle shape (quad, X type and so on) |
| `FLTMODE1`–`FLTMODE6` | Flight modes assigned to the transmitter's switch |
| `BATT_LOW_VOLT`, `BATT_FS_LOW_ACT` | The voltage at which the battery counts as low, and what to do then |
| `FENCE_ENABLE`, `FENCE_ALT_MAX`, `FENCE_RADIUS` | Geofence (an invisible fence) |
| `SERIAL2_PROTOCOL`, `SERIAL2_BAUD` | What a serial port (TELEM2 and so on) is used for, and its speed |
| `DDS_ENABLE` | Whether to use ROS 2 (DDS) (Chapter 9) |
| `GUID_TIMEOUT` | Seconds until stopping in GUIDED mode when velocity commands stop arriving (default 3 seconds) |

- When you change settings, record which parameter you set to what. Saving a file per vehicle and managing it with git gives peace of mind

## Flight modes

ArduPilot's behavior is switched with **flight modes**. The numbers are used when changing mode from ROS 2 or MAVLink.

### Copter

| Number | Mode | Behavior |
| --- | --- | --- |
| 0 | STABILIZE | Only keeps the tilt automatically. A person controls height and position |
| 2 | ALT_HOLD | Also holds the height |
| 3 | **AUTO** | Flies a mission made in the ground station (a list of waypoints) automatically |
| 4 | **GUIDED** | Flies where it is told from outside (ground station, companion computer, ROS 2). **Use this when driving it from ROS 2** |
| 5 | LOITER | Stays in place with GPS. Let go of the sticks and it stops |
| 6 | **RTL** | Returns to where it took off (home) and lands |
| 9 | LAND | Lands where it is |
| 16 | POSHOLD | Close to LOITER. The control feel is a little different |
| 21 | SMART_RTL | Goes back the way it came |

### Rover

| Number | Mode | Behavior |
| --- | --- | --- |
| 0 | MANUAL | A person drives with the transmitter |
| 4 | HOLD | Stops |
| 5 | LOITER | Stays in place (for a boat, near that place) |
| 10 | AUTO | Drives a mission |
| 11 | RTL | Returns home |
| 15 | **GUIDED** | Drives by instructions from outside |

- Always put a mode that hands control straight back to a person (STABILIZE, LOITER, MANUAL) and **RTL** on the transmitter's switch

## Arming and pre-arm checks

- **Arming**: putting the motors in a state where they can spin. **Disarming**: stopping them. Once armed, the propellers spin, so people stay away
- Before arming, ArduPilot does its own **pre-arm checks**. If there is a problem, it cannot be armed
  - The sensors (accelerometer, compass) are not calibrated
  - Not enough GPS satellites, or the EKF has not settled
  - Low battery voltage
  - The RC transmitter is not connected
  - Inconsistent parameters
- The cause appears in the ground station's messages as "PreArm: ...". You can turn the checks off (`ARMING_CHECK = 0`), but **never do so on a real vehicle**

## Failsafes and geofences

- **Failsafe**: a mechanism that automatically does something safe when something goes wrong

| If this happens | For example |
| --- | --- |
| The RC signal is lost | RTL or LAND |
| The ground station (telemetry) is lost | RTL, or carry on |
| The battery is low (two stages) | RTL → LAND |
| The EKF is wrong (position unknown) | LAND |
| Commands from the GCS (GUIDED velocity) stop arriving | Stops in place (`GUID_TIMEOUT`) |

- **Geofence**: an invisible fence. When it is about to exceed the maximum height (`FENCE_ALT_MAX`), the distance from home (`FENCE_RADIUS`) or a polygon area, it comes back with RTL or similar. It is an important insurance that keeps the vehicle inside the fence even if a ROS 2 program sends wrong commands

![An underwater robot running ArduSub (BlueROV2). The same ArduPilot runs underwater too](images/bluerov.jpg)

## Exercises

```quiz
Q: What three letters name the extended Kalman filter that combines all sensors to estimate position, velocity and attitude?
A: EKF | EKF3
E: ArduPilot uses EKF3.

Q: Which flight mode do you use to control the vehicle from ROS 2?
A: GUIDED
E: It flies to positions given from outside.

Q: Which flight mode returns to the takeoff point (home) and lands?
A: RTL | Return to Launch
E: Always put it on a transmitter switch.

Q: What is it called when the motors are allowed to spin?
A: arm | arming | armed
E: Stopping is disarming. Pre-arm checks run before arming.

Q: What is the invisible fence that brings the vehicle back if it goes too high or too far?
A: geofence | fence
E: It is insurance in case a ROS 2 program sends a wrong command.
```
