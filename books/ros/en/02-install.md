# 2. Installing ROS 2

## What you will learn in this chapter

- Installing ROS 2 Jazzy on Ubuntu 24.04
- Making it usable with `source`
- Checking that it works with turtlesim and the demos
- The basics of the `ros2` command
- Avoiding crosstalk with other robots on the same network (ROS_DOMAIN_ID)

## Installing

These are the same steps as the official ROS 2 instructions (the Jazzy "Ubuntu (deb packages)" page on docs.ros.org).

1. Set the character encoding (locale) to UTF-8

```bash
locale                     # check that it is UTF-8
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

2. Add the ROS 2 apt repository (the `ros2-apt-source` package installs the key and the repository settings together)

```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
```

3. Install ROS 2

```bash
sudo apt update && sudo apt upgrade
sudo apt install ros-jazzy-desktop    # includes RViz, demos and GUI tools (on a robot, ros-jazzy-ros-base)
sudo apt install ros-dev-tools        # development tools: colcon (build), rosdep (dependencies), vcstool and more
```

- `ros-jazzy-desktop` is several GB. On the small computer carried by a robot, install `ros-jazzy-ros-base`, which has no screen tools
- It is installed in `/opt/ros/jazzy/`

## Making it usable (source)

Each time you open a terminal, you load a settings file before using the ROS 2 commands and libraries.

```bash
source /opt/ros/jazzy/setup.bash
```

Typing it every time is a chore, so write it in `~/.bashrc`.

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
```

- If `printenv ROS_DISTRO` prints `jazzy`, you are set
- For packages you make yourself (Chapter 3), you also load your workspace's `install/setup.bash`. **When a command cannot be found in a new terminal, first suspect that you forgot to source**

## Trying it out

### talker and listener

Open two terminals.

```bash
# terminal 1: send "Hello World" every second
ros2 run demo_nodes_cpp talker
```

```bash
# terminal 2: receive and print it
ros2 run demo_nodes_py listener
```

- You can see that a node written in C++ and a node written in Python can talk on the same topic
- Stop them with Ctrl + C

### turtlesim

```bash
# terminal 1: a window with one turtle appears
ros2 run turtlesim turtlesim_node
```

```bash
# terminal 2: move the turtle with the arrow keys
ros2 run turtlesim turtle_teleop_key
```

## ros2 command basics

With turtlesim still running, try these in a third terminal.

```bash
ros2 node list                       # list of running nodes
ros2 node info /turtlesim            # that node's topics, services and actions
ros2 topic list -t                   # list of topics and their types
ros2 topic echo /turtle1/pose        # keep printing a topic's contents
ros2 topic hz /turtle1/pose          # how many times a second it arrives
ros2 interface show geometry_msgs/msg/Twist    # the message's format
ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0}, angular: {z: 1.8}}"
ros2 service list                    # list of services
ros2 service call /spawn turtlesim/srv/Spawn "{x: 2.0, y: 2.0, theta: 0.0, name: 'turtle2'}"
```

- The last line makes a second turtle appear
- With **rqt_graph** (type `rqt_graph`), you can see how nodes and topics are connected as a diagram

| Command | What it does |
| --- | --- |
| `ros2 run package executable` | Runs one node |
| `ros2 launch package file` | Starts a set of nodes together (Chapter 4) |
| `ros2 topic echo / pub / hz / info` | Look at, send to, rate of, and number of senders and receivers of a topic |
| `ros2 service list / call` | List services, call one |
| `ros2 param list / get / set` | Look at and change parameters (settings) |
| `ros2 bag record / play` | Record and play back topics (Chapter 5) |
| `ros2 doctor` | Checks the ROS 2 environment for problems |

## ROS_DOMAIN_ID

- ROS 2 **connects automatically to nodes on other computers on the same network** (DDS finds them). That is handy, but it also mixes in other people's robots on the same Wi-Fi
- To keep them apart, choose a group number (**ROS_DOMAIN_ID**; 0–101 are commonly used). Only nodes with the same number connect

```bash
echo "export ROS_DOMAIN_ID=7" >> ~/.bashrc
```

- To run only within one computer, use `export ROS_LOCALHOST_ONLY=1` (in Jazzy you can also use `ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST`)
- ArduPilot's DDS uses the same number too (Chapter 9; ArduPilot's `DDS_DOMAIN_ID` defaults to 0)

## Using it with Docker

If you do not have Ubuntu 24.04, or do not want to clutter your computer, you can use the official Docker image (the "Docker Textbook").

```bash
docker run -it --rm --net=host osrf/ros:jazzy-desktop
```

- With `--net=host`, nodes inside and outside the container connect on the same network
- Showing GUIs (RViz, turtlesim) needs X11 settings. Using VS Code's Dev Containers makes it easier
