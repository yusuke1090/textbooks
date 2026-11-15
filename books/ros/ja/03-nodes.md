# 3. ノードとトピック

## ノード・トピック・メッセージ

![ノード・トピック・サービスの関係](images/ros-graph.svg)

| 言葉 | 意味 | 例 |
| --- | --- | --- |
| **ノード** | 1つの仕事をする小さなプログラム | カメラのノード、モーターのノード |
| **トピック** | メッセージを流す「名前の付いた通り道」 | `/camera/image`、`/cmd_vel` |
| **メッセージ** | トピックを流れるデータの形（型） | `std_msgs/msg/String`、`geometry_msgs/msg/Twist` |
| **publish / subscribe** | 送る / 受け取る | ― |
| **サービス** | 頼みごとと答えの1回のやりとり（4章） | 「離陸して」→「OK」 |

- 送る側（publisher）は、だれが受け取るかを知らなくてよい。受け取る側（subscriber）も、だれが送ったかを知らなくてよい。トピックの**名前と型**だけでつながります
- このおかげで、ノードを入れ替えたり、記録用のノードを横から足したりが簡単にできます

## ワークスペースとパッケージ

- **ワークスペース**: 自分のパッケージを置いてビルドする場所。中に `src/` を作る
- **パッケージ**: ノード・設定・launch のファイルをまとめた単位。Python のパッケージ（`ament_python`）と C++ のパッケージ（`ament_cmake`）がある

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python --license Apache-2.0 my_first --dependencies rclpy std_msgs
```

できるもの:

```text
~/ros2_ws/src/my_first/
├── package.xml          # パッケージの名前・説明・依存するパッケージ
├── setup.py             # Python のパッケージの設定。ノードの登録もここ
├── setup.cfg
├── resource/my_first
├── test/
└── my_first/            # ここに Python のファイルを置く
    └── __init__.py
```

## 送るノード（publisher）

`~/ros2_ws/src/my_first/my_first/talker.py` を作ります。

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Talker(Node):
    def __init__(self):
        super().__init__('talker')                                  # ノードの名前
        self.pub = self.create_publisher(String, 'chatter', 10)    # 型・トピック名・キューの長さ
        self.count = 0
        self.timer = self.create_timer(0.5, self.on_timer)         # 0.5秒ごとに on_timer を呼ぶ

    def on_timer(self):
        msg = String()
        msg.data = f'こんにちは {self.count}'
        self.pub.publish(msg)
        self.get_logger().info(f'送った: {msg.data}')
        self.count += 1


def main():
    rclpy.init()
    node = Talker()
    try:
        rclpy.spin(node)        # Ctrl + C まで、タイマーや受信の処理を回し続ける
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == '__main__':
    main()
```

- `rclpy` は、ROS 2 の Python のライブラリです（C++ は `rclcpp`）
- ノードは `Node` を継承したクラスで書くのがふつうです
- `create_timer` と `rclpy.spin` の組み合わせで「決まった間隔で何かをする」を書きます。`while True` と `time.sleep` で書くと、受信の処理が止まってしまうので使いません

## 受け取るノード（subscriber）

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
        self.get_logger().info(f'受け取った: {msg.data}')


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

- メッセージが届くたびに、`on_msg`（**コールバック**）が呼ばれます

## ノードを登録する

`setup.py` の `entry_points` に、コマンドの名前と関数を書きます。

```python
    entry_points={
        'console_scripts': [
            'talker = my_first.talker:main',
            'listener = my_first.listener:main',
        ],
    },
```

## ビルドして動かす

```bash
cd ~/ros2_ws
colcon build --symlink-install --packages-select my_first
source install/setup.bash
ros2 run my_first talker
```

別のターミナルで:

```bash
source ~/ros2_ws/install/setup.bash
ros2 run my_first listener
```

- `colcon build` は、必ず**ワークスペースのいちばん上**（`~/ros2_ws`）で実行します。`build/`・`install/`・`log/` ができます
- `--symlink-install` を付けると、Python のファイルを直したときに、ビルドし直さなくても反映されます（setup.py や新しいファイルを足したときはビルドが要る）
- `~/.bashrc` に `source ~/ros2_ws/install/setup.bash` も書いておくと楽です
- 依存するパッケージが足りないときは、`rosdep install --from-paths src --ignore-src -y` で入れます

## よくあるつまずき

| 症状 | 原因と直し方 |
| --- | --- |
| `Package 'my_first' not found` | `source install/setup.bash` を忘れている |
| 新しいノードが見つからない | `setup.py` の `entry_points` に書いていない。書いたらビルドし直す |
| listener に何も届かない | トピック名のちがい（`chatter` と `/chatter` は、ふつう同じ。名前空間に注意）、型のちがい、`ROS_DOMAIN_ID` のちがい |
| ほかのパソコンのノードが見えない | ファイアウォール、別のネットワーク、`ROS_DOMAIN_ID`。Wi-Fi のマルチキャストが止められている |
| 届くデータの型が合わないと言われる | `ros2 topic info -v トピック名` で、送る側と受け取る側の型と QoS を見る（5章） |

## 練習問題

```quiz
Q: メッセージを流す、名前の付いた通り道を何といいますか。
A: トピック | topic
E: 送る側と受け取る側は、トピックの名前と型だけでつながります。

Q: メッセージが届くたびに呼ばれる関数を何といいますか。
A: コールバック | callback
E: 例えば `on_msg` のような関数です。

Q: ROS 2 のパッケージをビルドするコマンドは何ですか。
A: colcon build | colcon
E: 必ずワークスペースのいちばん上（`~/ros2_ws`）で実行します。

Q: Python のノードを登録するために書く、`setup.py` の項目は何ですか。
A: entry_points
E: 書いたらビルドし直します。
```
