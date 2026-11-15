# 4. Services, parameters, actions and launch

## What you will learn in this chapter

- Writing a service (request → answer)
- Parameters (a node's settings)
- Actions (jobs that take time)
- Starting many nodes together with a launch file

## Services

- A topic "keeps flowing"; a **service** is an exchange of "ask once, get one answer"
- In ArduPilot too, "arm", "change mode" and "take off" are services (Chapter 9)
- As an example, we write a service that adds two numbers (the type `example_interfaces/srv/AddTwoInts`, included in ROS 2)

```bash
ros2 interface show example_interfaces/srv/AddTwoInts
```

```text
int64 a
int64 b
---
int64 sum
```

- Above `---` is **what you send when asking** (request); below is **what the answer contains** (response)
- Add `<depend>example_interfaces</depend>` to `package.xml`

### The answering side (server)

`my_first/add_server.py`:

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class AddServer(Node):
    def __init__(self):
        super().__init__('add_server')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.on_request)

    def on_request(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'{request.a} + {request.b} = {response.sum}')
        return response


def main():
    rclpy.init()
    node = AddServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.try_shutdown()
```

### The asking side (client)

`my_first/add_client.py`:

```python
import sys

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


def main():
    rclpy.init()
    node = Node('add_client')
    cli = node.create_client(AddTwoInts, 'add_two_ints')
    while not cli.wait_for_service(timeout_sec=1.0):    # wait until the server starts
        node.get_logger().info('Waiting for the service...')

    req = AddTwoInts.Request()
    req.a = int(sys.argv[1])
    req.b = int(sys.argv[2])
    future = cli.call_async(req)                        # ask (the answer goes into future later)
    rclpy.spin_until_future_complete(node, future)      # wait until the answer comes
    node.get_logger().info(f'Answer: {future.result().sum}')

    node.destroy_node()
    rclpy.try_shutdown()
```

Add them to `entry_points` in `setup.py`, build, and run.

```python
            'add_server = my_first.add_server:main',
            'add_client = my_first.add_client:main',
```

```bash
ros2 run my_first add_server                 # terminal 1
ros2 run my_first add_client 3 4             # terminal 2 → Answer: 7
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 10, b: 20}"   # can also be called from the command line
```

- The basic pattern is to ask with `call_async` and wait with `spin_until_future_complete`. Be careful **not to wait for a service answer inside a callback** (waiting on the same thread stops the handler that receives the answer, and everything freezes)

## Parameters

- **Parameters** are a node's settings (speeds, thresholds, port names and so on). You can change them at startup or while running, without editing the program
- Let's make the talker's sending interval a parameter

```python
class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        self.declare_parameter('period', 0.5)                 # name and default value
        period = self.get_parameter('period').value
        self.pub = self.create_publisher(String, 'chatter', 10)
        self.count = 0
        self.timer = self.create_timer(period, self.on_timer)
```

```bash
ros2 run my_first talker --ros-args -p period:=2.0     # change it at startup
ros2 param list /talker
ros2 param get /talker period
ros2 param set /talker period 1.0                       # change it while running (in this example it has no effect unless you write code to reread it)
ros2 param dump /talker > talker.yaml                   # save the current values as YAML
```

- To react to changes while running, register a callback with `add_on_set_parameters_callback`
- ArduPilot's settings (parameters) can also be read and written with ROS 2 services (`/ap/get_parameters`, `/ap/set_parameters`) (Chapter 9)

## Actions

- **Actions** are used for **jobs that take time**, like "go to the destination". Unlike services, progress reports (feedback) arrive along the way, and you can stop partway (cancel)
- You can try them with turtlesim

```bash
ros2 run turtlesim turtlesim_node      # terminal 1
ros2 action list -t                    # /turtle1/rotate_absolute [turtlesim/action/RotateAbsolute]
ros2 action send_goal /turtle1/rotate_absolute turtlesim/action/RotateAbsolute "{theta: 1.57}" --feedback
```

- As the turtle turns, the remaining angle (feedback) is shown, and at the end the result arrives
- Nav2's "go to this place" (`NavigateToPose`) for autonomous driving is also an action

| Mechanism | Good for | Examples |
| --- | --- | --- |
| Topic | Data that keeps flowing | Sensor values, velocity commands, position |
| Service | Requests that finish quickly | Arming, changing mode, reading and writing settings |
| Action | Jobs that take time | Moving to a destination, moving an arm |

## Launch files

- On a robot, you start 10 or 20 nodes at once with set configurations. The file for that is a **launch file** (usually written in Python)
- `~/ros2_ws/src/my_first/launch/chat.launch.py`:

```python
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(package='my_first', executable='talker', parameters=[{'period': 1.0}]),
        Node(package='my_first', executable='listener', output='screen'),
    ])
```

- So that the launch file gets installed, add one line to `data_files` in `setup.py` (with `import os` and `from glob import glob` at the top of the file)

```python
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
```

```bash
cd ~/ros2_ws && colcon build --symlink-install --packages-select my_first && source install/setup.bash
ros2 launch my_first chat.launch.py
```

- Launch files can also take arguments (`DeclareLaunchArgument`), namespaces (`namespace=`, to start the same node for several robots), topic renaming (`remappings=`) and include other launch files (`IncludeLaunchDescription`)
- ArduPilot's simulator (Chapter 9) also starts SITL, the micro-ROS Agent and MAVProxy together with a launch file
