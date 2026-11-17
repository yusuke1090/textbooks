#!/usr/bin/env python3
"""ピコの教科書の付録G（クリスマスのイルミネーション）の図を作る。

    python3 tools/make_xmas_figures.py

- books/pico/images/xmas-circuit.svg     LED 10個と電池の回路
- books/pico/images/xmas-breadboard.svg  ブレッドボードへの並べ方
作り直したら python3 tools/translate_figures.py pico で英語の図も作り直す。
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "books" / "pico" / "images"
FONT = "system-ui, 'Noto Sans JP', sans-serif"
INK, SUB, PICO, PIN = "#2b2f36", "#555c66", "#1f7a3d", "#e0a800"
SIG, GND, VSYS = "#2f6fde", "#2b2f36", "#d93a3a"

# LED の色（名前・線・中）。GP0 から順に、赤・緑・黄・青・白を2回
COLORS = [("赤", "#d93a3a", "#ffcdd2"), ("緑", "#2e7d32", "#c8e6c9"), ("黄", "#c79100", "#fff59d"),
          ("青", "#1e63d6", "#bbdefb"), ("白", "#8a8f98", "#ffffff")] * 2
BANDS = {"330Ω": ["#f08c00", "#f08c00", "#8b4513", "#c9a227"],      # 橙・橙・茶・金
         "100Ω": ["#8b4513", "#222222", "#8b4513", "#c9a227"]}      # 茶・黒・茶・金
GP_PIN = [1, 2, 4, 5, 6, 7, 9, 10, 11, 12]   # GP0〜GP9 の物理ピン番号


def ohm(k):
    return "330Ω" if COLORS[k][0] in ("赤", "黄") else "100Ω"


def text(x, y, s, size=12, anchor="start", weight=400, fill=INK):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" '
            f'font-weight="{weight}" fill="{fill}">{s}</text>')


def line(x1, y1, x2, y2, color, w=3):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" '
            f'stroke-width="{w}" stroke-linecap="round"/>')


def svg(w, h, title, body):
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}" font-size="13">',
        f'<rect width="{w}" height="{h}" rx="10" fill="#ffffff"/>',
        text(w / 2, 26, title, 16, "middle", 700), *body, "</svg>", ""])


def battery(x, y, w=150, h=46):
    """電池ボックス（単3×3本・スイッチ付き）。左上が (x, y)"""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="#3a3f47"/>']
    cw = (w - 40) / 3
    for i in range(3):
        cx = x + 8 + i * (cw + 4)
        out.append(f'<rect x="{cx:.1f}" y="{y + 9}" width="{cw:.1f}" height="{h - 18}" rx="4" fill="#c9ced6"/>')
        out.append(f'<rect x="{cx + cw:.1f}" y="{y + h / 2 - 4:.1f}" width="3" height="8" fill="#c9ced6"/>')
    out.append(f'<rect x="{x + w - 18}" y="{y + 14}" width="10" height="18" rx="2" fill="#8a8f98"/>')
    out.append(f'<rect x="{x + w - 16}" y="{y + 16}" width="6" height="7" rx="1" fill="#ffffff"/>')
    return out


def circuit():
    b = []
    rows = [76 + 32 * i for i in range(10)]
    y_gnd, y_vsys = 404, 444
    b.append(f'<rect x="30" y="46" width="170" height="430" rx="8" fill="{PICO}"/>')
    b.append(text(64, 266, "ピコ", 18, "middle", 700, "#ffffff"))
    labels = [(y, f"GP{k}（{GP_PIN[k]}番）") for k, y in enumerate(rows)] + [(y_gnd, "GND（38番）"), (y_vsys, "VSYS（39番）")]
    for y, s in labels:
        b.append(text(192, y + 4, s, 12, "end", 700, "#ffffff"))
        b.append(f'<circle cx="200" cy="{y}" r="6" fill="{PIN}"/>')
    bus = 560
    for k, y in enumerate(rows):
        name, stroke, fill = COLORS[k]
        b.append(line(206, y, 250, y, SIG))
        b.append(f'<rect x="250" y="{y - 8}" width="50" height="16" rx="4" fill="#f4e3c4" stroke="#8a6d3b" stroke-width="1.5"/>')
        for j, c in enumerate(BANDS[ohm(k)]):
            b.append(f'<rect x="{258 + j * 9}" y="{y - 8}" width="5" height="16" fill="{c}"/>')
        b.append(text(275, y - 12, ohm(k), 11, "middle", 700, SUB))
        b.append(line(300, y, 370, y, SIG))
        b.append(f'<path d="M370 {y - 9} L370 {y + 9} L388 {y} Z" stroke="{stroke}" stroke-width="2" fill="{fill}" stroke-linejoin="round"/>')
        b.append(line(388, y - 9, 388, y + 9, stroke))
        b.append(text(398, y - 6, name, 12, "start", 700, stroke))
        b.append(line(392, y, bus, y, GND))
    b.append(line(bus, rows[0], bus, y_gnd, GND))
    b.append(line(bus, y_gnd, 206, y_gnd, GND))
    # 電池
    b += battery(400, 424)
    b.append(line(206, y_vsys, 400, y_vsys, VSYS))
    b.append(text(394, y_vsys - 6, "＋", 13, "end", 700, VSYS))
    b.append(line(550, 452, bus, 452, GND))
    b.append(line(bus, 452, bus, y_gnd, GND))
    b.append(text(555, 447, "−", 13, "middle", 700, INK))
    b.append(text(475, 488, "電池ボックス（単3×3本 = 4.5V）", 12, "middle", 700))
    # 右の説明
    notes = [(80, "LED の長い足（＋）", VSYS, 700), (96, "を抵抗の側に", VSYS, 400),
             (126, "短い足（−）は", INK, 700), (142, "GND の線へ", INK, 400),
             (184, "抵抗", INK, 700), (200, "赤・黄 → 330Ω", INK, 400), (216, "緑・青・白 → 100Ω", INK, 400)]
    for y, s, c, wt in notes:
        b.append(text(574, y, s, 12, "start", wt, c))
    b.append(text(30, 520, "USB をつなぐときは、電池のスイッチを切ります。", 12, "start", 400, SUB))
    return svg(760, 540, "イルミネーションの回路（LED 10個と電池）", b)


def breadboard():
    p = 10.6
    X = lambda col: 52 + (col - 1) * p
    top = {r: 204 + i * p for i, r in enumerate("abcde")}
    bot = {r: 204 + (i + 7) * p for i, r in enumerate("fghij")}
    row = {**top, **bot}
    rail_minus, rail_plus = bot["j"] + 2.5 * p, bot["j"] + 3.5 * p
    b = [f'<rect x="38" y="158" width="{X(63) + 14 - 38:.1f}" height="216" rx="8" fill="#f2efe6" stroke="#d6cfbd" stroke-width="2"/>',
         f'<rect x="44" y="{top["e"] + 8:.1f}" width="{X(63) + 2 - 44:.1f}" height="{bot["f"] - top["e"] - 16:.1f}" fill="#e2dccb"/>']
    # 電源の列の線（上: ＋ 赤・− 青、下: − 青・＋ 赤）
    b.append(line(X(1), 166, X(63), 166, VSYS, 1.5))
    b.append(line(X(1), 188.6, X(63), 188.6, SIG, 1.5))
    b.append(line(X(1), rail_minus - 6, X(63), rail_minus - 6, SIG, 1.5))
    b.append(line(X(1), rail_plus + 6, X(63), rail_plus + 6, VSYS, 1.5))
    b.append(text(44, rail_minus + 4, "−", 12, "middle", 700, SIG))
    b.append(text(44, rail_plus + 4, "+", 12, "middle", 700, VSYS))
    holes = []
    for col in range(1, 64):
        for y in [172, 182.6, rail_minus, rail_plus] if col % 6 else []:
            holes.append((X(col), y))
        for y in row.values():
            holes.append((X(col), y))
    for x, y in holes:
        b.append(f'<rect x="{x - 1.6:.1f}" y="{y - 1.6:.1f}" width="3.2" height="3.2" fill="#9a927e"/>')
    # ピコ（USB を右に。上の列が 1〜20番、下の列が 40〜21番）
    b.append(f'<rect x="{X(44) - 6:.1f}" y="{top["c"] - 8:.1f}" width="{X(63) - X(44) + 12:.1f}" height="{bot["h"] - top["c"] + 16:.1f}" rx="5" fill="{PICO}"/>')
    b.append(f'<rect x="{X(63) + 4:.1f}" y="{(top["c"] + bot["h"]) / 2 - 8:.1f}" width="14" height="16" rx="2" fill="#b8bec7"/>')
    for col in range(44, 64):
        for y in (top["c"], bot["h"]):
            b.append(f'<circle cx="{X(col):.1f}" cy="{y:.1f}" r="2.6" fill="{PIN}"/>')
    b.append(text((X(44) + X(63)) / 2, 266, "ピコ", 15, "middle", 700, "#ffffff"))
    b.append(text(X(63) + 2, top["c"] + 14, "GP0", 9, "end", 700, "#ffffff"))
    b.append(text(X(52), top["c"] + 14, "GP9", 9, "middle", 700, "#ffffff"))
    b.append(text(X(63) + 8, (top["c"] + bot["h"]) / 2 + 22, "USB", 9, "start", 700, SUB))
    b.append(text(X(62) + 3, bot["h"] - 22, "VSYS（39番）", 9, "end", 700, "#ffffff"))
    b.append(line(X(62), bot["h"] - 19, X(62), bot["h"] - 4, "#ffffff", 1))
    b.append(text(X(61) - 4, bot["h"] - 8, "GND（38番）", 9, "end", 700, "#ffffff"))
    b.append(line(X(61), bot["h"] - 14, X(61), bot["h"] - 4, "#ffffff", 1))
    # LED・抵抗・ワイヤー
    for k in range(10):
        n = 64 - GP_PIN[k]          # GPk の列（1番ピンが 63列）
        m = 14 + 3 * k              # LED の列
        h = 18 + (9 - k) * 11
        x1, x2, y = X(n), X(m), top["a"]
        b.append(f'<path d="M{x1:.1f} {y:.1f} C{x1:.1f} {y - h * 1.33:.1f} {x2:.1f} {y - h * 1.33:.1f} {x2:.1f} {y:.1f}" '
                 f'stroke="{SIG}" stroke-width="2.5" fill="none" stroke-linecap="round"/>')
        for x in (x1, x2):
            b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.8" fill="{SIG}"/>')
        # 抵抗: e（上）から g（下）へ、溝をまたぐ
        b.append(line(x2, top["e"], x2, bot["g"], "#8a8f98", 1.5))
        cy = (top["e"] + bot["g"]) / 2
        b.append(f'<rect x="{x2 - 4:.1f}" y="{cy - 10:.1f}" width="8" height="20" rx="3" fill="#f4e3c4" stroke="#8a6d3b" stroke-width="1"/>')
        for j, c in enumerate(BANDS[ohm(k)]):
            b.append(f'<rect x="{x2 - 4:.1f}" y="{cy - 7 + j * 4:.1f}" width="8" height="2.4" fill="{c}"/>')
        # LED: 長い足は j の穴、短い足は − の列
        name, stroke, fill = COLORS[k]
        lx, ly = x2 + p / 2, (bot["j"] + rail_minus) / 2
        b.append(line(x2, bot["j"], lx - 2, ly, "#8a8f98", 1.5))
        b.append(line(x2 + p, rail_minus, lx + 2, ly, "#8a8f98", 1.5))
        b.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="6.5" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        b.append(f'<circle cx="{x2 + p:.1f}" cy="{rail_minus:.1f}" r="2" fill="{INK}"/>')
        b.append(text(lx, 392, f"GP{k}", 10, "middle", 700, SUB))
    # GND（38番 = 61列）を − の列へ、電池の＋を VSYS（39番 = 62列）へ
    b.append(line(X(61), bot["j"], X(61), rail_minus, GND, 2.5))
    b.append(f'<circle cx="{X(61):.1f}" cy="{bot["j"]:.1f}" r="2.8" fill="{GND}"/>')
    b.append(f'<circle cx="{X(61):.1f}" cy="{rail_minus:.1f}" r="2.8" fill="{GND}"/>')
    bx, by = 520, 410
    b += battery(bx, by)
    b.append(f'<path d="M{X(62):.1f} {bot["j"]:.1f} C{X(62) + 30:.1f} {bot["j"] + 60:.1f} {bx + 160:.1f} {by - 40:.1f} {bx + 150:.1f} {by + 10:.1f}" '
             f'stroke="{VSYS}" stroke-width="2.5" fill="none" stroke-linecap="round"/>')
    b.append(f'<circle cx="{X(62):.1f}" cy="{bot["j"]:.1f}" r="2.8" fill="{VSYS}"/>')
    b.append(f'<path d="M{X(57):.1f} {rail_minus:.1f} C{X(57):.1f} {rail_minus + 40:.1f} {bx - 20:.1f} {by + 20:.1f} {bx:.1f} {by + 23:.1f}" '
             f'stroke="{GND}" stroke-width="2.5" fill="none" stroke-linecap="round"/>')
    b.append(f'<circle cx="{X(57):.1f}" cy="{rail_minus:.1f}" r="2.8" fill="{GND}"/>')
    b.append(text(bx + 75, by + 64, "電池ボックス（スイッチは切っておく）", 11, "middle", 700))
    notes = ["① 抵抗は、真ん中の溝をまたいで差す", "② LED の長い足は抵抗の下の列、短い足は − の列",
             "③ ワイヤーで、GP の列と抵抗の上の列をつなぐ"]
    for i, s in enumerate(notes):
        b.append(text(40, 422 + i * 20, s, 12))
    return svg(760, 490, "ブレッドボードへの並べ方", b)


def main():
    (OUT / "xmas-circuit.svg").write_text(circuit())
    (OUT / "xmas-breadboard.svg").write_text(breadboard())
    print("xmas-circuit.svg と xmas-breadboard.svg を作りました")


if __name__ == "__main__":
    main()
