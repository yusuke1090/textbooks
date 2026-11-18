# 13. When it won't connect

When "the internet is down" or "I can't see the Raspberry Pi's page from my PC", do not start changing settings on a hunch. Check **from the bottom layer up**. Climb the layers from Chapter 1 one step at a time and you will find where things stop.

![Tangled cables](images/tangled-cables.jpg)

## Check from the bottom up

| Step (what to check) | Command |
| --- | --- |
| 1. Cable or radio (the cable is plugged in / Wi-Fi is connected) | `ip -br link` |
| 2. IP address (you have a proper IP address) | `ip -br addr` |
| 3. Gateway (you can reach the home router) | `ping -c 3 192.168.3.1` |
| 4. Internet (you can reach an outside IP address) | `ping -c 3 8.8.8.8` |
| 5. DNS (names can be looked up) | `dig example.com` |
| 6. Port (the other side's port is open) | `nc -zv example.com 443` |
| 7. Application (the application answers properly) | `curl -v https://example.com/` |

### 1. Cable or radio

```bash
ip -br link
```

```text
lo        UNKNOWN  00:00:00:00:00:00 <LOOPBACK,UP,LOWER_UP>
enp2s0    DOWN     dc:a6:32:12:34:57 <NO-CARRIER,BROADCAST,MULTICAST,UP>
wlp3s0    UP       dc:a6:32:12:34:56 <BROADCAST,MULTICAST,UP,LOWER_UP>
```

`NO-CARRIER` means nothing is coming down the cable (not plugged in, the other end is switched off, or the cable is broken). You can see Wi-Fi signal strength as `SIGNAL` (0–100) in `nmcli dev wifi`.

### 2. IP address

```bash
ip -br addr
```

| What you see | Meaning |
| --- | --- |
| `192.168.3.123/24` or similar | You have one. Go to the next step |
| `169.254.x.x` | No DHCP answer, so the machine gave itself an address (Chapter 5). The router is not answering |
| Nothing | Not connected (go back to step 1), or the DHCP lease has run out |

### 3–4. Gateway and internet

If you can reach the gateway but not `8.8.8.8`, the problem is outside your home router. Check the lights on the router and ONU and your ISP's outage information. `tracepath -n 8.8.8.8` (Chapter 5) shows where things stop.

### 5. DNS

If `ping 8.8.8.8` works but `ping example.com` says `Temporary failure in name resolution`, it is DNS.

```bash
dig example.com              # ask the usual DNS server
dig @1.1.1.1 example.com     # try asking a different DNS server
resolvectl status            # the DNS servers in use now
```

If a different DNS server answers, the problem is your usual DNS server (the router's or the ISP's).

### 6–7. Ports and applications

```bash
nc -zv example.com 443                 # succeeded! means the port is open
curl -v https://example.com/ -o /dev/null
```

| What you get | Meaning |
| --- | --- |
| `Connection refused` | It reached the other side, but no application is waiting on that port |
| Nothing comes back until it times out | A firewall on the way is dropping it, or it is not reaching the other side |
| Certificate error | The clock is wrong, the name does not match, or it has expired (Chapter 9) |
| 4xx or 5xx | Communication works. The problem is how you asked, or inside the server (Chapter 2) |

## A server on a Raspberry Pi or Jetson cannot be seen from the PC

A common cause is that the server is only waiting inside the machine itself (`127.0.0.1`). Check with `ss` on the Raspberry Pi.

```bash
ss -tlnp      # listening (l) TCP sockets, with process names (p)
```

```text
State   Recv-Q  Send-Q  Local Address:Port   Peer Address:Port  Process
LISTEN  0       128         127.0.0.1:5000        0.0.0.0:*     users:(("python3",pid=812,fd=3))
LISTEN  0       128           0.0.0.0:22          0.0.0.0:*     users:(("sshd",pid=401,fd=3))
```

- `127.0.0.1:5000` can only be reached from inside the Raspberry Pi. To accept connections from outside too, start the server waiting on `0.0.0.0` (for Flask, `flask run --host 0.0.0.0`; for Python's simple server, `python3 -m http.server 8000 --bind 0.0.0.0`)
- `0.0.0.0:22` accepts from anywhere. SSH is set up this way

Other things to check:

- Whether a firewall is blocking it (`sudo ufw status`, Chapter 8)
- For a Docker container, whether the port is published with `-p 5000:5000` ([Docker Textbook](https://yusuke1090.github.io/textbooks/?b=docker))
- Whether the PC and Raspberry Pi are on the same network (is the network part the same in `ip -br addr`? Shop Wi-Fi and guest Wi-Fi are sometimes set up so that devices cannot talk to each other)

## Looking at the packets themselves: tcpdump and Wireshark

When you really cannot work it out, look at the packets that are flowing.

```bash
sudo tcpdump -n -i any port 53      # watch only DNS questions and answers
sudo tcpdump -n -i any host 192.168.3.50 and port 1883   # MQTT with the Raspberry Pi
```

For a graphical view, **Wireshark** (`sudo apt install wireshark`) is handy. It colors each protocol and lets you step through the TCP three-way handshake (Chapter 4) and the TLS greeting (Chapter 9) just as this book described them. Use it only on your own networks.

## When it is slow

| What to check | How |
| --- | --- |
| Line speed | A speed test site in the browser. Compare wired and Wi-Fi |
| Speed inside the LAN | Install `iperf3` on two machines; run `iperf3 -s` on one and `iperf3 -c <other machine's IP address>` on the other |
| Latency and lost packets | `mtr 8.8.8.8` (which router it gets slow from) |
| Wi-Fi signal | `SIGNAL` in `nmcli dev wifi`. Move closer to the router or use 5 GHz |
| Slow only in the evening | On Japanese fiber, it may be PPPoE congestion. Check for IPoE (Chapter 7) |

## Summary

- Check from the bottom up: cable or radio → IP address → gateway → internet → DNS → port → application
- `169.254.x.x` means DHCP failed, `Temporary failure in name resolution` means DNS, and `Connection refused` means no application is waiting on the port
- For a server that cannot be seen from outside, use `ss -tlnp` to check it is not waiting on `127.0.0.1`
- If you really cannot work it out, look at the packets themselves with tcpdump or Wireshark

## Exercises

```quiz
Q: `ip -br addr` shows an address starting with `169.254.`. Which four-letter system is not working?
A: DHCP
E: The machine could not get an address from the router and gave itself one.

Q: `ping 8.8.8.8` works but `ping example.com` does not. What three-letter system do you suspect?
A: DNS
E: You can reach IP addresses, so the problem is looking up names.

Q: What error appears when the packet reached the other side but no application is waiting on that port?
| nc -zv 192.168.3.50 5000
A: Connection refused | refused
E: If nothing comes back until it times out, a firewall on the way is usually dropping it.

Q: On a Raspberry Pi, `ss -tlnp` shows the server waiting on `127.0.0.1:5000`. Which address should it wait on to accept connections from outside too?
A: 0.0.0.0
E: `0.0.0.0` means "accept from every network".

Q: What command-line tool shows the packets that are flowing?
A: tcpdump | Wireshark | tshark
E: For a graphical view, Wireshark is handy.
```
