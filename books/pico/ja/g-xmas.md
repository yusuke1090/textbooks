# 付録G. クリスマスのイルミネーションを作る

ふつうの LED を10個ピコにつないで、チカチカ・順番に点灯・ふわっと・きらきらと光らせます。
プログラムは MicroPython で書いてコマンド（mpremote）で書き込み、電池で動かします。

![LED のクリスマスツリー](images/xmas-tree.jpg)

## 用意するもの

| もの | 数 | メモ |
| --- | --- | --- |
| LED（5mm） | 10個 | 赤・緑・黄・青・白を2個ずつ |
| 抵抗 330Ω | 4本 | 赤・黄の LED 用 |
| 抵抗 100Ω | 6本 | 緑・青・白の LED 用 |
| ブレッドボード | 1枚 | 830穴 |
| ジャンパーワイヤー（オス-オス） | 11本 | やわらかい線。遠い LED まで届く長さのもの |
| ピンヘッダ | 20ピン×2本 | ピコに付いてくることが多い。はんだ付けは8章 |
| USB ケーブル | 1本 | データ転送ができるもの。ピコの差し口（USB-C かマイクロUSB）に合わせる |
| 電池ボックス | 1個 | 単3×3本、スイッチ付き |
| 単3電池 | 3本 | アルカリ |

Amazon でそろえて約3,000円です（2026年11月）。

![5mm の LED](images/leds.jpg)

### 抵抗の選び方

| LED の色 | 抵抗 | 帯の色 |
| --- | --- | --- |
| 赤・黄 | 330Ω | 橙・橙・茶・金 |
| 緑・青・白 | 100Ω | 茶・黒・茶・金 |

赤と黄の LED は低い電圧で光るので、抵抗を大きくして、どの色も 4mA くらいの電流にそろえます。
ピコの GPIO は全部あわせて 50mA までなので、10個（約 40mA）なら直接つないで大丈夫です。
迷ったら全部 330Ω でもかまいません（緑・青・白が少し暗くなるだけです）。

![抵抗（帯の色で値がわかる）](images/resistors.jpg)

## 配線

![イルミネーションの回路（LED 10個と電池）](images/xmas-circuit.svg)

- GP0〜GP9 の10本に、抵抗と LED を1組ずつつなぎます。LED の短い足は、全部 GND にまとめます
- 電池ボックスの赤い線（＋）は **VSYS（39番）**、黒い線（−）は GND につなぎます。VSYS に入れられるのは 1.8〜5.5V なので、単3を4本（6V）にはしないでください

### ブレッドボードに並べる

![ブレッドボードへの並べ方](images/xmas-breadboard.svg)

1. USB と電池を外しておく
2. ピコを右はしに、USB を右に向けて、真ん中の溝をまたいで差す
3. 抵抗を、真ん中の溝をまたいで差す。左から GP0、GP1 … の順に、2列ずつあけて10本
4. LED の長い足（＋）を抵抗の下の列に、短い足（−）を青い線（−）の列に差す
5. ジャンパーワイヤーで、ピコの GP0〜GP9 の列と、抵抗の上の列をつなぐ。GP0 がいちばん左の LED
6. ピコの GND（38番）の列と、青い線（−）の列をワイヤーでつなぐ
7. 電池ボックスのスイッチを切ったまま、赤い線を VSYS（39番）の列に、黒い線を青い線（−）の列に差す

電池ボックスの線の先が細いより線なら、はんだで固めてから差すと抜けにくくなります。

## 配線を確かめる

USB で PC につなぎ（電池のスイッチは切ったまま）、LED が1つずつ光るか確かめます。次のプログラムを test.py という名前で保存します。

```python run
from machine import Pin
import time

for n in range(10):
    print("GP{} が光っているはず".format(n))
    led = Pin(n, Pin.OUT)
    led.on()
    time.sleep(1)
    led.off()

print("おわり")
```

```bash
mpremote run test.py
```

光らない LED があれば、LED の向き（長い足が抵抗の側）と、ワイヤーを差した列を確かめてください。

## イルミネーションのプログラム

次のプログラムを main.py という名前で保存します。

```python run
from machine import Pin, PWM
import time
import random

PINS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]   # LED をつないだ GP の番号（光る順）

leds = []
for n in PINS:
    p = PWM(Pin(n))
    p.freq(1000)
    leds.append(p)

def light(i, level):
    # i 番目の LED を、0〜100 の明るさにする
    leds[i].duty_u16(level * level * 65535 // 10000)   # 2乗すると、目に自然な明るさの変わり方になる

def all_light(level):
    for i in range(len(leds)):
        light(i, level)

def blink(times=10):
    # 全部いっしょにチカチカ
    for _ in range(times):
        all_light(100)
        time.sleep(0.4)
        all_light(0)
        time.sleep(0.4)

def chase(rounds=5):
    # 1つずつ順番に点ける
    for _ in range(rounds):
        for i in range(len(leds)):
            all_light(0)
            light(i, 100)
            time.sleep(0.1)
    all_light(0)

def fade(times=3):
    # ふわっと明るくして、ふわっと消す
    for _ in range(times):
        for level in range(0, 101, 2):
            all_light(level)
            time.sleep(0.02)
        for level in range(100, -1, -2):
            all_light(level)
            time.sleep(0.02)

def twinkle(seconds=15):
    # ランダムにきらきら
    levels = [0] * len(leds)
    end = time.ticks_add(time.ticks_ms(), seconds * 1000)
    while time.ticks_diff(end, time.ticks_ms()) > 0:
        if random.randint(1, 100) <= 20:                  # 5回に1回くらい
            levels[random.randint(0, len(leds) - 1)] = 100
        for i in range(len(leds)):
            levels[i] = levels[i] * 9 // 10              # 少しずつ暗くする
            light(i, levels[i])
        time.sleep(0.03)
    all_light(0)

while True:
    blink()
    chase()
    fade()
    twinkle()
```

| 関数 | 光り方 |
| --- | --- |
| `blink()` | 全部いっしょにチカチカ |
| `chase()` | 1つずつ順番に点ける |
| `fade()` | ふわっと明るくして、ふわっと消す |
| `twinkle()` | ランダムにきらきら |

- 明るさは **PWM**（7章）で変えます。`duty_u16()` に 0〜65535 を入れると、0 で消え、65535 でいちばん明るくなります
- `light()` は、0〜100 の明るさを2乗してから `duty_u16()` の値にします。比例させると、暗いところで急に明るくなって見えるためです
- 最後の `while True:` が、4つの光り方を順番にくり返します（1周35秒くらい）

### 光り方を変える

| 変えたいこと | 直すところ |
| --- | --- |
| LED の光る順番 | `PINS` の並び（`[9, 8, 7, 6, 5, 4, 3, 2, 1, 0]` で逆向き） |
| 速さ | `time.sleep()` の秒数 |
| くり返す回数 | `blink(20)` のように、かっこの中の数 |
| 光り方の順番 | 最後の `while True:` の中の並び |

## 書き込んで電池で動かす

```bash
mpremote run main.py           # 試す（止めるときは Ctrl + C）
mpremote cp main.py :main.py   # ピコに保存する
```

1. `mpremote run main.py` で光り方を確かめる
2. `mpremote cp main.py :main.py` でピコに保存する。main.py は、電源が入ると自動で動きます
3. USB を抜いて、電池ボックスのスイッチを入れる

Pico Studio の「▶ 実行」と「ピコに保存」でも同じことができます（付録E）。

> USB をつなぐときは、電池のスイッチを切ってください。両方つなぐと、USB の電気が電池に流れこむことがあります。

アルカリの単3なら、40〜50時間くらい光ります（毎晩4時間で10日ほど）。

## まとめ

- LED は1つずつ抵抗をはさんで GP0〜GP9 につなぎ、短い足は GND にまとめる
- 抵抗は、赤・黄が 330Ω、緑・青・白が 100Ω
- 明るさは PWM の `duty_u16()`（0〜65535）で変える
- main.py として保存すると、電池のスイッチを入れるだけで光る
- 電池は VSYS（1.8〜5.5V）へ。USB をつなぐときは電池のスイッチを切る

## 練習問題

```quiz
Q: 赤い LED につなぐ抵抗は何 Ω ですか。
A: 330
E: 赤・黄は 330Ω、緑・青・白は 100Ω です。

Q: 電池ボックスの赤い線（＋）をつなぐ、ピコのピンの名前は何ですか。
A: VSYS
E: 39番ピンです。1.8〜5.5V を入れられます。

Q: LED の長い足は、プラスとマイナスのどちらですか。
A: プラス | ＋ | アノード
E: 長い足（＋）を抵抗の側に、短い足（−）を GND の側にします。

Q: `duty_u16()` に入れる値で、いちばん明るくなる数はいくつですか。
A: 65535
E: 0 で消え、65535 でいちばん明るくなります。

Q: 単3のアルカリ電池を3本つなぐと、何 V になりますか。
A: 4.5
E: 1.5V × 3本 = 4.5V です。VSYS の 5.5V までに入っています。
```
