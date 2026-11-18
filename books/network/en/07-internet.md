# 7. From home to the internet (NAT, ISPs, undersea cables)

The packet has reached the home router. From here it goes over optical fiber to the **internet service provider (ISP)**, through the places where providers connect, sometimes across the sea through **undersea cables**, and on to the data center where the server is.

## DHCP: you get an IP address automatically

You can communicate just by joining Wi-Fi because the router's **DHCP server** hands out the settings you need.

1. Computer: "Can somebody give me an IP address?" (to everyone)
2. Router: "How about `192.168.3.123`?"
3. Computer: "I'll take that one"
4. Router: "It's yours. You can use it for 24 hours"

You receive an IP address, the subnet (`/24`), the default gateway, the DNS server and how long you may use them (the **lease**). If you use a Raspberry Pi or Jetson as a server, set the router to "always give this MAC address the same IP address" (a **DHCP reservation**) so you can always reach it at the same address.

## NAT: everyone shares one global IP address

![NAT rewrites addresses and ports](images/en/nat.svg)

An ISP usually gives a home just one global IP address. The phones, computers and TV inside cannot receive replies on the internet while they only have private IP addresses (`192.168.3.x`).

So the router rewrites the source of outgoing packets to its own global IP address and a port, and remembers the mapping in a table (**NAT**; because it also uses ports, it is also called NAPT or IP masquerading). When a reply arrives, it looks up the table and passes the reply back to the right machine.

| Inside the home | Outside the router | Other side |
| --- | --- | --- |
| `192.168.3.123:50001` (computer) | `203.0.113.45:40001` | `104.20.23.154:443` |
| `192.168.3.45:50001` (phone) | `203.0.113.45:40002` | `104.20.23.154:443` |

You can find your global IP address by asking a server outside.

```bash
curl https://api.ipify.org
```

### Nobody can come in from outside

NAT table entries are made when something goes from inside to outside. So nobody outside can suddenly connect to a machine inside the home. This protects you, but it is a problem when you want to use your Raspberry Pi at home from outside.

- Set the router to "send anything arriving at outside port 8080 to port 80 on the Raspberry Pi" (**port forwarding**). This exposes it to the outside, so take care with security
- Mobile networks (4G, 5G) and some ISPs share one global IP address among many homes (**CGNAT**). Port forwarding is not possible then
- So a common approach is for the device to connect out to a server first and keep that connection open: a VPN (Chapter 9) or MQTT for IoT (Chapter 12)

## From home to the ISP: access lines

| Line | How it works | Features |
| --- | --- | --- |
| **Fiber** (FTTH) | Optical fiber runs all the way to the house. An **ONU** at home converts between light and electricity | Fast and stable. 1–10 Gbps |
| **Mobile network** (4G, 5G) | Connects by radio to a nearby **base station** | No installation work. Usable in barns and fields |
| Cable TV | The TV coaxial cable | Depends on the area |
| **Satellite** (Starlink etc.) | Connects by radio to many satellites in low orbit | Works in mountains and at sea where no lines reach |

![5G base station antennas](images/5g-antenna.jpg)

![A Starlink antenna](images/starlink.jpg)

**Optical fiber** is a glass thread as thin as a hair, and light travels through it, bouncing off the inside walls. It carries signals farther than electricity without fading, and it is not affected by electrical noise such as lightning.

![Light travelling through an optical fiber](images/optical-fiber.jpg)

![Fiber-optic cable running along utility poles](images/fiber-pole.jpg)

### Japanese fiber lines: PPPoE and IPoE

Japanese fiber lines (NTT's FLET'S Hikari and the "Hikari Collaboration" services that resell it) have two ways of connecting to the ISP.

| Method | How it works | Evening congestion |
| --- | --- | --- |
| **PPPoE** (IPv4) | Log in with an ID and password and pass through the ISP's entry equipment | The entry equipment gets crowded, so it tends to slow down in the evening |
| **IPoE** (IPv6) | No login; goes through a wide entrance. IPv4 is carried inside IPv6 too (**IPv4 over IPv6**, such as "v6 Plus") | Less crowded |

If it is only slow in the evening, check whether your ISP and router support IPoE.

## How providers connect to each other

![From home to server: a network of networks](images/en/internet.svg)

The internet is tens of thousands of networks joined together. ISPs, large companies, universities and others each run their own network as one unit (an **AS**, autonomous system).

- ASes use a protocol called **BGP** to tell each other "you can reach this block of addresses through us". Routers' routing tables are built from this
- A place where many ASes gather to connect to each other is an **IX** (internet exchange). Tokyo and Osaka have JPIX, JPNAP, BBIX and others
- Small ISPs pay a large ISP to carry their traffic to the rest of the world (**transit**). Networks of similar size often exchange each other's traffic for free (**peering**)

![Equipment at an internet exchange (DE-CIX)](images/ix.jpg)

DE-CIX in Frankfurt, Germany, is one of the largest IXes in the world.

## Undersea cables: crossing the sea

![Cross-section of an undersea cable](images/submarine-cable.jpg)

Almost all data between countries (about 99%) is carried by **undersea cables**, not satellites. More than 500 cables lie across the world's oceans.

- In the deep sea they are about as thick as a garden hose (about 2 cm). The optical fibers at the center are wrapped in steel wires, copper and plastic. In shallow water they are thicker and armored, to protect them from anchors and fishing nets
- Every 50–100 km or so there is a **repeater** that boosts the weakened light. Power is sent from land through the copper in the cable
- A new cable can carry tens to hundreds of terabits per second (Tbps)
- They are laid by special **cable ships**, which also lift them up and repair them when they break

![A Japanese cable ship (KDDI Cable Infinity)](images/cable-ship.jpg)

The place where an undersea cable comes ashore is a **cable landing station**. Japan sits on the route between the Pacific and Asia, with landing stations on the Boso Peninsula in Chiba, at Shima in Mie and elsewhere.

![KDDI's Chikura cable landing station in Chiba](images/landing-station.jpg)

## Two kinds of speed: bandwidth and latency

A "fast line" can mean two different things.

| | Meaning | Unit | When it matters |
| --- | --- | --- | --- |
| **Bandwidth** (throughput) | How much can be carried per second. The number of lanes on a road | Mbps, Gbps | Video, large files |
| **Latency** | The time to go and come back (RTT). The length of the road | ms (milliseconds) | Games, calls, each exchange on the web |

Light in optical fiber travels about 200,000 km per second. Nothing can beat the speed of light, so the farther away the other side is, the higher the latency.

| Other side | Typical RTT |
| --- | --- |
| Inside the same LAN | Under 1 ms |
| A server in Japan (even far from Tokyo or Osaka) | 5–30 ms |
| The US west coast | About 100 ms |
| Europe | 200–250 ms |
| A geostationary satellite link | About 600 ms |
| Starlink (low-orbit satellites) | About 30–60 ms |

A web page goes back and forth many times: DNS, TCP, the encryption greeting and many requests. So latency often matters more than bandwidth. That is why CDNs (Chapter 8) and cloud regions (Chapter 10), which put servers near users, are important.

## Summary

- DHCP hands out IP addresses, the gateway and the DNS server automatically
- NAT merges the private IP addresses at home into one global IP address. Nobody can come in from outside
- Lines from home to the ISP include fiber, mobile and satellite. On Japanese fiber, IPoE (IPv6) is less crowded
- Providers (ASes) share routes with BGP and connect at IXes. Countries are linked by undersea cables
- Speed means bandwidth (Mbps) and latency (ms). Latency depends on distance

## Exercises

```quiz
Q: What automatically hands out IP addresses and the default gateway to devices that connect?
A: DHCP
E: It lends the address for a set time (the lease).

Q: What is the system that merges the private IP addresses at home into one global IP address?
A: NAT | NAPT | IP masquerade | IP masquerading
E: It remembers the address and port mapping in a table and passes replies back to the right machine.

Q: Which protocol do ASes use to tell each other "you can reach this address through us"?
A: BGP
E: Internet routing tables are built with BGP.

Q: What carries almost all data between countries?
A: undersea cable | undersea cables | submarine cable | submarine cables
E: It is carried through optical fibers on the sea floor, not by satellite.

Q: What do we call the kind of speed measured as "the time to go and come back"?
A: latency
E: The amount carried per second is bandwidth (throughput).
```
