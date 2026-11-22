#!/usr/bin/env python3
"""ピコの教科書の7章（外付けの LED）の図を作る。

    python3 tools/make_led_figures.py

- books/pico/images/led-breadboard.svg  ブレッドボードへの差し方（ハーフサイズ・30列）
作り直したら python3 tools/translate_figures.py pico で英語の図も作り直す。
"""
from make_xmas_figures import OUT, INK, SUB, PICO, PIN, SIG, GND, VSYS, text, line, svg

P = 20                                   # 穴の間隔
X = lambda col: 90 + (col - 1) * P       # 列 → x
ROW = {r: 150 + i * P for i, r in enumerate("abcde")} | {r: 290 + i * P for i, r in enumerate("fghij")}
TOP_PLUS, TOP_MINUS, BOT_MINUS, BOT_PLUS = 72, 92, 404, 424
MARK = "#ffe27a"                         # 中でつながっている穴


def mark(n, x, y):
    """手順の番号（本文の手順と同じ）"""
    return [f'<circle cx="{x}" cy="{y}" r="10" fill="#ffffff" stroke="{INK}" stroke-width="1.5"/>',
            text(x, y + 4.5, str(n), 12, "middle", 700)]


def breadboard():
    b = [f'<rect x="70" y="50" width="{X(30) + 20 - 70}" height="390" rx="8" fill="#f2efe6" stroke="#d6cfbd" stroke-width="2"/>',
         f'<rect x="76" y="{ROW["e"] + 10}" width="{X(30) + 14 - 76}" height="{ROW["f"] - ROW["e"] - 20}" fill="#e2dccb"/>']
    # つながっている所に色: GP15（20番 = 11列）・抵抗と LED の列（7列）・GND（18番 = 13列）・上の − の列
    for col in (7, 11, 13):
        b.append(f'<rect x="{X(col) - 8}" y="{ROW["a"] - 8}" width="16" height="{ROW["e"] - ROW["a"] + 16}" rx="4" fill="{MARK}"/>')
    b.append(f'<rect x="{X(1) - 8}" y="{TOP_MINUS - 8}" width="{X(30) - X(1) + 16}" height="16" rx="4" fill="{MARK}"/>')
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
    # ピコ（USB を右に。上の列が 1〜20番で、20番が左端）
    c, h = ROW["c"], ROW["h"]
    b.append(f'<rect x="{X(11) - 12}" y="{c - 14}" width="{X(30) - X(11) + 24}" height="{h - c + 28}" rx="6" fill="{PICO}"/>')
    b.append(f'<rect x="{X(30) + 12}" y="{(c + h) / 2 - 12}" width="18" height="24" rx="2" fill="#b8bec7"/>')
    b.append(text(X(30) + 34, (c + h) / 2 + 4, "USB", 11, "start", 700, SUB))
    for col in range(11, 31):
        for y in (c, h):
            b.append(f'<circle cx="{X(col)}" cy="{y}" r="3.5" fill="{PIN}"/>')
    b.append(text((X(11) + X(30)) / 2 + 40, (c + h) / 2 + 6, "ピコ", 18, "middle", 700, "#ffffff"))
    b.append(line(X(13), c + 6, X(13), c + 18, "#ffffff", 1.2))
    b.append(text(X(13) + 6, c + 26, "GND（18番）", 11, "start", 700, "#ffffff"))
    b.append(line(X(11), c + 6, X(11), c + 42, "#ffffff", 1.2))
    b.append(text(X(11) + 6, c + 50, "GP15（20番）", 11, "start", 700, "#ffffff"))
    # 抵抗: 11列の b と 7列の b
    y = ROW["b"]
    b.append(line(X(7), y, X(11), y, "#8a8f98", 2))
    bx = (X(7) + X(11)) / 2
    b.append(f'<rect x="{bx - 24}" y="{y - 8}" width="48" height="16" rx="5" fill="#f4e3c4" stroke="#8a6d3b" stroke-width="1.5"/>')
    for j, col in enumerate(["#d93a3a", "#d93a3a", "#8b4513", "#c9a227"]):    # 220Ω: 赤・赤・茶・金
        b.append(f'<rect x="{bx - 15 + j * 9}" y="{y - 8}" width="5" height="16" fill="{col}"/>')
    for col in (7, 11):
        b.append(f'<circle cx="{X(col)}" cy="{y}" r="3.5" fill="{INK}"/>')
    # LED: 長い足は 7列の a、短い足は上の − の列
    lx, ly = X(7) + P / 2, (ROW["a"] + TOP_MINUS) / 2
    b.append(line(X(7), ROW["a"], lx - 3, ly, "#8a8f98", 2))
    b.append(line(X(8), TOP_MINUS, lx + 3, ly, "#8a8f98", 2))
    b.append(f'<circle cx="{lx}" cy="{ly}" r="9" fill="#ffcdd2" stroke="#d93a3a" stroke-width="2"/>')
    b.append(text(lx - 16, ROW["a"] - 6, "長い足（＋）", 11, "end", 700, "#d93a3a"))
    b.append(text(X(8) + 10, TOP_MINUS + 24, "短い足（−）", 11, "start", 700, INK))
    b.append(f'<circle cx="{X(7)}" cy="{ROW["a"]}" r="3.5" fill="#d93a3a"/>')
    b.append(f'<circle cx="{X(8)}" cy="{TOP_MINUS}" r="3.5" fill="{INK}"/>')
    # ワイヤー: 13列の a と上の − の列
    b.append(f'<path d="M{X(13)} {ROW["a"]} C{X(13) + 14} {ROW["a"] - 10} {X(13) + 14} {TOP_MINUS + 10} {X(13)} {TOP_MINUS}" '
             f'stroke="{GND}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    for yy in (ROW["a"], TOP_MINUS):
        b.append(f'<circle cx="{X(13)}" cy="{yy}" r="3.5" fill="{GND}"/>')
    # 手順の番号
    b += mark(2, X(22), ROW["h"] - 30)
    b += mark(3, bx, ROW["b"] + 22)
    b += mark(4, lx - 30, TOP_MINUS + 24)
    b += mark(5, X(13) + 28, (ROW["a"] + TOP_MINUS) / 2)
    b.append(text(70, 466, "番号は本文の手順（② ピコ　③ 抵抗　④ LED　⑤ ワイヤー）。黄色の所は、中でつながっている穴", 12, "start", 400, SUB))
    return svg(760, 486, "ブレッドボードへの差し方", b)


def main():
    (OUT / "led-breadboard.svg").write_text(breadboard())
    print("led-breadboard.svg を作りました")


if __name__ == "__main__":
    main()
