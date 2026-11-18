#!/usr/bin/env python3
"""ネットワークの教科書（books/network）の図を SVG で作る。

    python3 tools/make_network_figures.py
    python3 tools/translate_figures.py network     # 英語の図（images/en/）も作り直す

箱と矢印の描き方・色は make_study_figures.py と同じものを使う。
アドレスや時間は本文の例と同じ値（例のアドレスは 192.0.2.x・203.0.113.x など、説明用のもの）。
"""
from pathlib import Path

from make_cow_figures import MUTED, S1, S2, S3, S4, S5, TEXT, TEXT2, svg, t
from make_study_figures import arrow, box

OUT = Path(__file__).resolve().parent.parent / "books" / "network" / "images"
MONO = ' font-family="ui-monospace, monospace"'
HALO = ' stroke="#ffffff" stroke-width="5" stroke-linejoin="round" paint-order="stroke"'   # 線の上に置く文字を読みやすく


def line(x1, y1, x2, y2, both=False, dash=None, head=True, width=1.6, color=TEXT2):
    ms = ' marker-start="url(#ah)"' if both else ""
    me = ' marker-end="url(#ah)"' if head else ""
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{ms}{me}{da}/>'


def area(x, y, w, h, label, color=MUTED, fill_opacity=0.0, size=12):
    """点線で囲んだ範囲と、左上の名前"""
    b = []
    if fill_opacity:
        b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{color}" opacity="{fill_opacity}"/>')
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="none" stroke="{color}" stroke-width="1.2" stroke-dasharray="6 4"/>')
    b.append(t(x + 12, y + 18, label, size, "start", TEXT2, 700))
    return b


def mono(x, y, s, size=11.5, anchor="middle", fill=TEXT, weight=None):
    return t(x, y, s, size, anchor, fill, weight, MONO)


# ---------------------------------------------------------------------------
# 1章
def fig_journey():
    b = []
    b += box(20, 34, 140, 52, "DNS サーバー", S3, "名前 → IP アドレス")
    b.append(line(90, 150, 90, 90, both=True))
    b.append(t(98, 124, "① 名前を聞く", 11.5, "start", TEXT2))
    nodes = [("ブラウザ", "スマホ・PC"), ("家のルーター", "Wi-Fi・LAN"), ("プロバイダ", "光回線・携帯"),
             ("IX・海底ケーブル", "ネットワークどうし"), ("データセンター", "CDN・サーバー")]
    xs = [20, 180, 340, 500, 660]
    for (label, sub), x in zip(nodes, xs):
        b += box(x, 150, 140, 60, label, S1 if x in (20, 660) else S2, sub, size=12.5)
    for x in xs[:-1]:
        b.append(line(x + 142, 180, x + 178, 180, both=True))
    b.append(line(240, 112, 730, 112))
    b.append(t(485, 104, "② リクエスト（HTTP）", 12, "middle", TEXT, 700))
    b.append(line(730, 242, 90, 242))
    b.append(t(410, 262, "③ レスポンス（HTML・画像）", 12, "middle", TEXT, 700))
    chapters = ["2章", "6章", "7章", "7章", "8章"]
    for x, c in zip(xs, chapters):
        b.append(t(x + 70, 228, c, 11, "middle", MUTED))
    b.append(t(410, 292, "途中は TCP/IP（4・5章）で運び、HTTPS（9章）で暗号にする", 12, "middle", TEXT2))
    return svg(820, 310, b)


def fig_layers():
    b = []
    rows = [("アプリケーション層", "HTTP・DNS・MQTT"), ("トランスポート層", "TCP・UDP"),
            ("インターネット層", "IP"), ("リンク層", "イーサネット・Wi-Fi")]
    for i, (label, sub) in enumerate(rows):
        y = 24 + i * 66
        b += box(20, y, 190, 52, label, MUTED, sub, opacity=0.10, size=12.5)
        yy = y + 8
        b += box(560, yy, 150, 36, "データ（HTTP）" if i == 0 else "データ", S1, size=12)
        if i >= 1:
            b += box(462, yy, 94, 36, "TCP ヘッダー", S2, size=11.5)
        if i >= 2:
            b += box(374, yy, 84, 36, "IP ヘッダー", S3, size=11.5)
        if i >= 3:
            b += box(270, yy, 100, 36, "MAC ヘッダー", S4, size=11.5)
            b += box(714, yy, 56, 36, "FCS", S4, size=11.5)
    b.append(line(790, 30, 790, 240))
    b.append(t(800, 140, "送る", 12, "start", TEXT, 700))
    b.append(line(240, 240, 240, 30))
    b.append(t(250, 140, "受け取る", 12, "start", TEXT, 700))
    b.append(t(410, 300, "送る側は上から順にヘッダーを付けて包み、受け取る側は下から順にはがす", 12.5, "middle", TEXT, 700))
    return svg(830, 320, b)


# ---------------------------------------------------------------------------
# 3章
def fig_dns():
    b = []
    b += box(20, 132, 130, 60, "パソコン", S1, "OS・ブラウザ")
    b += box(250, 122, 180, 80, "リゾルバー", S3, "ルーター・プロバイダ")
    b.append(t(340, 222, "答えを TTL のあいだ覚える", 11.5, "middle", TEXT2))
    b.append(line(154, 162, 246, 162, both=True))
    b.append(t(200, 152, "① 聞く", 11.5, "middle", TEXT, 700))
    b.append(t(200, 182, "⑤ 答え", 11.5, "middle", TEXT, 700))
    servers = [(24, "ルートサーバー", "「com はこのサーバーへ」", "②"),
               (132, "com のサーバー（TLD）", "「example.com はこのサーバーへ」", "③"),
               (240, "権威 DNS サーバー", "「104.20.23.154 です」", "④")]
    for y, label, sub, num in servers:
        b += box(560, y, 240, 60, label, S2, sub)
        b.append(line(434, 162, 556, y + 30, both=True))
    for (y, _, _, num), (lx, ly) in zip(servers, [(486, 98), (500, 150), (486, 220)]):
        b.append(t(lx, ly, num, 13, "middle", TEXT, 700))
    b.append(t(410, 330, "キャッシュに答えがあれば ②〜④ は飛ばして、すぐ答える", 12.5, "middle", TEXT, 700))
    return svg(820, 345, b)


# ---------------------------------------------------------------------------
# 4章
def fig_tcp():
    L, R = 230, 610
    b = [t(L, 26, "ブラウザ", 13, "middle", TEXT, 700), t(R, 26, "サーバー", 13, "middle", TEXT, 700)]
    b.append(line(L, 36, L, 400, head=False, color=MUTED))
    b.append(line(R, 36, R, 400, head=False, color=MUTED))
    msgs = [(52, True, "SYN（番号は 1000 から）"), (98, False, "SYN + ACK（1000 は受け取った。こちらは 5000 から）"),
            (144, True, "ACK（5000 も受け取った）"),
            (200, True, "データ（HTTP のリクエスト）"), (246, False, "ACK ＋ データ（レスポンス）"),
            (302, True, "FIN（終わります）"), (348, False, "ACK・FIN")]
    for y, right, label in msgs:
        x1, x2 = (L, R) if right else (R, L)
        b.append(line(x1, y, x2, y + 28))
        b.append(t((L + R) / 2, y + 8, label, 11.5, "middle", TEXT, 700, HALO))
    for y0, y1, label, color in [(48, 176, "つなぐ", S1), (196, 278, "送る", S3), (298, 380, "切る", S2)]:
        b.append(f'<rect x="20" y="{y0}" width="150" height="{y1 - y0}" rx="7" fill="{color}" opacity="0.12"/>')
        b.append(t(95, (y0 + y1) / 2 + 4, label, 13, "middle", TEXT, 700))
    b.append(t(95, 128, "3ウェイハンドシェイク", 11, "middle", TEXT2))
    b.append(t(R + 12, 116, "ここまでで1往復（RTT）", 11.5, "start", TEXT2))
    return svg(820, 410, b)


# ---------------------------------------------------------------------------
# 5章
def fig_ip_address():
    b = [mono(410, 30, "192.168.3.123/24", 20, weight=700)]
    octets = [("192", "11000000"), ("168", "10101000"), ("3", "00000011"), ("123", "01111011")]
    for i, (dec, bits) in enumerate(octets):
        x = 40 + i * 190
        color = S1 if i < 3 else S2
        b.append(f'<rect x="{x}" y="50" width="170" height="70" rx="7" fill="{color}" opacity="0.16"/>')
        b.append(f'<rect x="{x}" y="50" width="170" height="70" rx="7" fill="none" stroke="{color}" stroke-width="1.3"/>')
        b.append(mono(x + 85, 80, dec, 20, weight=700))
        b.append(mono(x + 85, 104, bits, 13, fill=TEXT2))
    b.append(f'<path d="M40 136 v8 H590 v-8" fill="none" stroke="{S1}" stroke-width="1.6"/>')
    b.append(f'<path d="M610 136 v8 H780 v-8" fill="none" stroke="{S2}" stroke-width="1.6"/>')
    b.append(t(315, 166, "ネットワーク部（24ビット）", 13, "middle", TEXT, 700))
    b.append(t(315, 186, "どのネットワークか", 12, "middle", TEXT2))
    b.append(t(695, 166, "ホスト部（8ビット）", 13, "middle", TEXT, 700))
    b.append(t(695, 186, "その中のどの機械か", 12, "middle", TEXT2))
    return svg(820, 205, b)


def fig_routing():
    b = []
    nodes = [(20, 120, "パソコン", "192.168.3.123", S1), (180, 120, "家のルーター", None, S2),
             (340, 160, "プロバイダのルーター", None, S2), (540, 110, "ルーター", "…", S2), (690, 120, "サーバー", "104.20.23.154", S1)]
    for x, w, label, sub, color in nodes:
        b += box(x, 70, w, 56, label, color, sub, size=12.5)
    gaps = [(140, 180, "TTL 64"), (300, 340, "TTL 63"), (500, 540, "TTL 62"), (650, 690, "TTL 61")]
    for x1, x2, ttl in gaps:
        b.append(line(x1 + 2, 98, x2 - 4, 98))
        b.append(mono((x1 + x2) / 2, 62, ttl, 10.5, fill=TEXT2))
    b.append(t(410, 30, "パケットのあて先は、最後までずっと 104.20.23.154", 12.5, "middle", TEXT, 700))

    def table(x, y, w, title, rows):
        out = [f'<rect x="{x}" y="{y}" width="{w}" height="{30 + 24 * len(rows)}" rx="7" fill="#ffffff" stroke="{MUTED}" stroke-width="1.2"/>',
               t(x + 10, y + 20, title, 12, "start", TEXT, 700)]
        for i, (dst, nxt) in enumerate(rows):
            out.append(mono(x + 10, y + 44 + 24 * i, dst, 11.5, "start"))
            out.append(t(x + w - 10, y + 44 + 24 * i, nxt, 11.5, "end", TEXT2))
        return out

    b.append(line(240, 128, 200, 168, head=False, dash="4 3", color=MUTED))
    b += table(20, 170, 360, "家のルーターのルーティングテーブル", [("192.168.3.0/24", "家の中へ直接"), ("その他（default）", "→ プロバイダへ")])
    b.append(line(420, 128, 520, 168, head=False, dash="4 3", color=MUTED))
    b += table(420, 170, 380, "プロバイダのルーターのルーティングテーブル", [("104.20.0.0/14", "→ となりの AS へ"), ("その他（default）", "→ 上の回線へ")])
    b.append(t(410, 282, "それぞれのルーターは「次にどこへ渡すか」だけを知っている", 12.5, "middle", TEXT, 700))
    return svg(820, 300, b)


# ---------------------------------------------------------------------------
# 6章
def fig_lan():
    b = []
    b += box(300, 30, 220, 56, "スイッチ", S3, "どのポートに、どの MAC か覚える")
    b.append(f'<rect x="560" y="20" width="250" height="100" rx="7" fill="#ffffff" stroke="{MUTED}" stroke-width="1.2"/>')
    b.append(t(572, 40, "MAC アドレステーブル", 12, "start", TEXT, 700))
    for i, (port, mac) in enumerate([("1", "dc:a6:32:12:34:56"), ("2", "dc:a6:32:ab:cd:ef"), ("4", "18:2c:a9:00:00:01")]):
        b.append(t(572, 64 + 20 * i, f"ポート {port}", 11.5, "start", TEXT2))
        b.append(mono(636, 64 + 20 * i, mac, 11.5, "start"))
    devs = [("パソコン", "192.168.3.123", S1), ("ラズパイ", "192.168.3.50", S1), ("スマホ（Wi-Fi）", "192.168.3.45", S1), ("ルーター", "192.168.3.1", S2)]
    for i, (label, ip, color) in enumerate(devs):
        x = 20 + i * 200
        b += box(x, 180, 180, 60, label, color, ip, size=12.5)
        b.append(line(410, 88, x + 90, 178, head=False))
        b.append(t(410 + (x + 90 - 410) * 0.45, 88 + 90 * 0.45 + 4, f"ポート {i + 1}", 11, "middle", TEXT2, None, HALO))
    b.append(t(110, 268, "①「192.168.3.1 の人、MAC アドレスは?」", 12, "start", TEXT, 700, ' dx="-90"'))
    b.append(t(110, 286, "（ブロードキャスト: 全員に届く）", 11.5, "start", TEXT2, None, ' dx="-90"'))
    b.append(t(800, 268, "②「私です。18:2c:a9:00:00:01」", 12, "end", TEXT, 700))
    b.append(t(800, 286, "（本人だけが答える）", 11.5, "end", TEXT2))
    return svg(820, 300, b)


# ---------------------------------------------------------------------------
# 7章
def fig_nat():
    b = []
    b += area(10, 30, 250, 230, "家の中（プライベート）", S1)
    b += box(30, 66, 210, 60, "パソコン", S1, "192.168.3.123:50001")
    b += box(30, 170, 210, 60, "スマホ", S1, "192.168.3.45:50001")
    b += box(300, 110, 160, 66, "ルーター（NAT）", S2, "外 203.0.113.45")
    b += box(650, 110, 160, 66, "サーバー", S3, "104.20.23.154:443")
    b.append(line(242, 96, 298, 130))
    b.append(line(242, 200, 298, 158))
    b.append(line(462, 136, 646, 136))
    b.append(mono(555, 112, "送り元 203.0.113.45:40001", 11))
    b.append(mono(555, 126, "送り元 203.0.113.45:40002", 11, fill=TEXT2))
    b.append(line(646, 156, 462, 156, dash="5 4"))
    b.append(t(555, 174, "返事は表を見て、元の機械へ戻す", 11.5, "middle", TEXT2))
    x, y = 300, 200
    b.append(f'<rect x="{x}" y="{y}" width="510" height="88" rx="7" fill="#ffffff" stroke="{MUTED}" stroke-width="1.2"/>')
    b.append(t(x + 12, y + 20, "NAT の表", 12, "start", TEXT, 700))
    b.append(t(x + 12, y + 42, "家の中", 11.5, "start", TEXT2))
    b.append(t(x + 300, y + 42, "外側のポート", 11.5, "start", TEXT2))
    for i, (inner, outer) in enumerate([("192.168.3.123:50001", "40001"), ("192.168.3.45:50001", "40002")]):
        b.append(mono(x + 12, y + 62 + 18 * i, inner, 11.5, "start"))
        b.append(mono(x + 300, y + 62 + 18 * i, outer, 11.5, "start"))
    return svg(820, 300, b)


def fig_internet():
    b = []
    b += box(320, 30, 180, 56, "IX", S3, "東京・大阪")
    b += box(600, 24, 210, 64, "海外のネットワーク", S5, "アメリカ・アジア・ヨーロッパ")
    b.append(line(504, 58, 596, 58, both=True, width=3))
    b.append(t(550, 44, "海底ケーブル", 11.5, "middle", TEXT, 700, HALO))
    ases = [(20, "プロバイダ A", "AS"), (200, "プロバイダ B", "AS"), (380, "携帯電話の会社", "AS"), (580, "Google・クラウド・CDN", "AS・データセンター")]
    for x, label, sub in ases:
        w = 230 if x == 580 else 160
        b += box(x, 150, w, 56, label, S2 if x < 580 else S1, sub, size=12.5)
        b.append(line(x + w / 2, 148, 410 + (x + w / 2 - 410) * 0.25, 90, both=True))
    b.append(t(20, 44, "AS どうしは BGP で", 11.5, "start", TEXT2))
    b.append(t(20, 60, "道を教え合う", 11.5, "start", TEXT2))
    b.append(line(182, 178, 198, 178, both=True))
    users = [(20, "家（光回線）"), (200, "会社"), (380, "スマホ（4G・5G）")]
    for x, label in users:
        b += box(x + 10, 260, 140, 44, label, MUTED, opacity=0.10, size=12)
        b.append(line(x + 80, 258, x + 80, 210, both=True))
    b.append(t(695, 240, "直接つなぐ（ピアリング）ことも", 11.5, "middle", TEXT2))
    b.append(t(695, 256, "上の回線を借りる（トランジット）ことも", 11.5, "middle", TEXT2))
    return svg(820, 320, b)


# ---------------------------------------------------------------------------
# 8章
def fig_server_side():
    b = []
    b += area(256, 12, 556, 232, "データセンター（クラウド）", MUTED)
    b += box(10, 100, 100, 56, "利用者", S1)
    b += box(130, 100, 110, 56, "CDN", S3, "エッジ")
    b += box(272, 100, 124, 56, "ファイアウォール", S2, "通すポートだけ", size=12.5)
    b += box(416, 100, 130, 56, "ロードバランサー", S2, "仕事を分ける", size=12.5)
    for y in (40, 103, 166):
        b += box(574, y, 108, 48, "サーバー", S1, "Web・アプリ", size=12)
        b.append(line(548, 128, 570, y + 24))
        b.append(line(684, y + 24, 700, 128))
    b += box(704, 100, 100, 56, "データベース", S4, size=12)
    b.append(line(112, 128, 126, 128))
    b.append(line(242, 128, 268, 128))
    b.append(line(398, 128, 412, 128))
    b.append(t(410, 268, "外から入れるのは決めた入り口だけ。データベースはいちばん奥に置く", 12.5, "middle", TEXT, 700))
    return svg(820, 285, b)


def fig_cdn():
    b = []
    b += box(20, 40, 150, 60, "札幌の人", S1)
    b += box(20, 190, 150, 60, "大阪の人", S1)
    b += box(300, 40, 180, 60, "東京のエッジ", S3, "写しを持っている")
    b += box(300, 190, 180, 60, "大阪のエッジ", S3, "写しを持っている")
    b += box(640, 115, 170, 60, "オリジン", S2, "アメリカのサーバー")
    for y in (70, 220):
        b.append(line(172, y, 296, y, both=True))
        b.append(t(234, y - 10, "近い（10 ms ほど）", 11.5, "middle", TEXT, 700))
    b.append(line(484, 76, 636, 136, both=True, dash="5 4"))
    b.append(line(484, 214, 636, 156, both=True, dash="5 4"))
    b.append(t(725, 84, "写しがないときだけ", 11.5, "middle", TEXT2))
    b.append(t(725, 100, "（100 ms ほど）", 11.5, "middle", TEXT2))
    b.append(t(410, 290, "ほとんどのリクエストは近くのエッジが答えるので、速く、オリジンも楽になる", 12.5, "middle", TEXT, 700))
    return svg(820, 305, b)


# ---------------------------------------------------------------------------
# 9章
def fig_tls():
    L, R = 230, 610
    b = [t(L, 26, "ブラウザ", 13, "middle", TEXT, 700), t(R, 26, "サーバー", 13, "middle", TEXT, 700)]
    b.append(f'<rect x="{L - 20}" y="196" width="{R - L + 40}" height="118" rx="8" fill="{S3}" opacity="0.12"/>')
    b.append(t(R + 30, 262, "暗号の中", 12, "start", TEXT, 700))
    b.append(line(L, 36, L, 320, head=False, color=MUTED))
    b.append(line(R, 36, R, 320, head=False, color=MUTED))
    msgs = [(50, True, "① 使える暗号・鍵交換の材料", None), (104, False, "② 暗号を決める・鍵交換の材料", "証明書・署名"),
            (206, True, "③ 終わり（ここから暗号）", None), (246, True, "④ HTTP のリクエスト", None), (282, False, "⑤ レスポンス", None)]
    for y, right, label, sub in msgs:
        x1, x2 = (L, R) if right else (R, L)
        b.append(line(x1, y, x2, y + 22))
        b.append(t((L + R) / 2, y + 4, label, 11.5, "middle", TEXT, 700, HALO))
        if sub:
            b.append(t((L + R) / 2, y + 40, sub, 11.5, "middle", TEXT2))
    b += box(20, 140, 190, 50, "証明書を確かめる", S2, "共通鍵ができる", size=12)
    b.append(t(R + 30, 90, "1往復で", 12, "start", TEXT2))
    b.append(t(R + 30, 106, "暗号が始まる", 12, "start", TEXT2))
    return svg(820, 330, b)


# ---------------------------------------------------------------------------
# 10章
def fig_cloud_models():
    layers = ["アプリ", "データ", "ランタイム（Python など）", "OS", "仮想化", "サーバー・ディスク", "ネットワーク・建物"]
    cols = [("オンプレミス", 7), ("IaaS", 4), ("PaaS", 2), ("SaaS", 0)]
    b = []
    for c, (name, mine) in enumerate(cols):
        x = 20 + c * 197
        b.append(t(x + 90, 30, name, 14, "middle", TEXT, 700))
        for i, layer in enumerate(layers):
            color = S1 if i < mine else MUTED
            b += box(x, 44 + i * 34, 180, 30, layer, color, opacity=0.18 if i < mine else 0.10, size=11.5)
    y = 300
    b.append(f'<rect x="230" y="{y}" width="16" height="16" rx="3" fill="{S1}" opacity="0.5"/>')
    b.append(t(254, y + 13, "自分でする", 12, "start", TEXT))
    b.append(f'<rect x="420" y="{y}" width="16" height="16" rx="3" fill="{MUTED}" opacity="0.5"/>')
    b.append(t(444, y + 13, "クラウドの会社がする", 12, "start", TEXT))
    return svg(820, 330, b)


# ---------------------------------------------------------------------------
# 11章
def fig_vpc():
    b = []
    b += box(330, 10, 160, 40, "インターネット", MUTED, opacity=0.12, size=12.5)
    b += area(10, 62, 800, 332, "リージョン（東京）", MUTED)
    b += area(30, 94, 760, 288, "VPC 10.0.0.0/16", S3, fill_opacity=0.04)
    b.append(line(410, 52, 410, 78, both=True))
    b += box(310, 80, 200, 30, "インターネットゲートウェイ", S3, size=12, opacity=0.25)
    for k, (x, az, pub, priv, db) in enumerate([(50, "AZ a", "10.0.1.0/24", "10.0.11.0/24", "データベース"),
                                                (420, "AZ c", "10.0.2.0/24", "10.0.12.0/24", "データベース（予備）")]):
        b += area(x, 124, 350, 246, az, MUTED)
        b.append(f'<rect x="{x + 14}" y="150" width="322" height="94" rx="8" fill="{S2}" opacity="0.10"/>')
        b.append(t(x + 326, 168, f"パブリックサブネット {pub}", 11.5, "end", TEXT, 700))
        b += box(x + 24, 178, 140, 44, "ロードバランサー", S2, size=12)
        b += box(x + 184, 178, 140, 44, "NAT ゲートウェイ", S2, size=12)
        b.append(f'<rect x="{x + 14}" y="256" width="322" height="102" rx="8" fill="{S1}" opacity="0.10"/>')
        b += box(x + 24, 268, 140, 44, "アプリのサーバー", S1, size=12)
        b += box(x + 184, 268, 140, 44, db, S1, size=12 if k == 0 else 11)
        b.append(t(x + 24, 344, f"プライベートサブネット {priv}", 11.5, "start", TEXT, 700))
        b.append(line(x + 94, 224, x + 94, 264))
        b.append(line(x + 166, 290, x + 180, 290))
        b.append(line(x + 130, 266, x + 230, 226, dash="4 3"))
        b.append(line(370 if k == 0 else 450, 112, x + 60, 174))
    b.append(t(410, 418, "外から届くのはパブリックサブネットだけ。中から外へ出るときは NAT ゲートウェイを通る", 12, "middle", TEXT, 700))
    return svg(820, 432, b)


# ---------------------------------------------------------------------------
# 12章
def fig_iot():
    b = []
    b += area(10, 20, 440, 290, "牧場", S3)
    b += area(470, 20, 200, 290, "クラウド", S1)
    sensors = [(48, "温度・湿度", "センサー"), (128, "牛の首輪", "活動量"), (208, "カメラ", "映像")]
    for y, label, sub in sensors:
        b += box(24, y, 130, 56, label, S4, sub, size=12.5)
    b += box(184, 70, 150, 60, "ゲートウェイ", S3, "LoRaWAN・BLE", size=12.5)
    b += box(184, 200, 150, 60, "Jetson（エッジ）", S3, "映像を調べる", size=12.5)
    b += box(356, 135, 84, 60, "ルーター", S2, "LTE・光", size=12.5)
    b.append(line(156, 76, 180, 94))
    b.append(line(156, 156, 180, 112))
    b.append(line(156, 236, 180, 232))
    b.append(line(336, 100, 352, 150))
    b.append(line(336, 230, 352, 182))
    b += box(490, 50, 160, 60, "MQTT ブローカー", S1, "8883（TLS）", size=12.5)
    b += box(490, 140, 160, 60, "データベース", S1, "時系列", size=12.5)
    b += box(490, 230, 160, 60, "グラフ・通知", S1, size=12.5)
    b.append(line(442, 160, 486, 86))
    b.append(t(456, 100, "MQTT", 11, "end", TEXT, 700, MONO))
    b.append(line(570, 112, 570, 136))
    b.append(line(570, 202, 570, 226))
    b += box(696, 230, 114, 60, "スマホ", S5, "見る・命令", size=12.5)
    b.append(line(652, 260, 692, 260))
    b.append(line(724, 228, 652, 86, dash="5 4"))
    b.append(t(704, 130, "命令は", 11.5, "start", TEXT2))
    b.append(t(704, 146, "ブローカー経由", 11.5, "start", TEXT2))
    b.append(t(410, 340, "機械のほうからクラウドへつなぎ、つながりを開いたままにする（NAT の後ろでも届く）", 12.5, "middle", TEXT, 700))
    return svg(820, 355, b)


FIGS = {
    "journey.svg": fig_journey, "layers.svg": fig_layers, "dns.svg": fig_dns, "tcp.svg": fig_tcp,
    "ip-address.svg": fig_ip_address, "routing.svg": fig_routing, "lan.svg": fig_lan, "nat.svg": fig_nat,
    "internet.svg": fig_internet, "server-side.svg": fig_server_side, "cdn.svg": fig_cdn, "tls.svg": fig_tls,
    "cloud-models.svg": fig_cloud_models, "vpc.svg": fig_vpc, "iot.svg": fig_iot,
}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in FIGS.items():
        (OUT / name).write_text(fn(), encoding="utf-8")
    print(f"{len(FIGS)} 枚の図を書き出しました")
