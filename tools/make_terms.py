#!/usr/bin/env python3
"""教科書の用語集（付録の表）から、本文の言葉を押したときに出す説明の一覧（terms.json）を作る。

    python3 tools/make_terms.py cow      # books/cow/ja/a-words.md と en/a-words.md → books/cow/terms.json

日本語の表は「日本語 | 読み | 英語 | 意味」、英語の表は「English | Japanese | Reading | Meaning」の形。
日本語の言葉でつなぎ合わせて、1つの言葉に日本語・読み・英語・意味（日本語と英語）をまとめる。
本文では、章ごとに最初に出てきた所だけに点線を付ける（読む画面 index.html が行う）。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# 本文によく出る、ほかの意味でも使う言葉には付けない（付けると、ちがう意味の所にも説明が出てしまう）
SKIP_EN = {"cow", "feed", "milking", "grains", "grass / forage crop", "dry cow", "fiber (ndf)",
           "as", "switch"}   # network: AS は英語の as、switch は「切り替える」にも当たる
SKIP_JA = {"飼料", "搾乳", "牧草", "繊維"}


def rows(md):
    """表の行（見出しと区切りの行を除く）を、マスの並びで返す"""
    out = []
    for line in md.splitlines():
        if not line.startswith("|") or re.match(r"^\|\s*-", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells[0] in ("日本語", "English"):
            continue
        out.append(cells)
    return out


def variants(cell, lang):
    """「未経産牛（育成牛）」→ [未経産牛, 育成牛]、「dairy cow / dairy cattle」→ [dairy cow, dairy cattle]"""
    cell = cell.replace("**", "")
    parts = re.split(r"\s*/\s*", re.sub(r"[（(][^）)]*[）)]", "", cell)) if lang == "en" else [re.sub(r"（.*?）", "", cell)]
    if lang == "ja":
        parts += re.findall(r"（([^）]+)）", cell)
    out = []
    for p in parts:
        p = p.strip()
        if len(p) >= 2 and not re.match(r"^[\d.]", p):
            out.append(p)
    return out


def main(book):
    d = ROOT / "books" / book
    ja = rows((d / "ja" / "a-words.md").read_text(encoding="utf-8"))
    en = rows((d / "en" / "a-words.md").read_text(encoding="utf-8"))
    en_by_ja = {r[1]: r for r in en}
    terms = []
    for jp, yomi, eng, mean in ja:
        e = en_by_ja.get(jp)
        terms.append({
            "ja": jp, "yomi": yomi, "en": eng, "mean_ja": mean, "mean_en": e[3] if e else "",
            "match_ja": [v for v in variants(jp, "ja") if v not in SKIP_JA],
            "match_en": [v for v in variants(eng, "en") if eng.lower() not in SKIP_EN and v.lower() not in SKIP_EN],
        })
    out = d / "terms.json"
    out.write_text(json.dumps(terms, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(terms)} 語を {out} に書き出しました")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "cow")
