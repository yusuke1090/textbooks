# 付録I. 安いカメラの写真を PC に映す

アリエクで買える OV7670 のカメラ（300円くらい）をピコにつなぎ、撮った写真を USB で PC に送って、窓に映します。
写真は保存もできるので、あとでカラスを機械学習で見分けるとき（付録H の #6）の材料になります。

## 全体の形

```text
カメラ（OV7670）  撮って、点ごとの色を数にする
   │ 18本の線
   ▼
ピコ              PC に頼まれたら1枚送る
   │ USB
   ▼
PC                窓に映す・保存する
```

ピコはメモリが 264KB しかないので、写真を受け取って送るだけにします。320×240 の写真1枚で、そのうち 150KB を使います。見分ける（機械学習）のは PC の仕事です。

## カメラを選ぶ

| カメラ | 値段の目安 | ちがい |
| --- | --- | --- |
| **OV7670（18ピン）** | 200〜500円 | この付録で使う。いちばん安い。30万画素。JPEG にできないので、色の数をそのまま送る |
| OV2640（18ピン） | 500〜1,500円 | 200万画素。カメラの中で JPEG にするので、大きい写真も速く送れる |
| ESP32-CAM | 1,000〜2,000円 | カメラと Wi-Fi のマイコンが1枚。ピコを使わずブラウザに映せるが、技適のない物が多い |

値段は 2026年11月のアリエクの目安です。カラスがいるかどうかを見分けるだけなら、30万画素で足ります（機械学習では、写真を 96×96 くらいに小さくして使います）。いちばん安い OV7670 にします。

![ESP32-CAM（OV2640 が細い帯の線でつながっている）](images/esp32-cam.jpg)

### 買うときに見ること

アリエクで **OV7670 camera module** と検索します。

- 写真で、**2列×9本（18本）のピン**が立っていること。**FIFO 付き**（裏に「AL422B」という大きいチップがあり、ピンが 22本）は別の物で、この付録のプログラムでは動きません
- **3.3V** で動くこと

## 用意するもの

| もの | 数 | メモ |
| --- | --- | --- |
| OV7670 カメラ（18ピン・FIFO なし） | 1個 | アリエク |
| ピコ | 1枚 | いまの RP2040 のもの。無線はいらない |
| ブレッドボード | 1枚 | 付録G のもの |
| ジャンパーワイヤー（オス-メス） | 18本 | メスをカメラのピンに、オスをブレッドボードに差す。10cm がよい（長いと写真が乱れやすい） |
| USB ケーブル | 1本 | 付録G のもの |

オス-メスのワイヤーもアリエクで買えます（**dupont wire male female 10cm**、40本で 200円くらい）。

## 配線

### 線の役目

![カメラの中のイメージセンサー（OV7670）。光を受けて、点ごとの明るさを数にする](images/image-sensor.jpg)

| 線 | 役目 |
| --- | --- |
| 3.3V・GND | 電源 |
| SIOC・SIOD | カメラの設定を書き込む。I2C と同じしくみ（11章） |
| XCLK | ピコからカメラに送る時計（1秒に1000万回）。これがないとカメラは動かない |
| VSYNC・HREF・PCLK | 「写真の始まり」「行の始まり」「次の1バイト」の合図 |
| D0〜D7 | 写真のデータ。8本で1回に1バイト送る |
| RESET・PWDN | やり直しと電源オフ。使わないので、RESET は 3.3V、PWDN は GND につなぐ |

ピコは PIO（ピンを速く読むための小さな回路）で、PCLK の合図ごとに D0〜D7 を読み取ります。PIO を動かすのは、あとで入れるライブラリです。

### つなぐ

![カメラとピコの配線](images/camera-wiring.svg)

| カメラ | ピコ | ピンの番号 |
| --- | --- | --- |
| 3.3V | 3V3(OUT) | 36番 |
| GND | GND | 38番 |
| SIOC | GP13 | 17番 |
| SIOD | GP12 | 16番 |
| VSYNC | GP2 | 4番 |
| HREF | GP3 | 5番 |
| PCLK | GP4 | 6番 |
| XCLK | GP5 | 7番 |
| D0〜D3 | GP14〜GP17 | 19・20・21・22番 |
| D4〜D7 | GP18〜GP21 | 24・25・26・27番 |
| RESET | 3V3(OUT) | 36番 |
| PWDN | GND | 38番 |

1. USB を外しておく
2. ピコをブレッドボードに差す（付録G と同じ。真ん中の溝をまたぐ）
3. カメラの基板に書いてある名前を見て、ワイヤーのメスを差す
4. オスは、表のピンの番号と**同じ縦の列**の、空いている穴に差す。上の列（1〜20番）は a・b、下の列（21〜40番）は i・j の穴が空いています
5. RESET は 36番の列、PWDN は 38番の列に差す。同じ縦の列に2本入って大丈夫です（中でつながっています）

![動画: カメラとピコの配線と、書き込んで確かめるまで](videos/camera-wiring.mp4)

- D0〜D7 は、**続いた8本**（GP14〜GP21）にしてください。ライブラリの決まりです
- レンズに保護フィルムが貼ってあれば、はがします

## プロジェクトを作る

1. VS Code の拡張機能「Raspberry Pi Pico」で **New C/C++ Project** を開く（4章）。名前は `camera`、場所は `~/apps`、**Console over USB** と **Generate C++ code** に ☑ して作る
2. VS Code のターミナルで、カメラのライブラリ [PicoCamera](https://github.com/umeiko/PicoCamera) をプロジェクトの中にダウンロードする

```bash
cd ~/apps/camera
git clone --depth 1 --branch 0.4.2 https://github.com/umeiko/PicoCamera.git
```

`Cloning into 'PicoCamera'...` のあとに `You are in 'detached HEAD' state.` と出ますが、版を 0.4.2 に決めてダウンロードしたためで、問題ありません。`ls PicoCamera` で `CMakeLists.txt` と `src` が見えれば成功です。

3. `CMakeLists.txt` に2か所足す（`target_link_libraries` の上に1行と、その中に `pico_camera`）

```cmake
add_subdirectory(PicoCamera)

target_link_libraries(camera
        pico_stdlib
        pico_camera)
```

| 足した行 | 意味 |
| --- | --- |
| `add_subdirectory(PicoCamera)` | `PicoCamera` フォルダの中の `CMakeLists.txt` も読んで、ライブラリをビルドする |
| `pico_camera` | そのライブラリを `camera` のプログラムで使う |

## 配線を確かめる

USB で PC につなぎます。`camera.cpp` の中身を次のプログラムにして、**Compile → Run (USB)** で書き込みます。初めての Compile は、ライブラリもビルドするので少し長くかかります。

```cpp
#include <cstdio>
#include "pico/stdlib.h"
#include "PicoCamera.h"

// カメラのつなぎ方（配線の表と同じ GP の番号）
camera_config_t camera_config() {
    camera_config_t c = {};
    c.pin_sccb_sda = 12;               // SIOD
    c.pin_sccb_scl = 13;               // SIOC
    c.pin_vsync = 2;
    c.pin_href = 3;
    c.pin_pclk = 4;
    c.pin_xclk = 5;
    c.pin_d0 = 14; c.pin_d1 = 15; c.pin_d2 = 16; c.pin_d3 = 17;   // D0〜D7 は GP14〜GP21（続いた8本）
    c.pin_d4 = 18; c.pin_d5 = 19; c.pin_d6 = 20; c.pin_d7 = 21;
    c.pin_reset = -1;                  // RESET は 3.3V、PWDN は GND につないだので、
    c.pin_pwdn = -1;                   // ピコからは動かさない
    c.xclk_freq_hz = 10000000;         // カメラに送る時計（10MHz）
    c.sccb_i2c_port = 0;               // GP12・GP13 は I2C0
    c.pixel_format = PIXFORMAT_RGB565; // 1つの点の色を2バイトで送る
    c.frame_size = FRAMESIZE_QVGA;     // 320×240
    c.fb_count = 1;
    return c;
}

// 写真の明るさ（0〜255）。全部の点の、緑の平均
int brightness(const camera_fb_t *fb) {
    size_t n = fb->len / 2;                                         // 点の数（1つの点が2バイト）
    uint32_t sum = 0;
    for (size_t i = 0; i < n; i++) {
        uint16_t px = (fb->buf[2 * i] << 8) | fb->buf[2 * i + 1];   // 上の桁のバイトが先に来る
        sum += (px >> 5) & 0x3F;                                    // 緑（0〜63）
    }
    return (int)(sum * 255 / (63 * n));
}

int main() {
    stdio_init_all();
    sleep_ms(3000);                    // Serial Monitor がつながるのを待つ
    camera_config_t config = camera_config();
    pico_camera_err_t err = pico_camera_init(&config);
    while (err != PICO_CAMERA_OK) {
        printf("カメラの準備に失敗: %s\n", pico_camera_err_str(err));
        sleep_ms(1000);
    }
    printf("カメラ: %s\n", pico_camera_sensor_info_get()->name);
    while (true) {
        camera_fb_t *fb = pico_camera_fb_get();
        if (fb == nullptr) {
            printf("撮れなかった\n");
        } else {
            printf("%u×%u の写真 %u バイト  明るさ %d\n",
                   (unsigned)fb->width, (unsigned)fb->height, (unsigned)fb->len, brightness(fb));
            pico_camera_fb_return(fb);
        }
        sleep_ms(1000);
    }
}
```

- `pico_camera_init()` が、カメラを探して設定し、写真を入れる場所（153,600 バイト）をメモリにとります
- `pico_camera_fb_get()` で1枚撮り、使い終わったら `pico_camera_fb_return()` で場所を返します。返さないと、次の1枚が撮れません
- `PIXFORMAT_RGB565` は、1つの点の色を2バイト（16ビット）で表す形です。赤5ビット・緑6ビット・青5ビットで、上の桁のバイトが先に来ます。320×240 なら 320×240×2 = 153,600 バイトです
- `brightness()` は、全部の点の緑（0〜63）の平均を 0〜255 にします。緑は、人の目が明るさをいちばん強く感じる色です

### Serial Monitor の読み方

うまくいくと、1秒ごとに写真の大きさと明るさが出ます（明るさの数は例です）。

```text
カメラ: OV7670
320×240 の写真 153600 バイト  明るさ 118
320×240 の写真 153600 バイト  明るさ 121
320×240 の写真 153600 バイト  明るさ 6      ← レンズを手でふさいだ
```

バイト数は、写すものが変わってもいつも 153600 です（JPEG のように小さくしないため）。配線が合っているかは**明るさ**で見ます。レンズを手でふさいで数が小さくなり、手を離すと戻れば成功です。

| 出たもの | 原因と直し方 |
| --- | --- |
| `カメラの準備に失敗: no sensor detected on the SCCB bus (check wiring/power)` | カメラと話せない。3.3V・GND・SIOC（GP13）・SIOD（GP12）・XCLK（GP5）を確かめる。SIOC と SIOD の入れ違いが多い。配線が合っていてもこれが出るときは、SIOC と SIOD を、それぞれ 4.7kΩ〜10kΩ の抵抗で 3.3V の列につなぐ |
| `カメラの準備に失敗: not supported (e.g. JPEG on a sensor without a JPEG encoder)` | `c.pixel_format` が `PIXFORMAT_JPEG` になっている。OV7670 は JPEG を作れないので、`PIXFORMAT_RGB565` にする |
| `カメラの準備に失敗: invalid argument (check pins, pixel_format, frame_size)` | プログラムのピンの番号が違う。D0〜D7 は続いた8本、SIOD は偶数の GP |
| `撮れなかった` がくり返し出る | VSYNC・HREF・PCLK のどれかが抜けている |
| 明るさが、手でふさいでも変わらない | D0〜D7 のどれかが抜けているか、順番が違う |
| `カメラ: OV7670` のあと何も出ない | 写真が大きすぎて、メモリが足りずにピコが止まった。`c.frame_size` を `FRAMESIZE_QVGA` にする |

## PC に映す

### ピコのプログラム

`camera.cpp` の中身を次のプログラムに入れかえて、**Compile → Run (USB)** で書き込みます。`camera_config()` は上と同じです。

```cpp
#include <cstdio>
#include "pico/stdlib.h"
#include "PicoCamera.h"

// カメラのつなぎ方（配線の表と同じ GP の番号）
camera_config_t camera_config() {
    camera_config_t c = {};
    c.pin_sccb_sda = 12;               // SIOD
    c.pin_sccb_scl = 13;               // SIOC
    c.pin_vsync = 2;
    c.pin_href = 3;
    c.pin_pclk = 4;
    c.pin_xclk = 5;
    c.pin_d0 = 14; c.pin_d1 = 15; c.pin_d2 = 16; c.pin_d3 = 17;   // D0〜D7 は GP14〜GP21（続いた8本）
    c.pin_d4 = 18; c.pin_d5 = 19; c.pin_d6 = 20; c.pin_d7 = 21;
    c.pin_reset = -1;                  // RESET は 3.3V、PWDN は GND につないだので、
    c.pin_pwdn = -1;                   // ピコからは動かさない
    c.xclk_freq_hz = 10000000;         // カメラに送る時計（10MHz）
    c.sccb_i2c_port = 0;               // GP12・GP13 は I2C0
    c.pixel_format = PIXFORMAT_RGB565; // 1つの点の色を2バイトで送る
    c.frame_size = FRAMESIZE_QVGA;     // 320×240
    c.fb_count = 1;
    return c;
}

int main() {
    stdio_init_all();
    camera_config_t config = camera_config();
    pico_camera_err_t err = pico_camera_init(&config);
    while (true) {
        int ch = getchar_timeout_us(100000);           // PC からの1文字を待つ（0.1秒ごと）
        if (ch != 'c') continue;                       // c が来たら1枚撮る
        if (err != PICO_CAMERA_OK) {
            printf("ERR %s\n", pico_camera_err_str(err));
            continue;
        }
        camera_fb_t *fb = pico_camera_fb_get();
        if (fb == nullptr) {
            printf("ERR 撮れなかった\n");
            continue;
        }
        printf("RGB %u %u\n", (unsigned)fb->width, (unsigned)fb->height);   // 1行目: 写真の幅と高さ
        stdio_put_string((const char *)fb->buf, (int)fb->len, false, false);   // 写真をそのまま送る
        stdio_flush();
        pico_camera_fb_return(fb);
    }
}
```

PC が `c` を1文字送ると、ピコは次の形で1枚返します。

```text
RGB 320 240        ← 1行目: 写真の幅と高さ
（色のデータ 320×240×2 = 153600 バイト）
```

- 先に幅と高さを送るので、PC は「幅×高さ×2」バイトを読めば1枚が終わったとわかります
- `printf()` は `\n` を `\r\n` に変えて送ります。写真のデータの中にも `\n` と同じ値があるので、写真は変えずに送る `stdio_put_string()` を使います（最後の `false` が「変えない」）
- PC が頼んだときだけ撮るので、PC の処理（あとの機械学習）が遅くても、写真がたまりません

### PC のプログラム

OpenCV（写真を扱う Python のライブラリ）を入れます。pyserial は3章で入れています。

```bash
sudo apt install python3-opencv
```

次のプログラムを `~/apps/camera/camera_view.py` という名前で保存します。

```python
# camera_view.py  ― 使い方: python3 camera_view.py
import os, time
import cv2
import numpy as np
import serial

PORT = "/dev/ttyACM0"
SAVE_DIR = "photos"     # s を押した写真を入れるフォルダ
AUTO_SAVE = 0           # 何秒ごとに自動で保存するか（0 なら自動では保存しない）
SCALE = 2               # 窓に映すときの倍率（320×240 は小さいので2倍）


def to_image(data, w, h):
    """RGB565（1つの点が2バイト）を、OpenCV の画像（点ごとに 青・緑・赤 の 0〜255）にする"""
    px = np.frombuffer(data, ">u2").reshape(h, w)     # 2バイトずつ。上の桁のバイトが先
    r = ((px >> 11) & 0x1F) << 3                       # 赤 5ビット
    g = ((px >> 5) & 0x3F) << 2                        # 緑 6ビット
    b = (px & 0x1F) << 3                               # 青 5ビット
    return np.dstack([b, g, r]).astype(np.uint8)


def get_photo(ser):
    """ピコに c を送って、写真を1枚受け取る。だめなら None"""
    ser.write(b"c")
    while True:
        line = ser.readline().decode(errors="replace").strip()
        if line == "":
            print("ピコから返事がありません。camera.cpp を書き込んだか確かめてください")
            return None
        if line.startswith("RGB "):
            w, h = map(int, line.split()[1:])
            data = ser.read(w * h * 2)
            if len(data) < w * h * 2:
                print("写真が途中で切れました")
                return None
            return to_image(data, w, h)
        print("ピコ:", line)            # ERR … などの知らせ
        if line.startswith("ERR"):
            return None


def save(img):
    name = time.strftime(f"{SAVE_DIR}/%Y%m%d_%H%M%S.jpg")
    cv2.imwrite(name, img)
    print("保存しました:", name)


ser = serial.Serial(PORT, 115200, timeout=3)
ser.reset_input_buffer()
os.makedirs(SAVE_DIR, exist_ok=True)
print("s で保存、q で終了")
count, start, last_save = 0, time.time(), time.time()
while True:
    img = get_photo(ser)
    if img is None:
        time.sleep(1)
        continue
    cv2.imshow("camera", cv2.resize(img, None, fx=SCALE, fy=SCALE, interpolation=cv2.INTER_NEAREST))
    count += 1
    if time.time() - start >= 5:                # 5秒ごとに速さを出す
        print(f"{img.shape[1]}×{img.shape[0]}  1秒に {count / (time.time() - start):.1f} 枚")
        count, start = 0, time.time()
    key = cv2.waitKey(1) & 0xFF
    if key == ord("s") or (AUTO_SAVE and time.time() - last_save >= AUTO_SAVE):
        save(img)
        last_save = time.time()
    elif key == ord("q"):
        break
ser.close()
cv2.destroyAllWindows()
```

| ところ | すること |
| --- | --- |
| `get_photo()` | `c` を送り、`RGB 320 240` の行を待って、幅×高さ×2 バイト読む。`ERR` の行が来たら、そのまま表示する |
| `to_image()` | 2バイトずつの色（RGB565）から赤・緑・青を取り出し、それぞれ 0〜255 に広げて、OpenCV の画像（点ごとの色の表）にする |
| `cv2.resize()` | 320×240 は PC の画面では小さいので、`SCALE` 倍にする |
| `cv2.imshow()` | `camera` という窓に映す |
| `cv2.waitKey(1)` | 窓を描き直し、押されたキーを受け取る。これがないと窓が固まる |
| `cv2.imwrite()` | 写真を JPEG のファイルにして保存する（名前が `.jpg` なので JPEG になる） |

### 動かす

1. VS Code の Serial Monitor を止める（Pico Studio を使っていたら「切断」）。同じポートは1つのソフトしか使えません
2. ターミナルで実行する

```bash
cd ~/apps/camera
python3 camera_view.py
```

3. `camera` という窓が開いて、写真が次々に映る。窓を選んだ状態で **s** を押すと保存、**q** で終わる

うまくいくと、ターミナルに次のように出ます（1秒の枚数は例です）。

```text
s で保存、q で終了
320×240  1秒に 2.0 枚
保存しました: photos/20261124_093015.jpg
```

1枚 150KB を USB で送るので、1秒に 2枚くらいです。もっと速くしたいときは、下の「変えたいとき」で写真を小さくします。

| 出たもの | 原因と直し方 |
| --- | --- |
| `could not open port /dev/ttyACM0: [Errno 16] Device or resource busy` | Serial Monitor か Pico Studio がポートを使っている。止める |
| `could not open port /dev/ttyACM0: [Errno 2] No such file or directory` | ピコがつながっていない。USB ケーブルを確かめる |
| `ModuleNotFoundError: No module named 'cv2'` | OpenCV がない。`sudo apt install python3-opencv` |
| `ピコから返事がありません` | ピコに `camera.cpp`（PC に映すほう）が入っていない。書き込み直す |
| `ピコ: 320×240 の写真 153600 バイト  明るさ 118` が流れる | 配線を確かめるプログラムのまま。PC に映すほうを書き込む |
| `ピコ: ERR no sensor detected …` | カメラと話せない。Serial Monitor の表と同じように配線を見る |
| 色がおかしい・しま模様になる | D0〜D7 の順番が違う。配線の表と同じか確かめる |
| 写真が白っぽい・ぼやける | レンズの保護フィルムをはがす。レンズを少し回すとピントが合う |

### できるファイル

| ファイル | できるとき・中身 |
| --- | --- |
| `PicoCamera/` | `git clone` したとき。カメラを動かすライブラリ（C++ のソース） |
| `build/camera.uf2` | Compile したとき。ピコに書き込むプログラム（4章） |
| `camera_view.py` | 自分で保存したとき。PC で動かすプログラム |
| `photos/20261124_093015.jpg` | **s** を押したとき（`AUTO_SAVE` を決めたら、その秒ごと）。撮った写真。名前は日付と時刻 |

### 変えたいとき

| 変えたいこと | 直すところ |
| --- | --- |
| 写真の大きさ | `camera.cpp` の `c.frame_size`。`FRAMESIZE_QQVGA`（160×120。データが 1/4 なので、1秒の枚数が増える）か `FRAMESIZE_QVGA`（320×240）。`FRAMESIZE_VGA`（640×480）はメモリが足りず、ピコが止まる |
| 自動で保存 | `camera_view.py` の `AUTO_SAVE = 10`（10秒ごと） |
| 窓の大きさ | `camera_view.py` の `SCALE`（3 なら3倍） |
| 上下が逆 | 下のコードを、`camera.cpp` の `pico_camera_init()` の次の行に足す |

```cpp
    if (err == PICO_CAMERA_OK) {
        sensor_t *s = pico_camera_sensor_get();
        s->set_vflip(s, 1);                        // 上下を反対にする（左右は set_hmirror）
    }
```

## カラスを見分ける材料にする

![カラス](images/h-crow.jpg)

- 窓ぎわなど、カラスの来る所にカメラを向けて `AUTO_SAVE = 10` で動かすと、写真がたまります。カラスが写った写真と、写っていない写真をフォルダに分けると、学習のラベルになります（17章）
- 見分けるプログラムは、`get_photo()` で受け取った `img` を、学習したモデルに渡す形になります。ピコの側は、このまま変えません
- 牛舎で使うときは、PC の代わりに付録H のラズパイに USB でつなぎます。`camera_view.py` はラズパイでもそのまま動きます

## まとめ

- カメラは OV7670 の18ピン（FIFO なし）の基板。いちばん安く、30万画素。JPEG にできないので、320×240 の色の数（153,600 バイト）をそのまま送る
- 線は18本。D0〜D7 は続いた8本（GP14〜GP21）、SIOC・SIOD は I2C0（GP13・GP12）、XCLK は GP5 からの 10MHz の時計
- ライブラリは PicoCamera を `git clone` し、`CMakeLists.txt` に `add_subdirectory(PicoCamera)` と `pico_camera` を足す
- 配線を確かめるプログラムで、レンズを手でふさぐと明るさの数が小さくなれば、配線は合っている
- PC が `c` を送ると、ピコは `RGB 幅 高さ` の行と色のデータを返す。データは `stdio_put_string()` で変えずに送る
- PC の `camera_view.py` が色の数を画像に戻して窓に映し、**s** で `photos/` に保存する。集めた写真がカラスの学習の材料になる

## 練習問題

```quiz
Q: この付録の配線で、カメラの D0 をつなぐピコのピンは GP 何番ですか。
A: 14 | GP14
E: D0〜D7 を GP14〜GP21 の続いた8本につなぎます。続いていないと、ライブラリが読めません。

Q: ピコからカメラに送る時計の線は、カメラの何というピンにつなぎますか。
A: XCLK
E: GP5 から 10MHz を送ります。これがないとカメラは動かず、`no sensor detected` になります。

Q: 320×240 の写真を RGB565（1つの点が2バイト）で送ると、何バイトですか。
A: 153600 | 153,600 | 153600バイト | 153,600バイト
E: 320×240×2 = 153,600 バイトです。OV7670 は JPEG にできないので、写すものが変わってもこの大きさです。

Q: `camera_view.py` で、写真を保存するキーは何ですか。
A: s
E: `photos/` フォルダに、日付と時刻の名前で保存します。終わるのは q です。

Q: `camera_view.py` で `Device or resource busy` と出ました。先に止めるのは VS Code の何ですか。
A: Serial Monitor | シリアルモニター | Serial Monitor のタブ
E: 同じポートは1つのソフトしか使えません。Pico Studio も「切断」します。
```
