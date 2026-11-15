# 7. SITL: パソコンの中で飛ばす

## この章でわかること

- SITL（Software In The Loop）とは
- ArduPilot をソースから入れて、SITL を動かす
- MAVProxy で離陸・移動・着陸
- 地上局（QGroundControl・Mission Planner）をつなぐ
- Rover と、場所の変え方

## SITL とは

- **SITL**（ソフトウェア・イン・ザ・ループ）は、ArduPilot のファームウェアを、フライトコントローラーではなく**パソコンの上で動かす**しくみです。センサーと機体の動きは、パソコンの中の物理のシミュレーションが作ります
- 実機とまったく同じプログラム・同じパラメータ・同じ MAVLink で動くので、地上局・自分のプログラム（ROS 2 など）を、壊す心配なしに試せます
- まず SITL で動かし、うまくいったものだけを実機で試す、が基本の順番です

## 入れる

```bash
sudo apt install git
cd ~
git clone --recurse-submodules https://github.com/ArduPilot/ardupilot.git
cd ardupilot
Tools/environment_install/install-prereqs-ubuntu.sh -y    # コンパイラ・Python の道具・MAVProxy などを入れる
. ~/.profile                                             # PATH を読み直す（一度ログインし直してもよい）
```

- `master` ブランチは開発中の版です。安定版で試すなら、`git checkout Copter-4.6` のように乗り物と版のブランチに切りかえて、`git submodule update --init --recursive` をします
- ROS 2 といっしょに使うとき（9章）は、ROS 2 のワークスペースの中に ArduPilot を取ってくるので、ここで入れたものとは別になります。この章は SITL と MAVLink に慣れるためのものです

## 動かす

```bash
cd ~/ardupilot
sim_vehicle.py -v ArduCopter --console --map -w
```

- `-v ArduCopter`: クアッドコプター。初めてのときは、ビルドに数分かかります
- `--console --map`: MAVProxy の状態の窓と、地図の窓を出す
- `-w`: パラメータを初期値に戻す（最初の1回だけ付ける）
- 起動すると、ターミナルが **MAVProxy** の入力になります（`STABILIZE>` のように、いまのモードが出る）

### 離陸して、移動して、着陸する

MAVProxy に打ち込みます（GPS がつかまり、コンソールに「EKF3 IMU0 is using GPS」などが出るまで、少し待つ）。

```text
mode guided
arm throttle
takeoff 10
```

- 10 m まで上がります。コンソールの「Alt」で高さを見ます
- 地図の窓で、行きたい所を**右クリック →「Fly to」**で、その場所へ飛びます
- 戻って着陸

```text
mode rtl
```

- `mode land` でその場で着陸、`disarm` でモーターを止める（着陸後）

### よく使う MAVProxy のコマンド

| コマンド | 何をする |
| --- | --- |
| `mode guided` / `mode loiter` / `mode rtl` / `mode land` / `mode auto` | モードを変える |
| `arm throttle` / `disarm` | アーム / ディスアーム |
| `takeoff 10` | 10 m まで離陸（GUIDED のとき） |
| `param show FENCE*` | `FENCE` で始まるパラメータを見る |
| `param set FENCE_ENABLE 1` | パラメータを変える |
| `wp load mission.txt` / `wp list` | ミッションを読み込む / 見る |
| `status` | いま届いているメッセージの中身 |
| `output add 127.0.0.1:14560` | MAVLink を、もう1か所に流す（自分のプログラム用） |

### ミッション（AUTO）を飛ぶ

- 地図の窓で右クリック →「Mission」→「Draw」で、ウェイポイントを置けます
- 地上局（下）で作ったミッションを送って、`mode auto` にすると、順番に飛びます（Copter は、アームしてスロットルを少し上げると始まる。SITL では `rc 3 1500`）

## 地上局をつなぐ

- `sim_vehicle.py` の MAVProxy は、MAVLink を **UDP の 14550 番と 14551 番**にも流しています
- **QGroundControl**（Ubuntu・Windows・Mac・Android・iOS）を起動すると、14550 番で自動でつながり、地図に機体が出ます
- **Mission Planner**（Windows）からは、右上で「UDP」→ 14550 を選びます
- 地上局からも、モードの変更・アーム・ミッションの作成と送信・パラメータの変更ができます。実機の設定（キャリブレーション・ファームウェアの書き込み）も地上局で行います

## Rover と、場所の変え方

```bash
sim_vehicle.py -v Rover --console --map -w
```

![ロボット芝刈り機。決めた範囲を自動で走る機械は、ArduPilot の Rover の得意な使いみち](images/robot-mower.jpg)

- Rover は、`mode guided` → `arm throttle` → 地図で「Fly to」で走ります（離陸はない）
- シミュレーションの場所は、初期はオーストラリアの飛行場です。日本の畑で試したいときは、緯度・経度・高さ・機首の向きを指定します

```bash
sim_vehicle.py -v ArduCopter --console --map --custom-location=42.92,143.20,40,0    # 十勝（帯広の近く）
```

- `--speedup 5` で、シミュレーションを5倍速にできます（長いミッションの確認に）
- `-I 1` で、2台めの機体を別の番号で起動できます（ポートが10番ずつずれる）

## ログ

- ArduPilot は、飛行中のすべてのデータ（センサー・推定した位置・モーターへの出力・モードの変化・エラー）を **DataFlash ログ**（`.bin`）に記録します。SITL では `logs/` に、実機では SD カードに保存されます
- ウェブの **UAV Log Viewer**、MAVProxy の **MAVExplorer**、Mission Planner で、グラフにして見られます
- 「なぜ落ちたのか」「なぜアームできなかったのか」は、ログを見ればたいていわかります。実機でトラブルがあったら、まずログを残します
