#!/usr/bin/env python3
"""統計（books/stats）・機械学習（books/ml）・Docker（books/docker）の教科書の図を SVG で作る。

    python3 tools/make_study_figures.py

軸・線・凡例の描き方は make_cow_figures.py と同じものを使う（色も同じ、検証ずみの順番）。
グラフは式から計算したもの。データの図は教科書の本文の例と同じ値。
"""
import math
from pathlib import Path

from make_cow_figures import (AXIS, GRID, MUTED, RED, S1, S2, S3, TEXT, TEXT2, WATER, Plot, legend, smooth, svg, t)

ROOT = Path(__file__).resolve().parent.parent
STATS = ROOT / "books" / "stats" / "images"
ML = ROOT / "books" / "ml" / "images"
DOCKER = ROOT / "books" / "docker" / "images"


def area(p, pts, color, opacity):
    """曲線と横軸のあいだを塗る"""
    d = f"M{p.X(pts[0][0]):.1f} {p.Y(0):.1f} " + " ".join(f"L{p.X(a):.1f} {p.Y(b):.1f}" for a, b in pts) + f" L{p.X(pts[-1][0]):.1f} {p.Y(0):.1f} Z"
    return f'<path d="{d}" fill="{color}" opacity="{opacity}"/>'


def phi(x):
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)


def chi2_pdf(x, k):
    if x <= 0:
        return 0.0
    return x ** (k / 2 - 1) * math.exp(-x / 2) / (2 ** (k / 2) * math.gamma(k / 2))


def t_pdf(x, v):
    return math.gamma((v + 1) / 2) / (math.sqrt(v * math.pi) * math.gamma(v / 2)) * (1 + x * x / v) ** (-(v + 1) / 2)


def gamma_pdf(x, shape, scale):
    if x <= 0:
        return 0.0
    return x ** (shape - 1) * math.exp(-x / scale) / (math.gamma(shape) * scale ** shape)


# ---------------------------------------------------------------------------
# 統計
def fig_normal():
    p = Plot(70, 40, 770, 250, -4, 4, 0, 0.45)
    b = [area(p, smooth(phi, -2, 2), S1, 0.16), area(p, smooth(phi, -1, 1), S1, 0.22)]
    b += p.grid([0, 0.1, 0.2, 0.3, 0.4], [(v, f"{v}σ" if v else "0（平均）") for v in range(-4, 5)], "確率密度", "平均からの離れ方 / distance from the mean", lambda v: f"{v:.1f}")
    b.append(p.line(smooth(phi, -4, 4), S1, 2.5))
    for v in (-2, -1, 1, 2):
        b.append(f'<path d="M{p.X(v):.1f} {p.Y(phi(v)):.1f} V{p.y1}" stroke="{S1}" stroke-width="1" stroke-dasharray="4 3"/>')
    b.append(t(p.X(0), p.Y(0.2), "±1σ に約 68%", 13, "middle", TEXT, 700))
    b.append(t(p.X(0), p.Y(0.2) + 16, "68% within ±1σ", 11, "middle", TEXT2))
    b.append(f'<path d="M{p.X(-2)+4:.1f} {p.Y(0.03):.1f} H{p.X(2)-4:.1f}" stroke="{TEXT2}" stroke-width="1.2" marker-start="url(#ah)" marker-end="url(#ah)"/>')
    b.append(t(p.X(0), p.Y(0.03) - 6, "±2σ に約 95%（正確には ±1.96σ）/ 95% within ±2σ", 11.5, "middle", TEXT, 700))
    return svg(820, 300, b)


def fig_chi2():
    p = Plot(70, 40, 770, 250, 0, 20, 0, 0.5)
    b = p.grid([0, 0.1, 0.2, 0.3, 0.4, 0.5], [(v, str(v)) for v in range(0, 21, 2)], "確率密度", "値 / value", lambda v: f"{v:.1f}")
    for k, col in ((2, S1), (4, S2), (8, S3)):
        b.append(p.line(smooth(lambda x: min(chi2_pdf(x, k), 0.55), 0.02, 20, 200), col, 2.5))
    b.append(t(p.X(1.6), p.Y(0.42), "自由度 2", 12, "start", TEXT, 700))
    b.append(t(p.X(2.6), p.Y(0.2), "自由度 4", 12, "start", TEXT, 700))
    b.append(t(p.X(8.8), p.Y(0.115), "自由度 8", 12, "start", TEXT, 700))
    b += legend(470, 22, [(S1, "k = 2"), (S2, "k = 4"), (S3, "k = 8")])
    b.append(t(p.x1, p.Y(0.33), "平均 = k、分散 = 2k", 12, "end", TEXT2))
    return svg(820, 300, b)


def fig_t():
    p = Plot(70, 40, 770, 250, -4, 4, 0, 0.45)
    b = p.grid([0, 0.1, 0.2, 0.3, 0.4], [(v, str(v)) for v in range(-4, 5)], "確率密度", "値 / value", lambda v: f"{v:.1f}")
    b.append(p.line(smooth(phi, -4, 4), TEXT2, 2, "6 4"))
    b.append(p.line(smooth(lambda x: t_pdf(x, 10), -4, 4), S2, 2.5))
    b.append(p.line(smooth(lambda x: t_pdf(x, 2), -4, 4), S1, 2.5))
    b += legend(380, 22, [(TEXT2, "標準正規 / N(0,1)"), (S2, "t（自由度10）"), (S1, "t（自由度2）")])
    b.append(t(p.X(2.55), p.Y(0.07), "t（自由度2）はすそが重い", 12, "start", TEXT, 700))
    b.append(f'<path d="M{p.X(2.5):.1f} {p.Y(0.067):.1f} L{p.X(2.3):.1f} {p.Y(t_pdf(2.3, 2)):.1f}" stroke="{S1}" stroke-width="1.5"/>')
    return svg(820, 300, b)


def fig_clt():
    b = []
    panels = [(1, "もとの分布（n = 1）"), (5, "5個の平均（n = 5）"), (30, "30個の平均（n = 30）")]
    for k, (n, title) in enumerate(panels):
        x0 = 40 + k * 262
        p = Plot(x0 + 20, 50, x0 + 240, 210, 0, 3, 0, 2.4)
        b.append(t(x0 + 130, 30, title, 13, "middle", TEXT, 700))
        b.append(f'<path d="M{p.x0} {p.y1} H{p.x1}" stroke="{AXIS}" stroke-width="1.5"/>')
        for v in (0, 1, 2, 3):
            b.append(f'<path d="M{p.X(v):.1f} {p.y1} v5" stroke="{AXIS}"/>' + t(p.X(v), p.y1 + 18, str(v), 11, "middle", MUTED))
        pts = smooth(lambda x: min(gamma_pdf(x, n, 1 / n), 2.4), 0.01, 3, 160)
        b.append(area(p, pts, S1, 0.18))
        b.append(p.line(pts, S1, 2.5))
        if n > 1:
            sd = 1 / math.sqrt(n)
            b.append(p.line(smooth(lambda x: min(phi((x - 1) / sd) / sd, 2.4), 0.01, 3, 160), S2, 2, "6 4"))
        b.append(f'<path d="M{p.X(1):.1f} {p.y0} V{p.y1}" stroke="{TEXT2}" stroke-width="1" stroke-dasharray="3 3"/>')
    b += legend(250, 262, [(S1, "平均の分布 / distribution of the mean"), (S2, "正規分布 / normal")])
    b.append(t(410, 290, "もとの分布は右にすそを引く（指数分布、平均 1）が、平均をとる個数が増えると正規分布に近づく", 12, "middle", TEXT2))
    return svg(820, 306, b)


def fig_ols():
    xs, ys = [1, 2, 3, 4, 5], [2, 4, 5, 4, 5]
    p = Plot(80, 40, 760, 260, 0, 6, 0, 6)
    b = p.grid([0, 1, 2, 3, 4, 5, 6], [(v, str(v)) for v in range(7)], "y", "x")
    b.append(p.line([(0, 2.2), (6, 2.2 + 0.6 * 6)], S1, 2.5))
    for x, y in zip(xs, ys):
        yh = 2.2 + 0.6 * x
        b.append(f'<path d="M{p.X(x):.1f} {p.Y(y):.1f} V{p.Y(yh):.1f}" stroke="{S2}" stroke-width="2" stroke-dasharray="4 3"/>')
    for x, y in zip(xs, ys):
        b.append(f'<circle cx="{p.X(x):.1f}" cy="{p.Y(y):.1f}" r="6" fill="{TEXT}" stroke="#ffffff" stroke-width="2"/>')
    b.append(f'<circle cx="{p.X(3):.1f}" cy="{p.Y(4):.1f}" r="7" fill="none" stroke="{S3}" stroke-width="2.5"/>')
    b.append(t(p.X(3) + 12, p.Y(4) + 22, "平均の点 (x̄, ȳ) = (3, 4) を通る", 11.5, "start", TEXT2))
    b.append(t(p.X(5.1), p.Y(5.6), "ŷ = 2.2 + 0.6x", 13, "start", TEXT, 700))
    b.append(t(p.X(2.08), p.Y(4.55), "残差 û", 12, "start", TEXT, 700))
    b += legend(420, 22, [(S1, "OLS の直線 / fitted line"), (S2, "残差 / residual")])
    return svg(820, 320, b)


# ---------------------------------------------------------------------------
# 機械学習
def fig_fit():
    import random
    rnd = random.Random(4)
    pts = [(x / 10, math.sin(x / 10 * 2.2) + rnd.gauss(0, 0.22)) for x in range(2, 30, 2)]
    b = []
    titles = [("適合不足 / underfitting", "直線では形をとらえられない"), ("ちょうどよい / good fit", "大まかな形をとらえる"), ("過学習 / overfitting", "点を全部通るが、新しいデータに弱い")]
    for k, (title, sub) in enumerate(titles):
        x0 = 30 + k * 265
        p = Plot(x0 + 10, 60, x0 + 245, 220, 0, 3, -1.8, 1.8)
        b.append(f'<rect x="{x0}" y="18" width="255" height="250" rx="8" fill="#ffffff" stroke="{GRID}" stroke-width="1.5"/>')
        b.append(t(x0 + 127, 40, title, 13, "middle", TEXT, 700))
        b.append(t(x0 + 127, 258, sub, 11.5, "middle", TEXT2))
        if k == 0:
            n = len(pts)
            mx, my = sum(a for a, _ in pts) / n, sum(c for _, c in pts) / n
            sl = sum((a - mx) * (c - my) for a, c in pts) / sum((a - mx) ** 2 for a, _ in pts)
            b.append(p.line([(0.1, my + sl * (0.1 - mx)), (2.9, my + sl * (2.9 - mx))], S1, 2.5))
        elif k == 1:
            b.append(p.line(smooth(lambda x: math.sin(x * 2.2), 0.1, 2.9), S1, 2.5))
        else:
            b.append(p.line(pts, S1, 2.5))
        for a, c in pts:
            b.append(f'<circle cx="{p.X(a):.1f}" cy="{p.Y(c):.1f}" r="4.5" fill="{TEXT}" stroke="#ffffff" stroke-width="1.5"/>')
    return svg(820, 282, b)


def fig_confusion():
    b = [t(410, 30, "混同行列（2クラス）/ confusion matrix", 14, "middle", TEXT, 700)]
    x0, y0, w, h = 250, 90, 190, 90
    b.append(t(x0 + w, y0 - 30, "予測 / predicted", 12.5, "middle", TEXT2, 700))
    b.append(t(x0 + w / 2, y0 - 10, "0（陰性）", 12.5, "middle", TEXT, 700) + t(x0 + w * 1.5, y0 - 10, "1（陽性）", 12.5, "middle", TEXT, 700))
    b.append(t(x0 - 120, y0 + h, "実際 / actual", 12.5, "middle", TEXT2, 700, extra=f' transform="rotate(-90 {x0 - 120} {y0 + h})"'))
    b.append(t(x0 - 12, y0 + h / 2 + 5, "0（陰性）", 12.5, "end", TEXT, 700) + t(x0 - 12, y0 + h * 1.5 + 5, "1（陽性）", 12.5, "end", TEXT, 700))
    cells = [("TN", "真陰性", "正しく 0", S3, 0, 0), ("FP", "偽陽性", "0 を 1 と誤る", S2, 1, 0),
             ("FN", "偽陰性", "1 を 0 と見逃す", S2, 0, 1), ("TP", "真陽性", "正しく 1", S3, 1, 1)]
    for code, ja, desc, col, cx, cy in cells:
        x, y = x0 + cx * w, y0 + cy * h
        b.append(f'<rect x="{x+2}" y="{y+2}" width="{w-4}" height="{h-4}" rx="8" fill="{col}" opacity="0.16"/>')
        b.append(f'<rect x="{x+2}" y="{y+2}" width="{w-4}" height="{h-4}" rx="8" fill="none" stroke="{col}" stroke-width="2"/>')
        b.append(t(x + w / 2, y + 36, f"{code}（{ja}）", 15, "middle", TEXT, 700))
        b.append(t(x + w / 2, y + 60, desc, 12, "middle", TEXT2))
    b.append(t(410, 300, "正解率 = (TP + TN) / 全体　適合率 = TP / (TP + FP)　再現率 = TP / (TP + FN)", 12.5, "middle", TEXT, 700))
    return svg(820, 320, b)


def fig_roc():
    p = Plot(100, 40, 420, 300, 0, 1, 0, 1)
    b = []
    curve = [(0, 0)] + [(f, min(1.0, 1 - (1 - f) ** 4.5)) for f in [i / 60 for i in range(1, 61)]]
    b.append(f'<path d="M{p.X(0)} {p.Y(0)} ' + " ".join(f"L{p.X(a):.1f} {p.Y(c):.1f}" for a, c in curve) + f' L{p.X(1)} {p.Y(0)} Z" fill="{S1}" opacity="0.15"/>')
    b += p.grid([0, 0.25, 0.5, 0.75, 1], [(v, f"{v:g}") for v in (0, 0.25, 0.5, 0.75, 1)], "真陽性率 TPR（再現率）", "偽陽性率 FPR", lambda v: f"{v:g}")
    b.append(p.line([(0, 0), (1, 1)], TEXT2, 1.5, "6 4"))
    b.append(p.line(curve, S1, 2.5))
    b.append(t(p.X(0.55), p.Y(0.35), "AUC = 塗った面積", 13, "middle", TEXT, 700))
    b.append(t(p.X(0.72), p.Y(0.62), "でたらめ（AUC = 0.5）", 11.5, "start", TEXT2, extra=f' transform="rotate(-39 {p.X(0.72):.1f} {p.Y(0.62):.1f})"'))
    lines = ["ROC 曲線: しきい値を 1 → 0 と動かしたときの", "（偽陽性率, 真陽性率）をつないだ線", "", "左上に近いほどよいモデル", "AUC は 0.5（でたらめ）〜 1（完ぺき）",
             "しきい値を決めなくても比べられる", "", "TPR = TP / (TP + FN)", "FPR = FP / (FP + TN)"]
    for i, s in enumerate(lines):
        b.append(t(470, 70 + i * 24, s, 13, "start", TEXT if i in (0, 1, 3, 4) else TEXT2, 700 if i in (3, 4) else None))
    return svg(820, 350, b)


def fig_kfold():
    b = [t(410, 28, "5分割の交差検証 / 5-fold cross-validation", 14, "middle", TEXT, 700)]
    x0, w, h = 150, 520, 30
    for k in range(5):
        y = 50 + k * (h + 10)
        b.append(t(x0 - 14, y + 20, f"{k+1}回目", 12.5, "end", TEXT, 700))
        for j in range(5):
            col = S2 if j == k else S1
            b.append(f'<rect x="{x0 + j*w/5 + 1:.1f}" y="{y}" width="{w/5 - 2:.1f}" height="{h}" rx="4" fill="{col}" opacity="{1 if j == k else 0.35}"/>')
        b.append(t(x0 + w + 14, y + 20, f"スコア {k+1}", 12, "start", TEXT2))
    y = 50 + 5 * (h + 10) + 14
    b.append(f'<rect x="{x0}" y="{y}" width="16" height="14" rx="3" fill="{S1}" opacity="0.35"/>' + t(x0 + 22, y + 12, "学習に使う / training", 12, "start", TEXT2))
    b.append(f'<rect x="{x0 + 240}" y="{y}" width="16" height="14" rx="3" fill="{S2}"/>' + t(x0 + 262, y + 12, "評価に使う / validation", 12, "start", TEXT2))
    b.append(t(410, y + 44, "5つのスコアの平均とばらつきで、モデルを評価する", 12.5, "middle", TEXT, 700))
    return svg(820, y + 60, b)


def box(x, y, w, h, label, color, sub=None, opacity=0.16, size=13):
    """色の付いた箱と、中の文字（sub は小さい2行目）"""
    b = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{color}" opacity="{opacity}"/>',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="none" stroke="{color}" stroke-width="1.3"/>']
    cy = y + h / 2 + (-3 if sub else 4.5)
    b.append(t(x + w / 2, cy, label, size, "middle", TEXT, 700))
    if sub:
        b.append(t(x + w / 2, cy + 17, sub, 11.5, "middle", TEXT2))
    return b


def arrow(x1, y1, x2, y2, label=None, lx=None, ly=None, anchor="middle"):
    b = [f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{TEXT2}" stroke-width="1.6" marker-end="url(#ah)"/>']
    if label:
        b.append(t(lx if lx is not None else (x1 + x2) / 2, ly if ly is not None else (y1 + y2) / 2 - 8, label, 12, anchor, TEXT, 700, ' font-family="ui-monospace, monospace"'))
    return b


AH = (f'<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
      f'<path d="M0 0 L10 5 L0 10 z" fill="{TEXT2}"/></marker></defs>')


def fig_docker_vm():
    b = [t(410, 28, "仮想マシンとコンテナ / Virtual machine vs container", 14, "middle", TEXT, 700)]
    def stack(x0, w, title, cols, layers, base):
        out = [t(x0 + w / 2, 60, title, 13.5, "middle", TEXT, 700)]
        y = 300
        for label, color in base:                       # 下から積む
            y -= 34
            out += box(x0, y, w, 30, label, color, size=12.5)
        gap = 8
        cw = (w - gap * (cols - 1)) / cols
        for c in range(cols):
            yy = y
            for label, color in layers:
                yy -= 34
                out += box(x0 + c * (cw + gap), yy, cw, 30, label, color, size=12)
        return out
    b += stack(40, 340, "仮想マシン / VM", 2,
               [("ゲスト OS", S2), ("ライブラリ", MUTED), ("アプリ", S1)],
               [("ハードウェア", MUTED), ("ホスト OS", MUTED), ("ハイパーバイザー", S2)])
    b += stack(440, 340, "コンテナ / Container", 3,
               [("ライブラリ", MUTED), ("アプリ", S1)],
               [("ハードウェア", MUTED), ("ホスト OS（Linux）", MUTED), ("Docker Engine", S3)])
    b.append(t(410, 330, "コンテナは OS を持たず、ホストの Linux を共有する。だから軽く、すぐ起動する", 12.5, "middle", TEXT, 700))
    return svg(820, 350, [AH] + b)


def fig_docker_flow():
    b = [t(410, 28, "Dockerfile からコンテナまで / From Dockerfile to container", 14, "middle", TEXT, 700)]
    b += box(30, 70, 170, 64, "Dockerfile", S2, "設計図（テキスト）")
    b += box(320, 70, 170, 64, "イメージ", S3, "ひな形（読むだけ）")
    for i in (2, 1):                                   # 奥の箱（右上にずらす）
        b += box(620 + i * 9, 70 - i * 9, 170, 64, "", S1, opacity=0.08)
    b.append('<rect x="620" y="70" width="170" height="64" rx="7" fill="#ffffff"/>')   # 奥の線を隠す
    b += box(620, 70, 170, 64, "コンテナ", S1, "動いている実体")
    b += arrow(204, 102, 314, 102, "docker build", 259, 92)
    b += arrow(494, 102, 614, 102, "docker run", 554, 92)
    b += box(320, 210, 170, 56, "Docker Hub", MUTED, "イメージの置き場")
    b += arrow(390, 206, 390, 140, "docker pull", 382, 178, "end")
    b += arrow(430, 140, 430, 206, "docker push", 438, 178, "start")
    b.append(t(705, 158, "1つのイメージから", 12, "middle", TEXT2))
    b.append(t(705, 175, "いくつでも作れる", 12, "middle", TEXT2))
    return svg(820, 290, [AH] + b)


FIGS = {STATS: {"normal.svg": fig_normal, "chi2.svg": fig_chi2, "t.svg": fig_t, "clt.svg": fig_clt, "ols.svg": fig_ols},
        ML: {"fit.svg": fig_fit, "confusion.svg": fig_confusion, "roc.svg": fig_roc, "kfold.svg": fig_kfold},
        DOCKER: {"vm.svg": fig_docker_vm, "flow.svg": fig_docker_flow}}

if __name__ == "__main__":
    n = 0
    for out, figs in FIGS.items():
        out.mkdir(parents=True, exist_ok=True)
        for name, fn in figs.items():
            (out / name).write_text(fn(), encoding="utf-8")
            n += 1
    print(f"{n} 枚の図を書き出しました")
