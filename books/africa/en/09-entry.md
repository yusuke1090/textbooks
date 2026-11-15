# 9. Comparing the three countries, and thinking about market entry

## Comparing the three countries

| Item | Tanzania | Kenya | Malawi |
| --- | --- | --- | --- |
| Population (census) | About 61.7 million (2022) | About 47.6 million (2019) | About 17.6 million (2018) |
| Business languages | Swahili, English | English, Swahili | English, Chewa |
| Cattle | About 39.2 million (about 1.41 million dairy) | About 2.2 million dairy, about 13 million native (2019) | About 55,000 dairy cattle |
| Milk per year | About 4.0 billion L | About 5.2 billion L | Only estimates (tens of millions of L) |
| Milk going through factories | 2–3% | About 20% | About half of milk sold goes through collection centers |
| Mobile money | M-Pesa, Mixx by Yas, Airtel | M-Pesa (82% of adults) | Airtel Money, Mpamba |
| Starlink | Not yet available | Available | Available |
| Personal data law | 2022 (foreign companies register too) | 2019 (register with the ODPC) | 2024 (MACRA) |
| Politics | Turmoil around the 2025 election; the internet was shut down | Frequent protests. Election in 2027 | Peaceful change of government in 2025 |
| In a word | Many cattle, but milk does not reach the factories | The most advanced, with the most competition | Small and difficult. Enter through aid projects |

### Where to start

- **Kenya is the safe first country**. The dairy system, payment methods, talent and investors are all in place, and you can test in English
- **For big growth, Tanzania**. It has many cattle and much milk, and cooling and collection are still to come. A system built in Kenya can be taken there as is, in Swahili
- **Malawi** is best thought of as a place to test cheap, tough devices, working with aid projects

## Hardware and system requirements

Devices made for Japanese farms will not work if you simply take them there. Match them to these conditions.

| Condition | Situation on the ground | How to build for it |
| --- | --- | --- |
| Electricity | Power cuts every day. Many places have no grid power | Run on solar panels and batteries. Record and report power cuts |
| Communications | Only 2G in rural areas, or no signal. The internet may be shut down | Send small amounts of data that work even over 2G. Store data while offline and send it when connected |
| Heat, dust, rain | Close to 40 °C in the daytime. Red dust. Heavy rain in the rainy season | Waterproof, dustproof enclosures. Mount them in the shade |
| Theft and breakdowns | Solar panels and batteries are easily stolen. Parts are hard to get | Mount them where they are hard to see. Use parts available locally so local people can repair them |
| Price | A small farmer can pay only a few hundred yen a month | Have cooperatives or dairies buy, not farmers. Or rent |
| Screens | Many people have no smartphone. Some find reading hard | Text messages, USSD, WhatsApp, voice. In Swahili and Chewa |
| Payment | Mobile money rather than banks | Use APIs such as M-Pesa's to receive fees and to pay farmers |

- When using radio such as LoRa, check the frequencies allowed in that country and type approval (CA in Kenya, TCRA in Tanzania, MACRA in Malawi)
- When using mobile networks, use a local SIM (Safaricom, Vodacom, Airtel and others) or an IoT SIM that works in several countries

## Ways to get paid

| Model | Example | Suited to |
| --- | --- | --- |
| Selling devices | Sell sensors and coolers | Medium and larger farms, dairies |
| Monthly fee (subscription) | Dashboards of collection data, cattle monitoring | Cooperatives, dairies |
| Pay per use | A fee for every liter cooled and carried (Savanna Circuit) | Cooperatives, farmer groups |
| Installments (PAYGo) | Pay daily or weekly by mobile money; the device stops if you do not pay | Farmers (solar pumps, refrigerators) |
| Paid from an aid project | Take charge of the devices and data in a World Bank, JICA or NGO project | Places with small markets, such as Malawi |

- Charging small farmers directly is very hard. Think about having **the people who gain when milk increases or quality improves** pay (cooperatives, dairies, feed and medicine companies, banks, insurers)
- Being able to show numbers — "milk increased by so many liters", "discarded milk fell by so many liters" — makes selling easier

## Steps toward entering the market

1. **Choose one problem**: "milk spoils at collection centers", "heat is missed" and so on. Something local people struggle with, where solving it makes someone money
2. **See it on the ground**: visit cooperatives, collection centers and farms. Talk to dairy staff, vets, artificial insemination technicians and farmers. You can also consult JICA's and JETRO's local offices
3. **Choose partners**: a cooperative or dairy (who pays), and local startups or engineers (who repair)
4. **Test small**: 3–6 months at one site. See whether the device works in the local heat, power cuts and signal conditions, and whether people keep using it
5. **Show it in numbers**: compare milk volume, discarded volume and income before and after the trial
6. **Company and paperwork**: set up a local company or partner with a distributor. Radio certification, personal data registration, import duties (Kenya and Tanzania share the EAC common tariff), work permits
7. **Expand**: other collection centers of the same cooperative → other regions of the same dairy → neighboring countries

## Using Japanese support

| Program | What it does for you |
| --- | --- |
| JICA private-sector partnership programs (SME and SDGs business support) | Money for surveys and demonstrations of products in developing countries, and coordination with local governments |
| JICA Project NINJA | Connects African startups with Japanese companies and investors |
| JETRO (offices in Nairobi, Johannesburg and elsewhere) | Market information, introductions to local companies, trade shows |
| TICAD | A summit every three years, with business meetings and exhibitions around it |

- Application periods and conditions change every year, so check each website

## Links to other books in this collection

- Cattle bodies, mastitis, silage and the basics of sensors: the [Dairy Cow Textbook](https://yusuke1090.github.io/textbooks/?b=cow)
- Building the sensor hardware: the [Raspberry Pi Pico Development Guide](https://yusuke1090.github.io/textbooks/?b=pico)

## Exercises

```quiz
Q: Which country does this book suggest as the safest first country?
A: Kenya
E: It has the dairy system, payments, people and investors, and you can work in English.

Q: Which country, with the most cattle and milk, is best for growing big?
A: Tanzania
E: Systems built in Kenya can be taken there in Swahili.

Q: Which country is best seen as a test bed for cheap, tough devices, working with aid projects?
A: Malawi
E: It is the hardest of the three to enter as a normal business.
```
