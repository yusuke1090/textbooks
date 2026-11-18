# 3. DNS（名前から IP アドレスへ）

ネットワークの中で相手を決めるのは、`104.20.23.154` のような **IP アドレス**（5章）です。でも人は番号を覚えられません。そこで `example.com` のような**ドメイン名**を、IP アドレスに変える電話帳のしくみが **DNS**（Domain Name System）です。

## なぜ名前を使うのか

- 人が覚えやすい
- サーバーを引っ越して IP アドレスが変わっても、DNS を書きかえれば、名前はそのまま使える
- 1つの名前に、いくつもの IP アドレスを返せる（近いサーバーや空いているサーバーに分ける。8章）

## ドメイン名は木の形

ドメイン名は、右から左へ大きなくくりから小さなくくりになります。一番上は名前のない**ルート**（`.`）です。

```text
www.example.com.
 │     │     │  └ ルート（ふつうは書かない）
 │     │     └ トップレベルドメイン（TLD）: com・org・jp・uk など
 │     └ 持ち主が登録した名前
 └ 持ち主が自由に付ける名前（サブドメイン）
```

| TLD | 意味 |
| --- | --- |
| `.com`・`.net`・`.org` | 世界のだれでも登録できる |
| `.jp` | 日本。`co.jp`（会社）・`ac.jp`（大学）・`go.jp`（国の機関）・`or.jp`（団体）など |
| `.uk`・`.tz`・`.ke` | イギリス・タンザニア・ケニアなど、国ごと |
| `.io`・`.dev`・`.app` | 新しくできたもの。`.dev` と `.app` は HTTPS が必須 |

ドメインは、**レジストラ**（お名前.com・Cloudflare など）で、1年ごとにお金をはらって借ります。

## 名前を調べる流れ

![DNS で名前を調べる流れ](images/dns.svg)

1. パソコンやスマホの OS が、ルーターやプロバイダの **DNS サーバー**（**フルサービスリゾルバー**。キャッシュ DNS サーバーともいう）に「`www.example.com` は?」と聞く
2. リゾルバーは、手元に答えを覚えていなければ、**ルートサーバー**に聞く。ルートは「`.com` のことは `.com` のサーバーに聞いて」と教える
3. `.com` のサーバーは「`example.com` のことは、このサーバーに聞いて」と教える
4. `example.com` の**権威 DNS サーバー**（その名前の本当の答えを持っているサーバー）が「`104.20.23.154` です」と答える
5. リゾルバーは答えをパソコンに返し、決められた時間（**TTL**）のあいだ覚えておく（**キャッシュ**）

ほとんどの場合、答えはリゾルバーのキャッシュにあるので、2〜4は飛ばされ、数ミリ秒で返ってきます。

`dig +trace` で、ルートからたどる様子を見られます（Ubuntu では `sudo apt install dnsutils` で入る）。

```bash
dig +trace www.example.com
```

```text
.                 53286  IN  NS  a.root-servers.net.
.                 53286  IN  NS  m.root-servers.net.
...
com.              172800 IN  NS  a.gtld-servers.net.
...
example.com.      172800 IN  NS  hera.ns.cloudflare.com.
example.com.      172800 IN  NS  elliott.ns.cloudflare.com.
www.example.com.  300    IN  A   104.20.23.154
www.example.com.  300    IN  A   172.66.147.243
```

2列目の数字が TTL（秒）です。ルートと `.com` の情報は2日（172,800秒）、`www.example.com` の答えは5分覚えてよい、という意味です。

## ルートサーバー

ルートサーバーの名前は `a.root-servers.net` から `m.root-servers.net` までの13個です。でも機械が13台しかないわけではありません。同じ IP アドレスを世界中の千か所をこえる場所で使い（**エニーキャスト**。8章）、近い所が答えます。M のルートサーバーは、日本の WIDE プロジェクトが運用しています。

![K のルートサーバー（アムステルダムの IX、AMS-IX の中）](images/k-root.jpg)

## DNS のレコード

DNS には、名前ごとにいろいろな種類の情報（**レコード**）を置けます。

| レコード | 意味 | 例 |
| --- | --- | --- |
| **A** | IPv4 アドレス | `example.com → 104.20.23.154` |
| **AAAA** | IPv6 アドレス | `example.com → 2606:4700:10::6814:179a` |
| **CNAME** | 別の名前（あだ名）。「こっちの名前を見て」 | `www.github.com → github.com` |
| **MX** | メールを受け取るサーバー | `gmail.com → gmail-smtp-in.l.google.com` |
| **NS** | その名前の権威 DNS サーバー | `example.com → hera.ns.cloudflare.com` |
| **TXT** | 自由な文字。持ち主の確認やメールの迷惑対策に使う | `"v=spf1 …"` |

```bash
dig example.com +short          # A レコードだけ
dig AAAA example.com +short     # IPv6
dig MX gmail.com +short         # メールのサーバー
dig @8.8.8.8 example.com        # Google の DNS サーバーに聞く
```

```text
104.20.23.154
172.66.147.243
```

## 自分のパソコンの中の DNS

- `/etc/hosts` に `192.168.3.50  jetson` のように書くと、DNS に聞く前にその答えを使う（その1台だけで効く）
- Ubuntu では、`systemd-resolved` が小さなリゾルバーになっていて、アプリは `127.0.0.53` に聞く。その先のサーバーは `resolvectl status` で見られる
- 公開の DNS サーバーもある。Google の `8.8.8.8`、Cloudflare の `1.1.1.1` など
- DNS はふつう **UDP の 53番ポート**（4章）を使う。答えが大きいときは TCP。中身を暗号にする **DNS over HTTPS**（DoH）もある

## `raspberrypi.local`: LAN の中の名前（mDNS）

ラズパイや Jetson に `ssh pi@raspberrypi.local` でつなげるのは、**mDNS**（マルチキャスト DNS）のおかげです。DNS サーバーに聞くのではなく、LAN の全員に「`raspberrypi.local` はだれ?」と呼びかけ、本人が「私です」と答えます。

- Ubuntu・ラズパイ OS・Jetson では Avahi、Mac と iPhone では Bonjour が受け持つ
- `.local` で終わる名前だけ。ルーターをまたいだ別のネットワークには届かない

## DNS のトラブル

| 起きること | よくある原因 |
| --- | --- |
| IP アドレスなら `ping` できるのに、名前だとつながらない | DNS サーバーの設定がおかしい（13章） |
| DNS を書きかえたのに、古いサーバーにつながる | キャッシュ。TTL の時間がたつまで古い答えが残る。引っ越しの前に TTL を短くしておく |
| ドメインの期限が切れて、サイトもメールも止まる | 1年ごとの更新を忘れた。自動更新にしておく |

## まとめ

- DNS は、ドメイン名を IP アドレスに変える、世界で分けて持っている電話帳
- リゾルバーが、ルート → TLD → 権威 DNS サーバーの順にたどり、答えを TTL のあいだキャッシュする
- A（IPv4）・AAAA（IPv6）・CNAME（別名）・MX（メール）・NS・TXT のレコードがある
- LAN の中の `.local` の名前は mDNS で調べる

## 練習問題

```quiz
Q: ドメイン名に対応する IPv4 アドレスを書いておく DNS のレコードは何ですか。
A: A | Aレコード | A record
E: IPv6 アドレスは AAAA レコードです。

Q: DNS の答えを覚えておいてよい時間を何といいますか。アルファベット3文字で答えてください。
A: TTL | Time To Live
E: TTL の時間がたつまでは、キャッシュの答えが使われます。

Q: 名前を、ルート・TLD・権威 DNS サーバーの順にたどって調べてくれる DNS サーバーを何といいますか。
A: フルサービスリゾルバー | リゾルバー | キャッシュ DNS サーバー | resolver | full-service resolver
E: 家ではふつう、ルーターかプロバイダのものを使います。

Q: DNS がふつう使う、UDP のポート番号は何番ですか。
A: 53
E: 答えが大きいときは TCP の 53番も使います。

Q: `raspberrypi.local` のような名前を、LAN の全員に呼びかけて調べるしくみを何といいますか。
A: mDNS | マルチキャスト DNS | multicast DNS | Bonjour | Avahi
E: DNS サーバーを使わず、LAN の中だけで名前を調べます。
```
