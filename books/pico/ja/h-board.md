# 付録H. 伝言板のアイデアをピコで作る

スマート農業News の[伝言板](https://yusuke1090.github.io/smart-agri-news/board.html)に書いた6つのアイデアを、実際にピコで作るときの作り方と、買う物をまとめます。
値段は Amazon での目安（2026年11月）です。店や時期で変わります。

## 全体の形

### ピコとラズパイで分ける

ピコは「測る」「動かす」が得意です。カメラの映像を AI で見るのは苦手です（メモリが 0.5MB くらいしかありません）。
そこで、カメラは牛舎に置くラズパイに任せ、ピコは測る・動かす・送るを受け持ちます。

```text
ピコ（牛・牛舎）    測る・動かす・送る
   │ Wi-Fi
   ▼
ラズパイ（牛舎）    集める・カメラ・画面
   │ Wi-Fi
   ▼
スマホ              見る
```

インターネットがなくても、牛舎の Wi-Fi の中で全部が動きます（17章と同じ考え方）。

![ラズパイ 5（牛舎の受信機にする）](images/h-rpi5.jpg)

### 6つのアイデアと作る物

| 伝言板 | ピコで作る物 | むずかしさ |
| --- | --- | --- |
| #1 牛の管理システム | 首輪の活動量計（14〜18章の続き） | ★★★ |
| #2 単機能センサー | 足・尾のタグ、飲み水の流量計 | ★★ |
| #3 牛舎の環境 | 温度・湿度・THI・CO2 の計測器 | ★ |
| #4 夜の乗駕・起き上がれない牛 | 尾根の乗駕センサー、足のタグ | ★★ |
| #5 余った生乳のアプリ | ほぼなし（アプリが中心） | − |
| #6 カラスの追い払い | 首振りの水鉄砲（見つけるのはラズパイ） | ★★★ |

**最初に作るなら #3（牛舎の環境）** です。牛に付けず、電源もコンセントから取れるので、いちばんかんたんです。
次に #2 の流量計、そのあと牛に付ける物（タグ・首輪・乗駕センサー）に進みます。

### みんなで使う物

太字の言葉で Amazon を検索すると見つかります。付録G でそろえた物（ブレッドボード・オス-オスのワイヤー・抵抗・電池ボックス・はんだごて）は、そのまま使います。

| もの | 数 | 目安 |
| --- | --- | --- |
| **Raspberry Pi Pico 2 WH**（無線とピンヘッダ付き） | 作る物の数 | 1枚 約2,000円 |
| **Raspberry Pi 5**（2GB か 4GB） | 1台 | 1.5万〜2.5万円 |
| **Raspberry Pi 5 電源 27W**（公式） | 1個 | 約2,000円 |
| **microSD 32GB** | 1枚 | 約1,000円 |
| **Raspberry Pi 5 ケース ファン付き** | 1個 | 約1,500円 |
| **マイクロUSB ケーブル データ転送** | 2本 | 約500円 |
| **USB 充電器 5V**（コンセントで動かすピコ用） | 2個 | 約1,000円 |
| **ジャンパーワイヤー オス-メス**・**メス-メス** | 1袋ずつ | 約500円 |
| **抵抗 キット**（10kΩ が入ったもの） | 1箱 | 約1,000円 |
| **防水ケース IP67**（10cm くらい） | 作る物の数 | 1個 約1,000円 |
| **デジタル テスター** | 1台 | 約2,000円 |

- 無線を使うので、ピコは **W の付いたもの**にします。Pico 2 W は差し口がマイクロUSB です
- 電波を出す物は、**技適マーク**のあるものを選びます（18章）。海外から直接届く互換ボードには、ないものがあります
- ラズパイ 5 は、2026年に何度も値上がりしています。買う前に値段を確かめてください。試すうちは、ふだんの PC を受信機にしてもかまいません

### ラズパイに送る（どれにも使う）

どの作り方でも、ピコは1分ごとに1行を作ってラズパイに送ります。行の形は次のようにそろえます。

```text
種類,番号,名前=値,名前=値 …
env,1,t=28.5,rh=70,thi=78,co2=850,alert=heat
```

`alert=` が付いた行は「知らせ」です。

#### ピコの側

1. VS Code の **New C/C++ Project** で、Board type を **Pico 2 W**、**Pico wireless options** を **Background lwIP** にして作る（4章）。`lwipopts.h` も自動でできます
2. 同じフォルダに `wifi_udp.h` を作り、次の中身にする。Wi-Fi の名前・パスワード・ラズパイの IP アドレスを書きかえる
3. プログラムの最初で `wifi_begin()` を呼び、`printf(` を `send_line(` に変える

```cpp
#pragma once
// Pico W・Pico 2 W から、牛舎のラズパイ（受信機）へ1行ずつ送る
#include <cstdarg>
#include <cstdio>
#include <cstring>
#include "pico/cyw43_arch.h"
#include "lwip/pbuf.h"
#include "lwip/udp.h"

#define WIFI_SSID     "牛舎の Wi-Fi の名前"
#define WIFI_PASSWORD "Wi-Fi のパスワード"
#define RECEIVER_IP   "192.168.1.10"      // ラズパイの IP アドレス（ラズパイで hostname -I）
constexpr uint16_t RECEIVER_PORT = 5005;

inline udp_pcb* udp_out = nullptr;
inline ip_addr_t receiver;

// Wi-Fi につなぐ（30秒待つ）。つながれば true
inline bool wifi_connect() {
    return cyw43_arch_wifi_connect_timeout_ms(WIFI_SSID, WIFI_PASSWORD, CYW43_AUTH_WPA2_AES_PSK, 30000) == 0;
}

// main() の最初に1回呼ぶ
inline bool wifi_begin() {
    if (cyw43_arch_init()) return false;
    cyw43_arch_enable_sta_mode();
    ipaddr_aton(RECEIVER_IP, &receiver);
    udp_out = udp_new();
    return wifi_connect();
}

// printf と同じ書き方で1行を送る。USB の Serial Monitor にも出す
inline void send_line(const char* fmt, ...) {
    char buf[200];
    va_list ap;
    va_start(ap, fmt);
    int n = vsnprintf(buf, sizeof buf, fmt, ap);
    va_end(ap);
    if (n <= 0) return;
    if (n >= (int)sizeof buf) n = sizeof buf - 1;
    printf("%s", buf);
    if (cyw43_wifi_link_status(&cyw43_state, CYW43_ITF_STA) != CYW43_LINK_JOIN) {
        wifi_connect();                       // 切れていたら、つなぎ直す
    }
    cyw43_arch_lwip_begin();
    pbuf* p = pbuf_alloc(PBUF_TRANSPORT, n, PBUF_RAM);
    if (p) {
        memcpy(p->payload, buf, n);
        udp_sendto(udp_out, p, &receiver, RECEIVER_PORT);
        pbuf_free(p);
    }
    cyw43_arch_lwip_end();
}
```

- **UDP** は、届いたかを確かめない、かんたんな送り方です。1分ごとに送り直すので、1行くらい落ちてもかまいません
- パスワードを書いたファイルは、GitHub に上げないでください

#### ラズパイの側

次の `receiver.py` を動かします。届いた行を日ごとの CSV に残し、スマホのブラウザで最新の値を見られるようにします。

```python
# receiver.py  ― 使い方: python3 receiver.py（ラズパイで動かし、スマホで http://ラズパイの IP:8000 を開く）
# ピコから届く行の形: 種類,番号,名前=値,名前=値 …（例: env,1,t=28.5,rh=70,thi=78）
import datetime
import html
import socket
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

DATA = Path.home() / "barn-data"      # CSV を置くフォルダ（種類-番号-日付.csv）
latest = {}                            # "env,1" → (届いた時刻, ["t=28.5", ...])


def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", 5005))
    while True:
        msg, _ = sock.recvfrom(1024)
        parts = msg.decode(errors="replace").strip().split(",")
        if len(parts) < 3:
            continue
        now = datetime.datetime.now()
        latest[",".join(parts[:2])] = (now, parts[2:])
        DATA.mkdir(exist_ok=True)
        with open(DATA / f"{parts[0]}-{parts[1]}-{now:%Y-%m-%d}.csv", "a") as f:
            f.write(f"{now:%H:%M:%S}," + ",".join(parts[2:]) + "\n")
        if any(p.startswith("alert=") for p in parts):
            print(now, "知らせ:", ",".join(parts), flush=True)   # ここでスマホに知らせてもよい


class Page(BaseHTTPRequestHandler):
    def do_GET(self):
        rows = ""
        for key, (t, values) in sorted(latest.items()):
            color = " style='color:red'" if any(v.startswith("alert=") for v in values) else ""
            rows += f"<tr{color}><td>{html.escape(key)}</td><td>{t:%H:%M}</td><td>{html.escape(' '.join(values))}</td></tr>"
        body = ("<meta charset='utf-8'><meta name='viewport' content='width=device-width'>"
                "<meta http-equiv='refresh' content='60'><h3>牛舎</h3>"
                f"<table border='1' cellpadding='4'>{rows}</table>").encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):      # 画面を開くたびのログは出さない
        pass


threading.Thread(target=listen, daemon=True).start()
ThreadingHTTPServer(("", 8000), Page).serve_forever()
```

- 知らせの行は、画面で赤くなります。ずっと動かすには systemd のサービスにします（付録C）
- スマホに通知を出したいときは、`print(now, "知らせ:" …)` のところで通知のサービスに送ります。インターネットがない牛舎では、ランプやブザーで知らせます（17章）

## #1 牛の管理システム（首輪）

> 伝言板: 売り切り・ローカル完結の、小規模酪農向けの U-motion のようなもの

これは、このガイドの 14〜18章で作ってきた物そのものです。首輪のピコが加速度から行動（休息・採食・反すうなど）を判定し、1分ごとの集計をラズパイに送ります。

![首輪を付けた牛（ニュージーランド）](images/h-collar.jpg)

### 買う物（みんなで使う物のほかに）

| もの | 数 | 目安 |
| --- | --- | --- |
| **GY-521**（MPU-6050） | 首輪の数＋予備 | 3個で約1,000円 |
| **電池ボックス 単3 3本 スイッチ付き** | 首輪の数 | 約300円 |
| **ナイロンベルト 50mm バックル** | 首輪の数 | 約1,000円 |

牛用の首輪は、畜産用品の店でも買えます。

### 作り方

1. 机の上で GY-521 をつなぎ（9・10章）、加速度をフラッシュに記録する（14章）
2. ピコ・GY-521・電池を防水ケースに入れ、ケースが首の上にくるようにベルトに付ける
3. 牛に付けて、動画と一緒にデータを集める（17章の「4. 牛に付けて、データと動画を集める」）
4. 15章で行動の判定を作り、18章の `collar.cpp` の形にする
5. 1分ごとの集計を `send_line()` で送る（例: `collar,12,rest=40,eat=20,rum=0`）
6. ラズパイで、牛ごとに「いつもの様子」と比べて、発情・病気の候補を出す（17章の「9.」）

### 気をつけること

- Wi-Fi につないだままだと、単3 3本で数日しかもちません。まず数日の試験で判定を作り、電池を長くする工夫（16章）や、BLE 付きの省電力マイコンへの切りかえ（17章）はそのあとで考えます
- 付け方は、牛を管理している人と決めます

## #2 単機能センサー

> 伝言板: 分娩・発情・病気の疑い・飲む水の量など、1つの状態だけを安く・小さく見つける

ピコ・GY-521・電池の同じ組み合わせ（**タグ**）を、**付ける場所を変えて**別の単機能センサーにします。飲み水だけは、水道の管に付ける流量計を作ります。

| 付ける場所 | わかること |
| --- | --- |
| 後ろ足 | 歩数（発情で増える）、横になっている時間 |
| 尾 | 尾を上げている時間（分娩が近い） |
| 首 | 反すう・採食（#1 の首輪） |
| 水道の管 | 飲んだ水の量（水槽ごと） |

受信機と画面は、どれも同じ `receiver.py` を使います。

### 足・尾のタグ

| もの | 数 | 目安 |
| --- | --- | --- |
| **GY-521**（MPU-6050） | タグの数 | 3個で約1,000円 |
| **電池ボックス 単3 3本 スイッチ付き** | タグの数 | 約300円 |
| **面ファスナー ベルト 50mm**（足に巻く） | タグの数 | 約800円 |
| **自着性 包帯**（尾に巻く。動物病院で使うもの） | 1巻 | 約500円 |

配線は 10章と同じです（GY-521 の VCC→3V3(OUT)、GND→GND、SDA→GP4、SCL→GP5）。
GY-521 の基板に印刷された **Y の矢印**を、足（尾）にそって下に向けて固定します。

```cpp run
#include <cmath>
#include <cstdio>
#include "pico/stdlib.h"
#include "mpu6050.h"

// 足（または尾）に付けるタグ。1分ごとに、歩数・横だった秒数・続けて横の分を出す
constexpr int ID = 1;              // タグの番号（牛ごとに変える）
constexpr int AXIS = 1;            // 足（尾）にそわせる軸。0=X、1=Y、2=Z
constexpr float TILT_DEG = 60;     // これより傾いたら「横」（足なら寝ている、尾なら上げている）
constexpr float STEP_G = 1.4f;     // 1歩と数える揺れの大きさ [g]
constexpr int LONG_MIN = 180;      // 続けて横がこの分を超えたら知らせる
constexpr int HZ = 10;             // 1秒に測る回数

Mpu6050 imu(i2c0);

int main() {
    stdio_init_all();
    if (!imu.begin(4, 5)) printf("MPU-6050 が見つかりません（配線を確かめる）\n");

    int n = 0, steps = 0, tilt_n = 0, tilt_min = 0;
    bool swing = false;
    absolute_time_t next = get_absolute_time();
    while (true) {
        float a[3];
        imu.read_accel(a[0], a[1], a[2]);
        float g = std::sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2]);   // 止まっていれば約1
        if (g > 0.5f) {
            float deg = std::acos(std::fmin(1.0f, std::fabs(a[AXIS]) / g)) * 57.3f;   // 軸と重力の角度
            if (deg > TILT_DEG) tilt_n++;
        }
        if (!swing && g > STEP_G) {        // 揺れが大きくなった瞬間を1歩と数える
            steps++;
            swing = true;
        } else if (g < 1.1f) {
            swing = false;
        }

        if (++n == 60 * HZ) {              // 1分たった
            int tilt_s = tilt_n / HZ;
            tilt_min = (tilt_s >= 50) ? tilt_min + 1 : 0;   // ほぼ1分ずっと横なら、続けて横の分を増やす
            printf("tag,%d,steps=%d,tilt_s=%d,tilt_min=%d%s\n", ID, steps, tilt_s, tilt_min,
                   tilt_min >= LONG_MIN ? ",alert=long" : "");
            n = steps = tilt_n = 0;
        }
        next = delayed_by_ms(next, 1000 / HZ);
        sleep_until(next);
    }
}
```

| 出る値 | 足に付けたとき | 尾に付けたとき |
| --- | --- | --- |
| `steps` | 1分の歩数。発情のときは、いつもの数倍に増える | （使わない） |
| `tilt_s` | 1分のうち、寝ていた秒数 | 1分のうち、尾を上げていた秒数 |
| `tilt_min` | 続けて寝ている分。長すぎると `alert=long` | （使わない） |

- 机の上で、基板を立てたり寝かせたり、振ったりして、値が変わるのを確かめてから牛に付けます
- 尾のタグは、分娩予定日の数日前から付けます。尾を上げる時間がいつもよりずっと増えたら、分娩が近い候補です
- 発情や分娩の判断は、その牛の数日分と比べます（17章の「9.」）。数字（1.4g・60度・180分）は試しながら直します

### 飲み水の流量計

![水を飲む牛](images/h-drink.jpg)

水道から水槽への管の途中に流量センサーを付け、羽根車が回るたびに出るパルスを数えます。

| もの | 数 | 目安 |
| --- | --- | --- |
| **YF-S201 水流センサー**（1/2 インチ） | 1個 | 約1,000円 |
| **ダイオード 1N4148** | 1本 | 数本で約300円 |
| **ホース ジョイント 1/2 ネジ**・**シールテープ** | 1式 | 約1,000円 |

YF-S201 は 5V で動き、信号も 5V で出ることがあります。ピコのピンに 5V を入れないよう、ダイオードを1本はさみます。

| YF-S201 の線 | つなぐ先 |
| --- | --- |
| 赤（＋） | VBUS（40番。USB の 5V） |
| 黒（−） | GND（38番） |
| 黄（信号） | ダイオードの帯のある側。帯のない側を GP15（20番）へ |

信号が 0V になるとダイオードを通ってピンも低くなり、5V のときはダイオードが止めるので、ピンはピコの中のプルアップで 3.3V になります。

ブレッドボードには、次のように差します。ピコの差し方とピンの並びは、7章の「外付けの LED」と同じです。

1. ダイオードの帯のない側の足を 20番（GP15）の列の空いている穴に、帯のある側の足をピコより左の空いている列に差す
2. センサーの線の先がコネクタ（メス）なら、オス-オスのジャンパーワイヤーを3本差して延ばす
3. 黄をダイオードの帯のある側の列へ、赤を 40番（VBUS）の列へ、黒を 38番（GND）の列へ差す。40番は下の列の右はし、38番は右から3つめ

```cpp run
#include <cstdio>
#include "pico/stdlib.h"

// 水道の管に付けた流量センサー（YF-S201）。1分ごとに、流れた水の量を出す
constexpr int ID = 1;
constexpr uint PIN = 15;                 // 黄色の線（ダイオードを通して GP15）
constexpr float PULSES_PER_L = 450;      // 1L で出るパルスの数（バケツで量って直す）

volatile uint32_t pulses = 0;            // 割り込みで数える（13章）

void on_pulse(uint, uint32_t) {
    pulses++;
}

int main() {
    stdio_init_all();
    gpio_init(PIN);
    gpio_set_dir(PIN, GPIO_IN);
    gpio_pull_up(PIN);
    gpio_set_irq_enabled_with_callback(PIN, GPIO_IRQ_EDGE_FALL, true, &on_pulse);

    uint32_t last = 0;
    absolute_time_t next = get_absolute_time();
    while (true) {
        next = delayed_by_ms(next, 60 * 1000);
        sleep_until(next);
        uint32_t now = pulses;
        float liters = (now - last) / PULSES_PER_L;
        last = now;
        printf("water,%d,l=%.1f,total_l=%.0f,pulses=%lu\n", ID, liters, now / PULSES_PER_L, (unsigned long)now);
    }
}
```

- **合わせ方:** バケツに 10L ためて、増えた `pulses` を 10 で割った数を `PULSES_PER_L` にします
- 本体の矢印を、水の流れる向きに合わせます。精度は ±10% くらいなので、「いつもより減った」を見るのに使います
- 水道の工事にならないよう、水槽の手前のホースの部分に付けます
- この方法でわかるのは水槽ごとの量です。牛ごとの量は、どの牛が飲んだかを見分ける仕組み（耳標の RFID など）がないとわかりません

## #3 牛舎の環境

> 伝言板: 温度・湿度と THI、換気やにおい、カメラで牛の様子。映像はクラウドに送らず数字だけ残す

ピコで温度・湿度・THI・CO2 を測ります。カメラで牛を数えるのはラズパイです。

![扇風機のある牛舎（フリーストール）](images/h-barn.jpg)

### 買う物

| もの | 数 | 目安 |
| --- | --- | --- |
| **SHT31 モジュール**（温度・湿度） | 1個 | 約1,000円 |
| **SCD41 モジュール**（CO2。なくてもよい） | 1個 | 6,000〜1万円 |
| **USB 延長ケーブル 3m** | 1本 | 約800円 |

### 配線

SHT31 と SCD41 は、どちらも I2C です。同じ4本の線に並べてつなぎます（11章）。ブレッドボードへの差し方は、9章の「配線の手順」と同じです。

| ピコ | SHT31・SCD41 |
| --- | --- |
| 3V3(OUT)（36番） | VIN（VCC） |
| GND（38番） | GND |
| GP4（6番） | SDA |
| GP5（7番） | SCL |

### プログラム

```cpp run
#include <cstdio>
#include "pico/stdlib.h"
#include "hardware/i2c.h"

// 牛舎の環境。1分ごとに、温度・湿度・THI と、CO2（SCD41 をつないだとき）を出す
constexpr int ID = 1;
constexpr uint8_t SHT31 = 0x44;
constexpr uint8_t SCD41 = 0x62;
constexpr float THI_ALERT = 72;          // この THI 以上で知らせる

// 確認用のバイト（CRC）。SHT31 も SCD41 も同じ決まり（11章）
uint8_t crc8(const uint8_t* data, int len) {
    uint8_t crc = 0xFF;
    for (int i = 0; i < len; i++) {
        crc ^= data[i];
        for (int b = 0; b < 8; b++) crc = (crc & 0x80) ? (crc << 1) ^ 0x31 : (crc << 1);
    }
    return crc;
}

// 2バイトの命令を送る
bool command(uint8_t addr, uint16_t cmd) {
    uint8_t b[2] = {uint8_t(cmd >> 8), uint8_t(cmd & 0xFF)};
    return i2c_write_blocking(i2c0, addr, b, 2, false) == 2;
}

// 「値2バイト＋確認1バイト」を n 組（3組まで）読む
bool read_words(uint8_t addr, uint16_t* w, int n) {
    uint8_t d[9];
    if (n > 3 || i2c_read_blocking(i2c0, addr, d, n * 3, false) != n * 3) return false;
    for (int i = 0; i < n; i++) {
        if (crc8(d + i * 3, 2) != d[i * 3 + 2]) return false;
        w[i] = (d[i * 3] << 8) | d[i * 3 + 1];
    }
    return true;
}

bool read_sht31(float& temp, float& hum) {
    uint16_t w[2];
    if (!command(SHT31, 0x2400)) return false;   // 1回測る
    sleep_ms(20);
    if (!read_words(SHT31, w, 2)) return false;
    temp = -45 + 175 * w[0] / 65535.0f;
    hum = 100 * w[1] / 65535.0f;
    return true;
}

bool read_co2(int& ppm) {
    uint16_t w[3];                                // CO2・温度・湿度の順
    if (!command(SCD41, 0xEC05)) return false;    // 測った値を読む
    sleep_ms(1);
    if (!read_words(SCD41, w, 3)) return false;
    ppm = w[0];
    return true;
}

int main() {
    stdio_init_all();
    i2c_init(i2c0, 100 * 1000);
    gpio_set_function(4, GPIO_FUNC_I2C);
    gpio_set_function(5, GPIO_FUNC_I2C);
    gpio_pull_up(4);
    gpio_pull_up(5);
    sleep_ms(1000);
    command(SCD41, 0x3F86);                  // 前の測定を止める（ピコだけ再起動したとき用）
    sleep_ms(500);
    bool has_co2 = command(SCD41, 0x21B1);   // 5秒ごとに測り始める。つないでいなければ false

    absolute_time_t next = get_absolute_time();
    while (true) {
        next = delayed_by_ms(next, 60 * 1000);
        sleep_until(next);
        float t = 0, rh = 0;
        if (!read_sht31(t, rh)) {
            printf("env,%d,error=sht31\n", ID);
            continue;
        }
        float thi = 0.8f * t + rh / 100 * (t - 14.4f) + 46.4f;
        char co2[16] = "";
        int ppm = 0;
        if (has_co2 && read_co2(ppm)) snprintf(co2, sizeof co2, ",co2=%d", ppm);
        printf("env,%d,t=%.1f,rh=%.0f,thi=%.0f%s%s\n", ID, t, rh, thi, co2,
               thi >= THI_ALERT ? ",alert=heat" : "");
    }
}
```

- **THI** は、牛の教科書と同じ式（0.8 × 気温 ＋ 湿度/100 × (気温 − 14.4) ＋ 46.4）です。68〜72 を超えると暑熱ストレスが始まるので、72 で知らせます
- **CO2** は換気の目安です。外の空気は約 420ppm で、牛舎の中が高いほど換気が足りません。家畜の建物では 3,000ppm を超えないことが目安とされます
- センサーは、牛がなめたりぶつかったりしない高さに付け、日光と、ミストの水が直接当たらないようにします
- **においの目安**を足すなら、アンモニアのセンサー **MQ-137**（約2,000円）があります。正確な ppm は出ず、上がった・下がったを見る程度です。5V で動き、出力も 5V まで出るので、10kΩ と 20kΩ で分圧してから GP26 に入れます（8章）

### カメラで牛を数える（ラズパイ）

![Raspberry Pi AI カメラ](images/h-ai-camera.jpg)

**Raspberry Pi AI カメラ**（約15,000円）は、カメラの中で AI が動き、牛・人・鳥などの位置を出します。ラズパイは位置を受け取るだけなので、軽く動きます。映像を残さず、数だけ残せます。

1. AI カメラをラズパイ 5 につなぎ、`sudo apt install imx500-all` を打って再起動する
2. `git clone https://github.com/raspberrypi/picamera2` で例をダウンロードし、`picamera2/examples/imx500/` の `imx500_object_detection_demo.py` を動かす。モデルは `--model /usr/share/imx500-models/imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk`
3. 牛に枠が付くのを確かめたら、例のファイルに次の関数を足し、検出の一覧（`last_results`）を作ったあとで `count_cows(last_results, get_labels())` を呼ぶ

```python
# 公式の例に足す（ラズパイ）。決めた四角の中の牛を数えて、1分ごとに receiver.py へ送る
import socket
import time

AREAS = {"feed": (0, 0, 640, 200), "water": (480, 200, 640, 480)}   # 画面の中の四角（左, 上, 右, 下）
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
last_sent = 0


def count_cows(detections, labels):
    global last_sent
    if time.time() - last_sent < 60:
        return
    last_sent = time.time()
    counts = {name: 0 for name in AREAS}
    for d in detections:
        if labels[int(d.category)] != "cow":
            continue
        x, y, w, h = d.box
        cx, cy = x + w / 2, y + h / 2                 # 枠のまん中
        for name, (x1, y1, x2, y2) in AREAS.items():
            if x1 <= cx < x2 and y1 <= cy < y2:
                counts[name] += 1
    line = "cam,1," + ",".join(f"{k}={v}" for k, v in counts.items())
    sock.sendto(line.encode(), ("127.0.0.1", 5005))  # 同じラズパイの receiver.py へ
```

- 画面をつながずに動かすときは、例の中の `show_preview=True` を `False` にします
- 夜は明かりがないと写りません
- 「横になっている牛」を見分けるには、牛舎で撮った写真に名前を付けて、自分でモデルを学習させる必要があります（15章と同じ考え方）

## #4 夜の乗駕・起き上がれない牛

> 伝言板: 夜の乗駕や、起き上がれない牛を AI で見つけて知らせ、人が確かめて記録する

伝言板の案はカメラと AI ですが、ピコではセンサーで同じことを知る方法がかんたんです。

| 知りたいこと | ピコでの方法 |
| --- | --- |
| 乗駕 | 尾根に貼った感圧センサーが、2秒以上押されたら1回と数える |
| 起き上がれない | 足のタグ（#2）で、横になったままの時間が長すぎる |

センサーで「いつ起きたか」を記録しておくと、あとでカメラの AI を作るときの正解（15章のラベル）にも使えます。

### 乗駕センサー

発情した牛は、ほかの牛に乗られてもじっとしています（スタンディング）。尾根（しっぽの付け根の上）に感圧センサーを貼ると、乗られた回数と長さがわかります。

| もの | 数 | 目安 |
| --- | --- | --- |
| **FSR402 感圧センサー** | 牛の数 | 1個 約1,500円 |
| 抵抗 10kΩ（抵抗キット） | 牛の数 | − |
| **電池ボックス 単3 3本 スイッチ付き** | 牛の数 | 約300円 |
| 尾根に貼る布と、牛の毛に使える接着剤 | 1式 | 畜産用品の店や獣医師に相談 |

| つなぐ物 | ピコ |
| --- | --- |
| FSR402 の片方の足 | 3V3(OUT)（36番） |
| FSR402 のもう片方の足 | GP26（31番） |
| 抵抗 10kΩ | GP26 と GND（33番）の間 |

押されるほど FSR402 の抵抗が下がり、GP26 の電圧が上がります。

机の上で試すときは、ブレッドボードに次のように差します。

1. FSR402 の2本の足を、ピコより左の空いている2つの縦の列に差す。抜けやすいときは、オス-メスのジャンパーワイヤーのメスをかぶせて延ばす
2. ジャンパーワイヤーで、片方の足の列を 36番（3V3(OUT)）の列へ、もう片方の足の列を 31番（GP26）の列へつなぐ
3. 抵抗 10kΩ の片方の足を、31番とつないだ足の列に差し、もう片方を空いている列に差す。その列と 33番（GND）の列をワイヤーでつなぐ

```cpp run
#include <cstdio>
#include "pico/stdlib.h"
#include "hardware/adc.h"

// 尾根に貼る乗駕センサー。2秒以上押されたら「乗られた」と数える
constexpr int ID = 1;
constexpr uint PRESSED = 1500;                  // 押されたとみなす値（0〜4095。手で押して決める）
constexpr uint32_t MIN_MS = 2000;               // これより短いのは数えない（ぶつかっただけ）
constexpr uint32_t MAX_MS = 30000;              // これより長いのは数えない（柵に押しつけている）
constexpr uint32_t WINDOW_MS = 4 * 3600 * 1000; // 4時間
constexpr int HEAT_COUNT = 3;                   // 4時間にこの回数で知らせる
constexpr int KEEP = 16;                        // 覚えておく乗駕の数

int main() {
    stdio_init_all();
    adc_init();
    adc_gpio_init(26);                          // GP26 = ADC0（8章）
    adc_select_input(0);

    uint32_t times[KEEP] = {};                  // 最近の乗駕の時刻
    int count = 0;
    uint32_t start = 0;
    bool pressed = false;
    while (true) {
        uint32_t now = to_ms_since_boot(get_absolute_time());
        bool p = adc_read() > PRESSED;
        if (p && !pressed) start = now;         // 押され始めた
        if (!p && pressed) {                    // 離れた
            uint32_t len = now - start;
            if (len >= MIN_MS && len <= MAX_MS) {
                times[count % KEEP] = now;
                count++;
                int recent = 0;                 // 4時間以内の回数
                for (int i = 0; i < KEEP && i < count; i++) {
                    if (now - times[i] <= WINDOW_MS) recent++;
                }
                printf("mount,%d,sec=%.1f,in4h=%d%s\n", ID, len / 1000.0f, recent,
                       recent >= HEAT_COUNT ? ",alert=heat" : "");
            }
        }
        pressed = p;
        sleep_ms(100);
    }
}
```

- `PRESSED` は、センサーを手で押しながら `adc_read()` の値を見て決めます（8章）
- 「4時間に3回」は、尾根に付ける発情発見の機器で使われている目安の1つです。牛舎に合わせて直します
- 貼る場所の毛は短く刈ります。貼り方と、はがれたあとの扱いは、牛を管理している人や獣医師と決めます

### 起き上がれない牛

#2 の足のタグをそのまま使います。牛は1回に1時間くらい横になり、何時間もずっと横になることはふつうありません。
`tilt_min`（続けて寝ている分）が `LONG_MIN`（180分）を超えると `alert=long` が出ます。夜はこの知らせを、ランプやスマホで受けます。

## #5 余った生乳のアプリ

> 伝言板: 余った生乳と、ジェラート・チーズ・脱脂粉乳などの需要をつなぐアプリ

![バルククーラー（生乳を冷やして貯めるタンク）](images/h-bulk-tank.jpg)

このアイデアの中心は、スマホやパソコンで動くアプリです。ピコで作る物は、ほとんどありません。
「いつ・どれだけ余りそうか」の乳量は、集乳の伝票やバルククーラーの目盛りで分かるので、まずは手で入力するほうが確かです。

ピコで手伝えるとしたら、バルククーラーの温度を見守って、冷えていないとき（故障）に知らせることです。乳に触れないよう、タンクの外側に防水の温度センサー（**DS18B20 防水**、約800円）を貼り、#3 と同じように1分ごとに送ります。DS18B20 の読み方は、Pico SDK の例（pico-examples の `pio/onewire`）にあります。

## #6 カラスの追い払い

> 伝言板: カメラでカラスを見つけて、そのカラスだけをねらって追い払う

![ハシブトガラス（大阪）](images/h-crow.jpg)

見つけるのはラズパイの AI カメラ、向けて水を出すのはピコです。

```text
AI カメラ       鳥を見つける
   ▼
ラズパイ        向きを計算する
   ▼ USB
ピコ            サーボを動かす・水を出す
   ▼
首振り台・電磁弁
```

2段階で作ります。

1. **首振り台と LED**で、ねらった所を向くかを確かめる
2. 先にノズルを付け、**電磁弁**で水を出す

### 買う物

| もの | 数 | 目安 |
| --- | --- | --- |
| **Raspberry Pi AI カメラ** | 1台 | 約15,000円 |
| **SG90 パンチルト**（サーボ2個付きの首振り台） | 1組 | 約1,500円 |
| **MG996R** 2個と **パンチルト ブラケット 金属** | 1組 | 約3,500円 |
| **電磁弁 12V ノーマルクローズ 1/2** | 1個 | 約1,500円 |
| **MOSFET モジュール 3.3V**（D4184 など） | 1個 | 約800円 |
| **ダイオード 1N4007** | 1本 | 数本で約300円 |
| **ACアダプター 12V 2A**（電磁弁用） | 1個 | 約1,200円 |
| **ACアダプター 5V 3A** と **DCジャック 変換**（サーボ用） | 1組 | 約1,500円 |
| ホースの継手・細いチューブ・ノズル | 1式 | 約1,500円 |

- SG90 は軽いので、1段階めの LED 用です。ノズルとチューブを載せる2段階めは、力の強い MG996R にします
- 「ノーマルクローズ」は、電気を流さないときは閉じている弁です。停電しても水が出っぱなしになりません

![サーボモーター（SG90）](images/h-servo.jpg)

### 配線

| ピコ | つなぐ先 |
| --- | --- |
| GP16（21番） | 横に回すサーボの信号（オレンジ） |
| GP17（22番） | 縦に回すサーボの信号（オレンジ） |
| GP18（24番） | MOSFET モジュールの信号（SIG・IN） |
| GND（23番） | サーボ用 5V の −、MOSFET モジュールの GND |

- サーボの赤（＋）と茶（−）は、5V 3A のアダプターにつなぎます。ピコの 3V3 や VBUS から取ると、ピコが止まります。**GND はピコとつないで共通に**します
- 電磁弁は、12V の ＋ → 電磁弁 → MOSFET モジュールの出力、とつなぎます。電磁弁の2本の線の間に、ダイオード 1N4007 を、帯のある側を ＋ に向けてつなぎます（切ったときの電圧からピコを守る）
- 1段階めは、電磁弁の代わりに LED と抵抗 330Ω を GP18 につなぎます（付録G）

ブレッドボードには、次のように差します。使うピン（21〜24番）は、どれも下の列の左はしから4つです。

1. 下の ＋ / − の列は、サーボの 5V 専用にする（ピコの 3V3 はつながない）。5V のアダプターの DC ジャック変換のネジの端子に、オス-オスのジャンパーワイヤーを止め、＋ を下の ＋ の列へ、− を下の − の列へ差す
2. ピコの 23番（GND）の列と、下の − の列をワイヤーでつなぐ（GND を共通にする）
3. サーボのコネクタ（メス）に、オス-オスのジャンパーワイヤーを3本ずつ差して延ばす。オレンジを 21番（GP16）・22番（GP17）の列へ、赤を下の ＋ の列へ、茶を下の − の列へ差す
4. MOSFET モジュールの信号（SIG・IN）と GND に、オス-メスのジャンパーワイヤーのメスを差し（ネジの端子なら、オスの側を止める）、信号を 24番（GP18）の列へ、GND を下の − の列へ差す。電磁弁と 12V の線は、モジュールの出力のネジの端子に止める

### ピコのプログラム

```cpp run
#include <cstdio>
#include "pico/stdlib.h"
#include "hardware/clocks.h"
#include "hardware/pwm.h"

// ラズパイから USB で届く命令で、首振り台を向けて水を出す
//   aim 横 縦    … サーボの角度（0〜180。90 が正面）
//   spray ミリ秒 … 電磁弁を開ける（長くても1秒）
constexpr uint PAN = 16, TILT = 17, VALVE = 18;

void servo_init(uint pin) {
    gpio_set_function(pin, GPIO_FUNC_PWM);
    uint slice = pwm_gpio_to_slice_num(pin);
    pwm_set_clkdiv(slice, clock_get_hz(clk_sys) / 1000000.0f);   // 1カウント = 1マイクロ秒
    pwm_set_wrap(slice, 19999);                                   // 20ms ごと（50Hz）
    pwm_set_enabled(slice, true);
}

void servo_deg(uint pin, int deg) {
    if (deg < 0) deg = 0;
    if (deg > 180) deg = 180;
    pwm_set_gpio_level(pin, 500 + deg * 2000 / 180);              // 0.5〜2.5ms のパルス
}

int main() {
    stdio_init_all();
    servo_init(PAN);
    servo_init(TILT);
    servo_deg(PAN, 90);
    servo_deg(TILT, 90);
    gpio_init(VALVE);
    gpio_set_dir(VALVE, GPIO_OUT);
    gpio_put(VALVE, 0);

    char line[32];
    int len = 0;
    while (true) {
        int c = getchar_timeout_us(100 * 1000);      // 1文字読む（0.1秒まで待つ）
        if (c == PICO_ERROR_TIMEOUT) continue;
        if (c != '\n' && c != '\r') {
            if (len < (int)sizeof line - 1) line[len++] = (char)c;
            continue;
        }
        line[len] = '\0';                            // 1行そろった
        len = 0;
        int a = 0, b = 0;
        if (sscanf(line, "aim %d %d", &a, &b) == 2) {
            servo_deg(PAN, a);
            servo_deg(TILT, b);
            printf("ok aim %d %d\n", a, b);
        } else if (sscanf(line, "spray %d", &a) == 1) {
            if (a < 0) a = 0;
            if (a > 1000) a = 1000;
            gpio_put(VALVE, 1);
            sleep_ms(a);
            gpio_put(VALVE, 0);
            printf("ok spray %d\n", a);
        }
    }
}
```

書き込んだら、Serial Monitor で `aim 60 90` や `spray 300` と打って、動きを確かめます。
サーボが端でうなるときは、0〜180 より狭い角度で使います。

### ラズパイのプログラム

#3 と同じ公式の例 `imx500_object_detection_demo.py` に、次の関数を足します。検出の一覧を作ったあとで `chase(last_results, get_labels())` を呼びます。
ピコは USB でラズパイにつなぎます（`/dev/ttyACM0` になります）。

```python
# 公式の例に足す（ラズパイ）。鳥を見つけたら、ピコに向きと水の命令を送る
import random
import time
from pathlib import Path

import serial                        # sudo apt install python3-serial

pico = serial.Serial("/dev/ttyACM0", 115200, timeout=1)
W, H = 640, 480                      # 画像の大きさ（例の設定のまま）
FOV_H, FOV_V = 66, 52                # AI カメラの見える角度（横・縦、度）
LOG = Path.home() / "barn-data"
last_shot = 0


def near(cow, cx, cy):
    x, y, w, h = cow.box
    return x - w / 2 < cx < x + w * 1.5 and y - h / 2 < cy < y + h * 1.5


def chase(detections, labels):
    global last_shot
    names = [labels[int(d.category)] for d in detections]
    birds = [d for d, n in zip(detections, names) if n == "bird"]
    cows = [d for d, n in zip(detections, names) if n == "cow"]
    if not birds or time.time() - last_shot < 5:     # 5秒に1回まで
        return
    x, y, w, h = birds[0].box
    cx, cy = x + w / 2, y + h / 2
    if any(near(c, cx, cy) for c in cows):            # 牛のそばの鳥はねらわない
        return
    pan = 90 - (cx / W - 0.5) * FOV_H                 # 逆に動くときは - と + を入れかえる
    tilt = 90 + (cy / H - 0.5) * FOV_V
    pico.write(f"aim {pan:.0f} {tilt:.0f}\n".encode())
    time.sleep(0.5)                                   # 向くのを待つ
    pico.write(f"spray {random.choice([200, 400, 700])}\n".encode())   # 長さを変えて、慣れにくくする
    last_shot = time.time()
    LOG.mkdir(exist_ok=True)
    with open(LOG / f"crow-{time.strftime('%Y-%m-%d')}.csv", "a") as f:
        f.write(f"{time.strftime('%H:%M:%S')},{cx:.0f},{cy:.0f}\n")
```

- 見つけた時刻が `crow-日付.csv` に残るので、カラスの多い時間帯がわかります
- AI カメラのモデルは「鳥」までしか見分けません。カラスだけにしたいときは、牛舎で撮ったカラスの写真で学習させます
- カメラとノズルは、なるべく近くに並べて付けます。離れていると、ねらいがずれます

### 気をつけること

- **牛に水をかけない。** 牛のそばの鳥はねらわず、水の向きも牛の体の高さを避けます
- **慣れを防ぐ。** 同じことを続けると、カラスは慣れます。水の長さを変えるほか、時間帯で光や音と組み合わせることも考えます
- **レーザーは使わない。** 牛や人の目を傷つけるおそれがあります
- **追い払うだけにする。** カラスを捕まえたり傷つけたりするには、鳥獣保護管理法の許可が要ります。追い払うだけなら許可は要りません
- 水まわりで電気を使うので、ピコと電源は防水ケースに入れ、コンセント側は水がかからない所にします

## 合計の目安

| 作る物 | 目安 |
| --- | --- |
| みんなで使う物（ラズパイ一式・ピコ2枚など） | 3万〜4万円 |
| #3 牛舎の環境（CO2 も測る） | 約1万円（カメラは別に 15,000円） |
| #2 流量計 | 約3,000円 |
| #1・#2・#4 タグや首輪（1つ） | 約3,000円 |
| #4 乗駕センサー（1つ） | 約4,000円 |
| #6 カラスの追い払い | 約3万円（AI カメラを含む） |

## まとめ

- ピコは測る・動かす・送る、カメラの AI と記録はラズパイ。牛舎の Wi-Fi の中で全部が動く
- ピコは `send_line()` で「種類,番号,名前=値」の1行を送り、ラズパイの `receiver.py` が CSV に残して画面に出す
- 最初は #3（牛舎の環境）から。次に流量計、そのあと牛に付ける物へ
- 足・尾・首のタグは同じ組み合わせで、付ける場所と数字だけを変える
- 判定は診断ではなく、人が確かめるための知らせ。数字は牛舎で試しながら直す

## 練習問題

```quiz
Q: カメラの映像を AI で見る仕事は、ピコとラズパイのどちらに任せますか。
A: ラズパイ | Raspberry Pi
E: ピコはメモリが少ないので、測る・動かす・送るを受け持ちます。

Q: この付録の牛舎の環境のプログラムは、THI がいくつ以上で `alert=heat` を出しますか。
A: 72
E: THI が 68〜72 を超えると、暑熱ストレスが始まります。

Q: YF-S201 は、1L の水が流れると約何回のパルスを出しますか。
A: 450 | 450回
E: 正確な数は、バケツに 10L ためて数えて合わせます。

Q: 乗駕センサーは、何秒以上押されたら1回と数えますか。
A: 2 | 2秒
E: 短いのはぶつかっただけ、長すぎるのは柵に押しつけているとみなして、数えません。

Q: カラスを追い払うのに、牛や人の目を傷つけるおそれがあるので使わない光は何ですか。
A: レーザー | レーザー光
E: 水・光・音を組み合わせ、慣れないように変えていきます。
```
