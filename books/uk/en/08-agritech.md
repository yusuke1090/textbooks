# 8. Agritech and IoT companies

## What you will learn

- Why agritech is growing in the UK
- Government support, and places for research
- The main companies (robots, apps, cameras)
- Drone rules
- Lessons from things that did not work

The state of the companies in this chapter was researched in November 2026. Startups change quickly, so check before relying on it.

## Why is it growing?

- **Labor is expensive and scarce**: the minimum wage is £12.71 an hour (about 2,600 yen). After Brexit, fewer people come from abroad to work. There is a reason to pay for machines and robots that can replace people
- **Farms are large**: an average farm is 80 ha, and an average dairy herd is 230 cows. The cost of machines and software can be spread over a large area or herd
- **Research and universities**: there are many agricultural research institutes and universities, and it is easy to borrow trial fields and barns
- **Money**: London has many investors. As of April 2026, there were about 250 active agritech companies, which had raised about £1.6 billion in total
- **Environmental rules**: strong demands to cut fertilizer, pesticides and methane create a need for technology that "measures and applies only where needed" (precision agriculture)

## Government support

- **Farming Innovation Programme**: the government (the Department for Environment, Food and Rural Affairs, Defra) and the R&D funding body **Innovate UK** give grants for agricultural R&D. Companies often apply together with universities and farmers
- In April 2026, it announced support for 12 technologies under a plan worth about £50 million to bring AI and robots onto farms (about £8 million from the government and about £40 million from the private sector)
- In August 2026, a £20 million call for R&D on farm **automation and robotics** (the Farming Futures R&D Fund)
- Gene editing: the Precision Breeding Act of 2023 allows gene-edited crops in England to be treated more lightly than, and separately from, genetically modified ones

## Places for research

![The Broadbalk experiment at Rothamsted Research. Wheat has been grown in the same field since 1843 — the longest-running agricultural experiment in the world](images/broadbalk.jpg)

| Place | In brief |
| --- | --- |
| **Rothamsted Research** (Hertfordshire) | Founded in 1843, one of the oldest agricultural research institutes in the world. Where fertilizer trials began |
| **Harper Adams University** (Shropshire) | Famous for agricultural engineering. In 2017 it was the first in the world to succeed with the "**Hands Free Hectare**", growing and harvesting barley with only automated machines and drones, without people entering the field |
| John Innes Centre (Norwich) | Plant genetics and breeding |
| University of Lincoln | Agricultural robotics (fruit picking and more) |
| SRUC (Scotland) | An agricultural college. Research farms for cattle and sheep |

![The Rothamsted Research building (Rothamsted Manor)](images/rothamsted-manor.jpg)

## The main companies

### Robots

- **Fieldwork Robotics** (Cambridge): a robot that finds raspberries and other fruit with cameras and picks them. In April 2026 it raised £3 million, and under a "harvesting as a service" model (not selling the robots, but being paid by the amount picked) it will run on farms in Norfolk and Staffordshire for two years. It plans to deploy many robots side by side in 2027
- Strawberries are often grown on waist-high tables inside polytunnels (simple plastic greenhouses), a setup that robots can get into easily

![Strawberry polytunnels (Herefordshire). Many British strawberries are grown in these](images/polytunnels.jpg)

- **Small Robot Company**: became famous for a plan in which "Tom", a robot that patrols fields, photographs each plant and destroys only the weeds with lasers and the like. But it could not raise money for mass production and **went into liquidation in February 2024**. Tom is now in the collection of the Science Museum Group

### Apps and data

- **Breedr**: an app born in Britain in 2018 for recording each animal (weight, feed, health) and for buying and selling cattle. It judges how good the feed is from how fast cattle gain weight. In August 2026 it raised 27 million dollars and records more than 2 million cattle. It has now moved its headquarters to the United States (Austin, Texas) and operates in the US, the UK and Australia
- For dairy camera AI (CattleEye and others) and sensor companies, see Chapter 7

### Indoor farming

![Vegetables grown under LED light in many stacked layers (a vertical farm)](images/vertical-farm.jpg)

- From the late 2010s, many **vertical farms** that grow vegetables under LEDs inside warehouses were set up
- But when electricity prices rose in 2022, many companies closed or scaled down. British electricity is expensive even by European standards, and vegetable prices struggle to cover the power bill

## Drone rules

- Until 2023, **spraying** pesticides and the like from drones **was prohibited**, and weight was limited to 25 kg
- In 2023, a spraying drone from China's XAG became the first to receive an "operational authorization" from the Civil Aviation Authority (**CAA**)
- After that, a company called AutoSpray Systems got permission to spray liquids and spread granular fertilizer with a large 120 kg drone, and in March 2025 also got permission to **fly beyond visual line of sight (BVLOS)** (it was accepted that agricultural flights below 15 m pose little danger to other aircraft)
- Today, farmers hire companies that hold permits to spray by drone. The government (the Health and Safety Executive, HSE, and Defra) is putting together the procedures for applying pesticides by drone
- In Japan, drone spraying is normal, but in Britain it is "still to come". This may be a field where Japanese experience can help

## Radio signals and connectivity

- Mobile signals are weak in the countryside, and there is often no connection in barns or at the edges of fields
- So farms are increasingly using **LoRaWAN** (low-power wireless that reaches far) and satellite internet (**Starlink**)
- **Caution**: as in the rest of Europe, LoRaWAN and the like use the **868 MHz** band. Japanese **920 MHz** devices cannot be used in Britain as they are (Chapter 9)

![A LoRaWAN gateway (base station). It receives signals from sensors several km away and connects them to the internet](images/lorawan-gateway.jpg)

## Lessons from things that did not work

- **Hardware takes money and time**: as with Small Robot Company, even good technology ends when the money for mass production and sales runs out. More companies now sell as a service (paid by the amount harvested, or monthly)
- **Farmers are strict about profit**: milk prices go up and down every month, and wheat prices are set by world markets. If you cannot clearly show "how many pounds they gain", they will not buy
- **Connecting data**: farmers already use several pieces of software — milking robots, cattle registration, accounts. New products are disliked unless they can exchange data with these
- **Weather and seasons**: many crops give one trial result a year, so results take time. If you try to sell during busy seasons (harvest, calving), nobody will meet you
