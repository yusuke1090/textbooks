#!/usr/bin/env python3
"""ピコの教科書の7章（道具の使い方）の、ジャンパーワイヤーとテスターの図を作る。

    python3 tools/make_tester_figures.py

- books/pico/images/jumper-types.svg   ジャンパーワイヤーのオス・メスと、3つの種類のつなぐ先
- books/pico/images/tester-parts.svg   テスター（デジタルマルチメーター）の各部の名前
作り直したら python3 tools/translate_figures.py pico で英語の図も作り直す。
テスターの絵（meter・probe）は、動画（make_pico_videos.py の tester-basics）でも使う。
"""
import math

from make_xmas_figures import OUT, INK, SUB, PICO, PIN, SIG, GND, VSYS, text, line, svg

CASE, CASE_LINE, FACE = "#f08a24", "#c96a10", "#2f343c"
LCD, LCD_INK = "#c9d6a3", "#1e2a16"
METAL = "#c9ced6"
HOUSING = "#2b2f36"
WHITE = "#ffffff"
MONO = "ui-monospace, Menlo, Consolas, 'DejaVu Sans Mono', monospace"

# ダイヤルの位置: 名前 → (角度（上が 0、時計回り）, 目盛りの字)
DIAL = {"OFF": (0, "OFF"),
        "V200m": (30, "200m"), "V2000m": (48, "2000m"), "V20": (66, "20"), "V200": (84, "200"), "V600": (102, "600"),
        "ACV": (125, "600"),
        "A20m": (150, "20m"), "A200m": (168, "200m"),
        "CONT": (-125, ""),
        "R200": (-30, "200"), "R2000": (-48, "2000"), "R20k": (-66, "20k"), "R200k": (-84, "200k"), "R2M": (-102, "2M")}
DIAL_C, DIAL_R = (0, 188), 80
TERM = {"10A": (-66, 318), "COM": (0, 318), "VΩmA": (66, 318)}   # 端子（テスターの中の座標）
METER_H = 360


def polar(angle, r, c=DIAL_C):
    a = math.radians(angle)
    return c[0] + r * math.sin(a), c[1] - r * math.cos(a)


def dc(x, y, letter, size=13, color=WHITE):
    """直流の記号（V や A の横に、直線と点線）。x は字の左はし"""
    w = size * 0.62
    return [text(x, y, letter, size, "start", 700, color),
            line(x + w + 2, y - size * 0.62, x + w + 14, y - size * 0.62, color, 1.6),
            f'<line x1="{x + w + 2:.1f}" y1="{y - size * 0.32:.1f}" x2="{x + w + 14:.1f}" y2="{y - size * 0.32:.1f}" '
            f'stroke="{color}" stroke-width="1.6" stroke-dasharray="3 2"/>']


def meter(pos="V20", shown="3.30"):
    """テスター。上の真ん中が (0, 0)。pos はダイヤルの位置（DIAL の名前か角度）、shown は画面の字（"" で何も出ない）"""
    b = [f'<rect x="-120" y="0" width="240" height="{METER_H}" rx="24" fill="{CASE}" stroke="{CASE_LINE}" stroke-width="2"/>',
         f'<rect x="-108" y="12" width="216" height="{METER_H - 24}" rx="16" fill="{FACE}"/>',
         f'<rect x="-84" y="26" width="168" height="60" rx="6" fill="{LCD}" stroke="#8a9a6a" stroke-width="1.5"/>']
    if shown:
        b.append(f'<text x="72" y="72" font-size="36" text-anchor="end" font-weight="700" fill="{LCD_INK}" '
                 f'font-family="{MONO}">{shown}</text>')
    # 目盛り
    for key, (ang, s) in DIAL.items():
        x, y = polar(ang, DIAL_R)
        if key == "CONT":
            b.append(text(x, y + 4, "·)))", 12, "middle", 700, WHITE))
            b.append(f'<path d="M{x - 9:.1f} {y + 8:.1f} l7 4.5 l-7 4.5 z M{x - 2:.1f} {y + 8:.1f} v9" stroke="{WHITE}" '
                     f'stroke-width="1.2" fill="{WHITE}"/>')
        else:
            tick = polar(ang, DIAL_R - 16)
            b.append(line(tick[0], tick[1], *polar(ang, DIAL_R - 22), "#8a8f98", 1.5))
            b.append(text(x, y + 3.5, s, 9.5, "middle", 700, "#ffcf8a" if key == "OFF" else WHITE))
    # まとまりの記号
    x, y = polar(66, 104)
    b += dc(x - 8, y + 5, "V")
    x, y = polar(125, 102)
    b.append(text(x - 2, y + 5, "V~", 13, "middle", 700, WHITE))
    x, y = polar(159, 104)
    b += dc(x - 8, y + 5, "A")
    x, y = polar(-66, 102)
    b.append(text(x, y + 5, "Ω", 15, "middle", 700, WHITE))
    # つまみ
    ang = DIAL[pos][0] if isinstance(pos, str) else pos
    cx, cy = DIAL_C
    b.append(f'<circle cx="{cx}" cy="{cy}" r="52" fill="#22262c" stroke="#5a6170" stroke-width="2"/>')
    tx, ty = polar(ang, 46)
    b.append(line(*polar(ang, -14), tx, ty, WHITE, 6))
    b.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="4" fill="{CASE}"/>')
    # 端子
    for name, (x, y) in TERM.items():
        ring = "#d93a3a" if name != "COM" else "#8a8f98"
        b.append(f'<circle cx="{x}" cy="{y}" r="12" fill="#111111" stroke="{ring}" stroke-width="3"/>')
        b.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#5a6170"/>')
        b.append(text(x, y - 18, name, 10, "middle", 700, WHITE))
    return b


def probe(tx, ty, angle, color):
    """テスターの棒。先が (tx, ty)。angle=0 で先が上、90 で先が右（体は左へのびる）。後ろのはしの座標も返す"""
    body = [line(0, 0, 0, 26, METAL, 3),
            f'<rect x="-9" y="26" width="18" height="6" rx="2" fill="{color}"/>',
            f'<rect x="-6" y="32" width="12" height="80" rx="5" fill="{color}"/>',
            f'<rect x="-3" y="40" width="6" height="60" rx="3" fill="#ffffff" opacity=".15"/>']
    a = math.radians(angle)
    back = (tx - 112 * math.sin(a), ty + 112 * math.cos(a))
    return [f'<g transform="translate({tx:.1f} {ty:.1f}) rotate({angle:.1f})">', *body, "</g>"], back


def cable(x1, y1, x2, y2, color, sag=70):
    return (f'<path d="M{x1:.1f} {y1:.1f} C{x1:.1f} {y1 + sag:.1f} {x2:.1f} {y2 + sag:.1f} {x2:.1f} {y2:.1f}" '
            f'stroke="{color}" stroke-width="4" fill="none" stroke-linecap="round"/>')


def plug(x, y, color):
    """端子に差したプラグ"""
    return [f'<rect x="{x - 7:.1f}" y="{y - 4:.1f}" width="14" height="22" rx="3" fill="{color}"/>']


# ---------------------------------------------------------------- ジャンパーワイヤー
def male_end(x, y, direction, color):
    """オスのはし。(x, y) は線とのつなぎ目、direction は -1 で左向き・1 で右向き"""
    h0, h1 = sorted((x, x + direction * 34))
    p0, p1 = sorted((x + direction * 34, x + direction * 52))
    return [f'<rect x="{h0}" y="{y - 7}" width="{h1 - h0}" height="14" rx="2" fill="{HOUSING}"/>',
            f'<rect x="{p0}" y="{y - 2}" width="{p1 - p0}" height="4" fill="{METAL}"/>']


def female_end(x, y, direction, color):
    """メスのはし（中の穴を点線で見せる）"""
    h0, h1 = sorted((x, x + direction * 46))
    hole0, hole1 = sorted((x + direction * 16, x + direction * 46))
    return [f'<rect x="{h0}" y="{y - 8}" width="{h1 - h0}" height="16" rx="2" fill="{HOUSING}"/>',
            f'<rect x="{hole0}" y="{y - 3}" width="{hole1 - hole0}" height="6" fill="#5a6170" stroke="{METAL}" '
            f'stroke-width="1" stroke-dasharray="2 2"/>']


def breadboard_icon(x, y):
    b = [f'<rect x="{x}" y="{y - 26}" width="92" height="52" rx="5" fill="#f2efe6" stroke="#d6cfbd" stroke-width="2"/>']
    for i in range(4):
        for j in range(3):
            b.append(f'<rect x="{x + 14 + i * 20}" y="{y - 16 + j * 14}" width="4" height="4" fill="#9a927e"/>')
    return b


def module_icon(x, y, name, fill, side):
    """ピンが1本出た基板。side は、ピンが出る向き（-1 で左、1 で右）"""
    b = [f'<rect x="{x}" y="{y - 26}" width="92" height="52" rx="5" fill="{fill}"/>',
         text(x + 46, y + 4, name, 12, "middle", 700, WHITE)]
    px = x if side < 0 else x + 92
    p0, p1 = sorted((px, px + side * 30))
    b.append(f'<rect x="{p0}" y="{y - 2}" width="{p1 - p0}" height="4" fill="{METAL}"/>')
    b.append(f'<rect x="{min(px, px + side * 8)}" y="{y - 6}" width="8" height="12" fill="#222222"/>')
    return b


def jumper_types():
    b = []
    # オスとメスの拡大
    y = 78
    b.append(line(60, y, 140, y, VSYS, 4))
    b += male_end(140, y, 1, VSYS)
    b.append(text(70, y + 36, "オス", 15, "start", 700))
    b.append(text(70, y + 56, "先にピンが出ている。穴に差す", 12, "start", 400, SUB))
    b.append(line(420, y, 500, y, SIG, 4))
    b += female_end(500, y, 1, SIG)
    b.append(text(430, y + 36, "メス", 15, "start", 700))
    b.append(text(430, y + 56, "先が穴。ピンにかぶせる", 12, "start", 400, SUB))
    b.append(line(30, 150, 730, 150, "#e2dccb", 1.5))

    # 3つの種類
    rows = [("オス-オス", "male", "male", ("bb", None), ("bb", None), "ブレッドボードの穴どうし", "いちばんよく使う（8章の LED）"),
            ("オス-メス", "male", "female", ("bb", None), ("mod", "モジュール"), "ブレッドボードとモジュール", "付録I のカメラ"),
            ("メス-メス", "female", "female", ("mod", "ピコ"), ("mod", "モジュール"), "ピンどうしを直接", "ブレッドボードを使わない")]
    for k, (name, left, right, dev_l, dev_r, s1, s2) in enumerate(rows):
        y = 214 + k * 86
        b.append(text(30, y - 36, name, 13, "start", 700))
        # 左の先（オスはピンを穴に差し、メスはピンにかぶせる）
        x1, x2 = 150, 330
        if dev_l[0] == "bb":
            b += breadboard_icon(30, y)
        else:
            b += module_icon(x1 - 136, y, dev_l[1], PICO, 1)
        # 線
        color = (VSYS, SIG, "#2e7d32")[k]
        b.append(line(x1, y, x2, y, color, 4))
        b += (male_end if left == "male" else female_end)(x1, y, -1, color)
        b += (male_end if right == "male" else female_end)(x2, y, 1, color)
        # 右の先
        if dev_r[0] == "bb":
            b += breadboard_icon(360, y)
        else:
            b += module_icon(x2 + 50, y, dev_r[1], "#2f5fa8", -1)
        b.append(text(500, y - 2, s1, 12, "start", 700))
        b.append(text(500, y + 16, s2, 11, "start", 400, SUB))
    return svg(760, 430, "ジャンパーワイヤーの種類", b)


# ---------------------------------------------------------------- テスターの各部
def callout(x1, y1, x2, y2, title, sub):
    return [line(x1, y1, x2, y2, SUB, 1.2), f'<circle cx="{x1}" cy="{y1}" r="3" fill="{SUB}"/>',
            text(x2 + 8, y2 - 2, title, 13, "start", 700), text(x2 + 8, y2 + 15, sub, 11, "start", 400, SUB)]


def tester_parts():
    mx, my = 300, 46
    b = [f'<g transform="translate({mx} {my})">', *meter("V20", "3.30"), "</g>"]
    # 棒とコード（左に立てて置く。コードはテスターの下を回る）
    for name, color, tx, sag in (("COM", "#2b2f36", 70, 120), ("VΩmA", "#d93a3a", 118, 150)):
        tx_, ty_ = TERM[name]
        px, py = mx + tx_, my + ty_
        pr, back = probe(tx, 150, 0, color)
        b.append(cable(px, py, back[0], back[1], color, sag))
        b += plug(px, py, color)
        b += pr
    b.append(text(94, 132, "棒（テストリード）", 13, "middle", 700))
    # 名前
    b += callout(mx + 84, my + 56, 470, my + 56, "画面", "測った値が出る")
    ax, ay = mx + 42, my + 169                     # つまみの先（目盛りの字の間を通す）
    b += [line(ax, ay, mx + 136, ay, SUB, 1.2), f'<circle cx="{ax}" cy="{ay}" r="3" fill="{SUB}"/>']
    b += callout(mx + 136, ay, 470, ay, "ダイヤル", "測るもの（記号）と目盛りを選ぶ")[2:]
    b.append(line(mx + 136, ay, 470, ay, SUB, 1.2))
    b.append(text(478, my + 262, "端子（下の3つの穴）", 13, "start", 700))
    for k, (name, s) in enumerate((("COM", "黒い棒を差す（いつもここ）"), ("VΩmA", "赤い棒を差す（電圧・抵抗・導通）"),
                                   ("10A", "大きな電流用。この本では使わない"))):
        b.append(text(478, my + 288 + k * 22, name, 12, "start", 700))
        b.append(text(530, my + 288 + k * 22, s, 11, "start", 400, SUB))
    b.append(text(380, 492, "ダイヤルは、直流の電圧（V）の 20。ピコの 3.3V を測ったところ", 12, "middle", 400, SUB))
    return svg(760, 510, "テスター（デジタルマルチメーター）の各部", b)


def main():
    (OUT / "jumper-types.svg").write_text(jumper_types())
    (OUT / "tester-parts.svg").write_text(tester_parts())
    print("jumper-types.svg・tester-parts.svg を作りました")


if __name__ == "__main__":
    main()
