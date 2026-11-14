# 付録A. コマンド早見表

## ROS 2

| コマンド | 何をする |
| --- | --- |
| `source /opt/ros/jazzy/setup.bash` | ROS 2 を使えるようにする |
| `source install/setup.bash` | 自分のワークスペースを使えるようにする |
| `ros2 pkg create --build-type ament_python 名前 --dependencies rclpy` | Python のパッケージを作る |
| `colcon build --symlink-install --packages-select 名前` | 1つのパッケージをビルド |
| `colcon build --packages-up-to 名前` | そのパッケージと、依存するものをビルド |
| `rosdep install --from-paths src --ignore-src -y` | 依存するパッケージを apt で入れる |
| `ros2 run パッケージ 実行ファイル --ros-args -p 名前:=値` | ノードを、パラメータを付けて動かす |
| `ros2 launch パッケージ ファイル.launch.py 引数:=値` | まとめて起動 |
| `ros2 node list` / `ros2 node info /名前` | ノードの一覧 / くわしく |
| `ros2 topic list -t` | トピックと型の一覧 |
| `ros2 topic echo /名前` | 中身を表示 |
| `ros2 topic echo --qos-reliability best_effort /名前` | BEST_EFFORT のトピックを表示 |
| `ros2 topic hz /名前` / `ros2 topic info -v /名前` | 届く速さ / 送る側・受け取る側と QoS |
| `ros2 topic pub --once /名前 型 "{...}"` | 1回だけ送る |
| `ros2 service call /名前 型 "{...}"` | サービスを呼ぶ |
| `ros2 action send_goal /名前 型 "{...}" --feedback` | アクションを送る |
| `ros2 param list` / `get` / `set` / `dump` | パラメータ |
| `ros2 interface show 型` | メッセージ・サービスの形 |
| `ros2 bag record -o 名前 /トピック…` / `ros2 bag play 名前` | 記録 / 再生 |
| `rqt_graph` / `rviz2` / `ros2 doctor` | つながりの図 / 3D 表示 / 環境の診断 |
| `export ROS_DOMAIN_ID=7` | グループの番号（ほかのロボットと混ざらない） |

## ArduPilot（SITL と MAVProxy）

| コマンド | 何をする |
| --- | --- |
| `sim_vehicle.py -v ArduCopter --console --map -w` | Copter の SITL を起動（パラメータを初期化） |
| `sim_vehicle.py -v Rover --console --map` | Rover の SITL |
| `--custom-location=緯度,経度,高さ,向き` | シミュレーションの場所 |
| `mode guided` / `mode loiter` / `mode rtl` / `mode land` | モード（MAVProxy） |
| `arm throttle` / `disarm` | アーム / ディスアーム |
| `takeoff 10` | 10 m まで離陸 |
| `param show 名前*` / `param set 名前 値` | パラメータ |
| `output add 127.0.0.1:14560` | MAVLink をもう1か所に流す |

## ArduPilot と ROS 2（AP_DDS）

| コマンド | 何をする |
| --- | --- |
| `ros2 launch ardupilot_sitl sitl_dds_udp.launch.py …` | SITL・Agent・MAVProxy を起動（9章） |
| `ros2 launch ardupilot_gz_bringup iris_runway.launch.py` | Gazebo つきで起動（10章） |
| `ros2 run micro_ros_agent micro_ros_agent serial -b 921600 -D /dev/ttyAMA0` | 実機（シリアル）の Agent |
| `ros2 run micro_ros_agent micro_ros_agent udp4 -p 2019` | 実機（UDP）の Agent |
| `ros2 service call /ap/prearm_check std_srvs/srv/Trigger` | アームできるか |
| `ros2 service call /ap/mode_switch ardupilot_msgs/srv/ModeSwitch "{mode: 4}"` | GUIDED（Copter） |
| `ros2 service call /ap/arm_motors ardupilot_msgs/srv/ArmMotors "{arm: True}"` | アーム |
| `ros2 service call /ap/experimental/takeoff ardupilot_msgs/srv/Takeoff "{alt: 10.5}"` | 離陸 |
| `ros2 topic echo /ap/geopose/filtered` | 緯度・経度・高度 |

## 実機のパラメータ（DDS をシリアルで使う）

| パラメータ | 値 |
| --- | --- |
| `DDS_ENABLE` | 1 |
| `SERIAL2_PROTOCOL` | 45（DDS） |
| `SERIAL2_BAUD` | 921（または 115）。Agent の `-b` と合わせる |
| `DDS_DOMAIN_ID` | `ROS_DOMAIN_ID` と同じ |

## Copter のモードの番号

| 番号 | モード |
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

Rover は、MANUAL 0・HOLD 4・LOITER 5・AUTO 10・RTL 11・GUIDED 15。
