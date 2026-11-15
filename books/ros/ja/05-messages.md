# 5. メッセージ・座標・QoS・記録

## この章でわかること

- よく使うメッセージの型
- 自分のメッセージの型を作る
- 座標の決まり（ROS の ENU と、ドローンの NED）と tf2
- QoS（届け方の約束）と、届かないときの原因
- ros2 bag で記録・再生、RViz で見る

## よく使うメッセージの型

| パッケージ | 型 | 中身 |
| --- | --- | --- |
| std_msgs | `String`, `Float64`, `Bool`, `Header` | 文字・数字。`Header` は時刻（stamp）と座標系の名前（frame_id） |
| geometry_msgs | `Twist` / `TwistStamped` | 速度（並進 linear x,y,z と回転 angular x,y,z） |
| geometry_msgs | `Pose` / `PoseStamped` | 位置（position）と向き（orientation、クォータニオン） |
| sensor_msgs | `NavSatFix` | GPS の緯度・経度・高度 |
| sensor_msgs | `Imu` | 加速度・角速度・向き |
| sensor_msgs | `Image`, `CompressedImage` | カメラの画像 |
| sensor_msgs | `LaserScan`, `PointCloud2` | LiDAR の距離・点群 |
| sensor_msgs | `BatteryState` | 電池の電圧・残り |
| nav_msgs | `Odometry`, `Path`, `OccupancyGrid` | 自己位置・経路・地図 |

- 型の中身は `ros2 interface show sensor_msgs/msg/NavSatFix` で見られます
- **`〜Stamped`** の付いた型には `Header` があり、「いつの」「どの座標系での」データかがわかります。ロボットでは、なるべく Stamped の型を使います

## 自分のメッセージの型を作る

- 決まった型にないものは、自分で作れます。メッセージの型は **C++ のパッケージ**（`ament_cmake`）で作る決まりです（Python のノードからも使える）

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_cmake --license Apache-2.0 my_interfaces
mkdir -p my_interfaces/msg
```

`my_interfaces/msg/CowStatus.msg`:

```text
std_msgs/Header header
string cow_id
float32 temperature     # 体温（℃）
uint32 steps            # 歩数
bool in_heat            # 発情しているか
```

`CMakeLists.txt` に足す（`ament_package()` の前）:

```cmake
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/CowStatus.msg"
  DEPENDENCIES std_msgs
)
```

`package.xml` に足す:

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

- Python からは `from my_interfaces.msg import CowStatus` で使えます
- ArduPilot も、自分の型（`ardupilot_msgs`。アームのサービスなど）を、同じやり方で作っています

## 座標の決まり

### ROS は ENU、ドローンは NED

ここは、ROS 2 と ArduPilot を組み合わせるときに、いちばん間違えやすい所です。

| 決まり | x | y | z | 使う所 |
| --- | --- | --- | --- | --- |
| **ENU**（地面に固定） | 東 | 北 | 上 | ROS（REP-103） |
| **FLU**（機体に固定） | 前 | 左 | 上 | ROS の機体（`base_link`） |
| **NED**（地面に固定） | 北 | 東 | 下 | 航空機、ArduPilot・MAVLink |
| **FRD**（機体に固定） | 前 | 右 | 下 | 航空機の機体 |

- ROS は「z が上」、航空機は「z が下」。高度 10 m は、ENU では z = 10、NED では z = −10 です
- 向き（ヨー角）も、ENU は東から反時計回り、NED は北から時計回り
- ArduPilot の DDS（9章）は、ROS 側には **ENU** で出し入れするように、中で変換してくれます。MAVLink（8章）を直接使うときは **NED** です

### tf2

- ロボットには、たくさんの座標系があります: 地図（`map`）・出発点（`odom`）・機体（`base_link`）・カメラ（`camera_link`）・LiDAR（`laser`）…
- **tf2** は、座標系どうしの位置関係（変換）を、時刻ごとに管理するしくみです。「カメラで見えた牛の位置は、地図の上ではどこか」を計算できます
- 変換は、`/tf`（動くもの）と `/tf_static`（動かないもの。機体にねじで固定したカメラなど）のトピックで流れます

```bash
# 機体の中心から、前に 0.2 m・上に 0.1 m の所にカメラを付けた、という固定の変換を流す
ros2 run tf2_ros static_transform_publisher --x 0.2 --y 0 --z 0.1 --frame-id base_link --child-frame-id camera_link
ros2 run tf2_ros tf2_echo base_link camera_link        # 変換を表示する
ros2 run tf2_tools view_frames                         # 座標系のつながりを PDF に出す
```

## QoS

- **QoS**（Quality of Service）は、トピックの「届け方の約束」です。送る側と受け取る側の約束が合わないと、**エラーも出ずに何も届かない**ことがあります

| 設定 | 選べるもの | 意味 |
| --- | --- | --- |
| Reliability | **RELIABLE** / **BEST_EFFORT** | 届くまで送り直す / 送りっぱなし（落ちてもよい） |
| Durability | VOLATILE / TRANSIENT_LOCAL | あとから来た受け手に、前のデータを渡さない / 最後のデータを渡す |
| History と Depth | KEEP_LAST と数 | 何個まで、ためておくか |

- センサーのデータ（GPS・IMU・カメラ）は、古いものを送り直すより、新しいものが早く届くほうが大事なので、**BEST_EFFORT** で送られることが多い
- **送る側が BEST_EFFORT で、受け取る側が RELIABLE だと、つながりません**。受け取る側を BEST_EFFORT にします
- ArduPilot の DDS が出すトピック（位置・GPS・電池）も BEST_EFFORT です。受け取るときは、センサー用の QoS を使います

```python
from rclpy.qos import qos_profile_sensor_data
from geometry_msgs.msg import PoseStamped

self.create_subscription(PoseStamped, '/ap/pose/filtered', self.on_pose, qos_profile_sensor_data)
```

- 何も届かないときは、`ros2 topic info -v /トピック名` で、送る側と受け取る側の QoS を見比べます
- コマンドでも指定できます: `ros2 topic echo --qos-reliability best_effort /ap/pose/filtered`

## ros2 bag: 記録と再生

- トピックを記録して、あとで同じように再生できます。実機で走らせたデータを持ち帰り、机の上でプログラムを何度も試すのに欠かせません

```bash
ros2 bag record -o flight1 /ap/pose/filtered /ap/navsat /camera/image_raw   # 選んだトピックだけ
ros2 bag record -a -o all                   # 全部（画像が多いと、すぐに数 GB になる）
ros2 bag info flight1                       # 何が何個入っているか
ros2 bag play flight1                       # 再生（記録したときと同じトピックで流れる）
ros2 bag play flight1 --rate 2.0 --loop     # 2倍速で、くり返し
```

- Jazzy の初期の保存形式は **MCAP**（`.mcap`）。Foxglove などの道具でも開けます

## RViz2 で見る

- **RViz2** は、ロボットの位置・座標系・点群・画像・経路を 3D で表示するツールです

```bash
rviz2
```

- 左下の「Add」で、表示するもの（TF、Pose、PointCloud2、Image、Path…）を選び、トピックを指定します
- 左上の「Fixed Frame」に、基準にする座標系（`map` や `odom`）を指定します。ここが合っていないと、何も表示されません
- 表示の設定は「File → Save Config」で `.rviz` ファイルに保存し、launch ファイルから読み込めます
- 画面がない機体（Jetson など）で動くノードも、同じネットワーク（同じ `ROS_DOMAIN_ID`）のパソコンの RViz で見られます

![LiDAR を付けた移動ロボット。LiDAR の点群は RViz で 3D で見られる](images/lidar-robot.jpg)

## 練習問題

```quiz
Q: ROS の地面に固定した座標系は、x が東・y が北・z が上です。これを何といいますか。
A: ENU
E: ArduPilot・MAVLink は NED（北・東・下）です。

Q: NED の z 軸は、上と下のどちらを向いていますか。
A: 下 | した | down
E: NED は North・East・Down です。

Q: 座標系どうしの位置関係を、時刻ごとに管理するしくみは何ですか。
A: tf2 | tf
E: 「カメラで見えた牛は地図の上でどこか」を計算できます。

Q: 送る側が BEST_EFFORT のとき、受け取る側の Reliability を何にするとつながりますか。
A: BEST_EFFORT | best effort
E: 受け取る側が RELIABLE だと、エラーも出ずに何も届きません。

Q: トピックを記録して、あとで再生するコマンドは `ros2` の何ですか。
A: bag | ros2 bag
E: `ros2 bag record` で記録し、`ros2 bag play` で再生します。
```
