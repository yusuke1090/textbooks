#!/usr/bin/env python3
"""ピコの教科書の付録G（クリスマスのイルミネーション）の動画を作る（使い方は tools/video.py）。

    .venv/bin/python tools/make_xmas_videos.py [名前 …]                # 動画を作る
    .venv/bin/python tools/make_xmas_videos.py --still フォルダ 名前 5 20   # その秒のコマを PNG にして見る

- xmas-hang  LED を赤黒の2芯の線で延ばして、ツリーの木にかける（字幕は付録G の「ツリーの木にかける」の手順①〜⑩）
"""
import math
import sys

from make_xmas_figures import COLORS, BANDS, PICO, VSYS, SIG, battery
from make_pico_videos import iron, solder_wire, mix, SOLDER
from video import Steps, frame, group, draw_path, render, text, clamp, ease, INK, SUB

RED, BLK, COPPER, TAPE, JUMP, MALE, LEG = "#d93a3a", "#2b2f36", "#c87533", "#f3e2a9", "#9aa0a8", "#3a3f47", "#8a8f98"
ORANGE = "#f08c00"
CX = 400                                  # 大きく描く LED の真ん中


def ln(x1, y1, x2, y2, c, w=3):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" '
            f'stroke-width="{w}" stroke-linecap="round"/>')


def nipper(x, y, closed, rot=0, sc=1.0, op=1.0, label=False):
    """ニッパー。刃の先が (x, y)。rot=0 で持ち手が下、90 で左、-90 で右。closed=1 で閉じる"""
    a = (1 - clamp(closed)) * 14

    def half(s):
        return (f'<g transform="rotate({-s * a:.2f})">'
                f'<path d="M0 0 L{-s * 10} -14 L{-s * 2} -30 L0 -30 Z" fill="#6b7280"/>'
                f'<line x1="0" y1="0" x2="{s * 9}" y2="30" stroke="#6b7280" stroke-width="7" stroke-linecap="round"/>'
                f'<line x1="{s * 9}" y1="30" x2="{s * 24}" y2="100" stroke="{RED}" stroke-width="12" stroke-linecap="round"/></g>')
    b = [f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot}) scale({sc}) translate(0 30)">',
         half(1), half(-1), '<circle cx="0" cy="0" r="4" fill="#3a3f47"/>', "</g>"]
    if label:
        b.append(text(x + 46 * sc, y + 120 * sc, "ニッパー", 14, "start", 700, SUB))
    return group(b, opacity=op)


def copper_h(x0, x1, y, twist=0.0, h=14):
    """むいた先の細い線（横）。twist=1 でねじってある"""
    k = 1 - 0.55 * twist
    b = [ln(x0, y + (j - 1.5) * h / 4 * k, x1, y + (j - 1.5) * h / 4 * k, COPPER, 2.2) for j in range(4)]
    if twist > 0:
        for xx in range(int(x0), int(x1) - 3, 6):
            b.append(f'<line x1="{xx}" y1="{y - h * k / 2:.1f}" x2="{xx + 5}" y2="{y + h * k / 2:.1f}" '
                     f'stroke="#9c5420" stroke-width="1.6" opacity="{twist:.2f}"/>')
    return b


def copper_v(x, y0, y1, w=6):
    """ねじった細い線（縦）"""
    b = [f'<rect x="{x - w / 2:.1f}" y="{y0:.1f}" width="{w}" height="{y1 - y0:.1f}" rx="2" fill="{COPPER}"/>']
    for yy in range(int(y0) + 2, int(y1) - 3, 5):
        b.append(f'<line x1="{x - w / 2:.1f}" y1="{yy}" x2="{x + w / 2:.1f}" y2="{yy + 4}" stroke="#9c5420" stroke-width="1.4"/>')
    return b


def male_h(x, y, side):
    """横の線の先のオス。side=-1 で x の左、1 で右"""
    x0 = x if side > 0 else x - 30
    px = x + 30 if side > 0 else x - 44
    return [f'<rect x="{px}" y="{y - 1.5}" width="14" height="3" fill="#c9ced6"/>',
            f'<rect x="{x0}" y="{y - 7}" width="30" height="14" rx="2" fill="{MALE}"/>']


def bracket(x1, x2, y, label, color=SUB, above=True):
    """長さの目盛り（横）"""
    d = -1 if above else 1
    return [ln(x1, y, x2, y, color, 1.5), ln(x1, y - 5, x1, y + 5, color, 1.5), ln(x2, y - 5, x2, y + 5, color, 1.5),
            text((x1 + x2) / 2, y + d * 9 + (0 if above else 9), label, 14, "middle", 700, color)]


def dimmed(body, op):
    return group(body, opacity=op)


def solder_seq(st, t, i, d, x, y):
    """手順 i の d 秒後から、(x, y) をはんだ付けする。(こてとはんだの絵, はんだの量 0〜1)"""
    p_in = st.p(t, i, 0.6, d)
    out = st.p(t, i, 0.4, d + 2.2)
    heat = clamp((st.local(t, i) - st.lead - d - 0.6) / 0.5) * (1 - out)
    p_sol = st.p(t, i, 0.5, d + 0.7) * (1 - st.p(t, i, 0.4, d + 1.9))
    fill = st.p(t, i, 0.8, d + 1.0)
    b = []
    if p_sol > 0:
        b += group(solder_wire(x - 2, y, p_sol, fill), opacity=min(1, p_sol * 3))
    p_iron = p_in * (1 - out)
    if p_iron > 0:
        b += group(iron(x + 2, y, p_iron, heat), opacity=min(1, p_iron * 3))
    return b, fill


# ---------------------------------------------------------------- 場面ごとの絵
def s_usb(p_usb, p_off):
    """① USB を抜き、電池のスイッチを切る"""
    b = [f'<rect x="150" y="130" width="380" height="140" rx="8" fill="#f2efe6" stroke="#d6cfbd" stroke-width="2"/>',
         f'<rect x="320" y="160" width="150" height="80" rx="5" fill="{PICO}"/>',
         f'<rect x="470" y="188" width="18" height="24" rx="2" fill="#b8bec7"/>',
         text(240, 205, "ブレッドボード", 14, "middle", 700, SUB)]
    x = 488 + p_usb * 150
    b += group([f'<rect x="{x:.1f}" y="186" width="40" height="28" rx="3" fill="{MALE}"/>',
                ln(x + 40, 200, x + 420, 200, MALE, 9)], opacity=1 - 0.8 * p_usb)
    b += dimmed([text(600, 170, "USB を抜く", 15, "start", 700, INK)], min(1, p_usb * 2))
    bx, by, bw, bh = 560, 290, 190, 64
    b += [ln(bx, by + 22, 500, 262, VSYS, 3), ln(bx, by + 42, 470, 266, BLK, 3)]
    b += battery(bx, by, bw, bh)
    b += [f'<rect x="{bx + bw - 30}" y="{by + 8}" width="22" height="48" rx="3" fill="#8a8f98"/>',
          f'<rect x="{bx + bw - 27}" y="{by + 11 + 24 * p_off:.1f}" width="16" height="20" rx="2" fill="#ffffff"/>']
    b.append(text(bx + bw + 8, by + 24, "ON", 13, "start", 700, SUB if p_off > 0.5 else INK))
    b.append(text(bx + bw + 8, by + 52, "OFF", 13, "start", 700, RED if p_off > 0.5 else SUB))
    b.append(text(bx + bw / 2 - 15, by + bh + 22, "電池ボックス", 14, "middle", 700, SUB))
    return b


def s_cut(closed, sep, p_nip, p_lab):
    """② ジャンパーワイヤーを真ん中で切る"""
    y, d = 200, 32 * sep
    b = []
    if sep <= 0:
        b += [ln(220, y, 580, y, JUMP, 6)]
    else:
        b += [ln(220 - d, y, 400 - d - 2, y, JUMP, 6), ln(402 + d, y, 580 + d, y, JUMP, 6),
              f'<rect x="{396 - d:.1f}" y="{y - 3}" width="4" height="6" fill="{COPPER}"/>',
              f'<rect x="{402 + d:.1f}" y="{y - 3}" width="4" height="6" fill="{COPPER}"/>']
    b += male_h(220 - d, y, -1) + male_h(580 + d, y, 1)
    b += nipper(400, y - 14, closed, op=p_nip * (1 - sep), label=True)
    b += dimmed([text(300 - d, y + 40, "オスの付いた線", 14, "middle", 700, INK),
                 text(500 + d, y + 40, "オスの付いた線", 14, "middle", 700, INK),
                 text(400, y + 110, "10本切ると、20本できる", 16, "middle", 700, RED)], p_lab)
    return b


def s_strip(p_nip, p, p_dim):
    """② 切った先を 5mm むく"""
    y = 200
    b = [f'<rect x="20" y="{y - 3}" width="30" height="6" fill="#c9ced6"/>',
         f'<rect x="50" y="{y - 15}" width="90" height="30" rx="3" fill="{MALE}"/>',
         f'<rect x="140" y="{y - 12}" width="420" height="24" rx="3" fill="{JUMP}"/>']
    b += copper_h(560, 640, y, 0, 16)
    b += group([f'<rect x="560" y="{y - 12}" width="80" height="24" rx="3" fill="{JUMP}"/>'], dx=90 * p, opacity=1 - p)
    b += nipper(560 + 90 * p, y - 18, 0.85, op=p_nip * (1 - clamp((p - 0.7) / 0.3)))
    b += dimmed(bracket(560, 640, y - 34, "5mm", RED), p_dim)
    b += dimmed([text(350, y + 48, "切った先", 14, "middle", 700, SUB)], 1 - p_dim)
    return b


TREE = [(30, 120, 55), (85, 205, 95), (150, 290, 135)]        # 上・下・半分の幅（⑨⑩ の大きさ）


def tree(tx, s=1.0, dy=0.0, op=1.0):
    b = []
    for top, bottom, half in TREE:
        b.append(f'<path d="M{tx} {dy + top * s:.1f} L{tx + half * s:.1f} {dy + bottom * s:.1f} L{tx - half * s:.1f} {dy + bottom * s:.1f} Z" '
                 f'fill="#3f8f4a" stroke="#2e6b36" stroke-width="2" stroke-linejoin="round"/>')
    b.append(f'<rect x="{tx - 12 * s:.1f}" y="{dy + 290 * s:.1f}" width="{24 * s:.1f}" height="{40 * s:.1f}" fill="#8b5a2b"/>')
    sy = dy + 14 * s
    b.append(f'<path d="M0 0 L5 12 L17 12 L7 19 L11 31 L0 23 L-11 31 L-7 19 L-17 12 L-5 12 Z" fill="#f2c200" '
             f'transform="translate({tx} {sy - 14 * s:.1f}) scale({s})"/>')
    return group(b, opacity=op)


def s_length(p_meas, p_wire, p_dim, p_nip, closed):
    """③ 2芯の線を、根元から枝までの長さ＋20cm に切る"""
    tx, s, dy = 180, 0.82, 40
    b = tree(tx, s, dy)
    base = dy + 330 * s
    b.append(f'<rect x="{tx - 62}" y="{base:.1f}" width="100" height="24" rx="4" fill="#f2efe6" stroke="#d6cfbd" stroke-width="2"/>')
    spot = (tx - 46, dy + 150 * s)
    b.append(f'<circle cx="{spot[0]}" cy="{spot[1]:.1f}" r="8" fill="#ffcdd2" stroke="{RED}" stroke-width="2"/>')
    d = f"M{tx} {base:.1f} L{tx} {spot[1] + 22:.1f} L{spot[0] + 8} {spot[1] + 4:.1f}"
    b += draw_path(d, ORANGE, p_meas, 4)
    x0, L, y = 360, 380, 200
    xe = x0 + L * p_wire
    if p_wire > 0:
        b += [ln(x0, y - 4, xe, y - 4, RED, 7), ln(x0, y + 4, xe, y + 4, BLK, 7)]
    b += dimmed(bracket(x0, x0 + 300, y - 34, "根元から枝まで", ORANGE) + bracket(x0 + 300, x0 + L, y - 34, "＋20cm", RED), p_dim)
    b += nipper(x0 + L, y - 14, closed, op=p_nip)
    return b


SPLIT_X, END_X, TIP_X = 380, 520, 580


def pair_end(p_split, p_strip, twist):
    """2芯の線のはし。赤と黒を裂いて、先をむいてねじる。(絵, 赤の y, 黒の y)"""
    off = 52 * p_split
    yr, yb = 193.5 - off, 206.5 + off
    b = [ln(40, 193.5, SPLIT_X, 193.5, RED, 13), ln(40, 206.5, SPLIT_X, 206.5, BLK, 13)]
    for y0, y1, c in ((193.5, yr, RED), (206.5, yb, BLK)):
        b.append(f'<path d="M{SPLIT_X} {y0} C{SPLIT_X + 60} {y0} {END_X - 60} {y1:.1f} {END_X} {y1:.1f}" stroke="{c}" '
                 f'stroke-width="13" fill="none"/>')
    for y1, c in ((yr, RED), (yb, BLK)):
        b += copper_h(END_X, TIP_X, y1, twist, 11)
        b += group([f'<rect x="{END_X}" y="{y1 - 6.5:.1f}" width="{TIP_X - END_X}" height="13" fill="{c}"/>'],
                   dx=80 * p_strip, opacity=1 - p_strip)
    return b, yr, yb


def s_split(p_split, p_d3, p_strip, p_d5, twist, p_tw, p_other):
    """④ 両はしで赤と黒を 3cm 裂いて、先を 5mm むいて、ねじる"""
    b, yr, yb = pair_end(p_split, p_strip, twist)
    b += dimmed(bracket(SPLIT_X, END_X, 112, "3cm", ORANGE), p_d3)
    b += dimmed(bracket(END_X, TIP_X, 112, "5mm", RED), p_d5)
    b += dimmed([text(TIP_X + 16, yr + 5, "ねじる", 14, "start", 700, INK),
                 text(TIP_X + 16, yb + 5, "ねじる", 14, "start", 700, INK)], p_tw)
    b += dimmed([text(40, 290, "反対のはしも同じようにする", 14, "start", 700, SUB)], p_other)
    return b


def jumper_half(x, y, dx):
    """右から来る、半分に切ったジャンパー（むいた先が x）"""
    return group(copper_h(x, x + 60, y, 0.6, 9) +
                 [f'<rect x="{x + 60}" y="{y - 5}" width="120" height="10" rx="2" fill="{JUMP}"/>'] +
                 male_h(x + 180, y, 1), dx=dx)


def s_join(st, t, i):
    """⑤ 片方のはしの赤と黒に、オスの付いた線をはんだ付けする"""
    b, yr, yb = pair_end(1, 1, 1)
    tools = []
    for k, y in enumerate((yr, yb)):
        p_in = st.p(t, i, 0.8, 0.2 * k)
        b += jumper_half(END_X, y + 6, (1 - p_in) * 260)
        tb, fill = solder_seq(st, t, i, 1.0 + 2.6 * k, (END_X + TIP_X) / 2, y + 3)
        if fill > 0:
            b.append(f'<ellipse cx="{(END_X + TIP_X) / 2}" cy="{y + 3:.1f}" rx="{34 * fill:.1f}" ry="{10 * fill:.1f}" '
                     f'fill="{SOLDER}" stroke="#9aa1ab" stroke-width="1"/>')
        tools += tb
    b += dimmed([text(790, yb + 36, "オスの付いた線", 14, "end", 700, INK)], st.p(t, i, 0.4, 0.8))
    return b + tools


def led_big(top, long_len=150, short_len=125, cut_long=None, cut_short=None, fall=(0, 0), labels=True):
    """大きく描いた LED。足は CX-12（長い足・＋）と CX+12（短い足・−）。cut_* で切る y、fall で切った先が落ちる"""
    b = []
    for k, (x, length, cut) in enumerate(((CX - 12, long_len, cut_long), (CX + 12, short_len, cut_short))):
        y0, y1 = top + 68, top + 68 + length
        if cut is None:
            b.append(ln(x, y0, x, y1, LEG, 3))
        else:
            b.append(ln(x, y0, x, cut, LEG, 3))
            q = fall[k]
            if q < 1:
                b += group([ln(x, cut + 2, x, y1, LEG, 3)], dy=70 * q, opacity=1 - q)
    b += [f'<path d="M{CX - 25} {top + 60} L{CX - 25} {top + 25} A25 25 0 0 1 {CX + 25} {top + 25} L{CX + 25} {top + 60} Z" '
          f'fill="#ffcdd2" stroke="{RED}" stroke-width="2.5"/>',
          f'<rect x="{CX - 29}" y="{top + 60}" width="58" height="8" rx="2" fill="#ffcdd2" stroke="{RED}" stroke-width="2.5"/>']
    if labels:
        b += [text(CX - 36, top + 44, "長い足（＋）", 14, "end", 700, RED), text(CX + 36, top + 44, "短い足（−）", 14, "start", 700, INK)]
    return b


CUT_Y = 158                                  # 足を切る所（つばから 1cm）
JR, JB = CX - 12 - 5, CX + 12 + 5            # 赤・黒のむいた先の x


def led_wires(p_in, e):
    """LED の足に付ける赤と黒（下から来る）。e は黒がまだ下にある長さ"""
    yb = CUT_Y + 2 + e
    b = [f'<path d="M{JR} {CUT_Y + 2} C{JR} 240 {CX - 4} 290 {CX - 4} 330 L{CX - 4} 420" stroke="{RED}" stroke-width="7" fill="none"/>',
         f'<path d="M{JB} {yb:.1f} C{JB} {yb + 40:.1f} {CX + 4} 290 {CX + 4} 330 L{CX + 4} 420" stroke="{BLK}" stroke-width="7" fill="none"/>']
    b += copper_v(JR, CUT_Y - 40, CUT_Y + 2) + copper_v(JB, CUT_Y - 40 + e, CUT_Y + 2 + e)
    return group(b, dy=(1 - p_in) * 260)


def blob(x, fill):
    if fill <= 0:
        return []
    return [f'<ellipse cx="{x}" cy="{CUT_Y - 19}" rx="{7 * fill:.1f}" ry="{22 * fill:.1f}" fill="{SOLDER}" stroke="#9aa1ab" stroke-width="1"/>']


def s_led(st, t, i):
    """⑥ LED を抜いて、長い足に赤、短い足に黒をはんだ付けする"""
    L1, L2, L3 = i, i + 1, i + 2               # 抜く・長い足・短い足
    if st.index(t) == L1:
        p = st.p(t, L1, 1.2, 0.2)
        top = 100 - 80 * p
        b = led_big(top)
        ops = 1 - st.p(t, L1, 0.6, 1.8)
        b += group([f'<rect x="230" y="270" width="340" height="80" rx="6" fill="#f2efe6" stroke="#d6cfbd" stroke-width="2"/>'] +
                   [f'<rect x="{x - 2.5}" y="{y - 2.5}" width="5" height="5" fill="#9a927e"/>'
                    for x in range(250, 560, 20) for y in (292, 312, 332)], opacity=ops)
        b += dimmed([text(590, 315, "ブレッドボード", 14, "start", 700, SUB)], ops)
        return b
    in_long = st.index(t) == L2
    # 長い足
    f_long = st.p(t, L2, 0.8, 0.9) if in_long else 1
    b = led_big(20, cut_long=CUT_Y if (not in_long or st.p(t, L2, 0.5, 0.3) >= 1) else None,
                cut_short=CUT_Y if (st.index(t) > L2 and st.p(t, L3, 0.5, 0.3) >= 1) else None,
                fall=(f_long, st.p(t, L3, 0.8, 0.9) if st.index(t) == L3 else 1))
    p_in = st.p(t, L2, 1.0, 1.4) if in_long else 1
    e = 110 * (1 - st.p(t, L3, 0.8, 1.4)) if st.index(t) <= L3 else 0
    b += led_wires(p_in, e)
    tools = []
    if in_long:
        b += nipper(CX - 12 + 6, CUT_Y, st.p(t, L2, 0.5, 0.3), rot=90, sc=0.85,
                    op=st.p(t, L2, 0.3, 0) * (1 - st.p(t, L2, 0.4, 1.0)))
        b += dimmed(bracket_v(CX + 34, 88, CUT_Y, "1cm"), st.p(t, L2, 0.4, 0) * (1 - st.p(t, L2, 0.4, 1.4)))
        b += dimmed([text(470, 250, "先に両方切ると、", 14, "start", 700, RED),
                     text(470, 270, "どちらが＋か分からなくなる", 14, "start", 700, RED)], st.p(t, L2, 0.4, 0.6))
        tb, fill = solder_seq(st, t, L2, 2.6, JR + 2, CUT_Y - 19)
        b += blob(JR + 2.5, fill)
        tools += tb
    else:
        b += blob(JR + 2.5, 1)
    if st.index(t) == L3:
        b += nipper(CX + 12 - 6, CUT_Y, st.p(t, L3, 0.5, 0.3), rot=-90, sc=0.85,
                    op=st.p(t, L3, 0.3, 0) * (1 - st.p(t, L3, 0.4, 1.0)))
        tb, fill = solder_seq(st, t, L3, 2.4, JB - 2, CUT_Y - 19)
        b += blob(JB - 2.5, fill)
        tools += tb
    elif st.index(t) > L3:
        b += blob(JB - 2.5, 1)
    return b + tools


def bracket_v(x, y1, y2, label):
    return [ln(x, y1, x, y2, RED, 1.5), ln(x - 5, y1, x + 5, y1, RED, 1.5), ln(x - 5, y2, x + 5, y2, RED, 1.5),
            text(x + 10, (y1 + y2) / 2 + 5, label, 14, "start", 700, RED)]


def s_tape(st, t, i):
    """⑦ テープで1本ずつ包み、LED の側は2本いっしょにもう一度巻く"""
    b = led_big(20, cut_long=CUT_Y, cut_short=CUT_Y, fall=(1, 1)) + led_wires(1, 0) + blob(JR + 2.5, 1) + blob(JB - 2.5, 1)
    for x, d in ((CX - 28, 0), (CX + 4, 0.9)):
        q = st.p(t, i, 0.8, d)
        if q > 0:
            b.append(f'<rect x="{x}" y="110" width="24" height="{62 * q:.1f}" rx="3" fill="{TAPE}" opacity=".95"/>')
    q = st.p(t, i, 1.0, 2.2)
    if q > 0:
        b.append(f'<rect x="{CX - 34}" y="104" width="68" height="{76 * q:.1f}" rx="5" fill="{TAPE}" opacity=".8" stroke="#d9c37a" stroke-width="1"/>')
    b += dimmed([text(470, 120, "1本ずつ", 14, "start", 700, INK)], st.p(t, i, 0.4, 0.2) * (1 - q))
    b += dimmed([text(470, 120, "2本いっしょに", 14, "start", 700, INK)], q)
    b += dimmed([text(470, 250, "金具どうしがふれると、", 14, "start", 700, RED),
                 text(470, 270, "その LED は光らない", 14, "start", 700, RED)], st.p(t, i, 0.4, 3.4))
    return b


def s_plug(p, p_r, p_b):
    """⑧ 赤のオスを抵抗の下の列、黒のオスを − の列に差す"""
    b = [f'<rect x="40" y="186" width="500" height="178" rx="8" fill="#f2efe6" stroke="#d6cfbd" stroke-width="2"/>',
         f'<rect x="46" y="194" width="488" height="16" fill="#e2dccb"/>',
         ln(60, 322, 520, 322, SIG, 1.5), text(52, 345, "−", 15, "middle", 700, SIG)]
    rows = (232, 254, 276, 298)
    px = [70 + 22 * k for k in range(21)]
    res_x, rail_x, rail_y = px[8], px[12], 340
    for x in px:
        for y in rows + (rail_y,):
            b.append(f'<rect x="{x - 2.5}" y="{y - 2.5}" width="5" height="5" fill="#9a927e"/>')
    b.append(ln(res_x, 150, res_x, rows[0], LEG, 2))
    b.append(f'<rect x="{res_x - 8}" y="158" width="16" height="40" rx="5" fill="#f4e3c4" stroke="#8a6d3b" stroke-width="1"/>')
    for j, c in enumerate(BANDS["330Ω"]):
        b.append(f'<rect x="{res_x - 8}" y="{164 + j * 8}" width="16" height="4" fill="{c}"/>')
    b.append(text(res_x - 16, 182, "抵抗", 14, "end", 700, SUB))
    ry, by = rows[3], rail_y
    mx = (res_x + rail_x) / 2
    g = [f'<path d="M{mx - 4} -10 L{mx - 4} 20 C{mx - 4} 45 {res_x} 40 {res_x} 62" stroke="{RED}" stroke-width="7" fill="none"/>',
         f'<path d="M{mx + 4} -10 L{mx + 4} 20 C{mx + 4} 45 {rail_x} 40 {rail_x} 62" stroke="{BLK}" stroke-width="7" fill="none"/>',
         ln(res_x, 96, res_x, ry - 26, JUMP, 6), ln(rail_x, 96, rail_x, by - 26, JUMP, 6)]
    for x, y in ((res_x, ry), (rail_x, by)):
        g += [f'<rect x="{x - 11}" y="58" width="22" height="40" rx="4" fill="{TAPE}"/>',
              f'<rect x="{x - 7}" y="{y - 28}" width="14" height="26" rx="2" fill="{MALE}"/>']
    b += group(g, dy=-(1 - p) * 80)
    if p >= 1:
        b += [f'<circle cx="{res_x}" cy="{ry}" r="4" fill="{RED}"/>', f'<circle cx="{rail_x}" cy="{by}" r="4" fill="{BLK}"/>']
    b += dimmed([text(556, ry + 5, "赤 → 抵抗の下の列", 15, "start", 700, RED),
                 text(556, ry + 25, "（長い足があった穴）", 13, "start", 400, SUB)], p_r)
    b += dimmed([text(556, by + 9, "黒 → − の列", 15, "start", 700, INK)], p_b)
    return b


# ---------------------------------------------------------------- ⑨⑩ 10個を光らせて、木にかける
TX, BASE_Y = 400, 342
SPOTS = [(-22, 140), (24, 156), (-50, 205), (8, 190), (52, 228), (-80, 270),
         (-24, 250), (34, 286), (90, 316), (-62, 322)]          # make_xmas_figures の木と同じ


def wire_pts(k, m):
    """LED k の線の点。m=0 で机の上に並べたところ、1 で木にかけたところ"""
    a = math.radians(160 - k * 140 / 9)
    lx, ly = TX + 240 * math.cos(a), BASE_Y - 200 * math.sin(a)
    ex = TX - 10 + (k - 4.5) * 5
    flat = [(lx, ly), ((lx + ex) / 2, (ly + BASE_Y) / 2 + 30), (ex, BASE_Y - 14), (ex, BASE_Y)]
    dx, y = SPOTS[k]
    y -= 50
    ex2 = TX + (k - 4.5) * 1.6
    hung = [(TX + dx, y), (TX + dx * 0.2, y + 18), (ex2, y + 30), (ex2, BASE_Y)]
    return [(a0 + (b0 - a0) * m, a1 + (b1 - a1) * m) for (a0, a1), (b0, b1) in zip(flat, hung)]


def s_tree(m, n_lit, on):
    b = tree(TX, op=m)
    for k in range(10):
        (lx, ly), (cx, cy), (ex, ey), (bx, by) = wire_pts(k, m)
        b.append(f'<path d="M{lx:.1f} {ly:.1f} Q{cx:.1f} {cy:.1f} {ex:.1f} {ey:.1f} L{bx:.1f} {by:.1f}" '
                 f'stroke="{mix("#555c66", "#d8dde3", m)}" stroke-width="2" fill="none"/>')
    for k in range(10):
        (lx, ly) = wire_pts(k, m)[0]
        name, stroke, fill = COLORS[k]
        lit = k < n_lit
        if lit:
            b.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="17" fill="{stroke}" opacity=".3"/>')
        b.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="8" fill="{stroke if lit and name != "白" else fill}" '
                 f'stroke="{stroke}" stroke-width="2"/>')
    b.append(f'<rect x="{TX - 80}" y="{BASE_Y}" width="140" height="34" rx="5" fill="#f2efe6" stroke="#d6cfbd" stroke-width="2"/>')
    b.append(f'<rect x="{TX + 10}" y="{BASE_Y + 6}" width="44" height="22" rx="3" fill="{PICO}"/>')
    b.append(text(TX - 32, BASE_Y + 22, "ブレッドボード", 11, "middle", 700, SUB))
    b += battery(TX + 80, BASE_Y + 2, 84, 30)
    b.append(ln(TX + 60, BASE_Y + 17, TX + 80, BASE_Y + 17, VSYS, 2))
    if on:
        b.append(text(TX + 172, BASE_Y + 22, "ON", 13, "start", 700, RED))
    return b


# ---------------------------------------------------------------- 動画
def xmas_hang():
    st = Steps([("LED を赤黒の2芯の線で延ばして、ツリーの木にかける", 3),
                ("① USB を抜き、電池のスイッチを切る", 3.5),
                ("② ジャンパーワイヤーを10本、真ん中で切る。オスの付いた線が20本できる", 4.5),
                ("② 切った先を 5mm くらいむく", 3.5),
                ("③ 2芯の線を「根元から枝までの長さ＋20cm」に切る。平均 2m まで", 5.5),
                ("④ 両はしで赤と黒を 3cm くらい裂き、先を 5mm むいて、中の細い線をねじる", 6),
                ("⑤ 片方のはしの赤と黒に、オスの付いた線を1本ずつはんだ付けする", 7),
                ("⑥ LED を1個ボードから抜く", 3),
                ("⑥ 長い足を 1cm くらいに切って、赤をはんだ付けする", 6.5),
                ("⑥ 次に短い足を切って、黒をはんだ付けする", 6),
                ("⑦ はんだ付けした所を1本ずつテープで包み、LED の側は2本いっしょにもう一度巻く", 6),
                ("⑧ 赤のオスを抵抗の下の列、黒のオスを − の列に差す", 5.5),
                ("⑨ 10個とも同じようにしたら、電池のスイッチを入れて全部光るか見る", 5),
                ("⑩ LED を枝にかけて線を巻きつけ、幹の近くを通して根元にまとめる", 6)])

    def f(t):
        i = st.index(t)
        p = lambda move, delay=0.0: st.p(t, i, move, delay)
        if i == 0:
            b = s_tree(1, 10, False)
        elif i == 1:
            b = s_usb(p(1.0, 0.1), p(0.5, 1.5))
        elif i == 2:
            b = s_cut(p(0.5, 0.6), p(0.8, 1.3), p(0.4), p(0.4, 2.0))
        elif i == 3:
            b = s_strip(p(0.3), p(1.0, 0.6), p(0.4, 1.8))
        elif i == 4:
            b = s_length(p(1.2), p(1.2, 1.0), p(0.4, 2.3), p(0.3, 2.6), p(0.5, 3.0))
        elif i == 5:
            b = s_split(p(1.0), p(0.4, 1.0), p(0.9, 1.6), p(0.4, 2.4), p(1.2, 3.0), p(0.4, 3.4), p(0.4, 4.4))
        elif i == 6:
            b = s_join(st, t, i)
        elif i in (7, 8, 9):
            b = s_led(st, t, 7)
        elif i == 10:
            b = s_tape(st, t, i)
        elif i == 11:
            b = s_plug(p(1.2, 0.2), p(0.4, 1.4), p(0.4, 2.2))
        elif i == 12:
            b = s_tree(0, int(p(3.0, 0.6) * 10.99), True)
        else:
            b = s_tree(p(2.5, 0.2), 10, True)
        return frame(b, st.caption(t))
    return f, st.duration


VIDEOS = {"xmas-hang": xmas_hang}


def still(out, name, times):
    """動画 name の決めた秒のコマを、フォルダ out に PNG で出す（見た目を確かめる用）"""
    from pathlib import Path
    from playwright.sync_api import sync_playwright
    from video import fit_caption, PX_W, PX_H
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    f, _ = VIDEOS[name]()
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="chrome")
        page = browser.new_page(viewport={"width": PX_W, "height": PX_H})
        for t in times:
            page.set_content(f"<html><body style='margin:0;overflow:hidden'>{fit_caption(f(t))}</body></html>")
            page.screenshot(path=str(out / f"{name}-{t:05.1f}.png"))
            print(out / f"{name}-{t:05.1f}.png")
        browser.close()


def main():
    args = sys.argv[1:]
    if args[:1] == ["--still"]:
        still(args[1], args[2], [float(a) for a in args[3:]])
        return
    for name in args or VIDEOS:
        f, duration = VIDEOS[name]()
        render("pico", name, f, duration)


if __name__ == "__main__":
    main()
