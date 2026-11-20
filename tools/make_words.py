#!/usr/bin/env python3
"""教科書の単語帳を、books/<id>/words/*.txt から作る（いまは ielts と swahili）。

    python3 tools/make_words.py            # 全部
    python3 tools/make_words.py swahili    # 本を選んで

words/ のファイル（ファイル名の順に並べる。頭の2けたの番号で、まとまり GROUPS に分ける）:
    1行目     # 日本語の題 | English title（日本語だけの本は「# 日本語の題」）
    2行目から  ielts:   単語 | 品詞の記号 | 日本語の意味 | English meaning | 例文（見出しの言葉は自動で太字）
              swahili: 単語 | 品詞（そのまま出す。例「名 KI-VI」） | 日本語の意味 | 例文（太字は **…** で自分で書く）
ielts の品詞の記号: n 名詞, v 動詞, adj 形容詞, adv 副詞, phr 句, pv 句動詞, conj 接続詞, prep 前置詞, id 慣用句

その本の単語帳の章の「## 単語帳」（英語は Word list）から「## 練習問題」（Exercises）の前までを作り直す。
そこより前と後ろは手で書いた本文なので、そのまま残す。
「## 単語帳」の説明と、1つの ```words のブロック（「## まとまり」「# 話題」の行と、1行に「単語 | 品詞 | 意味 | 例文」）を書く。
読む画面（index.html）が、話題の一覧と 20語ずつのページ、既読の □・○ のチェック・見直す・意味を隠す・探す・発音の付いた単語帳にする。
スワヒリ語の発音の mp3 は tools/make_word_audio.py で作る（```words sw audio）。
例文の中の見出しの言葉（-s・-ed・-ing などの形も）を太字にする。同じ言葉が2回出てきたら知らせる。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POS = {"n": ("名", "n."), "v": ("動", "v."), "adj": ("形", "adj."), "adv": ("副", "adv."), "phr": ("句", "phr."),
       "pv": ("句動", "phr. v."), "conj": ("接", "conj."), "prep": ("前", "prep."), "id": ("慣", "idiom")}
HEAD = {"ja": ("## 単語帳", "## 練習問題"), "en": ("## Word list", "## Exercises")}
OLD_HEAD = {"ja": "## 単語帳の使い方", "en": "## How to use this word list"}   # 前の版の見出し（あれば、そこから作り直す）
INTRO_IELTS = {
    "ja": """- IELTS のバンド7 に役立つ言葉 **{n:,} 語**を、{t} の話題に分けました。品詞・意味・例文つきです
- 下の一覧で話題を選ぶと、**20語ずつ**のページで出ます。下の番号で次のページへ、最後のページの「次の話題へ」で続けられます。次に開いたときは、前に見ていた所から始まります
- わからない単語は、左の **○** を押してチェックします。上の「**✓ 見直す**」で、チェックした単語だけを出します。話題の中で押すとその話題だけ、話題の一覧で押すと全部の話題から集めます（覚えたら、もう一度押して外す）
- 読んだ単語は、左はしの **□** にチェックを入れます（既読）。話題の一覧に、既読の数が出ます
- 「**意味を隠す**」で意味と例文がぼやけます。意味を言えるか試してから、押して確かめます。🔊 で発音、「単語・意味で探す」で全部の話題から探せます
- 品詞の記号: **名** 名詞、**動** 動詞、**形** 形容詞、**副** 副詞、**句** いくつかの語のまとまり、**句動** 句動詞、**接** 接続詞、**前** 前置詞、**慣** 慣用句。例文の太字がその言葉で、`sth` は something、`sb` は somebody の略です""",
    "en": """- **{n:,} words** that help with IELTS Band 7, in {t} topics, each with its part of speech, meaning and an example
- Choose a topic below to see it **20 words per page**. Use the numbers at the bottom to turn pages, and "Next topic" on the last page to carry on. Next time, you start where you left off
- Tap the **○** next to a word you don't know to mark it. "**✓ Review**" at the top shows only your marked words: from that topic when you are in one, or from every topic on the topic list (tap ○ again to unmark once you know it)
- Tick the **box** at the far left once you've read a word. The topic list shows how many you've read
- "**Hide meanings**" blurs meanings and examples. Try to recall the meaning, then tap to check. Tap 🔊 to hear a word, and search all topics with the search box
- Parts of speech: **n.** noun, **v.** verb, **adj.** adjective, **adv.** adverb, **phr.** phrase, **phr. v.** phrasal verb, **conj.** conjunction, **prep.** preposition, **idiom**. The word is in bold in its example; `sth` means something and `sb` means somebody""",
}

INTRO_SW = {
    "ja": """- この本の言葉と、東アフリカの暮らし・畑・牛と酪農でよく使う言葉 **{n:,} 語**を、{t} の話題に分けました。品詞・意味・例文（日本語の訳つき）があります
- 下の一覧で話題を選ぶと、**20語ずつ**のページで出ます。下の番号で次のページへ、最後のページの「次の話題へ」で続けられます。次に開いたときは、前に見ていた所から始まります
- わからない単語は、左の **○** を押してチェックします。上の「**✓ 見直す**」で、チェックした単語だけを出します。話題の中で押すとその話題だけ、話題の一覧で押すと全部の話題から集めます（覚えたら、もう一度押して外す）
- 読んだ単語は、左はしの **□** にチェックを入れます（既読）。話題の一覧に、既読の数が出ます
- 「**意味を隠す**」で意味と例文がぼやけます。意味を言えるか試してから、押して確かめます。「単語・意味で探す」は、スワヒリ語でも日本語でも探せます。🔊 で発音を聞けます（機械で作った声です）
- 名詞は（ ）に複数の形を、品詞にクラス（M-WA・KI-VI など、6章）を書きました。動詞は辞書の形（ku-）、形容詞は頭のない形（-zuri）です。例文の太字が、その言葉です""",
}
# 本ごとの設定: 単語帳の章のファイル、言葉、品詞の扱い、まとまり（ファイルの番号の、はじめの番号）、説明、```words の印
BOOKS = {
    "ielts": dict(chapter="01-vocabulary.md", langs=["ja", "en"], fields=5, pos=POS, intro=INTRO_IELTS, flag="",
                  groups=[(1, "学術の言葉", "Academic words"), (5, "話題ごとの言葉", "Words by topic"),
                          (23, "Writing と Speaking で使う言葉", "Words for Writing and Speaking")]),
    "swahili": dict(chapter="18-words.md", langs=[None], fields=4, pos=None, intro=INTRO_SW, flag=" sw audio",
                    groups=[(1, "はじめの言葉", ""), (5, "暮らしの言葉", ""), (14, "自然と社会の言葉", ""),
                            (22, "畑と牛の言葉", ""), (28, "文を作る言葉", "")]),
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


def load(bid, cfg):
    topics, seen, bad = [], {}, 0
    for f in sorted((ROOT / "books" / bid / "words").glob("*.txt")):
        lines = [l.rstrip("\n") for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
        ja, en = ([x.strip() for x in lines[0].lstrip("#").split("|")] + [""])[:2]
        rows = []
        for k, l in enumerate(lines[1:], 2):
            parts = [x.strip() for x in l.split(" | ")]
            if len(parts) == 4 and cfg["fields"] == 4:
                parts = parts[:3] + [""] + parts[3:]      # 英語の意味のない本
            if len(parts) != 5 or (cfg["pos"] and parts[1] not in cfg["pos"]) or not all(x for i, x in enumerate(parts) if i != 3 or cfg["fields"] == 5):
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


def build(lang, topics, cfg):
    n = sum(len(r) for *_, r in topics)
    L = lang or "ja"
    out = [HEAD[L][0], "", cfg["intro"][L].format(n=n, t=len(topics)), "", "```words" + cfg["flag"]]
    gi, groups = -1, cfg["groups"]
    for num, ja, en, rows in topics:
        while gi + 1 < len(groups) and num >= groups[gi + 1][0]:
            gi += 1
            out.append(f"## {groups[gi][1] if L == 'ja' else groups[gi][2]}")
        out.append(f"# {ja if L == 'ja' else en}")
        for word, pos, mja, men, ex in rows:
            p = cfg["pos"][pos][0 if L == "ja" else 1] if cfg["pos"] else pos
            ex = ex if "**" in ex or not cfg["pos"] else bold(word, ex)
            out.append(f"{cell(word)} | {p} | {cell(mja if L == 'ja' else men)} | {cell(ex)}")
    out += ["```", ""]
    return "\n".join(out)

def main():
    bad_all = 0
    for bid in sys.argv[1:] or list(BOOKS):
        cfg = BOOKS[bid]
        topics, bad = load(bid, cfg)
        bad_all += bad
        n = sum(len(r) for *_, r in topics)
        if cfg["pos"]:
            nobold = [(w, e) for *_, rows in topics for w, _, _, _, e in rows if "**" not in bold(w, e)]
        else:
            nobold = [(w, e) for *_, rows in topics for w, _, _, _, e in rows if "**" not in e]
        for lang in cfg["langs"]:
            p = ROOT / "books" / bid / (lang or "") / cfg["chapter"]
            L = lang or "ja"
            text = p.read_text(encoding="utf-8")
            a, b = text.find("\n" + HEAD[L][0] + "\n"), text.find("\n" + HEAD[L][1] + "\n")
            if a < 0:
                a = text.find("\n" + OLD_HEAD[L] + "\n")
            if a < 0 or b < 0 or b < a:
                sys.exit(f"{p}: 「{HEAD[L][0]}」と「{HEAD[L][1]}」の見出しが見つからない")
            p.write_text(text[:a + 1] + build(lang, topics, cfg) + "\n" + text[b + 1:], encoding="utf-8")
        print(f"{bid}: {len(topics)} の話題、{n} 語。例文に太字がないもの {len(nobold)} 語")
        for w, e in nobold[:40]:
            print(f"  ・{w}: {e}")
    sys.exit(1 if bad_all else 0)


if __name__ == "__main__":
    main()
