# 4. TCP and UDP (ports and reliable delivery)

An IP address (Chapter 5) only decides which computer. Inside one machine, many applications such as the browser, email and SSH are communicating at the same time. **TCP** and **UDP** in the transport layer decide which application gets the data and, when needed, deliver it "reliably and in order".

## Port numbers: which application?

A **port number** is a number from 0 to 65535 that tells the applications on one machine apart. If the IP address is the address of a building, the port number is the room number.

Server applications wait on fixed numbers (**well-known ports**, 0 to 1023).

| Port | Protocol | Use |
| --- | --- | --- |
| 22 | SSH | Log in to and control another computer (Chapter 9) |
| 53 | DNS | Look up names (Chapter 3) |
| 80 | HTTP | The web |
| 443 | HTTPS (HTTP/3 uses UDP 443) | The encrypted web |
| 25, 587 | SMTP | Send email |
| 123 | NTP | Set the clock |
| 1883, 8883 | MQTT (8883 is encrypted) | IoT devices and servers (Chapter 12) |
| 5000, 8000, 8080 | (no rule) | Often used by web servers under development |

The side that connects (such as a browser) gets a free number picked by the OS each time (an **ephemeral port**; 32768 to 60999 on Linux).

A single connection is identified by five things together: the sender's IP address and port, the receiver's IP address and port, and whether it is TCP or UDP. So however many connections one computer opens to port 443 on the same server, they never get mixed up.

```bash
ss -tn       # current TCP (t) connections, shown as numbers (n) rather than names
```

```text
State   Recv-Q  Send-Q  Local Address:Port    Peer Address:Port
ESTAB   0       0       192.168.3.123:33416   104.20.23.154:443
ESTAB   0       0       192.168.3.123:40048   185.199.108.153:443
```

The left side is you (an ephemeral port) and the right side is the other end (443 = HTTPS).

## TCP: delivering reliably and in order

**TCP** (Transmission Control Protocol) runs on top of IP, where packets may be lost or arrive out of order, and makes sure everything arrives "complete, in order and undamaged". It is used where not a single byte may be missing: the web, email, SSH, file transfers.

### The three-way handshake: greetings before data

![A TCP exchange (connect, send, close)](images/en/tcp.svg)

Before sending data, TCP sets up a **connection** with three greetings.

1. **SYN**: "I'd like to connect. My numbers start at 1000"
2. **SYN + ACK**: "Sure. I got your 1000. My numbers start at 5000"
3. **ACK**: "I got your 5000 too"

Now both sides know they can send and receive. If the other side is far away, this greeting alone costs one round trip (**RTT**).

### Numbers and ACKs: resend what was lost

- Every byte of data gets a **sequence number**. The receiver puts the data back in order using these numbers
- The receiver returns an **ACK** (acknowledgement) saying "I have received up to here"
- If no ACK arrives for a while, the sender assumes the data was lost and **retransmits** it
- The receiver says how much more it can take (the **window**), and the sender sends up to that amount without waiting for each ACK (**flow control**)
- The sender watches for signs that the network is busy (lost packets or delays) and slows itself down (**congestion control**). This stops everyone from sending too much and making things slow for all

To finish, both sides send each other a **FIN** and close.

## UDP: fire and forget, fast and light

**UDP** (User Datagram Protocol) has no greetings, no ACKs and no resending. It just adds port numbers and sends.

- No setup is needed, so it can send immediately
- Lost data is not sent again. It suits data that is useless if it arrives late anyway
- The application decides for itself what to do about losses

| | TCP | UDP |
| --- | --- | --- |
| Setup | Three-way handshake | None |
| When data is lost | Resent | Not resent |
| Order | Put in order | Not put in order |
| Speed and weight | A little heavier | Light |
| Uses | Web, email, SSH, files | DNS, video calls, online games, live streaming, setting the clock (NTP) |

In a video call, there is no point in having the picture from one second ago sent again. It is more important to keep showing the current picture, even if it glitches a little.

### QUIC: doing TCP's job on top of UDP

**QUIC**, used by HTTP/3 (Chapter 2), does its own resending and ordering on top of UDP. It combines the TCP and encryption (TLS, Chapter 9) greetings into one to save time, and it can keep a connection going when a phone switches networks.

## Try it: TCP and UDP with `nc`

With `nc` (netcat) you can send text over TCP or UDP. Try it with two terminals on the same computer (it also works between a Raspberry Pi and a PC; just replace `localhost` with the other machine's IP address).

```bash
# Terminal 1: wait on TCP port 5000
nc -l 5000

# Terminal 2: connect and send (-N closes once sending is done)
echo "hello from pc" | nc -N localhost 5000
```

`hello from pc` appears in terminal 1. For UDP, add `-u`.

```bash
nc -u -l 5001                              # terminal 1
echo "temp=21.5" | nc -u -w0 localhost 5001   # terminal 2
```

To check only whether a port on the other side is open, use `-z` (Chapter 13).

```bash
nc -zv example.com 443
```

```text
Connection to example.com (172.66.147.243) 443 port [tcp/https] succeeded!
```

## Summary

- Port numbers decide which application on a machine gets the data. Servers wait on fixed numbers (22, 53, 80, 443 and so on)
- TCP connects with a three-way handshake and uses numbers, ACKs and resending to deliver everything in order
- UDP just sends and is light. It is used for DNS, calls and games
- QUIC (HTTP/3) does TCP's job on top of UDP

## Exercises

```quiz
Q: Which port number does SSH usually use?
A: 22
E: HTTP uses 80, HTTPS 443 and DNS 53.

Q: In TCP's three greetings, what is sent first?
A: SYN
E: The order is SYN → SYN + ACK → ACK.

Q: What three-letter word is used for the message saying "I received it"?
A: ACK | acknowledgement | acknowledgment
E: If no ACK arrives for a while, the sender retransmits.

Q: Which transport-layer protocol just sends without resending?
A: UDP
E: It is used for DNS, video calls and online games.

Q: In TCP, what is the mechanism that watches how busy the network is and slows sending down?
A: congestion control
E: Matching the receiver's capacity is called flow control.
```
