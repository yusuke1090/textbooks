#!/usr/bin/env python3
"""ピコの教科書の付録I（安いカメラの画像を PC に映す）の図を作る。

    python3 tools/make_camera_figures.py

- books/pico/images/camera-wiring.svg  OV2640（18ピン）とピコの配線
作り直したら python3 tools/translate_figures.py pico で英語の図も作り直す。
"""
from make_xmas_figures import OUT, INK, SUB, PICO, PIN, line, svg, text

POWER, GND, SCCB, SYNC, CLK, DATA = "#d93a3a", "#2b2f36", "#2e7d32", "#7b4fd6", "#e07b00", "#2f6fde"

# (カメラのピン, ピコのピン, 色)。上から、カメラの基板の並びに近い順
ROWS = [("3.3V", "3V3（36番）", POWER), ("GND", "GND（38番）", GND),
        ("SIOC", "GP13（17番）", SCCB), ("SIOD", "GP12（16番）", SCCB),
        ("VSYNC", "GP2（4番）", SYNC), ("HREF", "GP3（5番）", SYNC), ("PCLK", "GP4（6番）", SYNC),
        ("XCLK", "GP5（7番）", CLK)] + \
       [(f"D{k}", f"GP{14 + k}（{p}番）", DATA) for k, p in enumerate([19, 20, 21, 22, 24, 25, 26, 27])]
GROUPS = [(0, "電源"), (2, "設定（I2C と同じ）"), (4, "合図"), (7, "時計"), (8, "データ 8本")]


def wiring():
    b = []
    y0, dy = 76, 24
    ys = [y0 + i * dy for i in range(len(ROWS) + 2)]   # 最後の2行は RESET と PWDN
    px, cx = 200, 560                                  # ピコの右の辺、カメラの左の辺
    b.append(f'<rect x="30" y="{y0 - 22}" width="{px - 30}" height="{ys[15] - y0 + 44}" rx="8" fill="{PICO}"/>')
    b.append(text(70, (y0 + ys[15]) / 2 + 6, "ピコ", 18, "middle", 700, "#ffffff"))
    b.append(f'<rect x="{cx}" y="{y0 - 22}" width="170" height="{ys[17] - y0 + 44}" rx="8" fill="#1d3557"/>')
    lens_y = (y0 + ys[17]) / 2
    b.append(f'<circle cx="{cx + 120}" cy="{lens_y}" r="30" fill="#0b1320" stroke="#8a8f98" stroke-width="4"/>')
    b.append(f'<circle cx="{cx + 120}" cy="{lens_y}" r="11" fill="#2a4a7a"/>')
    b.append(text(cx + 120, lens_y + 54, "OV2640", 13, "middle", 700, "#ffffff"))
    for (cam, pico, color), y in zip(ROWS, ys):
        b.append(text(px - 10, y + 4, pico, 12, "end", 700, "#ffffff"))
        b.append(f'<circle cx="{px}" cy="{y}" r="5" fill="{PIN}"/>')
        b.append(line(px + 6, y, cx - 6, y, color))
    for (cam, _, _), y in zip(ROWS + [("RESET", "", ""), ("PWDN", "", "")], ys):
        b.append(f'<circle cx="{cx}" cy="{y}" r="5" fill="{PIN}"/>')
        b.append(text(cx + 12, y + 4, cam, 12, "start", 700, "#ffffff"))
    # RESET は 3.3V へ、PWDN は GND へ
    for i, row, color, x in ((16, 0, POWER, 236), (17, 1, GND, 252)):
        b.append(line(cx - 6, ys[i], x, ys[i], color))
        b.append(line(x, ys[i], x, ys[row], color))
        b.append(f'<circle cx="{x}" cy="{ys[row]}" r="4" fill="{color}"/>')
    for i, label in GROUPS:
        b.append(text(400, ys[i] - 6, label, 11, "middle", 700, ROWS[i][2]))
    b.append(text(30, ys[17] + 52, "基板の名前が D2〜D9 のときは、D2 を GP14、D9 を GP21 につなぎます。", 12, "start", 400, SUB))
    return svg(760, ys[17] + 70, "カメラ（OV2640・18ピン）とピコの配線", b)


def main():
    (OUT / "camera-wiring.svg").write_text(wiring())
    print("camera-wiring.svg を作りました")


if __name__ == "__main__":
    main()
