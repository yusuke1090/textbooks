#!/usr/bin/env python3
"""ピコの教科書の動画を作る（使い方は tools/video.py）。

    .venv/bin/python tools/make_pico_videos.py            # 全部
    .venv/bin/python tools/make_pico_videos.py led-wiring # 選んで

- breadboard-inside  7章 ブレッドボードの中のつながり
- pin-header         7章 ピンヘッダのはんだ付け
- soldering-basics   7章 はんだごての準備（スポンジ・温め）・1か所の時間・片付け
- solder-cleanup     7章 金属たわしでこて先をきれいにする・吸い取り線で余分なはんだを取る
- tester-basics      7章 テスターで、ピコの 3.3V・ワイヤーの導通・抵抗を測る
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


# ---------------------------------------------------------------- 7章 はんだごての準備と片付け
TRAY = (100, 262, 230, 40)               # スポンジの入れ物（x, y, 幅, 高さ）
WORK = (460, 190)                        # 持っているときのこて先
REST = (500, 288)                        # こて台に置いたときのこて先


def mix(c1, c2, k):
    """色 c1 → c2 を k（0〜1）で混ぜる"""
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * clamp(k)):02x}" for x, y in zip(a, b))


def sponge(wet, squeeze=0.0):
    """こて台のスポンジ。wet: 水を含んだ量（0〜1）、squeeze: しぼっている強さ（0〜1）"""
    x, y, w, h = TRAY
    sh = 24 * (1 - 0.4 * squeeze)
    top = y + h - 6 - sh
    return [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#3a3f47"/>',
            f'<rect x="{x + 8}" y="{top:.1f}" width="{w - 16}" height="{sh:.1f}" rx="5" fill="{mix("#f4dc8e", "#c99a2e", wet)}"/>',
            f'<line x1="{x + w / 2}" y1="{top + 3:.1f}" x2="{x + w / 2}" y2="{top + sh - 3:.1f}" stroke="#8a6d2b" stroke-width="2"/>',
            text(x + w / 2, y + h + 20, "スポンジ", 12, "middle", 700, SUB)]


def tip_at(x, y, p=1.0):
    """iron(x, y, p) で描いたこての、先の座標"""
    off = (1 - p) * 130
    return x + 4 + off, y - 2 - off * 0.8


def tip_color(tx, ty, k, blob=0.0):
    """こて先の色。k=0 で黒っぽい（よごれ）、k=1 で銀色。blob はのせたはんだの量"""
    b = [f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="5" fill="{mix("#4a3b30", "#e6eaef", k)}"/>']
    if blob > 0:
        b.append(f'<circle cx="{tx - 1:.1f}" cy="{ty + 2:.1f}" r="{3 + 4 * blob:.1f}" fill="{SOLDER}" stroke="#9aa1ab" stroke-width="1"/>')
    if k > 0.6 or blob > 0:
        b.append(f'<circle cx="{tx - 2:.1f}" cy="{ty - 2:.1f}" r="1.8" fill="#ffffff"/>')
    return b


def gauge(temp, label, clock, power):
    """右の、こて先の温度と、経過時間"""
    x, y0, y1 = 712, 74, 290
    k = clamp((temp - 20) / (400 - 20))
    color = mix("#2f6fde", "#e8590c", clamp((temp - 60) / 250))
    y350 = y1 - (y1 - y0) * (350 - 20) / (400 - 20)
    b = [text(x, 30, "こて先の温度", 12, "middle", 700, SUB),
         text(x, 52, "電源 入" if power else "電源 切", 13, "middle", 700, "#2e7d32" if power else "#8a8f98"),
         f'<rect x="{x - 11}" y="{y0}" width="22" height="{y1 - y0}" rx="11" fill="#eef0f3" stroke="#c9ced6"/>',
         f'<rect x="{x - 7}" y="{y1 - (y1 - y0) * k:.1f}" width="14" height="{(y1 - y0) * k:.1f}" rx="7" fill="{color}"/>',
         f'<line x1="{x - 22}" y1="{y350:.1f}" x2="{x + 22}" y2="{y350:.1f}" stroke="#d93a3a" stroke-width="1.5" stroke-dasharray="4 3"/>',
         text(x - 26, y350 + 4, "350℃", 11, "end", 700, "#d93a3a"),
         text(x, 322, f"{temp:.0f}℃", 22, "middle", 700, color)]
    if label:
        b += [text(x, 346, label, 11, "middle", 700, SUB), text(x, 368, clock, 16, "middle", 700, INK)]
    return b


def steam(tx, ty, k):
    """スポンジでぬぐったときの湯気"""
    b = []
    for i in range(4):
        s = (k * 1.5 + i / 4) % 1
        b.append(f'<circle cx="{tx - 8 + 10 * i + 6 * s:.1f}" cy="{ty - 8 - 40 * s:.1f}" r="{4 + 6 * s:.1f}" fill="#c9ced6" opacity="{0.6 * (1 - s):.2f}"/>')
    return b


def stand(tx, ty):
    """こて台（こてを差しておく、ばねの筒と台）"""
    b = [f'<rect x="{tx - 40}" y="{ty + 34}" width="190" height="14" rx="4" fill="#3a3f47"/>',
         f'<line x1="{tx + 60}" y1="{ty + 34}" x2="{tx + 40}" y2="{ty - 18}" stroke="#3a3f47" stroke-width="6"/>']
    for k in range(6):                   # ばね: こての金属の部分に沿って
        cx, cy = tx + 10 + 6 * k, ty - 8 - 4.8 * k
        b.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="5" ry="13" transform="rotate(-38.7 {cx:.1f} {cy:.1f})" '
                 f'fill="none" stroke="#8a8f98" stroke-width="2.5"/>')
    return b


def joint(x, y, fill):
    """横から見た基板の穴と、部品の足。fill ははんだの量（0〜1）"""
    b = [f'<rect x="{x - 110}" y="{y}" width="220" height="12" rx="2" fill="{PICO}"/>',
         f'<rect x="{x - 16}" y="{y - 3}" width="32" height="3" fill="#c9a227"/>',
         f'<rect x="{x - 16}" y="{y + 12}" width="32" height="3" fill="#c9a227"/>',
         f'<line x1="{x}" y1="{y + 44}" x2="{x}" y2="{y - 50}" stroke="#9aa1ab" stroke-width="5" stroke-linecap="round"/>',
         text(x - 110, y + 32, "基板", 12, "start", 700, SUB),
         text(x + 10, y + 40, "部品の足", 12, "start", 700, SUB)]
    if fill > 0:
        top = y - 3
        b.append(f'<path d="M{x - 15} {top} Q{x - 5} {top - 6 * fill:.1f} {x - 3} {top - 18 * fill:.1f} L{x + 3} {top - 18 * fill:.1f} '
                 f'Q{x + 5} {top - 6 * fill:.1f} {x + 15} {top} Z" fill="{SOLDER}" stroke="#9aa1ab" stroke-width="1"/>')
    return b


def soldering_basics():
    st = Steps([("はんだごての準備と片付け", 2.5),
                ("① スポンジを水でぬらし、軽くしぼる（水がたれないくらい）", 4.5),
                ("② 電源を入れて待つ。温度調節つきで30秒〜1分、なしは2〜3分", 5),
                ("③ こて先を、ぬれたスポンジでさっとなでる（1秒）。銀色に光ればきれい", 5),
                ("④ こて先にはんだを少しのせる。すぐ溶ければ準備OK", 4),
                ("⑤ 足とパッドを2〜3秒温めてから、はんだを当てる。全部で5秒以内", 11),
                ("⑥ 使い終わったら、こて先にはんだを少しのせて電源を切り、こて台へ", 4.5),
                ("⑦ 電源を切っても10分くらいは熱い。冷めるまでさわらない", 5)])

    def f(t):
        i = st.index(t)
        b = []
        # 温度と時計
        if i < 2:
            temp, label, clock, power = 20, "", "", False
        elif i == 2:
            k = st.p(t, 2, 3.4)
            temp, label, clock, power = 20 + 330 * k, "電源を入れてから", f"0:{round(45 * k):02d}", True
        elif i < 6 or (i == 6 and st.local(t, 6) < 2.4):
            temp, label, clock, power = 350, "", "", True
        elif i == 6:
            temp, label, clock, power = 350, "", "", False
        else:
            k = st.p(t, 7, 3.6)
            m = 10 * k
            temp, label, clock, power = 350 - 300 * k, "電源を切ってから", f"{int(m)}:{int(m % 1 * 60):02d}", False
        b += gauge(temp, label, clock, power)
        heat = clamp((temp - 150) / 200)
        if i == 5:                                       # 1か所を付ける（大きく見せる）
            x, y = 400, 300
            lt = st.local(t, 5)
            p_iron = st.p(t, 5, 0.8) * (1 - st.p(t, 5, 0.8, 6.2))
            secs = clamp((lt - 1.2) / 4.6) * 4           # こてが当たってからの秒（動画では少しゆっくり）
            p_sol = st.p(t, 5, 0.6, 3.4) * (1 - st.p(t, 5, 0.6, 5.0))
            fill = st.p(t, 5, 1.4, 3.8)
            body = joint(x, y, fill)
            z = 1.7
            body += solder_wire(x - 4, y - 8, p_sol, fill, 12 / z)
            body += iron(x + 4, y - 6, p_iron, heat if p_iron > 0.99 else 0, 12 / z)
            b += zoom(body, z, x, y - 10, 300, 240)
            if lt >= 7.2:                                  # こてを離したら、固まるまで動かさない
                n = min(3, int((lt - 7.2) / 0.9) + 1)
                b.append(text(600, 110, str(n), 64, "middle", 700, "#2f6fde"))
                b.append(text(600, 140, "秒", 16, "middle", 700, SUB))
                b.append(text(600, 176, "固まるまで動かさない", 14, "middle", 700, INK))
            elif 0 < secs:
                n = min(4, int(secs) + 1)
                b.append(text(600, 110, str(n), 64, "middle", 700, "#d93a3a" if n >= 4 else INK))
                b.append(text(600, 140, "秒", 16, "middle", 700, SUB))
                note = "温める" if n <= 3 and p_sol <= 0 else ("はんだを当てる" if fill < 1 else "はんだ → こての順に離す")
                b.append(text(600, 176, note, 14, "middle", 700, INK))
            return frame(b, st.caption(t))
        # スポンジ
        wet = st.p(t, 1, 1.2) if i >= 1 else 0
        sq = 0.0
        if i == 1:
            lt = st.local(t, 1)
            sq = clamp((lt - 1.8) / 0.5) * (1 - clamp((lt - 3.2) / 0.5))
        b += sponge(wet, sq)
        if i == 1 and sq > 0.2:                          # しぼると水がたれる
            for k in range(3):
                s = (st.local(t, 1) * 1.6 + k / 3) % 1
                x0 = TRAY[0] + 60 + 50 * k
                b.append(f'<circle cx="{x0}" cy="{TRAY[1] + TRAY[3] + 8 + 30 * s:.1f}" r="3" fill="#4aa3df" opacity="{1 - s:.2f}"/>')
        # こて
        clean = 0.0 if i < 3 else 1.0
        blob = 0.0
        if i <= 2:
            x, y, p = WORK[0], WORK[1], 1.0
        elif i == 3:                                     # スポンジの上をなでる
            lt = st.local(t, 3)
            down = clamp((lt - 0.4) / 0.7)
            slide = clamp((lt - 1.1) / 1.2)
            up = clamp((lt - 2.5) / 0.7)
            sx0, sx1, sy = TRAY[0] + TRAY[2] - 40, TRAY[0] + 40, TRAY[1] + 14
            x = WORK[0] + (sx0 - WORK[0]) * down + (sx1 - sx0) * slide + (WORK[0] - sx1) * up
            y = WORK[1] + (sy - WORK[1]) * down + (WORK[1] - sy) * up
            p = 1.0
            clean = slide
            if 0 < slide < 1:
                b += steam(*tip_at(x, y), lt)
        elif i == 4:
            x, y, p = WORK[0], WORK[1], 1.0
            blob = st.p(t, 4, 0.8, 1.2)
        elif i == 6:
            lt = st.local(t, 6)
            blob = clamp((lt - 0.6) / 0.6)
            k = st.p(t, 6, 1.2, 2.6)
            x, y, p = WORK[0] + (REST[0] - WORK[0]) * k, WORK[1] + (REST[1] - WORK[1]) * k, 1.0
        else:
            x, y, p = REST[0], REST[1], 1.0
            blob = 1.0
        if i >= 6:
            b += stand(*tip_at(*REST))
        b += iron(x, y, p, heat)
        b += tip_color(*tip_at(x, y, p), clean, blob)
        if i == 4:
            b += solder_wire(*tip_at(x, y), st.p(t, 4, 0.6) * (1 - st.p(t, 4, 0.6, 2.4)), blob)
        if i == 7 and temp > 80:
            tx, ty = tip_at(*REST)
            b.append(text(tx - 30, ty - 40, "熱い！さわらない", 15, "end", 700, "#d93a3a"))
        return frame(b, st.caption(t))
    return f, st.duration


# ---------------------------------------------------------------- 7章 こて先をきれいにする・吸い取り線
COPPER = "#c77b3a"


def iron_tip(tx, ty, heat=0.6, fs=12):
    """こて先が (tx, ty) に来るように、こてを描く"""
    return iron(tx - 4, ty + 2, 1.0, heat, fs)


def wool(x, y):
    """金属たわし（真ちゅうの細い線を丸めたもの）と入れ物"""
    b = [f'<path d="M{x - 70} {y} L{x - 60} {y + 46} L{x + 60} {y + 46} L{x + 70} {y} Z" fill="#3a3f47"/>']
    for k in range(26):                  # 細い線のかたまり
        cx = x - 54 + (k * 37) % 108
        cy = y - 8 + (k * 13) % 22
        b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="16" ry="7" transform="rotate({(k * 47) % 180} {cx} {cy})" '
                 f'fill="none" stroke="#d4a52a" stroke-width="1.6"/>')
    b.append(text(x, y + 64, "金属たわし", 9, "middle", 700, SUB))
    return b


def pins_side(x1, x2, y, bridge):
    """横から見た基板と2本のピン。bridge は、ピンの間をつないだはんだの量（0〜1）"""
    top = y - 3
    b = [f'<rect x="{x1 - 140}" y="{y}" width="{x2 - x1 + 280}" height="12" rx="2" fill="{PICO}"/>']
    for x in (x1, x2):
        b += [f'<rect x="{x - 16}" y="{y - 3}" width="32" height="3" fill="#c9a227"/>',
              f'<line x1="{x}" y1="{y + 40}" x2="{x}" y2="{y - 24}" stroke="#9aa1ab" stroke-width="5" stroke-linecap="round"/>',
              f'<path d="M{x - 15} {top} Q{x - 5} {top - 6} {x - 3} {top - 18} L{x + 3} {top - 18} Q{x + 5} {top - 6} {x + 15} {top} Z" '
              f'fill="{SOLDER}" stroke="#9aa1ab" stroke-width="1"/>']
    if bridge > 0:
        h = 16 * bridge
        b.append(f'<path d="M{x1 + 3} {top} L{x1 + 3} {top - h:.1f} Q{(x1 + x2) / 2} {top - h - 6 * bridge:.1f} {x2 - 3} {top - h:.1f} '
                 f'L{x2 - 3} {top} Z" fill="{SOLDER}" stroke="#9aa1ab" stroke-width="1"/>')
    return b


def braid(x0, x1, y, silver=0.0, cut=None):
    """吸い取り線（横から見た、銅の編んだテープ）。x1 が先。silver は先から銀色になった長さ"""
    b = [f'<rect x="{x0}" y="{y - 4}" width="{x1 - x0}" height="8" fill="{COPPER}"/>']
    for x in range(int(x0) + 3, int(x1), 6):
        b.append(f'<line x1="{x}" y1="{y - 4}" x2="{x + 4}" y2="{y + 4}" stroke="#9c5a24" stroke-width="1"/>')
    if silver > 0:
        b.append(f'<rect x="{x1 - silver:.1f}" y="{y - 4}" width="{silver:.1f}" height="8" fill="{SOLDER}" stroke="#9aa1ab" stroke-width="1"/>')
    return b


def solder_cleanup():
    st = Steps([("こて先をきれいにする・余分なはんだを取る", 2.5),
                ("① 金属たわしに、こて先を軽く差して抜く（2〜3回）。銀色に光ればきれい", 6),
                ("② となりのピンと、はんだでつながってしまった（ブリッジ）", 3.5),
                ("③ 吸い取り線をはんだの上に置き、上からこてを押し当てる（2〜3秒）", 5),
                ("④ はんだが銅の線に吸い込まれて、銀色になる", 4),
                ("⑤ 吸い取り線とこてを、いっしょに離す", 3.5),
                ("⑥ 銀色になった先は、もう吸わないので、ニッパーで切って捨てる", 4)])

    def f(t):
        i = st.index(t)
        if i <= 1:                                       # 金属たわし
            b = wool(250, 300)
            home, inside = (470, 190), (262, 292)
            k = 0.0
            if i == 1:
                lt = st.local(t, 1) - 0.4
                k = clamp(lt / 4.8)                      # 2回差して抜く
                d = 0.5 - 0.5 * math.cos(2 * math.pi * min(2.0, max(0.0, lt / 2.4)))
            else:
                d = 0.0
            tx, ty = home[0] + (inside[0] - home[0]) * d, home[1] + (inside[1] - home[1]) * d
            b += iron_tip(tx, ty, 0.6, 12 / 1.6)
            b += tip_color(tx, ty, k)
            return frame(zoom(b, 1.6, 340, 250, 400, 215), st.caption(t))
        x1, x2, y = 360, 440, 300
        top = y - 3
        bridge = 1 - st.p(t, 4, 2.4) if i >= 4 else 1.0
        silver = 70 * st.p(t, 4, 2.4) if i >= 4 else 0
        lift = 70 * st.p(t, 5, 1.2) if i >= 5 else 0
        body = pins_side(x1, x2, y, bridge)
        if i == 2:
            body.append(text((x1 + x2) / 2, top - 70, "ブリッジ", 16, "middle", 700, "#d93a3a"))
            body.append(f'<path d="M{(x1 + x2) / 2} {top - 62} L{(x1 + x2) / 2} {top - 28}" stroke="#d93a3a" stroke-width="3" marker-end="url(#arr)"/>')
        if i >= 3:
            slide = st.p(t, 3, 1.2)
            end = x2 + 14
            bx1 = end - (1 - slide) * 400
            by = top - 30 - lift
            if i < 6:
                body += braid(bx1 - 420, bx1, by, silver)
            else:                                        # 先を切る
                c = st.p(t, 6, 0.8, 0.6)
                fall = st.p(t, 6, 1.0, 1.6)
                body += braid(bx1 - 420, bx1 - 70, by)
                body += group(braid(bx1 - 70, bx1, by, 70), dx=30 * fall, dy=140 * fall, opacity=1 - fall)
                if c > 0:
                    body.append(f'<line x1="{bx1 - 72}" y1="{by - 18}" x2="{bx1 - 72}" y2="{by + 18}" stroke="#d93a3a" stroke-width="2" stroke-dasharray="4 3" opacity="{c:.2f}"/>')
                    body.append(text(bx1 - 72, by - 26, "ニッパーで切る", 13, "middle", 700, "#d93a3a"))
            if i in (3, 4, 5):
                p_iron = st.p(t, 3, 0.9, 1.4) if i == 3 else 1.0
                body += iron(x1 + 44 - 4, by - 2, p_iron, 0.8 if p_iron >= 1 and i < 5 else 0, 12 / 1.6)
                body.append(text(bx1 - 300, by + 26, "吸い取り線", 12 / 1.6 * 1.6, "start", 700, COPPER))
        defs = ('<defs><marker id="arr" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto">'
                '<path d="M0 0 L10 5 L0 10 Z" fill="#d93a3a"/></marker></defs>')
        return frame([defs] + zoom(body, 1.6, 400, 270, 400, 220), st.caption(t))
    return f, st.duration


# ---------------------------------------------------------------- 7章 テスターの使い方
def tester_basics():
    from make_tester_figures import meter, probe, cable, plug, male_end, line, TERM, DIAL
    st = Steps([("テスターで、電圧・導通・抵抗を測る", 2.5),
                ("① 黒い棒を COM、赤い棒を VΩmA に差す", 3.5),
                ("② ダイヤルを、直流の電圧（V）の 20 にする", 3.5),
                ("③ 36番（3V3）と 38番（GND）の列に、ワイヤーを1本ずつ差す", 4),
                ("④ 黒い棒を GND、赤い棒を 3V3 のワイヤーの先に当てる → 3.30", 5),
                ("⑤ USB を抜いて、ダイヤルを ·))) （導通）にする", 4),
                ("⑥ ワイヤーの両はしに当てる。ピーと鳴れば、切れていない", 5),
                ("⑦ ダイヤルを Ω の 2000 にして、抵抗の両方の足に当てる → 328", 5.5),
                ("⑧ 使い終わったら OFF にする", 3)])
    MX, MY, MS = 130, 14, 0.83                       # テスターの位置と大きさ
    term = {k: (MX + x * MS, MY + y * MS) for k, (x, y) in TERM.items()}
    ZS, ZOX, ZOY, ZDX = 1.15, 440, 190, 335          # ブレッドボードの下の段を、右に大きく写す
    g = lambda x, y: (ZDX + ZS * (x - ZOX), ZS * (y - ZOY))
    REST = {"COM": (285, 250, 15), "VΩmA": (318, 250, 15)}
    VOLT = {"COM": (*g(488, 482), 90), "VΩmA": (*g(468, 455), 90)}
    WIRE = {"COM": (420, 232, 20), "VΩmA": (740, 232, -20)}
    RES = {"COM": (472, 232, 20), "VΩmA": (688, 232, -20)}
    ANG = {k: v[0] for k, v in DIAL.items()}

    def lerp(a, b, k):
        return tuple(x + (y - x) * k for x, y in zip(a, b))

    def f(t):
        i = st.index(t)
        # ダイヤルと画面
        if i <= 1:
            ang, shown = 0, ""
        elif i == 2:
            k = st.p(t, 2, 1.0)
            ang, shown = ANG["V20"] * k, "0.00" if k >= 1 else ""
        elif i in (3, 4):
            ang, shown = ANG["V20"], "0.00"
        elif i == 5:
            k = st.p(t, 5, 1.2, 1.0)
            ang, shown = ANG["V20"] + (ANG["CONT"] - ANG["V20"]) * k, "OL" if k >= 1 else "0.00"
        elif i == 6:
            ang, shown = ANG["CONT"], "OL"
        elif i == 7:
            k = st.p(t, 7, 1.0)
            ang, shown = ANG["CONT"] + (ANG["R2000"] - ANG["CONT"]) * k, "OL"
        else:
            k = st.p(t, 8, 1.0, 0.6)
            ang, shown = ANG["R2000"] * (1 - k), "OL" if k < 1 else ""
        # 棒の位置
        pos = dict(REST)
        touch = False
        if i == 4:
            k = st.p(t, 4, 1.2)
            pos = {n: lerp(REST[n], VOLT[n], k) for n in pos}
            touch = k >= 1
            if touch:
                shown = "3.30" if int(st.local(t, 4) * 3) % 4 else "3.29"
        elif i == 5:
            k = st.p(t, 5, 0.8)
            pos = {n: lerp(VOLT[n], REST[n], k) for n in pos}
        elif i == 6:
            k = st.p(t, 6, 1.2, 0.4)
            pos = {n: lerp(REST[n], WIRE[n], k) for n in pos}
            touch = k >= 1
            if touch:
                shown = "0.4"
        elif i == 7:
            back = st.p(t, 7, 0.6)
            k = st.p(t, 7, 1.2, 1.4)
            pos = {n: lerp(lerp(WIRE[n], REST[n], back), RES[n], k) for n in pos}
            touch = k >= 1
            if touch:
                shown = "328"
        elif i == 8:
            k = st.p(t, 8, 0.6)
            pos = {n: lerp(RES[n], REST[n], k) for n in pos}

        b = ['<defs><clipPath id="bbc"><rect x="335" y="0" width="465" height="402"/></clipPath></defs>']
        # 右: 測る物
        if i <= 5:
            wires = st.p(t, 3, 1.4) if i >= 3 else 0
            cols = [(26, "bottom"), (28, "bottom")] if wires >= 1 else []
            ux = 45 * st.p(t, 5, 0.8) if i == 5 else 0
            z = board(cols) + pico([(36, "3V3（36番）", 0, "end"), (38, "GND（38番）", 1, "end")]) + usb_plug(ux)
            for col, yy, tip, color in ((26, 455, 520, VSYS), (28, 482, 540, GND)):
                x = X(col)
                d = f"M{x} {ROW['j']} C{x} {yy - 10} {x - 10} {yy} {x - 40} {yy} L{tip} {yy}"
                z += draw_path(d, color, wires)
                if wires > 0:
                    z.append(dot(x, ROW["j"], color))
                if wires >= 1:
                    z += male_end(tip, yy, -1, color)
            b += ['<g clip-path="url(#bbc)">', f'<g transform="translate({ZDX} 0) scale({ZS}) translate({-ZOX} {-ZOY})">',
                  *z, "</g></g>"]
        elif i == 6:
            b += [f'<line x1="470" y1="230" x2="690" y2="230" stroke="#2e7d32" stroke-width="4"/>',
                  *male_end(470, 230, -1, "#2e7d32"), *male_end(690, 230, 1, "#2e7d32"),
                  text(580, 200, "ジャンパーワイヤー（オス-オス）", 13, "middle", 700)]
        else:
            b += [line(470, 230, 690, 230, LEG, 3),
                  '<rect x="545" y="216" width="70" height="28" rx="10" fill="#f4e3c4" stroke="#8a6d3b" stroke-width="1.5"/>']
            for j, c in enumerate(["#f08c00", "#f08c00", "#8b4513", "#c9a227"]):
                b.append(f'<rect x="{556 + j * 13 + (8 if j == 3 else 0)}" y="216" width="7" height="28" fill="{c}"/>')
            b.append(text(580, 200, "抵抗 330Ω（橙・橙・茶・金）", 13, "middle", 700))
        # 左: テスター
        b += group(meter(ang, shown), MX, MY, extra=f" scale({MS})")
        # 棒とコード
        plug_p = st.p(t, 1, 1.0) if i == 1 else (0 if i == 0 else 1)
        for n, color in (("COM", "#2b2f36"), ("VΩmA", "#d93a3a")):
            tx, ty = term[n]
            pr, back = probe(*pos[n], color)
            off = (1 - plug_p) * 60
            b.append(cable(tx, ty + off, back[0], back[1], color, 40))
            if plug_p > 0:
                b += group(plug(tx, ty + off, color), opacity=min(1, plug_p * 3))
            b += pr
        if i == 6 and touch:
            bx, by = MX + 112, MY + 40
            b.append(text(bx + 26, by + 6, "ピー", 18, "start", 700, "#d93a3a"))
            for r in (8, 15, 22):
                b.append(f'<path d="M{bx + r * 0.5:.1f} {by - r:.1f} Q{bx + r * 1.1:.1f} {by:.1f} {bx + r * 0.5:.1f} {by + r:.1f}" '
                         f'stroke="#d93a3a" stroke-width="2" fill="none"/>')
        return frame(b, st.caption(t))
    return f, st.duration


VIDEOS = {"breadboard-inside": breadboard_inside, "pin-header": pin_header, "led-wiring": led_wiring,
          "button-wiring": button_wiring, "pot-wiring": pot_wiring, "bootsel": bootsel,
          "soldering-basics": soldering_basics, "solder-cleanup": solder_cleanup,
          "tester-basics": tester_basics}


def main():
    names = sys.argv[1:] or list(VIDEOS)
    for name in names:
        f, duration = VIDEOS[name]()
        render("pico", name, f, duration)


if __name__ == "__main__":
    main()
