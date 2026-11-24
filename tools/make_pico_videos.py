#!/usr/bin/env python3
"""ピコの教科書の動画を作る（使い方は tools/video.py）。

    .venv/bin/python tools/make_pico_videos.py            # 全部
    .venv/bin/python tools/make_pico_videos.py led-wiring # 選んで

- breadboard-inside  7章 ブレッドボードの中のつながり
- pin-header         7章 ピンヘッダのはんだ付け
- led-wiring         8章 外付けの LED の差し方
- button-wiring      8章 外付けのボタンの差し方
- pot-wiring         9章 ボリュームの差し方
- bootsel            1章 書き込みモード（BOOTSEL）にする
"""
import math
import sys

from make_breadboard_figures import (P, X, ROW, TOP_MINUS, TOP_PLUS, MARK, LEG, WHITE, board, pico, dot, resistor, col_of)
from make_xmas_figures import PICO, PIN, SIG, GND, VSYS
from video import Steps, frame, group, draw_path, render, text, clamp, INK, SUB, W, H, CAP_H

BB = dict(dx=25, dy=-44)                 # ブレッドボードの図を動画の中に置く位置
PLUG = "#3a3f47"
SKIN, SKIN_LINE = "#f1c7a5", "#d9a77f"
SOLDER = "#c9ced6"


def bb(body):
    return group(body, **BB)


def usb_plug(ux):
    """ピコの USB（右）に差すケーブル。ux だけ右に離れる（0 で差さっている）"""
    y = (ROW["c"] + ROW["h"]) / 2
    x = X(30) + 30 + ux
    return [f'<rect x="{x}" y="{y - 11}" width="34" height="22" rx="3" fill="{PLUG}"/>',
            f'<line x1="{x + 34}" y1="{y}" x2="{x + 300}" y2="{y}" stroke="{PLUG}" stroke-width="7"/>']


def led_part(x1, y1, x2, y2, on=False, labels=True):
    """LED。長い足は (x1, y1)、短い足は (x2, y2) に差す"""
    lx, ly = (x1 + x2) / 2, (y1 + y2) / 2
    b = [f'<line x1="{x1}" y1="{y1}" x2="{lx - 3}" y2="{ly}" stroke="{LEG}" stroke-width="2"/>',
         f'<line x1="{x2}" y1="{y2}" x2="{lx + 3}" y2="{ly}" stroke="{LEG}" stroke-width="2"/>']
    if on:
        b.append(f'<circle cx="{lx}" cy="{ly}" r="22" fill="#ff6b6b" opacity=".35"/>')
    b.append(f'<circle cx="{lx}" cy="{ly}" r="9" fill="{"#ff3b3b" if on else "#ffcdd2"}" stroke="#d93a3a" stroke-width="2"/>')
    b += [dot(x1, y1, "#d93a3a"), dot(x2, y2)]
    if labels:
        b.append(text(lx - 16, y1 - 6, "長い足（＋）", 11, "end", 700, "#d93a3a"))
        b.append(text(x2 + 10, y2 + 24, "短い足（−）", 11, "start", 700, INK))
    return b


def wire_d(x1, y1, x2, y2, bend):
    return f"M{x1} {y1} C{x1} {y1 + bend * 1.33:.1f} {x2} {y2 + bend * 1.33:.1f} {x2} {y2}"


def wire_anim(x1, y1, x2, y2, color, bend, p):
    """ジャンパーワイヤーを、はしから描いていく"""
    if p <= 0:
        return []
    b = draw_path(wire_d(x1, y1, x2, y2, bend), color, p)
    b.append(dot(x1, y1, color))
    if p >= 1:
        b.append(dot(x2, y2, color))
    return b


def drop(body, p, dist=70):
    """上から落として差す"""
    if p <= 0:
        return []
    return group(body, dy=-(1 - p) * dist, opacity=min(1.0, p * 2))


def monitor(lines, x=555, y=12, w=230, title="Serial Monitor"):
    """右上に出す、ピコの出力の窓。lines は [[(字, 色), …], …]"""
    h = 30 + 20 * len(lines)
    b = [f'<rect x="{x + 3}" y="{y + 3}" width="{w}" height="{h}" rx="8" fill="#000000" opacity=".15"/>',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#1e2228"/>',
         text(x + 12, y + 19, title, 11, "start", 700, "#9aa1ab")]
    for i, parts in enumerate(lines):
        spans = "".join(f'<tspan fill="{color}">{s}</tspan>' for s, color in parts)
        b.append(f'<text x="{x + 12}" y="{y + 40 + 20 * i}" font-size="13" font-weight="700" xml:space="preserve">{spans}</text>')
    return b


# ---------------------------------------------------------------- 7章 ブレッドボードの中
def breadboard_inside():
    st = Steps([("ブレッドボードの中のつながり", 2.5),
                ("穴の下には金属の板が入っていて、縦の5穴（a〜e）が1本につながっている", 5.5),
                ("f〜j も同じ。溝の上と下は、つながっていない", 4.5),
                ("上下の ＋ / − の列は、横一列が全部つながっている", 4),
                ("同じ縦の列に差した足どうしは、線がなくてもつながる", 5),
                ("ピコは、真ん中の溝をまたぐように差す", 4)])

    def f(t):
        i = st.index(t)
        cols, rails = [], []
        p1 = st.p(t, 1, 0.8)
        n_top = int(st.p(t, 1, 2.0, 1.6) * 30)
        if p1 >= 1 and i <= 3:
            cols += [(5, "top")] + [(c, "top") for c in range(1, n_top + 1) if c != 5]
        n_bot = int(st.p(t, 2, 1.6) * 30)
        if i in (2, 3):
            cols += [(c, "bottom") for c in range(1, n_bot + 1)]
        if i == 3:
            k = st.p(t, 3, 1.6)
            rails = [y for y, d in ((TOP_PLUS, 0), (TOP_MINUS, 0.2), (ROW["j"] + 34, 0.4), (ROW["j"] + 54, 0.6)) if k > d]
        if i >= 4:
            cols = [(5, "top")]
        b = board(cols, rails)
        # 金属の板（5列の a〜e）
        if 1 <= i <= 2:
            b.append(f'<rect x="{X(5) - 6}" y="{ROW["a"] - 6}" width="12" height="{4 * P + 12}" rx="3" fill="#9aa1ab" opacity="{.55 * p1:.2f}"/>')
            b += group([text(X(5) + 12, ROW["a"] - 14, "金属の板", 12, "start", 700, SUB)], opacity=p1)
        if i == 2:
            q = st.p(t, 2, 0.6, 1.6)
            b.append(f'<rect x="{X(5) - 6}" y="{ROW["f"] - 6}" width="12" height="{4 * P + 12}" rx="3" fill="#9aa1ab" opacity="{.55 * q:.2f}"/>')
            cy = (ROW["e"] + ROW["f"]) / 2
            b += group([f'<path d="M{X(5) - 10} {cy - 10} L{X(5) + 10} {cy + 10} M{X(5) + 10} {cy - 10} L{X(5) - 10} {cy + 10}" '
                        f'stroke="#d93a3a" stroke-width="4" stroke-linecap="round"/>',
                        text(X(5) + 18, cy + 5, "つながっていない", 13, "start", 700, "#d93a3a")], opacity=q)
        if i >= 4:
            b += drop(resistor(5, 9, ROW["c"]), st.p(t, 4, 0.8))
            b += drop(led_part(X(5), ROW["a"], X(4), TOP_MINUS, labels=False), st.p(t, 4, 0.8, 0.5))
            if st.p(t, 4, 0.5, 1.6) > 0 and i == 4:
                b.append(text(X(5) + 14, ROW["e"] + 4, "← ここでつながる", 13, "start", 700, "#d93a3a"))
        if i >= 5:
            b += drop(pico([]), st.p(t, 5, 1.0), 110)
        return frame(bb(b), st.caption(t))
    return f, st.duration


# ---------------------------------------------------------------- 7章 ピンヘッダのはんだ付け
SIDE_BB_Y = 300            # 横から見たブレッドボードの上の面
PIN_XS = (275, 525)


def side_view(p_head, p_pico, fillet=(0, 0), lift=0.0, labels=True):
    """横から見たところ。p_head: ピンヘッダが差さる進み、p_pico: ピコが載る進み、fillet: 左右のはんだの量"""
    y0 = SIDE_BB_Y
    b = [f'<rect x="120" y="{y0}" width="560" height="70" rx="6" fill="#f2efe6" stroke="#d6cfbd" stroke-width="2"/>']
    if labels:
        b.append(text(130, y0 + 90, "ブレッドボード（横から見たところ）", 12, "start", 700, SUB))
    for x in PIN_XS:                       # 穴
        b.append(f'<rect x="{x - 5}" y="{y0}" width="10" height="56" fill="#d6cfbd"/>')
    up = -lift
    hy = y0 - (1 - p_head) * 120 + up      # ピンヘッダの樹脂の下の面
    for x in PIN_XS:
        b += group([f'<line x1="{x}" y1="{hy + 50}" x2="{x}" y2="{hy - 64}" stroke="#9aa1ab" stroke-width="5" stroke-linecap="round"/>',
                    f'<rect x="{x - 14}" y="{hy - 24}" width="28" height="24" rx="2" fill="{INK}"/>'], opacity=min(1, p_head * 2 + .001))
    if p_head > 0 and labels:
        b += group([text(PIN_XS[1] + 22, hy + 34, "長い側を下に", 12, "start", 700, INK),
                    text(PIN_XS[1] + 22, hy - 46, "短い側（ピコに通す）", 12, "start", 400, SUB)], opacity=min(1, p_head * 2))
    if p_pico > 0:
        py = (hy - 24) - (1 - p_pico) * 110            # ピコの下の面
        b += group([f'<rect x="{PIN_XS[0] - 22}" y="{py - 14}" width="{PIN_XS[1] - PIN_XS[0] + 44}" height="14" rx="2" fill="{PICO}"/>',
                    f'<rect x="370" y="{py - 26}" width="60" height="12" rx="2" fill="{INK}"/>'] +
                   ([text(400, py - 34, "チップのある面を上に", 12, "middle", 700, INK)] if labels else []), opacity=min(1, p_pico * 2))
        for k, x in enumerate(PIN_XS):
            a = fillet[k]
            if a > 0:
                top = py - 14
                b.append(f'<path d="M{x - 13} {top} Q{x - 4} {top - 6 * a} {x - 3} {top - 16 * a} L{x + 3} {top - 16 * a} '
                         f'Q{x + 4} {top - 6 * a} {x + 13} {top} Z" fill="{SOLDER}" stroke="#9aa1ab" stroke-width="1"/>')
    return b


def zoom(body, z, fx, fy, cx=400, cy=195):
    """(fx, fy) を画面の (cx, cy) に置いて z 倍にする"""
    return [f'<g transform="translate({cx} {cy}) scale({z:.3f}) translate({-fx:.1f} {-fy:.1f})">', *body, "</g>"]


def iron(x, y, p, heat=0.0, fs=12):
    """はんだごて。先が (x, y)。p=0 で右上に離れている"""
    off = (1 - p) * 130
    tx, ty = x + 4 + off, y - 2 - off * 0.8
    b = []
    if heat > 0:
        b.append(f'<circle cx="{x}" cy="{y}" r="{14 + 3 * heat:.1f}" fill="none" stroke="#ff9f43" stroke-width="3" opacity="{.8 * heat:.2f}"/>')
    b += [f'<line x1="{tx}" y1="{ty}" x2="{tx + 40}" y2="{ty - 32}" stroke="#9aa1ab" stroke-width="5" stroke-linecap="round"/>',
          f'<line x1="{tx + 40}" y1="{ty - 32}" x2="{tx + 110}" y2="{ty - 88}" stroke="#d93a3a" stroke-width="16" stroke-linecap="round"/>',
          text(tx + 70, ty - 22, "はんだごて", fs, "start", 700, INK)]
    return b


def solder_wire(x, y, p, used=0.0, fs=12):
    """はんだ（細い線）。先が (x, y)。p=0 で左上に離れている"""
    off = (1 - p) * 120
    tx, ty = x - 6 - off, y - 4 - off * 0.7
    length = 130 - 30 * used
    ex, ey = tx - length * 0.75, ty - length * 0.66
    return [f'<line x1="{tx}" y1="{ty}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{SOLDER}" stroke-width="4" stroke-linecap="round"/>',
            text(ex - 6, ey - 6, "はんだ", fs, "end", 700, INK)]


def top_view(done):
    """上から見たピコ。done は、はんだ付けが済んだピンの番号の集まり"""
    x0, y0, w, h = 140, 110, 510, 210
    b = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="10" fill="{PICO}"/>',
         f'<rect x="{x0 + w}" y="{y0 + h / 2 - 20}" width="26" height="40" rx="3" fill="#b8bec7"/>',
         text(x0 + w + 32, y0 + h / 2 + 5, "USB", 12, "start", 700, SUB),
         f'<rect x="{x0 + w / 2 - 34}" y="{y0 + h / 2 - 34}" width="68" height="68" rx="4" fill="{INK}"/>',
         text(x0 + w / 2, y0 + h / 2 + 5, "RP2040", 11, "middle", 700, "#9aa1ab")]
    pitch = 25.4
    xs = [x0 + 14 + (w - 28 - 19 * pitch) / 2 + k * pitch for k in range(20)]
    for k in range(20):
        for pin, y in ((20 - k, y0 + 18), (21 + k, y0 + h - 18)):       # 上の列は左が 20番、下の列は左が 21番
            x = xs[k]
            if pin in done:
                b.append(f'<circle cx="{x:.1f}" cy="{y}" r="9" fill="{SOLDER}" stroke="#9aa1ab" stroke-width="1.2"/>')
                b.append(f'<circle cx="{x - 2.5:.1f}" cy="{y - 2.5}" r="2.5" fill="#ffffff" opacity=".8"/>')
            else:
                b.append(f'<circle cx="{x:.1f}" cy="{y}" r="8" fill="{PIN}"/>')
                b.append(f'<rect x="{x - 2.5:.1f}" y="{y - 2.5}" width="5" height="5" fill="#9aa1ab"/>')
    b.append(text(xs[0], y0 - 12, "20番", 11, "middle", 700, SUB))
    b.append(text(xs[19], y0 - 12, "1番", 11, "middle", 700, SUB))
    b.append(text(xs[0], y0 + h + 24, "21番", 11, "middle", 700, SUB))
    b.append(text(xs[19], y0 + h + 24, "40番", 11, "middle", 700, SUB))
    return b, xs, (y0 + 18, y0 + h - 18)


def pin_header():
    st = Steps([("ピコにピンヘッダをはんだ付けする", 2.5),
                ("① ピンヘッダの長い側を下にして、ブレッドボードに差す（2本。間隔はピコの幅）", 4),
                ("② その上にピコを、チップのある面を上にして載せる", 3.5),
                ("③ こて先を、ピンとまわりの金属（パッド）の両方に当てて、2〜3秒温める", 4.5),
                ("④ はんだを当てて溶かし込む。穴のまわりが埋まるくらい", 3.5),
                ("⑤ はんだを先に離して、次にこてを離す", 3.5),
                ("⑥ まず対角の角の2本。ピコが傾いていなければ、残りを全部（40本）", 7),
                ("⑦ ピコをブレッドボードから、まっすぐ引き抜く", 3.5)])
    order = [1, 21] + [n for n in list(range(2, 21)) + list(range(22, 41))]

    def f(t):
        i = st.index(t)
        x, top = PIN_XS[1], SIDE_BB_Y - 24 - 14       # 右のピンの、ピコの上の面
        if i == 6:
            k = st.p(t, 6, 1.2)
            n = 2 if k < 1 else 2 + int(st.p(t, 6, 3.6, 1.6) * 38)
            body, xs, ys = top_view(set(order[:n]) if k > 0.5 else set())
            if k <= 0.5 or n == 2:
                body.append(text(400, 365, "最初は、対角の角の2本（1番と21番）", 14, "middle", 700, "#d93a3a"))
            return frame(body, st.caption(t))
        z0, f0 = 1.3, (400, 245)
        if i < 3:
            b = zoom(side_view(st.p(t, 1, 1.4) if i >= 1 else 0, st.p(t, 2, 1.2) if i >= 2 else 0), z0, *f0)
        elif i < 6:
            zp = clamp(st.local(t, 3) / 0.9) if i == 3 else 1
            zp = zp * zp * (3 - 2 * zp)
            z = z0 + (2.6 - z0) * zp
            fx, fy = f0[0] + (x - f0[0]) * zp, f0[1] + (top - 10 - f0[1]) * zp
            fill_r = st.p(t, 4, 1.6, 0.6) if i >= 4 else 0
            b = side_view(1, 1, (0, fill_r), labels=False)
            p_iron = st.p(t, 3, 1.0) if i < 5 else 1 - st.p(t, 5, 0.9, 1.2)
            heat = clamp((st.local(t, 3) - 1.4) / 1.0) if i >= 3 else 0
            if i == 5:
                heat *= 1 - st.p(t, 5, 0.9, 1.2)
            p_sol = st.p(t, 4, 0.8) if i == 4 else (1 - st.p(t, 5, 0.8) if i == 5 else 0)
            b += solder_wire(x, top - 4, p_sol, fill_r, 12 * z0 / z)
            b += iron(x + 4, top - 2, p_iron, heat, 12 * z0 / z)
            b = zoom(b, z, fx, fy)
        else:
            b = zoom(side_view(1, 1, (1, 1), lift=st.p(t, 7, 1.4) * 110, labels=False), z0, *f0)
        return frame(b, st.caption(t))
    return f, st.duration


# ---------------------------------------------------------------- 8章 外付けの LED
def led_wiring():
    st = Steps([("外付けの LED をブレッドボードに差す", 2.5),
                ("① USB を抜く", 2.5),
                ("② ピコを、真ん中の溝をまたぐように差す（USB を右に）", 3.5),
                ("③ 抵抗: 20番（GP15）の列と、左の空いている列に差す", 4),
                ("④ LED: 長い足は抵抗と同じ列、短い足は − の列に差す", 4),
                ("⑤ ワイヤー: 18番（GND）の列と − の列をつなぐ", 4),
                ("⑥ USB をつないで書き込むと、LED が点滅する", 6)])

    def f(t):
        i = st.index(t)
        p_pico, p_res, p_led, p_wire = (st.p(t, k, 1.0) if i >= k else 0 for k in (2, 3, 4, 5))
        cols = ([(11, "top"), (7, "top")] if p_res >= 1 else []) + ([(13, "top")] if p_wire >= 1 else [])
        b = board(cols, [TOP_MINUS] if p_led >= 1 else [])
        ux = (st.p(t, 1, 0.8) * 45 if i >= 1 else 0) if i < 6 else (1 - st.p(t, 6, 0.8)) * 45
        lift = (1 - p_pico) * 120
        b.append(f'<rect x="{X(11) - 12}" y="{ROW["c"] - 14}" width="{X(30) - X(11) + 24}" height="{ROW["h"] - ROW["c"] + 28}" '
                 f'rx="6" fill="#000000" opacity="{.12 * (1 - p_pico):.3f}"/>')
        b += group(pico([(18, "GND（18番）", 0, "start"), (20, "GP15（20番）", 1, "start")]) + usb_plug(ux), dy=-lift)
        b += drop(resistor(7, 11, ROW["b"]), p_res)
        on = i == 6 and st.local(t, 6) > 1.4 and (st.local(t, 6) - 1.4) % 0.8 < 0.4
        b += drop(led_part(X(7), ROW["a"], X(8), TOP_MINUS, on), p_led)
        d = f'M{X(13)} {ROW["a"]} C{X(13) + 14} {ROW["a"] - 10} {X(13) + 14} {TOP_MINUS + 10} {X(13)} {TOP_MINUS}'
        if p_wire > 0:
            b += draw_path(d, GND, p_wire) + [dot(X(13), ROW["a"], GND)] + ([dot(X(13), TOP_MINUS, GND)] if p_wire >= 1 else [])
        return frame(bb(b), st.caption(t))
    return f, st.duration


# ---------------------------------------------------------------- 8章 外付けのボタン
def button_part(pressed=False):
    x1, x2, y1, y2 = X(4), X(6), ROW["e"], ROW["f"]
    b = [f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{LEG}" stroke-width="3"/>' for x in (x1, x2)]
    b.append(f'<rect x="{x1 - 8}" y="{y1 + 8}" width="{x2 - x1 + 16}" height="{y2 - y1 - 16}" rx="4" fill="#3a3f47"/>')
    b.append(f'<circle cx="{(x1 + x2) / 2}" cy="{(y1 + y2) / 2}" r="{10 if pressed else 12}" fill="{"#5b616b" if pressed else "#8a8f98"}" stroke="#c9ced6" stroke-width="2"/>')
    b += [dot(x2, y1, LEG), dot(x1, y2, LEG), dot(x1, y1, SIG), dot(x2, y2, GND)]
    return b


def finger(x, y, p, label=None):
    """指。p=1 で (x, y) を押している"""
    if p <= 0:
        return []
    dy = (1 - p) * 60
    b = [f'<ellipse cx="{x}" cy="{y - 30 - dy:.1f}" rx="22" ry="34" fill="{SKIN}" stroke="{SKIN_LINE}" stroke-width="2" opacity=".92"/>']
    if label:
        b.append(text(x, y - 74 - dy, label, 14, "middle", 700, INK))
    return group(b, opacity=min(1, p * 2))


def button_wiring():
    st = Steps([("外付けのボタンをブレッドボードに差す", 2.5),
                ("① USB を抜く（ピコは差したまま）", 2.5),
                ("② ボタンを、真ん中の溝をまたぐように差す", 3.5),
                ("③ ワイヤー: 左上の足の列と、19番（GP14）の列をつなぐ", 3.5),
                ("④ ワイヤー: 右下の足の列と、23番（GND）の列をつなぐ", 3.5),
                ("⑤ 書き込んで押すと「押されている」と出る", 7)])

    def pressed_at(tt):
        lt = tt - st.starts[5] - 1.6
        return lt > 0 and lt % 2.2 > 1.1

    def f(t):
        i = st.index(t)
        p_btn, p_w1, p_w2 = (st.p(t, k, 1.0) if i >= k else 0 for k in (2, 3, 4))
        cols = ([(4, "top"), (6, "bottom")] if p_btn >= 1 else []) + ([(12, "top")] if p_w1 >= 1 else []) + \
               ([(13, "bottom")] if p_w2 >= 1 else [])
        b = board(cols)
        ux = (st.p(t, 1, 0.8) * 45 if i >= 1 else 0) if i < 5 else (1 - st.p(t, 5, 0.8)) * 45
        b += pico([(19, "GP14（19番）", 0, "start"), (23, "GND（23番）", 0, "start")]) + usb_plug(ux)
        pr = pressed_at(t)
        b += drop(button_part(pr), p_btn)
        b += wire_anim(X(4), ROW["a"], X(12), ROW["a"], SIG, -26, p_w1)
        b += wire_anim(X(6), ROW["j"], X(13), ROW["j"], GND, 22, p_w2)
        if i == 5:
            b += finger((X(4) + X(6)) / 2, (ROW["e"] + ROW["f"]) / 2, 1 if pr else 0.55)
        out = bb(b)
        if i == 5 and st.local(t, 5) > 1.0:
            q = [t - 0.2 * k for k in range(3, -1, -1)]
            out += monitor([[("押されている", "#7ee787")] if pressed_at(tt) else [("-", "#c9d1d9")] for tt in q])
        return frame(out, st.caption(t))
    return f, st.duration


# ---------------------------------------------------------------- 9章 ボリューム
def pot_part(angle):
    xs, y = (X(4), X(6), X(8)), ROW["f"]
    cx, cy = xs[1], (ROW["e"] + y) / 2
    b = [f'<rect x="{xs[0] - 18}" y="{ROW["e"] + 4}" width="{xs[2] - xs[0] + 36}" height="{y - ROW["e"] - 10}" rx="5" fill="#2f5fa8"/>',
         f'<circle cx="{cx}" cy="{cy}" r="17" fill="#c9ced6" stroke="#8a8f98" stroke-width="2"/>',
         f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - 14}" stroke="{INK}" stroke-width="2.5" transform="rotate({angle:.1f} {cx} {cy})"/>']
    for x, c in zip(xs, (VSYS, SIG, GND)):
        b += [f'<line x1="{x}" y1="{y - 8}" x2="{x}" y2="{y}" stroke="{LEG}" stroke-width="3"/>', dot(x, y, c)]
    return b


def pot_wiring():
    st = Steps([("ボリュームをブレッドボードに差す", 2.5),
                ("① USB を抜く（ピコは差したまま）", 2.5),
                ("② ボリュームの3本の足を、溝の下の空いている所に差す", 3.5),
                ("③ 左の足の列 → 36番（3V3(OUT)）の列", 3),
                ("③ 真ん中の足の列 → 31番（GP26）の列", 3),
                ("③ 右の足の列 → 28番（GND）の列", 3),
                ("④⑤ 書き込んでつまみを回すと、値が 0〜4095 の間で変わる", 7.5)])

    def angle_at(t):
        lt = st.local(t, 6) - 1.4
        return -135 + 270 * (0.5 - 0.5 * math.cos(lt * math.pi / 2.6)) if lt > 0 else -135

    def f(t):
        i = st.index(t)
        p_pot, p_r, p_b, p_k = (st.p(t, k, 1.0) if i >= k else 0 for k in (2, 3, 4, 5))
        cols = ([(4, "bottom"), (6, "bottom"), (8, "bottom")] if p_pot >= 1 else []) + \
               ([(26, "bottom")] if p_r >= 1 else []) + ([(21, "bottom")] if p_b >= 1 else []) + ([(18, "bottom")] if p_k >= 1 else [])
        b = board(cols)
        ux = (st.p(t, 1, 0.8) * 45 if i >= 1 else 0) if i < 6 else (1 - st.p(t, 6, 0.8)) * 45
        b += pico([(28, "GND（28番）", 0, "end"), (31, "GP26（31番）", 0, "start"), (36, "3V3(OUT)（36番）", 1, "end")],
                  name_dx=-30, name_dy=-6) + usb_plug(ux)
        ang = angle_at(t) if i == 6 else -135
        b += drop(pot_part(ang), p_pot)
        b += wire_anim(X(4), ROW["j"], X(col_of(36)), ROW["j"], VSYS, 50, p_r)
        b += wire_anim(X(6), ROW["j"], X(col_of(31)), ROW["j"], SIG, 34, p_b)
        b += wire_anim(X(8), ROW["j"], X(col_of(28)), ROW["j"], GND, 18, p_k)
        out = bb(b)
        if i == 6 and st.local(t, 6) > 1.0:
            raw = round((ang + 135) / 270 * 4095)
            q = [t - 0.5 * k for k in range(2, -1, -1)]
            lines = []
            for tt in q:
                r = round((angle_at(tt) + 135) / 270 * 4095)
                lines.append([("値:", "#9aa1ab"), (f" {r:4d}", "#7ee787"), ("  電圧:", "#9aa1ab"), (f" {r * 3.3 / 4095:.2f} V", "#7ee787")])
            out += monitor(lines, x=500, w=285)
        return frame(out, st.caption(t))
    return f, st.duration


# ---------------------------------------------------------------- 1章 書き込みモード
def bootsel():
    st = Steps([("書き込みモード（BOOTSEL）にする（方法A）", 2.5),
                ("① BOOT ボタンを押したまま", 3),
                ("② USB ケーブルで PC につなぐ", 3),
                ("③ BOOT ボタンを離す", 2.5),
                ("PC に「RPI-RP2」が出れば成功", 4.5)])
    x0, y0, w, h = 170, 200, 400, 165
    bx, by = x0 + 70, y0 + 52                       # BOOT ボタン

    def f(t):
        i = st.index(t)
        b = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="8" fill="{PICO}"/>',
             f'<rect x="{x0 - 16}" y="{y0 + h / 2 - 16}" width="18" height="32" rx="2" fill="#b8bec7"/>',
             f'<rect x="{x0 + w / 2 - 20}" y="{y0 + h / 2 - 22}" width="48" height="48" rx="3" fill="{INK}"/>']
        for k in range(20):
            px = x0 + 14 + k * (w - 28) / 19
            b += [f'<circle cx="{px:.1f}" cy="{y0 + 10}" r="4" fill="{PIN}"/>', f'<circle cx="{px:.1f}" cy="{y0 + h - 10}" r="4" fill="{PIN}"/>']
        held = (i == 1 and st.p(t, 1, 0.8) >= 1) or i == 2 or (i == 3 and st.p(t, 3, 0.6) < 0.5)
        b += [f'<rect x="{bx - 16}" y="{by - 12}" width="32" height="24" rx="3" fill="#e9ecef"/>',
              f'<rect x="{bx - 9}" y="{by - 7}" width="18" height="14" rx="3" fill="{"#8a8f98" if held else "#ffffff"}" stroke="#9aa1ab"/>',
              text(bx, by + 28, "BOOT", 12, "middle", 700, "#ffffff")]
        # USB ケーブル（左から差す）
        p_usb = st.p(t, 2, 1.0) if i >= 2 else 0
        ux = x0 - 16 - 36 - (1 - p_usb) * 90
        b += [f'<rect x="{ux}" y="{y0 + h / 2 - 12}" width="36" height="24" rx="3" fill="{PLUG}"/>',
              f'<line x1="{ux}" y1="{y0 + h / 2}" x2="{ux - 300}" y2="{y0 + h / 2}" stroke="{PLUG}" stroke-width="7"/>',
              text(ux + 18, y0 + h / 2 + 40, "PC へ", 12, "middle", 700, SUB)]
        # 指
        if i == 1:
            b += finger(bx, by, st.p(t, 1, 0.8), "押したまま")
        elif i == 2:
            b += finger(bx, by, 1, "押したまま")
        elif i == 3:
            b += finger(bx, by, 1 - st.p(t, 3, 0.8), "離す")
        # PC の窓
        if i == 4:
            q = st.p(t, 4, 0.8)
            wx, wy = 505, 18
            b += group([f'<rect x="{wx + 4}" y="{wy + 4}" width="270" height="170" rx="8" fill="#000000" opacity=".12"/>',
                        f'<rect x="{wx}" y="{wy}" width="270" height="170" rx="8" fill="#ffffff" stroke="#c9ced6" stroke-width="2"/>',
                        f'<rect x="{wx}" y="{wy}" width="270" height="30" rx="8" fill="#e9ecef"/>',
                        text(wx + 12, wy + 20, "ファイル", 12, "start", 700, INK),
                        f'<rect x="{wx + 30}" y="{wy + 56}" width="60" height="44" rx="5" fill="#9aa1ab"/>',
                        f'<rect x="{wx + 38}" y="{wy + 88}" width="44" height="6" rx="2" fill="#5b616b"/>',
                        text(wx + 104, wy + 76, "RPI-RP2", 16, "start", 700, INK),
                        text(wx + 104, wy + 96, "（USB メモリのように見える）", 11, "start", 400, SUB)], dy=(1 - q) * 20, opacity=q)
        return frame(b, st.caption(t))
    return f, st.duration


VIDEOS = {"breadboard-inside": breadboard_inside, "pin-header": pin_header, "led-wiring": led_wiring,
          "button-wiring": button_wiring, "pot-wiring": pot_wiring, "bootsel": bootsel}


def main():
    names = sys.argv[1:] or list(VIDEOS)
    for name in names:
        f, duration = VIDEOS[name]()
        render("pico", name, f, duration)


if __name__ == "__main__":
    main()
