# 12. IoT とクラウド（センサーからクラウドまで）

**IoT**（Internet of Things、モノのインターネット）は、センサーや機械をインターネットにつなぎ、データを集めたり、遠くから動かしたりすることです。牛舎の温度、牛の首輪の活動量、畑の土の水分、電気のメーターなどがクラウドに集まります。この章では、ここまでの話を、センサーからクラウドまでの道のりに当てはめます。

## IoT のネットワークは、パソコンとちがう

| | パソコン・スマホ | IoT の機械 |
| --- | --- | --- |
| 電気 | コンセントか、毎日充電 | 電池で何年も動かしたいことが多い |
| 場所 | 家・会社 | 牛舎・畑・山・電柱。Wi-Fi が届かない |
| 送る量 | 動画など、たくさん | 数十バイトの数字を、数分に1回 |
| 台数 | 1人に数台 | 何百・何千台 |
| 人 | そばにいる | だれもいない。こわれても気づきにくい |

そのため、遠くまで届き、電気をあまり使わない、IoT のための回線が使われます。

## つなぎ方を選ぶ

| つなぎ方 | とどく範囲 | 速さ / 電気 | 向いているもの |
| --- | --- | --- | --- |
| **Wi-Fi** | 数十 m | 速い / 多い | 家や牛舎の中、カメラ。ピコ W・ESP32 |
| **Bluetooth（BLE）** | 数 m〜数十 m | おそい / とても少ない | スマホとつなぐ機械、首輪から近くの受信機へ |
| **LoRaWAN** | 数 km〜十数 km | とてもおそい / とても少ない | 広い牧場や畑のセンサー。電池で何年も |
| **LTE-M・NB-IoT** | 携帯電話の基地局の範囲 | おそい / 少ない | 1台ずつ SIM を入れて、どこでも。メーター・見守り |
| **4G・5G** | 携帯電話の基地局の範囲 | 速い / 多い | カメラ・ルーター・機械の遠隔操作 |
| **衛星**（Starlink など） | 空が見えればどこでも | 速い / とても多い | 回線のない牧場・山・海 |

![LoRaWAN の機械（左: 土の水分のセンサー、右: ゲートウェイ）](images/lorawan.jpg)

**LoRaWAN** では、センサーが日本では 920 MHz の電波で、近くの**ゲートウェイ**に小さなデータを送ります。ゲートウェイは、Wi-Fi・LAN・LTE でインターネットにつながっていて、データをクラウドの**ネットワークサーバー**に渡します。

![高い所に付けた LoRaWAN のゲートウェイ](images/lora-gateway.jpg)

![電気のスマートメーター](images/smart-meter.jpg)

日本の電気の**スマートメーター**も IoT です。電力会社へ 30分ごとの使用量を送り、家の中の機械とは Wi-SUN（920 MHz）という無線で話せます。

## 牧場から、クラウドまで

![牧場のセンサーからクラウドまで](images/iot.svg)

1. 牛舎の温度・湿度のセンサーや、牛の首輪が、数分ごとに値をはかる
2. LoRaWAN・BLE・Wi-Fi で、牛舎の**ゲートウェイ**に送る
3. ゲートウェイは、光回線や LTE のルーターを通って、クラウドの **MQTT ブローカー**（下）にデータを送る
4. クラウドでは、データを**時系列データベース**にしまい、グラフにし、決めた値をこえたらスマホに知らせる
5. カメラの映像のような大きなデータは、牛舎の Jetson などでその場で調べ（**エッジコンピューティング**）、結果だけを送る

## なぜ機械のほうからつなぐのか

7章で見たように、家や牛舎のルーターの NAT、携帯電話の回線の CGNAT の後ろにある機械には、外から直接つなげません。そこで IoT では、機械のほうからクラウドへつなぎに行き、そのつながりをずっと開いておきます。クラウドからの命令（「換気扇を回して」）も、そのつながりを通って届きます。そのために作られたのが **MQTT** です。

## MQTT: IoT のための、小さなプロトコル

**MQTT** では、機械どうしは直接話さず、真ん中の**ブローカー**を通します。送る側は「この**トピック**に、この値」と**パブリッシュ**し、受け取る側は「このトピックのものをください」と**サブスクライブ**しておきます。

```text
farm/barn1/temp        牛舎1の温度
farm/barn1/humidity    牛舎1の湿度
farm/barn2/temp        牛舎2の温度
farm/barn1/fan/set     牛舎1の換気扇への命令
```

- トピックは `/` で区切った名前。`+` は1段ぶん、`#` はそれより下の全部にあてはまる（`farm/+/temp` は全部の牛舎の温度、`farm/#` は全部）
- ヘッダーが2バイトからと小さく、電気と回線をあまり使わない
- TCP の上で動き、つながりを開いたままにする。ポートは 1883、TLS で暗号にするときは 8883

| 機能 | 意味 |
| --- | --- |
| **QoS** | 0: 送りっぱなし、1: 少なくとも1回は届ける（2回届くこともある）、2: ちょうど1回 |
| **リテイン** | ブローカーが最後の値を覚えておき、あとからサブスクライブした人にもすぐ渡す |
| **ラストウィル** | 機械が急に切れたら、ブローカーが代わりに決めておいたメッセージ（`offline` など）を出す |
| **キープアライブ** | 送るものがなくても、ときどき「生きています」と知らせる |

| | HTTP | MQTT |
| --- | --- | --- |
| 形 | 頼む → 答える | 送る → ブローカー → 受け取りたい全員 |
| つながり | 1回ごと（または少しのあいだ） | 開きっぱなし |
| 外からの命令 | 届かない（機械が聞きに行く） | 開いたつながりで、すぐ届く |
| 大きさ | ヘッダーが大きい | 小さい |

### 試してみる（Python）

パソコンでブローカーを動かします（Ubuntu なら `sudo apt install mosquitto mosquitto-clients` で Mosquitto が入り、すぐ 1883番で待ちます）。Python のライブラリは `pip install paho-mqtt` で入れます。

受け取る側（`sub.py`）:

```python
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, reason_code, properties):
    print("つながった:", reason_code)
    client.subscribe("farm/+/temp", qos=1)    # どの牛舎の温度も受け取る


def on_message(client, userdata, msg):
    print(msg.topic, msg.payload.decode())


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883)
client.loop_forever()
```

送る側（`pub.py`）:

```python
import json
import random
import time

import paho.mqtt.client as mqtt

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("localhost", 1883)
client.loop_start()

for i in range(3):
    temp = round(20 + random.random() * 5, 1)      # 本物ではセンサーの値
    info = client.publish("farm/barn1/temp", json.dumps({"temp": temp}), qos=1)
    info.wait_for_publish()
    print("送った:", temp)
    time.sleep(1)

client.loop_stop()
client.disconnect()
```

ターミナルを2つ開き、`python3 sub.py` を動かしたまま `python3 pub.py` を動かすと、受け取る側に出ます。

```text
つながった: Success
farm/barn1/temp {"temp": 21.1}
farm/barn1/temp {"temp": 23.3}
farm/barn1/temp {"temp": 23.8}
```

`localhost` をラズパイの IP アドレスにすれば、ラズパイと PC の間でも試せます。コマンドだけなら `mosquitto_sub -h localhost -t 'farm/#' -v` と `mosquitto_pub -h localhost -t farm/barn1/temp -m 21.5` でも同じことができます。ピコ W でも、MicroPython の `umqtt` や、C++（Pico SDK の lwIP）の MQTT で同じように送れます。

## クラウドの IoT のサービス

| 使い方 | 例 |
| --- | --- |
| クラウドの会社の IoT サービス | AWS IoT Core・Azure IoT Hub（Google Cloud IoT Core は 2023年に終わった） |
| MQTT ブローカーだけを借りる | HiveMQ Cloud・EMQX Cloud など |
| 自分で立てる | クラウドのサーバー（11章）に Mosquitto を入れる |
| データをためて見る | 時系列データベース（InfluxDB・TimescaleDB など）と Grafana のグラフ |

AWS IoT Core などは、機械1台ずつに証明書（9章）を持たせ、TLS で、その機械に許したトピックだけを読み書きさせます。

## IoT で気をつけること

- **1台ずつちがう鍵**: 全部の機械に同じパスワードを入れると、1台から盗まれたら全部が危ない
- **暗号にする**: 8883番（MQTT over TLS）を使う。1883番のまま外に出さない
- **切れる前提で作る**: 牛舎の回線は切れる。機械やゲートウェイの中にデータをためておき、つながったら送る
- **ソフトを遠くから更新できるように**: 見つかった弱点を直すため（**OTA** 更新）
- **時刻を合わせる**: データに正しい時刻を付けるため、NTP（4章）や GPS で合わせる

## まとめ

- IoT の機械は、電池・遠い場所・小さなデータ・たくさんの台数が特ちょう。Wi-Fi・BLE・LoRaWAN・LTE-M・4G/5G・衛星から選ぶ
- NAT や CGNAT の後ろにあるので、機械のほうからクラウドへつなぎ、つながりを開いておく
- MQTT は、ブローカーを通して、トピックにパブリッシュ・サブスクライブする。1883番、TLS なら 8883番
- 大きなデータはエッジで調べて、結果だけを送る。1台ずつの鍵・暗号・切れる前提が大事

## 練習問題

```quiz
Q: MQTT で、送る側と受け取る側の真ん中で、メッセージを配るサーバーを何といいますか。
A: ブローカー | broker | MQTT ブローカー
E: 機械どうしは直接話さず、ブローカーを通します。

Q: MQTT で、全部の牛舎の温度（farm/barn1/temp、farm/barn2/temp …）を受け取るためにサブスクライブするトピックは何ですか。
A: farm/+/temp
E: `+` は1段ぶんにあてはまります。`farm/#` だと温度以外も全部受け取ります。

Q: MQTT を TLS で暗号にするときに使うポート番号は何番ですか。
A: 8883
E: 暗号にしないときは 1883番です。

Q: 機械が急に切れたとき、ブローカーが代わりに出すよう決めておくメッセージを何といいますか。
A: ラストウィル | Last Will | ウィル | LWT | Last Will and Testament
E: `offline` などを出して、ほかの機械に切れたことを知らせます。

Q: 数 km 以上届き、電池で何年も動かせる、広い牧場や畑のセンサー向きの無線は何ですか。
A: LoRaWAN | LoRa | ローラワン
E: 日本では 920 MHz の電波を使い、ゲートウェイがインターネットへ取り次ぎます。
```
