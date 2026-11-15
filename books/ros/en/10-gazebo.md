# 10. Simulation with Gazebo

## What is Gazebo?

- **Gazebo** is a 3D robot simulator. It reproduces physics such as gravity, collisions and ground friction, and sensors such as cameras, LiDAR and IMUs, inside the computer
- SITL in Chapter 7 calculated the vehicle's motion with simple equations. Connected to Gazebo, you can test **in a 3D world**, using camera images and LiDAR point clouds too
  - A rover that finds crop rows with a camera and drives along them
  - A drone that avoids obstacles with LiDAR
- Today's Gazebo (formerly called Ignition Gazebo) has a name for each version. The standard pairing for ROS 2 Jazzy is **Gazebo Harmonic** (for ROS 2 Lyrical, Gazebo Jetty)
- The old "Gazebo Classic" (Gazebo 11) reached end of support in January 2025. Steps in old articles often do not work, so be careful

## Installing

Add ArduPilot's Gazebo package (**ardupilot_gz**) to `~/ardu_ws` from Chapter 9 (ArduPilot's official steps).

```bash
sudo apt install ros-jazzy-ros-gz        # the parts connecting ROS 2 and Gazebo Harmonic (Gazebo itself is installed too)
cd ~/ardu_ws
vcs import --input https://raw.githubusercontent.com/ArduPilot/ardupilot_gz/main/ros2_gz.repos --recursive src
export GZ_VERSION=harmonic
source /opt/ros/jazzy/setup.bash
sudo apt update
rosdep update
rosdep install --from-paths src --ignore-src -y
colcon build --packages-up-to ardupilot_gz_bringup
source install/setup.bash
```

- `export GZ_VERSION=harmonic` is needed every time you build, so it is safest to write it in `~/.bashrc`

## Flying

```bash
cd ~/ardu_ws
source install/setup.bash
ros2 launch ardupilot_gz_bringup iris_runway.launch.py
```

- **SITL, Gazebo and RViz** start together, and a quadcopter (Iris) appears on a runway
- In another terminal, connect MAVProxy and fly

```bash
mavproxy.py --console --map --aircraft test --master=:14550
```

```text
mode guided
arm throttle
takeoff 5
```

- The vehicle lifts off in the Gazebo window. `pilot.py` from Chapter 9 also works as it is (the same `/ap/...` topics and services)
- Other examples

| Launch | Contents |
| --- | --- |
| `iris_runway.launch.py` | Quadcopter, runway |
| `iris_maze.launch.py` | Quadcopter, maze (LiDAR practice) |
| `wildthumper_playpen.launch.py` | Six-wheeled rover (Rover) |
| `alti_transition_runway.launch.py` | An airplane that takes off and lands vertically (QuadPlane) |
| `multiagent.launch.py` | Several vehicles at once |

## Viewing it in RViz too

- The RViz started by the launch shows the vehicle's position (`/ap/pose/filtered`), coordinate frames (TF) and sensors
- Data from sensors inside Gazebo (cameras, LiDAR) becomes ROS 2 topics through **ros_gz_bridge** (which connects Gazebo and ROS 2 topics). Use `ros2 topic list` to see which topics exist
- Images can also be viewed with `rqt_image_view` (`ros2 run rqt_image_view rqt_image_view`)

## Your own vehicles and worlds

- A vehicle's shape and how its sensors are mounted are written in **SDF** (Gazebo's XML format). The shortcut is to copy the Iris model in `ardupilot_gz_description` and add a camera or LiDAR
- Worlds (ground, buildings, trees, crop rows) are written in SDF too. You can borrow tree and building models from Gazebo's Fuel (a model-sharing site)
- Fields and barns do not need to look like the real thing. The trick is to **build only what you want to test (whether the row lines are visible, whether there are obstacles)**

## When it is slow

- Gazebo uses the GPU. On laptops and virtual machines it can be very slow
  - Turn off shadows, lower the camera resolution and frame rate
  - Run without a display (headless: just the server, `gz sim -s`)
  - Even if the simulation speed (real-time factor) is below 1.0, the results are correct. But use `/clock` for time (`use_sim_time:=True`)
- Things you can test without Gazebo are faster to test with SITL alone (Chapters 7–9)

## Exercises

```quiz
Q: Which Gazebo release is the standard partner for ROS 2 Jazzy?
A: Harmonic | Gazebo Harmonic
E: ROS 2 Lyrical uses Gazebo Jetty.

Q: What connects Gazebo topics to ROS 2 topics?
A: ros_gz_bridge
E: Camera and LiDAR data in Gazebo become ROS 2 topics.

Q: Which XML format describes a vehicle's shape and sensors in Gazebo?
A: SDF
E: Copying the Iris model and adding a camera or LiDAR is the quickest way.

Q: Which setting makes nodes use simulation time (`/clock`)?
A: use_sim_time | use_sim_time:=True
E: Results stay correct even if the simulation runs slower than real time.
```
