# 9. Connecting safely (HTTPS, SSH, VPN)

Packets pass through many machines that belong to other people: café Wi-Fi, ISPs, IXes and undersea cables. Left as they are, they might be read, changed or answered by a fake server on the way. Encryption prevents this.

## Three things to protect

| Worry | Protection | Mechanism |
| --- | --- | --- |
| Being **read** on the way | Encrypt the contents | Symmetric-key encryption |
| Being **changed** on the way | Add a mark that shows any change | Message authentication codes |
| Connecting to a **fake** | Check the other side is genuine | Certificates and digital signatures |

## Two kinds of keys

- **Symmetric-key encryption**: the same key encrypts and decrypts. It is fast, so the data itself is encrypted this way (AES and others). The problem is how to hand the key safely to the other side
- **Public-key encryption**: uses a pair of keys (a **public key** and a **private key**). The public key can be shown to anyone. A **digital signature** made with the private key can be checked with the public key

In TLS (below), the public-key system is used to check the other side while the two sides make a one-time shared key together (**key exchange**). After that, everything goes through fast symmetric-key encryption.

## HTTPS and TLS

**HTTPS** is HTTP encrypted with **TLS**. Today almost all of the web is HTTPS.

![The TLS greeting (TLS 1.3)](images/en/tls.svg)

1. Browser: "I'd like to connect. These are the ciphers I can use. Here is my part for the key exchange"
2. Server: "Let's use this cipher. Here is my part for the key exchange, my **certificate** and a signature"
3. The browser checks that the certificate is genuine and that the name matches the URL it opened. Both sides now make the same shared key from the two parts
4. From here on, everything is encrypted, and the HTTP exchange takes place

In TLS 1.3 this greeting is finished in a single round trip.

### Certificates and certificate authorities

A **certificate** says "the public key for `example.com` is this one", signed and guaranteed by a **certificate authority** (CA).

- The certificate authorities' own certificates (**root certificates**) come built into the OS and browser. Checking follows the signatures "root → intermediate authority → site"
- **Let's Encrypt** is a certificate authority that issues certificates for free. They are currently valid for 90 days and are renewed automatically. GitHub Pages uses it too
- When a certificate expires, the browser shows a big warning

`curl -v` shows the certificate and the result of the greeting.

```bash
curl -v -o /dev/null https://yusuke1090.github.io/textbooks/
```

```text
* SSL connection using TLSv1.3 / TLS_AES_128_GCM_SHA256 / X25519MLKEM768 / RSASSA-PSS
* ALPN: server accepted h2
* Server certificate:
*   subject: CN=*.github.io
*   start date: Sep 30 23:44:46 2026 GMT
*   expire date: Dec 29 23:44:45 2026 GMT
*   issuer: C=US; O=Let's Encrypt; CN=YR1
*   subjectAltName: "yusuke1090.github.io" matches cert's "*.github.io"
```

- With `TLSv1.3`, the data is encrypted with `AES_128_GCM` (symmetric-key encryption). The key exchange `X25519MLKEM768` is strengthened so that even future quantum computers cannot break it
- The certificate is for `*.github.io` (any name under github.io), issued by Let's Encrypt for 90 days
- `h2` means they agreed to speak HTTP/2

### The padlock does not mean "a safe site"

The padlock in the address bar only means "nobody on the way can read this" and "you are connected to the real server for this domain". A fake site (phishing) also gets a padlock if it gets a certificate for its own domain. It is important to check yourself that the domain name is right.

## SSH: controlling another computer safely

**SSH** is the protocol for logging in to a computer across the network and typing commands (port 22). It is used to work on a Raspberry Pi, a Jetson or a cloud server. Everything exchanged is encrypted.

```bash
ssh pi@raspberrypi.local
```

- The first time you connect, it asks "this server's key fingerprint is SHA256:…. Continue?" If you say yes, it remembers the key in `~/.ssh/known_hosts` and warns you next time if the key has changed (to catch fake servers)
- Use **public-key authentication** (a key made with `ssh-keygen`) rather than a password. Making the key is the same as in Chapter 3 of the [GitHub Textbook](https://yusuke1090.github.io/textbooks/?b=github)
- If the machine can be seen from outside, turn off password login (`PasswordAuthentication no` in `/etc/ssh/sshd_config`)

### Port forwarding: an SSH tunnel

You can also pass other traffic through an SSH connection. For example, you can view a web page that only runs inside the Raspberry Pi (port 80) in the browser on your own computer.

```bash
ssh -L 8080:localhost:80 pi@raspberrypi.local
# open http://localhost:8080 in your browser to see port 80 on the Raspberry Pi
```

## VPN: your own network on top of the internet

A **VPN** (Virtual Private Network) builds an encrypted tunnel across the internet and connects distant machines as if they were on the same LAN.

| Use | Example |
| --- | --- |
| Getting into the office network from home | Using company servers and files |
| Protection on outside Wi-Fi | Using café Wi-Fi through your home or company network |
| Bringing distant machines into your own network | SSH to the Jetson on the farm or the Raspberry Pi at home from anywhere |

- **WireGuard** is a newer, fast VPN with short settings. It is built into Linux
- **Tailscale** is a service that uses WireGuard to connect your own machines to each other automatically. It reaches machines behind NAT or on mobile networks (CGNAT, Chapter 7) without port forwarding. Each machine gets a `100.x.y.z` address

## Security basics

- Keep the software on your OS and router up to date (`sudo apt update && sudo apt upgrade`)
- Always change default passwords (routers, cameras, Raspberry Pi)
- Open as few ports to the outside as possible (the firewall in Chapter 8). Allow SSH with public keys only, or only from inside a VPN
- For important services, check identity with something besides the password, such as a phone app (**two-factor authentication**)

## Summary

- Encryption prevents reading, changing and faking. Data uses a symmetric key; checking the other side and exchanging keys use public-key methods
- HTTPS is HTTP encrypted with TLS. Certificate authorities vouch for certificates. The padlock does not mean "the site is safe"
- SSH lets you control another computer safely. `-L` makes a tunnel
- A VPN brings distant machines into your own network (WireGuard, Tailscale)

## Exercises

```quiz
Q: Which three-letter protocol is used to encrypt HTTP?
A: TLS | SSL | SSL/TLS
E: HTTPS is HTTP over TLS. Its older name was SSL.

Q: What is the organization that signs to guarantee that a site's public key is genuine?
A: certificate authority | CA
E: Certificate authorities' root certificates come built into the OS and browser.

Q: What is the name of the well-known certificate authority that issues certificates for free?
A: Let's Encrypt | Lets Encrypt
E: Certificates are valid for 90 days and renewed automatically.

Q: Which SSH option makes a tunnel from local port 8080 to port 80 on the remote machine?
| ssh ??? 8080:localhost:80 pi@raspberrypi.local
A: -L
E: It forwards a local port, so it is -L.

Q: What is the system that builds an encrypted tunnel across the internet and connects distant machines as if they were on the same LAN?
A: VPN | Virtual Private Network
E: WireGuard and Tailscale are examples.
```
