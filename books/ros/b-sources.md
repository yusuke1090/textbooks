# 付録B. 出典と公式のドキュメント

コマンド・トピック名・パラメータは、2026年11月に、次の公式のドキュメントとソースコードで確かめたものです。ROS 2 と ArduPilot は更新が速いので、うまくいかないときは、まず公式のドキュメントの最新の手順を見てください。

この環境では、ROS 2 と ArduPilot（SITL）を実際には動かしていません。Python のコードは文法を確かめ、8章の pymavlink のコードは、MAVLink を話す小さな偽物の機体を相手に、最後まで動くことを確かめました。

## ROS 2

- [ROS 2 Jazzy のドキュメント](https://docs.ros.org/en/jazzy/)（インストール、チュートリアル）
- [ROS 2 Lyrical Luth のリリース（2026年5月）](https://docs.ros.org/en/lyrical/Releases/Release-Lyrical-Luth.html)
- [REP-103（座標の決まり、ENU）](https://www.ros.org/reps/rep-0103.html)、[REP-105（map・odom・base_link）](https://www.ros.org/reps/rep-0105.html)

## ArduPilot

- [ArduPilot の開発者のドキュメント: ROS 2](https://ardupilot.org/dev/docs/ros2.html)、[ROS 2 with SITL](https://ardupilot.org/dev/docs/ros2-sitl.html)、[ROS 2 interfaces](https://ardupilot.org/dev/docs/ros2-interfaces.html)、[ROS 2 with Gazebo](https://ardupilot.org/dev/docs/ros2-gazebo.html)、[ROS 2 over Ethernet](https://ardupilot.org/dev/docs/ros2-over-ethernet.html)
- [ArduPilot の Tools/ros2/README.md](https://github.com/ArduPilot/ardupilot/blob/master/Tools/ros2/README.md)（Humble と Jazzy のワークスペース）
- [ArduPilot の libraries/AP_DDS/README.md](https://github.com/ArduPilot/ardupilot/blob/master/libraries/AP_DDS/README.md)（シリアルの設定、サービスの例）
- ソースコード: `libraries/AP_DDS/AP_DDS_Topic_Table.h`（トピックの名前と QoS）、`AP_DDS_ExternalControl.cpp`（`/ap/cmd_vel` の `map`・`base_link`）、`Tools/ros2/ardupilot_msgs/srv/`（サービスの形）、`ArduCopter/Parameters.cpp`（`GUID_TIMEOUT`）
- [SITL の使い方（sim_vehicle.py）](https://ardupilot.org/dev/docs/using-sitl-for-ardupilot-testing.html)
- [Copter 4.6.3 のリリース](https://discuss.ardupilot.org/t/copter-4-6-3-released/140596)
- [MAVLink のメッセージ（common・ardupilotmega）](https://mavlink.io/en/messages/common.html)

## 日本の法律

- [国土交通省 無人航空機の飛行ルール](https://www.mlit.go.jp/koku/operation.html)
- 2026年の改正: [内閣府 資料（人口集中地区の工業専用地域）](https://www.chisou.go.jp/tiiki/kokusentoc/pdf/punch/260610_didchiku_gaiyou.pdf)、[多数機同時運航の上限撤廃（2026年6月）](https://english.adnkronos.com/2026/06/22/japan-lifts-upper-limit-on-drones-operated-by-one-pilot/)、[小型無人機等飛行禁止法の改正（2026年3月 閣議決定）](https://english.adnkronos.com/2026/03/24/japan-govt-oks-bill-for-wider-drone-no-fly-zones/)
- 電波: [総務省 電波利用ホームページ ドローン等に用いられる無線設備について](https://www.tele.soumu.go.jp/j/sys/others/drone/)
