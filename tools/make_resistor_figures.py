#!/usr/bin/env python3
"""ピコの教科書の、抵抗の帯の読み方の図を作る。

    python3 tools/make_resistor_figures.py

- books/pico/images/resistor-bands.svg   7章 抵抗の値の読み方（330Ω の4本帯と5本帯、色と数字）
作り直したら python3 tools/translate_figures.py pico で英語の図も作り直す。
"""
from make_xmas_figures import OUT, SUB, text, line, svg

# 色の名前・塗り・上に書く数字の色
DIGITS = [("黒", "#222222", "#ffffff"), ("茶", "#8b4513", "#ffffff"), ("赤", "#d93a3a", "#ffffff"),
          ("橙", "#f08c00", "#ffffff"), ("黄", "#f2c500", "#2b2f36"), ("緑", "#2e7d32", "#ffffff"),
          ("青", "#1e63d6", "#ffffff"), ("紫", "#7b3fb0", "#ffffff"), ("灰", "#8a8f98", "#ffffff"),
          ("白", "#ffffff", "#2b2f36")]
C = {name: fill for name, fill, _ in DIGITS} | {"金": "#c9a227"}
LEAD = "#8a8f98"


def resistor(y, body, bands, label):
    """横向きの抵抗。bands は (x, 色の名前, 下に書く文字)"""
    b = [text(40, y + 5, label, 14, "start", 700),
         line(110, y, 560, y, LEAD, 4),
         f'<rect x="150" y="{y - 22}" width="370" height="44" rx="20" fill="{body}" stroke="#7d7462" stroke-width="1.5"/>']
    for x, name, note in bands:
        b.append(f'<rect x="{x - 9}" y="{y - 22}" width="18" height="44" fill="{C[name]}" stroke="#7d7462" stroke-width="0.8"/>')
        b.append(text(x, y + 42, name, 12, "middle", 400, SUB))
        b.append(text(x, y + 60, note, 13, "middle", 700))
    b.append(text(590, y + 7, "→ 330Ω", 20, "start", 700))
    return b


def bands():
    b = [text(380, 52, "離れた帯（金・茶）を右にして、左から読む", 13, "middle", 400, SUB)]
    b += resistor(100, "#e8d5a8", [(200, "橙", "3"), (250, "橙", "3"), (300, "茶", "0を1つ"), (470, "金", "誤差")], "4本帯")
    b += resistor(215, "#9cc3e6", [(190, "橙", "3"), (240, "橙", "3"), (290, "黒", "0"),
                                   (340, "黒", "0なし"), (470, "茶", "誤差")], "5本帯")
    # 色と数字
    b.append(text(40, 336, "色と数字", 14, "start", 700))
    for i, (name, fill, ink) in enumerate(DIGITS):
        x = 140 + i * 60
        b.append(f'<rect x="{x}" y="310" width="52" height="34" rx="5" fill="{fill}" stroke="#7d7462" stroke-width="1"/>')
        b.append(text(x + 26, 333, str(i), 16, "middle", 700, ink))
        b.append(text(x + 26, 364, name, 12, "middle", 400, SUB))
    return svg(760, 390, "抵抗の帯の読み方（330Ω の例）", b)


def main():
    (OUT / "resistor-bands.svg").write_text(bands())
    print("resistor-bands.svg を作りました")


if __name__ == "__main__":
    main()
