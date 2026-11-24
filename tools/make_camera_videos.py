#!/usr/bin/env python3
"""ピコの教科書の付録I（安いカメラの写真を PC に映す）の動画を作る（使い方は tools/video.py）。

    .venv/bin/python tools/make_camera_videos.py              # 動画を作る
    .venv/bin/python tools/make_camera_videos.py --still フォルダ 5 20   # その秒のコマを PNG にして見る

- camera-wiring  カメラ（OV7670・18ピン）とピコの配線、書き込んで明るさで確かめるまで

ブレッドボードは make_breadboard_figures.py と同じ（ピコは USB を右にして 11〜30列）。
"""
import sys

from make_breadboard_figures import X, ROW, MARK, board, pico, col_of
from make_xmas_figures import PIN
from video import Steps, frame, group, draw_path, render, text, INK

S, OX, OY = 0.7, 281, 27                 # ブレッドボードの図を縮めて、右に置く


def at(x, y):
    """ブレッドボードの図の座標 → 画面の座標"""
    return OX + S * x, OY + S * y


def hole(col, row):
    return at(X(col), ROW[row])


POWER, GND, SCCB, SYNC, CLK, DATA = "#d93a3a", "#2b2f36", "#2e7d32", "#7b4fd6", "#e07b00", "#2f6fde"

# カメラのピンの並び（2列×9本。左の列, 右の列）
HEADER = [("3.3V", "GND"), ("SIOC", "SIOD"), ("VSYNC", "HREF"), ("PCLK", "XCLK"), ("D7", "D6"),
          ("D5", "D4"), ("D3", "D2"), ("D1", "D0"), ("RESET", "PWDN")]
# カメラのピン → (ピコの物理ピン, ブレッドボードの段, 色)
DEST = {"3.3V": (36, "j", POWER), "GND": (38, "j", GND), "SIOC": (17, "a", SCCB), "SIOD": (16, "a", SCCB),
        "VSYNC": (4, "a", SYNC), "HREF": (5, "a", SYNC), "PCLK": (6, "a", SYNC), "XCLK": (7, "a", CLK),
        "D0": (19, "a", DATA), "D1": (20, "a", DATA), "D2": (21, "j", DATA), "D3": (22, "j", DATA),
        "D4": (24, "j", DATA), "D5": (25, "j", DATA), "D6": (26, "j", DATA), "D7": (27, "j", DATA),
        "RESET": (36, "i", POWER), "PWDN": (38, "i", GND)}

CAM_X, CAM_Y, CAM_W, CAM_H = 14, 66, 240, 262
PX_L, PX_R = 170, 196                    # ピンの列の x
ROW0, ROW_DY = 92, 27                    # 1段目のピンの y と間隔
LENS = (76, 168)

# 線の通り道。カメラを出たら、縦の位置 XV で上か下へ曲がり、ブレッドボードの上（TOP）か下（BOTTOM）の道を通って穴へ。
# 上の道は外側から、下の道も外側から並べる（右の穴へ行く線ほど外側。穴の近くで交わらない）
TOP = ["VSYNC", "HREF", "PCLK", "XCLK", "SIOD", "SIOC", "D0", "D1"]
BOTTOM = ["PWDN", "GND", "RESET", "3.3V", "D7", "D6", "D5", "D4", "D3", "D2"]
LANE = {n: 12 + 6 * k for k, n in enumerate(TOP)} | {n: 396 - 5.6 * k for k, n in enumerate(BOTTOM)}
# 縦の位置の順番（左から）。交わる数が少なくなるように選んだ
XV = {n: 266 + 11 * k for k, n in enumerate(["RESET", "PWDN", "VSYNC", "HREF", "SIOD", "SIOC", "PCLK", "XCLK", "D0",
                                             "D3", "D7", "D5", "D4", "D6", "GND", "D2", "D1", "3.3V"])}


def cam_pin(name):
    for r, pair in enumerate(HEADER):
        if name in pair:
            return (PX_L if pair[0] == name else PX_R), ROW0 + r * ROW_DY
    raise KeyError(name)


def camera(active=()):
    """カメラの基板（レンズは左、ピンは右に2列×9本）。active は目立たせるピンの名前"""
    b = [f'<rect x="{CAM_X}" y="{CAM_Y}" width="{CAM_W}" height="{CAM_H}" rx="10" fill="#1d3557"/>',
         f'<circle cx="{LENS[0]}" cy="{LENS[1]}" r="44" fill="#2b2f36"/>',
         f'<circle cx="{LENS[0]}" cy="{LENS[1]}" r="32" fill="#0b1320" stroke="#8a8f98" stroke-width="4"/>',
         f'<circle cx="{LENS[0]}" cy="{LENS[1]}" r="12" fill="#2a4a7a"/>',
         f'<circle cx="{LENS[0] - 8}" cy="{LENS[1] - 9}" r="4" fill="#ffffff" opacity=".5"/>',
         text(LENS[0], LENS[1] + 70, "OV7670", 14, "middle", 700, "#ffffff")]
    for r, (left, right) in enumerate(HEADER):
        y = ROW0 + r * ROW_DY
        for name, x in ((left, PX_L), (right, PX_R)):
            if name in active:
                b.append(f'<circle cx="{x}" cy="{y}" r="10" fill="none" stroke="{MARK}" stroke-width="3"/>')
            b.append(f'<rect x="{x - 4}" y="{y - 4}" width="8" height="8" fill="{PIN}"/>')
        for name, x, anchor in ((left, PX_L - 13, "end"), (right, PX_R + 13, "start")):
            on = name in active
            b.append(text(x, y + 4.5, name, 12.5 if on else 11, anchor, 700, MARK if on else "#c9d6e8"))
    return b


def housing(name):
    """ワイヤーのメス（カメラのピンにかぶせる黒い四角）"""
    x, y = cam_pin(name)
    return f'<rect x="{x - 6}" y="{y - 6}" width="12" height="12" rx="2" fill="#111418" stroke="#4a515c" stroke-width="1"/>'


def rounded(pts, r=7):
    """折れ線の角を丸くした path"""
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for (x0, y0), (x1, y1), (x2, y2) in zip(pts, pts[1:], pts[2:]):
        l1, l2 = max(abs(x1 - x0), abs(y1 - y0)), max(abs(x2 - x1), abs(y2 - y1))
        k = min(r, l1 / 2, l2 / 2)
        ax, ay = x1 - (x1 - x0) / l1 * k, y1 - (y1 - y0) / l1 * k
        bx, by = x1 + (x2 - x1) / l2 * k, y1 + (y2 - y1) / l2 * k
        d += f" L{ax:.1f} {ay:.1f} Q{x1:.1f} {y1:.1f} {bx:.1f} {by:.1f}"
    return d + f" L{pts[-1][0]:.1f} {pts[-1][1]:.1f}"


def wire_points(name):
    x1, y1 = cam_pin(name)
    pin, row, _ = DEST[name]
    x2, y2 = hole(col_of(pin), row)
    gap = 17 if x1 == PX_L else 10               # ピンの段の間を通って、右へ出る（左の列は右の列のピンの下を通る）
    pts = [(x1, y1), (x1 + 8, y1 + gap), (XV[name], y1 + gap), (XV[name], LANE[name])]
    if row == "i":                                # i の段は、j の穴の線と重ならないように左から入る
        return pts + [(x2 - 7, LANE[name]), (x2 - 7, y2), (x2, y2)]
    return pts + [(x2, LANE[name]), (x2, y2)]


def wire(name, p, dim=False):
    """カメラのピンからブレッドボードの穴まで、p（0〜1）だけ描く。返すのは（線, 両はし）"""
    if p <= 0:
        return [], []
    color = DEST[name][2]
    pin, row, _ = DEST[name]
    x2, y2 = hole(col_of(pin), row)
    lines = draw_path(rounded(wire_points(name)), color, p, 3)
    ends = [housing(name)]
    if p >= 1:
        ends.append(f'<rect x="{x2 - 3.5:.1f}" y="{y2 - 3.5:.1f}" width="7" height="7" rx="1.5" fill="{color}" stroke="#ffffff" stroke-width="1"/>')
    if dim:
        lines = group(lines, opacity=0.3)
    return lines, ends


def pin_numbers(pins):
    """ピコの上に、いま使うピンの番号を出す"""
    b = []
    for pin in pins:
        x, _ = at(X(col_of(pin)), 0)
        if pin <= 20:
            y = at(0, ROW["c"])[1] + 17
        else:
            y = at(0, ROW["h"])[1] - 9
        b.append(text(x, y, str(pin), 10, "middle", 700, "#ffffff"))
    return b


def usb_plug(ux):
    """ピコの USB に差すケーブル。ux だけ右に離れる（0 で差さっている）"""
    x, y = at(X(30) + 30, (ROW["c"] + ROW["h"]) / 2)
    x += ux
    return [f'<rect x="{x:.1f}" y="{y - 8:.1f}" width="26" height="16" rx="2" fill="#3a3f47"/>',
            f'<line x1="{x + 26:.1f}" y1="{y:.1f}" x2="{x + 300:.1f}" y2="{y:.1f}" stroke="#3a3f47" stroke-width="6"/>']


def monitor(lines, x=470, y=66, w=316):
    """右上に出す、ピコの出力の窓。lines は [(字, 色), …]"""
    h = 32 + 21 * len(lines)
    b = [f'<rect x="{x + 3}" y="{y + 3}" width="{w}" height="{h}" rx="8" fill="#000000" opacity=".15"/>',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#1e2228"/>',
         text(x + 12, y + 19, "Serial Monitor", 11, "start", 700, "#9aa1ab")]
    for i, (s, color) in enumerate(lines):
        b.append(text(x + 12, y + 41 + 21 * i, s, 12.5, "start", 700, color).replace("<text ", '<text xml:space="preserve" ', 1))
    return b


def hand(p):
    """レンズをふさぐ手。p=0 で左下に離れている、p=1 でレンズの上"""
    dx, dy = -(1 - p) * 200, (1 - p) * 140
    skin, edge = "#f1c7a5", "#d9a77f"
    x, y = LENS[0] - 6 + dx, LENS[1] + dy
    b = [f'<rect x="{x - 26 + 18 * k}" y="{y - 70 + abs(k - 1.5) * 9}" width="16" height="64" rx="8" fill="{skin}" stroke="{edge}" stroke-width="1.5"/>'
         for k in range(4)]
    b.append(f'<ellipse cx="{x + 4}" cy="{y + 10}" rx="44" ry="40" fill="{skin}" stroke="{edge}" stroke-width="1.5"/>')
    b.append(f'<rect x="{x - 26}" y="{y + 30}" width="58" height="120" rx="20" fill="{skin}" stroke="{edge}" stroke-width="1.5"/>')
    return group(b, opacity=min(1.0, p * 3))


# ---------------------------------------------------------------- 配線
GROUPS = [["3.3V", "GND"], ["SIOC", "SIOD"], ["VSYNC", "HREF", "PCLK"], ["XCLK"],
          ["D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7"], ["RESET", "PWDN"]]
GAP = (0.9, 0.9, 0.8, 0.9, 0.55, 0.9)            # 同じまとまりの中で、次の線を始めるまでの秒


def camera_wiring():
    st = Steps([("カメラ（OV7670）とピコを、オス-メスのワイヤー18本でつなぐ", 3),
                ("① USB を外す", 2.5),
                ("電源: 3.3V → 36番の列、GND → 38番の列", 4),
                ("設定の線: SIOC → 17番（GP13）、SIOD → 16番（GP12）", 4),
                ("合図の線: VSYNC → 4番、HREF → 5番、PCLK → 6番", 4.5),
                ("時計: XCLK → 7番（GP5）", 3),
                ("データ: D0〜D7 → 19・20・21・22・24・25・26・27番（GP14〜GP21）", 7),
                ("RESET → 36番の列、PWDN → 38番の列（同じ列に2本で大丈夫）", 4.5),
                ("USB をつないで、配線を確かめるプログラムを書き込む", 4),
                ("レンズを手でふさいで、明るさの数が小さくなれば成功", 5.5)])
    first = 2                                     # 線を差す最初の手順

    def f(t):
        i = st.index(t)
        lines, ends, cols, active, nums = [], [], [], [], []
        for g, names in enumerate(GROUPS):
            step = first + g
            for k, name in enumerate(names):
                p = st.p(t, step, 1.0, k * GAP[g]) if i >= step else 0.0
                ln, en = wire(name, p, dim=step < i < 8)
                lines += ln
                ends += en
                if i == step:
                    pin, row, _ = DEST[name]
                    cols.append((col_of(pin), "top" if row in "ab" else "bottom"))
                    active.append(name)
                    nums.append(pin)
        b = []
        b += group(board(cols) + pico([], name_dx=60, name_dy=6), extra=f" translate({OX} {OY}) scale({S})")
        b += pin_numbers(sorted(set(nums)))
        # USB: 外す → 差す
        out = st.p(t, 1, 0.8)
        back = st.p(t, 8, 0.8)
        b += usb_plug(60 * out * (1 - back))
        b += camera(active)
        b += lines + ends
        if i == first:                            # 最初の線のときだけ、メスとオスの説明
            q = st.p(t, first, 0.5, 1.2)
            x2, y2 = hole(col_of(36), "j")
            halo = '<text stroke="#ffffff" stroke-width="5" paint-order="stroke" '     # 線の上でも読めるように白いふち
            b += group([text(CAM_X + CAM_W, CAM_Y - 12, "メス → カメラのピン", 13, "end", 700, INK),
                        text(x2 - 24, y2 + 4, "オス → 同じ縦の列の穴", 13, "end", 700, INK).replace("<text ", halo, 1)], opacity=q)
        if i >= 8:
            q1 = st.p(t, 8, 0.4, 1.4)
            q2 = st.p(t, 8, 0.4, 2.4)
            q3 = st.p(t, 9, 0.4, 2.0)
            ml = []
            if q1 > 0:
                ml.append(("カメラ: OV7670", "#7ee787"))
            if q2 > 0:
                ml.append(("320×240 の写真 153600 バイト  明るさ 118", "#e6edf3"))
            if q3 > 0:
                ml.append(("320×240 の写真 153600 バイト  明るさ 6", "#ffb454"))
            if ml:
                b += monitor(ml)
        if i >= 9:
            b += hand(st.p(t, 9, 1.0, 0.2))
        return frame(b, st.caption(t))
    return f, st.duration


VIDEOS = {"camera-wiring": camera_wiring}


def still(out, times):
    """決めた秒のコマを、フォルダ out に PNG で出す（見た目を確かめる用）"""
    from pathlib import Path
    from playwright.sync_api import sync_playwright
    from video import fit_caption, PX_W, PX_H
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    f, _ = camera_wiring()
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="chrome")
        page = browser.new_page(viewport={"width": PX_W, "height": PX_H})
        for t in times:
            page.set_content(f"<html><body style='margin:0;overflow:hidden'>{fit_caption(f(t))}</body></html>")
            page.screenshot(path=str(out / f"still-{t:05.1f}.png"))
            print(out / f"still-{t:05.1f}.png")
        browser.close()


def main():
    args = sys.argv[1:]
    if args[:1] == ["--still"]:
        still(args[1], [float(a) for a in args[2:]])
        return
    for name in args or VIDEOS:
        f, duration = VIDEOS[name]()
        render("pico", name, f, duration)


if __name__ == "__main__":
    main()
