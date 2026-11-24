#!/usr/bin/env python3
"""教科書の動画（mp4）を作る道具。図と同じように SVG で1コマずつ描き、Chrome で写して、ffmpeg で mp4 にする。

使う前に（1回だけ）:
    python3 -m venv .venv && .venv/bin/pip install playwright imageio-ffmpeg
    （Chrome はパソコンに入っているものを使う）

動画を作る:
    .venv/bin/python tools/make_<本>_videos.py [名前 …]

- 日本語の動画は books/<本>/videos/<名前>.mp4、英語は books/<本>/videos/en/<名前>.mp4
- 英語の字は、図と同じ books/<本>/figures-en.json の訳を使う。訳がない字があると、一覧を出して止まる
- 章には図と同じ1行で入れる: ![動画: 説明](videos/<名前>.mp4)（英語の章は videos/en/<名前>.mp4）
- H.264 の mp4 なので、iPhone の Safari でも再生できる
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
W, H = 800, 450                  # 描くときの大きさ（16:9）
PX_W, PX_H = 1280, 720           # 動画の大きさ
FPS = 24
FONT = "system-ui, 'Noto Sans JP', sans-serif"
INK, SUB = "#2b2f36", "#555c66"
CAP_H = 48                       # 下の字幕の帯の高さ
JA = re.compile(r"[　-ヿ㐀-鿿＀-￯]")
SEG = re.compile(r">([^<>]+)<")


def clamp(x):
    return max(0.0, min(1.0, x))


def ease(p):
    p = clamp(p)
    return p * p * (3 - 2 * p)


def text(x, y, s, size=13, anchor="start", weight=400, fill=INK):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" '
            f'font-weight="{weight}" fill="{fill}">{s}</text>')


def group(body, dx=0.0, dy=0.0, opacity=1.0, extra=""):
    """まとめて動かす・薄くする"""
    if opacity <= 0.001:
        return []
    attrs = f' transform="translate({dx:.1f} {dy:.1f}){extra}"' if (dx or dy or extra) else ""
    if opacity < 0.999:
        attrs += f' opacity="{opacity:.3f}"'
    return [f"<g{attrs}>", *body, "</g>"]


def draw_path(d, color, p, width=3):
    """線を、はしから p（0〜1）まで描く"""
    if p <= 0:
        return []
    return [f'<path d="{d}" pathLength="1" stroke-dasharray="1" stroke-dashoffset="{1 - clamp(p):.3f}" '
            f'stroke="{color}" stroke-width="{width}" fill="none" stroke-linecap="round"/>']


class Steps:
    """手順の並び。steps = [(字幕, 秒), …]。手順 i は starts[i] 秒に始まる"""

    def __init__(self, steps, lead=0.4):
        self.steps, self.starts, self.lead = steps, [], lead
        s = 0.0
        for _, d in steps:
            self.starts.append(s)
            s += d
        self.duration = s + 1.5          # 最後に少し止める

    def index(self, t):
        i = 0
        for k, s in enumerate(self.starts):
            if t >= s:
                i = k
        return i

    def p(self, t, i, move=1.0, delay=0.0):
        """手順 i の動きの進み（0〜1）。手順が始まって lead＋delay 秒後から move 秒で動く"""
        return ease((t - self.starts[i] - self.lead - delay) / move)

    def local(self, t, i):
        """手順 i が始まってからの秒"""
        return t - self.starts[i]

    def caption(self, t):
        return self.steps[self.index(t)][0]


def frame(body, caption=None):
    """1コマ。caption は下の帯に出す字幕"""
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{PX_W}" height="{PX_H}" '
           f'font-family="{FONT}" font-size="13">', f'<rect width="{W}" height="{H}" fill="#ffffff"/>', *body]
    if caption:
        out += [f'<rect x="0" y="{H - CAP_H}" width="{W}" height="{CAP_H}" fill="{INK}"/>',
                text(W / 2, H - CAP_H / 2 + 6.5, caption, 18, "middle", 700, "#ffffff").replace("<text ", '<text data-cap="1" ', 1)]
    out.append("</svg>")
    return "\n".join(out)


CAP = re.compile(r'(<text data-cap="1" [^>]*font-size=")18("[^>]*>)([^<]*)(</text>)')


def fit_caption(svg):
    """字幕が横にはみ出すときは、字を小さくする"""
    def repl(m):
        s = html.unescape(m.group(3))
        width = sum(18 if ord(ch) > 0x2000 else 9.8 for ch in s)
        size = 18 if width <= W - 40 else max(12, 18 * (W - 40) / width)
        return f"{m.group(1)}{size:.1f}{m.group(2)}{m.group(3)}{m.group(4)}"
    return CAP.sub(repl, svg)


def translate(svg, table, missing):
    def repl(m):
        raw = m.group(1)
        s = html.unescape(raw).strip()
        if not JA.search(s):
            return m.group(0)
        if not table.get(s):
            missing.add(s)
            return m.group(0)
        lead, trail = raw[: len(raw) - len(raw.lstrip())], raw[len(raw.rstrip()):]
        en = "" if table[s] == "-" else table[s]
        return ">" + lead + html.escape(en, quote=False) + trail + "<"
    return SEG.sub(repl, svg)


def render(book, name, make_frame, duration, langs=("ja", "en")):
    """make_frame(t) が返す SVG を、duration 秒ぶん動画にする"""
    import imageio_ffmpeg
    from playwright.sync_api import sync_playwright

    bdir = ROOT / "books" / book
    table_path = bdir / "figures-en.json"
    table = json.loads(table_path.read_text()) if table_path.exists() else {}
    n = int(duration * FPS)
    ja_frames = [make_frame(i / FPS) for i in range(n)]
    for lang in langs:
        frames = ja_frames
        if lang == "en":
            missing = set()
            frames = [translate(f, table, missing) for f in ja_frames]
            if missing:
                print(f"{name}: 訳がない字（{table_path.relative_to(ROOT)} に足す）:")
                for s in sorted(missing):
                    print("  " + s)
                sys.exit(1)
        frames = [fit_caption(f) for f in frames]
        out = bdir / "videos" / ("en" if lang == "en" else "") / f"{name}.mp4"
        out.parent.mkdir(parents=True, exist_ok=True)
        ff = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "image2pipe",
                               "-framerate", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                               "-crf", "27", "-preset", "slow", "-tune", "animation", "-movflags", "+faststart",
                               str(out)], stdin=subprocess.PIPE)
        with sync_playwright() as pw:
            browser = pw.chromium.launch(channel="chrome")
            page = browser.new_page(viewport={"width": PX_W, "height": PX_H})
            last, png = None, None
            for f in frames:
                if f != last:                       # 同じコマは写し直さない
                    page.set_content(f"<html><body style='margin:0;overflow:hidden'>{f}</body></html>")
                    png, last = page.screenshot(type="png"), f
                ff.stdin.write(png)
            browser.close()
        ff.stdin.close()
        ff.wait()
        print(f"{out.relative_to(ROOT)}（{duration:.0f}秒・{out.stat().st_size // 1024} KB）")
