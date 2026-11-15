# 3. Nodes and topics

## Nodes, topics and messages

![How nodes, topics and services relate](images/en/ros-graph.svg)

| Term | Meaning | Example |
| --- | --- | --- |
| **Node** | A small program that does one job | A camera node, a motor node |
| **Topic** | A "named channel" that messages flow through | `/camera/image`, `/cmd_vel` |
| **Message** | The format (type) of the data flowing on a topic | `std_msgs/msg/String`, `geometry_msgs/msg/Twist` |
| **publish / subscribe** | Send / receive | ― |
| **Service** | A single exchange of a request and an answer (Chapter 4) | "Take off" → "OK" |

- The sender (publisher) does not need to know who receives. The receiver (subscriber) does not need to know who sent. They connect by the topic's **name and type** alone
- Thanks to this, you can easily swap nodes or add a recording node on the side

## Workspaces and packages

- **Workspace**: the place where you put and build your packages. Make `src/` inside it
- **Package**: a unit bundling nodes, settings and launch files. There are Python packages (`ament_python`) and C++ packages (`ament_cmake`)

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python --license Apache-2.0 my_first --dependencies rclpy std_msgs
```

What you get:

```text
~/ros2_ws/src/my_first/
├── package.xml          # the package's name, description and the packages it depends on
├── setup.py             # Python package settings; nodes are registered here too
├── setup.cfg
├── resource/my_first
├── test/
└── my_first/            # put your Python files here
    └── __init__.py
```

## A sending node (publisher)

Make `~/ros2_ws/src/my_first/my_first/talker.py`.

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Talker(Node):
    def __init__(self):
        super().__init__('talker')                                  # node name
        self.pub = self.create_publisher(String, 'chatter', 10)    # type, topic name, queue length
        self.count = 0
        self.timer = self.create_timer(0.5, self.on_timer)         # call on_timer every 0.5 seconds

    def on_timer(self):
        msg = String()
        msg.data = f'Hello {self.count}'
        self.pub.publish(msg)
        self.get_logger().info(f'Sent: {msg.data}')
        self.count += 1


def main():
    rclpy.init()
    node = Talker()
    try:
        rclpy.spin(node)        # keep running timer and receive handlers until Ctrl + C
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == '__main__':
    main()
```

- `rclpy` is ROS 2's Python library (for C++, `rclcpp`)
- A node is usually written as a class that inherits from `Node`
- "Do something at a fixed interval" is written with `create_timer` and `rclpy.spin` together. Writing it with `while True` and `time.sleep` would stop message handling, so do not do that

## A receiving node (subscriber)

`~/ros2_ws/src/my_first/my_first/listener.py`:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Listener(Node):
    def __init__(self):
        super().__init__('listener')
        self.sub = self.create_subscription(String, 'chatter', self.on_msg, 10)

    def on_msg(self, msg):
        self.get_logger().info(f'Received: {msg.data}')


def main():
    rclpy.init()
    node = Listener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == '__main__':
    main()
```

- Each time a message arrives, `on_msg` (a **callback**) is called

## Registering the nodes

Write the command names and functions in `entry_points` in `setup.py`.

```python
    entry_points={
        'console_scripts': [
            'talker = my_first.talker:main',
            'listener = my_first.listener:main',
        ],
    },
```

## Building and running

```bash
cd ~/ros2_ws
colcon build --symlink-install --packages-select my_first
source install/setup.bash
ros2 run my_first talker
```

In another terminal:

```bash
source ~/ros2_ws/install/setup.bash
ros2 run my_first listener
```

- Always run `colcon build` at **the top of the workspace** (`~/ros2_ws`). It makes `build/`, `install/` and `log/`
- With `--symlink-install`, changes to Python files take effect without rebuilding (you do need to build after changing setup.py or adding new files)
- It is convenient to also write `source ~/ros2_ws/install/setup.bash` in `~/.bashrc`
- When packages you depend on are missing, install them with `rosdep install --from-paths src --ignore-src -y`

## Common stumbling blocks

| Symptom | Cause and fix |
| --- | --- |
| `Package 'my_first' not found` | You forgot `source install/setup.bash` |
| A new node cannot be found | It is not in `entry_points` in `setup.py`. After adding it, build again |
| Nothing reaches the listener | Different topic names (`chatter` and `/chatter` are usually the same; watch out for namespaces), different types, different `ROS_DOMAIN_ID` |
| Nodes on another computer are invisible | Firewall, a different network, `ROS_DOMAIN_ID`. Wi-Fi multicast is blocked |
| You are told the data types do not match | Use `ros2 topic info -v topic_name` to see the sender's and receiver's types and QoS (Chapter 5) |

## Exercises

```quiz
Q: What is the named channel that messages flow through called?
A: topic | topics
E: Publishers and subscribers connect only by topic name and type.

Q: What is the function called each time a message arrives?
A: callback
E: For example a function like `on_msg`.

Q: Which command builds ROS 2 packages?
A: colcon build | colcon
E: Always run it at the top of the workspace (`~/ros2_ws`).

Q: Which `setup.py` field registers your Python nodes?
A: entry_points
E: Rebuild after editing it.
```
