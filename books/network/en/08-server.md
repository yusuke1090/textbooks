# 8. The server side (firewalls, load balancers, CDNs)

The packet has crossed the sea and arrived at the data center where the server is. On a big site, a single server does not answer everyone. The entrance is guarded, the work is shared among many servers, and sometimes a machine close to the user answers instead.

## Data centers

![Server racks in a data center](images/server-racks.jpg)

A **data center** is a building for holding thousands of servers. To keep running, it has two of everything: power, cooling and network lines. Servers are stacked in 19-inch shelves called **racks**.

The path to a site's servers usually looks something like this.

![The path on the server side](images/en/server-side.svg)

## Firewalls: let through only allowed traffic

A **firewall** is a checkpoint that lets through only traffic matching its rules and stops everything else.

- Rules are written as "from where, to where, to which port". For example: "From outside, allow only 443 (HTTPS). Allow 22 (SSH) only from the office IP address"
- Replies to connections started from inside are remembered and let through (**stateful**)
- Firewalls sit in several places: the home router, the company entrance, the server's OS, the cloud's security groups (Chapter 11) and so on

On Ubuntu you can set one up with `ufw`. Use it too when you put a Raspberry Pi or Jetson where it can be seen from outside.

```bash
sudo ufw default deny incoming   # block everything from outside by default
sudo ufw allow 22/tcp            # allow SSH
sudo ufw allow 443/tcp           # allow HTTPS
sudo ufw enable
sudo ufw status
```

If you run `ufw enable` on a machine you are connected to over SSH before allowing port 22, you lock yourself out too. Watch the order.

## Load balancers: sharing the work

A **load balancer** is a machine (or software) that shares out many requests among several servers behind it.

- When one server is not enough, you can add more to increase the total power (**scaling out**)
- If one server breaks, the load balancer notices (**health checks**) and sends work only to the rest
- If you update servers one at a time, you can replace them without taking the site down

| Type | What it looks at | What it can do |
| --- | --- | --- |
| L4 (transport layer) | IP addresses and ports | Fast. Does not look at the contents |
| L7 (application layer) | URLs, headers, cookies | Can send `/api/` to the API servers and `/images/` to the image servers. Often decrypts HTTPS here |

## Web servers and application servers

Behind the load balancer, software with separate roles is running.

| Software | Job | Examples |
| --- | --- | --- |
| **Web server** | Returns files such as HTML and images. Passes other requests to the application | nginx, Apache, Caddy |
| **Application server** | Builds answers each time: logins, searches, orders | Python (Django, FastAPI), Node.js, Go and others |
| **Database** | Stores and searches data | PostgreSQL, MySQL, Redis |

The database goes in an inner network that cannot be reached directly from outside (Chapter 11).

## CDNs: answering from nearby

![A CDN answers from a server near the user](images/en/cdn.svg)

As Chapter 7 showed, talking to a faraway server takes time even at the speed of light. A **CDN** (Content Delivery Network) puts servers (**edges**) in hundreds of places around the world, keeps copies of images and HTML there, and answers from the edge nearest the user.

- It is fast because requests do not have to go all the way to the original server (the **origin**). The origin has less work too
- It goes to the origin only when it has no copy or the copy is too old
- When attacked with huge amounts of traffic (DDoS), edges all over the world absorb it
- Well-known CDN companies are Cloudflare, Akamai, Fastly and Amazon CloudFront. This textbook's site (GitHub Pages) is also delivered from a CDN

The `example.com` headers in Chapter 2 showed the CDN at work.

```text
Server: cloudflare
Age: 13682
cf-cache-status: HIT
CF-RAY: a5c6c32e5a87e052-KIX
```

`cf-cache-status: HIT` means "the edge had a copy, so it returned that". `Age` is how many seconds ago the copy was taken. `KIX` at the end of `CF-RAY` shows that the edge that answered is in Kansai (the code for Kansai International Airport).

## Anycast: the same address all over the world

`8.8.8.8` (Google's DNS), `1.1.1.1` (Cloudflare's DNS) and the DNS root servers use the same IP address at hundreds of places around the world (**anycast**). Each place announces through BGP (Chapter 7) "send this address to us", so packets naturally reach the nearest one through the way routers choose roads. CDNs often pick edges this way too.

## Summary

- Data centers double up power, cooling and lines, and stack servers in racks
- Firewalls let through only the ports you need. On Ubuntu, use `ufw`
- Load balancers share work among many servers and avoid broken ones
- CDNs return copies from edges near the user, making sites faster and tougher
- With anycast, the nearest of many places around the world receives the same IP address

## Exercises

```quiz
Q: What is the mechanism that lets through only traffic matching its rules and stops the rest?
A: firewall | FW
E: Rules say "from where, to where, to which port".

Q: What is the thing that shares out many requests among several servers behind it?
A: load balancer | LB
E: It also uses health checks to find broken servers and avoid them.

Q: What is the three-letter name for the system that keeps copies on servers near users and answers quickly?
A: CDN | Content Delivery Network
E: Cloudflare, Akamai, Fastly and Amazon CloudFront are examples.

Q: What is the method of using the same IP address in many places around the world so that the nearest one is reached?
A: anycast
E: It is used by 8.8.8.8, 1.1.1.1 and the DNS root servers.

Q: Which command sets up the firewall on Ubuntu?
A: ufw
E: Choose the ports to allow, as in `sudo ufw allow 22/tcp`.
```
