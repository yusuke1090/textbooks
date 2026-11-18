# 3. DNS (from names to IP addresses)

Inside the network, the other side is identified by an **IP address** (Chapter 5) such as `104.20.23.154`. But people cannot remember numbers. **DNS** (Domain Name System) is the phone book that turns **domain names** such as `example.com` into IP addresses.

## Why use names?

- They are easy for people to remember
- If a server moves and its IP address changes, you just update DNS and the name keeps working
- One name can return several IP addresses (to spread users over nearby or less busy servers, Chapter 8)

## Domain names form a tree

A domain name goes from big groups on the right to small groups on the left. At the very top is the unnamed **root** (`.`).

```text
www.example.com.
 │     │     │  └ root (usually not written)
 │     │     └ top-level domain (TLD): com, org, jp, uk and so on
 │     └ the name the owner registered
 └ a name the owner chooses freely (subdomain)
```

| TLD | Meaning |
| --- | --- |
| `.com`, `.net`, `.org` | Anyone in the world can register |
| `.jp` | Japan. `co.jp` (companies), `ac.jp` (universities), `go.jp` (government), `or.jp` (organizations) and so on |
| `.uk`, `.tz`, `.ke` | One per country: the UK, Tanzania, Kenya and so on |
| `.io`, `.dev`, `.app` | Newer ones. `.dev` and `.app` require HTTPS |

You rent a domain from a **registrar** (such as Onamae.com or Cloudflare), paying every year.

## How a name is looked up

![How DNS looks up a name](images/en/dns.svg)

1. The OS on your computer or phone asks a **DNS server** at your router or ISP (a **full-service resolver**, also called a caching DNS server): "What is `www.example.com`?"
2. If the resolver does not already know the answer, it asks a **root server**. The root says: "For `.com`, ask the `.com` servers"
3. The `.com` server says: "For `example.com`, ask this server"
4. The **authoritative DNS server** for `example.com` (the server that holds the real answer for that name) replies: "It is `104.20.23.154`"
5. The resolver returns the answer to your computer and remembers it for a set time (the **TTL**), in its **cache**

Most of the time the answer is already in the resolver's cache, so steps 2 to 4 are skipped and the answer comes back in a few milliseconds.

`dig +trace` shows the lookup starting from the root (on Ubuntu, install it with `sudo apt install dnsutils`).

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

The number in the second column is the TTL in seconds. The root and `.com` information may be kept for two days (172,800 seconds), and the answer for `www.example.com` for five minutes.

## Root servers

The root servers are named `a.root-servers.net` to `m.root-servers.net`, thirteen names in all. That does not mean there are only thirteen machines. The same IP addresses are used at more than a thousand places around the world (**anycast**, Chapter 8), and the nearest one answers. The M root server is run by the WIDE Project in Japan.

![The K root server (inside AMS-IX, the internet exchange in Amsterdam)](images/k-root.jpg)

## DNS records

DNS can hold different kinds of information (**records**) for each name.

| Record | Meaning | Example |
| --- | --- | --- |
| **A** | IPv4 address | `example.com → 104.20.23.154` |
| **AAAA** | IPv6 address | `example.com → 2606:4700:10::6814:179a` |
| **CNAME** | Another name (an alias): "look at this name instead" | `www.github.com → github.com` |
| **MX** | The server that receives email | `gmail.com → gmail-smtp-in.l.google.com` |
| **NS** | The authoritative DNS servers for the name | `example.com → hera.ns.cloudflare.com` |
| **TXT** | Free text. Used to prove ownership and fight spam | `"v=spf1 …"` |

```bash
dig example.com +short          # only the A records
dig AAAA example.com +short     # IPv6
dig MX gmail.com +short         # mail servers
dig @8.8.8.8 example.com        # ask Google's DNS server
```

```text
104.20.23.154
172.66.147.243
```

## DNS inside your computer

- If you write a line such as `192.168.3.50  jetson` in `/etc/hosts`, that answer is used before asking DNS (it works only on that one machine)
- On Ubuntu, `systemd-resolved` acts as a small resolver, and applications ask `127.0.0.53`. You can see which servers it uses next with `resolvectl status`
- There are public DNS servers too, such as Google's `8.8.8.8` and Cloudflare's `1.1.1.1`
- DNS usually uses **UDP port 53** (Chapter 4), and TCP when the answer is large. **DNS over HTTPS** (DoH) also encrypts the contents

## `raspberrypi.local`: names inside the LAN (mDNS)

You can connect with `ssh pi@raspberrypi.local` thanks to **mDNS** (multicast DNS). Instead of asking a DNS server, your computer calls out to everyone on the LAN, "Who is `raspberrypi.local`?", and that machine answers, "Me."

- Avahi handles it on Ubuntu, Raspberry Pi OS and Jetson; Bonjour on Mac and iPhone
- It works only for names ending in `.local`, and does not reach other networks across a router

## DNS trouble

| What happens | Common cause |
| --- | --- |
| You can `ping` the IP address but not the name | The DNS server settings are wrong (Chapter 13) |
| You changed DNS but still reach the old server | The cache. Old answers remain until the TTL runs out. Shorten the TTL before moving |
| The domain expires and the site and email stop | Someone forgot the yearly renewal. Turn on auto-renew |

## Summary

- DNS is the world's shared phone book that turns domain names into IP addresses
- A resolver follows root → TLD → authoritative DNS server and caches the answer for the TTL
- There are A (IPv4), AAAA (IPv6), CNAME (alias), MX (mail), NS and TXT records
- Names ending in `.local` inside the LAN are looked up with mDNS

## Exercises

```quiz
Q: Which DNS record holds the IPv4 address for a domain name?
A: A | A record
E: IPv6 addresses go in AAAA records.

Q: What is the three-letter name for how long a DNS answer may be remembered?
A: TTL | Time To Live
E: Until the TTL runs out, the answer from the cache is used.

Q: What is the DNS server called that follows root, TLD and authoritative servers to look up a name for you?
A: full-service resolver | resolver | caching DNS server | recursive resolver
E: At home you usually use the one in your router or at your ISP.

Q: Which UDP port number does DNS usually use?
A: 53
E: TCP port 53 is also used when the answer is large.

Q: What is the system that looks up names such as `raspberrypi.local` by calling out to everyone on the LAN?
A: mDNS | multicast DNS | Bonjour | Avahi
E: It looks up names only inside the LAN, without a DNS server.
```
