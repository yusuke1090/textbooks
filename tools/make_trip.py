#!/usr/bin/env python3
"""本棚の「今日の勉強」の旅（教科書をめぐる世界一周）のデータを作る。

  python3 tools/make_trip.py <Natural Earth の geojson のフォルダ>

- trip/trip.json: 町（名前・経度緯度・その町に着くまでの時間・写真）と、地図の陸と湖（メルカトルの SVG パス）
- trip/<slug>.jpg: 町の写真の小さい版（教科書の写真から 160px の正方形に切る）
地図は Natural Earth の 1:50m（パブリックドメイン）の ne_50m_land.geojson と ne_50m_lakes.geojson を使う。
https://github.com/nvkelso/natural-earth-vector/tree/master/geojson からダウンロードしておく。
"""
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "trip"

# (slug, 日本語, English, 経度, 緯度, 前の町からの時間, 写真 = 教科書/画像)
STOPS = [
    ("tokyo", "東京", "Tokyo", 139.69, 35.69, 0, "religion/hatsumode"),
    ("kyoto", "京都", "Kyoto", 135.77, 34.97, 0.5, "religion/fushimi-inari"),
    ("beijing", "北京", "Beijing", 116.41, 39.88, 1, "religion/temple-of-heaven"),
    ("lhasa", "ラサ", "Lhasa", 91.12, 29.66, 1.5, "religion/potala"),
    ("lumbini", "ルンビニ", "Lumbini", 83.28, 27.47, 2, "religion/lumbini"),
    ("varanasi", "バラナシ", "Varanasi", 83.01, 25.32, 2, "religion/varanasi"),
    ("amritsar", "アムリトサル", "Amritsar", 74.88, 31.62, 2.5, "religion/golden-temple"),
    ("yazd", "ヤズド", "Yazd", 54.37, 31.90, 3, "religion/yazd"),
    ("istanbul", "イスタンブール", "Istanbul", 28.98, 41.01, 3, "religion/hagia-sophia"),
    ("jerusalem", "エルサレム", "Jerusalem", 35.23, 31.78, 3, "religion/dome-of-the-rock"),
    ("cairo", "カイロ", "Cairo", 31.26, 30.05, 3, "religion/al-azhar"),
    ("lalibela", "ラリベラ", "Lalibela", 39.04, 12.03, 3.5, "religion/lalibela"),
    ("nairobi", "ナイロビ", "Nairobi", 36.82, -1.29, 3.5, "africa/nairobi"),
    ("serengeti", "セレンゲティ", "Serengeti", 34.83, -2.33, 3.5, "africa/serengeti"),
    ("arusha", "アルーシャ", "Arusha", 36.68, -3.37, 3.5, "swahili/arusha-clock"),
    ("kilimanjaro", "キリマンジャロ", "Kilimanjaro", 37.36, -3.07, 4, "africa/kilimanjaro"),
    ("zanzibar", "ザンジバル", "Zanzibar", 39.19, -6.16, 4, "africa/dhow"),
    ("dar", "ダルエスサラーム", "Dar es Salaam", 39.28, -6.82, 4, "swahili/dar-waterfront"),
    ("malawi", "マラウイ湖", "Lake Malawi", 34.84, -14.02, 4, "africa/lake-malawi"),
    ("rome", "ローマ", "Rome", 12.45, 41.90, 4.5, "religion/st-peters"),
    ("wittenberg", "ヴィッテンベルク", "Wittenberg", 12.64, 51.87, 4.5, "religion/wittenberg"),
    ("london", "ロンドン", "London", -0.12, 51.50, 4.5, "uk/westminster"),
    ("stonehenge", "ストーンヘンジ", "Stonehenge", -1.83, 51.18, 4.5, "uk/stonehenge"),
    ("cotswolds", "コッツウォルズ", "Cotswolds", -1.76, 51.88, 4.5, "uk/cotswolds"),
    ("lakedistrict", "湖水地方", "Lake District", -3.08, 54.46, 5, "uk/herdwick"),
    ("edinburgh", "エディンバラ", "Edinburgh", -3.20, 55.95, 5, "uk/edinburgh-castle"),
    ("home", "東京", "Tokyo", 139.69, 35.69, 6, "religion/hatsumode"),
]

BOX = (-30, 165, -40, 68)   # 経度・緯度の範囲（この中にかかる陸だけを入れる）
TOL = 0.04                  # 間引き（度）
MIN_AREA = 0.02             # これより小さい島は入れない（度²）


def merc(lon, lat):
    lat = max(-80, min(80, lat))
    return lon, -math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))


def simplify(pts, tol):
    """Douglas–Peucker（両はしは残す）"""
    if len(pts) < 3:
        return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        (x1, y1), (x2, y2) = pts[a], pts[b]
        dx, dy = x2 - x1, y2 - y1
        n = math.hypot(dx, dy) or 1e-12
        best, idx = 0, -1
        for i in range(a + 1, b):
            x, y = pts[i]
            d = abs(dy * (x - x1) - dx * (y - y1)) / n if (dx or dy) else math.hypot(x - x1, y - y1)
            if d > best:
                best, idx = d, i
        if best > tol and idx > 0:
            keep[idx] = True
            stack += [(a, idx), (idx, b)]
    return [p for p, k in zip(pts, keep) if k]


def area(pts):
    return abs(sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]))) / 2


def rings(geom):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    for poly in polys:
        yield from poly


def path_of(geojson, min_area):
    out = []
    for f in json.loads(Path(geojson).read_text())["features"]:
        for ring in rings(f["geometry"]):
            lons = [p[0] for p in ring]
            lats = [p[1] for p in ring]
            if max(lons) < BOX[0] or min(lons) > BOX[1] or max(lats) < BOX[2] or min(lats) > BOX[3]:
                continue
            pts = simplify([merc(*p[:2]) for p in ring], TOL)
            if len(pts) < 4 or area(pts) < min_area:
                continue
            if pts[0] == pts[-1]:
                pts = pts[:-1]
            out.append("M" + "L".join(f"{x:.2f} {y:.2f}".replace(".00", "").replace("-0 ", "0 ") for x, y in pts) + "Z")
    return "".join(out)


def main():
    src_dir = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    OUT.mkdir(exist_ok=True)
    stops = []
    for slug, ja, en, lon, lat, h, photo in STOPS:
        book, name = photo.split("/")
        img = ROOT / "books" / book / "images" / f"{name}.jpg"
        src = next((p["src"] for p in json.loads((ROOT / "books" / book / "photos.json").read_text()) if p["file"] == f"{name}.jpg"), None)
        if not img.exists() or not src:
            sys.exit(f"写真がありません: {photo}")
        thumb = OUT / f"{slug}.jpg"
        if slug != "home":
            with Image.open(img) as im:
                ImageOps.fit(im.convert("RGB"), (160, 160), Image.LANCZOS).save(thumb, quality=82, optimize=True)
        x, y = merc(lon, lat)
        stops.append({"ja": ja, "en": en, "x": round(x, 2), "y": round(y, 2), "h": h,
                      "img": f"books/{book}/images/{name}.jpg", "thumb": f"trip/{'tokyo' if slug == 'home' else slug}.jpg", "src": src})
    data = {"stops": stops,
            "land": path_of(src_dir / "ne_50m_land.geojson", MIN_AREA),
            "lakes": path_of(src_dir / "ne_50m_lakes.geojson", 0.15)}
    (OUT / "trip.json").write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    total = sum(s["h"] for s in stops)
    print(f"{len(stops)} 町、全部で {total} 時間、trip.json {len((OUT / 'trip.json').read_bytes()) // 1024} KB")


if __name__ == "__main__":
    main()
