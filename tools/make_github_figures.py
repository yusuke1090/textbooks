#!/usr/bin/env python3
"""GitHub の教科書（books/github/）の、VS Code の画面の図（イメージ）を SVG で作る。

    python3 tools/make_github_figures.py      # books/github/images/vscode-*.svg に書き出す

画面は VS Code の暗いテーマに似せたイメージ。赤い丸の番号と、右（か下）の説明を対応させる。
色と書き方は、ピコのガイドの図（books/pico/images/vscode-new-project.svg）にそろえている。
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "books" / "github" / "images"
FONT = "system-ui, 'Noto Sans JP', sans-serif"
MONO = "ui-monospace, 'DejaVu Sans Mono', 'Noto Sans Mono', monospace"

TEXT, SUB = "#2b2f36", "#555c66"
RED, BLUE, PURPLE, AMBER, GREEN, GRAY = "#c0392b", "#2f6fde", "#6b3fa0", "#c28a00", "#1f7a3d", "#555c66"
LIGHT = {BLUE: "#e8f0fd", PURPLE: "#f1ebf8", AMBER: "#fff6e0", GREEN: "#e7f4ec", GRAY: "#f3f4f6"}
# 画面（暗いテーマ）
UI, UI_DARK, UI2, UI_LINE, UI_BORDER = "#1f2329", "#181b20", "#2b3038", "#3a404a", "#454c58"
UI_TEXT, UI_LABEL, UI_DIM, UI_BTN, UI_SEL = "#e3e7ee", "#c9ced6", "#8b93a1", "#2f6fde", "#2a4a72"
LETTER = {"M": "#e2c08d", "U": "#73c991", "D": "#f14c4c", "!": "#e4676b"}


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def width(s, size, mono=False):
    """文字の幅のだいたいの値（バッジやボタンの大きさを決めるため）。"""
    if mono:
        return len(s) * size * 0.6
    return sum(size if ord(c) > 0x2E80 else size * 0.58 for c in s)


class Fig:
    def __init__(self, w, h, title):
        self.w, self.h, self.p, self.markers = w, h, [], set()
        self.rect(0, 0, w, h, fill="#ffffff", rx=10)
        self.text(w / 2, 28, title, 16, "middle", TEXT, 700)

    def rect(self, x, y, w, h, fill="none", stroke=None, sw=1, rx=0, dash=None, opacity=None):
        a = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        a += f' stroke-dasharray="{dash}"' if dash else ""
        a += f' opacity="{opacity}"' if opacity else ""
        self.p.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"{a}/>')

    def text(self, x, y, s, size=12, anchor="start", fill=SUB, weight=None, mono=False, italic=False):
        a = f' font-weight="{weight}"' if weight else ""
        a += f' font-family="{MONO}"' if mono else ""
        a += ' font-style="italic"' if italic else ""
        self.p.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{fill}"{a}>{esc(s)}</text>')

    def line(self, x1, y1, x2, y2, stroke, sw=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.p.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def path(self, d, stroke, sw=2, fill="none", arrow=False, dash=None):
        m = ""
        if arrow:
            self.markers.add(stroke)
            m = f' marker-end="url(#ah-{stroke[1:]})"'
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        self.p.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dd}{m}/>')

    def circle(self, x, y, r, fill, stroke=None, sw=1):
        a = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}"{a}/>')

    def num(self, x, y, n):
        """赤い丸の番号。"""
        self.circle(x, y, 11, RED, "#ffffff", 1.5)
        self.text(x, y + 4, n, 12, "middle", "#ffffff", 700)

    def legend(self, x, y, items, wrap_gap=16, item_gap=12):
        """番号の説明を、上から並べる。items は (番号, [行, …])。"""
        for n, lines in items:
            self.num(x, y - 4, n)
            for i, s in enumerate(lines):
                self.text(x + 20, y + i * wrap_gap, s, 12, fill=TEXT)
            y += len(lines) * wrap_gap + item_gap
        return y

    def badge(self, x, y, s, color, outline=False, bold=False):
        """ブランチやタグの名前の札。x は左端、y は文字の下の線。幅を返す。"""
        w = width(s, 10.5) + 12
        if outline:
            self.rect(x, y - 12, w, 16, fill=UI, stroke=color, rx=3)
            self.text(x + 6, y, s, 10.5, fill=color, weight=700 if bold else None)
        else:
            self.rect(x, y - 12, w, 16, fill=color, rx=3)
            self.text(x + 6, y, s, 10.5, fill="#ffffff", weight=700 if bold else None)
        return w

    def branch_icon(self, x, y, color):
        """ブランチのアイコン（枝分かれ）。"""
        self.circle(x - 4, y - 6, 2, "none", color, 1.4)
        self.circle(x - 4, y + 6, 2, "none", color, 1.4)
        self.circle(x + 5, y - 3, 2, "none", color, 1.4)
        self.line(x - 4, y - 4, x - 4, y + 4, color, 1.4)
        self.path(f"M{x + 5} {y - 1} Q{x + 5} {y + 3} {x - 3} {y + 4}", color, 1.4)

    def window(self, x, y, w, h):
        self.rect(x, y, w, h, fill=UI, stroke=UI_LINE, sw=2, rx=8)

    def status_bar(self, x, y, w, branch="main*", sync="↻ 0↓ 1↑"):
        self.rect(x, y, w, 26, fill=UI_BTN)
        self.branch_icon(x + 14, y + 13, "#ffffff")
        self.text(x + 26, y + 17.5, branch, 12, fill="#ffffff")
        self.text(x + 26 + width(branch, 12) + 14, y + 17.5, sync, 12, fill="#ffffff")

    def note(self, s, y=None):
        self.text(self.w / 2, y or self.h - 14, s, 11, "middle", SUB)

    def save(self, name):
        defs = "".join(
            f'<marker id="ah-{c[1:]}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{c}"/></marker>' for c in sorted(self.markers))
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" font-family="{FONT}" font-size="13">\n'
               + (f"<defs>{defs}</defs>\n" if defs else "") + "\n".join(self.p) + "\n</svg>\n")
        (OUT / name).write_text(svg, encoding="utf-8")
        print("wrote", OUT / name)


def scm_view():
    f = Fig(820, 520, "ソース管理の画面（イメージ）")
    f.window(20, 50, 450, 420)
    # 左の縦のアイコンの列
    f.rect(21, 51, 41, 392, fill=UI_DARK, rx=7)
    f.rect(33, 72, 12, 15, stroke=UI_DIM, sw=1.4, rx=1)          # エクスプローラー
    f.rect(37, 68, 12, 15, fill=UI_DARK, stroke=UI_DIM, sw=1.4, rx=1)
    f.circle(39, 118, 6, "none", UI_DIM, 1.6)                    # 検索
    f.line(43.5, 122.5, 48, 127, UI_DIM, 1.8)
    f.rect(21, 148, 3, 26, fill="#ffffff")                        # ソース管理（選んでいる）
    f.branch_icon(41, 161, "#ffffff")
    f.circle(52, 171, 7, UI_BTN)
    f.text(52, 174.5, "3", 9.5, "middle", "#ffffff", 700)
    f.path("M35 196 L48 204 L35 212 Z", UI_DIM, 1.5)              # 実行とデバッグ
    for dx, dy in ((0, 0), (9, 0), (0, 9), (9, 9)):               # 拡張機能
        f.rect(33 + dx, 236 + dy, 7, 7, stroke=UI_DIM, sw=1.3)
    f.circle(41, 405, 5, "none", UI_DIM, 1.5)                     # アカウント
    f.path("M32 422 Q41 409 50 422", UI_DIM, 1.5)
    f.num(62, 146, "1")
    # パネル
    f.text(74, 72, "SOURCE CONTROL", 11, fill=UI_DIM, weight=700)
    f.text(404, 72, "✓", 13, "middle", UI_LABEL)
    f.text(424, 72, "↻", 13, "middle", UI_LABEL)
    f.text(446, 72, "⋯", 13, "middle", UI_LABEL)
    f.rect(72, 84, 380, 28, fill=UI2, stroke=UI_BORDER, rx=4)
    f.text(80, 102.5, "Message (Ctrl+Enter to commit on 'main')", 11.5, fill=UI_DIM)
    f.num(462, 98, "2")
    f.rect(72, 120, 380, 28, fill=UI_BTN, rx=4)
    f.text(250, 138.5, "✓ Commit", 12.5, "middle", "#ffffff", 600)
    f.line(424, 124, 424, 144, "#ffffff", 1)
    f.text(438, 138.5, "▾", 12, "middle", "#ffffff")
    f.num(462, 134, "3")

    def group(y, title, count):
        f.text(74, y, "⌄", 12, fill=UI_LABEL)
        f.text(88, y, title, 11.5, fill=UI_LABEL, weight=700)
        f.circle(436, y - 4, 8, UI_LINE)
        f.text(436, y - 0.5, count, 10, "middle", UI_TEXT)

    def file_row(y, name, letter, hover=False):
        if hover:
            f.rect(62, y - 15, 407, 22, fill=UI2)
            f.text(396, y, "↶", 14, "middle", UI_TEXT)
            f.text(416, y, "+", 15, "middle", UI_TEXT)
        f.text(92, y, name, 12, fill=UI_TEXT)
        f.text(452, y, letter, 12, "middle", LETTER[letter], 700)

    group(172, "Staged Changes", "1")
    file_row(195, "collar.cpp", "M")
    f.num(462, 168, "4")
    group(222, "Changes", "2")
    file_row(245, "CMakeLists.txt", "M", hover=True)
    file_row(269, "mpu6050.h", "U")
    f.num(372, 234, "5")
    f.num(430, 265, "6")
    # Graph
    group(302, "Graph", "")
    f.rect(426, 290, 20, 16, fill=UI)                              # 数の丸を消す
    for i, (msg, labels) in enumerate((
            ("I2C の読み取りを足した", [("main", BLUE, False)]),
            ("LED のピンを変えた", [("origin/main", PURPLE, True)]),
            ("最初のバージョン", []))):
        y = 328 + i * 26
        if i < 2:
            f.line(84, y, 84, y + 26, BLUE, 2)
        f.circle(84, y - 4, 4.5, UI, BLUE, 2)
        f.text(100, y, msg, 12, fill=UI_TEXT)
        x = 100 + width(msg, 12) + 10
        for s, c, outline in labels:
            x += f.badge(x, y, s, c, outline=outline) + 6
    f.num(462, 298, "7")
    f.status_bar(22, 443, 446)
    f.num(178, 456, "8")

    f.legend(500, 76, [
        ("1", ["ソース管理を開く（Ctrl + Shift + G）。", "数字は、変えたファイルの数"]),
        ("2", ["コミットの説明を書く欄"]),
        ("3", ["Commit。▾ で Commit & Push など"]),
        ("4", ["Staged Changes: 次のコミットに入る", "変更（git add したもの）"]),
        ("5", ["マウスを置くと出る。↶ は変更を捨てる、", "＋ はステージに入れる"]),
        ("6", ["M 変えた・U 新しい・D 消した・", "! コンフリクト"]),
        ("7", ["Graph: コミットの歴史。main（手元）と", "origin/main（GitHub）の位置が見える"]),
        ("8", ["今のブランチ（* はコミットしていない", "変更あり）と、取り込んでいない（↓）・", "送っていない（↑）コミットの数"]),
    ])
    f.note("表示や並びは、VS Code のバージョンや設定で少し違うことがある", 500)
    f.save("vscode-scm.svg")


def scm_button():
    f = Fig(820, 330, "ソース管理の大きいボタンの変わり方")
    cols = [
        (20, GRAY, ["リポジトリでない", "（git init の前）"], ["Initialize Repository", "Publish to GitHub"],
         ["リポジトリにする", "GitHub に置く（4章）"], ["git init"]),
        (222, AMBER, ["変えたファイルが", "ある"], ["✓ Commit"], ["記録する"], ["git add", "git commit"]),
        (424, GREEN, ["送っていない", "コミットがある"], ["↻ Sync Changes 1↑"], ["取り込んで、送る"], ["git pull", "git push"]),
        (626, PURPLE, ["ブランチがまだ", "GitHub にない"], ["Publish Branch"], ["ブランチを送る"], ["git push -u", "origin 名前"]),
    ]
    for x, c, title, buttons, does, cmds in cols:
        f.rect(x, 50, 174, 216, fill=LIGHT[c], stroke=c, sw=2, rx=8)
        for i, s in enumerate(title):
            f.text(x + 87, 74 + i * 18, s, 13.5, "middle", c, 700)
        by = 112 if len(buttons) == 1 else 104
        for i, s in enumerate(buttons):
            f.rect(x + 12, by + i * 34, 150, 26, fill=UI_BTN, rx=4)
            f.text(x + 87, by + i * 34 + 17.5, s, 11.5, "middle", "#ffffff", 600)
        y = 186
        for s in does:
            f.text(x + 87, y, s, 12, "middle", TEXT)
            y += 17
        for s in cmds:
            f.text(x + 87, y + 4, s, 11.5, "middle", SUB, mono=True)
            y += 16
    f.path("M194 158 L218 158", BLUE, 2, arrow=True)
    f.path("M396 158 L420 158", BLUE, 2, arrow=True)
    f.path("M511 266 C511 300 309 300 309 270", GREEN, 2, arrow=True, dash="5 4")
    f.text(410, 306, "また書き換えると Commit に戻る", 12, "middle", GREEN)
    f.line(612, 56, 612, 260, GRAY, 1.5, dash="4 4")
    f.text(713, 290, "新しいブランチを作ったとき", 12, "middle", PURPLE)
    f.save("vscode-scm-button.svg")


def diff_view():
    f = Fig(820, 500, "変更の見え方（イメージ）")
    f.text(20, 58, "A. ソース管理でファイルを押したとき（前と今が左右に並ぶ）", 13, fill=TEXT, weight=700)
    f.window(20, 68, 780, 182)
    f.rect(21, 69, 230, 28, fill=UI2, rx=7)
    f.text(34, 88, "collar.cpp (Working Tree)", 12, fill=UI_TEXT)
    f.line(410, 97, 410, 248, UI_LINE, 1.5)
    f.line(21, 97, 799, 97, UI_LINE, 1)
    left = [("9", '#include "pico/stdlib.h"', None, None),
            ("10", "const int SAMPLE_HZ = 50;", "#4b1d1d", "50"),
            (None, "", "filler", None),
            ("11", "", None, None),
            ("12", "void setup() {", None, None)]
    right = [("9", '#include "pico/stdlib.h"', None, None),
             ("10", "const int SAMPLE_HZ = 100;", "#1e3d23", "100"),
             ("11", "const int LED_PIN = 25;", "#1e3d23", None),
             ("12", "", None, None),
             ("13", "void setup() {", None, None)]
    for x0, rows, strong in ((21, left, "#7a2a2a"), (411, right, "#2d6a35")):
        for i, (n, code, bg, hi) in enumerate(rows):
            y = 104 + i * 26
            if bg == "filler":
                f.rect(x0, y, 388, 24, fill="#262a30")
                for k in range(0, 388, 12):
                    f.line(x0 + k, y + 24, x0 + k + 12, y, "#323844", 1)
                continue
            if bg:
                f.rect(x0, y, 388, 24, fill=bg)
            if hi:
                pre = code.index(hi)
                f.rect(x0 + 44 + pre * 7.2, y + 3, len(hi) * 7.2 + 2, 18, fill=strong)
            if n:
                f.text(x0 + 30, y + 17, n, 12, "end", UI_DIM, mono=True)
            f.text(x0 + 44, y + 17, code, 12, fill=UI_TEXT, mono=True)
    f.num(392, 112, "1")
    f.num(782, 112, "2")
    f.num(362, 142, "3")
    f.num(752, 155, "4")
    y = 274
    x = 20
    for n, s in (("1", "左: 最後のコミット（前）"), ("2", "右: 今のファイル（後）"),
                 ("3", "赤: 消した・変える前"), ("4", "緑: 足した・変えた後")):
        f.num(x + 11, y - 4, n)
        f.text(x + 28, y, s, 12, fill=TEXT)
        x += 195

    f.text(20, 318, "B. ふだんの画面（行番号の横の色）", 13, fill=TEXT, weight=700)
    f.window(20, 328, 420, 152)
    rows = [("8", "// 首輪のプログラム", None), ("9", '#include "pico/stdlib.h"', None),
            ("10", "const int SAMPLE_HZ = 100;", "blue"), ("11", "const int LED_PIN = 25;", "green"),
            ("12", "", "deleted"), ("13", "void setup() {", None)]
    for i, (n, code, mark) in enumerate(rows):
        y = 350 + i * 21
        f.text(54, y, n, 12, "end", UI_DIM, mono=True)
        f.text(76, y, code, 12, fill=UI_TEXT, mono=True)
        if mark == "blue":
            f.rect(62, y - 15, 4, 21, fill="#1b81a8")
        elif mark == "green":
            f.rect(62, y - 15, 4, 21, fill="#487e02")
        elif mark == "deleted":
            f.path(f"M61 {y + 2} L69 {y + 6} L61 {y + 10} Z", "#f14c4c", 1, fill="#f14c4c")
    # 説明
    lx = 470
    f.rect(lx, 352, 5, 20, fill="#487e02")
    f.text(lx + 18, 367, "緑の線: 足した行", 12, fill=TEXT)
    f.rect(lx, 384, 5, 20, fill="#1b81a8")
    f.text(lx + 18, 399, "青の線: 変えた行", 12, fill=TEXT)
    f.path(f"M{lx} 418 L{lx + 9} 423 L{lx} 428 Z", "#f14c4c", 1, fill="#f14c4c")
    f.text(lx + 18, 428, "赤い三角: ここにあった行を消した", 12, fill=TEXT)
    f.text(lx, 456, "色の所を押すと、その場で前との違いが出る", 12, fill=SUB)
    f.text(lx, 474, "（↶ で、その所だけ元に戻せる）", 12, fill=SUB)
    f.save("vscode-diff.svg")


def branch_menu():
    f = Fig(820, 430, "ブランチの切り替えと作成（イメージ）")
    f.window(20, 50, 500, 344)
    f.rect(56, 62, 428, 236, fill="#252a31", stroke=UI_BORDER, rx=6)
    f.rect(66, 72, 408, 26, fill=UI2, stroke=UI_BTN, rx=3)
    f.text(74, 89.5, "Select a branch or tag to checkout", 11.5, fill=UI_DIM)
    items = [
        (118, "+ Create new branch...", "", True),
        (142, "+ Create new branch from...", "", False),
        (166, "Checkout detached...", "", False),
        (208, "main", "3d3b5db・I2C の読み取りを足した", False),
        (232, "try-sleep", "9f8e7d6・スリープを試す", False),
        (274, "origin/main", "a1c2e3f・LED のピンを変えた", False),
    ]
    for y, s, sub, sel in items:
        if sel:
            f.rect(60, y - 16, 420, 23, fill=UI_SEL)
        f.text(78, y, s, 12, fill=UI_TEXT)
        if sub:
            f.text(78 + width(s, 12) + 12, y, sub, 11, fill=UI_DIM)
    for y, s in ((184, "branches"), (250, "remote branches")):
        f.line(60, y - 4, 480, y - 4, UI_LINE, 1)
        f.text(474, y + 8, s, 10.5, "end", UI_DIM)
    f.status_bar(22, 367, 496)
    f.num(178, 380, "1")
    f.num(470, 114, "2")
    f.num(470, 220, "3")
    f.num(470, 286, "4")
    f.legend(550, 92, [
        ("1", ["左下のブランチ名を押すと、", "上に一覧が出る"]),
        ("2", ["新しいブランチを作って移る", "（git switch -c）。名前を打って Enter"]),
        ("3", ["手元のブランチ。押すと、そこに移る", "（git switch）"]),
        ("4", ["GitHub にあるブランチ。押すと、", "手元にも同じ名前で作って移る"]),
    ], item_gap=18)
    f.note("表示や並びは、VS Code のバージョンで少し違うことがある", 418)
    f.save("vscode-branch.svg")


def conflict():
    f = Fig(820, 400, "コンフリクトの画面（イメージ）")
    f.window(20, 50, 540, 312)
    f.rect(21, 51, 140, 28, fill=UI2, rx=7)
    f.text(34, 70, "collar.cpp", 12, fill=UI_TEXT)
    f.line(21, 79, 559, 79, UI_LINE, 1)
    rows = [
        ("9", '#include "pico/stdlib.h"', None),
        (None, "lens", None),
        ("10", "<<<<<<< HEAD (Current Change)", "#2a5a45"),
        ("11", "const int SAMPLE_HZ = 50;", "#1b3a2e"),
        ("12", "=======", None),
        ("13", "const int SAMPLE_HZ = 100;", "#18324f"),
        ("14", ">>>>>>> 9f8e7d6 (Incoming Change)", "#25507c"),
        ("15", "", None),
        ("16", "void setup() {", None),
    ]
    for i, (n, code, bg) in enumerate(rows):
        y = 88 + i * 24
        if code == "lens":
            f.text(70, y + 15, "Accept Current Change | Accept Incoming Change | Accept Both Changes | Compare Changes",
                   9.6, fill=UI_DIM)
            continue
        if bg:
            f.rect(21, y, 538, 23, fill=bg)
        f.text(52, y + 16, n, 12, "end", UI_DIM, mono=True)
        f.text(70, y + 16, code, 12, fill=UI_TEXT, mono=True)
    f.rect(388, 322, 160, 28, fill=UI_BTN, rx=4)
    f.text(468, 340.5, "Resolve in Merge Editor", 11.5, "middle", "#ffffff", 600)
    f.num(36, 123, "1")
    f.num(540, 159, "2")
    f.num(540, 231, "3")
    f.num(380, 336, "4")
    f.legend(590, 82, [
        ("1", ["押すと、残すほうが決まり、", "印の行（<<<<<<< など）も消える"]),
        ("2", ["手元の変更（Current）"]),
        ("3", ["取り込もうとした側（Incoming）"]),
        ("4", ["3つの画面（手元・取り込む側・", "結果）で見比べて直す"]),
    ], item_gap=18)
    f.text(590, 262, "Accept Current Change: 手元を残す", 11.5, fill=SUB)
    f.text(590, 280, "Accept Incoming Change: 取り込む側", 11.5, fill=SUB)
    f.text(590, 298, "Accept Both Changes: 両方を残す", 11.5, fill=SUB)
    f.text(590, 316, "Compare Changes: 左右に並べて見る", 11.5, fill=SUB)
    f.note("表示や並びは、VS Code のバージョンで少し違うことがある", 388)
    f.save("vscode-conflict.svg")


def git_graph():
    f = Fig(820, 430, "拡張機能 Git Graph の画面（イメージ）")
    f.window(20, 50, 780, 270)
    cols = ((34, "Graph"), (130, "Description"), (520, "Date"), (622, "Author"), (712, "Commit"))
    for x, s in cols:
        f.text(x, 72, s, 11.5, fill=UI_LABEL, weight=700)
    f.line(21, 82, 799, 82, UI_LINE, 1)
    L1, L2 = 52, 76
    rows = [
        ("Uncommitted Changes (2)", [], "*", "*", "*", L1, GRAY),
        ("スリープを試す", [("try-sleep", PURPLE, False, False)], "11/14 10:20", "Taro", "9f8e7d6", L2, PURPLE),
        ("I2C の読み取りを足した", [("main", BLUE, False, True)], "11/14 09:05", "Taro", "3d3b5db", L1, BLUE),
        ("LED のピンを変えた", [("origin/main", BLUE, True, False), ("v1.0.0", AMBER, False, False)],
         "11/13 17:40", "Taro", "a1c2e3f", L1, BLUE),
        ("最初のバージョン", [], "11/13 15:12", "Taro", "5b6d7e8", L1, BLUE),
    ]
    ys = [104 + i * 30 for i in range(len(rows))]
    # 線（先に描いて、点を上に重ねる）
    f.line(L1, ys[0] - 4, L1, ys[2] - 4, "#8b93a1", 2, dash="3 3")
    f.line(L1, ys[2] - 4, L1, ys[4] - 4, BLUE, 2)
    f.path(f"M{L2} {ys[1] - 4} L{L2} {ys[1] + 10} Q{L2} {ys[2] - 4} {L1} {ys[2] - 4}", PURPLE, 2)
    for y, (msg, labels, date, author, sha, lane, color) in zip(ys, rows):
        if msg.startswith("Uncommitted"):
            f.circle(lane, y - 4, 4.5, UI, "#8b93a1", 2)
            f.text(130, y, msg, 12, fill=UI_DIM, italic=True)
        else:
            f.circle(lane, y - 4, 4.5, color if lane == L2 else UI, color, 2)
            x = 130
            for s, c, outline, bold in labels:
                x += f.badge(x, y, s, c, outline=outline, bold=bold) + 6
            f.text(x + 4, y, msg, 12, fill=UI_TEXT)
        f.text(520, y, date, 11.5, fill=UI_LABEL)
        f.text(622, y, author, 11.5, fill=UI_LABEL)
        f.text(712, y, sha, 11.5, fill=UI_LABEL, mono=True)
    # 右クリックのメニュー
    f.rect(300, 200, 250, 112, fill="#252a31", stroke=UI_BORDER, rx=5)
    for i, s in enumerate(("Add Tag...", "Create Branch...", "Checkout...", "Revert...", "Copy Commit Hash to Clipboard")):
        if i == 3:
            f.rect(303, 260, 244, 20, fill=UI_SEL)
        f.text(314, 218 + i * 20, s, 11.5, fill=UI_TEXT)
    f.num(98, 130, "1")
    f.num(118, 190, "2")
    f.num(340, 100, "3")
    f.num(288, 214, "4")
    rows = [
        (40, 350, "1", ["点がコミット、線がブランチ。", "枝分かれと合流が見える"]),
        (420, 350, "2", ["ブランチ（太字は今いるもの）・", "GitHub の位置（origin/main）・タグ"]),
        (40, 396, "3", ["まだコミットしていない変更"]),
        (420, 396, "4", ["コミットを右クリック: タグ・ブランチを", "作る、そこに移る、取り消す（Revert）"]),
    ]
    for x, y, n, lines in rows:
        f.legend(x, y, [(n, lines)])
    f.save("vscode-git-graph.svg")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    scm_view()
    scm_button()
    diff_view()
    branch_menu()
    conflict()
    git_graph()
