#!/usr/bin/env python3
"""コードの言葉の説明（books/<id>/glossary.json）を、tools/glossary/ の辞書から作る。

    python3 tools/make_glossaries.py

- tools/glossary/*.json は、言語・ライブラリごとの辞書（python・numpy・cpp・shell・ros など）
- 本ごとに、使う辞書を BOOKS に並べる（先に書いた辞書が優先）。その本のコードに出てくる言葉だけを入れる
- pico・github の glossary.json は手で書いたものなので、上書きせず、足りない言葉だけを足す（FILL）
- キーの書き方は glossary.json の "_説明"（「単語」「関数名.引数名」「$ コマンド サブコマンド」「#include <名前>」）
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
}
FILL = {"pico": ["cpp", "python", "shell"], "github": ["shell"]}
NOTE = ("コードの単語をクリックしたときに出す説明。tools/make_glossaries.py が tools/glossary/ の辞書から作る（直すときは辞書のほうを直す）。"
        "キーは「単語」「関数名.引数名」「$ コマンド サブコマンド」「#include <名前>」。")


def corpus(book):
    """本の中のコード（コードブロックと `…`）の、言葉とコマンドの切れはし"""
    d = ROOT / "books" / book
    text = "\n".join(p.read_text(encoding="utf-8") for p in sorted(d.glob("**/*.md")))
    code = re.findall(r"```[^\n]*\n(.*?)```", text, re.S) + re.findall(r"`([^`\n]+)`", text)
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


def load(name):
    if name.startswith("book:"):           # 手で書いた本の glossary.json（コマンドの説明だけ使う）
        g = json.loads((ROOT / "books" / name[5:] / "glossary.json").read_text(encoding="utf-8"))
        return {k: v for k, v in g.items() if k.startswith("$ ")}
    return json.loads((SRC / f"{name}.json").read_text(encoding="utf-8"))


def merged(names):
    out = {}
    for n in names:
        for k, v in load(n).items():
            out.setdefault(k, v)            # 先に書いた辞書が優先
    return out


def main():
    shared_shell = ["book:github", "book:pico"]   # git・ssh・apt などは、手で書いた説明を先に使う
    for book, names in BOOKS.items():
        words, toks, joined = corpus(book)
        src = merged([n for n in names if n != "shell"] + (shared_shell + ["shell"] if "shell" in names else []))
        g = {"_説明": NOTE}
        g.update({k: v for k, v in src.items() if used(k, words, toks, joined)})
        (ROOT / "books" / book / "glossary.json").write_text(json.dumps(g, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{book}: {len(g) - 1} 語")
    for book, names in FILL.items():
        p = ROOT / "books" / book / "glossary.json"
        g = json.loads(p.read_text(encoding="utf-8"))
        words, toks, joined = corpus(book)
        add = {k: v for k, v in merged(names).items() if k not in g and used(k, words, toks, joined)}
        if add:                             # 手で書いた並びと空行を崩さないよう、最後に書き足す
            text = p.read_text(encoding="utf-8").rstrip()
            assert text.endswith("}")
            body = text[:-1].rstrip()
            lines = [f"  {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)}" for k, v in add.items()]
            p.write_text(body + ",\n\n" + ",\n".join(lines) + "\n}\n", encoding="utf-8")
            json.loads(p.read_text(encoding="utf-8"))
        print(f"{book}: {len(add)} 語を足した")


if __name__ == "__main__":
    main()
