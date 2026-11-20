# 17. The real development flow

This chapter is an example plan using a cow behavior classification system. The numbers are rough guides to explain the ideas, and have not been tested on real cows.

## The overall system

In real development, you build a flow of "read → compute → transmit → view".
But you do not do it all on one microcontroller. **You divide it into three roles.**

```text
Collar microcontroller   Barn receiver            Phone / PC
(battery powered)        (plugged in)             (barn Wi-Fi)

 Measure                  Receive                  View
 Compute     -- radio --> Store       -- Wi-Fi --> Get alerts
 Classify behavior        Find heat/illness candidates
 Send
```

| Place | Role | Program that runs |
| --- | --- | --- |
| Collar microcontroller | Measure, classify behavior, send results | A C++ program (`collar.cpp`) |
| Barn receiver | Receive, store, classify across days, show screens | A service on a Raspberry Pi |
| Phone / PC | View | A browser |

It does not send directly to a phone, because there is not always a phone near the cow. The receiver keeps receiving and storing, so you can look at everything later.

### Splitting classification into two stages

| Classification | Where | Example | Data needed |
| --- | --- | --- | --- |
| Behavior | Collar | Is it now resting, eating, walking or ruminating? | A few seconds of acceleration |
| Condition | Receiver | Signs of heat, suspected illness | Several days of behavior records |

Heat and illness can only be recognized by comparing with that cow's usual behavior. So they are classified on the receiver, where the records are kept.

### Send only the results

Sending the acceleration as is increases the amount of data and drains the battery. Classify inside the collar and send only a summary every minute.

```text
Raw data:     25 per second x 3 axes x 60 seconds = 4500 numbers
Data to send: cow ID, resting 40 s, eating 20 s, walking 0 s, ruminating 0 s
```

## The shape of the collar's program

In a product, the collar's program is written in C++. Its shape is the following loop. Measuring is based on Chapter 10, classification on Chapter 15, and making the battery last on Chapter 16.
The code below shows the shape and will not run as is.

```text
#include "model.h"                 // the classification code made in Chapter 15

int main() {
    stdio_init_all();
    watchdog_enable(5000, true);   // restart if no response for 5 s (Chapter 16)
    init_sensor();
    init_radio();

    while (true) {
        read_window(samples);          // read 2 seconds of acceleration
        make_features(samples, fe);    // turn it into features
        counts[label_index(predict(fe))]++;   // classify and add to the tally

        if (one_minute_passed()) {
            send(counts);              // send to the receiver every minute
            reset_counts();
        }
        watchdog_update();             // report "I'm alive"
        sleep_until_next_window();     // wait for the next measurement at low power (Chapter 16)
    }
}
```

Things to think about when making it a product are collected in Chapter 18.

## The order of development

Do not build everything at once; check things one at a time in this order.

| Order | What to do | Where | Related chapters |
| --- | --- | --- | --- |
| 1 | Decide what you want to report | At the desk | This chapter |
| 2 | Read the sensor | At the desk | Chapters 7, 10 |
| 3 | Record data in flash | At the desk | Chapter 14 |
| 4 | Put it on a cow and collect data and video | In the barn | Chapter 14 |
| 5 | Build the behavior classification | PC | Chapter 15 |
| 6 | Send by radio | At the desk, in the barn | This chapter |
| 7 | Store on the receiver | In the barn | Appendix C |
| 8 | Make the screen to view on a phone | In the barn | This chapter |
| 9 | Find heat and illness candidates | Receiver | This chapter |
| 10 | Test on several cows for a long time | In the barn | This chapter |
| 11 | Refine the battery, case and cost | Everything | This chapter |

### 1. Decide what you want to report

First decide who wants to know what. Once this is decided, what to measure and what to classify follow.

| What to report | Example of changes to watch |
| --- | --- |
| Signs of heat | Activity increases above that cow's usual level |
| Suspected illness | Rumination, eating and activity fall below usual |

### 4. Put it on a cow and collect data and video

This is the most important step and takes the most time. To build a classifier, you need the right answer: "what was the cow doing at this time?"

1. Put the collar on a cow and record acceleration in flash (Chapter 14)
2. Film the same period on video. Match the times of the microcontroller and the video
3. Watch the video and label the behavior for each period
4. Collect from several cows, not just one

When the cow's body or the way the collar is fitted changes, the data changes too. Decide how to fit it without burdening the cow together with the people who look after the cows.

### 5. Build the behavior classification

Make a decision tree with the steps in Chapter 15. The example in Chapter 15 has three kinds: resting, walking and eating. To classify rumination, collect rumination data and add more kinds.

Check the classifier's scores **on data from cows not used for training**. If you check only with data from the same cows, you will not notice that it fails on other cows.

### 6. Send by radio

Radio requires a board with wireless, such as the Pico W. First check whether radio signals reach inside the barn. Metal fences and the cows' bodies weaken them.

| Method | Rough range | Power | Good when |
| --- | --- | --- | --- |
| BLE | Tens of meters | Small | You can put the receiver inside the barn |
| LoRa | Hundreds of meters to several km | Small | Large areas such as pasture. Only small amounts can be sent |
| Wi-Fi | Tens of meters | Large | Prototypes. Not suited to running long on batteries |

> In Japan, devices that transmit radio need *giteki* certification. Check this when buying boards and modules.

### 7–8. The receiver and the phone screen

Use a Raspberry Pi as the receiver and run the following programs as services (Appendix C).

- Receive the radio signals and store them in a database (SQLite or the like)
- Show graphs and lists for each cow with a small web server

Even without the internet, if your phone connects to the barn's Wi-Fi, you can open the receiver's screen in a browser. No cloud is used, so there are no data charges.

Without the internet, phone push notifications are hard to use. Instead, think about checking the screen, or putting a buzzer or lamp in the barn.

### 9. Find heat and illness candidates

On the receiver, compare the cow's past records with now.

1. Total the activity and rumination time for each hour
2. Compare with the average for the same time of day over the past few days
3. If it is far off, report it as a candidate

Starting with this comparison, without machine learning, is recommended. The reasons are easy to explain, and it is easy to fix.

The result is not a diagnosis but **an alert for a person to check**. The final judgment is made by the people who look after the cows, or a veterinarian.

### 10. Test on several cows for a long time

Put collars on several cows and test for weeks to months. Compare the alerts with records of actual heat and illness.

| Number to watch | Meaning |
| --- | --- |
| Misses | There really was heat or illness, but no alert was given |
| False alarms | An alert was given, but nothing was wrong |

Trying to reduce misses increases false alarms. Decide together with the users how much is acceptable in practice.

### 11. Refine the battery, case and cost

**Battery:** the average current decides how long it lasts.

```text
Battery capacity / average current = running time

2000 mAh / 30 mA  = about 67 hours (about 3 days)
2000 mAh / 1 mA   = 2000 hours (about 83 days)
2000 mAh / 0.2 mA = 10000 hours (about 14 months)
```

The Pico uses tens of mA while running. As is, a battery lasts only a few days. To make it last for months, you need the following.

- Put the microcontroller to sleep while not measuring
- Keep the time the radio is in use as short as possible
- Measure the actual current to check

The Pico is good for prototypes, but it is a board with high power consumption. For practical use, also consider switching to a low-power microcontroller with BLE. In that case, the classification approach and the receiver can be used as they are.

**Case:** you need a case that withstands rain, manure and cows bumping into things. Pay attention to battery safety too.

**Cost:** estimate parts, the case, assembly, the receiver and replacements when things break.

**If you sell it:** besides radio certification, check in advance with experts how the law treats a product that claims to detect illness.

## A list of things to decide

| Item | Options | How to check |
| --- | --- | --- |
| Where to attach | Neck, leg, ear | Test whether the behaviors you want to classify can be seen, and how much burden it puts on the cow |
| Radio | BLE, LoRa, Wi-Fi | Measure whether signals reach in the barn |
| Battery | Capacity and replacement interval | Measure the average current and calculate |
| Classification | Kinds of behavior, how candidates are found | Compare with records |

The movements that are easy to see depend on where it is attached. The neck is thought to suit rumination and eating, which are linked to jaw movement, and the leg suits counting steps. Decide by actually testing.

## Summary

- In real development, divide the roles into three: measuring, collecting and viewing
- The collar's program repeats read → compute → classify → send
- Heat and illness are judged on the receiver, where records are kept, by comparing with that cow's usual behavior
- The most important thing is collecting labeled data on cows
- The Pico is good for prototypes. Running for months on batteries needs extra work or a different board
- The result is not a diagnosis but an alert for a person to check

## Exercises

```quiz
Q: The collar program loops "read → calculate → ? → send". What is "?"?
A: judge | classify | decide | judgement
E: Send only the results, to save battery.

Q: To detect heat or illness, what do you compare a cow's data with?
A: her usual behavior | usual | normal | her normal behavior | usual behavior
E: A receiver keeps records and compares with the cow's usual behavior.

Q: The most important thing is to collect data from cows with what attached?
A: correct labels | labels | answers | correct answers
E: Record the true behavior, together with video.

Q: Is the result a diagnosis, or an alert for a person to check?
A: alert | an alert | notice
E: It is not a diagnosis. A person makes the final check.
```
