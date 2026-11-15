# Appendix A. Command quick reference

## ROS 2

| Command | What it does |
| --- | --- |
| `source /opt/ros/jazzy/setup.bash` | Makes ROS 2 usable |
| `source install/setup.bash` | Makes your workspace usable |
| `ros2 pkg create --build-type ament_python name --dependencies rclpy` | Makes a Python package |
| `colcon build --symlink-install --packages-select name` | Builds one package |
| `colcon build --packages-up-to name` | Builds that package and what it depends on |
| `rosdep install --from-paths src --ignore-src -y` | Installs dependencies with apt |
| `ros2 run package executable --ros-args -p name:=value` | Runs a node with parameters |
| `ros2 launch package file.launch.py arg:=value` | Starts things together |
| `ros2 node list` / `ros2 node info /name` | List nodes / details |
| `ros2 topic list -t` | List topics and types |
| `ros2 topic echo /name` | Print the contents |
| `ros2 topic echo --qos-reliability best_effort /name` | Print a BEST_EFFORT topic |
| `ros2 topic hz /name` / `ros2 topic info -v /name` | Arrival rate / senders, receivers and QoS |
| `ros2 topic pub --once /name type "{...}"` | Send once |
| `ros2 service call /name type "{...}"` | Call a service |
| `ros2 action send_goal /name type "{...}" --feedback` | Send an action goal |
| `ros2 param list` / `get` / `set` / `dump` | Parameters |
| `ros2 interface show type` | Format of a message or service |
| `ros2 bag record -o name /topic...` / `ros2 bag play name` | Record / play back |
| `rqt_graph` / `rviz2` / `ros2 doctor` | Connection diagram / 3D view / environment check |
| `export ROS_DOMAIN_ID=7` | Group number (keeps you from mixing with other robots) |

## ArduPilot (SITL and MAVProxy)

| Command | What it does |
| --- | --- |
| `sim_vehicle.py -v ArduCopter --console --map -w` | Start Copter SITL (resetting parameters) |
| `sim_vehicle.py -v Rover --console --map` | Rover SITL |
| `--custom-location=lat,lon,alt,heading` | Simulation location |
| `mode guided` / `mode loiter` / `mode rtl` / `mode land` | Modes (MAVProxy) |
| `arm throttle` / `disarm` | Arm / disarm |
| `takeoff 10` | Take off to 10 m |
| `param show name*` / `param set name value` | Parameters |
| `output add 127.0.0.1:14560` | Send MAVLink to one more place |

## ArduPilot and ROS 2 (AP_DDS)

| Command | What it does |
| --- | --- |
| `ros2 launch ardupilot_sitl sitl_dds_udp.launch.py ...` | Start SITL, the Agent and MAVProxy (Chapter 9) |
| `ros2 launch ardupilot_gz_bringup iris_runway.launch.py` | Start with Gazebo (Chapter 10) |
| `ros2 run micro_ros_agent micro_ros_agent serial -b 921600 -D /dev/ttyAMA0` | Agent for real hardware (serial) |
| `ros2 run micro_ros_agent micro_ros_agent udp4 -p 2019` | Agent for real hardware (UDP) |
| `ros2 service call /ap/prearm_check std_srvs/srv/Trigger` | Can it arm? |
| `ros2 service call /ap/mode_switch ardupilot_msgs/srv/ModeSwitch "{mode: 4}"` | GUIDED (Copter) |
| `ros2 service call /ap/arm_motors ardupilot_msgs/srv/ArmMotors "{arm: True}"` | Arm |
| `ros2 service call /ap/experimental/takeoff ardupilot_msgs/srv/Takeoff "{alt: 10.5}"` | Take off |
| `ros2 topic echo /ap/geopose/filtered` | Latitude, longitude, altitude |

## Real-hardware parameters (DDS over serial)

| Parameter | Value |
| --- | --- |
| `DDS_ENABLE` | 1 |
| `SERIAL2_PROTOCOL` | 45 (DDS) |
| `SERIAL2_BAUD` | 921 (or 115). Match the Agent's `-b` |
| `DDS_DOMAIN_ID` | Same as `ROS_DOMAIN_ID` |

## Copter mode numbers

| Number | Mode |
| --- | --- |
| 0 | STABILIZE |
| 2 | ALT_HOLD |
| 3 | AUTO |
| 4 | GUIDED |
| 5 | LOITER |
| 6 | RTL |
| 9 | LAND |
| 16 | POSHOLD |
| 21 | SMART_RTL |

Rover: MANUAL 0, HOLD 4, LOITER 5, AUTO 10, RTL 11, GUIDED 15.
