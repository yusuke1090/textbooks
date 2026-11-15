# 7. SITL: flying inside a computer

## What is SITL?

- **SITL** (software in the loop) runs ArduPilot's firmware **on a computer** instead of a flight controller. A physics simulation inside the computer produces the sensors and the vehicle's motion
- It runs exactly the same program, the same parameters and the same MAVLink as the real vehicle, so you can try ground stations and your own programs (ROS 2 and so on) without fear of breaking anything
- The basic order is: run it in SITL first, and try only what works on the real vehicle

## Installing

```bash
sudo apt install git
cd ~
git clone --recurse-submodules https://github.com/ArduPilot/ardupilot.git
cd ardupilot
Tools/environment_install/install-prereqs-ubuntu.sh -y    # installs the compiler, Python tools, MAVProxy and more
. ~/.profile                                             # reload PATH (or log out and back in once)
```

- The `master` branch is the development version. To try a stable version, switch to a vehicle-and-version branch like `git checkout Copter-4.6` and run `git submodule update --init --recursive`
- When using it with ROS 2 (Chapter 9), ArduPilot is fetched into the ROS 2 workspace, separately from what you install here. This chapter is for getting used to SITL and MAVLink

## Running it

```bash
cd ~/ardupilot
sim_vehicle.py -v ArduCopter --console --map -w
```

- `-v ArduCopter`: a quadcopter. The first time, the build takes a few minutes
- `--console --map`: show MAVProxy's status window and a map window
- `-w`: reset the parameters to defaults (use it only the first time)
- Once started, the terminal becomes **MAVProxy**'s input (the current mode is shown, like `STABILIZE>`)

### Take off, move and land

Type into MAVProxy (wait a little until GPS has a fix and the console shows something like "EKF3 IMU0 is using GPS").

```text
mode guided
arm throttle
takeoff 10
```

- It climbs to 10 m. Watch the height in "Alt" on the console
- In the map window, **right-click where you want to go → "Fly to"** and it flies there
- Return and land

```text
mode rtl
```

- `mode land` lands where it is; `disarm` stops the motors (after landing)

### Commonly used MAVProxy commands

| Command | What it does |
| --- | --- |
| `mode guided` / `mode loiter` / `mode rtl` / `mode land` / `mode auto` | Change mode |
| `arm throttle` / `disarm` | Arm / disarm |
| `takeoff 10` | Take off to 10 m (in GUIDED) |
| `param show FENCE*` | Show parameters starting with `FENCE` |
| `param set FENCE_ENABLE 1` | Change a parameter |
| `wp load mission.txt` / `wp list` | Load / view a mission |
| `status` | The contents of the messages arriving now |
| `output add 127.0.0.1:14560` | Send MAVLink to one more place (for your own program) |

### Flying a mission (AUTO)

- In the map window, right-click → "Mission" → "Draw" to place waypoints
- Send a mission made in the ground station (below) and switch to `mode auto`, and it flies them in order (Copter starts when armed and the throttle is raised a little; in SITL, `rc 3 1500`)

## Connecting a ground station

- MAVProxy in `sim_vehicle.py` also sends MAVLink to **UDP ports 14550 and 14551**
- Start **QGroundControl** (Ubuntu, Windows, Mac, Android, iOS) and it connects automatically on 14550, showing the vehicle on the map
- From **Mission Planner** (Windows), choose "UDP" → 14550 at the top right
- From the ground station too you can change mode, arm, make and send missions, and change parameters. Real-vehicle setup (calibration, flashing firmware) is also done in the ground station

## Rover, and changing the location

```bash
sim_vehicle.py -v Rover --console --map -w
```

![A robot lawn mower. Machines that drive a set area automatically are a strong use for ArduPilot's Rover](images/robot-mower.jpg)

- A Rover drives with `mode guided` → `arm throttle` → "Fly to" on the map (there is no takeoff)
- The simulation's default location is an airfield in Australia. To try it on a Japanese field, give the latitude, longitude, height and heading

```bash
sim_vehicle.py -v ArduCopter --console --map --custom-location=42.92,143.20,40,0    # Tokachi (near Obihiro)
```

- `--speedup 5` runs the simulation 5 times faster (for checking long missions)
- `-I 1` starts a second vehicle with a different number (the ports shift by 10)

## Logs

- ArduPilot records all in-flight data (sensors, estimated position, motor outputs, mode changes, errors) in **DataFlash logs** (`.bin`). In SITL they are saved in `logs/`, on a real vehicle on the SD card
- You can view them as graphs with the web-based **UAV Log Viewer**, MAVProxy's **MAVExplorer**, or Mission Planner
- "Why did it crash?" and "why could it not arm?" can usually be answered by looking at the logs. If there is trouble with a real vehicle, keep the logs first

## Exercises

```quiz
Q: What is running ArduPilot firmware on a PC for simulation called?
A: SITL | software in the loop
E: A physics simulation on the PC creates the sensors and vehicle motion.

Q: What is the name of the script that starts SITL?
A: sim_vehicle.py | sim_vehicle
E: For example `sim_vehicle.py -v ArduCopter --console --map`.

Q: Which UDP port does QGroundControl use to connect to SITL automatically?
A: 14550
E: MAVProxy sends MAVLink to ports 14550 and 14551.

Q: What file extension do ArduPilot flight logs have?
A: .bin | bin
E: They are DataFlash logs, saved to the SD card on real hardware.
```
