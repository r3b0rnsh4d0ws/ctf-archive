# STARPWN 2026 — Silent Horizon (Forensics, 500)

**Re-host:** SGC 2026 "Mission Silent Horizon" (Cal Poly CCI / James Pavur, Henry Danielson, Rob Randle) — satellite-constellation forensics.

**Flag:** `STARPWN{450:SAT1211SAT1111SAT1303SAT1207}`

## Files
- `SilentHorizonContsellation.vdf` — STK scenario file (gzip) with 36 CubeSats + 1, 60-s ephemeris (24 Apr 2026 20:00:00 UTC → 25 Apr 00:00:00 UTC)
- `Access Reports/GCS1..4.txt` — all access windows (GCS→satellite) for the 4-hour window
- `Ground Station Infection Times.txt` — when each GCS was compromised
- `STK_Viewer_v12.6.0.exe` — the intended GUI (Windows-only)

## Intended Method (report lookups)
Each GCS was infected while a satellite was **connecting** to it. Find, per GCS, the access window that contains the infection time:

| GCS (facility) | Infection (UTC) | Satellite connecting | Reported access |
|---|---|---|---|
| GCS1 Goldstone (35.23N, 116.53W) | 20:16:20 | **CubeSat1211** | 20:15:53.358–20:24:35.695 (start 26.6 s before) |
| GCS2 Canberra (35.40S, 148.98E) | 20:25:30 | **CubeSat1303** | 20:25:14.863–20:33:27.062 (start 15.1 s before) |
| GCS3 Madrid (40.25N, 4.24W) | 20:52:30 | **CubeSat1111** | 20:50:19.402–20:53:11.506 (only access in ±3 min) |
| GCS4 South Pole (90S) | 23:18:50 | **CubeSat1207** | 23:18:33.966–23:28:12.607 (start 16.0 s before) |

Flag template pins the order: `SAT12XX SAT11XX SAT13XX 12XX` → 1211, 1111, 1303, 1207.

## Validation (independent ephemeris model)
- VDF is gzip text; parsed all 37 `BEGIN Satellite` blocks.
- Epoch JD 2461155.3333 = 24 Apr 2026 20:00:00 UTC confirmed; GMST0 = 152.86035759514198°.
- ECI→ECEF rotation by `theta = GMST0 + 360.98564736629 * t/86400`; WGS84 GCS ECEF; elevation from sin of topocentric angle.
- Recomputed every pass (0° mask): all reported accesses match within ≤40 s EXCEPT two **fabricated** entries with no computed pass:
  - `GCS1→CubeSat1111` t=41930.9–42010.0 s (25 Apr 07:38:50.9–07:40:09.9, dur 79 s)
  - `GCS3→CubeSat1207` t=69783.0–69828.9 s (25 Apr 15:23:02.9–15:24:08.9)
- These two fakes are exactly what the README describes: "once infected, satellites transmitted randomized access times to ground stations" — they independently confirm 1111 and 1207 as infected.
- Only satellites 1111 and 1207 exceed normal delta (~40 s max, e.g. CubeSat1105 39.7 s); 1211/1303 match everywhere (their infections left no detectable forged pass).

## Lessons
- STK VDF files are plain gzip text — no STK license needed to analyze.
- Intended solution is pure report cross-referencing (high-school CTF); a full ephemeris model is overkill but cross-validates.
- "450:" prefix is the constellation orbital altitude (450 km) flavor.
- Description example IDs (1108, 1208, **1303**, **1207**) randomly but conveniently include two real answers.
