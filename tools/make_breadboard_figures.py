#!/usr/bin/env python3
"""ピコの教科書の、ブレッドボードへの差し方の図を作る（ハーフサイズ・30列。ピコは USB を右にして 11〜30列）。

    python3 tools/make_breadboard_figures.py

- books/pico/images/led-breadboard.svg     8章 外付けの LED
- books/pico/images/led-nowire.svg         8章 外付けの LED（ジャンパーワイヤーなし）
- books/pico/images/button-breadboard.svg  8章 外付けのボタン
- books/pico/images/pot-breadboard.svg     9章 ボリューム
作り直したら python3 tools/translate_figures.py pico で英語の図も作り直す。

ピンの番号と列: 上の列は 20番が 11列で、右へ 19、18 … 1番（30列）。下の列は 21番が 11列で、右へ 22 … 40番（30列）。
"""
from make_xmas_figures import OUT, INK, SUB, PICO, PIN, SIG, GND, VSYS, text, line, svg

P = 20                                   # 穴の間隔
X = lambda col: 90 + (col - 1) * P       # 列 → x
ROW = {r: 150 + i * P for i, r in enumerate("abcde")} | {r: 290 + i * P for i, r in enumerate("fghij")}
TOP_PLUS, TOP_MINUS, BOT_MINUS, BOT_PLUS = 72, 92, 404, 424
MARK = "#ffe27a"                         # 中でつながっている穴
LEG = "#8a8f98"
WHITE = "#ffffff"


def col_of(pin):
    """物理ピンの番号 → 列"""
    return 31 - pin if pin <= 20 else pin - 10


def board(cols=(), rails=()):
    """ブレッドボード。cols は色を付ける (列, "top" か "bottom")、rails は色を付ける電源の列の y"""
    b = [f'<rect x="70" y="50" width="{X(30) + 20 - 70}" height="390" rx="8" fill="#f2efe6" stroke="#d6cfbd" stroke-width="2"/>',
         f'<rect x="76" y="{ROW["e"] + 10}" width="{X(30) + 14 - 76}" height="{ROW["f"] - ROW["e"] - 20}" fill="#e2dccb"/>']
    for col, half in cols:
        y0 = ROW["a"] if half == "top" else ROW["f"]
        b.append(f'<rect x="{X(col) - 8}" y="{y0 - 8}" width="16" height="{4 * P + 16}" rx="4" fill="{MARK}"/>')
    for y in rails:
        b.append(f'<rect x="{X(1) - 8}" y="{y - 8}" width="{X(30) - X(1) + 16}" height="16" rx="4" fill="{MARK}"/>')
    # 電源の列（上: ＋ 赤・− 青、下: − 青・＋ 赤）
    for y, c in ((TOP_PLUS - 10, VSYS), (TOP_MINUS + 10, SIG), (BOT_MINUS - 10, SIG), (BOT_PLUS + 10, VSYS)):
        b.append(line(X(1), y, X(30), y, c, 1.5))
    for y, s, c in ((TOP_PLUS, "+", VSYS), (TOP_MINUS, "−", SIG), (BOT_MINUS, "−", SIG), (BOT_PLUS, "+", VSYS)):
        b.append(text(78, y + 4, s, 13, "middle", 700, c))
    for r, y in ROW.items():
        b.append(text(78, y + 4, r, 10, "middle", 400, SUB))
    for col in range(1, 31):
        ys = list(ROW.values()) + ([TOP_PLUS, TOP_MINUS, BOT_MINUS, BOT_PLUS] if col % 6 else [])
        for y in ys:
            b.append(f'<rect x="{X(col) - 2}" y="{y - 2}" width="4" height="4" fill="#9a927e"/>')
    return b


def pico(labels, name_dx=40, name_dy=6):
    """ピコ（11〜30列、ピンは c と h）。labels は (物理ピン, 文字, 段, "start" か "end")"""
    c, h = ROW["c"], ROW["h"]
    b = [f'<rect x="{X(11) - 12}" y="{c - 14}" width="{X(30) - X(11) + 24}" height="{h - c + 28}" rx="6" fill="{PICO}"/>',
         f'<rect x="{X(30) + 12}" y="{(c + h) / 2 - 12}" width="18" height="24" rx="2" fill="#b8bec7"/>',
         text(X(30) + 34, (c + h) / 2 + 4, "USB", 11, "start", 700, SUB)]
    for col in range(11, 31):
        for y in (c, h):
            b.append(f'<circle cx="{X(col)}" cy="{y}" r="3.5" fill="{PIN}"/>')
    b.append(text((X(11) + X(30)) / 2 + name_dx, (c + h) / 2 + name_dy, "ピコ", 18, "middle", 700, WHITE))
    for pin, s, level, anchor in labels:
        x = X(col_of(pin))
        if pin <= 20:
            y1 = c + 18 + level * 24
            b += [line(x, c + 6, x, y1, WHITE, 1.2), text(x + 6 if anchor == "start" else x - 6, y1 + 8, s, 11, anchor, 700, WHITE)]
        else:
            y1 = h - 18 - level * 24
            b += [line(x, h - 6, x, y1, WHITE, 1.2), text(x + 6 if anchor == "start" else x - 6, y1 - 4, s, 11, anchor, 700, WHITE)]
    return b


def dot(x, y, color=INK):
    return f'<circle cx="{x}" cy="{y}" r="3.5" fill="{color}"/>'


def wire(x1, y1, x2, y2, color, bend):
    """ジャンパーワイヤー。bend はふくらみ（− で上、＋ で下）"""
    return [f'<path d="M{x1} {y1} C{x1} {y1 + bend * 1.33:.1f} {x2} {y2 + bend * 1.33:.1f} {x2} {y2}" '
            f'stroke="{color}" stroke-width="3" fill="none" stroke-linecap="round"/>', dot(x1, y1, color), dot(x2, y2, color)]


def mark(n, x, y):
    """手順の番号（本文の手順と同じ）"""
    return [f'<circle cx="{x}" cy="{y}" r="10" fill="{WHITE}" stroke="{INK}" stroke-width="1.5"/>',
            text(x, y + 4.5, str(n), 12, "middle", 700)]


def note(s):
    return text(70, 466, s, 12, "start", 400, SUB)


def resistor(col1, col2, y):
    """抵抗（220Ω: 赤・赤・茶・金）。col1 と col2 の、同じ段 y に足を差す"""
    b = [line(X(col1), y, X(col2), y, LEG, 2)]
    bx = (X(col1) + X(col2)) / 2
    b.append(f'<rect x="{bx - 24}" y="{y - 8}" width="48" height="16" rx="5" fill="#f4e3c4" stroke="#8a6d3b" stroke-width="1.5"/>')
    for j, col in enumerate(["#d93a3a", "#d93a3a", "#8b4513", "#c9a227"]):
        b.append(f'<rect x="{bx - 15 + j * 9}" y="{y - 8}" width="5" height="16" fill="{col}"/>')
    return b + [dot(X(col1), y), dot(X(col2), y)]


def led():
    """8章 外付けの LED: GP15（20番）→ 抵抗 → LED → − の列 ← GND（18番）"""
    b = board(cols=[(7, "top"), (11, "top"), (13, "top")], rails=[TOP_MINUS])
    b += pico([(18, "GND（18番）", 0, "start"), (20, "GP15（20番）", 1, "start")])
    # 抵抗: 11列の b と 7列の b
    b += resistor(7, 11, ROW["b"])
    bx = (X(7) + X(11)) / 2
    # LED: 長い足は 7列の a、短い足は上の − の列
    lx, ly = X(7) + P / 2, (ROW["a"] + TOP_MINUS) / 2
    b.append(line(X(7), ROW["a"], lx - 3, ly, LEG, 2))
    b.append(line(X(8), TOP_MINUS, lx + 3, ly, LEG, 2))
    b.append(f'<circle cx="{lx}" cy="{ly}" r="9" fill="#ffcdd2" stroke="#d93a3a" stroke-width="2"/>')
    b.append(text(lx - 16, ROW["a"] - 6, "長い足（＋）", 11, "end", 700, "#d93a3a"))
    b.append(text(X(8) + 10, TOP_MINUS + 24, "短い足（−）", 11, "start", 700, INK))
    b += [dot(X(7), ROW["a"], "#d93a3a"), dot(X(8), TOP_MINUS)]
    # ワイヤー: 13列の a と上の − の列
    b.append(f'<path d="M{X(13)} {ROW["a"]} C{X(13) + 14} {ROW["a"] - 10} {X(13) + 14} {TOP_MINUS + 10} {X(13)} {TOP_MINUS}" '
             f'stroke="{GND}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    b += [dot(X(13), ROW["a"], GND), dot(X(13), TOP_MINUS, GND)]
    b += mark(2, X(22), ROW["h"] - 30)
    b += mark(3, bx, ROW["b"] + 22)
    b += mark(4, lx - 30, TOP_MINUS + 24)
    b += mark(5, X(13) + 28, (ROW["a"] + TOP_MINUS) / 2)
    b.append(note("番号は本文の手順（② ピコ　③ 抵抗　④ LED　⑤ ワイヤー）。黄色の所は、中でつながっている穴"))
    return svg(760, 486, "ブレッドボードへの差し方", b)


def led_nowire():
    """8章 外付けの LED（ジャンパーワイヤーなし）: GP15（20番）→ LED → 抵抗 → GND（18番）"""
    b = board(cols=[(9, "top"), (11, "top"), (13, "top")])
    b += pico([(18, "GND（18番）", 0, "start"), (20, "GP15（20番）", 1, "start")])
    # LED: 長い足は 11列（20番）の a、短い足は 9列の a
    lx, ly = X(10), ROW["a"] - 30
    b.append(line(X(11), ROW["a"], lx + 3, ly, LEG, 2))
    b.append(line(X(9), ROW["a"], lx - 3, ly, LEG, 2))
    b.append(f'<circle cx="{lx}" cy="{ly}" r="9" fill="#ffcdd2" stroke="#d93a3a" stroke-width="2"/>')
    b.append(text(X(11) + 10, ROW["a"] - 12, "長い足（＋）", 11, "start", 700, "#d93a3a"))
    b.append(text(X(9) - 10, ROW["a"] - 12, "短い足（−）", 11, "end", 700, INK))
    b += [dot(X(11), ROW["a"], "#d93a3a"), dot(X(9), ROW["a"])]
    # 抵抗: 9列の b と 13列（18番）の b
    b += resistor(9, 13, ROW["b"])
    b.append(note("抵抗は LED の短い足の側に入れる。ジャンパーワイヤーはいらない。黄色の所は、中でつながっている穴"))
    return svg(760, 486, "ジャンパーワイヤーなしの差し方", b)


def button():
    """8章 外付けのボタン: 溝をまたいで差し、対角の足を GP14（19番）と GND（23番）へ"""
    b = board(cols=[(4, "top"), (12, "top"), (6, "bottom"), (13, "bottom")])
    b += pico([(19, "GP14（19番）", 0, "start"), (23, "GND（23番）", 0, "start")])
    # ボタン: 足は 4列と 6列の e・f
    x1, x2, y1, y2 = X(4), X(6), ROW["e"], ROW["f"]
    for x in (x1, x2):
        b.append(line(x, y1, x, y2, LEG, 3))
    b.append(f'<rect x="{x1 - 8}" y="{y1 + 8}" width="{x2 - x1 + 16}" height="{y2 - y1 - 16}" rx="4" fill="#3a3f47"/>')
    b.append(f'<circle cx="{(x1 + x2) / 2}" cy="{(y1 + y2) / 2}" r="12" fill="#8a8f98" stroke="#c9ced6" stroke-width="2"/>')
    b += [dot(x2, y1, LEG), dot(x1, y2, LEG), dot(x1, y1, SIG), dot(x2, y2, GND)]
    # ワイヤー: 左上の足（4列）→ 19番の列、右下の足（6列）→ 23番の列
    b += wire(X(4), ROW["a"], X(12), ROW["a"], SIG, -26)
    b += wire(X(6), ROW["j"], X(13), ROW["j"], GND, 22)
    b += mark(2, X(1) + 4, (y1 + y2) / 2)
    b += mark(3, X(8), ROW["c"])
    b += mark(4, X(9), ROW["h"])
    b.append(note("番号は本文の手順（② ボタン　③④ ワイヤー）。ボタンは対角の2本の足を使う。黄色の所は、中でつながっている穴"))
    return svg(760, 486, "ボタンの差し方", b)


def pot():
    """9章 ボリューム: 足は 4・6・8列の f。左 → 36番、真ん中 → 31番（GP26）、右 → 28番（GND）"""
    b = board(cols=[(4, "bottom"), (6, "bottom"), (8, "bottom"), (18, "bottom"), (21, "bottom"), (26, "bottom")])
    b += pico([(28, "GND（28番）", 0, "end"), (31, "GP26（31番）", 0, "start"), (36, "3V3(OUT)（36番）", 1, "end")],
              name_dx=-30, name_dy=-6)
    # ボリューム: 本体は溝の上、足は f の列
    xs, y = (X(4), X(6), X(8)), ROW["f"]
    b.append(f'<rect x="{xs[0] - 18}" y="{ROW["e"] + 4}" width="{xs[2] - xs[0] + 36}" height="{y - ROW["e"] - 10}" rx="5" fill="#2f5fa8"/>')
    cx, cy = xs[1], (ROW["e"] + y) / 2
    b.append(f'<circle cx="{cx}" cy="{cy}" r="17" fill="#c9ced6" stroke="#8a8f98" stroke-width="2"/>')
    b.append(line(cx, cy, cx + 8, cy - 11, INK, 2.5))
    for x, c in zip(xs, (VSYS, SIG, GND)):
        b.append(line(x, y - 8, x, y, LEG, 3))
        b.append(dot(x, y, c))
    # ワイヤー: 左の足 → 36番、真ん中 → 31番、右 → 28番（内側から順に、交わらない）
    b += wire(X(8), ROW["j"], X(col_of(28)), ROW["j"], GND, 18)
    b += wire(X(6), ROW["j"], X(col_of(31)), ROW["j"], SIG, 34)
    b += wire(X(4), ROW["j"], X(col_of(36)), ROW["j"], VSYS, 50)
    b += mark(2, X(1) + 4, cy)
    b += mark(3, X(2), ROW["i"])
    b.append(note("番号は本文の手順（② ボリューム　③ ワイヤー）。黄色の所は、中でつながっている穴"))
    return svg(760, 486, "ボリュームの差し方", b)


def main():
    for name, make in (("led-breadboard", led), ("led-nowire", led_nowire),
                       ("button-breadboard", button), ("pot-breadboard", pot)):
        (OUT / f"{name}.svg").write_text(make())
    print("led-breadboard.svg・led-nowire.svg・button-breadboard.svg・pot-breadboard.svg を作りました")


if __name__ == "__main__":
    main()
