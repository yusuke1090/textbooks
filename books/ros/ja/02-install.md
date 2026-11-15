# 2. ROS 2 を入れる

## この章でわかること

- Ubuntu 24.04 に ROS 2 Jazzy を入れる
- `source` で使えるようにする
- turtlesim とデモで動きを確かめる
- `ros2` コマンドの基本
- 同じネットワークの別のロボットとの混線を防ぐ（ROS_DOMAIN_ID）

## 入れる

ROS 2 の公式の手順（docs.ros.org の Jazzy の「Ubuntu (deb packages)」）と同じです。

1. 文字コード（ロケール）を UTF-8 にする

```bash
locale                     # UTF-8 になっているか確かめる
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

2. ROS 2 の apt のリポジトリを足す（`ros2-apt-source` というパッケージで、鍵と置き場所の設定をまとめて入れる）

```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
```

3. ROS 2 を入れる

```bash
sudo apt update && sudo apt upgrade
sudo apt install ros-jazzy-desktop    # RViz・デモ・GUI のツールまで入る（ロボットの上なら ros-jazzy-ros-base）
sudo apt install ros-dev-tools        # colcon（ビルド）・rosdep（依存関係）・vcstool など、開発の道具
```

- `ros-jazzy-desktop` は数 GB あります。ロボットに載せる小さなコンピューターには、画面のツールのない `ros-jazzy-ros-base` を入れます
- 入る場所は `/opt/ros/jazzy/` です

## 使えるようにする（source）

ROS 2 のコマンドとライブラリは、ターミナルを開くたびに、設定のファイルを読み込んでから使います。

```bash
source /opt/ros/jazzy/setup.bash
```

毎回打つのは面倒なので、`~/.bashrc` に書いておきます。

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
```

- `printenv ROS_DISTRO` で `jazzy` と出れば OK
- 自分で作ったパッケージ（3章）は、さらに自分のワークスペースの `install/setup.bash` を読み込みます。**新しいターミナルでコマンドが見つからないときは、まず source を忘れていないか**を疑います

## 動かしてみる

### talker と listener

ターミナルを2つ開きます。

```bash
# ターミナル1: 1秒ごとに "Hello World" を送る
ros2 run demo_nodes_cpp talker
```

```bash
# ターミナル2: 受け取って表示する
ros2 run demo_nodes_py listener
```

- C++ で書かれたノードと Python で書かれたノードが、同じトピックで話せていることがわかります
- Ctrl + C で止めます

### turtlesim

```bash
# ターミナル1: 亀が1匹いる画面が出る
ros2 run turtlesim turtlesim_node
```

```bash
# ターミナル2: 矢印キーで亀を動かす
ros2 run turtlesim turtle_teleop_key
```

## ros2 コマンドの基本

turtlesim を動かしたまま、3つめのターミナルで試します。

```bash
ros2 node list                       # 動いているノードの一覧
ros2 node info /turtlesim            # そのノードのトピック・サービス・アクション
ros2 topic list -t                   # トピックの一覧と型
ros2 topic echo /turtle1/pose        # トピックの中身を表示し続ける
ros2 topic hz /turtle1/pose          # 1秒に何回 届いているか
ros2 interface show geometry_msgs/msg/Twist    # メッセージの形
ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0}, angular: {z: 1.8}}"
ros2 service list                    # サービスの一覧
ros2 service call /spawn turtlesim/srv/Spawn "{x: 2.0, y: 2.0, theta: 0.0, name: 'turtle2'}"
```

- 最後の行で、2匹めの亀が出ます
- **rqt_graph**（`rqt_graph` と打つ）で、ノードとトピックのつながりを図で見られます

| コマンド | 何をする |
| --- | --- |
| `ros2 run パッケージ 実行ファイル` | ノードを1つ動かす |
| `ros2 launch パッケージ ファイル` | 決めたノードをまとめて動かす（4章） |
| `ros2 topic echo / pub / hz / info` | トピックを見る・送る・速さ・送り手と受け手の数 |
| `ros2 service list / call` | サービスの一覧・呼ぶ |
| `ros2 param list / get / set` | パラメータ（設定値）を見る・変える |
| `ros2 bag record / play` | トピックを記録・再生する（5章） |
| `ros2 doctor` | ROS 2 の環境の問題を調べる |

## ROS_DOMAIN_ID

- ROS 2 は、**同じネットワークの中なら、ほかのパソコンのノードとも自動でつながります**（DDS が相手を探す）。便利ですが、同じ Wi-Fi の別の人のロボットとも混ざってしまいます
- 混ざらないように、グループの番号（**ROS_DOMAIN_ID**、0〜101 がよく使われる）を決めます。同じ番号のノードだけがつながります

```bash
echo "export ROS_DOMAIN_ID=7" >> ~/.bashrc
```

- 1台のパソコンの中だけで動かしたいときは `export ROS_LOCALHOST_ONLY=1`（Jazzy では `ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST` も使える）
- ArduPilot の DDS も同じ番号を使います（9章。ArduPilot の `DDS_DOMAIN_ID` は、初期値 0）

## Docker で使う

Ubuntu 24.04 がないときや、パソコンを汚したくないときは、Docker の公式イメージを使えます（「Docker の教科書」）。

```bash
docker run -it --rm --net=host osrf/ros:jazzy-desktop
```

- `--net=host` にすると、コンテナの中と外のノードが同じネットワークでつながります
- GUI（RViz・turtlesim）を出すには、X11 の設定が要ります。VS Code の Dev Containers を使うと楽です
