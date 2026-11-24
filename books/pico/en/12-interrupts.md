# 15. Interrupts, timers and two cores

This assumes you understand the "no-waiting style" in Chapter 14.

## What is an interrupt?

There are two ways to read a button.

| Method | How it works | Good points | Cautions |
| --- | --- | --- | --- |
| Polling | Go and read the pin again and again inside a loop | Easy to understand | Misses changes shorter than the reading interval. Always running, so it uses power |
| Interrupt | The moment the pin changes, the Pico pauses what it is doing and calls a function you chose | Misses nothing. It can rest while waiting | Keep the interrupt function short. Be careful when passing data |

The function called by an interrupt is called an **interrupt handler** (callback).

## Acting the moment a button is pressed

Count how many times the USR button (GP24) is pressed.

```cpp run
#include <cstdio>
#include "pico/stdlib.h"

constexpr uint BTN_PIN = 24;

volatile uint32_t press_count = 0;     // mark variables changed in interrupts as volatile
volatile uint32_t last_press_ms = 0;

// called when the button is pressed (an interrupt handler). gpio is the pin number, events is what happened
void on_button(uint gpio, uint32_t events) {
    if (gpio != BTN_PIN || !(events & GPIO_IRQ_EDGE_FALL)) return;   // ignore other pins and anything but a press
    uint32_t now = to_ms_since_boot(get_absolute_time());
    if (now - last_press_ms < 50) return;          // ignore a second one within 50 ms as contact bounce
    last_press_ms = now;
    press_count++;
}

int main() {
    stdio_init_all();
    gpio_init(BTN_PIN);
    gpio_set_dir(BTN_PIN, GPIO_IN);
    gpio_pull_up(BTN_PIN);
    // call on_button when it changes from 1 to 0 (when pressed)
    gpio_set_irq_enabled_with_callback(BTN_PIN, GPIO_IRQ_EDGE_FALL, true, &on_button);

    uint32_t shown = 0;
    while (true) {
        if (press_count != shown) {                // do printf outside the interrupt
            shown = press_count;
            printf("times pressed: %u\n", static_cast<unsigned>(shown));
        }
        sleep_ms(10);
    }
}
```

| Code | Meaning |
| --- | --- |
| `gpio_set_irq_enabled_with_callback(pin, kind, true, &function)` | Enables the pin's interrupt and sets the function to call |
| `GPIO_IRQ_EDGE_FALL` | When it changes from 1 to 0 (when a pull-up button is pressed) |
| `GPIO_IRQ_EDGE_RISE` | When it changes from 0 to 1 (when released). You can specify both with `\|` |
| `volatile` | A marker meaning "this variable may change at any time". Without it, `main` may keep seeing an old value |

> There is **one interrupt handler for all pins**. Enable a second pin with `gpio_set_irq_enabled(pin, kind, true)`, and tell them apart inside the handler by looking at the `gpio` argument.

## What you must not do inside an interrupt

While an interrupt handler runs, `main` is stopped. Other interrupts are kept waiting too.

| Do not | Why |
| --- | --- |
| `printf` | Takes time, and can clash with USB processing |
| Waits such as `sleep_ms` | Everything stops meanwhile |
| Long calculations, long loops | The same |
| `new` / `malloc` | Using them at the same time as `main` can corrupt things |

In the handler, **only read values and put them in variables or buffers**; do the heavy work in `main`.

## Acting precisely at fixed intervals

In Chapter 12, the interval was kept even with `sleep_until`, but if other work in the loop (classification or sending) takes time, the next measurement is late.
With a **repeating timer**, a function is called at fixed intervals even while other work is going on.

The following program reads the MPU-6050 at 100 Hz (every 10 ms), and `main` prints the average every second.
The values read are passed from the interrupt to `main` through a **ring buffer**.

```cpp run
#include <cstdio>
#include "pico/stdlib.h"
#include "hardware/sync.h"
#include "mpu6050.h"

// a circular container for passing data between an interrupt (writer) and main (reader)
template <typename T, int N>
class RingBuffer {
public:
    bool push(const T& v) {                    // called from the interrupt
        int next = (head_ + 1) % N;
        if (next == tail_) return false;       // full (the reader is falling behind)
        buf_[head_] = v;
        head_ = next;
        return true;
    }
    bool pop(T& v) {                           // called from main
        uint32_t irq = save_and_disable_interrupts();   // stop interrupts only while taking one out
        bool ok = tail_ != head_;
        if (ok) {
            v = buf_[tail_];
            tail_ = (tail_ + 1) % N;
        }
        restore_interrupts(irq);
        return ok;
    }

private:
    T buf_[N];
    volatile int head_ = 0, tail_ = 0;
};

struct Sample { float ax, ay, az; };

Mpu6050 mpu(i2c0);
RingBuffer<Sample, 256> samples;               // can hold 2.5 seconds' worth
volatile uint32_t dropped = 0;

// called every 10 ms
bool on_timer(repeating_timer_t*) {
    Sample s;
    if (mpu.read_accel(s.ax, s.ay, s.az) && !samples.push(s)) dropped++;
    return true;                               // returning true makes it repeat
}

int main() {
    stdio_init_all();
    mpu.begin(4, 5);

    repeating_timer_t timer;
    add_repeating_timer_ms(-10, on_timer, nullptr, &timer);   // -10 = every 10 ms from the previous start

    float sum = 0;
    int n = 0;
    absolute_time_t next = make_timeout_time_ms(1000);
    while (true) {
        Sample s;
        while (samples.pop(s)) {               // take out everything that has built up
            sum += s.az;
            n++;
        }
        if (absolute_time_diff_us(get_absolute_time(), next) <= 0) {
            printf("%d times in 1 s  mean z %.3f g  dropped %u\n", n, n ? sum / n : 0.0f,
                   static_cast<unsigned>(dropped));
            sum = 0;
            n = 0;
            next = delayed_by_ms(next, 1000);
        }
        sleep_ms(5);
    }
}
```

Every second it shows something like this.

```text
100 times in 1 s  mean z 1.002 g  dropped 0
```

| Code | Meaning |
| --- | --- |
| `add_repeating_timer_ms(-10, function, nullptr, &timer)` | Calls the function every 10 ms. Negative means "from the previous start", positive means "from the previous end" |
| `bool on_timer(repeating_timer_t*)` | The function called by the timer. Returning `false` stops it |
| `repeating_timer_t timer;` | The timer's information. Put it **somewhere that does not disappear while it runs** (inside `main` is fine, since `main` never ends) |
| `RingBuffer<Sample, 256>` | A container that can hold up to 256 `Sample`s. When full, it throws away the new one and counts it |
| `save_and_disable_interrupts()` | Stops interrupts for a short time so that an interrupt arriving mid-removal does not put `head_` and `tail_` out of step |

- The I2C read (about 0.2 ms for 6 bytes) is done inside the interrupt. 0.2 ms is fine, but for work that takes longer, just set a flag and do it in `main`
- To call something only once, use `add_alarm_in_ms(ms, function, nullptr, false)`

## Using the two cores

The Pico's chip has two cores and can truly run two pieces of work at the same time. `main` runs on core 0, and the other is core 1.
In the following program, core 1 takes care of measuring and core 0 takes care of printing.

```cpp run
#include <cstdio>
#include <cstring>
#include "pico/stdlib.h"
#include "pico/multicore.h"
#include "mpu6050.h"

Mpu6050 mpu(i2c0);

// core 1: measure at 50 Hz and send the "amount of movement" every second to core 0
void core1_main() {
    mpu.begin(4, 5);
    absolute_time_t next = get_absolute_time();
    float sum = 0;
    for (int n = 1;; n++) {
        float ax, ay, az;
        if (mpu.read_accel(ax, ay, az)) sum += (ax * ax + ay * ay + az * az);   // add only when read successfully
        if (n % 50 == 0) {
            float mean = sum / 50;
            uint32_t bits;
            memcpy(&bits, &mean, 4);               // send the float as a 32-bit number
            multicore_fifo_push_blocking(bits);
            sum = 0;
        }
        next = delayed_by_ms(next, 20);
        sleep_until(next);
    }
}

int main() {
    stdio_init_all();
    multicore_launch_core1(core1_main);            // start running core1_main on core 1

    while (true) {
        uint32_t bits = multicore_fifo_pop_blocking();   // wait until something arrives from core 1
        float mean;
        memcpy(&mean, &bits, 4);
        printf("amount of movement (mean squared acceleration): %.3f\n", mean);
    }
}
```

| Code | Meaning |
| --- | --- |
| `multicore_launch_core1(function)` | Runs the function on core 1. Make sure the function never ends |
| `multicore_fifo_push_blocking(number)` | Sends a 32-bit number to the other core. If full, waits until there is room |
| `multicore_fifo_pop_blocking()` | Receives a number that has arrived. Waits until one arrives |
| `memcpy(&bits, &mean, 4)` | Copies the contents of a `float` as is into a `uint32_t` (no value conversion) |

### Sharing data between the cores

The FIFO can hold only 8 items. When sharing large data, share variables and **lock them so they are not touched at the same time (a critical section)**.

```cpp
#include "pico/sync.h"

critical_section_t lock;
float shared_features[8];

// once at the start: critical_section_init(&lock);

// writer (core 1)
critical_section_enter_blocking(&lock);
memcpy(shared_features, fe, sizeof(fe));
critical_section_exit(&lock);

// reader (core 0)
critical_section_enter_blocking(&lock);
memcpy(fe, shared_features, sizeof(fe));
critical_section_exit(&lock);
```

### Things to watch out for with two cores

- Use `printf` from only one core. If both use it, characters can get mixed up
- Do not use the same I2C unit from both cores. Leave the sensors to one core
- When writing to flash (Chapters 16 and 18), the other core must also be stopped. Call `multicore_lockout_victim_init()` on core 1, and on the writing side, wrap the write with `multicore_lockout_start_blocking()` and `multicore_lockout_end_blocking()`

## Which to use

| What you want to do | Method |
| --- | --- |
| Move several things forward at roughly regular intervals | The state machine in Chapter 14 (look at the time and move on) |
| Never miss a button or sensor signal | GPIO interrupts |
| Measure precisely at fixed intervals | A repeating timer + a ring buffer |
| Truly run heavy computation (such as classification) and measurement at the same time | The two cores |
| Take data even faster (tens of kHz or more) | DMA (a circuit that moves data without using the CPU). [adc/dma_capture in pico-examples](https://github.com/raspberrypi/pico-examples/tree/master/adc/dma_capture) |

## Summary

- An interrupt is a way to have a function called the moment a signal changes or at a set time
- GPIO uses `gpio_set_irq_enabled_with_callback`; repetition uses `add_repeating_timer_ms`
- Mark variables changed in interrupts as `volatile`. Keep handlers short, with no `printf` or waiting
- Pass data between interrupts and `main` with a ring buffer. Stop interrupts only while taking data out
- Use the two cores with `multicore_launch_core1`. Pass data through the FIFO or locked shared variables

## Exercises

```quiz
Q: Which keyword do you add to variables changed inside an interrupt?
A: volatile
E: Keep handlers short, with no `printf` or waiting.

Q: Which function calls your function at a fixed interval?
A: add_repeating_timer_ms
E: GPIO interrupts use `gpio_set_irq_enabled_with_callback`.

Q: How many CPU cores does the Pico have?
A: 2 | two
E: Start the second core with `multicore_launch_core1`.

Q: What circular buffer passes data between interrupts and `main`?
A: ring buffer | circular buffer
E: Disable interrupts only while taking data out.
```
