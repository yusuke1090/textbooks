# 12. Smart agriculture

## What you will learn

- Why smart agriculture now
- Smart agriculture for rice (drones, water management, automated driving, yield-measuring combines)
- Smart agriculture for upland crops (auto-steering, variable-rate fertilizing, sensing)
- Costs and challenges

## Why now

- The number of people farming has roughly halved in the last 20 years, and their average age is about 70. The remaining farmers take over the paddies and fields of farmers who quit, so the area per farm keeps growing
- Since more people cannot be added, technology that lets **one person look after a large area** is essential
- In October 2024, the **Act on Promoting the Use of Smart Agricultural Technology** came into force. If the government approves a plan to change how crops are grown to suit smart agriculture (a **production method innovation plan**), the farm can get low-interest loans and tax benefits. Rice growing has the most approved plans

## Rice growing

### Drones

![An agricultural drone used in paddies in Aomori](images/drone-paddy.jpg)

- The most widely used smart agriculture machine. It sprays pesticides and fertilizer (top-dressing) from the air. It can cover 10 a in about 1–2 minutes
- In the past, spraying was done with radio-controlled helicopters (large and expensive) or by people carrying power sprayers on their backs. Drones have greatly reduced the heavy labor, especially in the heat of summer
- They are also used to sow seed for **direct seeding** (Chapter 3)
- Rules for using them (for details, see the safety and law chapter of the "ROS 2 and ArduPilot Textbook")
  - Drones of 100 g or more must be **registered** with the government and fitted with a Remote ID
  - Spraying pesticides counts as "**carrying dangerous goods**" and "**dropping objects**" under the Civil Aeronautics Act, so government **approval** is needed
  - Use only pesticides registered for drone spraying, at the specified concentration
- Many farmers do not own one, and instead hire companies that do the spraying (**agricultural support services**)

![A demonstration of spraying with an agricultural drone. The downwash from the propellers carries the spray down to the base of the rice plants](images/drone-irri.jpg)

### Water management systems

- As in Chapter 4, adjusting water depth is a big daily job. On large farms with dozens of scattered paddies, the rounds alone can take all day
- Put **automatic water valves** (attached to the inlet; they open and close automatically while watching the water level) and **water level sensors** in the paddies, and you can check water levels on a smartphone and operate them remotely
- Example products: WATARAS (Kubota ChemiX), Suiden farmo (farmo), paditch (Enowa) and others. Many report a big reduction in time spent on rounds
- Communication uses mobile networks (LTE) or low-power wireless that reaches far (**LPWA**, such as 920 MHz LoRa). They run on batteries and solar cells
- They can also be used to record extended midseason drainage (J-Credits, Chapter 4). There are also startup services that record the midseason drainage dates and handle credit applications for many farms together

### Machines that drive themselves

- **Auto-straight** rice transplanters: measure position with GNSS (GPS and others) and plant in straight lines. The operator does not hold the wheel and can focus on refilling seedlings and turning at the ends
- **Robot tractors** and robot rice transplanters: run with nobody on board. Currently, the condition is that a person watches from nearby (within sight). Systems that run with only remote monitoring are also being tested
- Measuring position to the centimeter needs **RTK** (a method using correction information from a base station). Farmers use base stations run by JA or local governments, or network RTK services from mobile phone companies

### Yield-measuring combines and farm management apps

- Combines with **taste and yield sensors**: while harvesting, they measure the yield of each paddy and the rice's moisture and protein
- The data is sent to the maker's farm management cloud (Kubota's KSAS, Yanmar's SMARTASSIST and others), where it can be viewed alongside records of fertilizer, work and yield for each paddy
- It is used to plan the next year, for example: "this paddy has low yield and high protein → use less fertilizer next year"

### Satellites and remote sensing

- Cameras on satellites and drones show **uneven growth** in paddies and fields. Measures such as **NDVI**, which turns leaf color (how healthy the plants are) into a number, are used
- It is used to predict when to harvest rice, decide how much panicle fertilizer to apply, and find where rice has fallen over
- There are also services for farmers that use satellite images (for example, Europe's Sentinel-2, free every 5 days)

## Upland crops

### GNSS auto-steering

![A self-driving tractor (an experiment in a vineyard). It follows a set path using GNSS and sensors](images/robot-tractor.jpg)

- A device that turns the steering wheel automatically is retrofitted to an existing tractor, so it drives straight along GNSS positions (**auto-steering**)
- It spread rapidly on large field-crop farms in Hokkaido
  - In sowing, fertilizing and spraying, overlaps and gaps decrease, saving seed, fertilizer and pesticide
  - Work can be done at night or where there are no visible markers
  - Fatigue from long hours of driving is greatly reduced
- Recently, cheaper devices made overseas have increased, and more people are using them on paddies and fields in Honshu too

### Variable-rate fertilizing

- From uneven growth seen by satellites or drones, soil tests and the previous year's yield map, a **map that sets the amount of fertilizer for each spot** (a fertilizer map) is made
- A fertilizer spreader (broadcaster) linked to GNSS changes the amount it spreads as it drives, following the map
- More where growth is poor, less where it is good. This makes it possible to even out yield and quality while using less fertilizer. It is used for top-dressing wheat (to even out protein), and for basal fertilizer for sugar beet and potatoes, among others

### Disease prediction

- There are systems that calculate from weather data how likely diseases are, and send alerts
  - Rice **blast**: estimates days when infection is likely from how long the leaves are wet and the temperature (BLASTAM and others)
  - Wheat **Fusarium head blight**: decides the day to spray fungicide from the predicted flowering date and the rain around it
- Combined with the prefecture's pest forecasts, they cut down on unnecessary pesticide

## Costs and challenges

| Technology | Rough cost |
| --- | --- |
| Agricultural drone | 1–3 million yen (if you hire spraying, from a little over 1,000 yen per 10 a) |
| Automatic water valve | Tens of thousands to about 100,000 yen per valve + communication fees |
| Retrofit auto-steering | Hundreds of thousands to a few million yen |
| Robot tractor | 10 million yen or more |

- **Cost**: expensive for small farms. Sharing machines, hiring out work (agricultural support services) and leasing are spreading
- **Field shape**: Japanese paddies are small, irregular in shape and scattered. Large machines and automated driving cannot show their full power. It is important to combine them with work to enlarge and reshape paddy plots (land consolidation)
- **Radio signals**: in mountain paddies, mobile signals and RTK correction information may not reach
- **Connecting data**: each maker has its own app, making it hard to view data together. The government is building a platform for linking agricultural data (WAGRI)
- **Making good use of it**: even with the machines, the benefit is small unless you read the data and change how you farm. Young people and systems where people in the area teach each other are important

---

How to build and run your own drones and robots (ArduPilot and ROS 2) is covered in the "**ROS 2 and ArduPilot Textbook**".

## Exercises

```quiz
Q: Which four-letter index turns leaf color into a number for plant health, used by satellites and drones?
A: NDVI
E: It shows uneven growth across paddies and fields.

Q: Which method uses correction data from a base station to measure position to the centimeter?
A: RTK
E: Farmers use base stations run by JA or local governments, or network RTK from mobile companies.

Q: Which four letters name low-power, long-range radio such as 920 MHz LoRa?
A: LPWA
E: It links paddy water level sensors and automatic water valves.

Q: What do we call spreading different amounts of fertilizer in each part of a field, using a fertilizer map?
A: variable-rate fertilizing | variable-rate fertilization | variable rate | VRA
E: The map is made from uneven growth, soil tests and last year's yield map.
```
