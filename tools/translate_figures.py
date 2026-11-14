#!/usr/bin/env python3
"""図（SVG）の日本語を英語に置き換えて、英語の版を images/en/ に作る。

    python3 tools/translate_figures.py <本の id>          # 例: stats
    python3 tools/translate_figures.py <本の id> --init   # 訳のない文字を figures-en.json に "" で足す

- books/<id>/figures-en.json に {"日本語の文字": "English", ...} を並べる。
  キーは図の中の文字（<text> などのタグの間の文字。前後の空白は除く）。
  英語がもう横に書いてある図で、日本語の行を消したいときは "-" にする。
- images/ の SVG で日本語があるものを、images/en/ に同じ名前で書き出す（日本語がない図は作らない）。
  英語の章（en/*.md）からは images/en/<名前>.svg を使う。
- 図を作り直したら（make_*_figures.py）、これも動かし直す。
- 訳がない文字があると、一覧を出して止まる。
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JA = re.compile(r"[　-ヿ㐀-鿿＀-￯]")
SEG = re.compile(r">([^<>]+)<")


def segments(svg):
    for m in SEG.finditer(svg):
        s = html.unescape(m.group(1)).strip()
        if JA.search(s):
            yield s


def main():
    book = ROOT / "books" / sys.argv[1]
    table_path = book / "figures-en.json"
    table = json.loads(table_path.read_text()) if table_path.exists() else {}
    svgs = sorted(p for p in (book / "images").glob("*.svg") if JA.search(p.read_text(encoding="utf-8")))
    missing = []
    for p in svgs:
        for s in segments(p.read_text(encoding="utf-8")):
            if not table.get(s) and s not in missing:
                missing.append(s)
    if "--init" in sys.argv:
        for s in missing:
            table.setdefault(s, "")
        table_path.write_text(json.dumps(table, indent=1, ensure_ascii=False) + "\n")
        print(f"{len(missing)} 個の文字を {table_path.relative_to(ROOT)} に足しました（英語を書いてください）")
        return
    if missing:
        print("訳がない文字:")
        for s in missing:
            print("  " + s)
        sys.exit(1)

    def repl(m):
        raw = m.group(1)
        s = html.unescape(raw).strip()
        if not JA.search(s):
            return m.group(0)
        lead, trail = raw[: len(raw) - len(raw.lstrip())], raw[len(raw.rstrip()):]
        en = "" if table[s] == "-" else table[s]
        return ">" + lead + html.escape(en, quote=False) + trail + "<"

    out = book / "images" / "en"
    out.mkdir(exist_ok=True)
    for p in svgs:
        svg = SEG.sub(repl, p.read_text(encoding="utf-8"))
        svg = svg.replace("'Noto Sans JP', 'Hiragino Sans', ", "")
        (out / p.name).write_text(svg, encoding="utf-8")
    unused = [k for k in table if k not in {s for p in svgs for s in segments(p.read_text(encoding="utf-8"))}]
    print(f"{len(svgs)} 枚の英語の図を {out.relative_to(ROOT)} に書き出しました")
    if unused:
        print(f"使っていない訳: {len(unused)} 個（{', '.join(unused[:5])}{' …' if len(unused) > 5 else ''}）")


if __name__ == "__main__":
    main()
