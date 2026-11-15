# 9. If you were to do agricultural IoT in the UK

## What you will learn

- The good points and the hard points of the British market
- The rules for selling products (certification, radio, data)
- How to proceed (research → trade shows → trials → sales)
- What could be done with IoT for dairy

Reading this alongside Chapter 9 of the Africa Textbook (Tanzania, Kenya, Malawi) makes the differences clear.

## Good points and hard points

| Good points | Hard points |
| --- | --- |
| You can do business in English. Laws and contracts are solid | Large European and American companies (Lely, DeLaval, GEA, Deere, MSD and others) are already there |
| Labor is expensive and farms are large, so farmers pay for machines and data | Farmers are strict about profit, and budgets change quickly with milk and wheat prices |
| Many subsidies and research sites make trials easy | Farmers are cautious about trying new products. Word of mouth between farmers matters |
| Dairy farmers are used to smartphones and data | Many farms have no mobile signal |
| Japanese machinery (Kubota and others) has a good reputation | A 9-hour time difference and about 14 hours of travel (direct flight) |

- Africa (especially Kenya and Tanzania) is "a market that will grow, where cheapness comes first"; Britain is "a market that is already large, and wants quality and results"

## Rules for selling products

| Item | Details |
| --- | --- |
| **Product safety and certification** | The EU's **CE mark** is accepted in Great Britain indefinitely (for many products, including radio equipment). Britain's own **UKCA mark** is also fine. Northern Ireland requires CE |
| **Radio** | The same bands as Europe. LoRaWAN, Sigfox and the like use **868 MHz** (Japan uses 920 MHz). Devices certified under Japan's *giteki* rules cannot be used as they are. Prepare devices for the British frequencies |
| **Security of connected devices** | Since April 2024, internet-connected products must meet three requirements: "no universal default passwords", "provide a way to report vulnerabilities" and "state how long updates will be provided" (the PSTI Act) |
| **Data** | **UK GDPR** (almost the same as the EU's personal data rules). Farmers' names, locations and contact details are personal data. State in contracts where data is stored and who can use it |
| **Electricity** | 230 V, 50 Hz, three-pin type BF plugs |
| **Livestock rules** | Every cow has an ear tag, and births, movements and deaths are reported to the government. Be ready to explain devices attached to animals from an animal welfare point of view too |

- When selling under the CE mark, you must follow all the EU rules and give the name of an importer or representative within the EU

## How to proceed

### 1. Research

- Statistics and markets: **AHDB** (milk prices, herd numbers, production costs), Defra's agricultural statistics
- News: farming newspapers (Farmers Weekly, Farmers Guardian), farmers' organizations (NFU)
- Japanese contact point: **JETRO London** (market research, Japanese pavilions at trade shows, advice on setting up a company)

### 2. Go to trade shows and agricultural shows

![Cattle judging at the Royal Highland Show (Edinburgh). Agricultural shows are a place to talk with farmers directly](images/highland-show.jpg)

| Name | When and where | What it is |
| --- | --- | --- |
| **LAMMA** | January, Birmingham | Farm machinery and technology. One of the largest in Britain |
| **Dairy-Tech** | February, Stoneleigh (near Coventry) | A trade show only for dairy technology |
| **Cereals** | June | Arable farming. Machines are demonstrated working in real fields |
| **Groundswell** | Late June–July, Hertfordshire | Regenerative agriculture (no-till, cover crops and more) |
| **Royal Highland Show** | June, Edinburgh | Scotland's big agricultural show |
| **Royal Welsh Show** | July, Builth Wells | Wales's big agricultural show |
| **UK Dairy Day** | September, Telford | Where dairy farmers gather. Cattle judging and exhibitions |

- Summer agricultural shows are "festivals" that local farmers come to with their families. Think of them as places to listen first, rather than to sell

### 3. Run trials

- Partner with universities and research farms (Harper Adams, SRUC, Rothamsted and others) to produce numbers (how many cows' illnesses were found how many days earlier, how many pounds were gained)
- Innovate UK grants are normally applied for by companies registered in Britain
- A British company (Ltd) can be set up online in about a day for a few tens of pounds

### 4. Sell

- Rather than going to farmers directly, the shortcut is to go through **people farmers already trust**
  - Farm machinery dealers
  - Vets (dairy farmers see their vet several times a month)
  - Milk processors and supermarkets (they ask farmers on aligned contracts to record data; Chapter 7)
  - Dairy consultants and milk recording companies
- Pricing is more often **monthly** (per cow, per farm) than a one-off purchase. The initial burden on the farmer is smaller

![A Kubota tractor. Japanese farm machinery is also used in Britain for small and medium tractors and mowers](images/kubota.jpg)

## Japanese companies

- **Kubota**: has a sales company in Britain (Kubota UK, Oxfordshire). Tractors, compact construction machinery, mowers
- **Yanmar** and **Iseki**: sell small tractors and machines through dealers
- Japanese companies have a reputation for "hard to break" and "parts are available", which is a tailwind when selling new products

## What could be done with IoT for dairy

| Problem (Chapter 7) | What IoT might do |
| --- | --- |
| Not enough labor | Alerts for heat, calving and illness cut the time spent checking cows |
| Lameness records are required | Cameras score gait automatically, and produce reports for milk processors as they are |
| Managing grass for grazing | Measure grass (satellites, drones, plate meters), track where cows are (GPS) |
| Bovine TB | Record contacts between cattle, and between cattle and wildlife. Manage test schedules |
| Milk price and production cost | Combine data on milk yield, feed and costs to work out the production cost per liter |
| Environment (slurry, methane) | Record tank levels and the amount and place of spreading. Make methane visible |
| No signal | Put a LoRaWAN (868 MHz) gateway on the farm. Combine with satellite |

- It is important to be able to say in one sentence **how you differ** from existing products (SenseHub, CowManager, CattleEye and others in Chapter 7): cheaper, longer battery life, works with grazing, connects to other data
- British dairy herds are larger than Japanese ones, so the way data is presented (hundreds of cows at a glance) also changes

## Summary

- Britain is "a mature market where people have reasons to pay". In return, competition is fierce and results in numbers are demanded
- Build radio (868 MHz), certification (CE/UKCA), security (PSTI) and data (UK GDPR) into the product from the start
- Listen at trade shows and agricultural shows, partner with universities, vets and dealers, test small, then expand

## Exercises

```quiz
Q: Which frequency (MHz) do LoRaWAN devices use in the UK (Japan uses 920 MHz)?
A: 868
E: Japanese-certified devices cannot be used as they are.

Q: What is the UK's own product safety marking (the EU CE mark is also accepted)?
A: UKCA | UKCA mark
E: Northern Ireland needs the CE mark.

Q: Which law, from April 2024, bans the same default password on all connected products?
A: PSTI | PSTI Act
E: Makers must also give a way to report weaknesses and say how long updates will last.

Q: Which January show in Birmingham is one of the UK's biggest for farm machinery and technology?
A: LAMMA
E: The dairy-only technology show is Dairy-Tech, in February.
```
