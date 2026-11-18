# 6. The LAN (Ethernet and Wi-Fi)

The IP address decides where a packet is going, but electricity or radio only carries it as far as the next machine. Inside a home or office **LAN**, packets are carried to the next machine by wired **Ethernet** and wireless **Wi-Fi**.

## Ethernet (wired LAN)

![A LAN cable with an RJ45 connector](images/lan-cable.jpg)

**Ethernet** is a wired LAN connected with LAN cables. The square connector at the end is called **RJ45**. One cable can be up to 100 m long, and its type (category) decides how fast it can go.

| Category | Speed | Use |
| --- | --- | --- |
| Cat5e | 1 Gbps | Enough for an ordinary home |
| Cat6 | 1 Gbps (10 Gbps if short) | When you want some headroom |
| Cat6A | 10 Gbps | 10 Gbps fiber lines and servers |

With **PoE** (Power over Ethernet), which also sends power down the LAN cable, you can power barn cameras or ceiling Wi-Fi units without a socket.

## MAC addresses: names for the next machine

Machines on a LAN are told apart by their **MAC address**. It is a 48-bit number written in hexadecimal, like `dc:a6:32:12:34:56`. Each network part (a LAN port or Wi-Fi chip) gets one at the factory.

- The first half (`dc:a6:32`) identifies the maker. `dc:a6:32` is the Raspberry Pi company
- An IP address changes with where you are, but a MAC address goes with the part
- iPhones and Android phones use a random MAC address for each Wi-Fi network ("private Wi-Fi address") so nobody can track where they have been

### Frames

One unit sent over Ethernet is called a **frame**. It is an IP packet wrapped in a header with MAC addresses.

```text
| destination MAC | source MAC | type (IPv4 etc.) | data (the IP packet, up to 1,500 bytes) | error check |
```

The largest amount of data that fits in one go (1,500 bytes) is called the **MTU**.

## Switches: sending only to the right port

![A switch and ARP](images/en/lan.svg)

A **switch** is a box that connects many LAN cables. Every time a frame arrives, it notes "this MAC address is on port so-and-so" (the **MAC address table**), and after that sends frames for that address only to that port. It does not disturb the other machines.

![A Raspberry Pi and a switch](images/pi-switch.jpg)

Frames for addresses it has not learned yet, and frames for everyone (**broadcast**, `ff:ff:ff:ff:ff:ff`), go out of every port.

## ARP: finding the MAC address from an IP address

Even when a computer wants to send a packet to `192.168.3.1` (the router), the frame needs a MAC address. **ARP** finds it.

1. The computer broadcasts to everyone on the LAN: "Whoever is `192.168.3.1`, tell me your MAC address"
2. Only the router answers: "Me. It is `18:2c:a9:00:00:01`"
3. The computer remembers the answer for a while (the ARP table)

```bash
ip neigh      # the remembered ARP table
```

```text
192.168.3.1 dev wlp3s0 lladdr 18:2c:a9:00:00:01 REACHABLE
```

### The IP address stays the same; the MAC address changes every hop

When sending to a server on the internet, the computer sets the frame's destination to the **router's MAC address**, while the IP packet inside keeps the **server's IP address** as its destination. The router removes the frame and wraps the packet again with the next router's MAC address.

| | Stays the same to the end | Changes at every hop |
| --- | --- | --- |
| What it decides | The final destination (IP address) | Who to hand it to next (MAC address) |
| Analogy | The address on the shipping label | The truck from one depot to the next |

## Wi-Fi (wireless LAN)

**Wi-Fi** is a LAN that connects by radio. The base unit that sends out the radio signal is the **access point**, and the network's name is the **SSID**.

| Band | Range | Speed | Features |
| --- | --- | --- | --- |
| 2.4 GHz | Wide. Gets through walls more easily | Slow | Easily mixed up with microwaves and Bluetooth. Many IoT devices, such as the Pico W, can only use this |
| 5 GHz | Medium | Fast | Less crowded |
| 6 GHz | Narrow | Very fast | Available with Wi-Fi 6E and Wi-Fi 7. The emptiest |

| Name | Standard | Year |
| --- | --- | --- |
| Wi-Fi 4 | IEEE 802.11n | 2009 |
| Wi-Fi 5 | IEEE 802.11ac | 2013 |
| Wi-Fi 6 / 6E | IEEE 802.11ax | 2019 / 2020 |
| Wi-Fi 7 | IEEE 802.11be | 2024 |

- Devices take turns on one radio channel; while someone is sending, others wait (**CSMA/CA**). The more devices connect, the slower each one gets
- Traffic is encrypted with **WPA2** or **WPA3** (WEP has been broken, so do not use it)
- In a large house, **mesh Wi-Fi**, where several units build one Wi-Fi network, is handy. To reach a barn, an outdoor access point or a run of LAN cable is more stable

![An outdoor Wi-Fi access point](images/outdoor-ap.jpg)

## A home router is several machines in one

![A home router (home gateway)](images/home-router.jpg)

One home "Wi-Fi router" contains every machine that appears in this book.

| Inside | Job | Chapter |
| --- | --- | --- |
| Router | Passes packets between the home LAN and the internet | 5 |
| Switch | Connects the LAN ports on the back | 6 |
| Wi-Fi access point | Connects by radio | 6 |
| DHCP server | Gives IP addresses to devices that connect | 7 |
| NAT | Merges private IP addresses into one global IP address | 7 |
| DNS relay | Passes name lookups on to the ISP's DNS server | 3 |
| Firewall | Stops traffic from coming in uninvited from outside | 8 |

## Summary

- Machines on a LAN are told apart by MAC address (48 bits, one per part)
- A switch learns MAC addresses and sends frames only to the port needed
- ARP finds the MAC address for an IP address
- The final destination (IP address) never changes; who it is handed to next (MAC address) changes at every hop
- Wi-Fi uses 2.4 GHz (long range, good for IoT), 5 GHz and 6 GHz (fast)

## Exercises

```quiz
Q: What is the 48-bit address used to tell machines apart on a LAN?
A: MAC address | MAC
E: The first half is the maker's number.

Q: Which protocol finds the MAC address from an IP address?
A: ARP
E: It asks everyone "who has this IP address?" and the owner answers.

Q: What is the machine that learns MAC addresses and sends frames only to the port needed?
A: switch | switching hub | L2 switch | network switch
E: Frames for unknown addresses and broadcasts go out of every port.

Q: What is the maximum amount of data in one Ethernet frame (normally 1,500 bytes) called?
A: MTU
E: It stands for Maximum Transmission Unit.

Q: Which Wi-Fi band, in GHz, can many IoT devices such as the Pico W use?
A: 2.4 | 2.4GHz
E: 2.4 GHz reaches far and gets through walls more easily, but it is crowded.
```
