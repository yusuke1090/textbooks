# 4. サービス・パラメータ・アクション・launch

## サービス

- トピックは「流しっぱなし」、**サービス**は「1回頼んで、1回答えをもらう」やりとりです
- ArduPilot でも「アームして」「モードを変えて」「離陸して」はサービスです（9章）
- 例として、2つの数を足すサービス（ROS 2 に入っている型 `example_interfaces/srv/AddTwoInts`）を書きます

```bash
ros2 interface show example_interfaces/srv/AddTwoInts
```

```text
int64 a
int64 b
---
int64 sum
```

- `---` の上が**頼むときの中身**（request）、下が**答えの中身**（response）です
- `package.xml` に `<depend>example_interfaces</depend>` を足しておきます

### 答える側（server）

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

### 頼む側（client）

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
    while not cli.wait_for_service(timeout_sec=1.0):    # サーバーが起動するまで待つ
        node.get_logger().info('サービスを待っています…')

    req = AddTwoInts.Request()
    req.a = int(sys.argv[1])
    req.b = int(sys.argv[2])
    future = cli.call_async(req)                        # 頼む（答えはあとで future に入る）
    rclpy.spin_until_future_complete(node, future)      # 答えが来るまで待つ
    node.get_logger().info(f'答え: {future.result().sum}')

    node.destroy_node()
    rclpy.try_shutdown()
```

`setup.py` の `entry_points` に足してビルドし、動かします。

```python
            'add_server = my_first.add_server:main',
            'add_client = my_first.add_client:main',
```

```bash
ros2 run my_first add_server                 # ターミナル1
ros2 run my_first add_client 3 4             # ターミナル2 → 答え: 7
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 10, b: 20}"   # コマンドからも呼べる
```

- `call_async` で頼み、`spin_until_future_complete` で待つのが基本の形です。サービスの答えを、**コールバックの中で待たない**ように注意します（同じスレッドで待つと、答えを受け取る処理が回らず、止まってしまう）

## パラメータ

- **パラメータ**は、ノードの設定値です（速さ・しきい値・ポート名など）。プログラムを直さずに、起動するときや動かしている途中に変えられます
- talker の送る間隔を、パラメータにしてみます

```python
class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        self.declare_parameter('period', 0.5)                 # 名前と初期値
        period = self.get_parameter('period').value
        self.pub = self.create_publisher(String, 'chatter', 10)
        self.count = 0
        self.timer = self.create_timer(period, self.on_timer)
```

```bash
ros2 run my_first talker --ros-args -p period:=2.0     # 起動するときに変える
ros2 param list /talker
ros2 param get /talker period
ros2 param set /talker period 1.0                       # 動いている途中で変える（この例では、読み直す処理を書かないと反映されない）
ros2 param dump /talker > talker.yaml                   # いまの値を YAML に保存
```

- 動いている途中の変更に反応させるには、`add_on_set_parameters_callback` でコールバックを登録します
- ArduPilot の設定値（パラメータ）も、ROS 2 のサービス（`/ap/get_parameters`・`/ap/set_parameters`）で読み書きできます（9章）

## アクション

- **アクション**は、「目的地まで行って」のような**時間のかかる仕事**に使います。サービスとちがい、途中経過（feedback）が届き、途中でやめる（cancel）こともできます
- turtlesim で試せます

```bash
ros2 run turtlesim turtlesim_node      # ターミナル1
ros2 action list -t                    # /turtle1/rotate_absolute [turtlesim/action/RotateAbsolute]
ros2 action send_goal /turtle1/rotate_absolute turtlesim/action/RotateAbsolute "{theta: 1.57}" --feedback
```

- 亀が回りながら、残りの角度（feedback）が表示され、最後に結果（result）が届きます
- 自動走行の Nav2 の「この場所まで行って」（`NavigateToPose`）もアクションです

| しくみ | 向いていること | 例 |
| --- | --- | --- |
| トピック | 流れ続けるデータ | センサーの値、速度の指令、位置 |
| サービス | すぐ終わる頼みごと | アーム、モードの変更、設定の読み書き |
| アクション | 時間のかかる仕事 | 目的地へ移動、アームを動かす |

## launch ファイル

- ロボットでは、10個・20個のノードを、決まった設定で一度に起動します。そのためのファイルが **launch ファイル**（Python で書くのがふつう）です
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

- launch ファイルをインストールするように、`setup.py` の `data_files` に1行足します（ファイルの先頭に `import os` と `from glob import glob`）

```python
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
```

```bash
cd ~/ros2_ws && colcon build --symlink-install --packages-select my_first && source install/setup.bash
ros2 launch my_first chat.launch.py
```

- launch ファイルでは、引数（`DeclareLaunchArgument`）・名前空間（`namespace=`、同じノードを何台分も起動する）・トピック名の付け替え（`remappings=`）・ほかの launch ファイルの読み込み（`IncludeLaunchDescription`）もできます
- ArduPilot のシミュレーター（9章）も、launch ファイルで、SITL・micro-ROS Agent・MAVProxy をまとめて起動します

## 練習問題

```quiz
Q: 1回頼んで、1回答えをもらうやりとりを何といいますか。
A: サービス | service
E: トピックは「流しっぱなし」です。

Q: 「目的地まで行って」のような時間のかかる仕事で、途中経過が届き、途中でやめることもできるしくみを何といいますか。
A: アクション | action
E: 途中経過は feedback、やめるのは cancel です。

Q: プログラムを直さずに変えられる、ノードの設定値を何といいますか。
A: パラメータ | parameter | パラメーター
E: 起動するときや、動かしている途中に変えられます。

Q: たくさんのノードを決まった設定で一度に起動するためのファイルを何といいますか。
A: launch ファイル | launchファイル | launch | ローンチファイル
E: Python で書くのがふつうです。`ros2 launch` で起動します。
```
