# 12. Safety and law

## What you will learn in this chapter

- Safety rules before operating real hardware
- Handling LiPo batteries
- Japan's drone laws (the Civil Aeronautics Act, the Small Unmanned Aircraft Flight Prohibition Act)
- Radio law (the Radio Act, technical conformity certification)
- Rules for spraying pesticides, and for rovers

The legal information in this chapter was researched in November 2026. Laws and procedures change often, so check the pages of the Ministry of Land, Infrastructure, Transport and Tourism (MLIT) and the Ministry of Internal Affairs and Communications before flying.

## Safety rules

- Try it on real hardware **only after testing everything in simulation**. Every new program starts in SITL
- On the desk, **remove the propellers**. Propellers cut fingers and can even break bones
- Make sure **you can switch back to manual with the transmitter at any time**. Decide the switches for LOITER (Copter), HOLD (Rover) and RTL, and practice until you can flip them with your eyes closed
- Always set a **geofence** (height and range) and **failsafes** (RC, GCS, battery, EKF), and check how they behave in SITL (Chapter 6)
- Prepare an **emergency stop** switch that stops the motors (assign "Motor Emergency Stop" to an RC auxiliary channel)
- Keep away from people, cars and buildings. Watch for wind (be careful above 5 m/s at ground level), rain, power lines and birds
- Make a pre-flight checklist (propellers, screws, battery, number of GPS satellites, compass, modes, failsafes) and go through it every time
- Keep the logs every time (DataFlash, ros2 bag). If something happens, look at the logs first

## LiPo batteries

![Charging a LiPo battery. A dedicated balance charger charges while keeping each cell's voltage equal](images/arducopter-early.jpg)

- LiPo (lithium polymer) batteries are light and give high current, but **they burn if mishandled**
  - Charge with a dedicated **balance charger**, without taking your eyes off it, inside a fire-resistant bag (LiPo bag)
  - Do not use them below 3.0–3.3 V per cell (it damages the battery and makes it swell). Set `BATT_LOW_VOLT`
  - When not in use, keep them at a **storage voltage** of about 3.8 V per cell. Do not leave them fully charged
  - Do not use swollen or damaged batteries. Dispose of them following your local government's rules

## The Civil Aeronautics Act (drone rules)

- Drones and radio-controlled aircraft weighing **100 g or more** are "**unmanned aircraft**" and must follow the Civil Aeronautics Act (the weight includes the battery)

### Registration and Remote ID

- Unmanned aircraft must be **registered** with the national government (MLIT) (since June 2022). Display the registration code on the aircraft and fit **Remote ID** (a device that broadcasts the aircraft's number by radio)
- Home-built aircraft are the same. ArduPilot aircraft also need registration and Remote ID (ArduPilot can work with Remote ID devices)
- The procedures are done on MLIT's **DIPS 2.0** (Drone/UAS Information Platform System)

### Specified flights

The following kinds of flight are "**specified flights**", and need national **permission or approval** (applied for on DIPS 2.0), or **aircraft certification** plus a **pilot competency certificate** (first- or second-class unmanned aircraft pilot).

| Place (airspace) | Way of flying |
| --- | --- |
| Around airports | At night |
| 150 m or more above the ground | Where you cannot see it (beyond visual line of sight) |
| Over densely inhabited districts (DID) | Less than 30 m from people or objects |
| Emergency operation airspace | Over places where people gather, such as festivals |
| | **Carrying dangerous goods** (pesticides and so on) |
| | **Dropping objects** (spraying pesticides, fertilizer or seed) |

- When **flying automatically with ROS 2** too, the basics are to stay within sight and be able to switch back to manual at once. Automatic flight beyond visual line of sight has stricter conditions for permission and approval
- Before flying, file a **flight plan notification** on DIPS 2.0 and keep a flight **log book** (for specified flights)
- Flying after drinking alcohol and dangerous flying are always prohibited. If an accident happens, you must report it to the government
- Changes in 2026
  - March: flights over exclusively industrial zones within densely inhabited districts no longer need permission
  - June: the limit on how many aircraft one pilot may fly at once (5 beyond visual line of sight) was removed
  - July 14: the **Small Unmanned Aircraft Flight Prohibition Act** was amended. The no-fly zone around important national facilities (the Diet, the Prime Minister's Office, defense facilities, airports, nuclear power plants, embassies and so on) widened from about 300 m to **about 1 km** (aircraft under 100 g are covered too)

## The Radio Act (technical conformity)

- Devices that emit radio waves in Japan need the **technical conformity mark** (giteki), showing they meet Japanese standards. Using a radio without it violates the Radio Act
- Radio used by drones

| Frequency | Use | What you need |
| --- | --- | --- |
| **2.4 GHz** | Transmitter (RC), Wi-Fi, telemetry | With certified devices, no license or qualification |
| **920 MHz** | Telemetry (specified low power) | With certified devices, none |
| **5.7 GHz** | Video and data (unmanned mobile image transmission system) | A radio station **license** and a **Third-Class On-Land Special Radio Operator** qualification or higher |
| 169 MHz | Long-range control and data | A radio station license and Third-Class On-Land Special Radio Operator or higher |
| 5.8 GHz (amateur radio) | Hobby FPV video | An amateur radio license. **Cannot be used for work** |
| Mobile phone (LTE, 5G) | Remote control and video from afar | A carrier plan for "use in the air" |

- **Telemetry radios sold overseas (915 MHz and 433 MHz SiK radios and so on) cannot be used in Japan**. Choose certified 920 MHz or 2.4 GHz products
- The companion computer's Wi-Fi and Bluetooth are radio too. Use Wi-Fi modules on the Raspberry Pi or Jetson that have the conformity certification

## Spraying pesticides

![Spraying with an agricultural drone (DJI Agras T50). Spraying pesticide counts as "carrying dangerous goods" and "dropping objects" under the Civil Aeronautics Act](images/agras-spray.jpg)

- Civil Aeronautics Act: spraying pesticides counts as "**carrying dangerous goods**" and "**dropping objects**", so permission and approval (or aircraft certification and a competency certificate) are needed
- **Agricultural Chemicals Control Act**: use only pesticides registered for drone application, at the concentration, amount, number of times and timing on the label. Take care that it does not drift onto neighboring fields, houses or waterways
- Local rules: you are often expected to notify neighboring farmers and residents before spraying. Also see the Ministry of Agriculture, Forestry and Fisheries' guidelines on "aerial pesticide application by unmanned multicopters"
- Read Chapter 12 (smart agriculture) of the "Field Crops and Rice Textbook" as well

![An agricultural drone over rice paddies in Aomori Prefecture](images/drone-aomori.jpg)

## Rovers (robots that drive on the ground)

- Inside your own farm (private land), you need no national permission to drive one
- Driving on **public roads** is subject to rules on license plates, safety standards, drivers and more (the Road Transport Vehicle Act, the Road Traffic Act), and is normally not possible. Small robots that drive on sidewalks have a separate notification system (remote-controlled small vehicles)
- For autonomous farm machinery (robot tractors), there are the Ministry of Agriculture, Forestry and Fisheries' "Guidelines for ensuring the safety of autonomous driving of agricultural machinery". Requirements include a person watching nearby and stopping when a person is detected
- Heavy vehicles cause serious injuries if they hit someone. Limit the speed (with parameters) and fit an emergency stop button

## Exercises

```quiz
Q: From what weight (g) is a drone an "unmanned aircraft" under Japan's Civil Aeronautics Act?
A: 100
E: The weight includes the battery.

Q: What is the device that broadcasts a drone's registration number by radio?
A: remote ID | RID
E: Register through MLIT's DIPS 2.0.

Q: Which Japanese certification mark must radio equipment have?
A: Giteki | technical conformity mark | giteki mark
E: Using uncertified radios breaks the Radio Act.

Q: When not in use, to about how many volts per cell should a LiPo battery be stored?
A: 3.8
E: Do not leave it fully charged.

Q: Spraying pesticide by drone counts as "carrying dangerous goods" and what else under the aviation law?
A: dropping objects | dropping | dropping things
E: You need permission and approval, or type certification and a pilot license.
```
