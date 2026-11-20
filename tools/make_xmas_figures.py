#!/usr/bin/env python3
"""ピコの教科書の付録G（クリスマスのイルミネーション）の図を作る。

    python3 tools/make_xmas_figures.py

- books/pico/images/xmas-circuit.svg     LED 10個と電池の回路
- books/pico/images/xmas-breadboard.svg  ブレッドボードへの並べ方
- books/pico/images/xmas-hang.svg        LED を赤黒の2芯の線で延ばして木にかける
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


def hang():
    """LED を赤黒の2芯の線（UL2468・24AWG）で延ばして、ツリーの枝にかける。ボード側は半分に切ったジャンパーのオスを付ける"""
    RED, BLK, MALE, COPPER, SOLDER, JUMP = "#d93a3a", "#2b2f36", "#3a3f47", "#c87533", "#b8bec7", "#9aa0a8"
    b = [text(40, 64, "① LED 1個のつなぎ方", 13, "start", 700), text(420, 64, "② 枝にかける", 13, "start", 700)]

    def joint(x, y):   # はんだ付けした所を包んだテープ（上が y）
        b.append(f'<ellipse cx="{x}" cy="{y + 13}" rx="4.5" ry="7" fill="{SOLDER}"/>')
        b.append(f'<rect x="{x - 7}" y="{y}" width="14" height="28" rx="3" fill="#f3e2a9" opacity=".8"/>')

    def curve(x1, y1, x2, y2, c, w=3):
        m = (y1 + y2) / 2
        b.append(f'<path d="M{x1} {y1} C{x1} {m} {x2} {m} {x2} {y2}" stroke="{c}" stroke-width="{w}" fill="none" stroke-linecap="round"/>')

    # ---- 左: LED → 赤黒の2芯 → ジャンパーのオス → ブレッドボード ----
    lx, rx = 108, 132                                   # 長い足・短い足
    cx = (lx + rx) / 2
    b.append(f'<path d="M{cx - 15} 122 L{cx - 15} 98 A15 15 0 0 1 {cx + 15} 98 L{cx + 15} 122 Z" fill="#ffcdd2" stroke="#d93a3a" stroke-width="2"/>')
    b.append(f'<rect x="{cx - 18}" y="122" width="36" height="5" rx="1" fill="#ffcdd2" stroke="#d93a3a" stroke-width="2"/>')
    b.append(text(lx - 8, 140, "長い足（＋）", 11, "end", 700, RED))
    b.append(text(rx + 8, 140, "短い足（−）", 11, "start", 700, INK))
    for x in (lx, rx):
        b.append(line(x, 127, x, 162, "#8a8f98", 2))
        b.append(line(x + 2.5, 150, x + 2.5, 172, COPPER, 2))
        joint(x + 1, 146)
    b.append(text(rx + 22, 160, "はんだ付けして、1本ずつテープで包む", 11, "start", 400, SUB))
    # 2芯の線（とちゅうは省略）
    curve(lx + 2.5, 176, cx - 3, 210, RED)
    curve(rx + 2.5, 176, cx + 3, 210, BLK)
    for y1, y2 in ((210, 246), (256, 268)):
        b.append(line(cx - 3, y1, cx - 3, y2, RED))
        b.append(line(cx + 3, y1, cx + 3, y2, BLK))
    b.append(f'<path d="M{cx - 10} 252 L{cx + 10} 244 M{cx - 10} 260 L{cx + 10} 252" stroke="{SUB}" stroke-width="1.5"/>')
    b.append(text(cx + 22, 230, "赤黒の2芯の線（UL2468・24AWG）", 11, "start", 700, SUB))
    b.append(text(cx + 22, 246, "長さは、根元から枝まで＋20cm", 11, "start", 400, SUB))
    # 根元側: 赤と黒を裂いて、半分に切ったジャンパー（オス付き）をはんだ付け
    jr, jb = 92, 148
    curve(cx - 3, 268, jr, 300, RED)
    curve(cx + 3, 268, jb, 300, BLK)
    joint(jr, 296)
    joint(jb, 296)
    b.append(text(jb + 18, 310, "ジャンパーを半分に切って、", 11, "start", 400, SUB))
    b.append(text(jb + 18, 325, "オスの側をはんだ付け", 11, "start", 400, SUB))
    # ブレッドボード（下の半分と − の列）
    gy = 380                                            # ブレッドボードの溝
    rows = {"g": gy + 22, "h": gy + 33, "i": gy + 44, "j": gy + 55}
    rail = gy + 80
    px = [100 + 11 * i for i in range(14)]
    res_x, rail_x = px[6], px[10]                       # 抵抗の列・− の列でつなぐ穴
    b.append(f'<rect x="60" y="{gy - 12}" width="196" height="{rail - gy + 26}" rx="6" fill="#f2efe6" stroke="#d6cfbd" stroke-width="2"/>')
    b.append(f'<rect x="64" y="{gy - 6}" width="188" height="10" fill="#e2dccb"/>')
    b.append(line(70, rail - 7, 246, rail - 7, SIG, 1.5))
    b.append(text(72, rail + 4, "−", 12, "middle", 700, SIG))
    for x in px:
        for y in rows.values():
            b.append(f'<rect x="{x - 1.6:.1f}" y="{y - 1.6:.1f}" width="3.2" height="3.2" fill="#9a927e"/>')
        if x != px[0]:
            b.append(f'<rect x="{x - 1.6:.1f}" y="{rail - 1.6:.1f}" width="3.2" height="3.2" fill="#9a927e"/>')
    # 抵抗（溝をまたいで、下の足は g）
    b.append(line(res_x, gy - 22, res_x, rows["g"], "#8a8f98", 1.5))
    b.append(f'<rect x="{res_x - 4}" y="{gy - 10}" width="8" height="20" rx="3" fill="#f4e3c4" stroke="#8a6d3b" stroke-width="1"/>')
    for j, c in enumerate(BANDS["330Ω"]):
        b.append(f'<rect x="{res_x - 4}" y="{gy - 7 + j * 4}" width="8" height="2.4" fill="{c}"/>')
    b.append(text(res_x + 10, gy - 14, "抵抗", 11, "start", 700, SUB))
    # ジャンパーの半分（オス）を穴に差す
    b.append(f'<path d="M{jr} 324 C{jr} {rows["j"] - 30} {res_x - 24} {rows["j"] - 22} {res_x} {rows["j"] - 16}" stroke="{JUMP}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    b.append(f'<path d="M{jb} 324 C{jb} {rail - 40} {rail_x - 24} {rail - 22} {rail_x} {rail - 16}" stroke="{JUMP}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    for x, y, c in ((res_x, rows["j"], RED), (rail_x, rail, BLK)):
        b.append(f'<rect x="{x - 5}" y="{y - 17}" width="10" height="15" rx="2" fill="{MALE}"/>')
        b.append(f'<circle cx="{x}" cy="{y}" r="2.8" fill="{c}"/>')
    b.append(text(266, rows["j"] + 4, "赤 → 抵抗の下の列", 11, "start", 700, RED))
    b.append(text(266, rail + 4, "黒 → − の列", 11, "start", 700, INK))
    b.append('<g transform="translate(0 40)">')
    # ---- 右: ツリー ----
    tx = 575
    tiers = [(80, 170, 55), (135, 255, 95), (200, 340, 135)]   # 上・下・半分の幅
    for top, bottom, half in tiers:
        b.append(f'<path d="M{tx} {top} L{tx + half} {bottom} L{tx - half} {bottom} Z" fill="#3f8f4a" stroke="#2e6b36" stroke-width="2" stroke-linejoin="round"/>')
    b.append(f'<rect x="{tx - 12}" y="340" width="24" height="40" fill="#8b5a2b"/>')
    b.append(f'<path d="M{tx} 64 L{tx + 5} 76 L{tx + 17} 76 L{tx + 7} 83 L{tx + 11} 95 L{tx} 87 L{tx - 11} 95 L{tx - 7} 83 L{tx - 17} 76 L{tx - 5} 76 Z" fill="#f2c200"/>')
    spots = [(-22, 140), (24, 156), (-50, 205), (8, 190), (52, 228), (-80, 270),
             (-24, 250), (34, 286), (90, 316), (-62, 322)]
    base_y = 392
    for k, (dx, y) in enumerate(spots):
        x = tx + dx
        b.append(f'<path d="M{x} {y} Q{tx + dx * 0.2:.1f} {y + 18} {tx + (k - 4.5) * 1.6:.1f} {y + 30} L{tx + (k - 4.5) * 1.6:.1f} {base_y}" '
                 f'stroke="#d8dde3" stroke-width="1.6" fill="none" opacity=".9"/>')
    for k, (dx, y) in enumerate(spots):
        name, stroke, fill = COLORS[k]
        b.append(f'<circle cx="{tx + dx}" cy="{y}" r="7" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    # 根元: ブレッドボード（ピコ・抵抗）と電池
    b.append(f'<rect x="{tx - 80}" y="{base_y}" width="140" height="34" rx="5" fill="#f2efe6" stroke="#d6cfbd" stroke-width="2"/>')
    b.append(f'<rect x="{tx + 10}" y="{base_y + 6}" width="44" height="22" rx="3" fill="{PICO}"/>')
    b.append(text(tx - 32, base_y + 22, "ブレッドボード", 10, "middle", 700, SUB))
    b += battery(tx + 80, base_y + 2, 84, 30)
    b.append(line(tx + 60, base_y + 17, tx + 80, base_y + 17, VSYS, 2))
    b.append(text(tx, base_y + 52, "ピコ・抵抗・電池は根元に置く", 11, "middle", 700))
    b.append("</g>")
    return svg(760, 520, "LED を線で延ばして木にかける", b)


def main():
    (OUT / "xmas-circuit.svg").write_text(circuit())
    (OUT / "xmas-breadboard.svg").write_text(breadboard())
    (OUT / "xmas-hang.svg").write_text(hang())
    print("xmas-circuit.svg・xmas-breadboard.svg・xmas-hang.svg を作りました")


if __name__ == "__main__":
    main()
