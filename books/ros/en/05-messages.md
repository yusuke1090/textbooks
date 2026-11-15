# 5. Messages, coordinates, QoS and recording

## What you will learn in this chapter

- Commonly used message types
- Making your own message type
- Coordinate conventions (ROS's ENU and drones' NED) and tf2
- QoS (delivery agreements) and why messages sometimes do not arrive
- Recording and playing back with ros2 bag, and viewing with RViz

## Commonly used message types

| Package | Type | Contents |
| --- | --- | --- |
| std_msgs | `String`, `Float64`, `Bool`, `Header` | Text and numbers. `Header` is a time (stamp) and a coordinate frame name (frame_id) |
| geometry_msgs | `Twist` / `TwistStamped` | Velocity (linear x, y, z and angular x, y, z) |
| geometry_msgs | `Pose` / `PoseStamped` | Position and orientation (a quaternion) |
| sensor_msgs | `NavSatFix` | GPS latitude, longitude and altitude |
| sensor_msgs | `Imu` | Acceleration, angular velocity and orientation |
| sensor_msgs | `Image`, `CompressedImage` | Camera images |
| sensor_msgs | `LaserScan`, `PointCloud2` | LiDAR distances and point clouds |
| sensor_msgs | `BatteryState` | Battery voltage and remaining charge |
| nav_msgs | `Odometry`, `Path`, `OccupancyGrid` | Own position, paths and maps |

- You can see what a type contains with `ros2 interface show sensor_msgs/msg/NavSatFix`
- Types ending in **`...Stamped`** have a `Header`, so you know "when" and "in which coordinate frame" the data is. On robots, use Stamped types where possible

## Making your own message type

- If no standard type fits, you can make your own. The rule is that message types are made in a **C++ package** (`ament_cmake`) (they can be used from Python nodes too)

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_cmake --license Apache-2.0 my_interfaces
mkdir -p my_interfaces/msg
```

`my_interfaces/msg/CowStatus.msg`:

```text
std_msgs/Header header
string cow_id
float32 temperature     # body temperature (°C)
uint32 steps            # step count
bool in_heat            # whether in heat
```

Add to `CMakeLists.txt` (before `ament_package()`):

```cmake
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/CowStatus.msg"
  DEPENDENCIES std_msgs
)
```

Add to `package.xml`:

```xml
<depend>std_msgs</depend>
<buildtool_depend>rosidl_default_generators</buildtool_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

```bash
cd ~/ros2_ws && colcon build --packages-select my_interfaces && source install/setup.bash
ros2 interface show my_interfaces/msg/CowStatus
```

- From Python, use it with `from my_interfaces.msg import CowStatus`
- ArduPilot makes its own types (`ardupilot_msgs`, such as the arming service) in the same way

## Coordinate conventions

### ROS is ENU, drones are NED

This is the easiest place to make mistakes when combining ROS 2 and ArduPilot.

| Convention | x | y | z | Used in |
| --- | --- | --- | --- | --- |
| **ENU** (fixed to the ground) | East | North | Up | ROS (REP-103) |
| **FLU** (fixed to the body) | Forward | Left | Up | The ROS vehicle body (`base_link`) |
| **NED** (fixed to the ground) | North | East | Down | Aircraft, ArduPilot, MAVLink |
| **FRD** (fixed to the body) | Forward | Right | Down | Aircraft bodies |

- ROS has "z up", aircraft have "z down". An altitude of 10 m is z = 10 in ENU and z = −10 in NED
- Heading (yaw) too: ENU measures counterclockwise from east, NED clockwise from north
- ArduPilot's DDS (Chapter 9) converts internally so that it sends and receives in **ENU** on the ROS side. When you use MAVLink (Chapter 8) directly, it is **NED**

### tf2

- A robot has many coordinate frames: the map (`map`), the starting point (`odom`), the body (`base_link`), the camera (`camera_link`), the LiDAR (`laser`)...
- **tf2** is the system that keeps track of the positional relationships (transforms) between frames over time. It can calculate "where on the map is the cow the camera saw?"
- Transforms flow on the topics `/tf` (things that move) and `/tf_static` (things that do not, like a camera screwed to the body)

```bash
# publish a fixed transform: a camera mounted 0.2 m forward of and 0.1 m above the body's center
ros2 run tf2_ros static_transform_publisher --x 0.2 --y 0 --z 0.1 --frame-id base_link --child-frame-id camera_link
ros2 run tf2_ros tf2_echo base_link camera_link        # print the transform
ros2 run tf2_tools view_frames                         # output how the frames connect as a PDF
```

## QoS

- **QoS** (Quality of Service) is a topic's "delivery agreement". If the sender's and receiver's agreements do not match, **nothing arrives, without even an error**

| Setting | Choices | Meaning |
| --- | --- | --- |
| Reliability | **RELIABLE** / **BEST_EFFORT** | Resend until it arrives / send and forget (drops are OK) |
| Durability | VOLATILE / TRANSIENT_LOCAL | Do not give earlier data to late receivers / give them the last data |
| History and Depth | KEEP_LAST and a number | How many to keep |

- For sensor data (GPS, IMU, camera), new data arriving quickly matters more than resending old data, so it is often sent **BEST_EFFORT**
- **If the sender is BEST_EFFORT and the receiver is RELIABLE, they do not connect**. Make the receiver BEST_EFFORT
- The topics ArduPilot's DDS publishes (position, GPS, battery) are BEST_EFFORT too. Use the sensor QoS when receiving them

```python
from rclpy.qos import qos_profile_sensor_data
from geometry_msgs.msg import PoseStamped

self.create_subscription(PoseStamped, '/ap/pose/filtered', self.on_pose, qos_profile_sensor_data)
```

- When nothing arrives, compare the sender's and receiver's QoS with `ros2 topic info -v /topic_name`
- You can set it on the command line too: `ros2 topic echo --qos-reliability best_effort /ap/pose/filtered`

## ros2 bag: recording and playback

- You can record topics and later play them back the same way. It is essential for bringing home data from a real run and trying your program on the desk again and again

```bash
ros2 bag record -o flight1 /ap/pose/filtered /ap/navsat /camera/image_raw   # only the chosen topics
ros2 bag record -a -o all                   # everything (with many images, it quickly reaches several GB)
ros2 bag info flight1                       # what is inside, and how many
ros2 bag play flight1                       # play back (flows on the same topics as when recorded)
ros2 bag play flight1 --rate 2.0 --loop     # double speed, repeating
```

- Jazzy's default storage format is **MCAP** (`.mcap`). It can also be opened with tools like Foxglove

## Viewing with RViz2

- **RViz2** is a tool that shows a robot's position, coordinate frames, point clouds, images and paths in 3D

```bash
rviz2
```

- Use "Add" at the bottom left to choose what to show (TF, Pose, PointCloud2, Image, Path...) and specify the topic
- Set the reference frame (`map` or `odom`) in "Fixed Frame" at the top left. If this is wrong, nothing is shown
- Save the display settings to a `.rviz` file with "File → Save Config"; it can be loaded from a launch file
- Nodes running on a vehicle with no screen (like a Jetson) can be viewed in RViz on a computer on the same network (same `ROS_DOMAIN_ID`)

![A mobile robot with a LiDAR. LiDAR point clouds can be viewed in 3D in RViz](images/lidar-robot.jpg)
