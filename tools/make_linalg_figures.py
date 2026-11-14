#!/usr/bin/env python3
"""線形代数の教科書（books/linalg）の図を SVG で作る。

    python3 tools/make_linalg_figures.py

色・文字の描き方は make_cow_figures.py と同じ。数値は教科書の例題と同じもの。
"""
import math
from pathlib import Path

from make_cow_figures import AXIS, GRID, MUTED, RED, S1, S2, S3, S4, TEXT, TEXT2, svg, t

OUT = Path(__file__).resolve().parent.parent / "books" / "linalg" / "images"
COLORS = {"s1": S1, "s2": S2, "s3": S3, "s4": S4, "red": RED, "muted": MUTED}


def markers():
    return "<defs>" + "".join(
        f'<marker id="m-{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0 0 L10 5 L0 10 z" fill="{c}"/></marker>' for k, c in COLORS.items()) + "</defs>"


class Plane:
    """座標平面。(ox, oy) が原点の画面の位置、s が1目盛りのピクセル"""

    def __init__(self, ox, oy, s, xr, yr):
        self.ox, self.oy, self.s, self.xr, self.yr = ox, oy, s, xr, yr

    def X(self, x):
        return self.ox + x * self.s

    def Y(self, y):
        return self.oy - y * self.s

    def grid(self, labels=True):
        b = []
        for x in range(self.xr[0], self.xr[1] + 1):
            b.append(f'<path d="M{self.X(x):.1f} {self.Y(self.yr[0]):.1f} V{self.Y(self.yr[1]):.1f}" stroke="{GRID}" stroke-width="1"/>')
        for y in range(self.yr[0], self.yr[1] + 1):
            b.append(f'<path d="M{self.X(self.xr[0]):.1f} {self.Y(y):.1f} H{self.X(self.xr[1]):.1f}" stroke="{GRID}" stroke-width="1"/>')
        b.append(f'<path d="M{self.X(self.xr[0]):.1f} {self.Y(0):.1f} H{self.X(self.xr[1]):.1f}" stroke="{AXIS}" stroke-width="1.5"/>')
        b.append(f'<path d="M{self.X(0):.1f} {self.Y(self.yr[0]):.1f} V{self.Y(self.yr[1]):.1f}" stroke="{AXIS}" stroke-width="1.5"/>')
        if labels:
            b.append(t(self.X(self.xr[1]) - 4, self.Y(0) - 6, "x", 12, "end", MUTED))
            b.append(t(self.X(0) + 6, self.Y(self.yr[1]) + 12, "y", 12, "start", MUTED))
            b.append(t(self.X(0) - 5, self.Y(0) + 14, "O", 11, "end", MUTED))
        return b

    def vec(self, x0, y0, x1, y1, color="s1", width=2.6, dash=None):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        return (f'<line x1="{self.X(x0):.1f}" y1="{self.Y(y0):.1f}" x2="{self.X(x1):.1f}" y2="{self.Y(y1):.1f}" '
                f'stroke="{COLORS[color]}" stroke-width="{width}" marker-end="url(#m-{color})"{da}/>')

    def line(self, pts, color, width=1.4, dash=None, fill="none", opacity=1):
        d = "M" + " L".join(f"{self.X(a):.1f} {self.Y(b):.1f}" for a, b in pts)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<path d="{d}" fill="{fill}" fill-opacity="{opacity}" stroke="{color}" stroke-width="{width}"{da}/>'

    def label(self, x, y, s, color=TEXT, size=13, anchor="start", dx=6, dy=-6):
        return t(self.X(x) + dx, self.Y(y) + dy, s, size, anchor, color, 700)


def fig_vectors():
    p = Plane(150, 330, 60, (-1, 5), (-1, 5))
    b = [markers()] + p.grid()
    b.append(p.line([(0, 0), (2, 1), (3, 4), (1, 3), (0, 0)], S3, 1, None, S3, 0.08))
    b.append(p.vec(2, 1, 3, 4, "muted", 1.6, "5 4"))
    b.append(p.vec(1, 3, 3, 4, "muted", 1.6, "5 4"))
    b += [p.vec(0, 0, 2, 1, "s1"), p.vec(0, 0, 1, 3, "s2"), p.vec(0, 0, 3, 4, "s3", 3)]
    b += [p.label(2, 1, "a = (2, 1)", S1, dy=16), p.label(1, 3, "b = (1, 3)", S2, dx=-8, dy=-8, anchor="end"),
          p.label(3, 4, "a + b = (3, 4)", S3)]
    b.append(t(560, 120, "和は、平行四辺形の対角線", 13, "start", TEXT, 700))
    b.append(t(560, 142, "（a の先に b をつないでもよい）", 12, "start", TEXT2))
    b.append(t(560, 190, "a + b = (2+1, 1+3) = (3, 4)", 13, "start", TEXT, 700))
    return svg(820, 380, b)


def fig_projection():
    p = Plane(170, 320, 60, (-2, 5), (-1, 4))
    b = [markers()] + p.grid()
    b.append(p.line([(-1, -0.5), (4.6, 2.3)], MUTED, 1, "3 4"))
    b += [p.vec(0, 0, 2, 1, "s1", 4), p.vec(0, 0, 1, 3, "s2")]
    b.append(p.vec(1, 3, 2, 1, "red", 1.6, "5 4"))
    # 直角の印
    u, v = (2 / math.sqrt(5), 1 / math.sqrt(5)), (-1 / math.sqrt(5), 2 / math.sqrt(5))
    k = 0.22
    b.append(p.line([(2 - k * u[0], 1 - k * u[1]), (2 - k * u[0] + k * v[0], 1 - k * u[1] + k * v[1]), (2 + k * v[0], 1 + k * v[1])], TEXT2, 1.2))
    # 角
    r = 0.7
    a0, a1 = math.atan2(1, 2), math.atan2(3, 1)
    b.append(f'<path d="M{p.X(r * math.cos(a0)):.1f} {p.Y(r * math.sin(a0)):.1f} A{r * p.s:.1f} {r * p.s:.1f} 0 0 0 {p.X(r * math.cos(a1)):.1f} {p.Y(r * math.sin(a1)):.1f}" fill="none" stroke="{TEXT2}" stroke-width="1.3"/>')
    b.append(p.label(0.75, 0.9, "θ = 45°", TEXT, 12))
    b += [p.label(2, 1, "a = (2, 1)", S1, dy=18), p.label(1, 3, "b = (1, 3)", S2)]
    b.append(t(560, 100, "b の a への正射影", 13, "start", TEXT, 700))
    b.append(t(560, 124, "= (a·b / |a|²) a = (5/5) a = (2, 1)", 12.5, "start", TEXT2))
    b.append(t(560, 160, "赤い点線 b − (2, 1) = (−1, 2) は", 12.5, "start", TEXT2))
    b.append(t(560, 182, "a と直交する（内積が 0）", 12.5, "start", TEXT2))
    b.append(t(560, 218, "cos θ = a·b / (|a||b|) = 5 / (√5 √10) = 1/√2", 12.5, "start", TEXT2))
    return svg(820, 390, b)


def fig_transform():
    b = [markers()]
    L = Plane(140, 300, 50, (-1, 4), (-1, 4))
    R = Plane(520, 300, 50, (-1, 4), (-1, 4))
    b += L.grid() + R.grid()
    b.append(L.line([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)], S1, 1.5, None, S1, 0.15))
    b += [L.vec(0, 0, 1, 0, "s1"), L.vec(0, 0, 0, 1, "s2")]
    b += [L.label(1, 0, "e₁", S1, 13, dy=16), L.label(0, 1, "e₂", S2, 13, dx=-14)]
    b.append(t(L.X(1.5), 46, "変換する前（面積 1）", 13, "middle", TEXT, 700))
    b.append(R.line([(0, 0), (2, 1), (3, 3), (1, 2), (0, 0)], S1, 1.5, None, S1, 0.15))
    b += [R.vec(0, 0, 2, 1, "s1"), R.vec(0, 0, 1, 2, "s2")]
    b += [R.label(2, 1, "Ae₁ = (2, 1)", S1, 12.5, dy=16), R.label(1, 2, "Ae₂ = (1, 2)", S2, 12.5, dx=-8, anchor="end")]
    b.append(t(R.X(1.5), 46, "変換したあと（面積 3 = |det A|）", 13, "middle", TEXT, 700))
    b.append(f'<line x1="{L.X(4) + 8}" y1="170" x2="{R.X(-1) - 8}" y2="170" stroke="{TEXT2}" stroke-width="1.8" marker-end="url(#m-muted)"/>')
    b.append(t((L.X(4) + R.X(-1)) / 2, 160, "A = (2 1; 1 2)", 12.5, "middle", TEXT, 700))
    return svg(820, 350, b)


def fig_eigen():
    p = Plane(300, 250, 34, (-3, 6), (-5, 6))
    b = [markers()] + p.grid()
    b.append(p.line([(-2.5, -2.5), (5.8, 5.8)], S1, 1, "3 4"))
    b.append(p.line([(-1.2, 2.4), (2.5, -5)], S2, 1, "3 4"))
    b += [p.vec(0, 0, 5, 5, "s1", 2, "6 4"), p.vec(0, 0, 1, 1, "s1", 3.4)]
    b += [p.vec(0, 0, 2, -4, "s2", 2, "6 4"), p.vec(0, 0, 1, -2, "s2", 3.4)]
    b += [p.vec(0, 0, 0, 1, "muted", 2.2), p.vec(0, 0, 1, 3, "muted", 1.6, "6 4")]
    b += [p.label(1, 1, "x₁ = (1, 1)", S1, 12, dy=14), p.label(5, 5, "Ax₁ = 5x₁", S1, 12, dx=-6, anchor="end")]
    b += [p.label(1, -2, "x₂ = (1, −2)", S2, 12), p.label(2, -4, "Ax₂ = 2x₂", S2, 12)]
    b += [p.label(0, 1, "(0, 1)", MUTED, 11.5, dx=-8, anchor="end", dy=4), p.label(1, 3, "A(0, 1) = (1, 3)", MUTED, 11.5, dx=-8, anchor="end")]
    b.append(t(560, 70, "A = (4 1; 2 3)", 13, "start", TEXT, 700))
    b.append(t(560, 100, "固有ベクトルは、向きが変わらず", 12.5, "start", TEXT2))
    b.append(t(560, 122, "長さだけが固有値の倍になる", 12.5, "start", TEXT2))
    b.append(t(560, 160, "(1, 1) は 5 倍、(1, −2) は 2 倍", 12.5, "start", TEXT, 700))
    b.append(t(560, 198, "ふつうのベクトル（灰色）の (0, 1) は", 12.5, "start", TEXT2))
    b.append(t(560, 220, "(1, 3) に変わり、向きも変わる", 12.5, "start", TEXT2))
    return svg(820, 440, b)


def fig_least_squares():
    p = Plane(110, 350, 45, (0, 5), (0, 7))
    b = [markers()] + p.grid()
    for x in range(1, 5):
        b.append(t(p.X(x), p.Y(0) + 16, str(x), 11, "middle", MUTED))
    for y in range(1, 8):
        b.append(t(p.X(0) - 8, p.Y(y) + 4, str(y), 11, "end", MUTED))
    b.append(p.line([(0, 0.5), (4.6, 0.5 + 1.4 * 4.6)], S1, 2.4))
    pts = [(1, 2), (2, 3), (3, 5), (4, 6)]
    for x, y in pts:
        yh = 0.5 + 1.4 * x
        b.append(p.line([(x, y), (x, yh)], RED, 2.4, "3 2"))
        b.append(f'<circle cx="{p.X(x):.1f}" cy="{p.Y(y):.1f}" r="4" fill="{S2}"/>')
    b.append(p.label(3.6, 0.5 + 1.4 * 3.6, "y = 0.5 + 1.4x", S1, 13, dx=-10, anchor="end"))
    b.append(t(480, 110, "最小二乗法", 13.5, "start", TEXT, 700))
    b.append(t(480, 136, "赤い点線（残差）の2乗の合計が", 12.5, "start", TEXT2))
    b.append(t(480, 158, "いちばん小さくなる直線を選ぶ", 12.5, "start", TEXT2))
    b.append(t(480, 196, "正規方程式 XᵀX β = Xᵀy を解くと", 12.5, "start", TEXT2))
    b.append(t(480, 218, "β = (0.5, 1.4)", 13, "start", TEXT, 700))
    return svg(820, 390, b)


def fig_ellipse():
    p = Plane(300, 200, 62, (-3, 3), (-3, 3))
    b = [markers()] + p.grid()
    # 5x² − 4xy + 2y² = 6 は、u = (1,2)/√5 の向きに半径 √6、v = (−2,1)/√5 の向きに半径 1 の楕円
    u = (1 / math.sqrt(5), 2 / math.sqrt(5))
    v = (-2 / math.sqrt(5), 1 / math.sqrt(5))
    pts = [(math.sqrt(6) * math.cos(a) * u[0] + math.sin(a) * v[0], math.sqrt(6) * math.cos(a) * u[1] + math.sin(a) * v[1])
           for a in [i * 2 * math.pi / 120 for i in range(121)]]
    b.append(p.line(pts, S1, 2.4, None, S1, 0.08))
    b.append(p.line([(-1.5 * u[0] * 2, -1.5 * u[1] * 2), (1.5 * u[0] * 2, 1.5 * u[1] * 2)], S2, 1.2, "5 4"))
    b.append(p.line([(-1.6 * v[0] * 1.5, -1.6 * v[1] * 1.5), (1.6 * v[0] * 1.5, 1.6 * v[1] * 1.5)], S3, 1.2, "5 4"))
    b += [p.vec(0, 0, u[0], u[1], "s2", 2.8), p.vec(0, 0, v[0], v[1], "s3", 2.8)]
    b += [p.label(u[0] * 2.5, u[1] * 2.5, "X 軸（固有値 1）", S2, 12), p.label(v[0] * 2, v[1] * 2, "Y 軸（固有値 6）", S3, 12, dx=-6, anchor="end")]
    b.append(t(560, 80, "5x² − 4xy + 2y² = 6", 13, "start", TEXT, 700))
    b.append(t(560, 106, "↓ 直交行列で座標を回す", 12.5, "start", TEXT2))
    b.append(t(560, 132, "X² + 6Y² = 6（X²/6 + Y² = 1）", 13, "start", TEXT, 700))
    b.append(t(560, 170, "軸の向きは、対称行列の", 12.5, "start", TEXT2))
    b.append(t(560, 192, "固有ベクトルの向き", 12.5, "start", TEXT2))
    return svg(820, 400, b)


FIGS = {"vectors.svg": fig_vectors, "projection.svg": fig_projection, "transform.svg": fig_transform,
        "eigen.svg": fig_eigen, "least-squares.svg": fig_least_squares, "ellipse.svg": fig_ellipse}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in FIGS.items():
        (OUT / name).write_text(fn(), encoding="utf-8")
    print(f"{len(FIGS)} 枚の図を書き出しました")
