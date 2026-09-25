# STARPWN 2026 — Tumbling Through Space (Space Operations, 496 pts)

## Summary
Satellite detumbling physics challenge behind a TCP shell (application_target). Given inertia tensor
diagonals (Ixx,Iyy,Izz) and angular velocities (ωx,ωy,ωz), submit `Tx Ty Tz duration` to bring |ω| < 0.01 rad/s.
Torque magnitude capped at 1.0 N·m, duration ≤ 100 s, 5 attempts per connection.

## Key insight
The server simulates the **simplified linear attitude model** `dL/dt = T` (NO gyroscopic term ω×L).
One constant body-frame torque burn `T = -L/d` exactly cancels the angular momentum L = I·ω over duration d.
Gotcha: the magnitude cap check is strict — computing |T| = 1.0 gets rejected from float rounding;
use margin 0.95.

## Solution
```
L = (Ixx·ωx, Iyy·ωy, Izz·ωz)
d = |L| / 0.95
T = -L / d          # |T| = 0.95 < 1.0 cap
send(f"{Tx} {Ty} {Tz} {d}")
```
Result on probe: |ω| 0.503 → 0.00312 < 0.01 → SUCCESS with flag.

## Connection mechanism (application_target)
- Challenge modal JS uses `window.challenge.launch()` → `POST /services/deploy?challenge_id=<id>`
- Requires `CSRF-Token: <csrfNonce>` header (nonce from page HTML `window.init.csrfNonce`)
- Response: `{"targets":[{"info":"://0.cloud.chals.io:23524","label":null}]}` → `nc 0.cloud.chals.io 23524`

## Flag
`STARPWN{d3tumbl3_m4st3r_sp4c3_0p5}`

## Solver
`solve_tumble.py` in challenge folder — parse banner floats, compute, send, extract flag.
