#!/usr/bin/env python3
"""コードの言葉の説明（books/<id>/glossary.json）を、tools/glossary/ の辞書から作る。

    python3 tools/make_glossaries.py

- tools/glossary/*.json は、言語・ライブラリごとの辞書（python・numpy・cpp・shell・ros など）
- 本ごとに、使う辞書を BOOKS に並べる（先に書いた辞書が優先）。その本のコードに出てくる言葉だけを入れる
- pico・github の glossary.json は手で書いたものなので、上書きせず、足りない言葉だけを足す（FILL）
- キーの書き方は glossary.json の "_説明"（「単語」「関数名.引数名」「$ コマンド サブコマンド」「#include <名前>」）
- 英語でも読める本（books.json の langs に "en"）には、tools/glossary/en/ の英語の辞書から glossary-en.json も作る
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "glossary"
BOOKS = {
    "python": ["numpy", "pandas", "matplotlib", "shell", "python"],
    "ml": ["sklearn", "numpy", "pandas", "matplotlib", "python"],
    "stats": ["stats", "numpy", "pandas", "python"],
    "linalg": ["numpy", "python"],
    "ros": ["ros", "docker", "shell", "python"],
    "cpp": ["cpp", "shell"],
    "docker": ["docker", "shell", "python"],
    "network": ["network", "shell", "python"],
}
FILL = {"pico": ["cpp", "python", "shell"], "github": ["shell"]}
NOTE = ("コードの単語をクリックしたときに出す説明。tools/make_glossaries.py が tools/glossary/ の辞書から作る（直すときは辞書のほうを直す）。"
        "キーは「単語」「関数名.引数名」「$ コマンド サブコマンド」「#include <名前>」。")
NOTE_EN = ("Explanations shown when you click a word in the code (English). tools/make_glossaries.py makes this file "
           "from the dictionaries in tools/glossary/en/ (fix the dictionaries, not this file).")


def corpus(book):
    """本の中のコード（コードブロックと `…`）の、言葉とコマンドの切れはし"""
    d = ROOT / "books" / book
    if (d / "ja").is_dir():                 # 英語版はコードが同じでコメントだけ英語なので、日本語版だけを見る
        d = d / "ja"
    text = "\n".join(p.read_text(encoding="utf-8") for p in sorted(d.glob("**/*.md")))
    blocks = re.findall(r"```([^\n]*)\n(.*?)```", text, re.S)
    code = [b for info, b in blocks if info.strip() != "quiz"]
    code += ["\n".join(re.findall(r"^\|\s?(.*)$", b, re.M)) for info, b in blocks if info.strip() == "quiz"]   # 練習問題はコードの行だけ
    code += re.findall(r"`([^`\n]+)`", text)
    joined = "\n".join(code)
    return set(re.findall(r"\w+", joined)), set(joined.split()), joined


def used(key, words, toks, joined):
    if key == "_説明":
        return False
    if key.startswith("#include"):
        return key[len("#include "):].strip("<>\"") in joined
    if key.startswith("$ "):
        return all(p in toks for p in key[2:].split(" "))
    return all(p in words for p in key.split("."))


def load(name, en=False):
    if name.startswith("book:"):           # 手で書いた本の glossary.json（コマンドの説明だけ使う）
        p = ROOT / "books" / name[5:] / ("glossary-en.json" if en else "glossary.json")
        g = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
        return {k: v for k, v in g.items() if k.startswith("$ ")}
    return json.loads((SRC / ("en" if en else "") / f"{name}.json").read_text(encoding="utf-8"))


def merged(names, en=False):
    out = {}
    for n in names:
        for k, v in load(n, en).items():
            out.setdefault(k, v)            # 先に書いた辞書が優先
    return out


def append(p, add):
    """手で書いた並びと空行を崩さないよう、最後に書き足す"""
    text = p.read_text(encoding="utf-8").rstrip()
    assert text.endswith("}")
    body = text[:-1].rstrip()
    lines = [f"  {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)}" for k, v in add.items()]
    p.write_text(body + ",\n\n" + ",\n".join(lines) + "\n}\n", encoding="utf-8")
    json.loads(p.read_text(encoding="utf-8"))


def english(book):
    meta = json.loads((ROOT / "books.json").read_text(encoding="utf-8"))
    meta = meta if isinstance(meta, list) else meta["books"]
    return any(b["id"] == book and "en" in b.get("langs", []) for b in meta)


def write_en(book, names, g):
    """glossary.json と同じ言葉の英語版。英語の辞書にない言葉は出して知らせる（画面では日本語のまま）"""
    src = merged(names, en=True)
    ge = {"_説明": NOTE_EN}
    ge.update({k: src[k] for k in g if k != "_説明" and k in src})
    (ROOT / "books" / book / "glossary-en.json").write_text(json.dumps(ge, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    miss = [k for k in g if k != "_説明" and k not in src]
    print(f"{book}: 英語 {len(ge) - 1} 語" + (f"（英語の辞書にない: {', '.join(miss)}）" if miss else ""))


def main():
    shared_shell = ["book:github", "book:pico"]   # git・ssh・apt などは、手で書いた説明を先に使う
    for book, names in BOOKS.items():
        words, toks, joined = corpus(book)
        order = [n for n in names if n != "shell"] + (shared_shell + ["shell"] if "shell" in names else [])
        src = merged(order)
        g = {"_説明": NOTE}
        g.update({k: v for k, v in src.items() if used(k, words, toks, joined)})
        (ROOT / "books" / book / "glossary.json").write_text(json.dumps(g, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{book}: {len(g) - 1} 語")
        if english(book):
            write_en(book, order, g)
    for book, names in FILL.items():
        p = ROOT / "books" / book / "glossary.json"
        g = json.loads(p.read_text(encoding="utf-8"))
        words, toks, joined = corpus(book)
        add = {k: v for k, v in merged(names).items() if k not in g and used(k, words, toks, joined)}
        if add:
            append(p, add)
            g.update(add)
        print(f"{book}: {len(add)} 語を足した")
        pe = ROOT / "books" / book / "glossary-en.json"
        if pe.exists():                     # 英語版も、日本語にあって英語にない言葉を足す
            ge = json.loads(pe.read_text(encoding="utf-8"))
            src = merged(names, en=True)
            add = {k: src[k] for k in g if k not in ge and k in src}
            if add:
                append(pe, add)
            miss = [k for k in g if k not in ge and k not in src]
            print(f"{book}: 英語に {len(add)} 語を足した" + (f"（英語の辞書にない: {', '.join(miss)}）" if miss else ""))


if __name__ == "__main__":
    main()
