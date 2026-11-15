# Appendix B. Sources and official documentation

The commands, topic names and parameters were checked in November 2026 against the following official documentation and source code. ROS 2 and ArduPilot change quickly, so if something does not work, first look at the latest steps in the official documentation.

ROS 2 and ArduPilot (SITL) were not actually run in this environment. The Python code was syntax-checked, and the pymavlink code in Chapter 8 was run to the end against a small fake vehicle that speaks MAVLink.

## ROS 2

- [ROS 2 Jazzy documentation](https://docs.ros.org/en/jazzy/) (installation, tutorials)
- [ROS 2 Lyrical Luth release (May 2026)](https://docs.ros.org/en/lyrical/Releases/Release-Lyrical-Luth.html)
- [REP-103 (coordinate conventions, ENU)](https://www.ros.org/reps/rep-0103.html), [REP-105 (map, odom, base_link)](https://www.ros.org/reps/rep-0105.html)

## ArduPilot

- [ArduPilot developer documentation: ROS 2](https://ardupilot.org/dev/docs/ros2.html), [ROS 2 with SITL](https://ardupilot.org/dev/docs/ros2-sitl.html), [ROS 2 interfaces](https://ardupilot.org/dev/docs/ros2-interfaces.html), [ROS 2 with Gazebo](https://ardupilot.org/dev/docs/ros2-gazebo.html), [ROS 2 over Ethernet](https://ardupilot.org/dev/docs/ros2-over-ethernet.html)
- [ArduPilot's Tools/ros2/README.md](https://github.com/ArduPilot/ardupilot/blob/master/Tools/ros2/README.md) (Humble and Jazzy workspaces)
- [ArduPilot's libraries/AP_DDS/README.md](https://github.com/ArduPilot/ardupilot/blob/master/libraries/AP_DDS/README.md) (serial settings, service examples)
- Source code: `libraries/AP_DDS/AP_DDS_Topic_Table.h` (topic names and QoS), `AP_DDS_ExternalControl.cpp` (`map` and `base_link` for `/ap/cmd_vel`), `Tools/ros2/ardupilot_msgs/srv/` (service formats), `ArduCopter/Parameters.cpp` (`GUID_TIMEOUT`)
- [Using SITL (sim_vehicle.py)](https://ardupilot.org/dev/docs/using-sitl-for-ardupilot-testing.html)
- [Copter 4.6.3 release](https://discuss.ardupilot.org/t/copter-4-6-3-released/140596)
- [MAVLink messages (common, ardupilotmega)](https://mavlink.io/en/messages/common.html)

## Japanese law

- [MLIT: flight rules for unmanned aircraft](https://www.mlit.go.jp/koku/operation.html) (Japanese)
- 2026 amendments: [Cabinet Office document (exclusively industrial zones in densely inhabited districts)](https://www.chisou.go.jp/tiiki/kokusentoc/pdf/punch/260610_didchiku_gaiyou.pdf) (Japanese), [Upper limit on simultaneous multi-aircraft operation removed (June 2026)](https://english.adnkronos.com/2026/06/22/japan-lifts-upper-limit-on-drones-operated-by-one-pilot/), [Amendment of the Small Unmanned Aircraft Flight Prohibition Act (Cabinet decision, March 2026)](https://english.adnkronos.com/2026/03/24/japan-govt-oks-bill-for-wider-drone-no-fly-zones/)
- Radio: [MIC Radio Use website: radio equipment used for drones and the like](https://www.tele.soumu.go.jp/j/sys/others/drone/) (Japanese)
