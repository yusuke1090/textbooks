# 付録G. クリスマスのイルミネーションを作る

ふつうの LED を10個ピコにつないで、チカチカ・順番に点灯・ふわっと・きらきらと光らせます。
プログラムは C++ で書き、VS Code で書き込んで（4章）、電池で動かします。

![LED のクリスマスツリー](images/xmas-tree.jpg)

## 用意するもの

| もの | 数 | メモ |
| --- | --- | --- |
| LED（5mm） | 10個 | 赤・緑・黄・青・白を2個ずつ |
| 抵抗 330Ω | 4本 | 赤・黄の LED 用 |
| 抵抗 100Ω | 6本 | 緑・青・白の LED 用 |
| ブレッドボード | 1枚 | 830穴 |
| ジャンパーワイヤー（オス-オス） | 11本 | やわらかい線。遠い LED まで届く長さのもの |
| ピンヘッダ | 20ピン×2本 | ピコに付いてくることが多い。はんだ付けは7章 |
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

![イルミネーションの回路図](images/xmas-sch.svg)

1. USB と電池を外しておく
2. ピコを右はしに、USB を右に向けて、真ん中の溝をまたいで差す
3. 抵抗を、真ん中の溝をまたいで差す。左から GP0、GP1 … の順に、2列ずつあけて10本
4. LED の長い足（＋）を抵抗の下の列に、短い足（−）を青い線（−）の列に差す
5. ジャンパーワイヤーで、ピコの GP0〜GP9 の列と、抵抗の上の列をつなぐ。GP0 がいちばん左の LED
6. ピコの GND（38番）の列と、青い線（−）の列をワイヤーでつなぐ
7. 電池ボックスのスイッチを切ったまま、赤い線を VSYS（39番）の列に、黒い線を青い線（−）の列に差す

電池ボックスの線の先が細いより線なら、はんだで固めてから差すと抜けにくくなります。

## VS Code でプロジェクトを作る

1. VS Code の左のピコのアイコンを押し、Quick Access の **New C/C++ Project** を押す（4章）
2. 開いた画面を、写真の番号のとおりに設定する

![New C/C++ Project の画面（番号は下の表。この写真は ④⑤ に ☑ する前）](images/xmas-new-project.png)

| 番号 | 項目 | 設定 |
| --- | --- | --- |
| ① | Name | `xmas` と打つ。`xmas.cpp` や `xmas.uf2` の名前になる |
| ② | Board type | **Pico** のまま。Pico 2 なら **Pico 2**、Pico W なら **Pico W** |
| ③ | Location | **Change** を押し、ホームの中の `apps` フォルダを選ぶ。`/home/ユーザー名/apps` と出ればよい |
| ④ | Console over USB | ☑ する。`printf` が PC に届き、次の書き込みで BOOT ボタンを押さずにすむ |
| ⑤ | Generate C++ code | ☑ する。☐ のままだと `xmas.c`（C 言語）ができる |

番号のないところ（Pico SDK version、Features、☑ ずみの Use project name as entry point file name、いちばん下の Debugger）は、そのままにします。PWM は Features にないので、手順4で足します。

3. いちばん下の **Create** を押す。VS Code が `~/apps/xmas` を開き直し、左に `xmas.cpp` と `CMakeLists.txt` が出れば成功（初めてのときは SDK のダウンロードで数分かかる）
4. 明るさを変える PWM を使うので、`CMakeLists.txt` の `target_link_libraries` に `hardware_pwm` を足す（5章）

```cmake
target_link_libraries(xmas
        pico_stdlib
        hardware_pwm)
```

## 配線を確かめる

USB で PC につなぎ（電池のスイッチは切ったまま）、LED が1つずつ光るか確かめます。`xmas.cpp` の中身を次のプログラムにして、**Compile → Run (USB)** で書き込みます。

```cpp run
#include <cstdio>
#include "pico/stdlib.h"

int main() {
    stdio_init_all();
    sleep_ms(1500);                     // Serial Monitor がつながるのを待つ
    for (uint n = 0; n < 10; n++) {     // GP0〜GP9 を出力にする
        gpio_init(n);
        gpio_set_dir(n, GPIO_OUT);
    }
    while (true) {
        for (uint n = 0; n < 10; n++) {
            printf("GP%u が光っているはず\n", n);
            gpio_put(n, 1);
            sleep_ms(1000);
            gpio_put(n, 0);
        }
        printf("1周おわり\n");
    }
}
```

Serial Monitor に、いま光っているはずの GP の番号が出ます。光らない LED があれば、LED の向き（長い足が抵抗の側）と、ワイヤーを差した列を確かめてください。

## イルミネーションのプログラム

`xmas.cpp` の中身を次のプログラムに入れかえて、**Compile → Run (USB)** で書き込みます。

```cpp run
#include <cstdlib>
#include "pico/stdlib.h"
#include "hardware/pwm.h"

constexpr uint PINS[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};   // LED をつないだ GP の番号（光る順）
constexpr int N = sizeof(PINS) / sizeof(PINS[0]);

// i 番目の LED を、0〜100 の明るさにする
void light(int i, int level) {
    pwm_set_gpio_level(PINS[i], level * level / 10);   // 0〜1000。2乗すると、目に自然な明るさの変わり方になる
}

void all_light(int level) {
    for (int i = 0; i < N; i++) light(i, level);
}

// 全部いっしょにチカチカ
void blink(int times = 10) {
    for (int k = 0; k < times; k++) {
        all_light(100);
        sleep_ms(400);
        all_light(0);
        sleep_ms(400);
    }
}

// 1つずつ順番に点ける
void chase(int rounds = 5) {
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < N; i++) {
            all_light(0);
            light(i, 100);
            sleep_ms(100);
        }
    }
    all_light(0);
}

// ふわっと明るくして、ふわっと消す
void fade(int times = 3) {
    for (int k = 0; k < times; k++) {
        for (int level = 0; level <= 100; level += 2) { all_light(level); sleep_ms(20); }
        for (int level = 100; level >= 0; level -= 2) { all_light(level); sleep_ms(20); }
    }
}

// ランダムにきらきら
void twinkle(int seconds = 15) {
    int levels[N] = {};
    absolute_time_t end = make_timeout_time_ms(seconds * 1000);
    while (!time_reached(end)) {
        if (rand() % 100 < 20) levels[rand() % N] = 100;   // 5回に1回くらい
        for (int i = 0; i < N; i++) {
            levels[i] = levels[i] * 9 / 10;                // 少しずつ暗くする
            light(i, levels[i]);
        }
        sleep_ms(30);
    }
    all_light(0);
}

int main() {
    stdio_init_all();
    for (uint pin : PINS) {
        gpio_set_function(pin, GPIO_FUNC_PWM);         // PWM 用にする（9章）
        uint slice = pwm_gpio_to_slice_num(pin);
        pwm_set_clkdiv(slice, 125.0f);                 // 125MHz ÷ 125 ÷ 1000 = 1kHz
        pwm_set_wrap(slice, 999);
        pwm_set_enabled(slice, true);
    }
    srand(time_us_32());                               // 乱数の種
    while (true) {
        blink();
        chase();
        fade();
        twinkle();
    }
}
```

| 関数 | 光り方 |
| --- | --- |
| `blink()` | 全部いっしょにチカチカ |
| `chase()` | 1つずつ順番に点ける |
| `fade()` | ふわっと明るくして、ふわっと消す |
| `twinkle()` | ランダムにきらきら |

- 明るさは **PWM**（9章）で変えます。1秒に1000回、点けたり消したりして、点いている時間の割合を `pwm_set_gpio_level()` で決めます。`wrap` が 999 なので、0 で消え、1000 でいちばん明るくなります
- `light()` は、0〜100 の明るさを2乗してから 0〜1000 にします。比例させると、暗いところで急に明るくなって見えるためです
- 2本の GP で1つの PWM の回路（スライス）を使うので、GP0〜GP9 は5つの回路を使います。同じ回路を2回設定しても問題ありません
- 最後の `while (true)` が、4つの光り方を順番にくり返します（1周35秒くらい）

### 光り方を変える

| 変えたいこと | 直すところ |
| --- | --- |
| LED の光る順番 | `PINS` の並び（`{9, 8, 7, 6, 5, 4, 3, 2, 1, 0}` で逆向き） |
| 速さ | `sleep_ms()` のミリ秒 |
| くり返す回数 | `blink(20)` のように、かっこの中の数 |
| 光り方の順番 | 最後の `while (true)` の中の並び |

直したら、もう一度 Compile → Run (USB) で書き込みます。

## 電池で動かす

1. Run (USB) で書き込んだプログラムは、ピコに残ります。電源が入ると、自動で動きます
2. USB を抜いて、電池ボックスのスイッチを入れる

> USB をつなぐときは、電池のスイッチを切ってください。両方つなぐと、USB の電気が電池に流れこむことがあります。

アルカリの単3なら、40〜50時間くらい光ります（毎晩4時間で10日ほど）。

## ツリーの木にかける

ブレッドボードの上で全部光るのを確かめたら、LED をボードから抜き、赤黒の2芯の線で延ばして枝にかけます。
ピコ・抵抗・電池はボードに残して、ツリーの根元に置きます。

![LED を線で延ばして木にかける](images/xmas-hang.svg)

| もの | 数 | メモ |
| --- | --- | --- |
| 赤黒の2芯の線（UL2468・24AWG） | 20m | 赤を長い足（＋）、黒を短い足（−）にする。AliExpress で買える |
| ジャンパーワイヤー（オス-オス 20cm） | 10本 | 半分に切って、オスの付いた線を20本作る。ボードに差す側に使う |
| ビニールテープ | 少し | はんだ付けした所を包む。熱収縮チューブがあれば、そのほうがきれい |
| ニッパー | 1本 | 線を切る・先をむく。なければはさみ |

1. USB を抜き、電池のスイッチを切る
2. ジャンパーワイヤーを10本、真ん中で切る。オスの付いた線が20本できるので、切った先を 5mm くらいむく
3. LED をかける枝を決めて、根元からその枝までの長さ＋20cm に、2芯の線を切る。20m を10本に分けるので、平均 2m までにする
4. 線の両はしで赤と黒を 3cm くらい裂いて分け、先を 5mm くらいむいて、中の細い線をねじる
5. 片方のはしの赤と黒に、オスの付いた線を1本ずつはんだ付けする
6. LED を1個ボードから抜く。長い足を 1cm くらいに切って赤を、次に短い足を切って黒をはんだ付けする
7. はんだ付けした所を1本ずつテープで包む。LED の側は、2本をいっしょにもう一度巻く。金具どうしがふれると、その LED は光りません
8. 赤の線のオスを抵抗の下の列（抜いた LED の長い足の穴）に、黒の線のオスを − の列に差す。1個ずつ作って抜いた所へ戻すと、LED の色と抵抗がずれません
9. 10個とも同じようにしたら、電池のスイッチを入れて全部光るか見る。光らない LED は、はんだが外れていないか、赤と黒が逆になっていないかを見る
10. LED を枝にかけて、線を枝に巻きつける。線は幹の近くを通して根元にまとめると、目立ちにくくなります

## まとめ

- LED は1つずつ抵抗をはさんで GP0〜GP9 につなぎ、短い足は GND にまとめる
- 抵抗は、赤・黄が 330Ω、緑・青・白が 100Ω
- プログラムは C++。PWM を使うので `CMakeLists.txt` に `hardware_pwm` を足し、Compile → Run (USB) で書き込む
- 明るさは `pwm_set_gpio_level()`（この付録では 0〜1000）で変える
- 書き込んだプログラムは、電池のスイッチを入れるだけで動く。電池は VSYS（1.8〜5.5V）へ、USB をつなぐときは電池を切る
- 木にかけるときは、LED の足に赤黒の2芯の線をはんだ付けして延ばし、ボード側には半分に切ったジャンパーのオスを付ける。ピコ・抵抗・電池は根元に置く

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

Q: PWM を使うために、`CMakeLists.txt` の `target_link_libraries` に足すライブラリは何ですか。
A: hardware_pwm
E: ADC なら `hardware_adc`、I2C なら `hardware_i2c` のように、使う機能のライブラリを足します（5章）。

Q: この付録のプログラム（`wrap` が 999）で、`pwm_set_gpio_level()` に入れていちばん明るくなる数はいくつですか。
A: 1000 | 999
E: 0 で消え、1000（`wrap` + 1）でずっと点いた状態になります。
```
