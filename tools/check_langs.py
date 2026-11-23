#!/usr/bin/env python3
"""2つの言葉の教科書で、日本語（ja/）と英語（en/）がそろっているかを確かめる。

    python3 tools/check_langs.py            # 2つの言葉の本を全部
    python3 tools/check_langs.py stats ml   # 本を選んで

確かめること:
- chapters.json の章が ja/ と en/ の両方にあり、題名と部に ja と en がある
- 見出し（##・###・####）の数と深さの並びが同じ（言葉を切り替えたとき、見出しの番号で場所を合わせるため）
- 練習問題（```quiz）の問題の数が同じ
- 図・写真の数と順番が同じ（図の番号がずれないように）。英語の章の図は、日本語の入った SVG なら images/en/ を使う。動画は、同じ場所にあれば、日本語と英語でちがう動画でよい
- 使っている画像のファイルがある
- 英語の章に日本語が残りすぎていない（多い行を出す。用語集などで日本語を見せる行はそのままでよい）
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JA = re.compile(r"[぀-ヿ㐀-鿿]")
IMG = re.compile(r"^\s*!\[[^\]]*\]\(([^)\s]+)\)\s*$")


def strip_code(text):
    out, fence = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
            out.append("")
            continue
        out.append("" if fence else line)
    return out


def shape(text):
    heads, imgs = [], []
    for line in strip_code(text):
        m = re.match(r"^(#{2,4})\s", line)
        if m:
            heads.append(len(m.group(1)))
        m = IMG.match(line)
        if m:
            imgs.append(m.group(1))
    return heads, imgs


def quiz(text):
    """練習問題（```quiz）の Q: と E: の行"""
    out, inq = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            inq = (not inq) and line.strip() == "```quiz"
            continue
        if inq and re.match(r"^[QE]:", line):
            out.append(line)
    return out


def norm(src):
    """くらべるための形。動画（YouTube・mp4・webm）は、言葉ごとにちがう動画でよいので「動画」にまとめる"""
    if re.search(r"youtube\.com/|youtu\.be/|\.(mp4|webm)$", src):
        return "動画"
    return re.sub(r"^images/en/", "images/", src)


def check(bid):
    book = ROOT / "books" / bid
    errs, warns = [], []
    chapters = json.loads((book / "chapters.json").read_text())
    for ch in chapters:
        f = ch["file"]
        for k in ("title", "part"):
            if not (isinstance(ch.get(k), dict) and ch[k].get("ja") and ch[k].get("en")):
                errs.append(f"{f}: chapters.json の {k} に ja と en がない")
        paths = {lang: book / lang / f for lang in ("ja", "en")}
        if not all(p.exists() for p in paths.values()):
            errs.append(f"{f}: " + "、".join(f"{l}/ にない" for l, p in paths.items() if not p.exists()))
            continue
        (hj, ij), (he, ie) = shape(paths["ja"].read_text()), shape(paths["en"].read_text())
        if hj != he:
            errs.append(f"{f}: 見出しがちがう（ja {len(hj)} 個 {''.join(map(str, hj))} / en {len(he)} 個 {''.join(map(str, he))}）")
        qj, qe = (sum(l.startswith("Q:") for l in quiz(paths[k].read_text())) for k in ("ja", "en"))
        if qj != qe:
            errs.append(f"{f}: 練習問題の数がちがう（ja {qj} / en {qe}）")
        if [norm(s) for s in ij] != [norm(s) for s in ie]:
            errs.append(f"{f}: 図の並びがちがう（ja {ij} / en {ie}）")
        for src in ie:
            if src.startswith("http"):
                continue
            p = book / src
            if not p.exists():
                errs.append(f"en/{f}: 画像がない {src}")
            elif src.endswith(".svg") and not src.startswith("images/en/") and (book / "images" / "en" / p.name).exists():
                errs.append(f"en/{f}: 英語の図があるのに {src} を使っている")
        for src in ij:
            if not src.startswith("http") and not (book / src).exists():
                errs.append(f"ja/{f}: 画像がない {src}")
        lines = strip_code(paths["en"].read_text())
        many = [i + 1 for i, l in enumerate(lines) if len(JA.findall(l)) > 12]
        many += [l[:30] for l in quiz(paths["en"].read_text()) if len(JA.findall(l)) > 12]
        if many and not f.startswith(("a-", "b-", "c-", "d-", "e-", "f-")):
            warns.append(f"en/{f}: 日本語の多い行 {many[:8]}")
    return errs, warns


def main():
    books = json.loads((ROOT / "books.json").read_text())
    ids = sys.argv[1:] or [b["id"] for b in books if len(b["langs"]) > 1]
    bad = 0
    for bid in ids:
        errs, warns = check(bid)
        print(f"{bid}: {'OK' if not errs else str(len(errs)) + ' 個の問題'}")
        for e in errs:
            print("  ✗ " + e)
        for w in warns:
            print("  △ " + w)
        bad += len(errs)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
