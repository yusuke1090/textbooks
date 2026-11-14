# 8. MAVLink と pymavlink

## この章でわかること

- MAVLink のしくみ（メッセージ・システム ID・ハートビート）
- よく使うメッセージとコマンド
- Python（pymavlink）で、SITL の機体を離陸・移動・着陸させる
- テレメトリ無線と、MAVLink をいくつかに分ける方法

## MAVLink とは

- **MAVLink** は、ドローンと地上局・コンパニオンコンピューターが話すための、小さく軽い**通信の決まり**です。ArduPilot・PX4・多くの地上局が使っています
- 1つのメッセージは数十バイト。遅くて切れやすい無線（テレメトリ）でも使えるように作られています。いまは **MAVLink 2** が使われます
- シリアル（UART）・UDP・TCP のどれの上でも流せます

| 言葉 | 意味 |
| --- | --- |
| **システム ID**（sysid） | 機体ごとの番号（1〜255）。地上局は 255 がふつう。何台も飛ばすときは機体ごとに変える（`SYSID_THISMAV`） |
| **コンポーネント ID**（compid） | 1つの機体の中の部品の番号（オートパイロット 1、カメラ 100 など） |
| **HEARTBEAT** | 「生きているよ」の合図。1秒に1回、全員が送る。機体の種類・モード・アームしているかが入っている |
| メッセージ | 決まった形のデータ（位置・姿勢・電池…）。番号と名前がある |
| **COMMAND_LONG** | 「離陸して」「モードを変えて」などの指令。答え（**COMMAND_ACK**）が返る |

### よく使うメッセージ

| メッセージ | 中身 |
| --- | --- |
| `HEARTBEAT` | 機体の種類、モード（custom_mode）、アームしているか |
| `GLOBAL_POSITION_INT` | 緯度・経度（×10⁷ の整数）、高さ（mm）、速度 |
| `ATTITUDE` | ロール・ピッチ・ヨー（ラジアン） |
| `SYS_STATUS`・`BATTERY_STATUS` | 電池の電圧・残り、センサーの状態 |
| `GPS_RAW_INT` | GPS の衛星の数、精度 |
| `STATUSTEXT` | 文字のメッセージ（「PreArm: 〜」など） |
| `SET_POSITION_TARGET_LOCAL_NED` | GUIDED で、位置や速度を指示する（**NED**） |
| `SET_POSITION_TARGET_GLOBAL_INT` | GUIDED で、緯度・経度で行き先を指示する |
| `MISSION_ITEM_INT` など | ミッション（ウェイポイント）の送受信 |

- メッセージの一覧と中身は、mavlink.io の「common」と「ardupilotmega」のページにあります

## pymavlink で動かす

**pymavlink** は、MAVLink を Python で使うライブラリです（MAVProxy も pymavlink で作られています）。

```bash
python3 -m venv ~/mav-venv
source ~/mav-venv/bin/activate
pip install pymavlink
```

SITL（7章）を動かして、MAVProxy の出力をもう1つ足します。

```text
output add 127.0.0.1:14560
```

`fly.py`:

```python
import time

from pymavlink import mavutil

# SITL の MAVProxy から流れてくる MAVLink を受け取る
master = mavutil.mavlink_connection('udpin:127.0.0.1:14560')
master.wait_heartbeat()
print(f'つながった: system {master.target_system}, component {master.target_component}')


def set_mode(name):
    """モードを名前で変える（GUIDED、LAND など）"""
    mode_id = master.mode_mapping()[name]
    master.mav.set_mode_send(master.target_system,
                             mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, mode_id)


def command(cmd, *params):
    """COMMAND_LONG を送って、その答え（COMMAND_ACK）を待つ。受け付けられたら True"""
    p = list(params) + [0] * (7 - len(params))
    master.mav.command_long_send(master.target_system, master.target_component, cmd, 0, *p)
    end = time.time() + 5
    while time.time() < end:
        ack = master.recv_match(type='COMMAND_ACK', blocking=True, timeout=1)
        if ack is not None and ack.command == cmd:
            return ack.result == mavutil.mavlink.MAV_RESULT_ACCEPTED
    return False


# 位置のメッセージを1秒に5回送ってもらう（200,000 マイクロ秒ごと）
command(mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
        mavutil.mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT, 200000)

set_mode('GUIDED')
while not command(mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 1):   # 1 でアーム、0 でディスアーム
    print('アームできません（GPS や EKF の準備中かもしれない）。待ってもう一度…')
    time.sleep(2)
print('アームしました')

command(mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 10)   # 7番目が高さ（m）

while True:
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    alt = msg.relative_alt / 1000                                  # mm → m（ホームからの高さ）
    print(f'高さ {alt:.1f} m')
    if alt > 9.5:
        break

# 北へ 2 m/s で5秒。速度だけを使う、というビットの目印（type_mask）を付ける
VELOCITY_ONLY = 0b110111000111
for _ in range(10):
    master.mav.set_position_target_local_ned_send(
        0, master.target_system, master.target_component,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, VELOCITY_ONLY,
        0, 0, 0,            # 位置（使わない）
        2.0, 0, 0,          # 速度 北・東・下（NED。上がるときは下の速度をマイナスにする）
        0, 0, 0,            # 加速度（使わない）
        0, 0)               # ヨー・ヨーの速さ（使わない）
    time.sleep(0.5)        # 3秒（GUID_TIMEOUT）より短い間隔で送り続ける

set_mode('LAND')
print('着陸します')
```

```bash
python3 fly.py
```

- `mavlink_connection` の書き方: `udpin:127.0.0.1:14560`（受け取りを待つ）、`tcp:127.0.0.1:5760`（SITL に直接）、`/dev/ttyACM0`（USB の実機。`baud=115200` を足す）
- `recv_match(type=..., blocking=True)` で、ほしい種類のメッセージが来るまで待ちます
- **速度の指令は送り続ける**: GUIDED の速度の指令は、`GUID_TIMEOUT`（初期値 3秒）の間に次の指令が来ないと、止まります。プログラムが止まったときに機体が飛んで行かないための、安全のしくみです
- **NED に注意**: MAVLink の LOCAL_NED は、x が北・y が東・**z が下**です。ROS（ENU）とちがいます（5章）

## テレメトリ無線とルーティング

- 実機と地上局は、**テレメトリ無線**（シリアルの無線モデム）で MAVLink を流します。機体側は FC の TELEM1 にさします
- **日本で使える周波数と、技適のある無線機を使います**。海外でよく売られている 915 MHz や 433 MHz の無線機は、日本ではそのまま使えません（12章）
- 地上局とコンパニオンコンピューターの両方が MAVLink を使いたいときは、FC の別のシリアル（TELEM2）にコンパニオンコンピューターをつなぐか、**mavlink-router** で、1本の MAVLink を何か所にも分けて流します
- ROS 2 から使うときは、MAVLink を直接書くかわりに、9章の **AP_DDS**（または MAVROS）を使うのがふつうです。それでも、困ったときに中で何が起きているかを知るために、MAVLink の知識は役に立ちます
