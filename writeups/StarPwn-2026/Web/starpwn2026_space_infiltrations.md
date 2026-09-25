# Space Infiltrations — STARPWN 2026 (Ground Operations)

## Summary
Uploaded a malicious "golden image" (patched telemetry status generator) to a satellite ground station, triggered a Power-On Reset over the command API, and exfiltrated the satellite's `/opt/flag.txt` through the status telemetry downlink.

**Flag:** `STARPWN{9de48ee5d75bd14b45e48948f5b74914}`

## Target
- YeetSat Inc. Ground Station: `https://<host>/`
- Endpoints: `GET /api/status`, `POST /api/command`, `POST /upload/goldenimage`, `GET /download/goldenimage`, `GET /download/picture`

## Steps
1. **Analyze the golden image** (`/download/goldenimage` zip): `status-generator.py` reads status files from `/opt/` and downlinks them; on the satellite it uses `nasa_cfs_api`; the golden image is installed to `/opt/` on reboot (Power-On Reset boots from it). Flag lives at `/opt/flag.txt` on the satellite.
2. **Extract exact command payloads from gs.js** — earlier "Unknown command" failures were payload-format mistakes:
   - `CFE ES Reset` with `{"reset_type":"Power-On Reset"}` (this is the reboot trigger)
   - Others: ADCS Set Momentum Management (`mode`), EPS Modify Payload Power (`voltage` int 0–25), Take Picture (`{}` → `/download/picture`, a red-herring black starfield PNG).
3. **Build evil golden image** (small flat zip via python zipfile — full 7MB re-zips got HTTP 500):
   - `status-generator.py` replaced: reads `/opt/flag.txt` (+ candidates), dumps secret env vars, lists `/opt` and `/`, prints `EVIL_STATUS|...` then `Functioning Normally`.
   - Keep original status txt files + README.md.
4. **Upload** `POST /upload/goldenimage` (multipart file) → `?upload_success=1`.
5. **Trigger reboot** `POST /api/command` `{"command":"CFE ES Reset","options":{"reset_type":"Power-On Reset"}}` → `success:true`.
6. **Poll `GET /api/status`** every 10s: `COMMS LOST` → `Restored from Golden Image` → `EVIL_STATUS|FILE[/opt/flag.txt]=STARPWN{...}`.

## Technique: malicious flight-image uplink
1. Download the pristine golden image package (it documents install paths and boot semantics).
2. Patch the "status generator" script (the piece executed on the target) to read the flag file + env and print it in the downlink format.
3. Keep the package structure identical; zip flat with python `zipfile` (re-packing the whole tree with Compress-Archive breaks the upload → 500).
4. Uplink, then issue the reset/power-cycle command that makes the target boot the new image.
5. Read the flag from the telemetry/status channel.
