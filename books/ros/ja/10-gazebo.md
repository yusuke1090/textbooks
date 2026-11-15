# 10. Gazebo でシミュレーション

## この章でわかること

- Gazebo とは（SITL との組み合わせ）
- ardupilot_gz を入れて、ドローンを 3D の世界で飛ばす
- RViz でいっしょに見る
- Rover・カメラ・自分の世界

## Gazebo とは

- **Gazebo** は、ロボットの 3D シミュレーターです。重力・ぶつかり・地面の摩擦などの物理と、カメラ・LiDAR・IMU などのセンサーを、パソコンの中で再現します
- 7章の SITL は、機体の動きを簡単な式で計算していました。Gazebo とつなぐと、**3D の世界の中で**、カメラの画像や LiDAR の点群も使って試せます
  - カメラで畝を見つけて走るローバー
  - LiDAR で障害物をよけるドローン
- いまの Gazebo（以前は Ignition Gazebo と呼ばれた）は、版ごとに名前があります。ROS 2 Jazzy には **Gazebo Harmonic** を組み合わせるのが基本です（ROS 2 Lyrical は Gazebo Jetty）
- 昔の「Gazebo Classic」（Gazebo 11）は、2025年1月にサポートが終わりました。古い記事の手順は使えないことが多いので注意します

## 入れる

9章の `~/ardu_ws` に、ArduPilot の Gazebo 用のパッケージ（**ardupilot_gz**）を足します（ArduPilot の公式の手順）。

```bash
sudo apt install ros-jazzy-ros-gz        # ROS 2 と Gazebo Harmonic をつなぐ部品（Gazebo 本体もいっしょに入る）
cd ~/ardu_ws
vcs import --input https://raw.githubusercontent.com/ArduPilot/ardupilot_gz/main/ros2_gz.repos --recursive src
export GZ_VERSION=harmonic
source /opt/ros/jazzy/setup.bash
sudo apt update
rosdep update
rosdep install --from-paths src --ignore-src -y
colcon build --packages-up-to ardupilot_gz_bringup
source install/setup.bash
```

- `export GZ_VERSION=harmonic` は、ビルドするときに毎回 要るので、`~/.bashrc` に書いておくと安心です

## 飛ばす

```bash
cd ~/ardu_ws
source install/setup.bash
ros2 launch ardupilot_gz_bringup iris_runway.launch.py
```

- **SITL・Gazebo・RViz** がまとめて起動し、滑走路の上にクアッドコプター（Iris）が出ます
- 別のターミナルで、MAVProxy をつないで飛ばします

```bash
mavproxy.py --console --map --aircraft test --master=:14550
```

```text
mode guided
arm throttle
takeoff 5
```

- Gazebo の画面で、機体が浮き上がります。9章の `pilot.py` も、そのまま使えます（同じ `/ap/...` のトピックとサービス）
- ほかの例

| launch | 中身 |
| --- | --- |
| `iris_runway.launch.py` | クアッドコプター、滑走路 |
| `iris_maze.launch.py` | クアッドコプター、迷路（LiDAR の練習） |
| `wildthumper_playpen.launch.py` | 6輪のローバー（Rover） |
| `alti_transition_runway.launch.py` | 垂直に離着陸できる飛行機（QuadPlane） |
| `multiagent.launch.py` | 何台も同時に |

## RViz といっしょに見る

- launch で起動した RViz には、機体の位置（`/ap/pose/filtered`）・座標系（TF）・センサーが表示されます
- Gazebo の中のセンサー（カメラ・LiDAR）のデータは、**ros_gz_bridge**（Gazebo と ROS 2 のトピックをつなぐ）で ROS 2 のトピックになります。`ros2 topic list` で、どんなトピックがあるかを見ます
- 画像は `rqt_image_view`（`ros2 run rqt_image_view rqt_image_view`）でも見られます

## 自分の機体と世界

- 機体の形・センサーの付け方は **SDF**（Gazebo の XML の形式）で書きます。`ardupilot_gz_description` の Iris のモデルをコピーして、カメラや LiDAR を足すのが近道です
- 世界（地面・建物・木・畑の畝）も SDF で書きます。Gazebo の Fuel（モデルの共有サイト）から、木や建物のモデルを借りられます
- 畑や牛舎を、本物そっくりにする必要はありません。**試したいこと（畝の線が見えるか、障害物があるか）だけを作る**のがコツです

## 重いときは

- Gazebo は、GPU を使います。ノートパソコンや仮想マシンでは、とても遅くなることがあります
  - 影を消す、カメラの解像度とフレームレートを下げる
  - 画面を出さずに動かす（ヘッドレス。`gz sim -s` のサーバーだけ）
  - シミュレーションの速さ（リアルタイム係数）が 1.0 より小さくても、結果は正しい。ただし、時刻は `/clock` を使う（`use_sim_time:=True`）
- Gazebo なしで試せることは、7〜9章の SITL だけで試すほうが早い
