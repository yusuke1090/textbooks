# 11. Cloud networking (VPCs and serverless)

Everything we have seen in this book also exists inside the cloud: subnets, routers, NAT, firewalls, load balancers, DNS and CDNs. The difference is that you build them all from web pages and configuration files, without buying any machines.

## VPC: your own network inside the cloud

A **VPC** (Virtual Private Cloud) is a private network of your own that you build inside the cloud. It is like building your home LAN inside the cloud.

![Subnets inside a VPC and how they connect to the outside](images/en/vpc.svg)

| Part | Meaning | At home |
| --- | --- | --- |
| **VPC** | Your own range of private IP addresses, such as `10.0.0.0/16` | The whole home LAN |
| **Subnet** | A piece of the VPC in one AZ (such as `10.0.1.0/24`) | The LAN in each room |
| **Internet gateway** | The door between the VPC and the internet | Where the fiber line comes in |
| **Route table** | The road table for each subnet (Chapter 5) | The router's settings |
| **NAT gateway** | NAT that only lets traffic out from inside (Chapter 7) | The home router's NAT |
| **Security group** | A firewall for each server (Chapter 8) | A checkpoint for each machine |

### Public subnets and private subnets

- **Public subnet**: its route table says "everything else goes to the internet gateway". A machine with a global IP address can be reached from outside. Load balancers and entry servers go here
- **Private subnet**: has no road to the internet gateway and cannot be reached directly from outside. Application servers and databases go here. When they need to go out, for OS updates and the like, they go through the NAT gateway

The basic rule is to put the most important things deepest inside and have just one entrance.

### Security groups

A security group decides, for each server, "from where, which ports to allow". Replies to traffic that went out from inside are allowed automatically (stateful).

| Where | What to allow |
| --- | --- |
| Load balancer | 443 (HTTPS) from anywhere |
| Application server | 8000, only from the load balancer's security group |
| Database | 5432 (PostgreSQL), only from the application servers' security group |
| Management | 22 (SSH), only from your home or office IP address |

Because you can write "from this group" instead of IP addresses, you do not need to change the rules when the number of servers changes. It is important not to open SSH port 22 to "anywhere (`0.0.0.0/0`)".

### Names at each company

| What it is | AWS | Google Cloud |
| --- | --- | --- |
| Your own network | VPC | VPC network |
| Virtual servers | EC2 | Compute Engine |
| Firewall | Security groups | Firewall rules |
| Load balancer | ELB (ALB, NLB) | Cloud Load Balancing |
| DNS | Route 53 | Cloud DNS |
| CDN | CloudFront | Cloud CDN |
| Linking to a home or office | Site-to-Site VPN, Direct Connect | Cloud VPN, Cloud Interconnect |

Azure calls them VNet, Virtual Machines, network security groups, Azure Load Balancer, Azure DNS, Azure Front Door, ExpressRoute and so on.

## Setting up one server

The steps are almost the same at every company.

1. Choose the Tokyo region and create a virtual server. Use Ubuntu 24.04 and the smallest size (the free tier if there is one)
2. Register an SSH key (one you made, or one made and downloaded on the spot)
3. In the firewall (security group), allow port 22 only from your own IP address and port 80 from anywhere
4. Connect over SSH to the outside IP address shown on the screen

```bash
ssh -i ~/Downloads/mykey.pem ubuntu@203.0.113.10
```

5. Install a web server and open `http://203.0.113.10` in the browser on your computer

```bash
sudo apt update && sudo apt install -y nginx
curl -I http://localhost     # if HTTP/1.1 200 OK comes back, it is running
```

6. When you have finished trying it, **delete** the server (just stopping it may still cost money for the disk and IP address)

## Serverless: no servers to own

**Serverless** means not preparing servers at all, and asking for work in units such as "run this function when a request comes to this URL" or "do this when this data changes". It is not that there are no servers; the cloud company takes care of them entirely.

- Code runs only when a request arrives, and you pay only for the number of calls and the time. If nobody uses it, it costs almost nothing
- If traffic suddenly grows, it scales automatically
- If it has not been used for a while, only the first call takes extra time to start (a **cold start**). There is also a limit on how long one run can take

| Kind | Examples |
| --- | --- |
| Running functions (FaaS) | AWS Lambda, Google Cloud Run functions, Azure Functions |
| Running containers | Google Cloud Run, AWS Fargate (you can deploy Docker images as they are) |
| Using building blocks (BaaS) | Firebase (login, databases, files), Supabase |
| Serving fixed files | GitHub Pages, Cloudflare Pages, Amazon S3 + CloudFront |

### Example: this textbook's site

This textbook's site does not have a single server of its own to manage.

| Job | What it uses |
| --- | --- |
| Serving the HTML, chapter Markdown and photos | GitHub Pages (delivered from a CDN) |
| Logging in with an ID and password | Firebase Authentication |
| Syncing study records between phone and PC | Firebase's Firestore (Tokyo region) |
| Letting people read and write only their own records | Firestore security rules |

The browser talks to Firebase directly, and rules decide who can read which data. While there are few users, it runs within the free tier.

If you can build a Docker image ([Docker Textbook](https://yusuke1090.github.io/textbooks/?b=docker)), you can also put it on Cloud Run or similar and run it without owning a server.

## Summary

- A VPC is your own network in the cloud, built from per-AZ subnets, route tables, an internet gateway and NAT gateways
- The entrance (load balancer) goes in public subnets; applications and databases go in private subnets
- Security groups decide, per server, which ports and which senders to allow. Do not open SSH to the whole world
- Serverless means asking for work in units and paying for what you use. Fixed files can be served from GitHub Pages and similar services

## Exercises

```quiz
Q: What is the three-letter name for a private network of your own built inside the cloud?
A: VPC | Virtual Private Cloud
E: Azure calls it a VNet.

Q: What is a subnet with no road to the internet gateway, which cannot be reached directly from outside, called?
A: private subnet | private
E: Application servers and databases go here.

Q: What do servers in a private subnet go through when they go out, for example for OS updates?
A: NAT gateway | NAT
E: It only lets through traffic going from inside to outside.

Q: On AWS, what is the firewall that decides for each server which ports and senders to allow?
A: security group | security groups | SG
E: It is stateful, so replies to traffic sent from inside are allowed automatically.

Q: In serverless, what is it called when a function that has not been used for a while takes extra time to start on its first call?
A: cold start
E: While it is in regular use, it runs immediately.
```
