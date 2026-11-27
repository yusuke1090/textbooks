#!/usr/bin/env python3
"""ピコの教科書の、ブレッドボードの図の下に置く回路図を作る（記号は10章「回路図の読み方」と同じ）。

    python3 tools/make_circuit_figures.py

- books/pico/images/led-sch.svg         8章 外付けの LED（led-breadboard.svg の下）
- books/pico/images/led-nowire-sch.svg  8章 ジャンパーワイヤーなし（led-nowire.svg の下）
- books/pico/images/button-sch.svg      8章 外付けのボタン（button-breadboard.svg の下）
- books/pico/images/pot-sch.svg         9章 ボリューム（pot-breadboard.svg の下）
- books/pico/images/xmas-sch.svg        付録G イルミネーション（xmas-breadboard.svg の下）
作り直したら python3 tools/translate_figures.py pico で英語の図も作り直す。
"""
from make_xmas_figures import OUT, INK, SUB, text, line, svg
from make_schematic_figures import W, wire, dot, ic, res, led_h

BW = 80                     # ピコの箱の幅
L = 26                      # IC の足の長さ（make_schematic_figures と同じ）


def pico(x, y, pins, pitch, w=BW):
    """ピコの箱（足は右）。足の先の x と、名前 → y を返す"""
    p, at, _ = ic(x, y, w, [], pins, "ピコ", "", pitch=pitch)
    return p, x + w + L, {name: py for name, (_, py) in at.items()}


def note(y, s):
    return text(380, y, s, 12, "middle", 400, SUB)


def switch(x1, x2, y):
    """横向きのスイッチ（押していない形）"""
    cx = (x1 + x2) / 2
    return [wire((x1, y), (cx - 18, y)), dot(cx - 18, y), wire((cx - 18, y), (cx + 16, y - 16)),
            dot(cx + 18, y), wire((cx + 18, y), (x2, y)), text(cx, y + 26, "SW1", 12, "middle", 700)]


def battery(x1, x2, y):
    """横向きの電池（左が＋）。単3×3本"""
    cx = (x1 + x2) / 2
    out = [wire((x1, y), (cx - 15, y)), wire((cx + 15, y), (x2, y))]
    for dx in (-15, 5):
        out += [line(cx + dx, y - 14, cx + dx, y + 14, INK, W), line(cx + dx + 10, y - 7, cx + dx + 10, y + 7, INK, W + 2)]
    out += [text(cx - 22, y - 10, "+", 13, "end", 700),
            text(cx, y + 34, "BT1", 12, "end", 700), text(cx + 6, y + 34, "4.5V（単3×3本）", 12, "start", 400, SUB)]
    return out


def led_loop(order):
    """8章の外付けの LED。order は GP15 の側から並べる部品（"R" か "D"）"""
    bx = 202
    b, x0, ys = pico(bx, 64, [("20", "GP15"), ("18", "GND")], 84)
    y1, y2 = ys["GP15"], ys["GND"]
    x = x0
    for part in order:
        if part == "R":
            b += res(x, y1, x + 110, y1, "R1", "220Ω")
            x += 110
        else:
            b += led_h(x, x + 90, y1)
            b.append(text(x + 45, y1 + 30, "D1", 12, "middle", 700))
            x += 90
    b.append(wire((x, y1), (x + 50, y1), (x + 50, y2), (x0, y2)))
    return b, y2


def led():
    b, y = led_loop("RD")
    b.append(note(y + 44, "LED の記号は、三角の左が長い足（＋）。記号の読み方は10章"))
    return svg(760, y + 62, "外付けの LED の回路図", b)


def led_nowire():
    b, y = led_loop("DR")
    b.append(note(y + 44, "抵抗は LED の後ろでも、働きは同じ"))
    return svg(760, y + 62, "ジャンパーワイヤーなしの回路図", b)


def button():
    b, x0, ys = pico(222, 64, [("19", "GP14"), ("23", "GND")], 84)
    y1, y2 = ys["GP14"], ys["GND"]
    b += switch(x0, x0 + 150, y1)
    b.append(wire((x0 + 150, y1), (x0 + 210, y1), (x0 + 210, y2), (x0, y2)))
    b.append(note(y2 + 44, "ふだんは 1（ピコの中のプルアップ）。押すと GND とつながって 0"))
    return svg(760, y2 + 62, "ボタンの回路図", b)


def pot():
    bx, w = 210, 100
    b, x0, ys = pico(bx, 64, [("36", "3V3(OUT)"), ("31", "GP26"), ("28", "GND")], 56, w)
    ya, yb, yc = ys["3V3(OUT)"], ys["GP26"], ys["GND"]
    xp = x0 + 160
    # ボリューム: 上の足 → 3V3、下の足 → GND、真ん中の足（矢印）→ GP26
    b.append(wire((x0, ya), (xp, ya), (xp, yb - 16)))
    pts = [(xp, yb - 16)] + [(xp + (6 if k % 2 == 0 else -6), yb - 12 + 8 * k) for k in range(4)] + [(xp, yb + 16)]
    b.append(wire(*pts))
    b.append(wire((xp, yb + 16), (xp, yc), (x0, yc)))
    tip = xp - 9
    b.append(wire((x0, yb), (tip, yb)))
    b.append(f'<path d="M{tip - 10} {yb - 6} L{tip} {yb} L{tip - 10} {yb + 6} Z" fill="{INK}"/>')
    b += [text(xp + 16, yb - 2, "RV1", 12, "start", 700), text(xp + 16, yb + 13, "10kΩ", 12, "start", 400, SUB)]
    b.append(note(yc + 44, "矢印が真ん中の足。つまみを回すと、矢印が上下に動く"))
    return svg(760, yc + 62, "ボリュームの回路図", b)


XMAS = [("1", "GP0", "330Ω", "赤", "#d93a3a"), ("2", "GP1", "100Ω", "緑", "#2e7d32"), ("4", "GP2", "330Ω", "黄", "#c79100"),
        ("5", "GP3", "100Ω", "青", "#2f6fde"), ("6", "GP4", "100Ω", "白", "#8a8f98"), ("7", "GP5", "330Ω", "赤", "#d93a3a"),
        ("9", "GP6", "100Ω", "緑", "#2e7d32"), ("10", "GP7", "330Ω", "黄", "#c79100"), ("11", "GP8", "100Ω", "青", "#2f6fde"),
        ("12", "GP9", "100Ω", "白", "#8a8f98")]


def xmas():
    pins = [(n, gp) for n, gp, *_ in XMAS] + [("38", "GND"), ("39", "VSYS")]
    b, x0, ys = pico(212, 64, pins, 38, 70)
    xb = x0 + 270                                      # GND にまとめる縦の線
    for i, (_, gp, ohm, name, color) in enumerate(XMAS):
        y = ys[gp]
        b += res(x0, y, x0 + 90, y, f"R{i + 1}", ohm)
        b += led_h(x0 + 90, x0 + 170, y)
        b += [text(x0 + 180, y - 6, f"D{i + 1}", 11, "start", 700), text(x0 + 214, y - 6, name, 11, "start", 700, color)]
        b.append(wire((x0 + 170, y), (xb, y)))
        if i:
            b.append(dot(xb, y))
    yg, yv = ys["GND"], ys["VSYS"]
    b.append(wire((xb, ys["GP0"]), (xb, yv)))
    b += [wire((x0, yg), (xb, yg)), dot(xb, yg)]
    b += battery(x0, xb, yv)
    return svg(760, yv + 52, "イルミネーションの回路図", b)


def main():
    figs = {"led-sch": led, "led-nowire-sch": led_nowire, "button-sch": button, "pot-sch": pot, "xmas-sch": xmas}
    for name, make in figs.items():
        (OUT / f"{name}.svg").write_text(make())
    print("・".join(f"{n}.svg" for n in figs), "を作りました")


if __name__ == "__main__":
    main()
