#!/usr/bin/env python3
"""ピコの教科書の10章（回路図の読み方）の図を作る。

    python3 tools/make_schematic_figures.py

- books/pico/images/sch-led.svg            同じ LED の回路を、絵と回路図で
- books/pico/images/sch-symbols.svg        よく出る部品の記号
- books/pico/images/sch-wires.svg          線がつながっている所・いない所
- books/pico/images/sch-names.svg          名前でつなぐ（ネット名と電源の記号）
- books/pico/images/sch-ic.svg             IC の箱の読み方
- books/pico/images/sch-camera-power.svg   カメラの基板（OV7670）の電源の部分
- books/pico/images/sch-camera-sensor.svg  カメラの基板のセンサーとコネクタ
作り直したら python3 tools/translate_figures.py pico で英語の図も作り直す。
"""
from make_xmas_figures import OUT, INK, SUB, PICO, PIN, VSYS, text, line, svg

W = 2                       # 線の太さ
NET = "#2f6fde"             # つながっている線の色（説明用）
OTHER = "#d93a3a"           # 別の線の色（説明用）
HI = "#e8590c"              # 目立たせる所（オレンジ）
BOX = "#fff8d6"             # IC の箱
L = 26                      # IC の足の長さ


def wire(*pts, color=INK, w=W):
    d = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f} {y:.1f}" for i, (x, y) in enumerate(pts))
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"/>'


def dot(x, y, color=INK):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.8" fill="{color}"/>'


def num(n, x, y):
    return [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{HI}"/>',
            text(x, y + 4.5, str(n), 13, "middle", 700, "#ffffff")]


def zig(x1, y1, x2, y2, color=INK):
    """(x1, y1) から (x2, y2) までの線の真ん中に、ギザギザ（抵抗）を入れる"""
    vert = x1 == x2
    a, b = (y1, y2) if vert else (x1, x2)
    c = (a + b) / 2
    s, e = c - 16, c + 16
    pts = [(a, 0), (s, 0)] + [(s + 4 + 8 * k, (-6 if k % 2 == 0 else 6)) for k in range(4)] + [(e, 0), (b, 0)]
    if vert:
        pts = [(x1 + o, p) for p, o in pts]
    else:
        pts = [(p, y1 + o) for p, o in pts]
    return wire(*pts, color=color)


def res(x1, y1, x2, y2, ref, val, side=1):
    """抵抗。ref と val は線の上（横向き）か右（縦向き）に書く"""
    out = [zig(x1, y1, x2, y2)]
    if x1 == x2:
        cy = (y1 + y2) / 2
        out += [text(x1 + 14, cy - 2, ref, 12, "start", 700), text(x1 + 14, cy + 13, val, 12, "start", 400, SUB)]
    else:
        cx = (x1 + x2) / 2
        out += [text(cx - 4, y1 - 12, ref, 12, "end", 700), text(cx + 4, y1 - 12, val, 12, "start", 400, SUB)]
    return out


def cap(x, y1, y2, ref="", val="", color=INK, right=True):
    """縦向きのコンデンサ。上が y1、下が y2"""
    cy = (y1 + y2) / 2
    out = [wire((x, y1), (x, cy - 4), color=color), wire((x, cy + 4), (x, y2), color=color),
           line(x - 12, cy - 4, x + 12, cy - 4, color, W + 1), line(x - 12, cy + 4, x + 12, cy + 4, color, W + 1)]
    if ref:
        tx, anc = (x + 17, "start") if right else (x - 17, "end")
        out += [text(tx, cy - 3, ref, 12, anc, 700), text(tx, cy + 12, val, 12, anc, 400, SUB)]
    return out


def cap_h(x1, x2, y, ref="", val=""):
    """横向きのコンデンサ"""
    cx = (x1 + x2) / 2
    out = [wire((x1, y), (cx - 4, y)), wire((cx + 4, y), (x2, y)),
           line(cx - 4, y - 12, cx - 4, y + 12, INK, W + 1), line(cx + 4, y - 12, cx + 4, y + 12, INK, W + 1)]
    if ref:
        out += [text(cx, y - 18, ref, 12, "middle", 700), text(cx, y + 26, val, 12, "middle", 400, SUB)]
    return out


def gnd(x, y, name="", color=INK):
    """GND の記号（下向きの三角）。(x, y) が線の端"""
    out = [wire((x, y), (x, y + 8), color=color),
           f'<path d="M{x - 10:.1f} {y + 8:.1f} L{x + 10:.1f} {y + 8:.1f} L{x:.1f} {y + 19:.1f} Z" fill="none" '
           f'stroke="{color}" stroke-width="{W}" stroke-linejoin="round"/>']
    if name:
        out.append(text(x, y + 33, name, 11, "middle", 700, color))
    return out


def agnd(x, y, name="AGND", color=INK):
    """アナログの GND の記号（短くなっていく横線）"""
    out = [wire((x, y), (x, y + 8), color=color), line(x - 11, y + 8, x + 11, y + 8, color, W),
           line(x - 7, y + 13, x + 7, y + 13, color, W), line(x - 3, y + 18, x + 3, y + 18, color, W)]
    if name:
        out.append(text(x, y + 32, name, 11, "middle", 700, color))
    return out


def pwr(x, y, name, color=VSYS):
    """電源の記号（T の字）。(x, y) が線の端で、記号は上に出す"""
    return [wire((x, y), (x, y - 12), color=color), line(x - 10, y - 12, x + 10, y - 12, color, W),
            text(x, y - 18, name, 12, "middle", 700, color)]


def ic(x, y, w, left, right, ref, part, pitch=22):
    """IC の箱。left・right は (ピンの番号, 名前) の並び。足の先の位置を名前で返す"""
    n = max(len(left), len(right))
    h = 14 + (n - 1) * pitch + 14
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{BOX}" stroke="{INK}" stroke-width="{W}"/>',
           text(x, y - 7, ref, 12, "start", 700), text(x, y + h + 16, part, 12, "start", 400, SUB)]
    pins = {}
    for side, pl in ((-1, left), (1, right)):
        for i, (pn, name) in enumerate(pl):
            py = y + 14 + i * pitch
            x0 = x if side < 0 else x + w
            x1 = x0 + side * L
            out.append(wire((x0, py), (x1, py)))
            out.append(text(x0 + side * 5, py - 4, pn, 10, "end" if side < 0 else "start", 400, SUB))
            out.append(text(x0 - side * 6, py + 4, name, 11, "start" if side < 0 else "end", 400))
            pins[name] = (x1, py)
    return out, pins, h


def led_h(x1, x2, y, color=INK, fill="none"):
    """横向きの LED（左がプラス）"""
    cx = (x1 + x2) / 2
    return [wire((x1, y), (cx - 9, y), color=color), wire((cx + 9, y), (x2, y), color=color),
            f'<path d="M{cx - 9:.1f} {y - 10:.1f} L{cx - 9:.1f} {y + 10:.1f} L{cx + 9:.1f} {y:.1f} Z" fill="{fill}" '
            f'stroke="{color}" stroke-width="{W}" stroke-linejoin="round"/>',
            line(cx + 9, y - 10, cx + 9, y + 10, color, W),
            arrow(cx - 1, y - 13, cx + 8, y - 24, color), arrow(cx + 6, y - 11, cx + 15, y - 22, color)]


def arrow(x1, y1, x2, y2, color=INK):
    return (f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f} M{x2 - 6:.1f} {y2 + 1:.1f} L{x2:.1f} {y2:.1f} '
            f'L{x2 - 1:.1f} {y2 + 6:.1f}" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>')


def diode_h(x1, x2, y):
    cx = (x1 + x2) / 2
    return [wire((x1, y), (cx - 9, y)), wire((cx + 9, y), (x2, y)),
            f'<path d="M{cx - 9:.1f} {y - 10:.1f} L{cx - 9:.1f} {y + 10:.1f} L{cx + 9:.1f} {y:.1f} Z" fill="none" '
            f'stroke="{INK}" stroke-width="{W}" stroke-linejoin="round"/>', line(cx + 9, y - 10, cx + 9, y + 10, INK, W)]


def panel(x, y, w, h, title, color=SUB):
    return [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#f7f8fa" stroke="#d5d9e0" stroke-width="1.5"/>',
            text(x + 14, y + 22, title, 13, "start", 700, color)]


# ---------------------------------------------------------------- 図

def sch_led():
    b = panel(20, 46, 350, 230, "絵（配線図）") + panel(390, 46, 350, 230, "回路図")
    # 絵: ピコ・抵抗・LED を本物に似た形で
    b.append(f'<rect x="40" y="96" width="120" height="140" rx="8" fill="{PICO}"/>')
    b.append(text(82, 172, "ピコ", 16, "middle", 700, "#ffffff"))
    for y, s in ((120, "GP15（20番）"), (212, "GND（18番）")):
        b.append(text(152, y + 4, s, 11, "end", 700, "#ffffff"))
        b.append(f'<circle cx="160" cy="{y}" r="5" fill="{PIN}"/>')
    b.append(line(166, 120, 205, 120, NET, 3))
    b.append(f'<rect x="205" y="112" width="48" height="16" rx="5" fill="#f4e3c4" stroke="#8a6d3b" stroke-width="1.5"/>')
    for j, c in enumerate(["#f08c00", "#f08c00", "#8b4513", "#c9a227"]):
        b.append(f'<rect x="{212 + j * 9}" y="112" width="5" height="16" fill="{c}"/>')
    b.append(text(229, 106, "抵抗", 11, "middle", 700, SUB))
    b.append(line(253, 120, 286, 120, NET, 3))
    b.append(line(286, 120, 286, 196, NET, 3))
    b.append(line(286, 196, 304, 196, NET, 3))
    # LED（丸い頭と、長い足・短い足）
    b.append(line(304, 150, 304, 196, "#8a8f98", 3))
    b.append(line(320, 150, 320, 180, "#8a8f98", 3))
    b.append(f'<path d="M296 150 L296 128 A16 16 0 0 1 328 128 L328 150 Z" fill="#ffcdd2" stroke="{OTHER}" stroke-width="2"/>')
    b.append(line(292, 150, 332, 150, OTHER, 3))
    b.append(text(338, 132, "LED", 11, "start", 700, OTHER))
    b.append(text(298, 176, "+", 12, "end", 700, OTHER))
    b.append(text(326, 172, "−", 12, "start", 700, INK))
    b.append(line(320, 180, 340, 180, INK, 3))
    b.append(line(340, 180, 340, 212, INK, 3))
    b.append(line(340, 212, 166, 212, INK, 3))
    b.append(text(196, 262, "本物に近い形と並びで描く", 11, "start", 400, SUB))
    # 回路図: 同じつながりを記号で
    p, pins, h = ic(420, 104, 70, [], [("20", "GP15"), ("18", "GND")], "ピコ", "", pitch=88)
    b += p
    x0, y0 = pins["GP15"]
    _, yg = pins["GND"]
    b += res(x0, y0, x0 + 80, y0, "R1", "330Ω")
    b += led_h(x0 + 80, x0 + 150, y0)
    b.append(text(x0 + 115, y0 + 28, "D1", 12, "middle", 700))
    b.append(wire((x0 + 150, y0), (x0 + 190, y0), (x0 + 190, yg), (x0, yg)))
    b.append(text(565, 262, "決まった記号で、つながりだけを描く", 11, "middle", 400, SUB))
    return svg(760, 290, "同じ LED の回路を、絵と回路図で", b)


def sch_symbols():
    b = []
    cells = []
    cw, ch = 180, 142
    for r in range(2):
        for c in range(4):
            cells.append((20 + c * (cw + 6), 46 + r * (ch + 8)))

    def cell(i, name, letter):
        x, y = cells[i]
        b.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="8" fill="#f7f8fa" stroke="#d5d9e0" stroke-width="1.5"/>')
        b.append(text(x + cw / 2, y + ch - 30, name, 13, "middle", 700))
        b.append(text(x + cw / 2, y + ch - 12, letter, 12, "middle", 400, SUB))
        return x + cw / 2, y + 50

    cx, cy = cell(0, "抵抗", "R")
    b.append(zig(cx - 50, cy - 10, cx + 50, cy - 10))
    b.append(wire((cx - 50, cy + 22), (cx - 18, cy + 22)))
    b.append(f'<rect x="{cx - 18}" y="{cy + 15}" width="36" height="14" fill="none" stroke="{INK}" stroke-width="{W}"/>')
    b.append(wire((cx + 18, cy + 22), (cx + 50, cy + 22)))
    cx, cy = cell(1, "コンデンサ", "C")
    b += [wire((cx - 50, cy), (cx - 5, cy)), wire((cx + 5, cy), (cx + 50, cy)),
          line(cx - 5, cy - 16, cx - 5, cy + 16, INK, W + 1), line(cx + 5, cy - 16, cx + 5, cy + 16, INK, W + 1)]
    cx, cy = cell(2, "電解コンデンサ（＋ − あり）", "C")
    b += [wire((cx - 50, cy), (cx - 5, cy)), wire((cx + 7, cy), (cx + 50, cy)),
          line(cx - 5, cy - 16, cx - 5, cy + 16, INK, W + 1),
          f'<path d="M{cx + 11} {cy - 16} Q{cx + 3} {cy} {cx + 11} {cy + 16}" fill="none" stroke="{INK}" stroke-width="{W + 1}"/>',
          text(cx - 16, cy - 10, "+", 14, "middle", 700)]
    cx, cy = cell(3, "LED", "D・LED")
    b += led_h(cx - 50, cx + 50, cy + 6)
    cx, cy = cell(4, "ダイオード", "D")
    b += diode_h(cx - 50, cx + 50, cy)
    cx, cy = cell(5, "スイッチ", "SW")
    b += [wire((cx - 50, cy + 6), (cx - 18, cy + 6)), dot(cx - 18, cy + 6), wire((cx - 18, cy + 6), (cx + 16, cy - 10)),
          dot(cx + 18, cy + 6), wire((cx + 18, cy + 6), (cx + 50, cy + 6))]
    cx, cy = cell(6, "IC（チップ）", "U・IC")
    p, _, _ = ic(cx - 26, cy - 30, 52, [("1", ""), ("2", "")], [("4", ""), ("3", "")], "", "", pitch=34)
    b += p
    b.append(text(cx, cy - 8, "U1", 12, "middle", 700))
    cx, cy = cell(7, "コネクタ（ピン）", "J・P・CN")
    b.append(f'<rect x="{cx - 22}" y="{cy - 32}" width="44" height="62" fill="{BOX}" stroke="{INK}" stroke-width="{W}"/>')
    for k in range(3):
        y = cy - 20 + k * 19
        b += [wire((cx - 44, y), (cx - 22, y)), wire((cx + 22, y), (cx + 44, y)),
              text(cx - 6, y + 4, str(2 * k + 1), 10, "end", 400, SUB), text(cx + 6, y + 4, str(2 * k + 2), 10, "start", 400, SUB)]
    return svg(760, 360, "よく出る部品の記号（下は、部品の番号の頭の文字）", b)


def sch_wires():
    b = []
    xs = [20, 266, 512]
    titles = [("点がある", "つながっている", NET), ("点がない", "つながっていない", OTHER), ("T の字", "つながっている", NET)]
    for i, x in enumerate(xs):
        b += panel(x, 46, 228, 210, "")
        cx, cy = x + 114, 130
        t1, t2, c = titles[i]
        if i == 0:
            b += [wire((cx - 70, cy), (cx + 70, cy), color=NET, w=3), wire((cx, cy - 60), (cx, cy + 60), color=NET, w=3), dot(cx, cy, NET)]
        elif i == 1:
            b += [wire((cx - 70, cy), (cx + 70, cy), color=NET, w=3), wire((cx, cy - 60), (cx, cy + 60), color=OTHER, w=3)]
        else:
            b += [wire((cx - 70, cy), (cx + 70, cy), color=NET, w=3), wire((cx, cy), (cx, cy + 60), color=NET, w=3), dot(cx, cy, NET)]
        b.append(text(cx, 222, t1, 13, "middle", 700))
        b.append(text(cx, 242, "→ " + t2, 13, "middle", 700, c))
    b.append(text(380, 282, "色は説明のため。同じ色の線は、つながっていて同じ電圧（本物の回路図はふつう全部黒）", 12, "middle", 400, SUB))
    return svg(760, 300, "線がつながっている所と、つながっていない所", b)


def sch_names():
    b = panel(20, 46, 420, 250, "同じ名前どうしは、つながっている") + panel(456, 46, 284, 250, "電源と GND の記号")
    # 左: コネクタの 3番 SIO_C と U3 の 3番 SIO_C
    b.append(f'<rect x="60" y="130" width="44" height="66" fill="{BOX}" stroke="{INK}" stroke-width="{W}"/>')
    b.append(text(60, 214, "camera", 12, "start", 700))
    for k, (pn, nm, col) in enumerate((("3", "SIO_C", HI), ("5", "VSYNC", INK))):
        y = 148 + k * 30
        b.append(wire((104, y), (170, y), color=col))
        b.append(text(108, y - 4, pn, 10, "start", 400, SUB))
        b.append(text(170, y - 5, nm, 12, "end", 700, col))
    p, pins, h = ic(330, 134, 60, [("3", "SIO_C"), ("13", "VSYNC")], [], "", "", pitch=30)
    b += p
    b.append(text(330, 214, "U3", 12, "start", 700))
    for k, (nm, col) in enumerate((("SIO_C", HI), ("VSYNC", INK))):
        y = 148 + k * 30
        b.append(wire((250, y), (304, y), color=col))
        b.append(text(250, y - 5, nm, 12, "start", 700, col))
    b.append(f'<path d="M150 128 C170 100 260 100 280 128" fill="none" stroke="{HI}" stroke-width="2" stroke-dasharray="5 4"/>')
    b.append(text(215, 96, "線がなくても、つながっている", 12, "middle", 700, HI))
    b.append(text(40, 254, "線の先に付けた名前（ネット名）が同じなら、", 12, "start", 400, SUB))
    b.append(text(40, 272, "そこまで線を引いたのと同じ", 12, "start", 400, SUB))
    # 右: 電源と GND の記号
    items = [(500, "3V3", "3.3V"), (566, "2V8", "2.8V")]
    for x, nm, v in items:
        b += pwr(x, 140, nm)
        b.append(wire((x, 140), (x, 152), color=VSYS))
        b.append(text(x, 172, v, 12, "middle", 400, SUB))
    b += gnd(636, 112, "GND")
    b += agnd(700, 112, "AGND")
    b.append(text(668, 172, "0V", 12, "middle", 400, SUB))
    b.append(text(476, 214, "同じ名前の電源の記号どうし、", 12, "start", 400, SUB))
    b.append(text(476, 232, "GND の記号どうしは、", 12, "start", 400, SUB))
    b.append(text(476, 250, "全部つながっている", 12, "start", 400, SUB))
    return svg(760, 314, "名前でつなぐ", b)


def sch_ic():
    b = []
    p, pins, h = ic(310, 86, 120, [("1", "VIN"), ("2", "GND"), ("3", "EN")], [("5", "OUT"), ("4", "BYT")], "U1", "PAM3101DAB28")
    b += p
    # ① 部品の番号
    b += num(1, 180, 72)
    b.append(text(196, 77, "部品の番号", 12, "start", 700))
    b.append(wire((262, 73), (304, 78), color=HI, w=1.5))
    # ② 型番
    b += num(2, 200, 196)
    b.append(text(216, 201, "型番（データシートを探す名前）", 12, "start", 700))
    b.append(wire((310, 186), (310, 172), color=HI, w=1.5))
    # ③ ピンの番号（箱の外）
    b += num(3, 560, 72)
    b.append(text(576, 77, "ピンの番号（箱の外）", 12, "start", 700))
    b.append(wire((554, 82), (442, 96), color=HI, w=1.5))
    # ④ ピンの名前（箱の中）
    b += num(4, 560, 136)
    b.append(text(576, 141, "ピンの名前（箱の中）", 12, "start", 700))
    b.append(wire((550, 132), (420, 103), color=HI, w=1.5))
    b.append(text(380, 248, "箱の中の並びは、本物の足の並びとはちがう（読みやすい順に並べてある）", 12, "middle", 400, SUB))
    return svg(760, 268, "IC の箱の読み方", b)


def regulator(b, y, src, ref, part, cin, byt, out):
    """3.3V か 2.8V を下げる IC（U1・U2）と、まわりのコンデンサ。ブロックの下の GND の線の y を返す"""
    gy = y + 156
    b += pwr(30, y, src)
    b.append(wire((30, y), (209, y)))
    for x, r, v in cin:
        b.append(dot(x, y))
        b += cap(x, y, gy, r, v)
        b.append(dot(x, gy))
    p, u, h = ic(235, y - 14, 110, [("1", "VIN"), ("2", "GND"), ("3", "EN")], [("5", "OUT"), ("4", "BYT")], ref, part)
    b += p
    # EN は VIN につなぐ。GND の足の線とは交差するが、点がないのでつながっていない
    b.append(dot(185, y))
    b.append(wire((185, y), (185, u["EN"][1]), (209, u["EN"][1])))
    b.append(wire((209, u["GND"][1]), (197, u["GND"][1]), (197, gy)))
    b.append(dot(197, gy))
    xo, yb = u["BYT"]
    b.append(wire((xo, yb), (405, yb)))
    b += cap(405, yb, gy, *byt)
    b.append(dot(405, gy))
    b.append(wire((u["OUT"][0], y), (out, y)))
    return gy


def sch_camera_power():
    b = []
    top = 80
    gy = regulator(b, top, "3V3", "U1", "PAM3101DAB28", [(60, "C2", "10uF"), (125, "C3", "1uF")], ("C4", "10nF"), 530)
    b.append(dot(455, top))
    b += cap(455, top, gy, "C5", "10uF")
    b.append(wire((60, gy), (455, gy)))
    b += gnd(455, gy, "GND")
    b += pwr(495, top, "2V8")
    b.append(dot(495, top))
    # R1 → AVDD（C1 は AGND へ）
    b.append(dot(530, top))
    b += res(530, top, 620, top, "R1", "10")
    b.append(wire((620, top), (690, top)))
    b.append(dot(690, top))
    b += pwr(690, top, "AVDD")
    b += cap(690, top, top + 62, "C1", "4.7uF")
    b += agnd(690, top + 62, "AGND")
    # R2 → DOVDD（C10・C11 は GND へ）
    yd, gd = top + 124, top + 196
    b += res(530, top, 530, yd, "R2", "10")
    b.append(wire((530, yd), (720, yd)))
    b.append(dot(580, yd))
    b.append(dot(640, yd))
    b += pwr(640, yd, "DOVDD")
    b += cap(580, yd, gd, "C10", "4.7uF")
    b += cap(720, yd, gd, "C11", "0.1uF", right=False)
    b.append(wire((580, gd), (720, gd)))
    b.append(dot(650, gd))
    b += gnd(650, gd, "GND")
    # 下の段: 2V8 → U2 → DVDD（1.8V）
    t2 = 340
    g2 = regulator(b, t2, "2V8", "U2", "PAM3101DAB180", [(90, "C6", "1uF")], ("C7", "10nF"), 495)
    b += pwr(495, t2, "DVDD")
    b.append(wire((90, g2), (405, g2)))
    b += gnd(405, g2, "GND")
    # 番号（本文の ①〜④）
    b += num(1, 290, 40)
    b += num(2, 92, 118)
    b += num(3, 575, 40)
    b += num(4, 290, 300)
    b.append(text(380, 560, "uF は µF（マイクロファラッド）。抵抗の 10 は 10Ω", 12, "middle", 400, SUB))
    return svg(760, 578, "カメラの基板（OV7670）の電源の部分", b)


def sch_camera_sensor():
    b = []
    # 左: コネクタ（2列×9本）。奇数のピンが左、偶数のピンが右
    hx, hy, pitch = 140, 116, 26
    odd = ["3V3", "SIO_C", "VSYNC", "PCLK", "D7", "D5", "D3", "D1", "RESET"]
    even = ["GND", "SIO_D", "HREF", "XCLK", "D6", "D4", "D2", "D0", "PWDN"]
    b.append(f'<rect x="{hx}" y="{hy - 16}" width="60" height="{8 * pitch + 32}" fill="{BOX}" stroke="{INK}" stroke-width="{W}"/>')
    b.append(text(hx, hy - 23, "camera", 12, "start", 700))
    for k in range(9):
        y = hy + k * pitch
        b.append(text(hx + 22, y + 4, str(2 * k + 1), 10, "end", 400, SUB))
        b.append(text(hx + 38, y + 4, str(2 * k + 2), 10, "start", 400, SUB))
        for side, nm in ((-1, odd[k]), (1, even[k])):
            x0 = hx if side < 0 else hx + 60
            if nm == "3V3":
                b.append(wire((x0, y), (x0 - 30, y)))
                b += pwr(x0 - 30, y, "3V3")
            elif nm == "GND":
                b.append(wire((x0, y), (x0 + 90, y)))
                b += gnd(x0 + 90, y)
            else:
                col = HI if nm == "SIO_C" else INK
                x1 = x0 + side * 64
                b.append(wire((x0, y), (x1, y), color=col))
                b.append(text(x1, y - 5, nm, 11, "start" if side < 0 else "end", 700, col))
    # 右: U3（OV7670）
    left = [("1", "AVDD"), ("2", "SIO_D"), ("3", "SIO_C"), ("9", "D0"), ("4", "D1"), ("10", "D2"), ("5", "D3"),
            ("24", "D4"), ("19", "D5"), ("23", "D6"), ("18", "D7"), ("8", "AGND")]
    right = [("20", "DOVDD"), ("11", "DVDD"), ("6", "PWDN"), ("21", "RESET"), ("17", "XCLK"), ("15", "PCLK"),
             ("14", "HREF"), ("13", "VSYNC"), ("16", "STROBE"), ("12", "VREF1"), ("7", "VREF2"), ("22", "DOGND")]
    p, u3, h = ic(430, 66, 120, left, right, "U3", "OV7670", pitch=24)
    b += p
    for _, nm in left[1:-1]:
        x, y = u3[nm]
        col = HI if nm == "SIO_C" else INK
        b.append(wire((x, y), (x - 50, y), color=col))
        b.append(text(x - 50, y - 5, nm, 11, "start", 700, col))
    # AVDD: C12 で AGND へ
    x, y = u3["AVDD"]
    b.append(wire((x, y), (x - 46, y)))
    b.append(dot(x - 46, y))
    b.append(text(x - 46, y - 5, "AVDD", 11, "start", 700, VSYS))
    b += cap_h(x - 96, x - 46, y)
    b.append(text(x - 71, y - 16, "C12", 11, "middle", 700))
    b += agnd(x - 96, y, "")
    x, y = u3["AGND"]
    b.append(wire((x, y), (x - 16, y)))
    b += agnd(x - 16, y, "")
    for _, nm in right[2:-3]:
        x, y = u3[nm]
        b.append(wire((x, y), (x + 50, y)))
        b.append(text(x + 50, y - 5, nm, 11, "end", 700))
    # DOVDD・DVDD は C13・C14 で GND へ。VREF1・VREF2 は C16・C15 で AGND へ
    for nm, cx, ref, color in (("DOVDD", 715, "C13", VSYS), ("DVDD", 665, "C14", VSYS),
                               ("VREF1", 715, "C16", INK), ("VREF2", 665, "C15", INK)):
        x, y = u3[nm]
        b.append(wire((x, y), (cx, y)))
        b.append(text(x + 50, y - 5, nm, 11, "end", 700, color))
        b.append(dot(x + 50, y) if color == VSYS else "")
        if color == VSYS:
            yb = u3["DVDD"][1] + 70
            b += cap(cx, y, yb)
            b += gnd(cx, yb)
        else:
            yb = u3["DOGND"][1] + 6
            b += cap(cx, y, yb)
            b += agnd(cx, yb, "")
        b.append(text(cx + 16, (y + yb) / 2 + 4 + (10 if cx == 715 else 0), ref, 11, "start", 700))
    x, y = u3["DOGND"]
    b.append(wire((x, y), (x + 20, y)))
    b += gnd(x + 20, y)
    # 番号（本文の ①〜③）
    b += num(1, 218, 87)
    b += num(2, 330, 128)
    b += num(3, 735, 52)
    b.append(text(380, 420, "C12〜C16 は全部 0.1uF", 12, "middle", 400, SUB))
    return svg(760, 438, "カメラの基板のセンサー（U3）とコネクタ", b)


def main():
    figs = {"sch-led.svg": sch_led, "sch-symbols.svg": sch_symbols, "sch-wires.svg": sch_wires,
            "sch-names.svg": sch_names, "sch-ic.svg": sch_ic, "sch-camera-power.svg": sch_camera_power,
            "sch-camera-sensor.svg": sch_camera_sensor}
    for name, f in figs.items():
        (OUT / name).write_text(f())
    print(f"{len(figs)} 枚の図を作りました")


if __name__ == "__main__":
    main()
