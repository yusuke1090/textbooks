# 10. What is the cloud?

So far we have seen that at the far end of the network there are servers in data centers. The **cloud** is a way of renting computers in those data centers over the internet, paying only for what you use.

## Own it or rent it?

In the past, to start a service you bought servers, found a place and lines for them, and fixed them yourself when they broke (**on-premises**). In the cloud, you ask through a web page or a command and a server is ready in tens of seconds, and you can delete it when you no longer need it.

In terms of electricity, on-premises is your own generator and the cloud is power from the power company.

| | On-premises | Cloud |
| --- | --- | --- |
| Getting started | Buy servers. Takes weeks | Minutes. Almost no money up front |
| Paying | A lot at once when you buy | Only for what you use (per second, hour or GB) |
| Growing and shrinking | Buy more. Cannot shrink | Grow at once, shrink at once |
| When it breaks | You fix it | The cloud company fixes hardware faults |
| Watch out for | Space, power, lines | Usage bills; depending on one company |

The US National Institute of Standards and Technology (NIST) sums up the cloud in five features: on-demand self-service, access over the network, resources shared among many users, rapid growth, and measured use.

## IaaS, PaaS and SaaS: how much do you rent?

![What you handle and what the cloud company handles](images/en/cloud-models.svg)

| Model | What you rent | What you do | Examples |
| --- | --- | --- | --- |
| **IaaS** | Virtual servers, disks, networks | Everything from the OS up | Amazon EC2, Google Compute Engine, Azure Virtual Machines |
| **PaaS** | A place to run applications | Your application's code and data | Google Cloud Run, App Engine, Azure App Service, Heroku |
| **Serverless** (FaaS, BaaS) | A place to run functions; building blocks such as login and databases | Function code and settings | AWS Lambda, Cloud Functions, Firebase |
| **SaaS** | A finished application | Just use it | Gmail, Google Docs, Microsoft 365, GitHub |

The higher you go, the easier it gets, but the less freedom you have. If you want to install Ubuntu and use it freely, like a Raspberry Pi, choose IaaS. If you just want to put an application somewhere, PaaS or serverless suits you.

## Cloud companies

| Company | Started | Features |
| --- | --- | --- |
| **AWS** (Amazon Web Services) | 2006 (S3, EC2) | The largest, with the most services |
| **Microsoft Azure** | 2010 | Connects easily with Windows, Office and company systems. Offers OpenAI's AI |
| **Google Cloud** | 2008 (App Engine) | Data analysis and AI; Firebase |

These three companies hold about 60% of the world's cloud market. Japan also has clouds from Sakura Internet, IIJ, NTT and others.

## Regions and availability zones

Cloud companies have groups of data centers (**regions**) around the world. Japan has regions in Tokyo and Osaka.

| | AWS | Google Cloud |
| --- | --- | --- |
| Tokyo | `ap-northeast-1` | `asia-northeast1` |
| Osaka | `ap-northeast-3` | `asia-northeast2` |

- Choosing a region near your users lowers latency (Chapter 7)
- Each region is divided into several **availability zones** (AZs, zones) with separate power, cooling and lines. If you put servers in two AZs, the service keeps running even if one building stops
- Personal data and similar information may be kept in a domestic region because of laws or company rules

The system that syncs this textbook's records (Firebase's Firestore) is also in Google Cloud's Tokyo region (`asia-northeast1`).

## What data centers look like

![A Google data center (Iowa, USA)](images/google-dc.jpg)

Inside the cloud are huge buildings lined with tens of thousands of servers.

![Ashburn, Virginia, where data centers cluster](images/ashburn.jpg)

Northern Virginia in the US has more data centers than anywhere else in the world. AWS's oldest region (`us-east-1`) is there. In Japan they cluster in places such as Inzai in Chiba.

![Cooling equipment on a data center roof](images/dc-cooling.jpg)

- Servers turn electricity into heat, so cooling them takes a lot of electricity. Data centers use cold outside air or water to save cooling power, and some are built in cold places such as Ishikari in Hokkaido
- According to the International Energy Agency (IEA), data centers used about 1.5% of the world's electricity in 2024, and this is expected to roughly double by 2030 because of AI

## How pricing works

- **Pay for what you use**: servers by running time (seconds or hours), disks by amount stored (GB per month), databases by number of reads and writes, and so on
- **Data going out costs money**: data coming into the cloud from the internet is usually free, but data sent out of the cloud (**egress**) is charged per GB
- **Free tiers**: small servers and databases are often free up to a set amount
- **Watch for things left running**: a test server you forget to delete costs money every month. Set up a **budget alert** first (an email when spending passes a set amount)

## Splitting responsibility

The cloud company protects the buildings, hardware and virtualization. Updating the OS you put on top, passwords, firewall settings and who can see your data are the renter's responsibility (the **shared responsibility model**). Many cloud incidents come from configuration mistakes, such as leaving a data store open for anyone to see.

## The cloud stops too

On 20 October 2025, AWS's `us-east-1` had an outage in which the name of a database service (DynamoDB) could no longer be looked up in DNS, and many apps and sites around the world were unusable for hours. It is an example of a small DNS (Chapter 3) mistake spreading widely. Put important services in separate AZs or regions, and decide in advance what to do when one stops.

## Summary

- The cloud is a way of renting computers in data centers over the internet, paying for what you use
- It gets easier in the order IaaS (servers), PaaS (a place for apps), serverless, SaaS (finished apps)
- AWS, Azure and Google Cloud are the big ones. You choose a region (Tokyo, Osaka) and AZs
- You pay for what you use. Watch outgoing data and forgotten resources, and set a budget alert
- Settings and contents are the renter's responsibility. The cloud can stop too

## Exercises

```quiz
Q: What do we call buying servers yourself and keeping them at your own site?
A: on-premises | on-prem | on-premise
E: With the cloud, you rent only what you use.

Q: What is the four-letter name for renting virtual servers and disks and setting up everything from the OS up yourself?
A: IaaS
E: Amazon EC2 and Google Compute Engine are IaaS.

Q: What is the four-letter name for using finished applications such as Gmail or Microsoft 365?
A: SaaS
E: You just use the application.

Q: What is a group of data centers inside a region, with separate power and lines, called?
A: availability zone | AZ | zone
E: Putting servers in two AZs keeps the service running if one stops.

Q: What is data transfer out of the cloud called (it is often charged per GB)?
A: egress | data transfer out | outbound
E: Data coming into the cloud (ingress) is usually free.
```
