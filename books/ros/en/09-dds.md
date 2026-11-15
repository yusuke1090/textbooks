# 9. Driving ArduPilot from ROS 2

## How AP_DDS works

![How ArduPilot and ROS 2 connect](images/en/ardupilot-ros2.svg)

- From ArduPilot 4.5, the flight controller can speak **DDS** (ROS 2's communication) directly (**AP_DDS**)
- To run even on a small microcontroller, it uses **XRCE-DDS** (a lightweight version of DDS). The **micro-ROS Agent**, running on the companion computer, relays between XRCE-DDS and ordinary ROS 2
- Seen from the ROS 2 side, there is a node named `/ap` with a row of topics and services. You can drive the vehicle with ordinary ROS 2 programs without knowing MAVLink
- Coordinates go in and out in the ROS convention (**ENU**) (converted from NED inside ArduPilot)

## Making the workspace

These are ArduPilot's official steps (ArduPilot's `Tools/ros2/README.md`, for Jazzy). Separately from `~/ros2_ws` in Chapter 3, make `~/ardu_ws`.

```bash
mkdir -p ~/ardu_ws/src
cd ~/ardu_ws/src
wget https://raw.githubusercontent.com/ArduPilot/ardupilot/master/Tools/ros2/ros2.jazzy.repos
vcs import --recursive < ros2.jazzy.repos      # fetches ArduPilot, the micro-ROS Agent, ardupilot_msgs and more
```

Install the packages it depends on.

```bash
cd ~/ardu_ws
source /opt/ros/jazzy/setup.bash
sudo apt update
rosdep update
rosdep install --rosdistro ${ROS_DISTRO} --from-paths src --ignore-src --skip-keys microxrcedds_agent -y
```

Install the tool that generates the DDS code (**Micro-XRCE-DDS-Gen**, which runs on Java). For ArduPilot 4.7 and later (master), use `v4.7.0`.

```bash
sudo apt install default-jre
cd ~/ardu_ws
git clone --recurse-submodules --branch v4.7.0 https://github.com/ardupilot/Micro-XRCE-DDS-Gen.git
cd Micro-XRCE-DDS-Gen
./gradlew assemble
echo "export PATH=\$PATH:$PWD/scripts" >> ~/.bashrc
source ~/.bashrc
```

Install what SITL needs, and build.

```bash
cd ~/ardu_ws/src/ardupilot
Tools/environment_install/install-prereqs-ubuntu.sh -y
. ~/.profile
cd ~/ardu_ws
colcon build --packages-up-to ardupilot_sitl
source install/setup.bash
```

- The build takes a while (the first time, sometimes tens of minutes)
- If it fails, see the detailed errors with `colcon build --packages-up-to ardupilot_sitl --event-handlers=console_cohesion+`. The most common cause is that Micro-XRCE-DDS-Gen is not on the PATH (`microxrceddsgen` cannot be found)

## Starting SITL connected to ROS 2

```bash
cd ~/ardu_ws
source install/setup.bash
ros2 launch ardupilot_sitl sitl_dds_udp.launch.py transport:=udp4 synthetic_clock:=True wipe:=False model:=quad speedup:=1 slave:=0 instance:=0 defaults:=$(ros2 pkg prefix ardupilot_sitl)/share/ardupilot_sitl/config/default_params/copter.parm,$(ros2 pkg prefix ardupilot_sitl)/share/ardupilot_sitl/config/default_params/dds_udp.parm sim_address:=127.0.0.1 master:=tcp:127.0.0.1:5760 sitl:=127.0.0.1:5501
```

- It is long, but it is one line. This launch starts three things: the **micro-ROS Agent**, **SITL** (ArduCopter) and **MAVProxy**
- To show MAVProxy's windows too, add `map:=True console:=True` at the end
- Check in another terminal

```bash
source ~/ardu_ws/install/setup.bash
ros2 node list               # /ap is visible
ros2 topic list              # /ap/... topics are listed
ros2 topic echo /ap/geopose/filtered
```

- If you have changed `ROS_DOMAIN_ID`, set ArduPilot's parameter `DDS_DOMAIN_ID` (default 0) to the same number

## ArduPilot's topics and services

### Topics ArduPilot publishes

| Topic | Type | Contents |
| --- | --- | --- |
| `/ap/pose/filtered` | geometry_msgs/msg/PoseStamped | Position from home and orientation (ENU) |
| `/ap/twist/filtered` | geometry_msgs/msg/TwistStamped | Velocity (ENU) |
| `/ap/geopose/filtered` | geographic_msgs/msg/GeoPoseStamped | Latitude, longitude, altitude and orientation |
| `/ap/navsat` | sensor_msgs/msg/NavSatFix | GPS |
| `/ap/battery` | sensor_msgs/msg/BatteryState | Battery |
| `/ap/imu/experimental/data` | sensor_msgs/msg/Imu | Acceleration and angular velocity |
| `/ap/clock`, `/ap/time` | Time | ArduPilot's time |
| `/ap/tf_static` | tf2_msgs/msg/TFMessage | Fixed coordinate transforms |
| `/ap/status` | ardupilot_msgs/msg/Status | Whether armed, mode and so on |

- Topics such as position, GPS and battery are sent **BEST_EFFORT**. Use `qos_profile_sensor_data` when receiving them (Chapter 5)

### Topics ArduPilot subscribes to

| Topic | Type | Contents |
| --- | --- | --- |
| `/ap/cmd_vel` | geometry_msgs/msg/TwistStamped | Velocity commands. If `header.frame_id` is `map`, ENU fixed to the ground (east, north, up); if `base_link`, the vehicle's heading |
| `/ap/cmd_gps_pose` | ardupilot_msgs/msg/GlobalPosition | A destination by latitude and longitude (in GUIDED) |
| `/ap/joy` | sensor_msgs/msg/Joy | Control in place of the transmitter (RC) |
| `/ap/tf` | tf2_msgs/msg/TFMessage | Own position fed in from outside (visual odometry and so on) |

### Services

| Service | Type | Contents |
| --- | --- | --- |
| `/ap/arm_motors` | ardupilot_msgs/srv/ArmMotors | Request: `arm` (true/false) → answer: `result` |
| `/ap/mode_switch` | ardupilot_msgs/srv/ModeSwitch | Request: `mode` (number, Chapter 6) → answer: `status`, `curr_mode` |
| `/ap/experimental/takeoff` | ardupilot_msgs/srv/Takeoff | Request: `alt` (m) → answer: `status` |
| `/ap/prearm_check` | std_srvs/srv/Trigger | Whether it is ready to arm |
| `/ap/get_parameters`, `/ap/set_parameters` | rcl_interfaces | Read and change parameters |

Try them from the command line (Copter's GUIDED is 4).

```bash
ros2 service call /ap/prearm_check std_srvs/srv/Trigger
ros2 service call /ap/mode_switch ardupilot_msgs/srv/ModeSwitch "{mode: 4}"
ros2 service call /ap/arm_motors ardupilot_msgs/srv/ArmMotors "{arm: True}"
ros2 service call /ap/experimental/takeoff ardupilot_msgs/srv/Takeoff "{alt: 10.5}"
```

- If it does not take off for a while after arming, it disarms automatically for safety. Call the takeoff service right after arming
- Check that the vehicle rises in MAVProxy's windows or the ground station

## Flying with a Python node

Make your own package as in Chapter 3 (inside `~/ros2_ws` or `~/ardu_ws`), and add `ardupilot_msgs` and `geometry_msgs` to `package.xml`. Since it uses `ardupilot_msgs`, build and run in a terminal where `~/ardu_ws/install/setup.bash` has been sourced.

`pilot.py`:

```python
import time

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from ardupilot_msgs.srv import ArmMotors, ModeSwitch, Takeoff
from geometry_msgs.msg import PoseStamped, TwistStamped

GUIDED = 4   # Copter mode numbers (Chapter 6)
LAND = 9


class Pilot(Node):
    def __init__(self):
        super().__init__('pilot')
        self.arm_cli = self.create_client(ArmMotors, '/ap/arm_motors')
        self.mode_cli = self.create_client(ModeSwitch, '/ap/mode_switch')
        self.takeoff_cli = self.create_client(Takeoff, '/ap/experimental/takeoff')
        self.vel_pub = self.create_publisher(TwistStamped, '/ap/cmd_vel', qos_profile_sensor_data)
        self.create_subscription(PoseStamped, '/ap/pose/filtered', self.on_pose, qos_profile_sensor_data)
        self.z = None   # height above home (ENU z; up is +)

    def on_pose(self, msg):
        self.z = msg.pose.position.z

    def call(self, cli, req):
        """Call a service and wait until the answer comes"""
        while not cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(f'Waiting for {cli.srv_name}...')
        future = cli.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        return future.result()

    def set_mode(self, mode):
        return self.call(self.mode_cli, ModeSwitch.Request(mode=mode)).status

    def arm(self):
        return self.call(self.arm_cli, ArmMotors.Request(arm=True)).result

    def takeoff(self, alt):
        return self.call(self.takeoff_cli, Takeoff.Request(alt=alt)).status

    def send_velocity(self, east, north, up):
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'map'          # ENU fixed to the ground (x east, y north, z up)
        msg.twist.linear.x = east
        msg.twist.linear.y = north
        msg.twist.linear.z = up
        self.vel_pub.publish(msg)

    def wait(self, seconds):
        """Keep running the receive handlers (on_pose) while waiting"""
        end = time.monotonic() + seconds
        while time.monotonic() < end:
            rclpy.spin_once(self, timeout_sec=0.05)


def main():
    rclpy.init()
    node = Pilot()
    log = node.get_logger()
    try:
        while not node.set_mode(GUIDED):
            log.info('Cannot switch to GUIDED. Trying again...')
            node.wait(1.0)
        while not node.arm():
            log.info('Cannot arm (GPS or EKF may still be getting ready). Trying again...')
            node.wait(1.0)
        if not node.takeoff(10.0):
            log.error('The takeoff command was not accepted')
            return
        while node.z is None or node.z < 9.5:
            log.info(f'Climbing... {node.z}')
            node.wait(0.5)
        log.info('North at 2 m/s for 5 seconds')
        for _ in range(50):
            node.send_velocity(0.0, 2.0, 0.0)
            node.wait(0.1)                    # keep sending at intervals shorter than GUID_TIMEOUT (3 seconds)
        node.set_mode(LAND)
        log.info('Landing')
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
```

- `while not ...` repeats until it can arm. Right after startup, GPS and the EKF are often not ready, so arming often fails
- **Keep sending** velocity commands until you want to stop. If you stop sending, it stops in place after `GUID_TIMEOUT` (3 seconds)
- With `header.frame_id` set to `base_link`, the velocity is relative to the vehicle's heading (forward, left, up). Other strings are ignored
- **With a real vehicle**, first test many times in SITL, set up the geofence and failsafes, and make sure you can switch to LOITER or RTL from the transmitter at any time before flying (Chapter 12)

## The other method: MAVROS

- **MAVROS** is a relay node between MAVLink and ROS 2. It predates AP_DDS and works with both ArduPilot and PX4
- It is useful for older flight controllers (F4, F7) that cannot use AP_DDS, or when you want detailed MAVLink features (cameras, gimbals, everything about missions)

```bash
sudo apt install ros-jazzy-mavros ros-jazzy-mavros-extras
wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh
sudo bash ./install_geographiclib_datasets.sh
ros2 launch mavros apm.launch fcu_url:=udp://:14550@
```

| | AP_DDS | MAVROS |
| --- | --- | --- |
| How it works | ArduPilot speaks DDS directly | Converts MAVLink to ROS 2 |
| Requirements | ArduPilot 4.5 or later, an H7 FC | Any FC |
| Coordinates | Already converted to ENU | Already converted to ENU |
| Features | Limited to what is needed (still growing) | Almost all of MAVLink |
| Recommendation | Start here for new projects | Older FCs, or when you need detailed features |

## Exercises

```quiz
Q: What is the feature, from ArduPilot 4.5, that lets the flight controller speak DDS directly?
A: AP_DDS
E: It is the main approach in this book.

Q: What runs on the companion computer and relays between XRCE-DDS and normal ROS 2?
A: micro-ROS Agent | micro-ROS | microROS Agent | micro ros agent
E: XRCE-DDS is a light version of DDS for small microcontrollers.

Q: Which QoS profile do you use to subscribe to position, GPS and battery topics?
A: qos_profile_sensor_data
E: These topics are sent BEST_EFFORT.

Q: Which older bridge node connects MAVLink and ROS 2?
A: MAVROS
E: Use it with older flight controllers or for detailed MAVLink features.
```
