# Appendix A. Glossary (English and Japanese)

Words used in this book with their Japanese equivalents. Numbers in brackets show the chapter with more detail.

## The big picture

| English | Japanese | Reading | Meaning |
| --- | --- | --- | --- |
| network | ネットワーク | | Computers joined so they can exchange data (Ch. 1) |
| internet | インターネット | | The world's networks joined with the same protocols (Ch. 1) |
| protocol | プロトコル | | The agreed rules for connecting (Ch. 1) |
| packet | パケット | | A small piece of data with a header (Ch. 1) |
| header | ヘッダー | | The part in front of the data holding the destination and so on (Ch. 1) |
| layer | 階層 | かいそう | The work of a network divided by role (Ch. 1) |
| encapsulation | カプセル化 | かぷせるか | Wrapping data in headers from the top layer down (Ch. 1) |
| OSI reference model | OSI 参照モデル | おーえすあいさんしょうもでる | A way of dividing the work of a network into seven layers (Ch. 1) |

## The web and DNS

| English | Japanese | Reading | Meaning |
| --- | --- | --- | --- |
| request | リクエスト | | The message a browser or app sends to a server (Ch. 2) |
| response | レスポンス | | The answer a server sends back (Ch. 2) |
| method | メソッド | | The kind of request, such as GET or POST (Ch. 2) |
| status code | ステータスコード | | A three-digit number showing the result of a response, such as 200 or 404 (Ch. 2) |
| cookie | Cookie | くっきー | A value the server has the browser remember and send back every time (Ch. 2) |
| web API | Web API | うぇぶえーぴーあい | An entrance through which apps use each other's features over HTTP (Ch. 2) |
| domain name | ドメイン名 | どめいんめい | A name such as `example.com` used instead of an IP address (Ch. 3) |
| resolver | リゾルバー | | A DNS server that looks up names for you (Ch. 3) |
| authoritative DNS server | 権威 DNS サーバー | けんいでぃーえぬえすさーばー | The DNS server that holds the real answer for a name (Ch. 3) |
| root server | ルートサーバー | | A server at the top of the DNS tree (Ch. 3) |
| cache | キャッシュ | | Keeping an answer you got once for a while (Ch. 3) |
| record | レコード | | Information held in DNS, such as A, AAAA, CNAME and MX (Ch. 3) |

## TCP/IP

| English | Japanese | Reading | Meaning |
| --- | --- | --- | --- |
| port number | ポート番号 | ぽーとばんごう | A number that tells the applications on a machine apart (Ch. 4) |
| well-known port | ウェルノウンポート | | A fixed number that servers wait on, 0–1023 (Ch. 4) |
| connection | コネクション | | The link between two machines set up by TCP (Ch. 4) |
| three-way handshake | 3ウェイハンドシェイク | すりーうぇいはんどしぇいく | TCP's three greetings: SYN, SYN+ACK, ACK (Ch. 4) |
| retransmission | 再送 | さいそう | Sending lost data again (Ch. 4) |
| congestion control | 輻輳制御 | ふくそうせいぎょ | Slowing down to match how busy the network is (Ch. 4) |
| IP address | IP アドレス | あいぴーあどれす | An address on the network (Ch. 5) |
| subnet | サブネット | | A group of IP addresses with the same network part (Ch. 5) |
| subnet mask | サブネットマスク | | A number showing where the network part and host part divide (Ch. 5) |
| private IP address | プライベート IP アドレス | ぷらいべーとあいぴーあどれす | An address free to use inside homes and companies (Ch. 5) |
| global IP address / public IP address | グローバル IP アドレス | ぐろーばるあいぴーあどれす | An address unique in the world, used on the internet (Ch. 5) |
| router | ルーター | | A machine that reads a packet's destination and passes it on (Ch. 5) |
| routing table | ルーティングテーブル | | A router's table of where to send each destination (Ch. 5) |
| default gateway | デフォルトゲートウェイ | | The router you hand packets to first when leaving your own network (Ch. 5) |
| loopback | ループバック | | The address meaning the machine itself, 127.0.0.1 (Ch. 5) |

## The LAN and lines

| English | Japanese | Reading | Meaning |
| --- | --- | --- | --- |
| Ethernet | イーサネット | | Wired LAN using LAN cables (Ch. 6) |
| MAC address | MAC アドレス | まっくあどれす | A 48-bit address that tells machines apart on a LAN (Ch. 6) |
| frame | フレーム | | One unit sent over Ethernet (Ch. 6) |
| switch | スイッチ | | A machine that learns MAC addresses and sends only to the port needed (Ch. 6) |
| broadcast | ブロードキャスト | | Sending to everyone on the same network (Ch. 6) |
| access point | アクセスポイント | | The base unit that sends out the Wi-Fi signal (Ch. 6) |
| fiber-optic line / FTTH | 光回線 | ひかりかいせん | A line with optical fiber all the way to the house (Ch. 7) |
| optical fiber | 光ファイバー | ひかりふぁいばー | A thin glass thread that light travels through (Ch. 7) |
| internet service provider / ISP | プロバイダ | | A company that sells internet connections (Ch. 7) |
| base station / cell tower | 基地局 | きちきょく | The antennas and equipment that send out mobile signals (Ch. 7) |
| submarine cable / undersea cable | 海底ケーブル | かいていけーぶる | Optical fiber laid on the sea floor to link countries (Ch. 7) |
| cable landing station | 陸揚げ局 | りくあげきょく | Where an undersea cable comes ashore (Ch. 7) |
| bandwidth | 帯域 | たいいき | How much data can be carried per second (Ch. 7) |
| latency | 遅延 | ちえん | The time to go and come back (Ch. 7) |
| port forwarding | ポートフォワーディング | | A setting that passes traffic arriving at an outside port to a machine inside (Ch. 7) |

## Servers and security

| English | Japanese | Reading | Meaning |
| --- | --- | --- | --- |
| data center | データセンター | | A building holding thousands of servers (Ch. 8) |
| firewall | ファイアウォール | | A checkpoint that lets through only traffic matching its rules (Ch. 8) |
| load balancer | ロードバランサー | | A machine that shares work among many servers (Ch. 8) |
| health check | ヘルスチェック | | Regularly checking that a server is working (Ch. 8) |
| edge | エッジ | | A CDN server placed near users (Ch. 8) |
| origin | オリジン | | The original server behind a CDN (Ch. 8) |
| anycast | エニーキャスト | | Using the same IP address in many places so the nearest is reached (Ch. 8) |
| encryption | 暗号 | あんごう | Making contents unreadable without the key (Ch. 9) |
| public key | 公開鍵 | こうかいかぎ | A key that can be shown to anyone (Ch. 9) |
| private key | 秘密鍵 | ひみつかぎ | A key only you hold (Ch. 9) |
| digital signature | 電子署名 | でんししょめい | A mark showing something is genuine and unchanged (Ch. 9) |
| certificate | 証明書 | しょうめいしょ | A certificate authority's guarantee that a site's public key is genuine (Ch. 9) |
| certificate authority / CA | 認証局 | にんしょうきょく | An organization that issues certificates (Ch. 9) |
| key exchange | 鍵交換 | かぎこうかん | Safely making a shared key that only the two sides know (Ch. 9) |
| two-factor authentication | 二要素認証 | にようそにんしょう | Checking identity with something besides the password (Ch. 9) |

## The cloud and IoT

| English | Japanese | Reading | Meaning |
| --- | --- | --- | --- |
| cloud | クラウド | | Renting computers in data centers over the internet (Ch. 10) |
| on-premises | オンプレミス | | Owning servers and keeping them at your own site (Ch. 10) |
| region | リージョン | | An area where a cloud company has data centers (Ch. 10) |
| availability zone | アベイラビリティゾーン | | A group of data centers inside a region with separate power and lines (Ch. 10) |
| egress | エグレス | | Data transferred out of the cloud (Ch. 10) |
| shared responsibility model | 責任共有モデル | せきにんきょうゆうもでる | Dividing what the cloud company and the renter each protect (Ch. 10) |
| security group | セキュリティグループ | | A per-server firewall in the cloud (Ch. 11) |
| serverless | サーバーレス | | Asking for work in units without preparing servers (Ch. 11) |
| cold start | コールドスタート | | The slow first start of a function that has not been used for a while (Ch. 11) |
| gateway | ゲートウェイ | | A machine at the entrance between networks. In IoT, it passes sensor data on to the internet (Ch. 12) |
| broker | ブローカー | | The server in the middle that delivers MQTT messages (Ch. 12) |
| topic | トピック | | A name split by `/` attached to MQTT messages (Ch. 12) |
| publish | パブリッシュ | | Sending a message to a topic in MQTT (Ch. 12) |
| subscribe | サブスクライブ | | Signing up to receive a topic's messages in MQTT (Ch. 12) |
| edge computing | エッジコンピューティング | | Processing data on the spot before sending it to the cloud (Ch. 12) |

## Abbreviations

| English | Japanese | Reading | Meaning |
| --- | --- | --- | --- |
| LAN (local area network) | LAN | らん | A network inside a home or company |
| WAN (wide area network) | WAN | わん | A network linking distant places |
| HTTP (HyperText Transfer Protocol) | HTTP | えいちてぃーてぃーぴー | The rules for exchanges on the web (Ch. 2) |
| URL (Uniform Resource Locator) | URL | ゆーあーるえる | Text showing where data is (Ch. 2) |
| DNS (Domain Name System) | DNS | でぃーえぬえす | The system that turns names into IP addresses (Ch. 3) |
| TTL (time to live) | TTL | てぃーてぃーえる | In DNS, how long an answer may be kept; in IP, how many routers a packet may pass (Ch. 3, 5) |
| TCP (Transmission Control Protocol) | TCP | てぃーしーぴー | A protocol that delivers reliably and in order (Ch. 4) |
| UDP (User Datagram Protocol) | UDP | ゆーでぃーぴー | A light protocol that just sends (Ch. 4) |
| QUIC | QUIC | くいっく | The protocol of HTTP/3, running on UDP (Ch. 4) |
| ICMP (Internet Control Message Protocol) | ICMP | あいしーえむぴー | IP's messaging protocol, used by ping (Ch. 5) |
| ARP (Address Resolution Protocol) | ARP | あーぷ | A protocol that finds the MAC address for an IP address (Ch. 6) |
| MTU (maximum transmission unit) | MTU | えむてぃーゆー | The most data that can be sent in one go (Ch. 6) |
| DHCP (Dynamic Host Configuration Protocol) | DHCP | でぃーえいちしーぴー | Automatically hands out IP addresses and more (Ch. 7) |
| NAT (network address translation) | NAT | なっと | Rewriting addresses and ports so many machines share one address (Ch. 7) |
| CGNAT (carrier-grade NAT) | CGNAT | しーじーなっと | NAT used by carriers to share one address among many homes (Ch. 7) |
| AS (autonomous system) | AS | えーえす | A block of networks run by one organization (Ch. 7) |
| BGP (Border Gateway Protocol) | BGP | びーじーぴー | The protocol ASes use to share routes (Ch. 7) |
| IX (internet exchange) | IX | あいえっくす | A place where many ASes meet and connect (Ch. 7) |
| CDN (content delivery network) | CDN | しーでぃーえぬ | A system that returns copies from near the user (Ch. 8) |
| TLS (Transport Layer Security) | TLS | てぃーえるえす | A protocol that encrypts communication (Ch. 9) |
| SSH (Secure Shell) | SSH | えすえすえいち | A protocol for controlling another computer safely (Ch. 9) |
| VPN (virtual private network) | VPN | ぶいぴーえぬ | Your own network built on top of the internet (Ch. 9) |
| IaaS (infrastructure as a service) | IaaS | いあーす | Renting virtual servers and the like (Ch. 10) |
| PaaS (platform as a service) | PaaS | ぱーす | Renting a place to run applications (Ch. 10) |
| SaaS (software as a service) | SaaS | さーす | Using finished applications (Ch. 10) |
| VPC (virtual private cloud) | VPC | ぶいぴーしー | Your own network inside the cloud (Ch. 11) |
| IoT (Internet of Things) | IoT | あいおーてぃー | Connecting sensors and machines to the internet (Ch. 12) |
| MQTT | MQTT | えむきゅーてぃーてぃー | A publish/subscribe protocol for IoT (Ch. 12) |
