#!/usr/bin/env python3
"""ピコの教科書の付録I（安いカメラの画像を PC に映す）の図を作る。

    python3 tools/make_camera_figures.py

- books/pico/images/camera-wiring.svg  OV7670（18ピン）とピコの配線
- books/pico/images/pump-wiring.svg    水鉄砲のテスト（MOSFET モジュール・電池・ポンプ）の配線
作り直したら python3 tools/translate_figures.py pico で英語の図も作り直す。
"""
from make_xmas_figures import OUT, PICO, PIN, line, svg, text, battery

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
    b.append(text(cx + 120, lens_y + 54, "OV7670", 13, "middle", 700, "#ffffff"))
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
    return svg(760, ys[17] + 40, "カメラ（OV7670・18ピン）とピコの配線", b)


# ---------------------------------------------------------------- 水鉄砲のテスト
BOARD, TERM, WATER = "#2f5fa8", "#2e9e5b", "#bfe3f7"


def mosfet(x, y, w=160, h=190):
    """MOSFET モジュール（D4184 など）。左が信号と GND、右上が VIN、右下が OUT のネジの端子。
    （部品, 端子の場所 {名前: (x, y)}）を返す"""
    t = {"信号": (x, y + 60), "GND": (x, y + 110), "VIN+": (x + w, y + 35), "VIN−": (x + w, y + 65),
         "OUT+": (x + w, y + 120), "OUT−": (x + w, y + 150)}
    b = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{BOARD}"/>']
    for k in range(2):                                    # MOSFET のチップ
        b.append(f'<rect x="{x + w / 2 - 26 + k * 30}" y="{y + 70}" width="22" height="30" rx="2" fill="#15181d"/>')
    for name, (tx, ty) in t.items():
        left = tx == x
        bx = tx if left else tx - 22
        b.append(f'<rect x="{bx}" y="{ty - 12}" width="22" height="24" fill="{TERM}"/>')
        b.append(f'<circle cx="{bx + 11}" cy="{ty}" r="6" fill="#c9ced6" stroke="#8a8f98" stroke-width="1.5"/>')
        b.append(text(tx + 28 if left else tx - 28, ty + 4, name, 12, "start" if left else "end", 700, "#ffffff"))
    b.append(text(x + w / 2, y + h - 14, "MOSFET モジュール", 12, "middle", 700, "#ffffff"))
    return b, t


def cup_pump(x, y):
    """水を入れたコップと、沈めたポンプ。（部品, {"red": 赤の線の出口, "black": 黒の線の出口, "hose": ホースの出口}）"""
    b = [f'<path d="M{x} {y} L{x + 10} {y + 120} L{x + 90} {y + 120} L{x + 100} {y} Z" fill="#ffffff" stroke="#8a8f98" stroke-width="2"/>',
         f'<path d="M{x + 2} {y + 22} L{x + 10} {y + 118} L{x + 90} {y + 118} L{x + 98} {y + 22} Z" fill="{WATER}"/>',
         f'<rect x="{x + 22}" y="{y + 82}" width="50" height="32" rx="6" fill="#3a3f47"/>',
         f'<rect x="{x + 64}" y="{y + 70}" width="10" height="16" fill="#3a3f47"/>']
    return b, {"red": (x + 52, y + 82), "black": (x + 32, y + 82), "hose": (x + 69, y + 70)}


def diode(x, y1, y2, color="#15181d"):
    """縦に置いたダイオード。足は y1（帯のある側）から y2"""
    my = (y1 + y2) / 2
    return [line(x, y1, x, y2, "#8a8f98", 2),
            f'<rect x="{x - 6}" y="{my - 11}" width="12" height="22" rx="3" fill="{color}"/>',
            f'<rect x="{x - 6}" y="{my - 11}" width="12" height="5" fill="#c9ced6"/>']


def polyline(pts, color, w=3):
    d = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f} {y:.1f}" for i, (x, y) in enumerate(pts))
    return f'<path d="{d}" stroke="{color}" stroke-width="{w}" fill="none" stroke-linejoin="round" stroke-linecap="round"/>'


def pump_wiring():
    b = []
    # ピコ
    b.append(f'<rect x="30" y="60" width="160" height="190" rx="8" fill="{PICO}"/>')
    b.append(text(70, 160, "ピコ", 18, "middle", 700, "#ffffff"))
    for y, s in ((120, "GP22（29番）"), (170, "GND（28番）")):
        b.append(text(180, y + 4, s, 12, "end", 700, "#ffffff"))
        b.append(f'<circle cx="190" cy="{y}" r="5" fill="{PIN}"/>')
    m, t = mosfet(300, 60)
    b += m
    b.append(line(196, 120, t["信号"][0], 120, DATA))
    b.append(line(196, 170, t["GND"][0], 170, GND))
    # 電池ボックス（左から赤と黒の線）
    b.append(text(635, 62, "電池ボックス（単3×3本）", 12, "middle", 700))
    b += battery(560, 72)
    b.append(polyline([(560, 82), (510, 82), (510, t["VIN+"][1]), t["VIN+"]], POWER))
    b.append(polyline([(560, 104), (520, 104), (520, t["VIN−"][1]), t["VIN−"]], GND))
    # コップとポンプ。線は上から入れる
    c, e = cup_pump(560, 228)
    b += c
    rx, ry = e["red"]
    kx, ky = e["black"]
    b.append(polyline([t["OUT+"], (rx, t["OUT+"][1]), (rx, ry)], POWER))
    b.append(polyline([t["OUT−"], (kx, t["OUT−"][1]), (kx, ky)], GND))
    b += diode(530, t["OUT+"][1], t["OUT−"][1])
    b.append(text(522, t["OUT−"][1] + 26, "ダイオード（帯を ＋ に）", 11, "middle", 700))
    hx, hy = e["hose"]
    b.append(f'<path d="M{hx} {hy} C{hx} {hy - 60} {hx + 40} {hy - 80} {hx + 90} {hy - 110}" stroke="#8fb8d8" stroke-width="7" fill="none" stroke-linecap="round"/>')
    b.append(text(hx + 96, hy - 120, "ホース", 12, "end", 700))
    b.append(text(610, 372, "ポンプ（水に沈める）", 12, "middle", 700))
    return svg(760, 388, "水鉄砲のテストの配線", b)


def main():
    (OUT / "camera-wiring.svg").write_text(wiring())
    (OUT / "pump-wiring.svg").write_text(pump_wiring())
    print("camera-wiring.svg・pump-wiring.svg を作りました")


if __name__ == "__main__":
    main()
