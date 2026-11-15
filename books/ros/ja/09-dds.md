# 9. ROS 2 から ArduPilot を動かす

## この章でわかること

- AP_DDS（ArduPilot が直接 ROS 2 で話すしくみ）
- ワークスペースを作って、SITL と ROS 2 をつなぐ
- ArduPilot のトピックとサービス
- Python のノードで、離陸・移動・着陸
- もう1つの方法（MAVROS）

## AP_DDS のしくみ

![ArduPilot と ROS 2 のつながり](images/ardupilot-ros2.svg)

- ArduPilot 4.5 から、フライトコントローラーが **DDS**（ROS 2 の通信）で直接話せるようになりました（**AP_DDS**）
- 小さなマイコンでも動くように、**XRCE-DDS**（DDS の軽い版）を使います。コンパニオンコンピューターで動く **micro-ROS Agent** が、XRCE-DDS と ふつうの ROS 2 の間を中継します
- ROS 2 の側から見ると、`/ap` という名前のノードがいて、トピックとサービスが並んでいるように見えます。MAVLink を知らなくても、ふつうの ROS 2 のプログラムで機体を動かせます
- 座標は ROS の決まり（**ENU**）で出し入れされます（ArduPilot の中で NED から変換）

## ワークスペースを作る

ArduPilot の公式の手順（ArduPilot の `Tools/ros2/README.md`、Jazzy の場合）です。3章の `~/ros2_ws` とは別に、`~/ardu_ws` を作ります。

```bash
mkdir -p ~/ardu_ws/src
cd ~/ardu_ws/src
wget https://raw.githubusercontent.com/ArduPilot/ardupilot/master/Tools/ros2/ros2.jazzy.repos
vcs import --recursive < ros2.jazzy.repos      # ArduPilot・micro-ROS Agent・ardupilot_msgs などを取ってくる
```

依存するパッケージを入れます。

```bash
cd ~/ardu_ws
source /opt/ros/jazzy/setup.bash
sudo apt update
rosdep update
rosdep install --rosdistro ${ROS_DISTRO} --from-paths src --ignore-src --skip-keys microxrcedds_agent -y
```

DDS のコードを作る道具（**Micro-XRCE-DDS-Gen**、Java で動く）を入れます。ArduPilot 4.7 以降（master）には `v4.7.0` を使います。

```bash
sudo apt install default-jre
cd ~/ardu_ws
git clone --recurse-submodules --branch v4.7.0 https://github.com/ardupilot/Micro-XRCE-DDS-Gen.git
cd Micro-XRCE-DDS-Gen
./gradlew assemble
echo "export PATH=\$PATH:$PWD/scripts" >> ~/.bashrc
source ~/.bashrc
```

SITL に必要なものを入れて、ビルドします。

```bash
cd ~/ardu_ws/src/ardupilot
Tools/environment_install/install-prereqs-ubuntu.sh -y
. ~/.profile
cd ~/ardu_ws
colcon build --packages-up-to ardupilot_sitl
source install/setup.bash
```

- ビルドには時間がかかります（初回は数十分のことも）
- 失敗したときは `colcon build --packages-up-to ardupilot_sitl --event-handlers=console_cohesion+` で、くわしいエラーを見ます。多いのは、Micro-XRCE-DDS-Gen の PATH が通っていない（`microxrceddsgen` が見つからない）ことです

## SITL と ROS 2 をつないで起動する

```bash
cd ~/ardu_ws
source install/setup.bash
ros2 launch ardupilot_sitl sitl_dds_udp.launch.py transport:=udp4 synthetic_clock:=True wipe:=False model:=quad speedup:=1 slave:=0 instance:=0 defaults:=$(ros2 pkg prefix ardupilot_sitl)/share/ardupilot_sitl/config/default_params/copter.parm,$(ros2 pkg prefix ardupilot_sitl)/share/ardupilot_sitl/config/default_params/dds_udp.parm sim_address:=127.0.0.1 master:=tcp:127.0.0.1:5760 sitl:=127.0.0.1:5501
```

- 長いですが、1行です。この launch で、**micro-ROS Agent**・**SITL**（ArduCopter）・**MAVProxy** の3つが起動します
- MAVProxy の窓も出したいときは、最後に `map:=True console:=True` を足します
- 別のターミナルで、確かめます

```bash
source ~/ardu_ws/install/setup.bash
ros2 node list               # /ap が見える
ros2 topic list              # /ap/... が並ぶ
ros2 topic echo /ap/geopose/filtered
```

- `ROS_DOMAIN_ID` を変えている場合は、ArduPilot のパラメータ `DDS_DOMAIN_ID`（初期値 0）を同じ番号にします

## ArduPilot のトピックとサービス

### ArduPilot が出すトピック（publish）

| トピック | 型 | 中身 |
| --- | --- | --- |
| `/ap/pose/filtered` | geometry_msgs/msg/PoseStamped | ホームからの位置と向き（ENU） |
| `/ap/twist/filtered` | geometry_msgs/msg/TwistStamped | 速度（ENU） |
| `/ap/geopose/filtered` | geographic_msgs/msg/GeoPoseStamped | 緯度・経度・高度と向き |
| `/ap/navsat` | sensor_msgs/msg/NavSatFix | GPS |
| `/ap/battery` | sensor_msgs/msg/BatteryState | 電池 |
| `/ap/imu/experimental/data` | sensor_msgs/msg/Imu | 加速度・角速度 |
| `/ap/clock`・`/ap/time` | 時刻 | ArduPilot の時刻 |
| `/ap/tf_static` | tf2_msgs/msg/TFMessage | 固定の座標変換 |
| `/ap/status` | ardupilot_msgs/msg/Status | アームしているか、モード など |

- 位置・GPS・電池などのトピックは **BEST_EFFORT** で送られます。受け取るときは `qos_profile_sensor_data` を使います（5章）

### ArduPilot が受け取るトピック（subscribe）

| トピック | 型 | 中身 |
| --- | --- | --- |
| `/ap/cmd_vel` | geometry_msgs/msg/TwistStamped | 速度の指令。`header.frame_id` が `map` なら地面に固定した ENU（東・北・上）、`base_link` なら機体の向き |
| `/ap/cmd_gps_pose` | ardupilot_msgs/msg/GlobalPosition | 緯度・経度で行き先（GUIDED のとき） |
| `/ap/joy` | sensor_msgs/msg/Joy | 送信機（RC）の代わりの操作 |
| `/ap/tf` | tf2_msgs/msg/TFMessage | 外から入れる自己位置（Visual Odometry など） |

### サービス

| サービス | 型 | 中身 |
| --- | --- | --- |
| `/ap/arm_motors` | ardupilot_msgs/srv/ArmMotors | 頼む: `arm`（true/false） → 答え: `result` |
| `/ap/mode_switch` | ardupilot_msgs/srv/ModeSwitch | 頼む: `mode`（番号、6章） → 答え: `status`、`curr_mode` |
| `/ap/experimental/takeoff` | ardupilot_msgs/srv/Takeoff | 頼む: `alt`（m） → 答え: `status` |
| `/ap/prearm_check` | std_srvs/srv/Trigger | アームできる状態か |
| `/ap/get_parameters`・`/ap/set_parameters` | rcl_interfaces | パラメータを読む・変える |

コマンドで試してみます（Copter の GUIDED は 4）。

```bash
ros2 service call /ap/prearm_check std_srvs/srv/Trigger
ros2 service call /ap/mode_switch ardupilot_msgs/srv/ModeSwitch "{mode: 4}"
ros2 service call /ap/arm_motors ardupilot_msgs/srv/ArmMotors "{arm: True}"
ros2 service call /ap/experimental/takeoff ardupilot_msgs/srv/Takeoff "{alt: 10.5}"
```

- アームしたあと、しばらく離陸しないと、安全のために自動でディスアームします。アームしたらすぐに離陸のサービスを呼びます
- MAVProxy の窓や地上局で、機体が上がるのを確かめます

## Python のノードで飛ばす

3章のように自分のパッケージ（`~/ros2_ws` か `~/ardu_ws` の中）を作り、`package.xml` に `ardupilot_msgs`・`geometry_msgs` を足します。`ardupilot_msgs` を使うので、`~/ardu_ws/install/setup.bash` を source したターミナルでビルド・実行します。

`pilot.py`:

```python
import time

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from ardupilot_msgs.srv import ArmMotors, ModeSwitch, Takeoff
from geometry_msgs.msg import PoseStamped, TwistStamped

GUIDED = 4   # Copter のモードの番号（6章）
LAND = 9


class Pilot(Node):
    def __init__(self):
        super().__init__('pilot')
        self.arm_cli = self.create_client(ArmMotors, '/ap/arm_motors')
        self.mode_cli = self.create_client(ModeSwitch, '/ap/mode_switch')
        self.takeoff_cli = self.create_client(Takeoff, '/ap/experimental/takeoff')
        self.vel_pub = self.create_publisher(TwistStamped, '/ap/cmd_vel', qos_profile_sensor_data)
        self.create_subscription(PoseStamped, '/ap/pose/filtered', self.on_pose, qos_profile_sensor_data)
        self.z = None   # ホームからの高さ（ENU の z。上が +）

    def on_pose(self, msg):
        self.z = msg.pose.position.z

    def call(self, cli, req):
        """サービスを呼んで、答えが来るまで待つ"""
        while not cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(f'{cli.srv_name} を待っています…')
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
        msg.header.frame_id = 'map'          # 地面に固定した ENU（x 東・y 北・z 上）
        msg.twist.linear.x = east
        msg.twist.linear.y = north
        msg.twist.linear.z = up
        self.vel_pub.publish(msg)

    def wait(self, seconds):
        """待つ間も、受信の処理（on_pose）を回す"""
        end = time.monotonic() + seconds
        while time.monotonic() < end:
            rclpy.spin_once(self, timeout_sec=0.05)


def main():
    rclpy.init()
    node = Pilot()
    log = node.get_logger()
    try:
        while not node.set_mode(GUIDED):
            log.info('GUIDED にできません。もう一度…')
            node.wait(1.0)
        while not node.arm():
            log.info('アームできません（GPS や EKF の準備中かもしれない）。もう一度…')
            node.wait(1.0)
        if not node.takeoff(10.0):
            log.error('離陸の指示が通りませんでした')
            return
        while node.z is None or node.z < 9.5:
            log.info(f'上昇中… {node.z}')
            node.wait(0.5)
        log.info('北へ 2 m/s で5秒')
        for _ in range(50):
            node.send_velocity(0.0, 2.0, 0.0)
            node.wait(0.1)                    # GUID_TIMEOUT（3秒）より短い間隔で送り続ける
        node.set_mode(LAND)
        log.info('着陸します')
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
```

- `while not ...` で、アームできるまでくり返しています。起動してすぐは、GPS と EKF の準備ができていないため、アームできないことがよくあります
- 速度の指令は、止めたい所まで**送り続けます**。送るのをやめると、`GUID_TIMEOUT`（3秒）でその場に止まります
- `header.frame_id` を `base_link` にすると、機体の向きを基準にした速度（前・左・上）になります。ほかの文字列だと無視されます
- **本物の機体では**、まず SITL で何度も試し、ジオフェンスとフェイルセーフを設定し、いつでも送信機で LOITER や RTL に切りかえられるようにしてから飛ばします（12章）

## もう1つの方法: MAVROS

- **MAVROS** は、MAVLink と ROS 2 をつなぐ中継のノードです。AP_DDS より前からあり、ArduPilot・PX4 の両方で使えます
- AP_DDS が使えない古いフライトコントローラー（F4・F7）や、MAVLink の細かい機能（カメラ・ジンバル・ミッションの全部）を使いたいときに便利です

```bash
sudo apt install ros-jazzy-mavros ros-jazzy-mavros-extras
wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh
sudo bash ./install_geographiclib_datasets.sh
ros2 launch mavros apm.launch fcu_url:=udp://:14550@
```

| | AP_DDS | MAVROS |
| --- | --- | --- |
| しくみ | ArduPilot が直接 DDS で話す | MAVLink を ROS 2 に変換する |
| 必要なもの | ArduPilot 4.5 以降、H7 の FC | どの FC でも |
| 座標 | ENU に変換ずみ | ENU に変換ずみ |
| 機能 | 必要なものに絞っている（増えている途中） | MAVLink のほぼ全部 |
| おすすめ | 新しく作るなら、こちらから | 古い FC、細かい機能が要るとき |

## 練習問題

```quiz
Q: ArduPilot 4.5 から使える、フライトコントローラーが直接 DDS で話すしくみを何といいますか。
A: AP_DDS
E: この教科書のおもなやり方です。

Q: XRCE-DDS と、ふつうの ROS 2 の間を中継する、コンパニオンコンピューターで動くものは何ですか。
A: micro-ROS Agent | micro-ROS | microROS Agent | micro ros agent
E: 小さなマイコンでも動くように、XRCE-DDS（DDS の軽い版）を使います。

Q: 位置・GPS・電池のトピックを受け取るときに使う QoS のプロファイルは何ですか。
A: qos_profile_sensor_data
E: これらのトピックは BEST_EFFORT で送られます。

Q: MAVLink と ROS 2 をつなぐ、AP_DDS より前からある中継のノードは何ですか。
A: MAVROS
E: 古い FC や、MAVLink の細かい機能が要るときに使います。
```
