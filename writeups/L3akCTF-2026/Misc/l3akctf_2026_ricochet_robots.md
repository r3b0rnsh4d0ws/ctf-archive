# L3akCTF 2026 — Ricochet Robots (KoTH, misc)

**Files:** handout.zip → `game.py`, `sandbox.py`, `Dockerfile` (pwn.red/jail, python:3.14-slim)
**Flag:** none (KoTH — score via leaderboard). Deliverable = competitive solver.
**Full artifacts:** `D:\CTF\ctfs\0_l3akctf\misc\1_ricochet_robots\` (solve/, handout/, progress.md)

## Summary
KoTH speed challenge: submit Python source; per round the server execs it in a jail with a
6-byte game state in scope; code prints Ricochet Robots moves; server validates each move
against the real game and times the round-trip.

## Key insight
`Game.__init__` hardcodes robots at fixed `START`; only the target varies (17 possible).
⇒ Precompute optimal solutions offline (BFS), embed as a lookup table → O(1) per round
(~1.5-2.6 ms round-trip, dominated by jail Python startup). BFS fallback (1M-state budget)
covers any non-START state.

## Techniques
- BFS over 32-bit packed states with precomputed `nxt[pos][dir]` slide tables and a
  bytearray occupancy grid (~350k states/sec).
- Win check mirrors reference: non-wild = specific robot nibble == target; wild = any robot.
- No-op moves skipped (illegal in game). Budget cap keeps exec inside jail limits.
- Lookup table keyed `(target_robot_idx|4, target_pos)` with START-position gate.

## Verification
3-layer local test against handout code: in-process exec (17/17 targets), random-state BFS
(valid winning solutions, budget-capped), full socket round-trip incl. real sandbox.py
(17/17 wins, 8/8 random). Edge: already-won → `''` is valid.

## Gotchas
- Emitted `START_POS=1,2,3,4` (no brackets) → tuple → `list == tuple` False → lookup
  silently disabled. Fix: brackets + test the generated code.
- Handout `run_solution` has typo `g.make_move()` (no arg); live server passes the move.
- Port 4000 excluded on Windows (10013) → parameterized local test port.

## Authoring notes
Fixed board/start + random target + speed scoring makes precomputation the intended winning
strategy; 6-byte state, hex code transport, host-side move validation prevent jail cheating.
