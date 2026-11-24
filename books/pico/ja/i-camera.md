# 付録I. 安いカメラの写真を PC に映す

アリエクで買える OV2640 のカメラ（1,000円くらい）をピコにつなぎ、撮った写真を USB で PC に送って、窓に映します。
写真は保存もできるので、あとでカラスを機械学習で見分けるとき（付録H の #6）の材料になります。

## 全体の形

```text
カメラ（OV2640）  撮って JPEG にする
   │ 18本の線
   ▼
ピコ              PC に頼まれたら1枚送る
   │ USB
   ▼
PC                窓に映す・保存する
```

ピコはメモリが 264KB しかないので、写真を受け取って送るだけにします。見分ける（機械学習）のは PC の仕事です。

## カメラを選ぶ

| カメラ | 値段の目安 | ちがい |
| --- | --- | --- |
| **OV2640（18ピン）** | 500〜1,500円 | この付録で使う。200万画素。カメラの中で JPEG にするので、USB でも速く送れる |
| OV7670 | 200〜400円 | いちばん安い。30万画素で、JPEG にできない。この付録のプログラムでは動かない |
| ESP32-CAM | 1,000〜2,000円 | カメラと Wi-Fi のマイコンが1枚。ピコを使わずブラウザに映せるが、技適のない物が多い |

値段は 2026年11月のアリエクの目安です。カラスを見分けるには写真のきれいさが大事なので、OV2640 にします。

![ESP32-CAM（OV2640 が細い帯の線でつながっている）](images/esp32-cam.jpg)

### 買うときに見ること

アリエクで **OV2640 camera module 18pin** と検索します。

- 写真で、**2列×9本（18本）のピン**が立っていること。細い帯の線（FPC）だけの OV2640 は、カメラ用の電源の回路がないので、ピコに直接つなげません
- **3.3V** で動くこと
- レンズは**ふつうの画角（60〜70°）**。120°・160° の広角は、端がゆがみます。「Night Vision」「850nm」と書いてあるものは赤外線を通すので、昼の色が赤っぽくなります

## 用意するもの

| もの | 数 | メモ |
| --- | --- | --- |
| OV2640 カメラ（18ピン） | 1個 | アリエク |
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
3. カメラの基板に書いてある名前を見て、ワイヤーのメスを差す。オスは、ピコの同じ番号のピンの列（横に並んだ穴）に差す
4. RESET は 36番の列、PWDN は 38番の列に差す。同じ列に2本入って大丈夫です

- D0〜D7 は、**続いた8本**（GP14〜GP21）にしてください。ライブラリの決まりです
- データの線の名前が **D2〜D9** の基板もあります。そのときは D2 を GP14、D3 を GP15 … D9 を GP21 につなぎます
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
    c.pixel_format = PIXFORMAT_JPEG;
    c.frame_size = FRAMESIZE_VGA;      // 640×480
    c.jpeg_quality = 12;               // 0〜63。小さいほどきれいで、データが大きい
    c.fb_count = 1;
    return c;
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
            bool jpeg = fb->len > 2 && fb->buf[0] == 0xFF && fb->buf[1] == 0xD8;   // JPEG は FF D8 で始まる
            printf("%u×%u の写真 %u バイト（JPEG %s）\n",
                   (unsigned)fb->width, (unsigned)fb->height, (unsigned)fb->len, jpeg ? "OK" : "NG");
            pico_camera_fb_return(fb);
        }
        sleep_ms(1000);
    }
}
```

- `pico_camera_init()` が、カメラを探して設定し、写真を入れる場所（約 85KB）をメモリにとります
- `pico_camera_fb_get()` で1枚撮り、使い終わったら `pico_camera_fb_return()` で場所を返します。返さないと、次の1枚が撮れません

### Serial Monitor の読み方

うまくいくと、1秒ごとに写真の大きさが出ます（バイト数は、写すものによって変わります）。

```text
カメラ: OV2640
640×480 の写真 18234 バイト（JPEG OK）
640×480 の写真 18190 バイト（JPEG OK）
```

| 出たもの | 原因と直し方 |
| --- | --- |
| `カメラの準備に失敗: no sensor detected on the SCCB bus (check wiring/power)` | カメラと話せない。3.3V・GND・SIOC（GP13）・SIOD（GP12）・XCLK（GP5）を確かめる。SIOC と SIOD の入れ違いが多い |
| `カメラの準備に失敗: not supported (e.g. JPEG on a sensor without a JPEG encoder)` | カメラが OV2640 ではない（OV7670 など） |
| `カメラの準備に失敗: invalid argument (check pins, pixel_format, frame_size)` | プログラムのピンの番号が違う。D0〜D7 は続いた8本、SIOD は偶数の GP |
| `撮れなかった` がくり返し出る | VSYNC・HREF・PCLK のどれかが抜けている |
| `（JPEG NG）` | D0〜D7 の順番が違う。D2〜D9 の基板なら、D2 が GP14 |

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
    c.pixel_format = PIXFORMAT_JPEG;
    c.frame_size = FRAMESIZE_VGA;      // 640×480
    c.jpeg_quality = 12;               // 0〜63。小さいほどきれいで、データが大きい
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
        printf("JPG %u\n", (unsigned)fb->len);          // 1行目: 写真のバイト数
        stdio_put_string((const char *)fb->buf, (int)fb->len, false, false);   // 写真をそのまま送る
        stdio_flush();
        pico_camera_fb_return(fb);
    }
}
```

PC が `c` を1文字送ると、ピコは次の形で1枚返します。

```text
JPG 18234          ← 1行目: これから送るバイト数
（JPEG のデータ 18234 バイト）
```

- 先にバイト数を送るので、PC はその数だけ読めば1枚が終わったとわかります
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


def get_photo(ser):
    """ピコに c を送って、写真（JPEG）を1枚受け取る。だめなら None"""
    ser.write(b"c")
    while True:
        line = ser.readline().decode(errors="replace").strip()
        if line == "":
            print("ピコから返事がありません。camera.cpp を書き込んだか確かめてください")
            return None
        if line.startswith("JPG "):
            size = int(line[4:])
            data = ser.read(size)
            if len(data) < size:
                print("写真が途中で切れました")
                return None
            return data
        print("ピコ:", line)            # ERR … などの知らせ
        if line.startswith("ERR"):
            return None


def save(data):
    name = time.strftime(f"{SAVE_DIR}/%Y%m%d_%H%M%S.jpg")
    with open(name, "wb") as f:
        f.write(data)
    print("保存しました:", name)


ser = serial.Serial(PORT, 115200, timeout=2)
ser.reset_input_buffer()
os.makedirs(SAVE_DIR, exist_ok=True)
print("s で保存、q で終了")
count, start, last_save = 0, time.time(), time.time()
while True:
    data = get_photo(ser)
    if data is None:
        time.sleep(1)
        continue
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        print("JPEG を読めませんでした（次の1枚へ）")
        continue
    cv2.imshow("camera", img)
    count += 1
    if time.time() - start >= 5:                # 5秒ごとに速さを出す
        print(f"{img.shape[1]}×{img.shape[0]}  1秒に {count / (time.time() - start):.1f} 枚")
        count, start = 0, time.time()
    key = cv2.waitKey(1) & 0xFF
    if key == ord("s") or (AUTO_SAVE and time.time() - last_save >= AUTO_SAVE):
        save(data)
        last_save = time.time()
    elif key == ord("q"):
        break
ser.close()
cv2.destroyAllWindows()
```

| ところ | すること |
| --- | --- |
| `get_photo()` | `c` を送り、`JPG 18234` の行を待って、その数だけ読む。`ERR` の行が来たら、そのまま表示する |
| `cv2.imdecode()` | JPEG のデータを、OpenCV の画像（点ごとの色の表）に戻す |
| `cv2.imshow()` | `camera` という窓に映す |
| `cv2.waitKey(1)` | 窓を描き直し、押されたキーを受け取る。これがないと窓が固まる |

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
640×480  1秒に 4.8 枚
保存しました: photos/20261121_093015.jpg
```

| 出たもの | 原因と直し方 |
| --- | --- |
| `could not open port /dev/ttyACM0: [Errno 16] Device or resource busy` | Serial Monitor か Pico Studio がポートを使っている。止める |
| `could not open port /dev/ttyACM0: [Errno 2] No such file or directory` | ピコがつながっていない。USB ケーブルを確かめる |
| `ModuleNotFoundError: No module named 'cv2'` | OpenCV がない。`sudo apt install python3-opencv` |
| `ピコから返事がありません` | ピコに `camera.cpp`（PC に映すほう）が入っていない。書き込み直す |
| `ピコ: 640×480 の写真 18234 バイト（JPEG OK）` が流れる | 配線を確かめるプログラムのまま。PC に映すほうを書き込む |
| `ピコ: ERR no sensor detected …` | カメラと話せない。Serial Monitor の表と同じように配線を見る |
| 写真が白っぽい・ぼやける | レンズの保護フィルムをはがす。レンズを少し回すとピントが合う（接着されていて回らないものもある） |

### できるファイル

| ファイル | できるとき・中身 |
| --- | --- |
| `PicoCamera/` | `git clone` したとき。カメラを動かすライブラリ（C++ のソース） |
| `build/camera.uf2` | Compile したとき。ピコに書き込むプログラム（4章） |
| `camera_view.py` | 自分で保存したとき。PC で動かすプログラム |
| `photos/20261121_093015.jpg` | **s** を押したとき（`AUTO_SAVE` を決めたら、その秒ごと）。撮った写真。名前は日付と時刻 |

### 変えたいとき

| 変えたいこと | 直すところ |
| --- | --- |
| 写真の大きさ | `camera.cpp` の `c.frame_size`。`FRAMESIZE_QVGA`（320×240、速い）・`FRAMESIZE_VGA`（640×480）・`FRAMESIZE_SVGA`（800×600、これより大きいとメモリが足りない） |
| 写真のきれいさ | `camera.cpp` の `c.jpeg_quality`（10〜20。小さいほどきれいで、遅くなる） |
| 自動で保存 | `camera_view.py` の `AUTO_SAVE = 10`（10秒ごと） |
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
- 見分けるプログラムは、`get_photo()` で受け取った `img` を学習したモデルに渡す形になります。ピコの側は、このまま変えません
- 牛舎で使うときは、PC の代わりに付録H のラズパイに USB でつなぎます。`camera_view.py` はラズパイでもそのまま動きます

## まとめ

- カメラは OV2640 の18ピンの基板。カメラの中で JPEG にするので、ピコの少ないメモリと USB でも 640×480 を送れる
- 線は18本。D0〜D7 は続いた8本（GP14〜GP21）、SIOC・SIOD は I2C0（GP13・GP12）、XCLK は GP5 からの 10MHz の時計
- ライブラリは PicoCamera を `git clone` し、`CMakeLists.txt` に `add_subdirectory(PicoCamera)` と `pico_camera` を足す
- PC が `c` を送ると、ピコは `JPG バイト数` の行と JPEG を返す。写真は `stdio_put_string()` で変えずに送る
- PC の `camera_view.py` が窓に映し、**s** で `photos/` に保存する。集めた写真がカラスの学習の材料になる

## 練習問題

```quiz
Q: この付録の配線で、カメラの D0 をつなぐピコのピンは GP 何番ですか。
A: 14 | GP14
E: D0〜D7 を GP14〜GP21 の続いた8本につなぎます。続いていないと、ライブラリが読めません。

Q: ピコからカメラに送る時計の線は、カメラの何というピンにつなぎますか。
A: XCLK
E: GP5 から 10MHz を送ります。これがないとカメラは動かず、`no sensor detected` になります。

Q: OV2640 が、カメラの中で写真を小さくする形式は何ですか。
A: JPEG | JPG
E: 640×480 の写真が、数十 KB になります。OV7670 はこれができません。

Q: `camera_view.py` で、写真を保存するキーは何ですか。
A: s
E: `photos/` フォルダに、日付と時刻の名前で保存します。終わるのは q です。

Q: `camera_view.py` で `Device or resource busy` と出ました。先に止めるのは VS Code の何ですか。
A: Serial Monitor | シリアルモニター | Serial Monitor のタブ
E: 同じポートは1つのソフトしか使えません。Pico Studio も「切断」します。
```
