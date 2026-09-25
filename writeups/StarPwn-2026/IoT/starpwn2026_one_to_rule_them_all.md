# STARPWN 2026 — One to Rule Them All (Communications & RF, 500)

**Flag:** `starpwn{Allegiant_Stadium}`

## TL;DR
A 16 KB ArduPilot flight-controller EEPROM dump whose mission waypoints are **relative
coordinate offsets**. The challenge is an *application_target*: a live drone swarm
broadcasts MAVLink telemetry on a TCP port + a Web UI (`/api/state`, `/ws/telemetry`).
Calibrating the EEPROM's raw bytes against the live drone's GPS positions reveals the
encoding `lat = base + s16(XX YY)/1e7`, `lon = base + u16(ZZ WW)/1e7`, whose absolute
anchor (orbit center + SetROILocation home) is **Allegiant Stadium** in Las Vegas.

## Challenge Data
- `eeprom.bin` (16384 bytes): ArduPilot Copter EEPROM.
  - 0x0000–0x00DE: `PA` magic + AP_Param records (FORMAT_VERSION=120, sentinel @0xDE).
  - 0x0600–0x0952: bb-delimited 15-byte mission records (55 items).
  - 0x0FD0: `eb 00 00 00 63 00 00 00` (footer/decoy).
  - 0x1F80: 48-byte blob (decoy — resisted XOR/RC4/AES/XTEA/ChaCha with all keys).
  - Only ASCII string: `doM8H` (inside a VECTOR3F-typed param — decoy password).
- Live target (application_target):
  - Web UI: `starpwn-<instance>.chals.io` → "PRISMANTIR SWARM" telemetry dashboard.
  - `MAVLink Telemetry`: `tcp:0.cloud.chals.io:24387` (heartbeats, TIMESYNC, MISSION_ITEM_REACHED only).
  - REST: `/api/config`, `/api/state`; WS: `/ws/telemetry`.

## Mission structure (55 items)
| # | MAV_CMD byte | Meaning |
|---|--------------|---------|
| 1 | 0x16 (22) | NAV_TAKEOFF |
| 2 | 0x10 (16) | NAV_WAYPOINT |
| 3 | 0xc3 (195) | DO_SET_ROI_LOCATION (home) |
| 4–54 | 0x10 / 0xcb (203 DigiCamCtrl at 8) | 51 waypoints |
| 55 | 0xb1 (177) | DO_JUMP (loops) |

## The coordinate trap (WRONG first model)
Naively reading the 7-byte waypoint chunk `XX YY [83|82] 15 ZZ WW 58` as
`lat = [ZZ WW 58]/160000 (absolute), lon = s16(XX YY) offset` produces a ~11 km
"circle" centered at Desert Shores, Las Vegas — plausible-looking but a decoy
(Desert Shores Villas / Lake Jacqueline were red herrings).

## The real encoding (calibrate against the live drone!)
- Poll `/api/state` ~0.6 s while agent sysid=1 (55-item mission == the EEPROM) flies its
  waypoints (~4 s per waypoint); record `(mission.sequence, position)` where `distance_m≈0`.
- Correlate EEPROM raw byte columns with the live GPS waypoint offsets (both 1e-7 deg units):
  - `lat_off = s16(XX YY)`  (signed 16-bit LE, corr 0.999)
  - `lon_off = u16(ZZ WW)`  (unsigned 16-bit LE, corr 0.999)
  - circle center in offset space: (dxy 645.5, u16zw 27541.5)
- Absolute: `lat = 36.090743 + (s16(XX YY) − 645.5)/1e7`,
  `lon = −115.183329 + (u16(ZZ WW) − 27541.5)/1e7`.
- Verified: predicted wp0 (36.092084, −115.183120) matches live seq-4 position
  (36.092082, −115.183141) to ~2 m.

## Landmark
- Orbit center = SetROILocation home = `(36.090743, −115.183329)`.
- Nominatim reverse (zoom 18) → **Allegiant Stadium**.
- Overpass (kumi mirror) polygon: `Allegiant Stadium` bounds
  lat 36.089446–36.092024, lon −115.184750–−115.181912 — both points inside.
- Flag (place-name convention, cf. Deadly Parade `starpwn{Echo_Trail_Park}`):
  `starpwn{Allegiant_Stadium}`.

## Notes / gotchas
- The MAVLink TCP port ignores MISSION_REQUEST_LIST (read-only telemetry bridge).
- The 48-byte blob + `doM8H` are decoys (flag regex `[A-Za-z_]` rules out digits anyway).
- Overpass main endpoint 406s urllib → use `https://overpass.kumi.systems/api/interpreter`.
- `application_target` type ⇒ the live instance is mandatory; the EEPROM is only half the puzzle.
