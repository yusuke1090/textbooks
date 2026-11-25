#!/usr/bin/env python3
"""本棚の「今日の勉強」の旅（教科書をめぐる世界一周）のデータを作る。

  python3 tools/make_trip.py <Natural Earth の geojson のフォルダ>
  （フォルダを付けないと、地図の陸と湖は今の trip.json のまま。町や写真の説明だけ直すとき）

- trip/trip.json: 町（名前・経度緯度・その町に着くまでの時間・写真・もらえる写真）と、地図の陸と湖（メルカトルの SVG パス）
- trip/<slug>.jpg: 町の写真の小さい版（教科書の写真から 240×160px の横長に切る。旅の下の行き先のカード）
- trip/gifts/: 1日の目標に届いた日にもらう、その土地ゆかりの写真（幅 960px）と、t/ に 240px の正方形
  写真は trip/gifts.json に町ごとに並べる: {"kyoto": [{"src": "Commons のファイル名", "ja": "名前", "en": "name", "desc": "写真を見るときの説明"}, ...]}
  まだ取り込んでいない写真だけ Commons から取り、撮影者・ライセンスを gifts.json に書き戻す（fetch_photos.py と同じやり方）
地図は Natural Earth の 1:50m（パブリックドメイン）の ne_50m_land.geojson と ne_50m_lakes.geojson を使う。
https://github.com/nvkelso/natural-earth-vector/tree/master/geojson からダウンロードしておく。
"""
import hashlib
import json
import math
import re
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

# 町の写真を見るときの説明（国・町のこと）。最後の東京（home）は、はじめの東京と同じ
NOTES = {
    "tokyo": ("日本", "旅の出発地で、ゴールでもある日本の首都。写真は明治神宮の初詣で、お正月の三が日には毎年300万人ほどがお参りに来ます。"),
    "kyoto": ("日本", "1,000年以上、日本の都だった町。写真の伏見稲荷大社では、お礼に納められた朱色の鳥居が、山の上まで1万基ほども続きます。"),
    "beijing": ("中国", "明と清の時代から続く中国の首都。写真の天壇・祈年殿は、皇帝が豊作を祈った建物で、くぎを使わずに木を組んで建てられています。"),
    "lhasa": ("中国・チベット", "標高約3,650mにある、チベットの祈りの町。写真のポタラ宮はダライ・ラマの宮殿だった建物で、部屋は1,000をこえます。"),
    "lumbini": ("ネパール", "お釈迦さまが生まれたと伝わる場所。写真のマーヤーデーヴィー寺院は、お母さんのマーヤー夫人の名前から付けられ、世界遺産になっています。"),
    "varanasi": ("インド", "ガンジス川のほとりの、ヒンドゥー教でいちばん大切な聖地のひとつ。川へ下りる石段（ガート）が80以上並び、朝は沐浴する人で、夜は祈りの火でにぎわいます。"),
    "amritsar": ("インド", "シク教の中心の町。写真の黄金寺院の無料の食堂では、宗教や身分に関係なく、毎日何万人もの人が並んで食事をします。"),
    "yazd": ("イラン", "砂漠のオアシスの古い町。日干しれんがの家と、風を取りこむ塔（バードギール）が並びます。写真はゾロアスター教の寺院で、1,500年以上燃え続けていると伝わる火が守られています。"),
    "istanbul": ("トルコ", "ヨーロッパとアジアのあいだのボスポラス海峡にまたがる町。写真のアヤソフィアは537年に教会として建てられ、のちにモスクになりました。"),
    "jerusalem": ("", "ユダヤ教・キリスト教・イスラム教の聖地が、城壁に囲まれた旧市街に集まる町。写真の岩のドームは7世紀の終わりに建てられ、金色の屋根が町のあちこちから見えます。"),
    "cairo": ("エジプト", "ナイル川のほとりの、アフリカでいちばん大きな町のひとつ。写真のアズハル・モスクは970年ごろに建てられ、世界でもっとも古い大学のひとつ、アズハル大学のもとになりました。"),
    "lalibela": ("エチオピア", "標高約2,500mの高原にある、キリスト教の巡礼の町。写真の聖ギオルギス教会は、800年ほど前に、地面の岩を上から十字の形にほり抜いて作られました。"),
    "nairobi": ("ケニア", "ケニアの首都で、名前はマサイの言葉で「冷たい水」。町のすぐ横に国立公園があり、高いビルのそばでキリンやライオンがくらしています。"),
    "serengeti": ("タンザニア", "タンザニアに広がる、果てしない草原の国立公園。写真のヌーは100万頭をこえる大群で、雨と草を追って、一年じゅう草原をめぐって旅をしています。"),
    "arusha": ("タンザニア", "サファリの出発点の町。真ん中の時計台は、カイロとケープタウンのちょうど中間にあると言われます。まわりを走るのは、バイクタクシーの「ボダボダ」です。"),
    "kilimanjaro": ("タンザニア", "アフリカでいちばん高い山（5,895m）。赤道の近くなのに、山頂には氷河があります。写真は、国境の向こうのケニアのアンボセリから見た姿です。"),
    "zanzibar": ("タンザニア", "インド洋にうかぶ島。香辛料と交易で栄えた古い町ストーンタウンは世界遺産です。写真のダウ船は、季節風に乗って昔からアラビアやインドと行き来してきた帆船です。"),
    "dar": ("タンザニア", "タンザニアでいちばん大きな港町で、名前はアラビア語で「平和の家」。写真の海辺から、ザンジバル行きの船が出ています。"),
    "malawi": ("マラウイ", "アフリカで3番目に大きな湖で、マラウイの国の5分の1ほどをしめます。魚の種類が世界のどの湖よりも多く、写真のケープ・マクレアの浜は、すんだ水で泳げます。"),
    "rome": ("イタリア", "2,000年以上の歴史があるイタリアの首都。写真のサン・ピエトロ大聖堂は、町の中にある世界でいちばん小さな国、バチカン市国にあります。"),
    "wittenberg": ("ドイツ", "1517年、マルティン・ルターがこの町で95か条の論題を出し、宗教改革が始まりました。写真の城教会の扉に、それを貼り出したと伝わっています。"),
    "london": ("イギリス", "テムズ川が流れるイギリスの首都。写真のウェストミンスター宮殿は国会議事堂で、時計塔の大きな鐘の名前がビッグ・ベンです。"),
    "stonehenge": ("イギリス", "5,000年ほど前から作られた、平原に大きな石が輪に並ぶ遺跡。夏至の日には、日の出の方向と石の並びがそろいます。"),
    "cotswolds": ("イギリス", "なだらかな丘に、はちみつ色の石の家が並ぶ田舎。中世にはヒツジの毛（羊毛）の取引で栄えました。"),
    "lakedistrict": ("イギリス", "イングランドでいちばん高い山々と、たくさんの湖がある国立公園。ピーターラビットの作者ビアトリクス・ポターが暮らし、写真のハードウィック種のヒツジを守る活動もしていました。"),
    "edinburgh": ("イギリス", "スコットランドの首都。写真のエディンバラ城は、大昔の火山の岩の上に建っています。夏は町じゅうが芸術祭でにぎわいます。"),
}

# 地図に出す地域の名前（日本語, English, 経度, 緯度）。旅の全体を見るときだけ出す
REGIONS = [
    ("アジア", "Asia", 100, 47),
    ("中東", "Middle East", 46, 23),
    ("アフリカ", "Africa", 19, 3),
    ("ヨーロッパ", "Europe", 32, 50),
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


def fetch_gifts():
    """trip/gifts.json の写真を取り込む。町ごとに、trip.json に入れる形で返す"""
    path = OUT / "gifts.json"
    if not path.exists():
        return {}
    sys.path.insert(0, str(ROOT / "tools"))
    from fetch_photos import get, info, save
    g = json.loads(path.read_text())
    (OUT / "gifts" / "t").mkdir(parents=True, exist_ok=True)
    out = {}
    for slug, items in g.items():
        for it in items:
            key = re.sub(r"[^a-z0-9]+", "-", Path(it["src"]).stem.lower()).strip("-")[:70]
            if len(key) < 8:   # ヘブライ語などの名前は英数字が残らないので、名前から作った符号にする
                key = (key + "-" if key else "") + hashlib.md5(it["src"].encode()).hexdigest()[:10]
            img, th = OUT / "gifts" / f"{key}.jpg", OUT / "gifts" / "t" / f"{key}.jpg"
            if not img.exists() or "author" not in it:
                url, meta = info(it["src"])
                it.update(meta)
                save(get(url), img)
                path.write_text(json.dumps(g, ensure_ascii=False, indent=1) + "\n")   # 途中で止まっても、取り込んだ分は残す
            if not th.exists():
                with Image.open(img) as im:
                    ImageOps.fit(im.convert("RGB"), (240, 240), Image.LANCZOS).save(th, quality=80, optimize=True)
            out.setdefault(slug, []).append({"ja": it["ja"], "en": it["en"], "img": f"trip/gifts/{key}.jpg", "thumb": f"trip/gifts/t/{key}.jpg",
                                             "src": it["src"], "author": it["author"], "license": it["license"], "desc": it.get("desc", "")})
    path.write_text(json.dumps(g, ensure_ascii=False, indent=1) + "\n")
    print(f"もらえる写真 {sum(len(v) for v in out.values())} 枚")
    return out


def main():
    src_dir = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    OUT.mkdir(exist_ok=True)
    stops = []
    gifts = fetch_gifts()
    for slug, ja, en, lon, lat, h, photo in STOPS:
        book, name = photo.split("/")
        img = ROOT / "books" / book / "images" / f"{name}.jpg"
        src = next((p["src"] for p in json.loads((ROOT / "books" / book / "photos.json").read_text()) if p["file"] == f"{name}.jpg"), None)
        if not img.exists() or not src:
            sys.exit(f"写真がありません: {photo}")
        thumb = OUT / f"{slug}.jpg"
        if slug != "home":
            with Image.open(img) as im:
                ImageOps.fit(im.convert("RGB"), (240, 160), Image.LANCZOS).save(thumb, quality=82, optimize=True)
        x, y = merc(lon, lat)
        country, desc = NOTES["tokyo" if slug == "home" else slug]
        stops.append({"ja": ja, "en": en, "x": round(x, 2), "y": round(y, 2), "h": h, "country": country, "desc": desc,
                      "gifts": gifts.get(slug, []), "img": f"books/{book}/images/{name}.jpg", "thumb": f"trip/{'tokyo' if slug == 'home' else slug}.jpg", "src": src})
    regions = [{"ja": ja, "en": en, "x": round(merc(lon, lat)[0], 2), "y": round(merc(lon, lat)[1], 2)} for ja, en, lon, lat in REGIONS]
    if (src_dir / "ne_50m_land.geojson").exists():
        land, lakes = path_of(src_dir / "ne_50m_land.geojson", MIN_AREA), path_of(src_dir / "ne_50m_lakes.geojson", 0.15)
    else:   # geojson がなければ、今の trip.json の地図をそのまま使う（町や写真だけ直すとき）
        old = json.loads((OUT / "trip.json").read_text())
        land, lakes = old["land"], old["lakes"]
        print("地図は今の trip.json のまま")
    data = {"stops": stops, "regions": regions, "land": land, "lakes": lakes}
    (OUT / "trip.json").write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    total = sum(s["h"] for s in stops)
    print(f"{len(stops)} 町、全部で {total} 時間、trip.json {len((OUT / 'trip.json').read_bytes()) // 1024} KB")


if __name__ == "__main__":
    main()
