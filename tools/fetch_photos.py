"""Wikimedia Commons の写真を教科書の images/ に取り込み、写真の出典の付録を作る。

使い方:  python3 tools/fetch_photos.py <本の id>   （例: africa、cow、pico）

- books/<id>/photos.json に、使う写真を並べる:
    [{"file": "ugali.jpg", "src": "Ugali and cabbage.jpg"}, ...]
  src は Commons のファイル名（"File:" は付けない）。
- まだ取り込んでいない写真だけ、幅 960 px の JPEG にして images/<file> に保存する。
  撮影者・ライセンス・元のページは photos.json に書き戻す（次からは通信しない）。
- 本文（chapters.json の順）で使っている写真を拾い、付録「写真の出典」を作り直す。
  1つの言葉の本は books/<id>/c-photos.md、2つの言葉の本は ja/ と en/ に作る。
  付録の文字がずれる本は、chapters.json に "x-photos.md" の形で入れておけば、その名前で作る。
- 使えるのは CC0・パブリックドメイン・CC BY・CC BY-SA だけ（それ以外は止める）。
"""
import io
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
UA = "textbooks-photo-fetch/1.0 (educational textbook; python-urllib)"
WIDTH = 960
CREDITS = "c-photos.md"
OK = re.compile(r"^(CC0|Public domain|PD|CC BY(-SA)? [0-9.]+)", re.I)
TEXT = {
    "ja": {"title": "写真の出典", "lead": "写真は Wikimedia Commons から借りています。撮影者とライセンスは次のとおりです。写真は幅を小さくして使っています。",
           "head": "| 写真 | 撮影者 | ライセンス |"},
    "en": {"title": "Photo credits", "lead": "The photos come from Wikimedia Commons. Authors and licences are listed below. The photos have been resized.",
           "head": "| Photo | Author | Licence |"},
}


def get(url, tries=6):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for k in range(tries):
        try:
            time.sleep(1.0)
            return urllib.request.urlopen(req, timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or k == tries - 1:
                raise
            time.sleep(10 * (k + 1))


def strip(html):
    s = re.sub(r"<[^>]+>", "", html or "")
    return re.sub(r"\s+", " ", s).strip()


def info(src):
    q = urllib.parse.urlencode({"action": "query", "titles": "File:" + src, "prop": "imageinfo", "format": "json",
                                "iiprop": "url|extmetadata", "iiurlwidth": WIDTH,
                                "iiextmetadatafilter": "LicenseShortName|LicenseUrl|Artist|Credit"})
    page = next(iter(json.loads(get("https://commons.wikimedia.org/w/api.php?" + q))["query"]["pages"].values()))
    if "imageinfo" not in page:
        raise SystemExit(f"見つからない: {src}")
    ii = page["imageinfo"][0]
    m = {k: v.get("value", "") for k, v in ii.get("extmetadata", {}).items()}
    lic = strip(m.get("LicenseShortName"))
    if not OK.match(lic):
        raise SystemExit(f"使えないライセンス {lic}: {src}")
    author = strip(m.get("Artist")) or strip(m.get("Credit")) or "不明"
    if len(author) > 80:
        author = author[:78] + "…"
    return ii.get("thumburl") or ii["url"], {"author": author, "license": lic, "license_url": m.get("LicenseUrl", ""),
                                              "page": ii["descriptionurl"]}


def save(data, path):
    im = Image.open(io.BytesIO(data))
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, "white")
        bg.paste(im, mask=im.split()[-1])
        im = bg
    im = im.convert("RGB")
    if im.width > WIDTH:
        im = im.resize((WIDTH, round(im.height * WIDTH / im.width)), Image.LANCZOS)
    im.save(path, "JPEG", quality=80, optimize=True, progressive=True)


def cell(s):
    return s.replace("|", "／")


def credits(book, photos, lang):
    """本文で使っている順に、章ごとの表にする。"""
    by_file = {p["file"]: p for p in photos}
    chapters = json.loads((book / "chapters.json").read_text())
    md_dir = book / lang if (book / lang).is_dir() else book
    t = TEXT[lang]
    name = lambda ch: ch["title"][lang] if isinstance(ch["title"], dict) else ch["title"]
    own = next((ch for ch in chapters if ch["file"].endswith("-photos.md")), None)
    fname = own["file"] if own else CREDITS
    out, used = [f"# {name(own) if own else t['title']}", "", t["lead"], ""], set()
    for ch in chapters:
        if ch["file"] == fname:
            continue
        text = (md_dir / ch["file"]).read_text()
        rows = []
        for alt, f in re.findall(r"^\s*!\[([^\]]*)\]\(images/([^)\s]+)\)\s*$", text, re.M):
            if f in by_file and f not in used and "page" in by_file[f]:   # 取り込めなかった写真は載せない
                used.add(f)
                p = by_file[f]
                lic = f"[{p['license']}]({p['license_url']})" if p.get("license_url") else p["license"]
                rows.append(f"| [{cell(alt)}]({p['page']}) | {cell(p['author'])} | {lic} |")
        if rows:
            out += [f"## {name(ch)}", "", t["head"], "| --- | --- | --- |", *rows, ""]
    (md_dir / fname).write_text("\n".join(out).rstrip() + "\n")
    return used


def main():
    book = ROOT / "books" / sys.argv[1]
    plist = book / "photos.json"
    photos = json.loads(plist.read_text())
    (book / "images").mkdir(exist_ok=True)
    for p in photos:
        dest = book / "images" / p["file"]
        if dest.exists() and "page" in p:
            continue
        try:
            url, meta = info(p["src"])
        except SystemExit as e:          # 見つからない・使えないライセンスは飛ばして、最後に知らせる
            print(f"飛ばした: {e}")
            continue
        p.update(meta)
        save(get(url), dest)
        print(f"取り込み {p['file']}  {meta['license']}  {meta['author'][:30]}")
        plist.write_text(json.dumps(photos, indent=2, ensure_ascii=False) + "\n")
    langs = ["ja", "en"] if (book / "ja").is_dir() else ["ja"]
    for lang in langs:
        used = credits(book, photos, lang)
        unused = [p["file"] for p in photos if p["file"] not in used]
        if unused:
            print(f"[{lang}] 本文で使っていない写真: {', '.join(unused)}")
    plist.write_text(json.dumps(photos, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
