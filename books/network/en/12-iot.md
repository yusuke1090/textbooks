# 12. IoT and the cloud (from sensor to cloud)

**IoT** (Internet of Things) means connecting sensors and machines to the internet to collect data or control them from far away. Barn temperatures, activity from cows' collars, soil moisture in fields and electricity meters all flow into the cloud. This chapter applies everything so far to the road from a sensor to the cloud.

## IoT networks are not like PC networks

| | PCs and phones | IoT devices |
| --- | --- | --- |
| Power | Mains power or charged every day | Often expected to run on batteries for years |
| Place | Homes and offices | Barns, fields, mountains, utility poles. Out of Wi-Fi range |
| Amount sent | Lots, such as video | A few dozen bytes of numbers every few minutes |
| Number of devices | A few per person | Hundreds or thousands |
| People | Nearby | Nobody around. Hard to notice when one breaks |

So IoT uses lines made for IoT, which reach far and use little power.

## Choosing how to connect

| Connection | Range | Speed / power use | Good for |
| --- | --- | --- | --- |
| **Wi-Fi** | Tens of meters | Fast / high | Inside homes and barns, cameras. Pico W, ESP32 |
| **Bluetooth (BLE)** | A few to tens of meters | Slow / very low | Devices that pair with a phone; from a collar to a nearby receiver |
| **LoRaWAN** | A few km to over ten km | Very slow / very low | Sensors on large farms and fields. Years on a battery |
| **LTE-M, NB-IoT** | Mobile base station coverage | Slow / low | One SIM per device, usable anywhere. Meters, monitoring |
| **4G, 5G** | Mobile base station coverage | Fast / high | Cameras, routers, remote control of machines |
| **Satellite** (Starlink etc.) | Anywhere with a view of the sky | Fast / very high | Farms, mountains and seas with no lines |

![LoRaWAN equipment (left: a soil moisture sensor; right: a gateway)](images/lorawan.jpg)

With **LoRaWAN**, sensors send small pieces of data by radio (920 MHz in Japan) to a nearby **gateway**. The gateway is connected to the internet by Wi-Fi, LAN or LTE and passes the data to a **network server** in the cloud.

![A LoRaWAN gateway mounted up high](images/lora-gateway.jpg)

![An electricity smart meter](images/smart-meter.jpg)

Japan's electricity **smart meters** are IoT too. They send usage every 30 minutes to the power company, and can talk to devices in the home over a radio system called Wi-SUN (920 MHz).

## From the farm to the cloud

![From farm sensors to the cloud](images/en/iot.svg)

1. Temperature and humidity sensors in the barn and the cows' collars take readings every few minutes
2. They send them over LoRaWAN, BLE or Wi-Fi to a **gateway** in the barn
3. The gateway sends the data through a fiber or LTE router to an **MQTT broker** (below) in the cloud
4. In the cloud, the data is stored in a **time-series database**, turned into graphs, and a phone is alerted when a value passes a set limit
5. Large data such as camera video is analyzed on the spot by a Jetson or similar in the barn (**edge computing**), and only the results are sent

## Why devices connect out

As Chapter 7 showed, nobody can connect directly from outside to devices behind the NAT of a home or barn router, or behind the CGNAT of a mobile network. So in IoT, the device connects out to the cloud and keeps that connection open. Commands from the cloud ("turn on the fan") come back through the same connection. **MQTT** was made for this.

## MQTT: a small protocol for IoT

In **MQTT**, devices do not talk to each other directly; everything goes through a **broker** in the middle. The sender **publishes** "this value, on this **topic**", and receivers **subscribe** in advance: "send me what is on this topic".

```text
farm/barn1/temp        temperature in barn 1
farm/barn1/humidity    humidity in barn 1
farm/barn2/temp        temperature in barn 2
farm/barn1/fan/set     command for barn 1's fan
```

- A topic is a name split by `/`. `+` matches one level and `#` matches everything below (`farm/+/temp` is the temperature in every barn; `farm/#` is everything)
- The header can be as small as 2 bytes, so it uses little power and bandwidth
- It runs on TCP and keeps the connection open. The port is 1883, or 8883 when encrypted with TLS

| Feature | Meaning |
| --- | --- |
| **QoS** | 0: send and forget; 1: delivered at least once (maybe twice); 2: exactly once |
| **Retain** | The broker keeps the last value and gives it at once to anyone who subscribes later |
| **Last Will** | If a device drops off suddenly, the broker sends a message set in advance (such as `offline`) on its behalf |
| **Keep alive** | Even with nothing to send, the device says "I'm alive" now and then |

| | HTTP | MQTT |
| --- | --- | --- |
| Shape | Ask → answer | Send → broker → everyone who wants it |
| Connection | One per exchange (or briefly kept) | Kept open |
| Commands from outside | Cannot reach the device (it must ask) | Arrive at once over the open connection |
| Size | Large headers | Small |

### Try it (Python)

Run a broker on your computer (on Ubuntu, `sudo apt install mosquitto mosquitto-clients` installs Mosquitto, which starts waiting on port 1883 straight away). Install the Python library with `pip install paho-mqtt`.

The receiver (`sub.py`):

```python
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, reason_code, properties):
    print("connected:", reason_code)
    client.subscribe("farm/+/temp", qos=1)    # receive the temperature from every barn


def on_message(client, userdata, msg):
    print(msg.topic, msg.payload.decode())


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883)
client.loop_forever()
```

The sender (`pub.py`):

```python
import json
import random
import time

import paho.mqtt.client as mqtt

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("localhost", 1883)
client.loop_start()

for i in range(3):
    temp = round(20 + random.random() * 5, 1)      # a real device would read its sensor
    info = client.publish("farm/barn1/temp", json.dumps({"temp": temp}), qos=1)
    info.wait_for_publish()
    print("sent:", temp)
    time.sleep(1)

client.loop_stop()
client.disconnect()
```

Open two terminals. Leave `python3 sub.py` running and run `python3 pub.py`; the values appear on the receiver.

```text
connected: Success
farm/barn1/temp {"temp": 21.1}
farm/barn1/temp {"temp": 23.3}
farm/barn1/temp {"temp": 23.8}
```

Change `localhost` to the Raspberry Pi's IP address and you can try it between a Raspberry Pi and a PC. With commands only, `mosquitto_sub -h localhost -t 'farm/#' -v` and `mosquitto_pub -h localhost -t farm/barn1/temp -m 21.5` do the same. A Pico W can send the same way with MicroPython's `umqtt` or with MQTT in C++ (lwIP in the Pico SDK).

## Cloud IoT services

| Approach | Examples |
| --- | --- |
| A cloud company's IoT service | AWS IoT Core, Azure IoT Hub (Google Cloud IoT Core ended in 2023) |
| Renting just an MQTT broker | HiveMQ Cloud, EMQX Cloud and others |
| Running your own | Install Mosquitto on a cloud server (Chapter 11) |
| Storing and viewing data | A time-series database (InfluxDB, TimescaleDB and others) with Grafana graphs |

Services such as AWS IoT Core give every device its own certificate (Chapter 9) and let it read and write, over TLS, only the topics it is allowed.

## Things to watch in IoT

- **A different key for every device**: if every device holds the same password, stealing it from one puts them all at risk
- **Encrypt**: use port 8883 (MQTT over TLS). Do not expose port 1883 to the outside
- **Design for dropouts**: barn connections drop. Keep data inside the device or gateway and send it when the connection comes back
- **Make remote updates possible**: so weaknesses can be fixed once found (**OTA** updates)
- **Keep the clock right**: to stamp data with the correct time, set it with NTP (Chapter 4) or GPS

## Summary

- IoT devices mean batteries, remote places, small data and large numbers. Choose from Wi-Fi, BLE, LoRaWAN, LTE-M, 4G/5G and satellite
- They sit behind NAT or CGNAT, so devices connect out to the cloud and keep the connection open
- MQTT publishes and subscribes to topics through a broker. Port 1883, or 8883 with TLS
- Analyze large data at the edge and send only the results. A key per device, encryption and designing for dropouts matter

## Exercises

```quiz
Q: In MQTT, what is the server in the middle that delivers messages between senders and receivers called?
A: broker | MQTT broker
E: Devices do not talk directly; they go through the broker.

Q: In MQTT, which topic do you subscribe to in order to receive the temperature from every barn (farm/barn1/temp, farm/barn2/temp …)?
A: farm/+/temp
E: `+` matches one level. `farm/#` would also give you everything other than temperature.

Q: Which port number is used when MQTT is encrypted with TLS?
A: 8883
E: Without encryption it is 1883.

Q: What is the message called that the broker sends on a device's behalf when it drops off suddenly?
A: Last Will | will | LWT | Last Will and Testament
E: Sending `offline` or similar tells other devices it has dropped off.

Q: Which radio system reaches several km or more and runs on batteries for years, suiting sensors on large farms and fields?
A: LoRaWAN | LoRa
E: In Japan it uses 920 MHz, and a gateway passes the data on to the internet.
```
