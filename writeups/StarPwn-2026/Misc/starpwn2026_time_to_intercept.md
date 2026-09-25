# STARPWN 2026 — Time to Intercept (Space Operations, 497 pts)

## Summary
Hohmann transfer rendezvous behind a TCP shell (application_target). Given your circular orbit altitude,
target altitude, and current phase angle, submit `delta_v_burn wait_time`. Tolerances ±10 m/s on Δv,
±60 s on wait time. 5 attempts per connection, randomized scenario per connection.

## Solution formulas
```
r1 = 6371e3 + h1*1e3;  r2 = 6371e3 + h2*1e3     (R_earth = 6371 km, confirmed by banner radii)
a = (r1 + r2)/2
Δv1 = sqrt(μ*(2/r1 - 1/a)) - sqrt(μ/r1)          # injection burn, positive (target higher)
t_transfer = π*sqrt(a³/μ)
n1 = sqrt(μ/r1³);  n2 = sqrt(μ/r2³)
τ = (π - φ - n2*t_transfer) / (n1 - n2)  mod  2π/(n1-n2), made positive
```
μ = 3.986004418e14 (server actually uses ~3.98589e14, backed out from printed v; both within tolerance).

## Key gotcha
Phase-angle sign convention. First attempt with `τ = (φ + n2·t - π)/Δn` gave 13147 s (wrong); server
required 47628 s = the complementary formula `(π - φ - n2·t)/Δn mod cycle`. The failure response
PRINTS "Required wait time" — a free oracle to pin the convention.
Verified: formula reproduces server's required τ to 0.03 s; actual solve errors: Δv 0.001 m/s, τ 0.197 s.

## Connection mechanism (application_target)
`POST /services/deploy?challenge_id=19` with `CSRF-Token: <csrfNonce>` header →
`{"targets":[{"info":"://0.cloud.chals.io:19380"}]}` → `nc 0.cloud.chals.io 19380`.

## Flag
`STARPWN{h0hm4nn_tr4nsf3r_1nt3rc3pt}`

## Solver
`solve_intercept.py` in challenge folder — parse h1/h2/phase, compute, send, extract flag.
