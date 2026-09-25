# Deadly Parade — STAR PWN 2026 (Communications & RF)

## Challenge
> Prismantir was assigned to protect a VIP during DynaCon's parade... The sky above the Glittercity was tuned to a dead channel. No one realized what was happening until Prismantir's drones began falling from the sky like ducks. Your mission is to find where these deadly toys could have been hiding.
>
> **Flag**: `starpwn{[A-Za-z_]+}` (e.g. `Empire State Building` → `starpwn{Empire_State_Building}`)

**Flag**: `starpwn{Echo_Trail_Park}`

## Files
- `PRISM_S05_DNCN_20260831.pcap` (207.7 MB) — MAVLink v2 traffic, localhost UDP 14550 → 45177, SLL2 linktype.

## Method

### 1. Extract MAVLink frames
- Linktype 276 (SLL2) loopback capture. Wrote a manual `0xfd` (MAVLink v2) frame walker in Python (pymavlink's direct full-file parse hangs on the 74 MB stream).
- Forward stream (drone → GCS): `/tmp/s05.raw` (2,079,339 frames, 10 autopilot sysids 1–10). Reverse stream (GCS → drone): `/tmp/s05_rev.raw`.

### 2. Identify crashed drones
- Scanned `GLOBAL_POSITION_INT` (msgid 33) `relative_alt` per sysid. Only **sys2, sys3, sys5** hit the ground (`SIM Hit ground` + `Disarming motors` STATUSTEXTs). Others loitered at rel alt 50 m for the whole flight.
- sys2/3/5 crash points (last GPS before ground):
  - sys2: `36.0926140, -115.2428720`
  - sys3: `36.0778777, -115.2452151`
  - sys5: `36.0996908, -115.2489917`

### 3. Triangulate the jammer (omnidirectional antenna model)
- Hint 22 purchased: *"A jammer - assume an omnidirectional antenna model."*
- An omnidirectional jammer engulfs the drone's hover point once the drone is within its effective radius → all crash points are **exactly equidistant** from the jammer.
- Circumcenter of the 3 crash points:
  - **Center: `36.0871154, -115.2618174`**
  - **Radius: 1811.8 m** — all 3 crash points at *exactly* 1811.8 m (validates the model).

### 4. Identify the landmark at the jammer location
- Nominatim reverse: `5601 South Buffalo Drive, Spring Valley, NV 89113`.
- OSM Overpass `nwr(around:300)` nearest named feature: **Echo Trail Park** (leisure=park, polygon lat `36.0851128..36.0886809`, lon `-115.2655450..-115.2611819`) — the circumcenter lies **inside** the park polygon.
- Confirmed real park: **5655 Buffalo Dr, Las Vegas, NV 89113**, corner of Buffalo Dr & Russell Rd, opened March 2022 (playground, splash pad, tennis court, walking trail).
- Satellite tile (ESRI World Imagery, z17) at the center shows undeveloped desert/parkland — consistent.

## Flag
`starpwn{Echo_Trail_Park}`

## Notes
- Reverse stream contained a 232-frame repeated `COMMAND_LONG` (msgid 76) from GCS (255/230) with a mysterious float payload — not needed for the flag (appears to be a red herring or unparseable GCS command).
- Hint 23 only confirmed MAVLink needs a dedicated Wireshark dissector (already parsed manually).
- pymavlink direct parse of full raw stream hangs; extract single-msgid streams first, or use the manual frame walker.

## Scripts
| Script | Purpose | Status |
|--------|---------|--------|
| s05_fall2.py | Find first GPS frame with rel_alt < 40 m per crashed drone | Used |
| jam_circum.py | Circumcenter of crash points + radius check | Used |
| jam_verify.py / jam_geo5.py / jam_poi9.py | Reverse geocode + OSM POI queries | Used |
| s05_crashtext.py | Find "Hit ground" STATUSTEXTs | Used |
| s05_descstart.py | Confirm descent-start == crash point | Used |
