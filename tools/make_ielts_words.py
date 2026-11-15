#!/usr/bin/env python3
"""IELTS の教科書の単語帳（1章の後半）を、books/ielts/words/*.txt から作る。

    python3 tools/make_ielts_words.py

words/ のファイル（ファイル名の順に並べる）:
    1行目     # 日本語の題 | English title
    2行目から  単語 | 品詞 | 日本語の意味 | English meaning | 例文
品詞の記号: n 名詞, v 動詞, adj 形容詞, adv 副詞, phr 句, pv 句動詞, conj 接続詞, prep 前置詞, id 慣用句

1章（ja/01-vocabulary.md・en/01-vocabulary.md）の「## 単語帳の使い方」（How to use this word list）から
「## 練習問題」（Exercises）の前までを作り直す。そこより前と後ろは手で書いた本文なので、そのまま残す。
話題ごとに「## 題」と ```words のブロック（1行に「単語 | 品詞 | 意味 | 例文」）を書く。読む画面（index.html）が、
○ のチェック・絞りこみ・意味を隠す・探す・発音の付いた単語帳にする。
例文の中の見出しの言葉（-s・-ed・-ing などの形も）を太字にする。同じ言葉が2回出てきたら知らせる。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "ielts"
POS = {"n": ("名", "n."), "v": ("動", "v."), "adj": ("形", "adj."), "adv": ("副", "adv."), "phr": ("句", "phr."),
       "pv": ("句動", "phr. v."), "conj": ("接", "conj."), "prep": ("前", "prep."), "id": ("慣", "idiom")}
HEAD = {"ja": ("## 単語帳の使い方", "## 練習問題"), "en": ("## How to use this word list", "## Exercises")}
INTRO = {
    "ja": """- この単語帳には、IELTS のバンド7 に役立つ言葉が **{n:,} 語**あります。{t} の話題に分け、品詞・意味・例文を付けました
- 品詞の記号: **名** 名詞、**動** 動詞、**形** 形容詞、**副** 副詞、**句** いくつかの語のまとまり、**句動** 句動詞（動詞＋副詞・前置詞）、**接** 接続詞、**前** 前置詞、**慣** 慣用句
- 例文の太字が、その言葉です。動詞の形（-s・-ed・-ing）や名詞の複数形は、文に合わせて変えています。`sth` は something（何か）、`sb` は somebody（だれか）の略です
- わからなかった単語は、左の **○** を押してチェックします。上の「**✓ 見直す**」を押すと、チェックした単語だけが出ます（覚えたら、もう一度押して外す）。チェックはこの端末のブラウザに残ります
- 「**意味を隠す**」で意味と例文がぼやけます。単語を見て意味を言えるか試し、押すと出ます
- 「単語・意味で探す」に英語か日本語を入れると、その言葉をふくむ単語だけが出ます。🔊 で発音を聞けます
- 1日に1つの話題を目安に、例文ごと声に出して読みます。目次の ▶ から、話題の所へ飛べます""",
    "en": """- This word list has **{n:,} words** that help with IELTS Band 7, grouped into {t} topics, each with its part of speech, meaning and an example sentence
- Parts of speech: **n.** noun, **v.** verb, **adj.** adjective, **adv.** adverb, **phr.** phrase, **phr. v.** phrasal verb, **conj.** conjunction, **prep.** preposition, **idiom**
- The word is in bold in its example. Verb forms (-s, -ed, -ing) and plurals change to fit the sentence. `sth` means something and `sb` means somebody
- Tap the **○** next to a word you don't know to mark it. Press "**✓ Review**" at the top to show only marked words (tap again to unmark once you know it). Marks are saved in this browser
- "**Hide meanings**" blurs the meanings and examples. Test yourself on each word, then tap it to reveal
- Type English or Japanese in the search box to show only matching words. Tap 🔊 to hear a word
- Aim for one topic a day, reading the examples aloud. Use the ▶ in the table of contents to jump to a topic""",
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
        topics.append((ja, en, rows))
    return topics, bad


def build(lang, topics):
    n = sum(len(r) for _, _, r in topics)
    out = [HEAD[lang][0], "", INTRO[lang].format(n=n, t=len(topics)), ""]
    for ja, en, rows in topics:
        out += [f"## {ja if lang == 'ja' else en}", "", "```words"]
        for word, pos, mja, men, ex in rows:
            p = POS[pos][0 if lang == "ja" else 1]
            out.append(f"{cell(word)} | {p} | {cell(mja if lang == 'ja' else men)} | {cell(bold(word, ex))}")
        out += ["```", ""]
    return "\n".join(out)


def main():
    topics, bad = load()
    n = sum(len(r) for _, _, r in topics)
    nobold = [(w, e) for _, _, rows in topics for w, _, _, _, e in rows if "**" not in bold(w, e)]
    for lang in ("ja", "en"):
        p = BOOK / lang / "01-vocabulary.md"
        text = p.read_text(encoding="utf-8")
        a, b = text.find("\n" + HEAD[lang][0] + "\n"), text.find("\n" + HEAD[lang][1] + "\n")
        if a < 0 or b < 0 or b < a:
            sys.exit(f"{p}: 「{HEAD[lang][0]}」と「{HEAD[lang][1]}」の見出しが見つからない")
        p.write_text(text[:a + 1] + build(lang, topics) + "\n" + text[b + 1:], encoding="utf-8")
    print(f"{len(topics)} の話題、{n} 語。例文に見出しの言葉が見つからないもの {len(nobold)} 語")
    for w, e in nobold[:40]:
        print(f"  ・{w}: {e}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
