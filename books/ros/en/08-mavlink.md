# 8. MAVLink and pymavlink

## What is MAVLink?

- **MAVLink** is a small, lightweight **communication protocol** for drones to talk with ground stations and companion computers. ArduPilot, PX4 and many ground stations use it
- One message is a few dozen bytes. It is designed to work even over slow, unreliable radio links (telemetry). Today **MAVLink 2** is used
- It can run over serial (UART), UDP or TCP

| Term | Meaning |
| --- | --- |
| **System ID** (sysid) | A number for each vehicle (1–255). Ground stations are usually 255. When flying several vehicles, give each a different one (`SYSID_THISMAV`) |
| **Component ID** (compid) | A number for a part within one vehicle (autopilot 1, camera 100 and so on) |
| **HEARTBEAT** | An "I'm alive" signal. Everyone sends it once a second. It contains the vehicle type, mode and whether it is armed |
| Message | Data in a fixed format (position, attitude, battery...). Each has a number and a name |
| **COMMAND_LONG** | Commands such as "take off" or "change mode". An answer (**COMMAND_ACK**) comes back |

### Commonly used messages

| Message | Contents |
| --- | --- |
| `HEARTBEAT` | Vehicle type, mode (custom_mode), whether armed |
| `GLOBAL_POSITION_INT` | Latitude and longitude (integers ×10⁷), height (mm), velocity |
| `ATTITUDE` | Roll, pitch and yaw (radians) |
| `SYS_STATUS`, `BATTERY_STATUS` | Battery voltage and remaining charge, sensor status |
| `GPS_RAW_INT` | Number of GPS satellites, accuracy |
| `STATUSTEXT` | Text messages ("PreArm: ..." and so on) |
| `SET_POSITION_TARGET_LOCAL_NED` | In GUIDED, gives a position or velocity (**NED**) |
| `SET_POSITION_TARGET_GLOBAL_INT` | In GUIDED, gives a destination by latitude and longitude |
| `MISSION_ITEM_INT` and others | Sending and receiving missions (waypoints) |

- The list of messages and their contents is on the "common" and "ardupilotmega" pages of mavlink.io

## Driving it with pymavlink

**pymavlink** is a library for using MAVLink from Python (MAVProxy is built with pymavlink too).

```bash
python3 -m venv ~/mav-venv
source ~/mav-venv/bin/activate
pip install pymavlink
```

Run SITL (Chapter 7) and add one more MAVProxy output.

```text
output add 127.0.0.1:14560
```

`fly.py`:

```python
import time

from pymavlink import mavutil

# receive the MAVLink sent from SITL's MAVProxy
master = mavutil.mavlink_connection('udpin:127.0.0.1:14560')
master.wait_heartbeat()
print(f'Connected: system {master.target_system}, component {master.target_component}')


def set_mode(name):
    """Change mode by name (GUIDED, LAND and so on)"""
    mode_id = master.mode_mapping()[name]
    master.mav.set_mode_send(master.target_system,
                             mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, mode_id)


def command(cmd, *params):
    """Send COMMAND_LONG and wait for its answer (COMMAND_ACK). True if accepted"""
    p = list(params) + [0] * (7 - len(params))
    master.mav.command_long_send(master.target_system, master.target_component, cmd, 0, *p)
    end = time.time() + 5
    while time.time() < end:
        ack = master.recv_match(type='COMMAND_ACK', blocking=True, timeout=1)
        if ack is not None and ack.command == cmd:
            return ack.result == mavutil.mavlink.MAV_RESULT_ACCEPTED
    return False


# ask for the position message 5 times a second (every 200,000 microseconds)
command(mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
        mavutil.mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT, 200000)

set_mode('GUIDED')
while not command(mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 1):   # 1 arms, 0 disarms
    print('Cannot arm (GPS or EKF may still be getting ready). Waiting to try again...')
    time.sleep(2)
print('Armed')

command(mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 10)   # the 7th is the height (m)

while True:
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    alt = msg.relative_alt / 1000                                  # mm → m (height above home)
    print(f'Height {alt:.1f} m')
    if alt > 9.5:
        break

# north at 2 m/s for 5 seconds; set the bit mask (type_mask) meaning "use velocity only"
VELOCITY_ONLY = 0b110111000111
for _ in range(10):
    master.mav.set_position_target_local_ned_send(
        0, master.target_system, master.target_component,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, VELOCITY_ONLY,
        0, 0, 0,            # position (unused)
        2.0, 0, 0,          # velocity north, east, down (NED; to climb, make the down velocity negative)
        0, 0, 0,            # acceleration (unused)
        0, 0)               # yaw, yaw rate (unused)
    time.sleep(0.5)        # keep sending at intervals shorter than 3 seconds (GUID_TIMEOUT)

set_mode('LAND')
print('Landing')
```

```bash
python3 fly.py
```

- How to write `mavlink_connection`: `udpin:127.0.0.1:14560` (wait to receive), `tcp:127.0.0.1:5760` (directly to SITL), `/dev/ttyACM0` (a real vehicle over USB; add `baud=115200`)
- `recv_match(type=..., blocking=True)` waits until a message of the kind you want arrives
- **Keep sending velocity commands**: in GUIDED, if the next velocity command does not arrive within `GUID_TIMEOUT` (default 3 seconds), the vehicle stops. It is a safety mechanism so the vehicle does not fly off when your program stops
- **Watch out for NED**: MAVLink's LOCAL_NED has x north, y east and **z down**. It differs from ROS (ENU) (Chapter 5)

## Telemetry radios and routing

- A real vehicle and a ground station send MAVLink over a **telemetry radio** (a serial radio modem). On the vehicle side, it plugs into the FC's TELEM1
- **Use frequencies allowed in Japan and radios with Japanese technical conformity certification (giteki)**. The 915 MHz and 433 MHz radios commonly sold overseas cannot be used as they are in Japan (Chapter 12)
- When both the ground station and the companion computer want MAVLink, connect the companion computer to another FC serial port (TELEM2), or use **mavlink-router** to split one MAVLink stream to several places
- When working from ROS 2, rather than writing MAVLink directly, you normally use **AP_DDS** from Chapter 9 (or MAVROS). Even so, knowing MAVLink helps you understand what is happening inside when you are stuck

## Exercises

```quiz
Q: Which "I'm alive" message does everyone send once per second?
A: HEARTBEAT | heartbeat
E: It carries the vehicle type, mode and armed state.

Q: What system ID does a ground station usually use?
A: 255
E: Vehicles use 1–255; give each vehicle a different ID when flying several.

Q: Which Python library is used to work with MAVLink?
A: pymavlink
E: MAVProxy is built on pymavlink too.

Q: By default, how many seconds without a new GUIDED velocity command before the vehicle stops?
A: 3
E: `GUID_TIMEOUT`. It stops the vehicle flying away if your program dies.
```
