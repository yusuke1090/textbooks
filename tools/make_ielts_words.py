#!/usr/bin/env python3
"""IELTS の教科書の単語帳（1章の後半）を、books/ielts/words/*.txt から作る。

    python3 tools/make_ielts_words.py

words/ のファイル（ファイル名の順に並べる）:
    1行目     # 日本語の題 | English title
    2行目から  単語 | 品詞 | 日本語の意味 | English meaning | 例文
品詞の記号: n 名詞, v 動詞, adj 形容詞, adv 副詞, phr 句, pv 句動詞, conj 接続詞, prep 前置詞, id 慣用句

1章（ja/01-vocabulary.md・en/01-vocabulary.md）の「## 単語帳」（Word list）から
「## 練習問題」（Exercises）の前までを作り直す。そこより前と後ろは手で書いた本文なので、そのまま残す。
「## 単語帳」の説明と、1つの ```words のブロック（「## まとまり」「# 話題」の行と、1行に「単語 | 品詞 | 意味 | 例文」）を書く。
読む画面（index.html）が、話題の一覧と 20語ずつのページ、○ のチェック・見直す・意味を隠す・探す・発音の付いた単語帳にする。
例文の中の見出しの言葉（-s・-ed・-ing などの形も）を太字にする。同じ言葉が2回出てきたら知らせる。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "ielts"
POS = {"n": ("名", "n."), "v": ("動", "v."), "adj": ("形", "adj."), "adv": ("副", "adv."), "phr": ("句", "phr."),
       "pv": ("句動", "phr. v."), "conj": ("接", "conj."), "prep": ("前", "prep."), "id": ("慣", "idiom")}
HEAD = {"ja": ("## 単語帳", "## 練習問題"), "en": ("## Word list", "## Exercises")}
OLD_HEAD = {"ja": "## 単語帳の使い方", "en": "## How to use this word list"}   # 前の版の見出し（あれば、そこから作り直す）
# 話題のまとまり（ファイル名の頭の番号の、はじめの番号）
GROUPS = [(1, "学術の言葉", "Academic words"), (5, "話題ごとの言葉", "Words by topic"),
          (23, "Writing と Speaking で使う言葉", "Words for Writing and Speaking")]
INTRO = {
    "ja": """- IELTS のバンド7 に役立つ言葉 **{n:,} 語**を、{t} の話題に分けました。品詞・意味・例文つきです
- 下の一覧で話題を選ぶと、**20語ずつ**のページで出ます。下の番号で次のページへ、最後のページの「次の話題へ」で続けられます。次に開いたときは、前に見ていた所から始まります
- わからない単語は、左の **○** を押してチェックします。上の「**✓ 見直す**」で、チェックした単語だけを全部の話題から集めて出します（覚えたら、もう一度押して外す）
- 「**意味を隠す**」で意味と例文がぼやけます。意味を言えるか試してから、押して確かめます。🔊 で発音、「単語・意味で探す」で全部の話題から探せます
- 品詞の記号: **名** 名詞、**動** 動詞、**形** 形容詞、**副** 副詞、**句** いくつかの語のまとまり、**句動** 句動詞、**接** 接続詞、**前** 前置詞、**慣** 慣用句。例文の太字がその言葉で、`sth` は something、`sb` は somebody の略です""",
    "en": """- **{n:,} words** that help with IELTS Band 7, in {t} topics, each with its part of speech, meaning and an example
- Choose a topic below to see it **20 words per page**. Use the numbers at the bottom to turn pages, and "Next topic" on the last page to carry on. Next time, you start where you left off
- Tap the **○** next to a word you don't know to mark it. "**✓ Review**" at the top collects your marked words from every topic (tap ○ again to unmark once you know it)
- "**Hide meanings**" blurs meanings and examples. Try to recall the meaning, then tap to check. Tap 🔊 to hear a word, and search all topics with the search box
- Parts of speech: **n.** noun, **v.** verb, **adj.** adjective, **adv.** adverb, **phr.** phrase, **phr. v.** phrasal verb, **conj.** conjunction, **prep.** preposition, **idiom**. The word is in bold in its example; `sth` means something and `sb` means somebody""",
}

IRREGULAR = {"take": "took|taken", "make": "made", "bring": "brought", "give": "gave|given", "go": "went|gone",
                 "come": "came", "set": "set", "put": "put", "run": "ran", "fall": "fell|fallen", "rise": "rose|risen",
                 "grow": "grew|grown", "keep": "kept", "hold": "held", "break": "broke|broken", "get": "got|gotten",
                 "draw": "drew|drawn", "find": "found", "lead": "led", "seek": "sought", "spend": "spent",
                 "catch": "caught", "pay": "paid", "sell": "sold", "think": "thought", "be": "was|were|been|is|are",
                 "have": "had|has", "do": "did|done|does|doing", "see": "saw|seen", "know": "knew|known", "feel": "felt",
                 "stand": "stood", "build": "built", "send": "sent", "lay": "laid", "drive": "drove|driven",
                 "write": "wrote|written", "speak": "spoke|spoken", "choose": "chose|chosen", "forecast": "forecast",
                 "undertake": "undertook|undertaken", "overcome": "overcame", "withdraw": "withdrew|withdrawn",
                 "arise": "arose|arisen", "outweigh": "outweighed", "shrink": "shrank|shrunk", "seek out": "sought out", "overtake": "overtook|overtaken",
             "wear": "wore|worn", "go": "went|gone|goes|going"}


def forms(tok):
    """1語の、変化した形も含む正規表現"""
    t = re.escape(tok)
    if len(tok) <= 2:
        return "(?:" + t + ("|" + IRREGULAR[tok.lower()] if tok.lower() in IRREGULAR else "") + ")"
    alts = [t + r"(?:s|es|d|ed|ing|er|est|ly)?"]
    if tok.endswith("e"):
        alts.append(re.escape(tok[:-1]) + r"(?:ing|ion|ation)")
    if tok.endswith("y"):
        alts.append(re.escape(tok[:-1]) + r"(?:ies|ied|ier|iest|ily)")
    if re.search(r"[^aeiou][aeiou][bdgklmnprt]$", tok):
        alts.append(t + re.escape(tok[-1]) + r"(?:ed|ing|er)")
    if tok.lower() in IRREGULAR:
        alts.append(IRREGULAR[tok.lower()])
    return "(?:" + "|".join(alts) + ")"


def bold(word, example):
    """例文の中の見出しの言葉を **…** にする。見つからなければそのまま"""
    w = re.sub(r"\(.*?\)", "", word)
    w = re.sub(r"\b(sth|sb|one's|someone's|something|somebody)\b", " ", w)
    toks = [x for x in re.split(r"[\s/]+", w) if x and x not in ("…", "...", "-")]
    if len(toks) > 1:   # 句では、冠詞と be・it's（例文で形が変わる）を目印にしない
        toks = [x for x in toks if x.lower() not in ("a", "an", "the", "be", "it's", "is")] or toks
    if not toks:
        return example
    if len(toks) == 1:
        pat = r"(?<![\w-])" + forms(toks[0]) + r"(?![\w])"
    else:   # 句: 語の間に少し別の語（目的語など）が入ってもよい
        pat = r"(?<![\w-])" + r"(?:\W+(?:\w+\W+){0,3}?)".join(forms(x) for x in toks) + r"(?![\w])"
    m = re.search(pat, example, re.I)
    if not m:
        return example
    return example[:m.start()] + "**" + m.group(0) + "**" + example[m.end():]


def cell(s):
    return s.replace(" | ", " / ")


def load():
    topics, seen, bad = [], {}, 0
    for f in sorted((BOOK / "words").glob("*.txt")):
        lines = [l.rstrip("\n") for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
        ja, en = [x.strip() for x in lines[0].lstrip("#").split("|")]
        rows = []
        for k, l in enumerate(lines[1:], 2):
            parts = [x.strip() for x in l.split(" | ")]
            if len(parts) != 5 or parts[1] not in POS or not all(parts):
                print(f"✗ {f.name}:{k}: 形がちがう: {l}")
                bad += 1
                continue
            key = parts[0].lower() + " (" + parts[1] + ")"
            if key in seen:
                print(f"△ {f.name}:{k}: 「{parts[0]}」は {seen[key]} にもある")
            seen[key] = f.name
            rows.append(parts)
        topics.append((int(f.name[:2]), ja, en, rows))
    return topics, bad


def build(lang, topics):
    n = sum(len(r) for *_, r in topics)
    out = [HEAD[lang][0], "", INTRO[lang].format(n=n, t=len(topics)), "", "```words"]
    gi = -1
    for num, ja, en, rows in topics:
        while gi + 1 < len(GROUPS) and num >= GROUPS[gi + 1][0]:
            gi += 1
            out.append(f"## {GROUPS[gi][1] if lang == 'ja' else GROUPS[gi][2]}")
        out.append(f"# {ja if lang == 'ja' else en}")
        for word, pos, mja, men, ex in rows:
            p = POS[pos][0 if lang == "ja" else 1]
            out.append(f"{cell(word)} | {p} | {cell(mja if lang == 'ja' else men)} | {cell(bold(word, ex))}")
    out += ["```", ""]
    return "\n".join(out)

def main():
    topics, bad = load()
    n = sum(len(r) for *_, r in topics)
    nobold = [(w, e) for *_, rows in topics for w, _, _, _, e in rows if "**" not in bold(w, e)]
    for lang in ("ja", "en"):
        p = BOOK / lang / "01-vocabulary.md"
        text = p.read_text(encoding="utf-8")
        a, b = text.find("\n" + HEAD[lang][0] + "\n"), text.find("\n" + HEAD[lang][1] + "\n")
        if a < 0:
            a = text.find("\n" + OLD_HEAD[lang] + "\n")
        if a < 0 or b < 0 or b < a:
            sys.exit(f"{p}: 「{HEAD[lang][0]}」と「{HEAD[lang][1]}」の見出しが見つからない")
        p.write_text(text[:a + 1] + build(lang, topics) + "\n" + text[b + 1:], encoding="utf-8")
    print(f"{len(topics)} の話題、{n} 語。例文に見出しの言葉が見つからないもの {len(nobold)} 語")
    for w, e in nobold[:40]:
        print(f"  ・{w}: {e}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
