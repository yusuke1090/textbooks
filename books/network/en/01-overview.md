# 1. What is a network? (from URL to page)

Tap a URL on your phone and the page appears in under a second. In that time, the data has travelled out and back through your home Wi-Fi, optical fiber, your internet provider, undersea cables and a data center. This book follows that journey one step at a time to see why the network connects, and then moves on to the cloud and IoT.

## Networks and the internet

A **network** is a set of computers joined together so that they can exchange data. The Wi-Fi in your home is one network, and so is the LAN in an office.

The **internet** is what you get by joining those networks to each other across the whole world (inter = between). No single company owns it. Tens of thousands of networks run by providers, companies and universities connect because they all follow the same rules, called **protocols**.

| Term | Meaning | Examples |
| --- | --- | --- |
| **LAN** | A network covering a small area such as a home or office | Home Wi-Fi, wired office LAN |
| **WAN** | A network that links distant places | Fiber lines, mobile networks |
| **Internet** | The network of networks spanning the world | The web, email, video, the cloud |
| **Protocol** | The agreed rules for connecting | HTTP, TCP, IP, Wi-Fi |

## From opening a URL to seeing the page

Here is a rough outline of what happens when you open `https://example.com/`. Chapters 2 to 9 look at each step in detail.

![From opening a URL to seeing the page](images/en/journey.svg)

1. The **browser** reads the URL and builds a "please send me this" message for the server (an **HTTP request**) (Chapter 2)
2. It asks **DNS** to turn the name `example.com` into an **IP address**, a number such as `104.20.23.154` (Chapter 3)
3. **TCP** prepares a connection with the server and numbers the data, which is cut into small **packets** (Chapter 4)
4. Each packet carries the destination IP address. **Routers** pass it along to the next router, like a bucket brigade (Chapter 5)
5. Inside the home, it first reaches your home router over **Wi-Fi** or a **LAN cable** (Chapter 6)
6. From the home router it goes over fiber to your **internet service provider (ISP)**, then through the places where providers meet and sometimes through **undersea cables**, to the data center where the server lives (Chapter 7)
7. It passes the **firewall** and **load balancer** in front of the server, and a web server sends back an answer (the **response**). Often a nearby **CDN** answers instead (Chapter 8)
8. The whole exchange is encrypted with **HTTPS** so nobody on the way can read it (Chapter 9)

The answer travels back along the same road, and the browser reads the HTML and draws the page. Images and CSS inside the page are fetched the same way, one by one.

## Packets: sending data in small pieces

A network does not send a large piece of data by taking over a wire from start to finish. It splits the data into small **packets** of up to about 1,500 bytes.

- Many people's packets can take turns on one wire (nobody holds the line, unlike an old phone call)
- If one packet is lost on the way, only that packet needs to be sent again
- Each packet can take whichever road is free at that moment

A packet is like a parcel with a shipping label. In front of the contents (the data) is a **header** holding the destination, a number and so on.

## Layers: splitting up the work

The work of a network is divided by role into **layers**. The key idea is that an upper layer does not need to care how the layers below carry the data. If you switch from Wi-Fi to a wired LAN, the browser keeps working without any change.

![Each layer adds a header before sending](images/en/layers.svg)

| Layer (TCP/IP) | Role (in a parcel service) | Main protocols |
| --- | --- | --- |
| Application layer | Rules for how applications talk (the letter and how it is written) | HTTP, DNS, SSH, MQTT (Ch. 2, 3, 9, 12) |
| Transport layer | Which application gets it (ports); reliable delivery (the recipient's name; proof of delivery) | TCP, UDP (Ch. 4) |
| Internet layer | Which computer, by which road (the address; relays between depots) | IP (Ch. 5) |
| Link layer | Carry it to the next machine by wire or radio (the truck or bicycle) | Ethernet, Wi-Fi (Ch. 6) |

When sending, each layer from the top down **wraps** the data with its own header (**encapsulation**). The receiver **peels** the headers off from the bottom up.

Textbooks and exams also use the seven-layer **OSI reference model**. It maps to the four TCP/IP layers like this. People sometimes name things by layer number, as in "L2 switch" or "L7 load balancer".

| OSI reference model | TCP/IP |
| --- | --- |
| 7 Application, 6 Presentation, 5 Session | Application layer |
| 4 Transport | Transport layer |
| 3 Network | Internet layer |
| 2 Data link, 1 Physical | Link layer |

## How the internet began

![An IMP, a node of the ARPANET (1969)](images/arpanet-imp.jpg)

| Year | Event |
| --- | --- |
| 1969 | The US **ARPANET** starts running, linking four universities and research institutes. The ancestor of the internet |
| 1983 | ARPANET switches to **TCP/IP**, the start of today's internet rules |
| 1984 | JUNET is set up to link Japanese universities |
| 1989–1991 | At CERN, a European research lab, Tim Berners-Lee creates the **World Wide Web** (URLs, HTML and HTTP) |
| 1990s | Providers start selling internet access to the public. In Japan it spreads from around 1995 |
| 2000s | Always-on connections through ADSL and fiber. Smartphones from around 2007. AWS cloud services start in 2006 (Chapter 10) |

The web is just one of the things that run on top of the internet. Email, video, games and IoT sensors all use the same internet.

## Summary

- The internet joins the world's networks using the same protocols
- Data is split into packets, and routers carry them in a bucket brigade
- The work is divided into layers (application, transport, internet, link). The sender wraps headers on; the receiver peels them off

## Exercises

```quiz
Q: What do we call a small piece of data with a header holding its destination and other details?
A: packet | packets
E: Data is sent in packets of up to about 1,500 bytes. Only lost packets need to be sent again.

Q: What is the word for the agreed rules that networks follow so they can connect?
A: protocol | protocols
E: HTTP, TCP, IP and Wi-Fi are all protocols.

Q: Of the four TCP/IP layers, which one handles IP addresses and routers?
A: internet layer | internet
E: It corresponds to layer 3 (the network layer) in the OSI reference model.

Q: What is it called when each layer, from the top down, wraps the data with its own header?
A: encapsulation
E: The receiver peels the headers off from the bottom layer up.

Q: What was the name of the ancestor of the internet that started running in the US in 1969?
A: ARPANET
E: It switched to TCP/IP in 1983.
```
